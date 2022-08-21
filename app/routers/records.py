from typing import List
from db.conn import db
from db.crud.records import create_user_records, get_records_for_user
from models import Record, RecordCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="")


@router.post("/record", response_model=Record)
def create_record_for_user(
    user_id: int, record: RecordCreate, session: Session = Depends(db.get_db)
):
    return create_user_records(record=record, user_id=user_id, session=session)


@router.get("/records", response_model=List[Record])
def read_records_for_user(
    user_id: int, exercise_name: str, session: Session = Depends(db.get_db)
) -> List[Record]:

    records = get_records_for_user(
        user_id, exercise_name, skip=0, limit=100, session=session
    )
    return records
