from fastapi import APIRouter
from fastapi.responses import JSONResponse

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get("", summary="健康检查", description="检查系统健康状态")
async def health_check() -> JSONResponse:
    """
    健康检查接口

    返回:
    - JSONResponse: 包含健康状态的JSON响应
    """
    return JSONResponse(content={"msg": True}, status_code=200)
