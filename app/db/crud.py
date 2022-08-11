from db import models, schemas
from sqlalchemy.orm import Session


def get_records_for_user(
    db: Session, user_id: int, exercise_name: str, skip: int = 0, limit: int = 100
):
    print(user_id)
    return (
        db.query(models.Record)
        .filter(models.Record.user_id == user_id)
        .filter(models.Record.exercise_name == exercise_name)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_records(db: Session, record: schemas.RecordCreate, user_id: int):
    db_item = models.Record(**record.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
