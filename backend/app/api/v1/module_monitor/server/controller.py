from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.module_monitor.server.schema import ServerMonitorSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .service import ServerService

ServerRouter = APIRouter(route_class=OperationLogRoute, prefix="/server", tags=["系统监控", "服务器监控"])


@ServerRouter.get(
    "/info",
    summary="查询服务器监控信息",
    dependencies=[Depends(AuthPermission(["module_monitor:server:query"]))],
    response_model=ResponseSchema[ServerMonitorSchema],
)
async def get_monitor_server_info_controller() -> JSONResponse:
    result_dict = await ServerService.get_server_monitor_info()
    return SuccessResponse(data=result_dict, msg="获取服务器监控信息成功")
