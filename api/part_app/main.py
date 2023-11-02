from typing import Union
import uuid
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, status, Query
from pydantic import BaseModel
from .schemas import part
from .crud import parts
from .models import part_model as models

from .db import SessionLocal, engine

from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url="/parts/openapi.json",
    docs_url="/parts/docs",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/parts", response_model=part.ResponsePart)
def get_all_parts(type: Optional[str] = None, db: Session = Depends(get_db)):
    if type is not None:
        if type.lower() == "gpu" or type.lower() == 'cpu':
            parts_list = parts.get_parts(db, type)
            return {"status": parts_list["status"], "total": parts_list["count"], "average_price": parts_list["average_price"], "parts": parts_list["parts"]}
        raise HTTPException(status_code=400, detail={"status": "1", "message": "Invalid type. Valid choices are ‘CPU’ and ‘GPU’."})
    if type is None:
        parts_list = parts.get_parts(db, type)
        return {"status": parts_list["status"], "total": parts_list["count"], "average_price": parts_list["average_price"], "parts": parts_list["parts"]}

@app.get("/parts/{part_id}", response_model=part.PartProfile)
def get_part(part_id: uuid.UUID, db: Session = Depends(get_db)):
    db_part = parts.get_part(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return db_part

# TODO- handle id in request body
@app.put("/parts", response_model=part.ResponsePut)
def create_part(part: part.CreatePart, db: Session = Depends(get_db)):
    if "id" in part:
        raise HTTPException(status_code=400, detail={"status": "1", "message": "ID should not be provided"})
    elif part.type.lower() != "gpu" and part.type.lower() != 'cpu':
        raise HTTPException(status_code=400, detail={"status": "1", "message": "Invalid type. Valid choices are ‘CPU’ and ‘GPU’."})
    response = parts.create_part(db, part)
    return {"status": response["status"], "message": response["message"], "id": response["id"]}

@app.post("/parts/{part_id}", response_model=part.ResponsePost)
def update_part(part_id: uuid.UUID, part: part.UpdatePart, db: Session = Depends(get_db)):
    if "id" in part:
        raise HTTPException(status_code=400, detail={"status": "1", "message": "ID should not be provided"})
    if part.type.lower() == "gpu" or part.type.lower() == 'cpu':
        db_part = parts.get_part(db, part_id)
        if db_part is None:
            raise HTTPException(status_code=404, detail="Part not found")
        updated_part = parts.update_part(db, part_id, part)
        return {"status": 0, "message": "Part details updated"}
    raise HTTPException(status_code=400, detail={"status": "1", "message": "Invalid type. Valid choices are ‘CPU’ and ‘GPU’."})


@app.patch("/parts/{part_id}", response_model=part.ResponsePost)
def patch_part(part_id: uuid.UUID, request: dict, db: Session = Depends(get_db)):
    db_part = parts.get_part(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    for key, value in request.items():
        if value is not None and key in part.PatchPart.__fields__:
            if key == "type" and (value.lower() != "gpu" and value.lower() != "cpu"):
                raise HTTPException(status_code=400, detail={"status": "1", "message": "Invalid type. Valid choices are ‘CPU’ and ‘GPU’."})
            setattr(db_part, key, value)
        else:
            raise HTTPException(status_code=400, detail={"status": "1", "message": "Invalid key(s) or value(s)"})
    db.commit()
    return {"status": 0, "message": "Part modified"}


@app.delete("/parts/{part_id}", response_model=part.PartProfile)
def delete_part(part_id: uuid.UUID, db: Session = Depends(get_db)):
    db_part = parts.get_part(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    db.delete(db_part)
    db.commit()
    return db_part