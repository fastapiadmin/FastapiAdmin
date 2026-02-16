from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteResultSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowRunCreateSchema,
    WorkflowRunLogOutSchema,
    WorkflowRunLogQueryParam,
    WorkflowRunOutSchema,
    WorkflowRunQueryParam,
    WorkflowRunUpdateSchema,
    WorkflowUpdateSchema,
    WorkflowValidateResultSchema,
    WorkflowValidateSchema,
)
from .service import WorkflowRunLogService, WorkflowRunService, WorkflowService

WorkflowRouter = APIRouter(route_class=OperationLogRoute, prefix="/workflow", tags=["工作流模块"])


@WorkflowRouter.get(
    "/detail/{id}",
    summary="获取工作流详情",
    description="获取工作流详情",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:detail"]))],
) -> JSONResponse:
    """
    获取工作流详情

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流详情的JSON响应
    """
    result_dict = await WorkflowService.detail_service(id=id, auth=auth)
    log.info(f"获取工作流详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取工作流详情成功")


@WorkflowRouter.get(
    "/list",
    summary="查询工作流列表",
    description="查询工作流列表",
    response_model=ResponseSchema[list[WorkflowOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:query"]))],
) -> JSONResponse:
    """
    查询工作流列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (WorkflowQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流列表分页信息的JSON响应
    """
    result_dict = await WorkflowService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询工作流列表成功")
    return SuccessResponse(data=result_dict, msg="查询工作流列表成功")


@WorkflowRouter.post(
    "/create",
    summary="创建工作流",
    description="创建工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def create_obj_controller(
    data: WorkflowCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:create"]))],
) -> JSONResponse:
    """
    创建工作流

    参数:
    - data (WorkflowCreateSchema): 工作流创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建工作流详情的JSON响应
    """
    result_dict = await WorkflowService.create_service(auth=auth, data=data)
    log.info(f"创建工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建工作流成功")


@WorkflowRouter.put(
    "/update/{id}",
    summary="修改工作流",
    description="修改工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def update_obj_controller(
    data: WorkflowUpdateSchema,
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:update"]))],
) -> JSONResponse:
    """
    修改工作流

    参数:
    - data (WorkflowUpdateSchema): 工作流更新模型
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改工作流详情的JSON响应
    """
    result_dict = await WorkflowService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改工作流成功")


@WorkflowRouter.delete(
    "/delete",
    summary="删除工作流",
    description="删除工作流",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:delete"]))],
) -> JSONResponse:
    """
    删除工作流

    参数:
    - ids (list[int]): 工作流ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除工作流详情的JSON响应
    """
    await WorkflowService.delete_service(auth=auth, ids=ids)
    log.info(f"删除工作流成功: {ids}")
    return SuccessResponse(msg="删除工作流成功")


@WorkflowRouter.post(
    "/publish/{id}",
    summary="发布工作流",
    description="发布工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def publish_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    data: WorkflowPublishSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:publish"]))],
) -> JSONResponse:
    """
    发布工作流

    参数:
    - id (int): 工作流ID
    - data (WorkflowPublishSchema): 发布模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含发布工作流详情的JSON响应
    """
    result_dict = await WorkflowService.publish_service(auth=auth, id=id, data=data)
    log.info(f"发布工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="发布工作流成功")


@WorkflowRouter.post(
    "/validate",
    summary="验证工作流",
    description="验证工作流",
    response_model=ResponseSchema[WorkflowValidateResultSchema],
)
async def validate_obj_controller(
    data: WorkflowValidateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:validate"]))],
) -> JSONResponse:
    """
    验证工作流

    参数:
    - data (WorkflowValidateSchema): 验证模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含验证结果的JSON响应
    """
    result_dict = await WorkflowService.validate_service(auth=auth, data=data)
    log.info("验证工作流成功")
    return SuccessResponse(data=result_dict.model_dump(), msg="验证工作流成功")


@WorkflowRouter.get(
    "/templates",
    summary="获取模板列表",
    description="获取模板列表",
    response_model=ResponseSchema[list[WorkflowOutSchema]],
)
async def get_templates_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:query"]))],
) -> JSONResponse:
    """
    获取模板列表

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含模板列表的JSON响应
    """
    result_dict = await WorkflowService.templates_service(auth=auth)
    log.info("获取模板列表成功")
    return SuccessResponse(data=result_dict, msg="获取模板列表成功")


