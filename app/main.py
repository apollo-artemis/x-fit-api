from typing import List
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Records(BaseModel):
    date: datetime
    exercise_name: str
    weight: int = 0
    weight_unit: str = "lb"


@app.get("/")
def read_root():
    return "Hello World!"


@app.get("/records", response_model=List[Records])
def read_records(user_id: int, exercise_name: str) -> list:

    record_1 = {
        "date": datetime(2022, 6, 1),
        "exercise_name": "DeadLift",
        "weight": 185,
        "weight_unit": "lb",
    }
    record_2 = {
        "date": datetime(2022, 6, 2),
        "exercise_name": "DeadLift",
        "weight": 195,
        "weight_unit": "lb",
    }

    return [record_1, record_2]
