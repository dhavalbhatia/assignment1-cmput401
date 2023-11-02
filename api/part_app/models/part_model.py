from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..db import Base

class Part(Base):
    __tablename__ = "parts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    type = Column(String, index=True)
    price = Column(Float, index=True)
    release_date = Column(Integer, index=True)
    core_clock = Column(Float, index=True)
    boost_clock = Column(Float, nullable=True)
    clock_unit = Column(String, index=True)
    tdp = Column(Integer, index=True)
    part_no = Column(String, index=True)
    