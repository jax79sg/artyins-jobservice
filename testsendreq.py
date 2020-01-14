import requests 
from config import JobConfig

  
# api-endpoint
config = JobConfig()

URL = "http://localhost:9891/test"
r = requests.post(url = URL, data = "")
data=r.json()
print("Data received: ", data["message"])

URL = "http://localhost:9891/create_job"
r = requests.post(url = URL, json = )
data = r.json()
print("Data received: ", data["results"])

