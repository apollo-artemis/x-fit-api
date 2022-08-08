from sqlalchemy.orm import Session

from db import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_records_for_user(
    db: Session, user_id: int, exercise_name: str, skip: int = 0, limit: int = 100
):

    return (
        db.query(models.Record)
        .filter(models.Record.user_id == user_id)
        .filter(models.Record.exercise_name == exercise_name)
        .offset(skip)
        .limit(limit)
        .all()
        .order_by(models.Record.date.asec())
    )


def create_user_records(db: Session, record: schemas.RecordCreate, user_id: int):
    db_item = models.Record(**record.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
