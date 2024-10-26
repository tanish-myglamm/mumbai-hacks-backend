from flask import Blueprint, request, jsonify
from prompt_store import get_sales_strategy_prompt, get_product_list_prompt
from service import AzureOpenAIService
from scraper import scrape_website
from database import execute_query, load_data_from_csv
from urllib.parse import urlparse
import json
import os

routes = Blueprint('routes', __name__)
service = AzureOpenAIService()

@routes.route('/get-strategy', methods=['POST'])
def get_strategy():
    data = request.json
    website = data.get('website')
    month = data.get('month')
    category_selected = data.get('category_selected')

    if not all([website, month, category_selected]):
        return jsonify({"error": "Missing required fields"}), 400

    # Fetch events from the database
    query = "SELECT * FROM festivities_event WHERE start_date LIKE ?"
    query_with_params = query.replace("?", f"'{month[:7]}%'")
    events = execute_query(query_with_params)

    prompt = get_sales_strategy_prompt(website, month, category_selected, events)
    llm_answer = service.get_llm_response(prompt)
    llm_answer = llm_answer.replace("```json","")
    llm_answer = llm_answer.replace("```","")
    print("llm_answer", llm_answer)
    strategy = json.loads(llm_answer)
    return jsonify({"strategy": strategy})

@routes.route('/get-product-list', methods=['POST'])
def get_product_list():
    data = request.json
    domain = data.get('domain')

    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain

    parsed_url = urlparse(domain)
    if not parsed_url.netloc:
        return jsonify({"error": "Invalid domain"}), 400

    scraped_data = scrape_website(domain)
    formatted_prompt = get_product_list_prompt(scraped_data)
    llm_answer = service.get_llm_response(formatted_prompt)
    llm_answer = llm_answer.replace("```json","")
    llm_answer = llm_answer.replace("```","")
    # product_list = json.loads(llm_answer)

    return jsonify(json.loads(llm_answer))

@routes.route('/execute-query', methods=['POST'])
def execute_sql_query():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        results = execute_query(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join('/tmp', file.filename)
        file.save(filepath)
        try:
            load_data_from_csv(filepath)
            return jsonify({"success": "Data loaded successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type, only CSV allowed"}), 400