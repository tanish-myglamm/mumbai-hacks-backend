# routes.py

from flask import Blueprint, request, jsonify
from prompt_store import get_prompt
from service import AzureOpenAIService

routes = Blueprint('routes', __name__)
service = AzureOpenAIService()

@routes.route('/get-sales-strategy', methods=['POST'])
def get_sales_strategy():
    data = request.json
    month = data.get('month')
    business_context = data.get('business_context')

    prompt = get_prompt(month, business_context)
    llm_answer = service.get_llm_response(prompt)

    return jsonify({"strategy": llm_answer})