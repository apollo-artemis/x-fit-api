from datetime import datetime

from pydantic import BaseModel


# data model
class ExerciseRecord(BaseModel):
    exercise_name: str
    weight: int = 0
    unit: str = "lb"
    date: datetime = datetime.now()
