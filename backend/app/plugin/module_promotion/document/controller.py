"""
活动撰写 - 控制器
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

from .schema import DocumentCreateSchema, DocumentOutSchema, DocumentQuerySchema, DocumentUpdateSchema
from .service import DocumentService

DocumentRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/document",
    tags=["招生宣传活动 - 活动撰写"],
)


@DocumentRouter.get(
    "/detail/{id}",
    summary="获取活动撰写详情",
    description="获取活动撰写详情",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:detail"]))],
) -> JSONResponse:
    """
    获取活动撰写详情

    参数:
    - id (int): 活动撰写ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动撰写详情的JSON响应
    """
    result_dict = await DocumentService.detail_service(auth=auth, id=id)
    log.info(f"获取活动撰写详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@DocumentRouter.get(
    "/list",
    summary="查询活动撰写列表",
    description="查询活动撰写列表",
    response_model=ResponseSchema[list[DocumentOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[DocumentQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:query"]))],
) -> JSONResponse:
    """
    查询活动撰写列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (DocumentQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动撰写列表分页信息的JSON响应
    """
    result_dict = await DocumentService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询活动撰写列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@DocumentRouter.post(
    "/create",
    summary="创建活动撰写",
    description="创建活动撰写",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def create_obj_controller(
    data: DocumentCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:create"]))],
) -> JSONResponse:
    """
    创建活动撰写

    参数:
    - data (DocumentCreateSchema): 活动撰写创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建活动撰写详情的JSON响应
    """
    result_dict = await DocumentService.create_service(auth=auth, data=data)
    log.info(f"创建活动撰写成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@DocumentRouter.put(
    "/update/{id}",
    summary="更新活动撰写",
    description="更新活动撰写",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    data: DocumentUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:update"]))],
) -> JSONResponse:
    """
    更新活动撰写

    参数:
    - id (int): 活动撰写ID
    - data (DocumentUpdateSchema): 活动撰写更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后活动撰写详情的JSON响应
    """
    result_dict = await DocumentService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新活动撰写成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@DocumentRouter.delete(
    "/delete/{id}",
    summary="删除活动撰写",
    description="删除活动撰写",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:delete"]))],
) -> JSONResponse:
    """
    删除活动撰写

    参数:
    - id (int): 活动撰写ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await DocumentService.delete_service(auth=auth, id=id)
    log.info(f"删除活动撰写成功 {id}")
    return SuccessResponse(msg="删除成功")


@DocumentRouter.delete(
    "/batch-delete",
    summary="批量删除活动撰写",
    description="批量删除活动撰写",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:delete"]))],
) -> JSONResponse:
    """
    批量删除活动撰写

    参数:
    - ids (list[int]): 活动撰写ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await DocumentService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除活动撰写成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@DocumentRouter.post(
    "/publish/{id}",
    summary="发布文档",
    description="发布文档",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def publish_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:publish"]))],
) -> JSONResponse:
    """
    发布文档

    参数:
    - id (int): 活动撰写ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 发布成功的JSON响应
    """
    result_dict = await DocumentService.publish_service(auth=auth, id=id)
    log.info(f"发布文档成功 {id}")
    return SuccessResponse(data=result_dict, msg="发布成功")


@DocumentRouter.post(
    "/archive/{id}",
    summary="归档文档",
    description="归档文档",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def archive_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:archive"]))],
) -> JSONResponse:
    """
    归档文档

    参数:
    - id (int): 活动撰写ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 归档成功的JSON响应
    """
    result_dict = await DocumentService.archive_service(auth=auth, id=id)
    log.info(f"归档文档成功 {id}")
    return SuccessResponse(data=result_dict, msg="归档成功")


@DocumentRouter.post(
    "/view/{id}",
    summary="阅读文档",
    description="阅读文档",
    response_model=ResponseSchema[DocumentOutSchema],
)
async def view_controller(
    id: Annotated[int, Path(description="活动撰写ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:document:view"]))],
) -> JSONResponse:
    """
    阅读文档

    参数:
    - id (int): 活动撰写ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 阅读成功的JSON响应
    """
    result_dict = await DocumentService.view_service(auth=auth, id=id)
    log.info(f"阅读文档成功 {id}")
    return SuccessResponse(data=result_dict, msg="阅读成功")