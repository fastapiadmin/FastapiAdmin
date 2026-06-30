from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.ap_scheduler import SchedulerUtil
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import JobOutSchema, JobQueryParam
from .service import JobService

JobRouter = APIRouter(route_class=OperationLogRoute, prefix="/cronjob/job", tags=["任务调度", "调度器监控"])


@JobRouter.get(
    "/scheduler/status",
    summary="获取调度器状态",
    response_model=ResponseSchema[dict],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:query"]))],
)
async def get_scheduler_status_controller() -> JSONResponse:
    data = JobService.get_scheduler_status()
    return SuccessResponse(data=data, msg="获取调度器状态成功")


@JobRouter.get(
    "/scheduler/jobs",
    summary="获取调度器任务列表",
    response_model=ResponseSchema[list[dict]],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:query"]))],
)
async def get_scheduler_jobs_controller() -> JSONResponse:
    data = JobService.get_scheduler_jobs()
    return SuccessResponse(data=data, msg="获取调度器任务列表成功")


@JobRouter.post(
    "/scheduler/start",
    summary="启动调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:scheduler"]))],
)
async def start_scheduler_controller() -> JSONResponse:
    SchedulerUtil.start()
    return SuccessResponse(msg="调度器已启动")


@JobRouter.post(
    "/scheduler/pause",
    summary="暂停调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:scheduler"]))],
)
async def pause_scheduler_controller() -> JSONResponse:
    SchedulerUtil.pause()
    return SuccessResponse(msg="调度器已暂停")


@JobRouter.post(
    "/scheduler/resume",
    summary="恢复调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:scheduler"]))],
)
async def resume_scheduler_controller() -> JSONResponse:
    SchedulerUtil.resume()
    return SuccessResponse(msg="调度器已恢复")


@JobRouter.post(
    "/scheduler/shutdown",
    summary="关闭调度器",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:scheduler"]))],
)
async def shutdown_scheduler_controller() -> JSONResponse:
    await SchedulerUtil.shutdown()
    return SuccessResponse(msg="调度器已关闭")


@JobRouter.delete(
    "/scheduler/jobs/clear",
    summary="清空所有任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:task"]))],
)
async def clear_jobs_controller() -> JSONResponse:
    SchedulerUtil.clear_jobs()
    return SuccessResponse(msg="已清空所有任务")


@JobRouter.get(
    "/scheduler/console",
    summary="获取调度器控制台信息",
    response_model=ResponseSchema[str],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:query"]))],
)
async def get_scheduler_console_controller() -> JSONResponse:
    console_output = SchedulerUtil.print_jobs()
    return SuccessResponse(data=console_output, msg="获取控制台信息成功")


@JobRouter.post(
    "/scheduler/sync",
    summary="同步调度器任务到数据库",
    response_model=ResponseSchema[int],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:update"]))],
)
async def sync_jobs_controller() -> JSONResponse:
    sync_count = SchedulerUtil.sync_jobs_to_db()
    return SuccessResponse(data=sync_count, msg=f"同步完成，共同步 {sync_count} 个任务")


@JobRouter.post(
    "/task/pause/{job_id}",
    summary="暂停任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:task"]))],
)
async def pause_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    SchedulerUtil.pause_job(job_id=job_id)
    return SuccessResponse(msg="暂停任务成功")


@JobRouter.post(
    "/task/resume/{job_id}",
    summary="恢复任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:task"]))],
)
async def resume_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    SchedulerUtil.resume_job(job_id=job_id)
    return SuccessResponse(msg="恢复任务成功")


@JobRouter.post(
    "/task/run/{job_id}",
    summary="立即执行任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:task"]))],
)
async def run_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    SchedulerUtil.run_job_now(job_id=job_id)
    return SuccessResponse(msg="立即执行任务成功")


@JobRouter.delete(
    "/task/remove/{job_id}",
    summary="移除任务",
    response_model=ResponseSchema[None],
    dependencies=[Depends(AuthPermission(["module_task:cronjob:job:delete"]))],
)
async def remove_job_controller(
    job_id: Annotated[str, Path(description="调度器任务ID")],
) -> JSONResponse:
    SchedulerUtil.remove_job(job_id=job_id)
    return SuccessResponse(msg="移除任务成功")


@JobRouter.get(
    "/log/list",
    summary="查询执行日志列表",
    response_model=ResponseSchema[PageResultSchema[JobOutSchema]],
)
async def get_job_log_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:job:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[JobQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    order_by = [{"created_time": "desc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await JobService(auth).get_job_log_page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询执行日志列表成功")


@JobRouter.get(
    "/log/detail/{id}",
    summary="获取执行日志详情",
    response_model=ResponseSchema[JobOutSchema],
)
async def get_job_log_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:job:detail"]))],
    id: Annotated[int, Path(description="日志ID")],
) -> JSONResponse:
    result_dict = await JobService(auth).get_job_log_detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取执行日志详情成功")


@JobRouter.delete(
    "/log/delete",
    summary="删除执行日志",
    response_model=ResponseSchema[None],
)
async def delete_job_log_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:job:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await JobService(auth).delete_job_log(ids=ids)
    return SuccessResponse(msg="删除执行日志成功")
