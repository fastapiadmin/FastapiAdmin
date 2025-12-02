# -*- coding: utf-8 -*-

import urllib.parse
from fastapi import APIRouter, Depends, Body, Path, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import StreamResponse, SuccessResponse
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.dependencies import db_getter, get_current_user, AuthPermission
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log

from ..auth.schema import AuthSchema
from .service import UserService
from .schema import (
    CurrentUserUpdateSchema,
    ResetPasswordSchema,
    UserCreateSchema,
    UserForgetPasswordSchema,
    UserRegisterSchema,
    UserUpdateSchema,
    UserChangePasswordSchema,
    UserQueryParam
)


UserRouter = APIRouter(route_class=OperationLogRoute, prefix="/user", tags=["用户管理"])


@UserRouter.get("/current/info", summary="查询当前用户信息", description="查询当前用户信息")
async def get_current_user_info_controller(
    auth: AuthSchema = Depends(get_current_user)
) -> JSONResponse:
    """
    查询当前用户信息
    
    参数:
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 当前用户信息JSON响应
    """
    result_dict = await UserService.get_current_user_info_service(auth=auth)
    log.info(f"获取当前用户信息成功")
    return SuccessResponse(data=result_dict, msg='获取当前用户信息成功')


@UserRouter.post("/current/avatar/upload", summary="上传当前用户头像", dependencies=[Depends(get_current_user)])
async def user_avatar_upload_controller(
    file: UploadFile, 
    request: Request
) -> JSONResponse:
    """
    上传当前用户头像
    
    参数:
    - file (UploadFile): 上传的文件
    - request (Request): 请求对象
    
    返回:
    - JSONResponse: 上传头像JSON响应
    """
    result_str = await UserService.upload_avatar_service(base_url=str(request.base_url), file=file)
    log.info(f"上传头像成功: {result_str}")
    return SuccessResponse(data=result_str, msg='上传头像成功')


@UserRouter.put("/current/info/update", summary="更新当前用户基本信息", description="更新当前用户基本信息")
async def update_current_user_info_controller(
    data: CurrentUserUpdateSchema,
    auth: AuthSchema = Depends(get_current_user)
) -> JSONResponse:
    """
    更新当前用户基本信息
    
    参数:
    - data (CurrentUserUpdateSchema): 当前用户更新模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 更新当前用户基本信息JSON响应
    """
    result_dict = await UserService.update_current_user_info_service(data=data, auth=auth)
    log.info(f"更新当前用户基本信息成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg='更新当前用户基本信息成功')


@UserRouter.put("/current/password/change", summary="修改当前用户密码", description="修改当前用户密码")
async def change_current_user_password_controller(
    data: UserChangePasswordSchema,
    auth: AuthSchema = Depends(get_current_user)
) -> JSONResponse:
    """
    修改当前用户密码
    
    参数:
    - data (UserChangePasswordSchema): 用户密码修改模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 修改密码JSON响应
    """
    result_dict = await UserService.change_user_password_service(data=data, auth=auth)
    log.info(f"修改密码成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg='修改密码成功, 请重新登录')

@UserRouter.put("/reset/password", summary="重置密码", description="重置密码")
async def reset_password_controller(
    data: ResetPasswordSchema,
    auth: AuthSchema = Depends(get_current_user)
) -> JSONResponse:
    """
    重置密码
    
    参数:
    - data (ResetPasswordSchema): 重置密码模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 重置密码JSON响应
    """
    result_dict = await UserService.reset_user_password_service(data=data, auth=auth)
    log.info(f"重置密码成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg='重置密码成功')

@UserRouter.post('/register', summary="注册用户", description="注册用户")
async def register_user_controller(
    data: UserRegisterSchema, 
    db: AsyncSession = Depends(db_getter),
) -> JSONResponse:
    """
    注册用户
    
    参数:
    - data (UserRegisterSchema): 用户注册模型
    - db (AsyncSession): 异步数据库会话
    
    返回:
    - JSONResponse: 注册用户JSON响应
    """
    auth = AuthSchema(db=db)
    user_register_result = await UserService.register_user_service(data=data, auth=auth)
    log.info(f"{data.username} 注册用户成功: {user_register_result}")
    return SuccessResponse(data=user_register_result, msg='注册用户成功')


@UserRouter.post('/forget/password', summary="忘记密码", description="忘记密码")
async def forget_password_controller(
    data: UserForgetPasswordSchema, 
    db: AsyncSession = Depends(db_getter),
) -> JSONResponse:
    """
    忘记密码
    
    参数:
    - data (UserForgetPasswordSchema): 用户忘记密码模型
    - db (AsyncSession): 异步数据库会话
    
    返回:
    - JSONResponse: 忘记密码JSON响应
    """
    auth = AuthSchema(db=db)
    user_forget_password_result = await UserService.forget_password_service(data=data, auth=auth)
    log.info(f"{data.username} 重置密码成功: {user_forget_password_result}")
    return SuccessResponse(data=user_forget_password_result, msg='重置密码成功')


@UserRouter.get("/list", summary="查询用户", description="查询用户")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: UserQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:query"])),
) -> JSONResponse:
    """
    查询用户
    
    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (UserQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 分页查询结果JSON响应
    """
    result_dict_list = await UserService.get_user_list_service(search=search, auth=auth, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    log.info(f"查询用户成功")
    return SuccessResponse(data=result_dict, msg="查询用户成功")


@UserRouter.get("/detail/{id}", summary="查询用户详情", description="查询用户详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="用户ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:query"])),
) -> JSONResponse:
    """
    查询用户详情
    
    参数:
    - id (int): 用户ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 用户详情JSON响应
    """
    result_dict = await UserService.get_detail_by_id_service(id=id, auth=auth)
    log.info(f"获取用户详情成功 {id}")
    return SuccessResponse(data=result_dict, msg='获取用户详情成功')


@UserRouter.post("/create", summary="创建用户", description="创建用户")
async def create_obj_controller(
    data: UserCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:create"])),
) -> JSONResponse:
    """
    创建用户
    
    **注意**:
    - 创建用户时, 默认密码为: <PASSWORD>
    - 创建用户时, 默认用户状态为: 启用
    
    参数:
    - data (UserCreateSchema): 用户创建模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 创建用户JSON响应
    """
    result_dict = await UserService.create_user_service(data=data, auth=auth)
    log.info(f"创建用户成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建用户成功")


@UserRouter.put("/update/{id}", summary="修改用户", description="修改用户")
async def update_obj_controller(
    data: UserUpdateSchema,
    id: int = Path(..., description="用户ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:update"])),
) -> JSONResponse:
    """
    修改用户
    
    参数:
    - data (UserUpdateSchema): 用户修改模型
    - id (int): 用户ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 修改用户JSON响应
    """
    result_dict = await UserService.update_user_service(id=id, data=data, auth=auth)
    log.info(f"修改用户成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改用户成功")


@UserRouter.delete("/delete", summary="删除用户", description="删除用户")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:delete"])),
) -> JSONResponse:
    """
    删除用户
    
    参数:
    - ids (list[int]): 用户ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 删除用户JSON响应
    """
    await UserService.delete_user_service(ids=ids, auth=auth)
    log.info(f"删除用户成功: {ids}")
    return SuccessResponse(msg="删除用户成功")


