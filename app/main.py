from typing import List
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import records_crud
from model import ExerciseRecord
from fastapi.middleware.cors import CORSMiddleware
from db.conn import get_db
from db import schemas
from router import auth, records
from middleware.validator import AuthRequestMiddleware

app = FastAPI()

origins = ["*"]

# app.add_middleware(AuthRequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(records.router)


@app.get("/")
def read_root():
    return "Hello World!!"
