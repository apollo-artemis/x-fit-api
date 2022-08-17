from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.validator import AuthRequestMiddleware
from routers import auth, records
import uvicorn


def create_app():
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

    return app


app = create_app()


@app.get("/")
def read_root():
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
