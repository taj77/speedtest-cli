import requests
import json
from datetime import *
import time

STATIC_URL = "https://computernetworks-project.onrender.com/"
time_now = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
body = {
  "error": False,
  "upload": 400.512341234,
  "download": 400.4512341243,
  "time": time_now
}
json_data = json.dumps(body)


r = requests.post("http://127.0.0.1:8000/"+"upload", data=json_data)
