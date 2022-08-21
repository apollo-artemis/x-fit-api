from db.conn import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)

    def all_columns(self):
        return [c for c in self.__table__.columns]

    def __hash__(self):
        return hash(self.id)

    def create(self, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        for col in self.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(self, col_name, kwargs.get(col_name))
        session.add(self)
        session.flush()
        if auto_commit:
            session.commit()
        return self


class Users(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    record = relationship("Records", back_populates="user")


class Records(Base, BaseMixin):
    __tablename__ = "records"

    exercise_name = Column(String, index=True)
    weight = Column(Integer)
    unit = Column(String)
    date = Column(DateTime)
    repetition_maximum = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="record")
