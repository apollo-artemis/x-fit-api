import re
import bcrypt
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models import User
from db.database import engine as db_engine
from db.schemas import UserRegister, UserLogin


def create_new_user(new_user: UserRegister, session: Session):
    hash_pw = bcrypt.hashpw(new_user.password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
    user = User(email=new_user.email, hashed_password=hash_pw)
    session.add(user)
    session.commit()
    

def is_email_exist(user_info: UserRegister):
    engine = db_engine
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
    engine = db_engine
    query = text(f"SELECT hashed_password FROM users where email='{user.email}'")
    
    with engine.connect() as conn:
        query_result = conn.execute(query)
        res = query_result.scalar()
        result = bcrypt.checkpw(user.password.encode('utf-8'), res.encode('utf-8'))
        
        return bool(result)


async def url_pattern_check(path, re_pattern):
    result = re.match(re_pattern, path)
    
    if result:
        return True
    return False

