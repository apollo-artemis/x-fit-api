from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.validator import AuthRequestMiddleware
from routers import auth, records, root_router
import uvicorn
from common.config import conf
from dataclasses import asdict
from db.conn import db


def create_app():
    app = FastAPI()

    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

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
    app.include_router(root_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
