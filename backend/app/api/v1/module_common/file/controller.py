# -*- coding: utf-8 -*-

from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Body, Depends, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse

from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.common.response import SuccessResponse, UploadFileResponse
from app.core.router_class import OperationLogRoute
from app.utils.upload_util import UploadUtil

from .service import FileService


FileRouter = APIRouter(route_class=OperationLogRoute, prefix="/file", tags=["文件管理"])

@FileRouter.post("/upload", summary="上传文件", description="上传文件",dependencies=[Depends(AuthPermission(["module_common:file:upload"]))])
async def upload_controller(
    file: UploadFile,
    request: Request,
) -> JSONResponse:
    """
    上传文件
    
    参数:
    - file (UploadFile): 上传的文件
    - request (Request): 请求对象
    
    返回:
    - JSONResponse: 包含上传文件详情的JSON响应
    """
    result_dict = await FileService.upload_service(base_url=str(request.base_url), file=file)
    log.info(f"上传文件成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="上传文件成功")

@FileRouter.post("/download", summary="下载文件", description="下载文件", dependencies=[Depends(AuthPermission(["module_common:file:download"]))])
async def download_controller(
    background_tasks: BackgroundTasks,
    file_path: str = Body(..., description="文件路径"), 
    delete: bool = Body(False, description="是否删除文件"),
) -> FileResponse:
    """
    下载文件
    
    参数:
    - background_tasks (BackgroundTasks): 后台任务对象
    - file_path (str): 文件路径
    - delete (bool): 是否删除文件
    
    返回:
    - FileResponse: 包含下载文件的响应
    """
    result = await FileService.download_service(file_path=file_path)
    if delete:
        background_tasks.add_task(UploadUtil.delete_file, Path(file_path))
    log.info(f"下载文件成功")
    return UploadFileResponse(file_path=result.file_path, filename=result.file_name)
