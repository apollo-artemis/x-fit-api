from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic.networks import EmailStr


class SnsType(Enum):
    Kakao: str = "kakao"
    Apple: str = "apple"


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
    email: EmailStr

class SexType(str, Enum):
    male = "male"
    female = "female"

class UserRegister(UserBase):
    password: str
    birth: str 
    sex: SexType 
    height: int
    weight: int

class UserLogin(UserBase):
    password: str


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

class WodDetail(BaseModel):
    title: str
    text: str
    like: int
    view_counts: int
    created_at: str
    wod_type: str

    class Config:
        orm_mode = True
class WodDelete(BaseModel):
    wod_id: int

class WodUpdate(BaseModel):
    title: str
    text: str
    wod_type: str