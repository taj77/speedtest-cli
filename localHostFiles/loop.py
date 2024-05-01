import requests
import json
import time
import speedtest   
from datetime import datetime, timezone


GLOBAL_URL = "https://computernetworks-project.onrender.com/"
LOCAL_URL = "http://127.0.0.1:8000/" # Change LOCAL_URL if needed
STALL_DURATION = 1200 # Number of seconds between bandwidth data being sent to API

# Function to gather network metrics
def get_network_speed():
    st = speedtest.Speedtest()  # This function from the built-in framework gathers the bandwidth data
    # Create default values for if function fails
    error = False
    down_speed=0
    up_speed=0
    ping = 0
    try:
        down_speed = st.download() # gather Up and Down speed from request
        up_speed = st.upload()
        ping = st.results.ping
    except:
        error = True
    return {"error": error,"upload" : up_speed, "download": down_speed, "ping":ping}

# Infinite Loop to run on local machine.
# Will upload data via post request to Endpoint hosted on Render at GLOBAL_URL
def main():
    count = 0
    while True:
        time_now = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
        print(f"Iteration {count}.")
        bw = get_network_speed()
        body = {
        "error": bw["error"],
        "upload": int(bw["upload"]/1000000),
        "download": int(bw["download"]/1000000),
        "ping": bw["ping"],
        "date": time_now,
        "id": 0  # ID does not matter, but is required for schema.
        } 
        json_data = json.dumps(body)
        # API POST REQUEST TO 
        r = requests.post(GLOBAL_URL+"upload", data=json_data)
        time.sleep(STALL_DURATION)
        count = count + 1

if __name__ == '__main__':
    main()