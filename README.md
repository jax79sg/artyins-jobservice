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
- Save the information from above into storage
It simply calls other APIs to fulfil the above.

The `JobService` can be called by a HTTP POST call. Primarily on http://webserverip:port/create_job. It expects a json of the following format
```json
[{"filename":"file01.pdf",},{"filename":"file02.pdf"}]
```
and will vomit a json of one of the following.
```json
{"results": "ok"} #if things went well 
{"results": "nok"} #If things didn't go well
```
### config.py
The configuration will point to the URLs of the relevant APIs, and also set the logging level of the service.<br>
Note that log files are placed in `/logs` folder of the container by default.
```python
    EXTRACTION_URL='http://extractionsvc:9891/extract_content'
    INFERENCE_URL='http://classifiersvc:9891/infer_content'
    SAVE_URL='http://savesvc:9891/savecontent'    
    LOGGINGLEVEL=logging.DEBUG
```

### Flask
The API calls are coded in Flask. Upon deployment, they should be supported by a production WSGI server.<br>
A test call is also provided to test if the service is running.
```python
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
    response = {
        'message':'ok'
    }
    return jsonify(response), 200
```
---

## Virtualenv
All python requirements are located in requirements.txt
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt`
```
---

### Web Service Test
```python
URL = "http://127.0.0.1:9891/test"
r = requests.get(url = URL, data = "")
print("Data received: ", r)```
---

