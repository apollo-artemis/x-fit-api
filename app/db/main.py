from sqlalchemy.orm import Session


from db import crud, models, schemas
from db.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