@WorkflowRouter.get(
    "/export/{id}",
    summary="导出工作流",
    description="导出工作流",
    response_model=ResponseSchema[dict],
)
async def export_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:export"]))],
) -> JSONResponse:
    """
    导出工作流

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含导出工作流数据的JSON响应
    """
    result_dict = await WorkflowService.export_service(auth=auth, id=id)
    log.info(f"导出工作流成功: {id}")
    return SuccessResponse(data=result_dict, msg="导出工作流成功")


@WorkflowRouter.post(
    "/import",
    summary="导入工作流",
    description="导入工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def import_obj_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:import"]))],
) -> JSONResponse:
    """
    导入工作流

    参数:
    - data (dict): 工作流数据
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含导入工作流详情的JSON响应
    """
    result_dict = await WorkflowService.import_service(auth=auth, data=data)
    log.info(f"导入工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="导入工作流成功")


@WorkflowRouter.post(
    "/execute",
    summary="执行工作流",
    description="执行工作流",
    response_model=ResponseSchema[WorkflowExecuteResultSchema],
)
async def execute_obj_controller(
    data: WorkflowExecuteSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:execute"]))],
) -> JSONResponse:
    """
    执行工作流

    参数:
    - data (WorkflowExecuteSchema): 执行模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含执行结果的JSON响应
    """
    result_dict = await WorkflowService.execute_service(auth=auth, data=data)
    log.info(f"执行工作流成功: {result_dict.get('workflow_id')}")
    return SuccessResponse(data=result_dict, msg="执行工作流成功")


@WorkflowRouter.post(
    "/pause/{id}",
    summary="暂停工作流",
    description="暂停工作流",
    response_model=ResponseSchema[None],
)
async def pause_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:pause"]))],
) -> JSONResponse:
    """
    暂停工作流

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含暂停结果的JSON响应
    """
    await WorkflowService.pause_service(auth=auth, id=id)
    log.info(f"暂停工作流成功: {id}")
    return SuccessResponse(msg="暂停工作流成功")


@WorkflowRouter.post(
    "/resume/{id}",
    summary="恢复工作流",
    description="恢复工作流",
    response_model=ResponseSchema[None],
)
async def resume_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:resume"]))],
) -> JSONResponse:
    """
    恢复工作流

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含恢复结果的JSON响应
    """
    await WorkflowService.resume_service(auth=auth, id=id)
    log.info(f"恢复工作流成功: {id}")
    return SuccessResponse(msg="恢复工作流成功")


@WorkflowRouter.post(
    "/terminate/{id}",
    summary="终止工作流",
    description="终止工作流",
    response_model=ResponseSchema[None],
)
async def terminate_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:terminate"]))],
) -> JSONResponse:
    """
    终止工作流

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含终止结果的JSON响应
    """
    await WorkflowService.terminate_service(auth=auth, id=id)
    log.info(f"终止工作流成功: {id}")
    return SuccessResponse(msg="终止工作流成功")


@WorkflowRouter.get(
    "/run/list",
    summary="查询工作流运行记录列表",
    description="查询工作流运行记录列表",
    response_model=ResponseSchema[list[WorkflowRunOutSchema]],
)
async def get_workflow_run_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowRunQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:query"]))],
) -> JSONResponse:
    """
    查询工作流运行记录列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (WorkflowRunQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流运行记录列表的JSON响应
    """
    result_dict = await WorkflowRunService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search.__dict__ if search else None,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询工作流运行记录列表成功")


@WorkflowRouter.get(
    "/run/detail/{id}",
    summary="查询工作流运行记录详情",
    description="查询工作流运行记录详情",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def get_workflow_run_detail_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:query"]))],
) -> JSONResponse:
    """
    查询工作流运行记录详情

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流运行记录详情的JSON响应
    """
    result_dict = await WorkflowRunService.detail_service(auth=auth, id=id)
    return SuccessResponse(data=result_dict, msg="查询工作流运行记录详情成功")


