from flask import Blueprint, jsonify, request
import logging
from executor import get_agent_executor
import os

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize agent executor
analyst_agent_openai = get_agent_executor(OPENAI_API_KEY)


@main_bp.route('/api/v1/chat', methods=['POST'])
def index():
    data = request.json
    response = {
        "data" : None,
        "error" : None
    }
    statusCode = 404
    try:
        logging.info(f"data: {data}")
        message = data['message']
        answer = analyst_agent_openai.run(message)

        logging.info(f"response: {answer}")
        response["data"] = answer
        statusCode = 200
    except Exception as error:
        logging.error(error)
        response['error'] = {
        'message': f"{error}"
        }
        statusCode = 404
    return jsonify(response), statusCode
