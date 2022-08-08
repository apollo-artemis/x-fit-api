from pydantic import BaseModel
from datetime import datetime


class RecordBase(BaseModel):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime
    repetition_maximum: int = 1


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    records: list[Record] = []

    class Config:
        orm_mode = True
