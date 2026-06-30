from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.dependencies import AuthPermission, get_current_user
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from app.core.logger import logger
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    NoticeCreateSchema,
    NoticeOutSchema,
    NoticeQueryParam,
    NoticeUpdateSchema,
    PanelDataOut,
)
from .service import NoticeService

NoticeRouter = APIRouter(route_class=OperationLogRoute, prefix="/notice", tags=["系统管理", "公告通知"])

_NOTICE_NS = "notice"

@NoticeRouter.get(
    "/detail/{id}",
    summary="获取公告详情",
    response_model=ResponseSchema[NoticeOutSchema],
)
async def get_notice_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:detail"]))],
    id: Annotated[int, Path(description="公告ID")],
) -> JSONResponse:
    result_dict = await NoticeService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取公告详情成功")

@NoticeRouter.get(
    "/list",
    summary="查询公告",
    response_model=ResponseSchema[PageResultSchema[NoticeOutSchema]],
)
async def get_notice_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[NoticeQueryParam, Query(description="公告查询参数")],
) -> JSONResponse:
    result_dict = await NoticeService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询公告列表成功")

@NoticeRouter.post(
    "/create",
    summary="创建公告",
    response_model=ResponseSchema[NoticeOutSchema],
)
async def create_notice_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:create"]))],
    data: Annotated[NoticeCreateSchema, Body(description="公告创建参数")],
) -> JSONResponse:
    result_dict = await NoticeService(auth).create(data=data)
    await FastAPICache.clear(namespace=_NOTICE_NS)
    return SuccessResponse(data=result_dict, msg="创建公告成功")

@NoticeRouter.put(
    "/update/{id}",
    summary="修改公告",
    response_model=ResponseSchema[NoticeOutSchema],
)
async def update_notice_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:update"]))],
    id: Annotated[int, Path(description="公告ID")],
    data: Annotated[NoticeUpdateSchema, Body(description="公告修改参数")],
) -> JSONResponse:
    result_dict = await NoticeService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_NOTICE_NS)
    return SuccessResponse(data=result_dict, msg="修改公告成功")

@NoticeRouter.delete(
    "/delete",
    summary="删除公告",
    response_model=ResponseSchema[None],
)
async def delete_notice_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await NoticeService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_NOTICE_NS)
    return SuccessResponse(msg="删除公告成功")

@NoticeRouter.patch(
    "/status/batch",
    summary="批量修改公告状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_notice_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:patch"]))],
    data: Annotated[BatchSetAvailable, Body(description="批量修改公告状态参数")],
) -> JSONResponse:
    await NoticeService(auth).set_available(data=data)
    await FastAPICache.clear(namespace=_NOTICE_NS)
    return SuccessResponse(msg="批量修改公告状态成功")

@NoticeRouter.post(
    "/export",
    summary="导出公告",
)
async def export_notice_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:notice:export"]))],
    search: Annotated[NoticeQueryParam, Query(description="公告查询参数")],
) -> StreamingResponse:
    result_dict_list = await NoticeService(auth).get_list(search=search)
    export_data = [item.model_dump() for item in result_dict_list]
    export_result = NoticeService.export(notice_list=export_data)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=notice.xlsx"},
    )

@NoticeRouter.get(
    "/available",
    summary="获取全局启用公告",
    response_model=ResponseSchema[list[NoticeOutSchema]],
)
@cache(expire=120, namespace=_NOTICE_NS)
async def get_notice_list_available_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    result_dict = await NoticeService(auth).available_page()
    return SuccessResponse(data=result_dict, msg="查询已启用公告列表成功")

@NoticeRouter.get(
    "/panel",
    summary="通知面板数据（铃铛）",
    response_model=ResponseSchema[PanelDataOut],
)
@cache(expire=30, namespace=_NOTICE_NS)
async def get_notification_panel_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    """通知面板聚合接口，返回通知、消息、待办三个列表。"""
    result = await NoticeService(auth).panel_data()
    return SuccessResponse(data=result, msg="获取面板数据成功")

@NoticeRouter.post(
    "/read/{id}",
    summary="标记已读",
    response_model=ResponseSchema[None],
)
async def mark_read_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
    id: Annotated[int, Path(description="通知ID")],
) -> JSONResponse:
    """标记已读。通过 `sys_notice_read` 表记录已读时间。"""
    await NoticeService(auth).mark_read(notice_id=id)
    await FastAPICache.clear(namespace=_NOTICE_NS)
    logger.info(f"用户[{auth.user.id}]标记通知[{id}]已读")
    return SuccessResponse(msg="标记已读成功")

@NoticeRouter.post(
    "/read-all",
    summary="全部已读",
    response_model=ResponseSchema[int],
)
async def mark_all_read_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    """全部标记已读。返回本次操作标记的数量。"""
    count = await NoticeService(auth).mark_all_read()
    await FastAPICache.clear(namespace=_NOTICE_NS)
    logger.info(f"用户[{auth.user.id}]全部已读, 数量={count}")
    return SuccessResponse(data=count, msg=f"全部标记已读成功，共标记 {count} 条")

@NoticeRouter.get(
    "/unread-count",
    summary="获取未读数量",
    response_model=ResponseSchema[int],
)
@cache(expire=15, namespace=_NOTICE_NS)
async def get_unread_count_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    """获取未读通知数量。通过 LEFT JOIN 统计未读数。"""
    count = await NoticeService(auth).get_unread_count()
    return SuccessResponse(data=count, msg="获取未读数量成功")
