from flask import Blueprint, request, jsonify
from prompt_store import get_sales_strategy_prompt, get_product_list_prompt
from service import AzureOpenAIService
import json

routes = Blueprint('routes', __name__)
service = AzureOpenAIService()

@routes.route('/get-sales-strategy', methods=['POST'])
def get_sales_strategy():
    data = request.json
    month = data.get('month')
    business_context = data.get('business_context')

    prompt = get_sales_strategy_prompt(month, business_context)
    llm_answer = service.get_llm_response(prompt)

    return jsonify({"strategy": llm_answer})

@routes.route('/get-product-list', methods=['POST'])
def get_product_list():
    data = request.json
    domain = data.get('domain')

    # Get the prompt for the product list
    user_message = get_product_list_prompt(domain)

    # Get the response from the Azure OpenAI service
    llm_answer = service.get_llm_response(user_message)

    # Assuming the response is already in JSON format
    try:
        product_list = json.loads(llm_answer)
    except json.JSONDecodeError:
        product_list = {"error": "Failed to parse product list"}

    return jsonify(product_list)