from sqlalchemy.orm import Session
from db import records_crud


from db import models, schemas
from db.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
