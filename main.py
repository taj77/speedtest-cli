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
    return templates.TemplateResponse("home.html", context={"request":request, "bandwidth": read_latest_value(db)})

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

