from pydantic import BaseModel
from datetime import datetime


# data model
class ExerciseRecord(BaseModel):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime = datetime.now()
