from fastapi import APIRouter
from datetime import datetime
from starlette.responses import Response

root_router = APIRouter()


@root_router.get("/")
async def root():
    """
    ELB 상태 체크용 API
    :return:
    """
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
    )
