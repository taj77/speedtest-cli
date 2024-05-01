import requests
import json
from datetime import *

GLOBAL_URL = "https://computernetworks-project.onrender.com/upload/"
LOCAL_URL = "http://127.0.0.1:8000/upload/" 

time_now = (datetime.now(timezone.utc)-timedelta(hours=4)).strftime("%m/%d/%Y, %H:%M:%S")
body = {
  "error": False,
  "upload": 19, # speed of upload in MB
  "download": 394, # speed of download in MB
  "date": time_now, # time in string, not really used but needed for schema
  "ping" : 59, # Response time from server
  "id": 0, # ID is not important, only required for schema
}
json_data = json.dumps(body)

# Change LOCAL_URL to GLOBAL_URL as needed to send request locally or globally
r = requests.post(LOCAL_URL, data=json_data) 
