from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, Form, Query, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from app.api.v1.module_common.file.service import FileService
from app.common.request import PaginationService
from app.common.response import ResponseSchema, StreamResponse, SuccessResponse, UploadFileResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import UploadResponseSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    ResourceCopySchema,
    ResourceCreateDirSchema,
    ResourceItemSchema,
    ResourceMoveSchema,
    ResourceRenameSchema,
    ResourceSearchQueryParam,
)
from .service import ResourceService

ResourceRouter = APIRouter(route_class=OperationLogRoute, prefix="/resource", tags=["系统监控", "资源管理"])


@ResourceRouter.get(
    "/list",
    summary="获取目录列表",
    response_model=ResponseSchema[list[ResourceItemSchema]],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:query"]))],
)
async def get_directory_list_controller(
    request: Request,
    page: Annotated[PaginationQueryParam, Query()],
    search: Annotated[ResourceSearchQueryParam, Query()],
) -> JSONResponse:
    result_dict_list = await ResourceService.get_resources_list(search=search, base_url=str(request.base_url))
    result_dict = await PaginationService.paginate(
        data_list=result_dict_list,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    return SuccessResponse(data=result_dict, msg="获取目录列表成功")


@ResourceRouter.post(
    "/upload",
    summary="上传文件",
    response_model=ResponseSchema[UploadResponseSchema],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:upload"]))],
)
async def upload_file_controller(
    request: Request,
    file: Annotated[UploadFile, File(description="上传文件")],
    target_path: Annotated[str | None, Form(description="目标目录路径")] = None,
) -> JSONResponse:
    result = await FileService.upload_service(
        base_url=str(request.base_url),
        file=file,
        upload_type="resource",
        target_path=target_path,
    )
    return SuccessResponse(data=result, msg="上传文件成功")


@ResourceRouter.get(
    "/download",
    summary="下载文件",
    dependencies=[Depends(AuthPermission(["module_monitor:resource:download"]))],
)
async def download_file_controller(
    path: Annotated[str, Query(description="文件路径")],
) -> FileResponse:
    file_path = await ResourceService.download_file(file_path=path)

    import os

    filename = os.path.basename(file_path)

    return UploadFileResponse(
        file_path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@ResourceRouter.delete(
    "/delete",
    summary="删除文件",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:delete"]))],
)
async def delete_files_controller(
    paths: Annotated[list[str], Body(description="文件路径列表")],
) -> JSONResponse:
    await ResourceService.delete_file(paths=paths)
    return SuccessResponse(msg="删除文件成功")


@ResourceRouter.post(
    "/move",
    summary="移动文件",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:move"]))],
)
async def move_file_controller(
    data: Annotated[ResourceMoveSchema, Body(description="移动文件参数")],
) -> JSONResponse:
    await ResourceService.move_file(data=data)
    return SuccessResponse(msg="移动文件成功")


@ResourceRouter.post(
    "/copy",
    summary="复制文件",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:copy"]))],
)
async def copy_file_controller(
    data: Annotated[ResourceCopySchema, Body(description="复制文件参数")],
) -> JSONResponse:
    await ResourceService.copy_file(data=data)
    return SuccessResponse(msg="复制文件成功")


@ResourceRouter.post(
    "/rename",
    summary="重命名文件",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:rename"]))],
)
async def rename_file_controller(
    data: Annotated[ResourceRenameSchema, Body(description="重命名文件参数")],
) -> JSONResponse:
    await ResourceService.rename_file(data=data)
    return SuccessResponse(msg="重命名文件成功")


@ResourceRouter.post(
    "/create-dir",
    summary="创建目录",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:create_dir"]))],
)
async def create_directory_controller(
    data: Annotated[ResourceCreateDirSchema, Body(description="创建目录参数")],
) -> JSONResponse:
    await ResourceService.create_directory(data=data)
    return SuccessResponse(msg="创建目录成功")


@ResourceRouter.post(
    "/export",
    summary="导出资源列表",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_monitor:resource:export"]))],
)
async def export_resource_list_controller(
    request: Request,
    search: Annotated[ResourceSearchQueryParam, Query()],
) -> StreamingResponse:
    result_dict_list = await ResourceService.get_resources_list(search=search, base_url=str(request.base_url))
    export_result = await ResourceService.export_resource(data_list=result_dict_list)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=resource_list.xlsx"},
    )
