from db.schemas import Records
from models import RecordCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from db.conn import db


def get_records_for_user(
    user_id: int,
    exercise_name: str,
    session: Session = Depends(db.get_db),
):
    return (
        session.query(Records)
        .filter(Records.user_id == user_id)
        .filter(Records.exercise_name == exercise_name)
        .order_by(Records.date.desc())
        .all()
    )


def create_user_records(
    record: RecordCreate,
    user_id: int,
    session: Session = Depends(db.get_db),
):
    db_item = Records(**record.dict(), user_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
