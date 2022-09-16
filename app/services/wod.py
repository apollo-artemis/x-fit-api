from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.conn import db
from db.schemas import Wods, Users, WodTypes
from errors import exceptions as ex


def create_user_wod(wod_info, user_id, session):
    
    if wod_info.wod_type == "time":
        wod_type_no = 1
    elif wod_info.wod_type == "amrap":
        wod_type_no = 2
    else:
        wod_type_no = 3

    Wods.create(
        session, 
        auto_commit=True,
        title=wod_info.title,
        text=wod_info.text,
        wod_type_id=wod_type_no,
        like=0,
        view_counts=0,
        user_id=user_id
    )

async def get_wod_detail(wod_id, session):
    try:
        result = (
            session.query(Wods) 
            .filter(Wods.id == wod_id)
            .join(WodTypes, Wods.wod_type_id==WodTypes.id)
            .join(Users, Wods.user_id==Users.id)
            .one()
        )
        if not result:
            raise ex.NotFoundEx("No Matching Wod Id")
        
        result_dict = {
            "title": result.title,
            "text": result.text,
            "like": result.like,
            "view_counts": result.view_counts,
            "created_at": result.updated_at.strftime("%Y.%m.%d"),
            "wod_type": result.wod_type.wod_type_name
        }
        
        return result_dict
        
    except Exception as e:
        error: Exception = await ex.custom_exception_handler(e)
        error_dict: dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, ex=error.ex)
        raise HTTPException(status_code=error.status_code, detail=error_dict)
