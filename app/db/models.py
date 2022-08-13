from db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    record = relationship("Record", back_populates="user")


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, index=True)
    weight = Column(Integer)
    unit = Column(String)
    date = Column(DateTime, index=True)
    repetition_maximum = Column(Integer, index=True)
    # create_at =
    # update_at =
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="record")
