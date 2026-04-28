"""
咨询会信息聚合 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    InfoCollectionCreateSchema,
    InfoCollectionOutSchema,
    InfoCollectionQueryParam,
    InfoCollectionUpdateSchema,
    ThirdPartyUploadSchema,
)
from .service import InfoCollectionService

InfoCollectionRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/info-collection",
    tags=["招生咨询会 - 信息聚合"],
)


@InfoCollectionRouter.get(
    "/detail/{id}",
    summary="获取咨询会信息详情",
    description="获取咨询会信息详情",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:detail"]))
    ],
) -> JSONResponse:
    """
    获取咨询会信息详情

    参数:
    - id (int): 咨询会信息ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含咨询会信息详情的JSON响应
    """
    result_dict = await InfoCollectionService.detail_service(auth=auth, id=id)
    log.info(f"获取咨询会信息详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@InfoCollectionRouter.get(
    "/list",
    summary="查询咨询会信息列表",
    description="查询咨询会信息列表",
    response_model=ResponseSchema[list[InfoCollectionOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[InfoCollectionQueryParam, Depends()],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:query"]))
    ],
) -> JSONResponse:
    """
    查询咨询会信息列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (InfoCollectionQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含咨询会信息列表分页信息的JSON响应
    """
    result_dict = await InfoCollectionService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询咨询会信息列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@InfoCollectionRouter.post(
    "/create",
    summary="创建咨询会信息",
    description="创建咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def create_obj_controller(
    data: InfoCollectionCreateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:create"]))
    ],
) -> JSONResponse:
    """
    创建咨询会信息

    参数:
    - data (InfoCollectionCreateSchema): 咨询会信息创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建咨询会信息详情的JSON响应
    """
    result_dict = await InfoCollectionService.create_service(auth=auth, data=data)
    log.info("创建咨询会信息成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@InfoCollectionRouter.put(
    "/update/{id}",
    summary="更新咨询会信息",
    description="更新咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    data: InfoCollectionUpdateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:update"]))
    ],
) -> JSONResponse:
    """
    更新咨询会信息

    参数:
    - id (int): 咨询会信息ID
    - data (InfoCollectionUpdateSchema): 咨询会信息更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后咨询会信息详情的JSON响应
    """
    result_dict = await InfoCollectionService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新咨询会信息成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@InfoCollectionRouter.delete(
    "/delete/{id}",
    summary="删除咨询会信息",
    description="删除咨询会信息",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:delete"]))
    ],
) -> JSONResponse:
    """
    删除咨询会信息

    参数:
    - id (int): 咨询会信息ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await InfoCollectionService.delete_service(auth=auth, id=id)
    log.info(f"删除咨询会信息成功 {id}")
    return SuccessResponse(msg="删除成功")


@InfoCollectionRouter.delete(
    "/batch-delete",
    summary="批量删除咨询会信息",
    description="批量删除咨询会信息",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:delete"]))
    ],
) -> JSONResponse:
    """
    批量删除咨询会信息

    参数:
    - ids (list[int]): 咨询会信息ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await InfoCollectionService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除咨询会信息成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@InfoCollectionRouter.post(
    "/approve/{id}",
    summary="审核通过",
    description="审核通过咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:approve"]))
    ],
    review_comment: str | None = None,
) -> JSONResponse:
    """
    审核通过

    参数:
    - id (int): 咨询会信息ID
    - review_comment (str | None): 审核意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审核通过的JSON响应
    """
    result_dict = await InfoCollectionService.approve_service(
        auth=auth, id=id, review_comment=review_comment
    )
    log.info(f"审核通过咨询会信息成功 {id}")
    return SuccessResponse(data=result_dict, msg="审核通过")


@InfoCollectionRouter.post(
    "/reject/{id}",
    summary="审核拒绝",
    description="审核拒绝咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    review_comment: str,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:approve"]))
    ],
) -> JSONResponse:
    """
    审核拒绝

    参数:
    - id (int): 咨询会信息ID
    - review_comment (str): 审核意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审核拒绝的JSON响应
    """
    result_dict = await InfoCollectionService.reject_service(
        auth=auth, id=id, review_comment=review_comment
    )
    log.info(f"审核拒绝咨询会信息成功 {id}")
    return SuccessResponse(data=result_dict, msg="审核拒绝")


@InfoCollectionRouter.post(
    "/archive/{id}",
    summary="归档",
    description="归档咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def archive_controller(
    id: Annotated[int, Path(description="咨询会信息ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:archive"]))
    ],
) -> JSONResponse:
    """
    归档

    参数:
    - id (int): 咨询会信息ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 归档的JSON响应
    """
    result_dict = await InfoCollectionService.archive_service(auth=auth, id=id)
    log.info(f"归档咨询会信息成功 {id}")
    return SuccessResponse(data=result_dict, msg="归档成功")


@InfoCollectionRouter.post(
    "/third-party-upload",
    summary="第三方上传咨询会信息",
    description="支持第三方机构、高校、高中自助上传咨询会信息",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def third_party_upload_controller(
    data: ThirdPartyUploadSchema,
    source_type: Annotated[str, Query(description="上传来源(upload/high_school/university)")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:create"]))
    ],
) -> JSONResponse:
    """
    第三方上传咨询会信息

    参数:
    - data (ThirdPartyUploadSchema): 咨询会信息上传模型
    - source_type (str): 上传来源(upload-第三方机构/high_school-高中/university-高校)
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建咨询会信息详情的JSON响应
    """
    from .model import InfoSource

    # 转换source_type为InfoSource
    source_mapping = {
        "upload": InfoSource.UPLOAD.value,
        "high_school": InfoSource.HIGH_SCHOOL.value,
        "university": InfoSource.UNIVERSITY.value,
    }

    # 构建创建数据
    create_data = InfoCollectionCreateSchema(
        **data.model_dump(),
        source_type=source_mapping.get(source_type, InfoSource.UPLOAD.value),
    )

    result_dict = await InfoCollectionService.create_service(auth=auth, data=create_data)
    log.info(f"第三方上传咨询会信息成功，来源: {source_type}")
    return SuccessResponse(data=result_dict, msg="上传成功，请等待审核")


@InfoCollectionRouter.get(
    "/preview-list",
    summary="全部咨询会预览列表（带筛选）",
    description="在列表页直接按多维度筛选咨询会，无需先保存筛选条件",
    response_model=ResponseSchema[list[InfoCollectionOutSchema]],
)
async def preview_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:query"]))
    ],
    title: Annotated[str | None, Query(description="咨询会标题")] = None,
    organizer: Annotated[str | None, Query(description="主办方")] = None,
    province: Annotated[str | None, Query(description="省份")] = None,
    city: Annotated[str | None, Query(description="城市")] = None,
    organizer_nature: Annotated[str | None, Query(description="主办机构性质")] = None,
    compliance_level: Annotated[str | None, Query(description="合规等级")] = None,
    source_type: Annotated[str | None, Query(description="信息来源")] = None,
    status: Annotated[str | None, Query(description="状态")] = None,
    start_date_begin: Annotated[str | None, Query(description="开始日期-起")] = None,
    start_date_end: Annotated[str | None, Query(description="开始日期-止")] = None,
) -> JSONResponse:
    """
    全部咨询会预览列表（带筛选）

    支持直接在列表页按多维度筛选：
    - 地域：province, city
    - 时间：start_date_begin, start_date_end
    - 主办方：organizer, organizer_nature
    - 合规等级：compliance_level
    - 来源：source_type
    - 状态：status

    参数:
    - page: 分页参数
    - title: 咨询会标题（模糊搜索）
    - organizer: 主办方（模糊搜索）
    - province: 省份
    - city: 城市
    - organizer_nature: 主办机构性质
    - compliance_level: 合规等级
    - source_type: 信息来源
    - status: 状态
    - start_date_begin: 开始日期-起
    - start_date_end: 开始日期-止
    - auth: 认证信息

    返回:
    - JSONResponse: 筛选后的咨询会列表
    """
    result_dict = await InfoCollectionService.preview_list_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        title=title,
        organizer=organizer,
        province=province,
        city=city,
        organizer_nature=organizer_nature,
        compliance_level=compliance_level,
        source_type=source_type,
        status=status,
        start_date_begin=start_date_begin,
        start_date_end=start_date_end,
    )
    log.info("全部咨询会预览列表查询成功")
    return SuccessResponse(data=result_dict, msg="查询成功")
