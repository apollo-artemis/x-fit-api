from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime
from typing import List


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


class UserRegister(UserBase):
    email: EmailStr = None
    password: str = None


class UserLogin(UserBase):
    email: EmailStr = None
    password: str = None


class UserJWT(UserBase):
    id: int = None
    email: EmailStr = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    records: List[Record] = []

    class Config:
        orm_mode = True
