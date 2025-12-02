# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from redis.asyncio.client import Redis

from app.common.request import PaginationService
from app.common.response import StreamResponse, SuccessResponse
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, redis_getter
from app.core.logger import log

from ..auth.schema import AuthSchema
from .schema import ParamsCreateSchema, ParamsUpdateSchema, ParamsQueryParam
from .service import ParamsService


ParamsRouter = APIRouter(route_class=OperationLogRoute, prefix="/param", tags=["参数管理"])

@ParamsRouter.get("/detail/{id}", summary="获取参数详情", description="获取参数详情")
async def get_type_detail_controller(
    id: int = Path(..., description="参数ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:query"]))
) -> JSONResponse:
    """
    获取参数详情
    
    参数:
    - id (int): 参数ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含参数详情的 JSON 响应
    """
    result_dict = await ParamsService.get_obj_detail_service(id=id, auth=auth)
    log.info(f"获取参数详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取参数详情成功")


@ParamsRouter.get("/key/{config_key}", summary="根据配置键获取参数详情", description="根据配置键获取参数详情")
async def get_obj_by_key_controller(
    config_key: str = Path(..., description="配置键"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:query"]))
) -> JSONResponse:
    """
    根据配置键获取参数详情
    
    参数:
    - config_key (str): 配置键
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含参数详情的 JSON 响应
    """
    result_dict = await ParamsService.get_obj_by_key_service(config_key=config_key, auth=auth)
    log.info(f"根据配置键获取参数详情成功 {config_key}")
    return SuccessResponse(data=result_dict, msg="根据配置键获取参数详情成功")


@ParamsRouter.get("/value/{config_key}", summary="根据配置键获取参数值", description="根据配置键获取参数值")
async def get_config_value_by_key_controller(
    config_key: str = Path(..., description="配置键"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:query"]))
) -> JSONResponse:
    """
    根据配置键获取参数值
    
    参数:
    - config_key (str): 配置键
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含参数值的 JSON 响应
    """
    result_value = await ParamsService.get_config_value_by_key_service(config_key=config_key, auth=auth)
    log.info(f"根据配置键获取参数值成功 {config_key}")
    return SuccessResponse(data=result_value, msg="根据配置键获取参数值成功")


@ParamsRouter.get("/list", summary="获取参数列表", description="获取参数列表")
async def get_obj_list_controller(
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:query"])),
    page: PaginationQueryParam = Depends(),
    search: ParamsQueryParam = Depends(),
) -> JSONResponse:
    """
    获取参数列表
    
    参数:
    - auth (AuthSchema): 认证信息模型
    - page (PaginationQueryParam): 分页查询参数模型
    - search (ParamsQueryParam): 参数查询参数模型
    
    返回:
    - JSONResponse: 包含参数列表的 JSON 响应
    """
    result_dict_list = await ParamsService.get_obj_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    log.info(f"获取参数列表成功")
    return SuccessResponse(data=result_dict, msg="查询参数列表成功")


@ParamsRouter.post("/create", summary="创建参数", description="创建参数")
async def create_obj_controller(
    data: ParamsCreateSchema,
    redis: Redis = Depends(redis_getter),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:create"]))
) -> JSONResponse:
    """
    创建参数
    
    参数:
    - data (ParamsCreateSchema): 参数创建模型
    - redis (Redis): Redis 客户端实例
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建参数结果的 JSON 响应
    """
    result_dict = await ParamsService.create_obj_service(auth=auth, redis=redis, data=data)
    log.info(f"创建参数成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建参数成功")


@ParamsRouter.put("/update/{id}", summary="修改参数", description="修改参数")
async def update_objs_controller(
    data: ParamsUpdateSchema,
    id: int = Path(..., description="参数ID"),
    redis: Redis = Depends(redis_getter), 
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:update"]))
) -> JSONResponse:
    """
    修改参数
    
    参数:
    - data (ParamsUpdateSchema): 参数更新模型
    - id (int): 参数ID
    - redis (Redis): Redis 客户端实例
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改参数结果的 JSON 响应
    """
    result_dict = await ParamsService.update_obj_service(auth=auth, redis=redis, id=id, data=data)
    log.info(f"更新参数成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="更新参数成功")


@ParamsRouter.delete("/delete", summary="删除参数", description="删除参数")
async def delete_obj_controller(
    redis: Redis = Depends(redis_getter),
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:delete"]))
) -> JSONResponse:
    """
    删除参数
    
    参数:
    - redis (Redis): Redis 客户端实例
    - ids (list[int]): 参数ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除参数结果的 JSON 响应
    """
    await ParamsService.delete_obj_service(auth=auth, redis=redis, ids=ids)
    log.info(f"删除参数成功: {ids}")
    return SuccessResponse(msg="删除参数成功")


@ParamsRouter.post('/export', summary="导出参数", description="导出参数")
async def export_obj_list_controller(
    search: ParamsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:param:export"]))
) -> StreamingResponse:
    """
    导出参数
    
    参数:
    - search (ParamsQueryParam): 参数查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 包含导出参数的 Excel 文件流响应
    """
    result_dict_list = await ParamsService.get_obj_list_service(search=search, auth=auth)
    export_result = await ParamsService.export_obj_service(data_list=result_dict_list)
    log.info('导出参数成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=params.xlsx'
        }
    )


@ParamsRouter.post("/upload", summary="上传文件", dependencies=[Depends(AuthPermission(["module_system:param:upload"]))])
async def upload_file_controller(
    file: UploadFile,
    request: Request
) -> JSONResponse:
    """
    上传文件
    
    参数:
    - file (UploadFile): 上传的文件对象
    - request (Request): 请求对象
    
    返回:
    - JSONResponse: 包含上传文件结果的 JSON 响应
    """
    result_str = await ParamsService.upload_service(base_url=str(request.base_url), file=file)
    log.info(f"上传文件: {result_str}")
    return SuccessResponse(data=result_str, msg='上传文件成功')


@ParamsRouter.get("/info", summary="获取初始化缓存参数", description="获取初始化缓存参数")
async def get_init_obj_controller(
    redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    """
    获取初始化缓存参数
    
    参数:
    - redis (Redis): Redis 客户端实例
    
    返回:
    - JSONResponse: 获取初始化缓存参数的 JSON 响应
    """
    result_dict = await ParamsService.get_init_config_service(redis=redis)
    log.info(f"获取初始化缓存参数成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="获取初始化缓存参数成功")