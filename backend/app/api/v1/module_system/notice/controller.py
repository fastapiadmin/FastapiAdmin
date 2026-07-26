from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Security, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema, PaginationQueryParam
from app.core.dependencies import AuthPermission, db_getter, get_current_user
from app.core.router_class import OperationLogRoute

from .schema import NoticeCreateSchema, NoticeOutSchema, NoticeQueryParam, NoticeUpdateSchema
from .service import NoticeService

NoticeRouter = APIRouter(route_class=OperationLogRoute, prefix="/notice", tags=["公告通知"])


@NoticeRouter.get("/detail/{id}", summary="获取公告详情", response_model=ResponseSchema[NoticeOutSchema])
async def get_notice_detail_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:detail"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="公告ID")],
) -> JSONResponse:
    result_dict = await NoticeService(auth, db).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取公告详情成功")


@NoticeRouter.get("/list", summary="查询公告", response_model=ResponseSchema[PageResultSchema[NoticeOutSchema]])
async def get_notice_list_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[NoticeQueryParam, Query()],
) -> JSONResponse:
    result_dict = await NoticeService(auth, db).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询公告列表成功")


@NoticeRouter.post("/create", status_code=status.HTTP_201_CREATED, summary="创建公告", response_model=ResponseSchema[NoticeOutSchema])
async def create_notice_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:create"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[NoticeCreateSchema, Body(description="公告创建参数")],
) -> JSONResponse:
    result_dict = await NoticeService(auth, db).create(data=data)
    return SuccessResponse(data=result_dict, msg="创建公告成功")


@NoticeRouter.put("/update/{id}", summary="修改公告", response_model=ResponseSchema[NoticeOutSchema])
async def update_notice_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:update"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="公告ID", ge=1)],
    data: Annotated[NoticeUpdateSchema, Body(description="公告修改参数")],
) -> JSONResponse:
    result_dict = await NoticeService(auth, db).update(id=id, data=data)
    return SuccessResponse(data=result_dict, msg="修改公告成功")


@NoticeRouter.delete("/delete", summary="删除公告", response_model=ResponseSchema[None])
async def delete_notice_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:delete"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await NoticeService(auth, db).delete(ids=ids)
    return SuccessResponse(msg="删除公告成功")


@NoticeRouter.patch("/status/batch", summary="批量修改公告状态", response_model=ResponseSchema[None])
async def batch_set_available_notice_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_system:notice:patch"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[BatchSetAvailable, Body(description="状态设置")],
) -> JSONResponse:
    await NoticeService(auth, db).set_available(data=data)
    return SuccessResponse(msg="批量修改公告状态成功")


@NoticeRouter.get("/available", summary="获取全局启用公告", response_model=ResponseSchema[list[NoticeOutSchema]])
async def get_notice_list_available_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse:
    result_dict = await NoticeService(auth, db).available_page()
    return SuccessResponse(data=result_dict.items, msg="查询已启用公告列表成功")
