from pydantic import BaseModel

class BandBase(BaseModel):
    date: str
    upload: float
    download : float
    ping: float

#class BandCreate(BandBase):
#    ping: float


class Band(BandBase):
    id: int
    error: bool

    class Config:
        orm_mode = True

"""
class BandDict(BandBase):
    error: bool
    download : float
    date: str
    id: int
    upload: float
"""
