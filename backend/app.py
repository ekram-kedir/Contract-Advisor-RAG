import logging
import os,sys
import pandas as pd
import numpy as np
from flask import Flask
from flask_cors import CORS
from langchain_community.document_loaders import TextLoader
from flask import Flask, request, jsonify
rpath = os.path.abspath('./../../')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from rag.utility.finalResponse import generalResponse

app = Flask(__name__)
CORS(app) 
@app.route('/')
def home():
    return "Welcome to the Prompt Generation System!"

# template of what the api should look like
@app.route('/api/chat', methods=['POST'])
def submit_task():
    try:
        question = request.get_json()
        answer_df = generalResponse(question)

        # Convert DataFrame to list of dictionaries
        generated_prompts_list = answer_df.applymap(lambda x: x.tolist() if isinstance(x, np.ndarray) else x).to_dict(orient='records')

        response = {
            'status': 'success',
            'message': 'Task submitted successfully',
            'generated_prompts': generated_prompts_list
        }

        return jsonify(response)

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'status': 'error', 'message': str(e)})