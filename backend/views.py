# from flask import Blueprint, jsonify, request
# import logging
# from executor import get_agent_executor
# import os
# from dotenv import load_dotenv

# load_dotenv()
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# # Initialize agent executor
# analyst_agent_openai = get_agent_executor(OPENAI_API_KEY)


# @main_bp.route('/api/v1/chat', methods=['POST'])
# def index():
#     data = request.json
#     response = {
#         "data" : None,
#         "error" : None
#     }
#     statusCode = 404
#     try:
#         logging.info(f"data: {data}")
#         message = data['message']
#         answer = analyst_agent_openai.run(message)

#         logging.info(f"response: {answer}")
#         response["data"] = answer
#         statusCode = 200
#     except Exception as error:
#         logging.error(error)
#         response['error'] = {
#         'message': f"{error}"
#         }
#         statusCode = 404
#     return jsonify(response), statusCode
from flask import Flask, app, request, jsonify, Blueprint
import datetime
import logging
from utils import get_postgres_data
import os
from dotenv import load_dotenv
from executor import get_agent_executor

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
OPENAI_API_KEY ="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"
print(OPENAI_API_KEY)
analyst_agent_openai = get_agent_executor(OPENAI_API_KEY)
# # @main_bp.route('/api/v1/chat', methods=['POST'])

# @main_bp.route('/api/v1/chat', methods=['POST'])
# def index():
#     data = request.json
#     response = {
#         "isSuccess": False,
#         "value": {
#             "text": None,
#             "timestamp": None
#         },
#         "error": None
#     }
#     statusCode = 404
#     try:
#         # Extract message and sender from request
#         user_message = data['message']
#         sender = "user"  # Assuming the sender is the user
        
#         # Get current timestamp
#         response["value"]["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Save message to the database
#         answer = analyst_agent_openai.run(user_message)

#         logging.info(f"response: {answer}")
#         response["value"]["text"]= answer
#         statusCode = 200
#         sender = "system"  # Assuming the sender is the user
        
#         # Get current timestamp
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Save message to the database        
#         # Prepare the response
#     except Exception as error:
#         logging.error(error)
#         response['error'] = {
#             'message': f"{error}"
#         }
#     return jsonify(response), statusCode

# @main_bp.route('/api/v1/messages', methods=['GET'])
# def get_messages():
#     response = {
#         "data": None,
#         "error": None
#     }
#     statusCode = 404
#     try:
#         # Query all messages from the database
#         query = "SELECT * FROM messages"
#         messages, _ = get_postgres_data(query)
        
#         # Prepare the response
#         response["data"] = messages
#         statusCode = 200
#     except Exception as error:
#         logging.error(error)
#         response['error'] = {
#             'message': f"{error}"
#         }
#     return jsonify(response), statusCode

# def save_message_to_database(sender, timestamp, message):
#     query = f"INSERT INTO messages (sender, timestamp, text) VALUES ('{sender}', '{timestamp}', '{message}')"
#     try:
#         get_postgres_data(query)
#     except Exception as e:
#         logging.error(f"Error saving message to database: {e}")
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

app = Flask(__name__)

@main_bp.route('/api/v1/chat', methods=['POST'])
def index():
    data = request.json
    response = {
        "isSuccess": False,
        "value": {
            "text": None,
            "timestamp": None
        },
        "error": None
    }
    statusCode = 404
    try:
        user_message = data['message']
        history.add_user_message((user_message, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Get current timestamp
        response["value"]["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response["value"]["sender"]= "user"
        # Save message to the database
        # answer = analyst_agent_openai.run(user_message)
        answer="i love you and you strong"
        history.add_ai_message((answer, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logging.info(f"response: {answer}")
        response["value"]["text"]= answer
        response["value"]["sender"]= "system"
        statusCode = 200
        sender = "system"  # Assuming the sender is the user
        
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save message to the database        
        # Prepare the response
    except Exception as error:
        logging.error(error)
        response['error'] = {
            'message': f"{error}"
        }
    return jsonify(response), statusCode

            
@main_bp.route('/api/v1/messages', methods=['GET'])
def get_messages():
    try:
        response = []
        for message in history.messages:
            response.append({
                'type': type(message).__name__,
                'content': message.content,
            })
        return jsonify(response),200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500