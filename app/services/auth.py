import re

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
import bcrypt
from db.conn import db
from db.schemas import Users
from models import UserLogin, UserRegister


def create_new_user(new_user: UserRegister, session: Session = Depends(db.session)):
    hash_pw = bcrypt.hashpw(new_user.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    Users().create(
        session, auto_commit=True, email=new_user.email, hashed_password=hash_pw
    )


def is_email_exist(user_info: UserRegister):
    engine = db._engine
    query = text(f"SELECT email FROM users where email='{user_info.email}'")
    with engine.connect() as conn:
        res = conn.execute(query)
        result = res.scalar()

        return bool(result)


async def check_pw_format(password: UserRegister):
    # if re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$',password):
    #     return True
    if len(password) > 6 and len(password) <= 20:
        return True
    return False


async def check_password(user: UserLogin):
    engine = db._engine
    query = text(f"SELECT hashed_password FROM users where email='{user.email}'")

    with engine.connect() as conn:
        query_result = conn.execute(query)
        res = query_result.scalar()
        result = bcrypt.checkpw(user.password.encode("utf-8"), res.encode("utf-8"))

        return bool(result)


async def url_pattern_check(path, re_pattern):
    result = re.match(re_pattern, path)

    if result:
        return True
    return False
