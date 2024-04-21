# FastAPI app for network metrics
This is hosted for free with Render, at https://computernetworks-project.onrender.com

## Purpose
The goal is to have a local host send the bandwidth data to the webapp via a post request

## How to run?
To setup the webapp, run:
```
uvicorn main:app --reload
```
To have your local host upload the bandwidth data, run loop.py

