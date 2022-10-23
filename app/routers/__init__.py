from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

root_router = APIRouter()


@root_router.get("/")
async def root():
    """
    ELB 상태 체크용 API
    :return:
    """
    current_time = datetime.utcnow()
    return JSONResponse(status_code=200, content=dict(msg=f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"))
