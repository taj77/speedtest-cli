from sqlalchemy.orm import Session
from datetime import *

from . import models, schemas
def get_recent(db: Session):
    return db.query(models.Band).order_by(models.Band.id.desc()).first()


def get_num_data(db: Session):
    return db.query(models.Band).count()

def get_bw(db: Session, skip: int = 0, limit: int = 20): # can probably get rid of the lmit & skip
    return db.query(models.Band).order_by(models.Band.id.desc()).limit(limit).all()
    #return db.query(models.Band).offset(skip).limit(limit).all() OLD


def create_bw(db: Session, user: schemas.Band): #schemas.BandCreate):
    Upload = user.upload
    Download = user.download
    Ping = user.ping
    Error = False
    if (Upload == 0 and Download == 0):
        Error = True

    time_now = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
    db_user = models.Band(date=time_now, upload=Upload, download=Download, error=Error, ping=Ping)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user