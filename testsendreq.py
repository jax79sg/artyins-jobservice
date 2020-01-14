import requests 
from config import JobConfig

  
# api-endpoint
config = JobConfig()

URL = "http://localhost:9891/test"
r = requests.get(url = URL, data = "")
print("Data received: ", r)


