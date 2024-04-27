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
    return templates.TemplateResponse("home.html", context={"request":request, "bandwidth": read_latest_value(db), "bandwidthTuple" : Gather_Entries_Start_to_End(0,20,db)})

@app.post("/upload/", response_model=schemas.Band)
def create_bandwidth(user: schemas.Band, db: Session = Depends(get_db)):
    return crud.create_bw(db=db, user=user)


@app.get("/recent/", response_model=schemas.Band)
def read_latest_value(db: Session = Depends(get_db)):
    return crud.get_recent(db)

@app.get("/count/")
def count_bw_Probably_Dont_Need(db: Session = Depends(get_db)):
    return crud.get_num_data(db)

@app.get("/recentBandwidths/", response_model=list[schemas.Band]) #delete response_model if errors.
def Gather_Entries_Start_to_End(start: int, end:int, db: Session = Depends(get_db)):
    db_user = crud.get_bw(db, skip=start, limit=end)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Entries yet")
    return db_user

