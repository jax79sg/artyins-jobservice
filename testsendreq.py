import requests 
from config import JobConfig

  
# api-endpoint
config = JobConfig()

URL = "http://127.0.0.1:9891/test"
r = requests.get(url = URL, data = "")
print("Data received: ", r)


