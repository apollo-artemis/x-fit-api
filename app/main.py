from typing import List
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Record(BaseModel):
    date: datetime
    exercise_name: str
    weight: int = 0
    weight_unit: str = "lb"


@app.get("/")
def read_root():
    return "Hello World!"


@app.get("/records", response_model=List[Record])
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


@app.post("/record", response_model=Record)
def create_record(record: Record):

    # user_id , exercise_name 검증

    return
