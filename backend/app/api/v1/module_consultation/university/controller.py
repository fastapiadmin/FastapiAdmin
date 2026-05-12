"""
高校信息管理 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    UniversityCreateSchema,
    UniversityOutSchema,
    UniversityQuerySchema,
    UniversitySimpleOutSchema,
    UniversityUpdateSchema,
)
from .service import UniversityService

UniversityRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/university",
    tags=["招生咨询会 - 高校管理"],
)


@UniversityRouter.get(
    "/detail/{id}",
    summary="获取高校详情",
    description="获取高校详情",
    response_model=ResponseSchema[UniversityOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="高校ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:detail"]))],
) -> JSONResponse:
    """获取高校详情"""
    result_dict = await UniversityService.detail_service(id=id)
    log.info(f"获取高校详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@UniversityRouter.get(
    "/list",
    summary="查询高校列表",
    description="查询高校列表",
    response_model=ResponseSchema[list[UniversityOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[UniversityQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:query"]))],
) -> JSONResponse:
    """查询高校列表"""
    result_dict = await UniversityService.page_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询高校列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@UniversityRouter.get(
    "/options",
    summary="获取高校下拉选项",
    description="获取高校下拉选项（用于表单选择）",
    response_model=ResponseSchema[list[UniversitySimpleOutSchema]],
)
async def get_university_options_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:query"]))],
) -> JSONResponse:
    """获取高校下拉选项"""
    search = UniversityQuerySchema(status="active")
    result_list = await UniversityService.list_service(search=search)
    log.info("获取高校下拉选项成功")
    return SuccessResponse(data=result_list, msg="获取选项成功")


@UniversityRouter.post(
    "/create",
    summary="创建高校",
    description="创建高校",
    response_model=ResponseSchema[UniversityOutSchema],
)
async def create_obj_controller(
    data: UniversityCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:create"]))],
) -> JSONResponse:
    """创建高校"""
    result_dict = await UniversityService.create_service(
        data=data,
        user_id=auth.user.id if auth.user else None,
    )
    log.info("创建高校成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@UniversityRouter.put(
    "/update/{id}",
    summary="更新高校",
    description="更新高校",
    response_model=ResponseSchema[UniversityOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="高校ID")],
    data: UniversityUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:update"]))],
) -> JSONResponse:
    """更新高校"""
    result_dict = await UniversityService.update_service(
        id=id,
        data=data,
        user_id=auth.user.id if auth.user else None,
    )
    log.info(f"更新高校成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@UniversityRouter.delete(
    "/delete/{id}",
    summary="删除高校",
    description="删除高校",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="高校ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:university:delete"]))],
) -> JSONResponse:
    """删除高校"""
    await UniversityService.delete_service(id=id)
    log.info(f"删除高校成功 {id}")
    return SuccessResponse(msg="删除成功")