@UserRouter.patch("/available/setting", summary="批量修改用户状态", description="批量修改用户状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:patch"])),
) -> JSONResponse:
    """
    批量修改用户状态
    
    参数:
    - data (BatchSetAvailable): 批量修改用户状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 批量修改用户状态JSON响应
    """
    await UserService.set_user_available_service(data=data, auth=auth)
    log.info(f"批量修改用户状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改用户状态成功")


@UserRouter.post('/import/template', summary="获取用户导入模板", description="获取用户导入模板", dependencies=[Depends(AuthPermission(["module_system:user:import"]))])
async def export_obj_template_controller()-> StreamingResponse:
    """
    获取用户导入模板
    
    返回:
    - StreamingResponse: 用户导入模板流响应
    """
    user_import_template_result = await UserService.get_import_template_user_service()
    log.info('获取用户导入模板成功')

    return StreamResponse(
        data=bytes2file_response(user_import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': f'attachment; filename={urllib.parse.quote("用户导入模板.xlsx")}',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
    )


@UserRouter.post('/export', summary="导出用户", description="导出用户")
async def export_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: UserQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:export"])),
) -> StreamingResponse:
    """
    导出用户
    
    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (UserQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 用户导出模板流响应
    """
    user_list = await UserService.get_user_list_service(auth=auth, search=search, order_by=page.order_by)
    user_export_result = await UserService.export_user_list_service(user_list)
    log.info('导出用户成功')

    return StreamResponse(
        data=bytes2file_response(user_export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=user.xlsx'
        }
    )


@UserRouter.post('/import/data', summary="导入用户", description="导入用户")
async def import_obj_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_system:user:import"]))
) -> JSONResponse:
    """
    导入用户
    
    参数:
    - file (UploadFile): 用户导入文件
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 导入用户JSON响应
    """
    batch_import_result = await UserService.batch_import_user_service(file=file, auth=auth, update_support=True)
    log.info(f"导入用户成功: {batch_import_result}")
    return SuccessResponse(data=batch_import_result, msg="导入用户成功")
