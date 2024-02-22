# from flask import Blueprint, jsonify, request
# import logging

# import numpy as np
# from pandas import array

# from rag_utils import  get_generated_prompt_with_evaulation

# main_bp = Blueprint('main', __name__)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# @main_bp.route('/api/v1/chat', methods=['POST'])
# def index():
#     response = {
#         "data" : None,
#         "error" : None
#     }
#     statusCode = 404
#     try:
#         question = request.json.get('question')
#         # answer = get_generated_prompt_with_evaulation(question)

#         answer =  [
#     [
#       "question",
#       "answer",
#       "contexts",
#       "ground_truths",
#       "context_precision",
#       "context_recall",
#       "faithfulness",
#       "answer_relevancy"
#     ],
#     [
#       "What project did OpenAI use to showcase the capabilities of reinforcement learning algorithms?",
#       "OpenAI used the 'OpenAI Five' project to showcase the capabilities of reinforcement learning algorithms.",
#       [
#         "OpenAI showcased the capabilities of these reinforcement learning algorithms through its ‘OpenAI Five’ \nproject in 2018, which trained five independent AI agents to play a complex multiplayer online battle \narena game called ‘Dota 2’. Despite operating independently, these agents learned to work as a cohesive \nteam to coordinate strategies within the game.",
#         "The early years of OpenAI were marked with rapid experimentation. The company made significant progress \non research in deep learning and reinforcement learning, and released ‘OpenAI Gym’ in 2016, a toolkit \nfor developing and comparing reinforcement learning algorithms.",
#         "OpenAI was initially founded in 2015 by Sam Altman, Elon Musk, Ilya Sutskever and Greg Brockman as a \nnon-profit organization with the stated goal to “advance digital intelligence in the way that is most \nlikely to benefit humanity as a whole.” The company assembled a team of the best researchers in the \nfield of AI to pursue the goal of building AGI in a safe way."
#       ],
#       [
#         "OpenAI Five"
#       ],
#       0.99999999995,
#       1.0,
#       1.0,
#       1.0
#     ],
#     [
#       "When was OpenAI founded?",
#       "OpenAI was founded in 2015.",
#       [
#         "The early years of OpenAI were marked with rapid experimentation. The company made significant progress \non research in deep learning and reinforcement learning, and released ‘OpenAI Gym’ in 2016, a toolkit \nfor developing and comparing reinforcement learning algorithms.",
#         "OpenAI was initially founded in 2015 by Sam Altman, Elon Musk, Ilya Sutskever and Greg Brockman as a \nnon-profit organization with the stated goal to “advance digital intelligence in the way that is most \nlikely to benefit humanity as a whole.” The company assembled a team of the best researchers in the \nfield of AI to pursue the goal of building AGI in a safe way.",
#         "OpenAI showcased the capabilities of these reinforcement learning algorithms through its ‘OpenAI Five’ \nproject in 2018, which trained five independent AI agents to play a complex multiplayer online battle \narena game called ‘Dota 2’. Despite operating independently, these agents learned to work as a cohesive \nteam to coordinate strategies within the game."
#       ],
#       [
#         "2015"
#       ],
#       0.49999999995,
#       1.0,
#       1.0,
#       0.9999999999999996
#     ],
#     [
#       "What is the goal of OpenAI?",
#       "The goal of OpenAI is to advance digital intelligence in a way that benefits humanity as a whole.",
#       [
#         "OpenAI was initially founded in 2015 by Sam Altman, Elon Musk, Ilya Sutskever and Greg Brockman as a \nnon-profit organization with the stated goal to “advance digital intelligence in the way that is most \nlikely to benefit humanity as a whole.” The company assembled a team of the best researchers in the \nfield of AI to pursue the goal of building AGI in a safe way.",
#         "The early years of OpenAI were marked with rapid experimentation. The company made significant progress \non research in deep learning and reinforcement learning, and released ‘OpenAI Gym’ in 2016, a toolkit \nfor developing and comparing reinforcement learning algorithms.",
#         "OpenAI showcased the capabilities of these reinforcement learning algorithms through its ‘OpenAI Five’ \nproject in 2018, which trained five independent AI agents to play a complex multiplayer online battle \narena game called ‘Dota 2’. Despite operating independently, these agents learned to work as a cohesive \nteam to coordinate strategies within the game."
#       ],
#       [
#         "To advance digital intelligence in a way that benefits humanity"
#       ],
#       0.9999999999,
#       1.0,
#       1.0,
#       0.9999999999999997
#     ],
#     [
#       "What toolkit did OpenAI release in 2016?",
#       "OpenAI released the 'OpenAI Gym' toolkit in 2016.",
#       [
#         "The early years of OpenAI were marked with rapid experimentation. The company made significant progress \non research in deep learning and reinforcement learning, and released ‘OpenAI Gym’ in 2016, a toolkit \nfor developing and comparing reinforcement learning algorithms.",
#         "OpenAI showcased the capabilities of these reinforcement learning algorithms through its ‘OpenAI Five’ \nproject in 2018, which trained five independent AI agents to play a complex multiplayer online battle \narena game called ‘Dota 2’. Despite operating independently, these agents learned to work as a cohesive \nteam to coordinate strategies within the game.",
#         "OpenAI was initially founded in 2015 by Sam Altman, Elon Musk, Ilya Sutskever and Greg Brockman as a \nnon-profit organization with the stated goal to “advance digital intelligence in the way that is most \nlikely to benefit humanity as a whole.” The company assembled a team of the best researchers in the \nfield of AI to pursue the goal of building AGI in a safe way."
#       ],
#       [
#         "OpenAI Gym"
#       ],
#       0.9999999999,
#       1.0,
#       1.0,
#       0.9253182918334986
#     ],
#     [
#       "What game did the AI agents trained by OpenAI play?",
#       "The AI agents trained by OpenAI played a game called 'Dota 2'.",
#       [
#         "OpenAI showcased the capabilities of these reinforcement learning algorithms through its ‘OpenAI Five’ \nproject in 2018, which trained five independent AI agents to play a complex multiplayer online battle \narena game called ‘Dota 2’. Despite operating independently, these agents learned to work as a cohesive \nteam to coordinate strategies within the game.",
#         "The early years of OpenAI were marked with rapid experimentation. The company made significant progress \non research in deep learning and reinforcement learning, and released ‘OpenAI Gym’ in 2016, a toolkit \nfor developing and comparing reinforcement learning algorithms.",
#         "OpenAI was initially founded in 2015 by Sam Altman, Elon Musk, Ilya Sutskever and Greg Brockman as a \nnon-profit organization with the stated goal to “advance digital intelligence in the way that is most \nlikely to benefit humanity as a whole.” The company assembled a team of the best researchers in the \nfield of AI to pursue the goal of building AGI in a safe way."
#       ],
#       [
#         "Dota 2"
#       ],
#       0.9999999999,
#       1.0,
#       1.0,
#       0.9999999999999988
#     ]
#   ]
       
#         print(f"answer: {answer}")

#         response["data"] = answer[1:]
#         statusCode = 200
                
#     except Exception as error:
#         logging.error(error)
#         response['error'] = {
#         'message': f"{error}"
#         }

#     return response, statusCode


from flask import Blueprint, jsonify, request
import json
import logging
import os
from exectuors import get_agent_executor

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

OPENAI_API_KEY="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"

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