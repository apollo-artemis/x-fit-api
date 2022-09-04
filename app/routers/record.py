from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.conn import db
from db.crud.records import get_records_for_user
from services.record import create_user_records
from models import Record, RecordCreate
from middlewares.validator import TokenGenerator


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
router = APIRouter(prefix="")

@router.post("/record")
async def create_record_for_user(
    record: RecordCreate, 
    token: str = Depends(API_KEY_HEADER),
    session: Session = Depends(db.get_db)
):
    user_info = TokenGenerator().decode_token(token)
    created_record = create_user_records(record, user_info["id"], session)

    return created_record


@router.get("/records", response_model=List[Record])
async def read_records_for_user(
    exercise_name: str, 
    token: str = Depends(API_KEY_HEADER),
    session: Session = Depends(db.get_db)
) -> List[Record]:
    
    user_info = TokenGenerator().decode_token(token)
    records = get_records_for_user(
        user_info["id"], exercise_name, skip=0, limit=100, session=session
    )
    
    return records
