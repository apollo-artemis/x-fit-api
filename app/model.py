from datetime import datetime

from pydantic import BaseModel


# data model
class ExerciseRecord(BaseModel):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime = datetime.now()

class UserRegister(BaseModel):
    # 고도화 필요
    email: str = None
    password: str = None


class Login(BaseModel):
    email: str = None
    password: str = None