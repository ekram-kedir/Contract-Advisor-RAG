import datetime
from langchain.memory import ChatMessageHistory
from flask import Blueprint, jsonify, request
import logging, os
from dotenv import load_dotenv
from executor import get_agent_executor

# Initialize Flask Blueprint
main_bp = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize chat message history
history = ChatMessageHistory()

#load API key from environment
load_dotenv()
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

# Define API endpoint for handling chat requests
@main_bp.route('/api/v1/chat', methods=['POST'])
def index():
    """
    Handles incoming chat requests and processes user messages through the agent.

    Returns:
        JSON response containing the processed chat response and metadata.

    Raises:
        Exception: If errors occur during request processing, message execution, or response generation.
    """

    data = request.get_json()
    response = {
        "isSuccess": False,
        "value": {
            "text":None,
            "timestamp": None
        },
        "error": None
    }
    status_code = 404

    try:
        # Validate request data
        if not data:
            raise Exception("Invalid request: Missing JSON data")

        # Extract user message
        user_message = data.get("message")
        if not user_message:
            raise Exception("Invalid request: Missing message field")

        # Add user message to chat history
        history.add_user_message((user_message, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # Get current timestamp and set sender information
        response["value"]["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response["value"]["sender"] = "user"

        # Get agent from executor and process user message
        agent = get_agent_executor(COHERE_API_KEY)
        answer = agent(user_message)["output"]
        print(answer)
        history.add_ai_message((answer, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logging.info(f"Agent response: {answer}")

        # Update response with output and sender information
        response["value"]["text"] = answer
        response["value"]["sender"] = "system"
        status_code = 200

    except Exception as error:
        logging.error(error)
        response["error"] = {
            "message": str(error)
        }

    return jsonify(response), status_code


# API endpoint for retrieving chat messages
@main_bp.route('/api/v1/messages', methods=['GET'])
def get_messages():
    """
    Retrieves and returns the chat message history.

    Returns:
        JSON response containing the list of chat messages.

    Raises:
        Exception: If errors occur during message retrieval.
    """

    try:
        messages = []
        for message in history.messages:
            messages.append({
                "type": type(message).__name__,
                "content": message.content,
            })
        return jsonify(messages), 200

    except Exception as e:
        logging.error(f"Error retrieving chat messages: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
