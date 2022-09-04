from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic.networks import EmailStr


class RecordBase(BaseModel):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime
    repetition_maximum: int = 1


class RecordCreate(RecordBase):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime
    repetition_maximum: int = 1


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


class WodCreate(BaseModel):
    title: str
    text: str
    wod_type: str
    # like: int = 0
    # view_count: int = 0
    
