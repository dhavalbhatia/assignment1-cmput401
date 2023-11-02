from pydantic import BaseModel
import uuid
from typing import Optional

class PartBase(BaseModel):
    name: str
    type: str
    price: float
    
class CreatePart(PartBase):
    release_date: int
    core_clock: float
    boost_clock: float | None = None
    clock_unit: str
    tdp: int
    part_no: str

class UpdatePart(PartBase):
    release_date: int
    core_clock: float
    boost_clock: float
    clock_unit: str
    tdp: int
    part_no: str

class PartProfile(PartBase):
    id: uuid.UUID
    
    class config:
        orm_mode = True
        
class ResponsePart(BaseModel):
    status: int
    total: int
    average_price: float
    parts: list[PartProfile]
    
class ResponsePut(BaseModel):
    status: int
    message: str
    id: uuid.UUID
    
class ResponsePost(BaseModel):
    status: int
    message: str
    
class PatchPart(BaseModel):
    name: Optional[str]
    type: Optional[str]
    price: Optional[float]
    release_date: Optional[int]
    core_clock: Optional[float]
    boost_clock: Optional[float]
    clock_unit: Optional[str]
    tdp: Optional[int]
    part_no: Optional[str]
    