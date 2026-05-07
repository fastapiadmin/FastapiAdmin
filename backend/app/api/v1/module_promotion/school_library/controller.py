"""
全国高中学校库 - 控制器
"""

import urllib.parse
from typing import Annotated

from fastapi import APIRouter, Depends, Path, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    SchoolLibraryCreateSchema,
    SchoolLibraryOutSchema,
    SchoolLibraryQuerySchema,
    SchoolLibraryUpdateSchema,
)
from .service import SchoolLibraryService

SchoolLibraryRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/school-library",
    tags=["招生宣传活动 - 全国高中学校库"],
)


@SchoolLibraryRouter.get(
    "/detail/{id}",
    summary="获取学校详情",
    description="获取学校详情",
    response_model=ResponseSchema[SchoolLibraryOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="学校ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:detail"]))
    ],
) -> JSONResponse:
    """获取学校详情"""
    result_dict = await SchoolLibraryService.detail_service(auth=auth, id=id)
    log.info(f"获取学校详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@SchoolLibraryRouter.get(
    "/list",
    summary="查询学校列表",
    description="查询学校列表",
    response_model=ResponseSchema[list[SchoolLibraryOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[SchoolLibraryQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:school_library:query"]))],
) -> JSONResponse:
    """查询学校列表"""
    result_dict = await SchoolLibraryService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询学校列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@SchoolLibraryRouter.post(
    "/create",
    summary="创建学校",
    description="创建学校",
    response_model=ResponseSchema[SchoolLibraryOutSchema],
)
async def create_obj_controller(
    data: SchoolLibraryCreateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:create"]))
    ],
) -> JSONResponse:
    """创建学校"""
    result_dict = await SchoolLibraryService.create_service(auth=auth, data=data)
    log.info("创建学校成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@SchoolLibraryRouter.put(
    "/update/{id}",
    summary="更新学校",
    description="更新学校",
    response_model=ResponseSchema[SchoolLibraryOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="学校ID")],
    data: SchoolLibraryUpdateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:update"]))
    ],
) -> JSONResponse:
    """更新学校"""
    result_dict = await SchoolLibraryService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新学校成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@SchoolLibraryRouter.delete(
    "/delete/{id}",
    summary="删除学校",
    description="删除学校",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="学校ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:delete"]))
    ],
) -> JSONResponse:
    """删除学校"""
    await SchoolLibraryService.delete_service(auth=auth, id=id)
    log.info(f"删除学校成功 {id}")
    return SuccessResponse(msg="删除成功")


@SchoolLibraryRouter.delete(
    "/batch-delete",
    summary="批量删除学校",
    description="批量删除学校",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:delete"]))
    ],
) -> JSONResponse:
    """批量删除学校"""
    await SchoolLibraryService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除学校成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@SchoolLibraryRouter.post(
    "/import/template",
    summary="获取学校库导入模板",
    description="获取学校库导入模板",
    dependencies=[Depends(AuthPermission(["module_promotion:school_library:download"]))],
)
async def export_obj_template_controller() -> StreamingResponse:
    """获取学校库导入模板"""
    result = await SchoolLibraryService.import_template_download_service()
    log.info("获取学校库导入模板成功")

    return StreamResponse(
        data=bytes2file_response(result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={urllib.parse.quote('学校库导入模板.xlsx')}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@SchoolLibraryRouter.post(
    "/import/data",
    summary="导入学校库",
    description="导入学校库",
    response_model=ResponseSchema,
)
async def import_obj_list_controller(
    file: UploadFile,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:school_library:import"]))
    ],
) -> JSONResponse:
    """导入学校库"""
    result = await SchoolLibraryService.batch_import_service(
        file=file, auth=auth, update_support=True
    )
    log.info(f"导入学校库成功: {result}")
    return SuccessResponse(data=result, msg="导入学校库成功")
