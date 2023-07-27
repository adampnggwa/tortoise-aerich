from pydantic import BaseModel
from typing import List

class MetaData(BaseModel):
    code: int
    message: str

class DBsiswaData(BaseModel):
    id: int
    nama: str
    hobi: str

class DBsiswaResponse(BaseModel):
    meta: MetaData
    response: List[DBsiswaData]
