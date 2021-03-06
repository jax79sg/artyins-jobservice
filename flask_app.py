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
from config import JobConfig
# Root directory of the project
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library

config = JobConfig()
# Logging confg
logging.basicConfig(level=config.LOGGINGLEVEL,handlers=[
        logging.FileHandler("{0}/{1}.log".format("/logs", "jobsvc-flaskapp")),
        logging.StreamHandler()
    ] ,
                format="%(asctime)-15s %(levelname)-8s %(message)s")


# Create model object in inference mode.

def extractContent(data):
    logging.info("Preparing request for extract content")
    filelist=[]
    idcount=1
    for row in data:
       #logging.info("ROW is {} with type {}".format(row, type(row)))
       filelist.append({"filename":row["filename"],"id":idcount})
       idcount=idcount+1
    r = requests.post(url = config.EXTRACTION_URL, json  = filelist)
    results = r.json()
    logging.info("Extraction call completed")
    return results['results']

def inferContent(data):
    logging.info("Preparing request for inference")
    #logging.debug("DATA %s  TYPE %s", data, type(data))
    #Input: {"results":[{"filename":"file01.pdf","id":1,"section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"section":"observation","content":"kfsdfjsfsjhsd"}]}
    r = requests.post(url = config.INFERENCE_URL, json  = data)
    results = r.json()
    logging.info("Inference call completed")
    return results['results']
  
def saveContent(data):
    logging.info("Preparing request for saving")
    #logging.debug("DATA %s TYPE %s",data, type(data))
    if isinstance(data, str):
       logging.debug("data is not json dict, manually converting now")
       data=json.loads(data)
    r = requests.post(url = config.SAVE_URL, json  = data)
    results = r.json()
    logging.info("Saving call completed ")
    return results['results']
 
def mergejson(content1, content2):
    from pandas.io.json import json_normalize
    import pandas as pd
    logging.info("Merging results from Extraction and Inference")
    logging.debug("Extracted: %s with TYPE %s", content1, type(content1))
    logging.debug("Inferred: %s with TYPE %s", content2, type(content2))
    if isinstance(content1,str):
        logging.warn("Received content is not JSON obj, manually converting")
        content1 = json.loads(content1)
    if isinstance(content2, str):
        logging.warn("Received conetnt is not JSON obj, manually converting")
        content2 = json.loads(content2)
    c1=json_normalize(content1)
    c2=json_normalize(content2)
    merged_inner = pd.merge(left=c1,right=c2, left_on='id', right_on='id')
    logging.info("Merging completed")
    #logging.info("Merging complete %s",merged_inner.to_json(orient='records'))
    return merged_inner.to_json(orient='records')

def run_create_new_job(data):
    results="ok"
    try:
       logging.info("Starting job run")
       logging.debug('Loading data: %s', data)
       #eats [{"filename":"file01.pdf",},{"filename":"file02.pdf"}]
       extractedContent=extractContent(data)
       #vomits {"results":[{"filename":"file01.pdf","id":1,"section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"section":"observation","content":"kfsdfjsfsjhsd"}]}
       logging.debug("extraction vomitted: %s",str(extractedContent))
       #eats [{"id":1,"content":"adfsfswjhrafkf"},{"id":2,"content":"kfsdfjsfsjhsd"}]
       inferredContent=inferContent(extractedContent)
       logging.debug("Inference vomitted: %s",str(inferredContent))
       #vomits {"results":[{"id":1,"class":"DOCTRINE"},{"id":2,"class":"DOCTRINE"}]}

       mergedresult=mergejson(extractedContent,inferredContent)
       #vomits [{"filename":"file01.pdf","id":1,"class":"DOCTRINE","section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"class":"DOCTRINE","section":"observation","content":"kfsdfjsfsjhsd"}]}    
       logging.debug("merge vomitted: %s", str(mergedresult))
       #eats above vomit
       savedContent=saveContent(mergedresult)
       logging.debug("save vomitted: %s", str(savedContent))
       #vomits failed products [{"filename":"file01.pdf","id":1,"error":"report already exists"},{"filename":"file01.pdf","id":2,"results":"Some SQL problems, check logs"}]
       #If vomit is "ok", then no probles.
       savedContent=json.loads(savedContent)
       if len(savedContent["failreports"])>0:
          results="nok"
       #For those that fail, do 
       # Extract the report filenames that failed, send failed to monitor service who will move filename from processing to failed.
       # Extract the report filenames that passes, send passed to monitor service who will move filename from processing to succeed
    except Exception as  e:
       logging.error(str(e))
       results="nok"
    
    return results

# Instantiate the Node
app = Flask(__name__)

@app.route('/create_job', methods=['POST'])
def create_job_get():
    logging.info("Received CREATEJOB call")
    if request.method == 'POST':
        logging.debug("Getting json info")
        request_json = request.get_json(force=True)
        result = run_create_new_job(request_json)
        logging.debug("Dumping results back to caller")
        response_msg = json.dumps(result)
        response = {
            'results': response_msg
        }
        logging.info("Job call completed")
        return jsonify(response), 200

@app.route('/test',methods=['GET'])
def test_get():
    logging.info("Version 0.10")
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
