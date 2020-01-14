[![Job Service](https://github.com/jax79sg/artyins-jobservice/raw/master/images/SoftwareArchitectureJobService.jpg)]()

# Job Service For artyins deployment architecture
This is a submodule for the artyins deployment architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-jobservice.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-jobservice)
[![Container Status](https://quay.io/repository/jax79sg/artyins-jobservice/status)](https://quay.io/repository/jax79sg/artyins-jobservice)

Refer to [Trello Task list](https://trello.com/c/k32yAwNL) for running tasks.

---

## Table of Contents

- [Usage](#Usage)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---

## Usage
This is a web API call to start a job. Each job will comprise of 3 actions, namely;
- Extract content of report
- For each content of report, infer the classification
- Save the information from above into database
The API call simply calls other APIs to fulfil the above.

The job service can be called by a HTTP POST call. Primarily on http://webserverip:port/create_job. It expects a json of the following format
```python
```

### config.py
The configuration will point to the URLs of the relevant APIs
```python
class JobConfig():
    EXTRACTION_URL='http://ipaddr/extractreport'
    INFERENCE_URL='http://ipaddr/infercontent'
    SAVE_URL='http://ipaddr/savecontent'
```

### Flask
The API calls are coded in Flask. Upon deployment, they should be supported by a production WSGI server.
```python
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
```
---

## Virtualenv
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt`
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-jobservice). You are required to write the necessary unit tests if you introduce more methods.
### Unit Tests
```python

```

### Web Service Test
```
#Start gunicorn wsgi server
gunicorn --bind 0.0.0.0:9898 --daemon --workers 1 wsgi:app
```
Send test POST request
```python
```

---

