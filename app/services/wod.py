# from sqlalchemy import delete, where
from db.schemas import Users, Wods, WodTypes
from errors import exceptions
from fastapi import HTTPException


def wod_type_shift(wod_type_str):
    if wod_type_str == "time":
        wod_type_no = 1
    elif wod_type_str == "amrap":
        wod_type_no = 2
    else:
        wod_type_no = 3

    return wod_type_no


def create_user_wod(wod_info, user_id, session):
    
    wod_type_no = wod_type_shift(wod_info.wod_type)

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
            .first()
        )
        
        if not result:
            raise exceptions.NotFoundEx("Wod ID Not Found")
        
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
        error: Exception = await exceptions.custom_exception_handler(e)
        error_dict: dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, ex=error.ex)
        raise HTTPException(status_code=error.status_code, detail=error_dict)

async def wod_ownership_check(wod_id, user_id, session):
    try:
        result = (
            session.query(Wods)
            .filter(Wods.id == wod_id)
            .first()
        )
        if not result:
            raise exceptions.NotFoundEx("Wod ID Not Found")
        
        
        if result.user_id != user_id:
            raise exceptions.NotAuthorized("Not Authorized")
        
    except Exception as e:
        error: Exception = await exceptions.custom_exception_handler(e)
        error_dict: dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, ex=error.ex)
        raise HTTPException(status_code=error.status_code, detail=error_dict)

async def update_wod_info(wod_id, wod_info, session):

    wod_type_no = wod_type_shift(wod_info.wod_type)
    
    (
        session.query(Wods).
        filter(Wods.id == wod_id).
        update({'title': wod_info.title, 'text': wod_info.text, 'wod_type_id': wod_type_no})
    )

    session.commit()

async def wod_delete(wod_id, session):
    session.query(Wods).filter(Wods.id == wod_id).delete(synchronize_session=False)
    session.commit()

    # delete.where(Wods).filter(Wods.id == wod_id)


