"""
人员管理 - 控制器
"""

import urllib.parse
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    PersonnelCreateSchema,
    PersonnelOutSchema,
    PersonnelQuerySchema,
    PersonnelUpdateSchema,
)
from .service import PersonnelService

PersonnelRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/personnel",
    tags=["招生宣传活动 - 人员管理"],
)


@PersonnelRouter.get(
    "/detail/{id}",
    summary="获取招生人员详情",
    description="获取招生人员详情",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="招生人员ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:detail"]))],
) -> JSONResponse:
    """
    获取招生人员详情

    参数:
    - id (int): 招生人员ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生人员详情的JSON响应
    """
    result_dict = await PersonnelService.detail_service(auth=auth, id=id)
    log.info(f"获取招生人员详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@PersonnelRouter.get(
    "/list",
    summary="查询招生人员列表",
    description="查询招生人员列表",
    response_model=ResponseSchema[list[PersonnelOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PersonnelQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:query"]))],
) -> JSONResponse:
    """
    查询招生人员列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (PersonnelQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生人员列表分页信息的JSON响应
    """
    result_dict = await PersonnelService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询招生人员列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@PersonnelRouter.post(
    "/create",
    summary="创建招生人员",
    description="创建招生人员",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def create_obj_controller(
    data: PersonnelCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:create"]))],
) -> JSONResponse:
    """
    创建招生人员

    参数:
    - data (PersonnelCreateSchema): 招生人员创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建招生人员详情的JSON响应
    """
    result_dict = await PersonnelService.create_service(auth=auth, data=data)
    log.info("创建招生人员成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@PersonnelRouter.put(
    "/update/{id}",
    summary="更新招生人员",
    description="更新招生人员",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="招生人员ID")],
    data: PersonnelUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:update"]))],
) -> JSONResponse:
    """
    更新招生人员

    参数:
    - id (int): 招生人员ID
    - data (PersonnelUpdateSchema): 招生人员更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后招生人员详情的JSON响应
    """
    result_dict = await PersonnelService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新招生人员成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@PersonnelRouter.delete(
    "/delete/{id}",
    summary="删除招生人员",
    description="删除招生人员",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="招生人员ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:delete"]))],
) -> JSONResponse:
    """
    删除招生人员

    参数:
    - id (int): 招生人员ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await PersonnelService.delete_service(auth=auth, id=id)
    log.info(f"删除招生人员成功 {id}")
    return SuccessResponse(msg="删除成功")


@PersonnelRouter.delete(
    "/batch-delete",
    summary="批量删除招生人员",
    description="批量删除招生人员",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:delete"]))],
) -> JSONResponse:
    """
    批量删除招生人员

    参数:
    - ids (list[int]): 招生人员ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await PersonnelService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除招生人员成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@PersonnelRouter.post(
    "/invite",
    summary="邀请招生人员",
    description="邀请招生人员",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def invite_controller(
    data: PersonnelCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:invite"]))],
) -> JSONResponse:
    """
    邀请招生人员

    参数:
    - data (PersonnelCreateSchema): 邀请数据
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含邀请信息的JSON响应
    """
    result_dict = await PersonnelService.invite_service(auth=auth, data=data)
    log.info("邀请招生人员成功")
    return SuccessResponse(data=result_dict, msg="邀请成功")


@PersonnelRouter.post(
    "/join/{invite_code}",
    summary="招生人员加入",
    description="招生人员通过邀请码加入",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def join_controller(
    invite_code: Annotated[str, Path(description="邀请码")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:query"]))],
) -> JSONResponse:
    """
    招生人员加入

    参数:
    - invite_code (str): 邀请码
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 加入成功的JSON响应
    """
    user_id = auth.user.id if auth.user else None
    result_dict = await PersonnelService.join_service(
        auth=auth, invite_code=invite_code, user_id=user_id
    )
    log.info("招生人员加入成功")
    return SuccessResponse(data=result_dict, msg="加入成功")


@PersonnelRouter.post(
    "/set-status/{id}",
    summary="设置招生人员状态",
    description="设置招生人员状态",
    response_model=ResponseSchema[PersonnelOutSchema],
)
async def set_status_controller(
    id: Annotated[int, Path(description="招生人员ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:update"]))],
    status: Annotated[str, Query(description="状态(active/inactive)")],
) -> JSONResponse:
    """
    设置招生人员状态

    参数:
    - id (int): 招生人员ID
    - status (str): 状态
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 设置状态成功的JSON响应
    """
    result_dict = await PersonnelService.set_status_service(auth=auth, id=id, status=status)
    log.info(f"设置招生人员状态成功 {id}, status={status}")
    return SuccessResponse(data=result_dict, msg="设置状态成功")


@PersonnelRouter.get(
    "/team/{team_id}",
    summary="获取招生组下所有人员",
    description="获取招生组下所有人员",
    response_model=ResponseSchema[list[PersonnelOutSchema]],
)
async def get_by_team_controller(
    team_id: Annotated[int, Path(description="招生组ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:query"]))],
) -> JSONResponse:
    """
    获取招生组下所有人员

    参数:
    - team_id (int): 招生组ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生人员列表的JSON响应
    """
    result_list = await PersonnelService.get_by_team_service(auth=auth, team_id=team_id)
    log.info("获取招生组人员列表成功")
    return SuccessResponse(data=result_list, msg="获取列表成功")


@PersonnelRouter.post(
    "/import/template",
    summary="获取招生人员导入模板",
    description="获取招生人员导入模板",
    dependencies=[Depends(AuthPermission(["module_promotion:personnel:download"]))],
)
async def export_obj_template_controller() -> StreamingResponse:
    """获取招生人员导入模板"""
    result = await PersonnelService.import_template_download_service()
    log.info("获取招生人员导入模板成功")

    return StreamResponse(
        data=bytes2file_response(result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={urllib.parse.quote('招生人员导入模板.xlsx')}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@PersonnelRouter.post(
    "/import/data",
    summary="导入招生人员",
    description="导入招生人员",
    response_model=ResponseSchema,
)
async def import_obj_list_controller(
    file: UploadFile,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:personnel:import"]))],
) -> JSONResponse:
    """导入招生人员"""
    result = await PersonnelService.batch_import_service(file=file, auth=auth, update_support=True)
    log.info(f"导入招生人员成功: {result}")
    return SuccessResponse(data=result, msg="导入招生人员成功")
