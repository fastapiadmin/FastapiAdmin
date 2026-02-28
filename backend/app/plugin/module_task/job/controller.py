from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.request import PaginationService
from app.common.response import ResponseSchema, SuccessResponse
from app.core.ap_scheduler import SchedulerUtil
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import JobOutSchema, JobQueryParam
from .service import JobService

JobRouter = APIRouter(route_class=OperationLogRoute, prefix="/job", tags=["调度器监控"])


# ==================== 调度器状态和操作 ====================


@JobRouter.get(
    "/scheduler/status",
    summary="获取调度器状态",
    description="获取调度器运行状态",
    response_model=ResponseSchema[dict],
    dependencies=[Depends(AuthPermission(["module_task:job:query"]))],
)
async def get_scheduler_status_controller() -> JSONResponse:
    """
    获取调度器状态

    返回:
    - JSONResponse: 调度器状态信息
    """
    data = JobService.get_scheduler_status_service()
    return SuccessResponse(data=data, msg="获取调度器状态成功")


@JobRouter.get(
    "/scheduler/jobs",
    summary="获取调度器任务列表",
    description="获取调度器中的任务列表",
    response_model=ResponseSchema[list[dict]],
    dependencies=[Depends(AuthPermission(["module_task:job:query"]))],
)
async def get_scheduler_jobs_controller() -> JSONResponse:
    """
    获取调度器中的任务列表

    返回:
    - JSONResponse: 调度器任务列表
    """
    data = JobService.get_scheduler_jobs_service()
    return SuccessResponse(data=data, msg="获取调度器任务列表成功")


@JobRouter.post(
    "/scheduler/start",
    summary="启动调度器",
    description="启动调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:scheduler"]))],
)
async def start_scheduler_controller() -> JSONResponse:
    """
    启动调度器
    """
    SchedulerUtil.start()
    log.info("调度器已启动")
    return SuccessResponse(msg="调度器已启动")


@JobRouter.post(
    "/scheduler/pause",
    summary="暂停调度器",
    description="暂停调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:scheduler"]))],
)
async def pause_scheduler_controller() -> JSONResponse:
    """
    暂停调度器
    """
    SchedulerUtil.pause()
    log.info("调度器已暂停")
    return SuccessResponse(msg="调度器已暂停")


@JobRouter.post(
    "/scheduler/resume",
    summary="恢复调度器",
    description="恢复调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:scheduler"]))],
)
async def resume_scheduler_controller() -> JSONResponse:
    """
    恢复调度器
    """
    SchedulerUtil.resume()
    log.info("调度器已恢复")
    return SuccessResponse(msg="调度器已恢复")


@JobRouter.post(
    "/scheduler/shutdown",
    summary="关闭调度器",
    description="关闭调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:scheduler"]))],
)
async def shutdown_scheduler_controller() -> JSONResponse:
    """
    关闭调度器
    """
    await SchedulerUtil.shutdown()
    log.info("调度器已关闭")
    return SuccessResponse(msg="调度器已关闭")


@JobRouter.delete(
    "/scheduler/jobs/clear",
    summary="清空所有任务",
    description="清空调度器中的所有任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:task"]))],
)
async def clear_jobs_controller() -> JSONResponse:
    """
    清空调度器中的所有任务
    """
    SchedulerUtil.clear_jobs()
    log.info("已清空所有任务")
    return SuccessResponse(msg="已清空所有任务")


@JobRouter.get(
    "/scheduler/console",
    summary="获取调度器控制台信息",
    description="获取调度器任务的控制台输出",
    response_model=ResponseSchema[str],
    dependencies=[Depends(AuthPermission(["module_task:job:query"]))],
)
async def get_scheduler_console_controller() -> JSONResponse:
    """
    获取调度器控制台信息

    返回:
    - JSONResponse: 调度器任务的控制台输出
    """
    console_output = SchedulerUtil.print_jobs()
    return SuccessResponse(data=console_output, msg="获取控制台信息成功")


