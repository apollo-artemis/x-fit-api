from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.validator import AuthRequestMiddleware
from router import auth, records

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
