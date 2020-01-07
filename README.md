[![Classifier Service](https://github.com/jax79sg/artyins-classifierservice/raw/master/images/SoftwareArchitectureClassifierService.jpg)]()

# Classifier Service For artyins deployment architecture
This is a submodule for the artyins architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-classifierservice.svg?token=BREzYzgtHGHQp4of21Xp&branch=master)](https://travis-ci.com/jax79sg/artyins-classifierservice)

Refer to [Trello Task list](https://trello.com/c/qlDHKzBN) for running tasks.

---

## Table of Contents (Optional)

- [Usage](#Usage)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---

## Usage
All model inferencing classes needs to implement the abstract Model class from score/model.py. An example is created in score/testmodel.py. All configuration should be set in config.py. Finally, add your model into the web service flask_app.py. Contributors, please ensure that you add your test codes into test.py (See [Tests] before you push to master branch.)

### config.py
```python
class InferenceConfig():
    GPU_COUNT = 1
    
    MODEL_SAMPLE_INPUT=dict(sepal_length=1.0,sepal_width=2.2,petal_length=3.3,petal_width=4.4)
    MODEL_MODULE="score.testmodel"
    MODEL_CLASS="IrisSVCModel"
    MODEL_DIR = "model_files"
    MODEL_FILE = "svc_iris_model.pickle"

```

### Abstract Model Class
```python
from abc import ABC, abstractmethod
from schema import Schema
class ModelReport(ABC):
    """  An abstract base class for ML model prediction code """
    @property
    @abstractmethod
    def input_dataschema(self):
        Schema({'sentence': str})

    @property
    @abstractmethod
    def output_dataschema(self):
        Schema({'category': And(str,lambda s: s in ('doctrine', 'training','personnel'))
               ,'prob': And(float,lambda n: 0 <= n <= 100)})

    @abstractmethod
    #Implement the loading of model file here
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, data):
        self.input_dataschema.validate(data)
```

### An example on how to implement the Abstract model class
```python
from score.model import ModelReport
from schema import Schema
from schema import Or
import os
import numpy as np
from config import InferenceConfig
import pickle
class IrisSVCModel(ModelReport):
    # Note that this is overridden cos the one defined is meant for Keng On's use case 
    input_dataschema = Schema({'sepal_length': float,
                           'sepal_width': float,
                           'petal_length': float,
                           'petal_width': float})
    # Note that this is overriden cos the one defined is meant for Keng On's use case
    output_dataschema = Schema({'species': Or("setosa", 
                                          "versicolor", 
                                          "virginica")})
    def __init__(self,config=None):
        if config == None:
           config = InferenceConfig() 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file = open(os.path.join(dir_path, config.MODEL_DIR, config.MODEL_FILE), 'rb')
        self._svm_model = pickle.load(file)
        file.close()

    def predict(self, mydata):
        # calling the super method to validate against the
        # input_schema
        super().predict(data=mydata)
        # converting the incoming dictionary into a numpy array 
        # that can be accepted by the scikit-learn model
        X = np.array([mydata["sepal_length"], 
                   mydata["sepal_width"], 
                   mydata["petal_length"],
                   mydata["petal_width"]]).reshape(1, -1)
        # making the prediction 
        y_hat = int(self._svm_model.predict(X)[0])
        # converting the prediction into a string that will match 
        # the output schema of the model, this list will map the 
        # output of the scikit-learn model to the string expected by 
        # the output schema
        targets = ['setosa', 'versicolor', 'virginica']
        species = targets[y_hat]
        return {"species": species}

if __name__=="__main__":
    mymodel = IrisSVCModel()
    data=dict(sepal_length=1,sepal_width=2,petal_length=3,petal_width=4)
    classification=mymodel.predict(data)
    print(classification)
```

### Adding your model into Web Service
You will need to add your model function into the Web Service (flask_app.py). Here is an example, you may simply add your functions.
```python
# Import libraries
import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
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
from config import InferenceConfig
config = InferenceConfig()

# Create model object in inference mode.
module = __import__(config.MODEL_MODULE, fromlist=[config.MODEL_CLASS])
my_class = getattr(module,config.MODEL_CLASS)
model = my_class(config)

#Make a prediction before starting the server (First prediction takes longer)
data=config.MODEL_SAMPLE_INPUT 
classification=model.predict(data)
logging.info('Model and weight have been loaded.')

# Add your own functions here
def run_predict_flowers(data):
    logging.info('Loading data: %s', data)
    allresults=[]
    for entry in data:
        results = model.predict(entry)
        allresults.append(results)

    return allresults


# Instantiate the Node
app = Flask(__name__)

# Add your own functions here.
@app.route('/predict_flowers', methods=['POST'])
def predict_flowers_get():

    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_predict_flowers(request_json)
        
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
### Clone

- Clone this repo to your local machine using 
```shell
git clone https://github.com/jax79sg/artyins-classifierservice
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-classifierservice). You are required to write the necessary unit tests if you introduce more model classes.
### Unit Tests
```python
import unittest

class TestModels(unittest.TestCase):

    def test_testmodel(self):
        print("Running TestModel Loading and Prediction")
        from score.testmodel import IrisSVCModel
        mymodel = IrisSVCModel()
        data=dict(sepal_length=1.0,sepal_width=2.0,petal_length=3.0,petal_width=4.0)
        classification=mymodel.predict(data)

    def test_modifiedtopicmodel(self):
        print("Running empty Modified Topic Model -  Sure pass")
        pass #Wei Deng to insert


    def test_bertmodel(self):
        print("Running empty Bert Model - Sure pass")
        pass #Kah Siong to insert

if __name__ == '__main__':
    unittest.main()
```

### Web Service Test
```
#Start gunicorn wsgi server
gunicorn --bind 0.0.0.0:9898 --daemon --workers 1 wsgi:app
```
Send test POST request
```python
import requests 

TEST_TYPE = 'flowers' #Options flowers sentiments
  
# api-endpoint
URL = None
DATA = None
if TEST_TYPE=='flowers':
   URL = "http://localhost:9898/predict_flowers"
   DATA = [{"petal_width":1.0, 'petal_length':2.0,'sepal_width':3.1,'sepal_length':4.3,}]
elif (TEST_TYPE=='sentiments'): 
   URL = "http://localhost:9898/predict_sentiments"
   DATA = {'sentences':['Physical pain is like a norm to me nowadays','Its been a painful year','I still try hard to be relavant']}
  
# sending get request and saving the response as response object 
r = requests.post(url = URL, json  = DATA) 
print(r) 
# extracting results in json format 
data = r.json()
print("Data sent:\n{}\n\nData received:\n{}".format(DATA,data))
```

---