@JobRouter.post(
    "/scheduler/sync",
    summary="同步调度器任务到数据库",
    description="将调度器中的任务同步到执行日志表",
    response_model=ResponseSchema[int],
    dependencies=[Depends(AuthPermission(["module_task:job:update"]))],
)
async def sync_jobs_controller() -> JSONResponse:
    """
    同步调度器任务到数据库

    返回:
    - JSONResponse: 同步的任务数量
    """
    sync_count = SchedulerUtil.sync_jobs_to_db()
    log.info(f"同步任务完成，共同步 {sync_count} 个任务")
    return SuccessResponse(data=sync_count, msg=f"同步完成，共同步 {sync_count} 个任务")


# ==================== 调度器任务操作 ====================


@JobRouter.post(
    "/task/pause/{job_id}",
    summary="暂停任务",
    description="暂停调度器中的任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:task"]))],
)
async def pause_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    """
    暂停调度器中的任务

    参数:
    - job_id (str): 调度器任务ID
    """
    SchedulerUtil.pause_job(job_id=job_id)
    log.info(f"暂停任务成功: {job_id}")
    return SuccessResponse(msg="暂停任务成功")


@JobRouter.post(
    "/task/resume/{job_id}",
    summary="恢复任务",
    description="恢复调度器中的任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:task"]))],
)
async def resume_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    """
    恢复调度器中的任务

    参数:
    - job_id (str): 调度器任务ID
    """
    SchedulerUtil.resume_job(job_id=job_id)
    log.info(f"恢复任务成功: {job_id}")
    return SuccessResponse(msg="恢复任务成功")


@JobRouter.post(
    "/task/run/{job_id}",
    summary="立即执行任务",
    description="立即执行调度器中的任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:task"]))],
)
async def run_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    """
    立即执行调度器中的任务

    参数:
    - job_id (str): 调度器任务ID
    """
    SchedulerUtil.run_job_now(job_id=job_id)
    log.info(f"立即执行任务成功: {job_id}")
    return SuccessResponse(msg="立即执行任务成功")


@JobRouter.delete(
    "/task/remove/{job_id}",
    summary="移除任务",
    description="从调度器中移除任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:job:delete"]))],
)
async def remove_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    """
    从调度器中移除任务

    参数:
    - job_id (str): 调度器任务ID
    """
    SchedulerUtil.remove_job(job_id=job_id)
    log.info(f"移除任务成功: {job_id}")
    return SuccessResponse(msg="移除任务成功")


# ==================== 执行日志 ====================


@JobRouter.get(
    "/log/list",
    summary="查询执行日志列表",
    description="查询执行日志列表",
    response_model=ResponseSchema[list[JobOutSchema]],
)
async def get_job_log_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[JobQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:job:query"]))],
) -> JSONResponse:
    """
    查询执行日志列表

    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (JobQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含分页后的执行日志列表
    """
    result_dict_list = await JobService.get_job_log_list_service(
        auth=auth, search=search
    )
    result_dict = await PaginationService.paginate(
        data_list=result_dict_list,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    log.info("查询执行日志列表成功")
    return SuccessResponse(data=result_dict, msg="查询执行日志列表成功")


@JobRouter.get(
    "/log/detail/{id}",
    summary="获取执行日志详情",
    description="获取执行日志详情",
    response_model=ResponseSchema[JobOutSchema],
)
async def get_job_log_detail_controller(
    id: Annotated[int, Path(description="日志ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:job:detail"]))],
) -> JSONResponse:
    """
    获取执行日志详情

    参数:
    - id (int): 日志ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含执行日志详情
    """
    result_dict = await JobService.get_job_log_detail_service(id=id, auth=auth)
    log.info(f"获取执行日志详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取执行日志详情成功")


@JobRouter.delete(
    "/log/delete",
    summary="删除执行日志",
    description="删除执行日志",
    response_model=ResponseSchema[None],
)
async def delete_job_log_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:job:delete"]))],
) -> JSONResponse:
    """
    删除执行日志

    参数:
    - ids (list[int]): ID列表
    - auth (AuthSchema): 认证信息模型
    """
    await JobService.delete_job_log_service(auth=auth, ids=ids)
    log.info(f"删除执行日志成功: {ids}")
    return SuccessResponse(msg="删除执行日志成功")
