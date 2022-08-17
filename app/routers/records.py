from typing import List

from db.conn import get_db
from db.records_crud import create_user_records, get_records_for_user
from db.schemas import Record, RecordCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="")


@router.post("/record", response_model=Record)
def create_record_for_user(
    user_id: int, record: RecordCreate, db: Session = Depends(get_db)
):
    return create_user_records(db=db, record=record, user_id=user_id)


@router.get("/records", response_model=List[Record])
def read_records_for_user(
    user_id: int, exercise_name: str, db: Session = Depends(get_db)
) -> List[Record]:

    records = get_records_for_user(db, user_id, exercise_name, skip=0, limit=100)
    return records
