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
logging.basicConfig(level=logging.DEBUG,handlers=[
        logging.FileHandler("{0}/{1}.log".format(".", "log")),
        logging.StreamHandler()
    ] ,
                format="%(asctime)-15s %(levelname)-8s %(message)s")

############################################################
#  Configurations
#  Inherits from config.py
############################################################
from config import JobConfig
config = JobConfig()

# Create model object in inference mode.

def extractContent(data):
    filelist=[]
    idcount=1
    for row in data:
       filelist.append({"filename":row["filename"],"id":idcount})
       idcount=idcount+1
    r = requests.post(url = config.EXTRACTION_URL, json  = json.dumps(filelist))
    results = r.json()
    return results['results']

def inferContent(data):
    #Input: {"results":[{"filename":"file01.pdf","id":1,"section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"section":"observation","content":"kfsdfjsfsjhsd"}]}
    r = requests.post(url = config.INFERENCE_URL, json  = DATA)
    results = r.json()
    return results['results']
  
def saveContent(data):
    r = requests.post(url = config.SAVE_URL, json  = DATA)
    results = r.json()
    return results['results']
 
def mergejson(content1, content2):
    from pandas.io.json import json_normalize
    import pandas as pd
    #c1=json_normalize(data[content1)
    #c2=json_normalize(data[content2)
    merged_inner = pd.merge(left=content1,right=content2, left_on='id', right_on='id')
    return merged_inner.to_json(orient='records')

def run_create_new_job(data):
    logging.info('Loading data: %s', data)
    #eats [{"filename":"file01.pdf",},{"filename":"file02.pdf"}]
    extractedContent=extractContent(data)
    #vomits {"results":[{"filename":"file01.pdf","id":1,"section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"section":"observation","content":"kfsdfjsfsjhsd"}]}
    
    #eats [{"id":1,"content":"adfsfswjhrafkf"},{"id":2,"content":"kfsdfjsfsjhsd"}]
    inferredContent=inferContent(extractedContent)
    #vomits {"results":[{"id":1,"class":"DOCTRINE"},{"id":2,"class":"DOCTRINE"}]}

    mergedresult=mergejson(extractedContent,inferredContent)
    #vomits [{"filename":"file01.pdf","id":1,"class":"DOCTRINE","section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"class":"DOCTRINE","section":"observation","content":"kfsdfjsfsjhsd"}]}    

    #eats above vomit
    savedContent=saveContent(inferredContent)
    #vomits failed products [{"filename":"file01.pdf","id":1,"error":"report already exists"},{"filename":"file01.pdf","id":2,"results":"Some SQL problems, check logs"}]
    #If vomit is "ok", then no probles.

    #For those that fail, do 
    # Extract the report filenames that failed, send failed to monitor service who will move filename from processing to failed.
    # Extract the report filenames that passes, send passed to monitor service who will move filename from processing to succeed
    
    
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

@app.route('/test',methods=['GET'])
def test_get():
    response = {
        'message':'ok'
    }
    return jsonify(response), 200

if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9898, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, debug=True)
