from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, File, UploadFile

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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[EmailConfigQueryParam, Query(description="SMTP 配置查询参数")],
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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
    id: Annotated[int, Path(description="SMTP 配置ID")],
):
    result = await EmailConfigService(auth).detail(id=id)
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.post("/config/create", summary="创建 SMTP 配置", response_model=ResponseSchema[EmailConfigOutSchema])
async def email_config_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    data: Annotated[EmailConfigCreateSchema, Body(description="SMTP 配置创建参数")],
):
    result = await EmailConfigService(auth).create(data=data)
    return SuccessResponse(data=result, msg="创建成功")

@EmailRouter.put("/config/update/{id}", summary="更新 SMTP 配置", response_model=ResponseSchema[EmailConfigOutSchema])
async def email_config_update_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    id: Annotated[int, Path(description="SMTP 配置ID")],
    data: Annotated[EmailConfigUpdateSchema, Body(description="SMTP 配置更新参数")],
):
    result = await EmailConfigService(auth).update(id=id, data=data)
    return SuccessResponse(data=result, msg="更新成功")

@EmailRouter.delete("/config/delete", summary="删除 SMTP 配置", response_model=ResponseSchema[None])
async def email_config_delete_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    ids: Annotated[list[int], Body(description="要删除的 SMTP 配置ID列表")],
):
    await EmailConfigService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除成功")

@EmailRouter.post("/config/test", summary="测试 SMTP 连接", response_model=ResponseSchema)
async def email_config_test_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    data: Annotated[EmailTestSchema, Body(description="测试参数")],
):
    result = await EmailConfigService(auth).test(data=data)
    return SuccessResponse(data=result, msg="测试邮件已发送")

@EmailRouter.get("/template/list", summary="邮件模板列表", response_model=ResponseSchema[PageResultSchema[EmailTemplateOutSchema]])
async def email_template_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[EmailTemplateQueryParam, Query(description="邮件模板查询参数")],
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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
    id: Annotated[int, Path(description="邮件模板ID")],
):
    result = await EmailTemplateService(auth).detail(id=id)
    return SuccessResponse(data=result, msg="查询成功")

@EmailRouter.post("/template/create", summary="创建邮件模板", response_model=ResponseSchema[EmailTemplateOutSchema])
async def email_template_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    data: Annotated[EmailTemplateCreateSchema, Body(description="邮件模板创建参数")],
):
    result = await EmailTemplateService(auth).create(data=data)
    return SuccessResponse(data=result, msg="创建成功")

@EmailRouter.put("/template/update/{id}", summary="更新邮件模板", response_model=ResponseSchema[EmailTemplateOutSchema])
async def email_template_update_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    id: Annotated[int, Path(description="邮件模板ID")],
    data: Annotated[EmailTemplateUpdateSchema, Body(description="邮件模板更新参数")],
):
    result = await EmailTemplateService(auth).update(id=id, data=data)
    return SuccessResponse(data=result, msg="更新成功")

@EmailRouter.delete("/template/delete", summary="删除邮件模板", response_model=ResponseSchema[None])
async def email_template_delete_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    ids: Annotated[list[int], Body(description="要删除的邮件模板ID列表")],
):
    await EmailTemplateService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除成功")

@EmailRouter.post("/send", summary="手动发送邮件（超管测试/补发）", response_model=ResponseSchema)
async def email_send_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:update"]))],
    data: Annotated[EmailSendSchema, Body(description="发送参数")],
):
    result = await EmailSendService(auth).manual_send(data=data)
    return SuccessResponse(data=result, msg="发送成功")

@EmailRouter.get("/log/list", summary="邮件发送日志", response_model=ResponseSchema[PageResultSchema[EmailLogOutSchema]])
async def email_log_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:email:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[EmailLogQueryParam, Query(description="邮件发送日志查询参数")],
):
    result = await EmailLogService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")
