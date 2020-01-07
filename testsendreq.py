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
