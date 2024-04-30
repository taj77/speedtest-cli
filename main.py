from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse) #Home
async def name(request: Request, db: Session = Depends(get_db)):
    entries_size = 10
    data_json = Gather_Entries_Start_to_End(entries_size,db)
    upload_arr = [0]*entries_size
    download_arr = [0]*entries_size
    up_average = 0
    down_average = 0
    i = 0
    for items in data_json:
        upload_arr[i] = items.upload
        download_arr[i] = items.download
        up_average = up_average + upload_arr[i]
        down_average = down_average  +download_arr[i]
        i = i + 1
        pass
    up_average = up_average/entries_size
    down_average = down_average/entries_size
    
    return templates.TemplateResponse("home.html", context={"request":request, "bandwidth": read_latest_value(db),
     "uploads": upload_arr, "downloads": download_arr, "uploadAverage" : up_average, "downloadAverage" : down_average})

# Post request for upload bandwidth from local host to API
@app.post("/upload/", response_model=schemas.Band)
def create_bandwidth(user: schemas.Band, db: Session = Depends(get_db)):
    return crud.create_bw(db=db, user=user)


# returns the most recent Bandwidth object
@app.get("/recent/", response_model=schemas.Band)
def read_latest_value(db: Session = Depends(get_db)):
    return crud.get_recent(db)

# 
# Returns the X amount of most recent objects
# EX: Limit = 25: 
# return the 25 most recent values
@app.get("/recentBandwidths/", response_model=list[schemas.Band])
def Gather_Entries_Start_to_End(Limit:int, db: Session = Depends(get_db)):
    db_user = crud.get_bw(db, limit=Limit)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Entries yet")
    return db_user

