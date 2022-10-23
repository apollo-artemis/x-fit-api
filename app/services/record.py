from db.conn import db
from db.schemas import Records
from fastapi import Depends
from models import RecordCreate
from sqlalchemy.orm import Session


def create_user_records(
        record: RecordCreate,
        user_id: int,
        session: Session
    ):

    db_item = Records(**record.dict(), user_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


def get_records_for_user(
    user_id: int,
    exercise_name: str,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(db.get_db),
):
    return (
        session.query(Records)
        .filter(Records.user_id == user_id)
        .filter(Records.exercise_name == exercise_name)
        .offset(skip)
        .limit(limit)
        .all()
    )

# kg 2 lbs, lbs 2 kg
async def weight_shift(weight, current_unit):
    if current_unit == "kg":
        target = weight * 2.20462
    else:
        target = weight * 0.453592
    
    return target