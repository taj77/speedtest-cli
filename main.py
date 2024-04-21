from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel): # class for storing bandwidth
    error: bool
    upload: float
    download: float
    ping: float
    time: str


app = FastAPI()

bandwidth = Item
bandwidth.error = True
bandwidth.upload = 0
bandwidth.download = 0
bandwidth.ping = 0

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "bandwidth": bandwidth})

@app.get("/bandwidth")
async def receive_bandwidth():
    if bandwidth.error != True:
        return {"upload": bandwidth.upload, "download": bandwidth.download, "ping":bandwidth.ping, "time":bandwidth.time}
    else:
        return {"Error": "Bandwidth has not been uploaded yet"}
    #speed = get_network_speed()
    #return speed
    #if speed["error"] == "False":
    #    return speed
    #else:
    #    return {"error": "True"}



@app.post("/upload")
async def upload_bandwidth(item: Item):
    item_dict = item.dict()
    if item_dict["error"] != True:
        bandwidth.error = False
        bandwidth.upload = float(item_dict["upload"])
        bandwidth.download = float(item_dict["download"])
        bandwidth.upload = round(bandwidth.upload, 1)
        bandwidth.download = round(bandwidth.download, 1)
        bandwidth.ping = item_dict["ping"]
        bandwidth.time = item_dict["time"]
    return item_dict