
# API for network metrics

This is hosted for free with Render, at https://computernetworks-project.onrender.com/

See https://computernetworks-project.onrender.com/docs for api documentation

Front end is not finished.

## Purpose
The goal is to have my local host send the bandwidth data to the api via a post request


The most recent recent Bandwidth Request can be seen by GET /recent/ 

The latest 20 Bandwidth Requests can be seen by GET /recentBandwidths/

### SQLite
Each Bandwidth upload is stored in the sql_app.db.

The sql_app directory contains all the models/schemas for managing the DB



## How to use?

run 
```
pip install -r requirements.txt
```
and
```
uvicorn main:app --reload
```