@WorkflowRouter.post(
    "/run/create",
    summary="创建工作流运行记录",
    description="创建工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def create_workflow_run_controller(
    data: WorkflowRunCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:create"]))],
) -> JSONResponse:
    """
    创建工作流运行记录

    参数:
    - data (WorkflowRunCreateSchema): 创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.create_service(auth=auth, data=data)
    return SuccessResponse(data=result_dict, msg="创建工作流运行记录成功")


@WorkflowRouter.put(
    "/run/update/{id}",
    summary="更新工作流运行记录",
    description="更新工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def update_workflow_run_controller(
    id: int,
    data: WorkflowRunUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
) -> JSONResponse:
    """
    更新工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - data (WorkflowRunUpdateSchema): 更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.update_service(auth=auth, id=id, data=data)
    return SuccessResponse(data=result_dict, msg="更新工作流运行记录成功")


@WorkflowRouter.delete(
    "/run/delete",
    summary="删除工作流运行记录",
    description="删除工作流运行记录",
    response_model=ResponseSchema[None],
)
async def delete_workflow_run_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:delete"]))],
) -> JSONResponse:
    """
    删除工作流运行记录

    参数:
    - ids (list[int]): 工作流运行记录ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除结果的JSON响应
    """
    await WorkflowRunService.delete_service(auth=auth, ids=ids)
    return SuccessResponse(data=None, msg="删除工作流运行记录成功")


@WorkflowRouter.delete(
    "/run/clear",
    summary="清空工作流运行记录",
    description="清空工作流运行记录",
    response_model=ResponseSchema[None],
)
async def clear_workflow_run_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:delete"]))],
) -> JSONResponse:
    """
    清空工作流运行记录

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含清空结果的JSON响应
    """
    await WorkflowRunService.clear_service(auth=auth)
    return SuccessResponse(data=None, msg="清空工作流运行记录成功")


@WorkflowRouter.post(
    "/run/cancel/{id}",
    summary="取消工作流运行记录",
    description="取消工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def cancel_workflow_run_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
) -> JSONResponse:
    """
    取消工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含取消的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.cancel_service(auth=auth, id=id)
    return SuccessResponse(data=result_dict, msg="取消工作流运行记录成功")


@WorkflowRouter.post(
    "/run/retry/{id}",
    summary="重试工作流运行记录",
    description="重试工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def retry_workflow_run_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
    retry_count: int = 1,
) -> JSONResponse:
    """
    重试工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型
    - retry_count (int): 重试次数

    返回:
    - JSONResponse: 包含重试的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.retry_service(auth=auth, id=id, retry_count=retry_count)
    return SuccessResponse(data=result_dict, msg="重试工作流运行记录成功")


@WorkflowRouter.post(
    "/run/pause/{id}",
    summary="暂停工作流运行记录",
    description="暂停工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def pause_workflow_run_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
) -> JSONResponse:
    """
    暂停工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含暂停的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.pause_service(auth=auth, id=id)
    return SuccessResponse(data=result_dict, msg="暂停工作流运行记录成功")


@WorkflowRouter.post(
    "/run/resume/{id}",
    summary="恢复工作流运行记录",
    description="恢复工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def resume_workflow_run_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
) -> JSONResponse:
    """
    恢复工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含恢复的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.resume_service(auth=auth, id=id)
    return SuccessResponse(data=result_dict, msg="恢复工作流运行记录成功")


@WorkflowRouter.post(
    "/run/terminate/{id}",
    summary="终止工作流运行记录",
    description="终止工作流运行记录",
    response_model=ResponseSchema[WorkflowRunOutSchema],
)
async def terminate_workflow_run_controller(
    id: int,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:update"]))],
) -> JSONResponse:
    """
    终止工作流运行记录

    参数:
    - id (int): 工作流运行记录ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含终止的工作流运行记录的JSON响应
    """
    result_dict = await WorkflowRunService.terminate_service(auth=auth, id=id)
    return SuccessResponse(data=result_dict, msg="终止工作流运行记录成功")


@WorkflowRouter.get(
    "/run/log/list",
    summary="查询工作流运行日志列表",
    description="查询工作流运行日志列表",
    response_model=ResponseSchema[list[WorkflowRunLogOutSchema]],
)
async def get_workflow_run_log_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowRunLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:run:query"]))],
) -> JSONResponse:
    """
    查询工作流运行日志列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (WorkflowRunLogQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流运行日志列表的JSON响应
    """
    result_dict = await WorkflowRunLogService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search.__dict__ if search else None,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询工作流运行日志列表成功")
