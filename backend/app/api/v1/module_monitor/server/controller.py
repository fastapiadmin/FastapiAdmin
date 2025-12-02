# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import ServerService


ServerRouter = APIRouter(route_class=OperationLogRoute, prefix="/server", tags=["服务器监控"])

@ServerRouter.get(
    '/info',
    summary="查询服务器监控信息",
    description="查询服务器监控信息",
    dependencies=[Depends(AuthPermission(["module_monitor:server:query"]))]
)
async def get_monitor_server_info_controller() -> JSONResponse:
    """
    查询服务器监控信息
    
    返回:
    - JSONResponse: 包含服务器监控信息的JSON响应。
    """
    result_dict = await ServerService.get_server_monitor_info_service()
    log.info(f'获取服务器监控信息成功: {result_dict}')

    return SuccessResponse(data=result_dict, msg='获取服务器监控信息成功')
