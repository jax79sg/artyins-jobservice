# Import libraries
import os
import sys
import random
import math
import re
import time
import logging
import argparse
import json
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request
import requests

# Root directory of the project
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library

# Logging confg
logging.basicConfig(level=logging.DEBUG, filename="log", filemode="a+",
                format="%(asctime)-15s %(levelname)-8s %(message)s")

############################################################
#  Configurations
#  Inherits from config.py
############################################################
from config import JobConfig
config = JobConfig()

# Create model object in inference mode.

def extractContent(data):
    data = None #Preprocess the data
    r = requests.post(url = config.EXTRACTION_URL, json  = DATA)
    results = r.json()
    return results['data']

def inferContent(data):
    data = None #Preprocess the data
    r = requests.post(url = config.INFERENCE_URL, json  = DATA)
    results = r.json()
    return results['data']
  
def saveContent(data):
    data = None #Preprocess the data
    r = requests.post(url = config.SAVE_URL, json  = DATA)
    results = r.json()
    return results['data']
 

def run_create_new_job(data):
    #Expects 
    # path,filename,datetimesubmitted,reporttype
    logging.info('Loading data: %s', data)
    extractedContent=extractContent(data)
    inferredContent=inferContent(extractedContent)
    savedContent=saveContent(inferredContent)
    return 0

# Instantiate the Node
app = Flask(__name__)

@app.route('/create_job', methods=['POST'])
def create_job_get():

    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_create_new_job(request_json)
        
        response_msg = json.dumps(result)
        response = {
            'message': response_msg
        }
        return jsonify(response), 200


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9898, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, debug=True)
