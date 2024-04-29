import requests
import json
import time
import speedtest   
from datetime import datetime, timezone


STATIC_URL = "https://computernetworks-project.onrender.com/"

def get_network_speed():
    st = speedtest.Speedtest() 
    error = False
    down_speed=0
    up_speed=0
    ping = 0
    try:
        down_speed = st.download()
        up_speed = st.upload()
        ping = st.results.ping
    except:
        error = True
    return {"error": error,"upload" : up_speed, "download": down_speed, "ping":ping}

def main():
    while True:
        time_now = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
        print("Iteration 1.")
        bw = get_network_speed()
        body = {
        "error": bw["error"],
        "upload": bw["upload"]/1000000,
        "download": bw["download"]/1000000,
        "ping": bw["ping"],
        "time": time_now
        } 
        json_data = json.dumps(body)
        r = requests.post(STATIC_URL+"upload", data=json_data)
        time.sleep(900)

if __name__ == '__main__':
    main()