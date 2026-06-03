"""
咨询会信息聚合 - 控制器
"""

import urllib.parse
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Query, UploadFile
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, get_current_user, get_current_user_scoped
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .model import InfoSource, InfoStatus
from .schema import (
    InfoCollectionCreateSchema,
    InfoCollectionOutSchema,
    InfoCollectionQueryParam,
    InfoCollectionSimpleOutSchema,
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
    auth: Annotated[AuthSchema, Depends(get_current_user_scoped)],
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
    if not _has_permission(auth, "module_consultation:info_collection:detail"):
        if (
            result_dict.get("source_type") != InfoSource.CRAWLER.value
            or result_dict.get("status") != InfoStatus.APPROVED.value
        ):
            raise CustomException(msg="无权限操作", code=10403, status_code=403)
    log.info(f"获取咨询会信息详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


def _has_permission(auth: AuthSchema, permission: str) -> bool:
    """检查用户是否有指定权限"""
    if auth.user and auth.user.is_superuser:
        return True
    if not auth.user or not auth.user.roles:
        return False
    user_permissions = {
        menu.permission
        for role in auth.user.roles
        for menu in role.menus
        if role.status == "0" and menu.permission and menu.status == "0"
    }
    return permission in user_permissions


@InfoCollectionRouter.get(
    "/list",
    summary="查询咨询会信息列表",
    description="查询咨询会信息列表（无菜单权限用户仅可查看已审核数据）",
    response_model=ResponseSchema[list[InfoCollectionOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[InfoCollectionQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(get_current_user_scoped)],
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
    from app.common.enums import QueueEnum

    # 非超管且无 query 权限：仅可查已审核数据（含已审核的 crawler）
    if not (auth.user and auth.user.is_superuser) and not _has_permission(
        auth, "module_consultation:info_collection:query"
    ):
        search.status = (QueueEnum.eq.value, InfoStatus.APPROVED.value)

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
    background_tasks: BackgroundTasks,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:approve"]))
    ],
    review_comment: Annotated[str | None, Query(description="审核意见")] = None,
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
    background_tasks.add_task(InfoCollectionService.run_compliance_diagnosis_background, id)
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
    review_comment: Annotated[str, Query(description="审核意见")],
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


@InfoCollectionRouter.post(
    "/deduplicate",
    summary="手动触发去重",
    description="基于名称+时间+地点的相似度自动去重合并",
)
async def deduplicate_controller(
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:update"]))
    ],
    similarity_threshold: Annotated[
        float, Query(description="相似度阈值(0-1)", ge=0.5, le=1.0)
    ] = 0.8,
) -> JSONResponse:
    """手动触发去重"""
    result_dict = await InfoCollectionService.deduplicate_service(
        auth=auth, similarity_threshold=similarity_threshold
    )
    log.info(f"手动去重完成: {result_dict}")
    return SuccessResponse(data=result_dict, msg="去重完成")


@InfoCollectionRouter.post(
    "/update-expired",
    summary="更新过期咨询会状态",
    description="将已过期的咨询会状态自动更新为expired",
)
async def update_expired_controller(
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_consultation:info_collection:update"]))
    ],
) -> JSONResponse:
    """更新过期咨询会状态"""
    result_dict = await InfoCollectionService.update_expired_service(auth=auth)
    log.info(f"更新过期咨询会状态完成: {result_dict}")
    return SuccessResponse(data=result_dict, msg="更新完成")


@InfoCollectionRouter.post(
    "/public-upload",
    summary="第三方免登录上传咨询会信息",
    description="支持第三方机构、高校、高中无需登录即可自助上传咨询会信息，上传后状态为待审核",
    response_model=ResponseSchema[InfoCollectionOutSchema],
)
async def public_upload_controller(
    data: ThirdPartyUploadSchema,
    source_type: Annotated[
        str, Query(description="上传来源(upload/high_school/university)")
    ] = "upload",
) -> JSONResponse:
    """第三方免登录上传咨询会信息"""
    from app.core.database import async_db_session

    from .model import InfoSource

    source_mapping = {
        "upload": InfoSource.UPLOAD.value,
        "high_school": InfoSource.HIGH_SCHOOL.value,
        "university": InfoSource.UNIVERSITY.value,
    }

    create_data = data.model_dump()
    create_data["source_type"] = source_mapping.get(source_type, InfoSource.UPLOAD.value)
    create_data["status"] = InfoStatus.PENDING.value

    # 免登录创建，使用系统session
    async with async_db_session() as db:
        from app.api.v1.module_system.auth.schema import AuthSchema as AuthSchemaType

        system_auth = AuthSchemaType(db=db, check_data_scope=False)
        create_schema = InfoCollectionCreateSchema(**create_data)
        result_dict = await InfoCollectionService.create_service(
            auth=system_auth, data=create_schema
        )

    log.info(f"第三方免登录上传咨询会信息成功，来源: {source_type}")
    return SuccessResponse(data=result_dict, msg="上传成功，请等待审核")


@InfoCollectionRouter.post(
    "/crawl",
    summary="手动触发爬虫抓取",
    description="手动触发咨询会信息爬虫抓取并保存到数据库",
)
async def crawl_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    """手动触发爬虫抓取（仅超级管理员）"""
    _require_superuser(auth)
    result_dict = await InfoCollectionService.crawl_and_save_service(
        auth=auth,
        crawler_names=["wechat_official_account"],
    )
    log.info(f"手动触发爬虫抓取完成: {result_dict}")
    return SuccessResponse(data=result_dict, msg="抓取完成")


def _require_superuser(auth: AuthSchema) -> None:
    if not auth.user or not auth.user.is_superuser:
        raise CustomException(msg="仅超级管理员可执行此操作", code=10403, status_code=403)


@InfoCollectionRouter.post(
    "/import/template",
    summary="下载全网抓取 Excel 导入模板",
    description="下载与业务表格列一致的 Excel 导入模板",
)
async def import_template_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> StreamResponse:
    """下载 Excel 导入模板（仅超级管理员）"""
    _require_superuser(auth)
    result = InfoCollectionService.import_template_bytes_service()
    log.info("下载全网抓取 Excel 模板成功")
    return StreamResponse(
        data=bytes2file_response(result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": (
                f"attachment; filename={urllib.parse.quote('全网抓取导入模板.xlsx')}"
            ),
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@InfoCollectionRouter.post(
    "/import/data",
    summary="Excel 导入全网抓取咨询会信息",
    description="按标准 Excel 列导入咨询会信息，来源标记为 crawler",
)
async def import_excel_controller(
    file: UploadFile,
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    """Excel 导入（仅超级管理员）"""
    _require_superuser(auth)
    result_dict = await InfoCollectionService.import_excel_service(auth=auth, file=file)
    log.info(f"Excel 导入完成: {result_dict}")
    msg = (
        f"导入完成：有效 {result_dict['total_rows']} 行，"
        f"保存 {result_dict['total_saved']} 条，"
        f"跳过重复 {result_dict['total_skipped']} 条"
    )
    if result_dict.get("total_failed"):
        msg += f"，失败 {result_dict['total_failed']} 条"
    return SuccessResponse(data=result_dict, msg=msg)


@InfoCollectionRouter.get(
    "/approved-options",
    summary="获取已审核咨询会下拉选项",
    description="获取已审核状态的咨询会列表（所有登录用户可查看，用于报名表单选择）",
    response_model=ResponseSchema[list[InfoCollectionSimpleOutSchema]],
)
async def get_approved_options_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user_scoped)],
) -> JSONResponse:
    """获取已审核咨询会下拉选项"""
    result_list = await InfoCollectionService.get_approved_list_service(auth=auth)
    log.info("获取已审核咨询会下拉选项成功")
    return SuccessResponse(data=result_list, msg="获取选项成功")
