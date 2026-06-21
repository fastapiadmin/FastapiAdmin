from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    EmailConfigCreateSchema,
    EmailConfigOutSchema,
    EmailConfigQueryParam,
    EmailConfigUpdateSchema,
    EmailLogOutSchema,
    EmailLogQueryParam,
    EmailSendSchema,
    EmailTemplateCreateSchema,
    EmailTemplateOutSchema,
    EmailTemplateQueryParam,
    EmailTemplateUpdateSchema,
    EmailTestSchema,
)
from .service import EmailConfigService, EmailLogService, EmailSendService, EmailTemplateService

EmailRouter = APIRouter(route_class=OperationLogRoute, prefix="/email", tags=["平台管理", "邮件服务"])

@EmailRouter.get("/config/list", summary="SMTP 配置列表", response_model=ResponseSchema[PageResultSchema[EmailConfigOutSchema]])
async def email_config_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[EmailConfigQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
):
    result = await EmailConfigService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.get("/config/detail/{id}", summary="SMTP 配置详情", response_model=ResponseSchema[EmailConfigOutSchema])
async def email_config_detail_controller(
    id: Annotated[int, Path()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
):
    result = await EmailConfigService(auth).detail(id=id)
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.post("/config/create", summary="创建 SMTP 配置", response_model=ResponseSchema[EmailConfigOutSchema])
async def email_config_create_controller(
    data: EmailConfigCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailConfigService(auth).create(data=data)
    return SuccessResponse(data=result, msg="创建成功")

@EmailRouter.put("/config/update/{id}", summary="更新 SMTP 配置", response_model=ResponseSchema[EmailConfigOutSchema])
async def email_config_update_controller(
    id: Annotated[int, Path()],
    data: EmailConfigUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailConfigService(auth).update(id=id, data=data)
    return SuccessResponse(data=result, msg="更新成功")

@EmailRouter.delete("/config/delete", summary="删除 SMTP 配置", response_model=ResponseSchema[None])
async def email_config_delete_controller(
    ids: Annotated[list[int], Body()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    await EmailConfigService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除成功")

@EmailRouter.post("/config/test", summary="测试 SMTP 连接", response_model=ResponseSchema)
async def email_config_test_controller(
    data: EmailTestSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailConfigService(auth).test(data=data)
    return SuccessResponse(data=result, msg="测试邮件已发送")

@EmailRouter.get("/template/list", summary="邮件模板列表", response_model=ResponseSchema[PageResultSchema[EmailTemplateOutSchema]])
async def email_template_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[EmailTemplateQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
):
    result = await EmailTemplateService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.get("/template/detail/{id}", summary="邮件模板详情", response_model=ResponseSchema[EmailTemplateOutSchema])
async def email_template_detail_controller(
    id: Annotated[int, Path()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
):
    result = await EmailTemplateService(auth).detail(id=id)
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.post("/template/create", summary="创建邮件模板", response_model=ResponseSchema[EmailTemplateOutSchema])
async def email_template_create_controller(
    data: EmailTemplateCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailTemplateService(auth).create(data=data)
    return SuccessResponse(data=result, msg="创建成功")

@EmailRouter.put("/template/update/{id}", summary="更新邮件模板", response_model=ResponseSchema[EmailTemplateOutSchema])
async def email_template_update_controller(
    id: Annotated[int, Path()],
    data: EmailTemplateUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailTemplateService(auth).update(id=id, data=data)
    return SuccessResponse(data=result, msg="更新成功")

@EmailRouter.delete("/template/delete", summary="删除邮件模板", response_model=ResponseSchema[None])
async def email_template_delete_controller(
    ids: Annotated[list[int], Body()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    await EmailTemplateService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除成功")

@EmailRouter.post("/send", summary="手动发送邮件（超管测试/补发）", response_model=ResponseSchema)
async def email_send_controller(
    data: EmailSendSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
):
    result = await EmailSendService(auth).manual_send(data=data)
    return SuccessResponse(data=result, msg="发送成功")

@EmailRouter.get("/log/list", summary="邮件发送日志", response_model=ResponseSchema[PageResultSchema[EmailLogOutSchema]])
async def email_log_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[EmailLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
):
    result = await EmailLogService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")
