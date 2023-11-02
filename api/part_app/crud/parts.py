from sqlalchemy.orm import Session
from ..schemas import part as schemas
from ..models import part_model
import uuid
from sqlalchemy import desc

def create_part(db: Session, part:schemas.CreatePart):
    db_part = part_model.Part(name=part.name, type=part.type, price=part.price, release_date=part.release_date, core_clock=part.core_clock, boost_clock=part.boost_clock, clock_unit=part.clock_unit, tdp=part.tdp, part_no=part.part_no)
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return {"status": 0, "message": "New part added", "id": db_part.id}

def get_parts(db: Session, type: str):
    print(db.query(part_model.Part).filter(part_model.Part.type == type).first())
    parts = db.query(part_model.Part.id, part_model.Part.name, part_model.Part.type, part_model.Part.price).filter(part_model.Part.type == type).order_by(desc(part_model.Part.price)).all()
    count = len(parts)
    total_price = sum(part.price for part in parts)
    average_price = total_price / count if count > 0 else 0
    return {"status": 0, "count": count, "average_price": average_price, "parts": parts}
    
    
def get_part(db: Session, part_id: uuid.UUID):
    return db.query(part_model.Part).filter(part_model.Part.id == part_id).first()

def update_part(db: Session, part_id: uuid.UUID, part: schemas.UpdatePart):
    db_part = db.query(part_model.Part).filter(part_model.Part.id == part_id).first()
    db_part.name = part.name
    db_part.type = part.type
    db_part.price = part.price
    db_part.release_date = part.release_date
    db_part.core_clock = part.core_clock
    db_part.boost_clock = part.boost_clock
    db_part.clock_unit = part.clock_unit
    db_part.tdp = part.tdp
    db_part.part_no = part.part_no
    db.commit()
    db.refresh(db_part)
    return db_part
