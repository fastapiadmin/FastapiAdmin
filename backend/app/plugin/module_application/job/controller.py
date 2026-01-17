from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.request import PaginationService
from app.common.response import ErrorResponse, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    JobCreateSchema,
    JobLogQueryParam,
    JobQueryParam,
    JobUpdateSchema,
)
from .service import JobLogService, JobService
from .tools.ap_scheduler import SchedulerUtil

JobRouter = APIRouter(route_class=OperationLogRoute, prefix="/job", tags=["定时任务"])


@JobRouter.get("/detail/{id}", summary="获取定时任务详情", description="获取定时任务详情")
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="定时任务ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:detail"]))],
) -> JSONResponse:
    """
    获取定时任务详情

    参数:
    - id (int): 定时任务ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含定时任务详情的JSON响应
    """
    result_dict = await JobService.get_job_detail_service(id=id, auth=auth)
    log.info(f"获取定时任务详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取定时任务详情成功")


@JobRouter.get("/list", summary="查询定时任务", description="查询定时任务")
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[JobQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:query"]))],
) -> JSONResponse:
    """
    查询定时任务

    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (JobQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含分页后的定时任务列表的JSON响应
    """
    result_dict_list = await JobService.get_job_list_service(
        auth=auth, search=search, order_by=page.order_by
    )
    result_dict = await PaginationService.paginate(
        data_list=result_dict_list,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    log.info("查询定时任务列表成功")
    return SuccessResponse(data=result_dict, msg="查询定时任务列表成功")


@JobRouter.post("/create", summary="创建定时任务", description="创建定时任务")
async def create_obj_controller(
    data: JobCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:create"]))],
) -> JSONResponse:
    """
    创建定时任务

    参数:
    - data (JobCreateSchema): 创建参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建定时任务结果的JSON响应
    """
    result_dict = await JobService.create_job_service(auth=auth, data=data)
    log.info(f"创建定时任务成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建定时任务成功")


@JobRouter.put("/update/{id}", summary="修改定时任务", description="修改定时任务")
async def update_obj_controller(
    data: JobUpdateSchema,
    id: Annotated[int, Path(description="定时任务ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:update"]))],
) -> JSONResponse:
    """
    修改定时任务

    参数:
    - data (JobUpdateSchema): 更新参数模型
    - id (int): 定时任务ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改定时任务结果的JSON响应
    """
    result_dict = await JobService.update_job_service(auth=auth, id=id, data=data)
    log.info(f"修改定时任务成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改定时任务成功")


@JobRouter.delete("/delete", summary="删除定时任务", description="删除定时任务")
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:delete"]))],
) -> JSONResponse:
    """
    删除定时任务

    参数:
    - ids (list[int]): ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除定时任务结果的JSON响应
    """
    await JobService.delete_job_service(auth=auth, ids=ids)
    log.info(f"删除定时任务成功: {ids}")
    return SuccessResponse(msg="删除定时任务成功")


@JobRouter.post("/export", summary="导出定时任务", description="导出定时任务")
async def export_obj_list_controller(
    search: Annotated[JobQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:export"]))],
) -> StreamingResponse:
    """
    导出定时任务

    参数:
    - search (JobQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - StreamingResponse: 包含导出定时任务结果的流式响应
    """
    result_dict_list = await JobService.get_job_list_service(search=search, auth=auth)
    export_result = await JobService.export_job_service(data_list=result_dict_list)
    log.info("导出定时任务成功")

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=job.xlsx"},
    )


@JobRouter.delete("/clear", summary="清空定时任务日志", description="清空定时任务日志")
async def clear_obj_log_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:delete"]))],
) -> JSONResponse:
    """
    清空定时任务日志

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含清空定时任务结果的JSON响应
    """
    await JobService.clear_job_service(auth=auth)
    log.info("清空定时任务成功")
    return SuccessResponse(msg="清空定时任务成功")


@JobRouter.put(
    "/option",
    summary="暂停/恢复/重启定时任务",
    description="暂停/恢复/重启定时任务",
)
async def option_obj_controller(
    id: Annotated[int, Body(description="定时任务ID")],
    option: Annotated[int, Body(description="操作类型 1: 暂停 2: 恢复 3: 重启")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:update"]))],
) -> JSONResponse:
    """
    暂停/恢复/重启定时任务

    参数:
    - id (int): 定时任务ID
    - option (int): 操作类型 1: 暂停 2: 恢复 3: 重启
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含操作定时任务结果的JSON响应
    """
    await JobService.option_job_service(auth=auth, id=id, option=option)
    log.info(f"操作定时任务成功: {id}")
    return SuccessResponse(msg="操作定时任务成功")


@JobRouter.get(
    "/log",
    summary="获取定时任务日志",
    description="获取定时任务日志",
    dependencies=[Depends(AuthPermission(["module_application:job:query"]))],
)
async def get_job_log_controller():
    """
    获取定时任务日志

    返回:
    - JSONResponse: 获取定时任务日志的JSON响应
    """
    data = [
        {
            "id": i.id,
            "name": i.name,
            "trigger": i.trigger.__class__.__name__,
            "executor": i.executor,
            "func": i.func,
            "func_ref": i.func_ref,
            "args": i.args,
            "kwargs": i.kwargs,
            "misfire_grace_time": i.misfire_grace_time,
            "coalesce": i.coalesce,
            "max_instances": i.max_instances,
            "next_run_time": i.next_run_time,
            "state": SchedulerUtil.get_single_job_status(job_id=i.id),
        }
        for i in SchedulerUtil.get_all_jobs()
    ]

    return SuccessResponse(msg="获取定时任务日志成功", data=data)


# 定时任务日志管理接口
@JobRouter.get(
    "/log/detail/{id}",
    summary="获取定时任务日志详情",
    description="获取定时任务日志详情",
)
async def get_job_log_detail_controller(
    id: Annotated[int, Path(description="定时任务日志ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:query"]))],
) -> JSONResponse:
    """
    获取定时任务日志详情

    参数:
    - id (int): 定时任务日志ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 获取定时任务日志详情的JSON响应
    """
    result_dict = await JobLogService.get_job_log_detail_service(id=id, auth=auth)
    log.info(f"获取定时任务日志详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取定时任务日志详情成功")


@JobRouter.get("/log/list", summary="查询定时任务日志", description="查询定时任务日志")
async def get_job_log_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[JobLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:query"]))],
) -> JSONResponse:
    """
    查询定时任务日志

    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (JobLogQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 查询定时任务日志列表的JSON响应
    """
    order_by = [{"created_time": "desc"}]
    result_dict_list = await JobLogService.get_job_log_list_service(
        auth=auth, search=search, order_by=order_by
    )
    result_dict = await PaginationService.paginate(
        data_list=result_dict_list,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    log.info("查询定时任务日志列表成功")
    return SuccessResponse(data=result_dict, msg="查询定时任务日志列表成功")


@JobRouter.delete("/log/delete", summary="删除定时任务日志", description="删除定时任务日志")
async def delete_job_log_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:delete"]))],
) -> JSONResponse:
    """
    删除定时任务日志

    参数:
    - ids (list[int]): ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除定时任务日志结果的JSON响应
    """
    await JobLogService.delete_job_log_service(auth=auth, ids=ids)
    log.info(f"删除定时任务日志成功: {ids}")
    return SuccessResponse(msg="删除定时任务日志成功")


@JobRouter.delete("/log/clear", summary="清空定时任务日志", description="清空定时任务日志")
async def clear_job_log_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:delete"]))],
) -> JSONResponse:
    """
    清空定时任务日志

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含清空定时任务日志结果的JSON响应
    """
    await JobLogService.clear_job_log_service(auth=auth)
    log.info("清空定时任务日志成功")
    return SuccessResponse(msg="清空定时任务日志成功")


@JobRouter.post("/log/export", summary="导出定时任务日志", description="导出定时任务日志")
async def export_job_log_list_controller(
    search: Annotated[JobLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:export"]))],
) -> StreamingResponse:
    """
    导出定时任务日志

    参数:
    - search (JobLogQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - StreamingResponse: 包含导出定时任务日志结果的流式响应
    """
    result_dict_list = await JobLogService.get_job_log_list_service(search=search, auth=auth)
    export_result = await JobLogService.export_job_log_service(data_list=result_dict_list)
    log.info("导出定时任务日志成功")

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=job_log.xlsx"},
    )


@JobRouter.put(
    "/run/{id}",
    summary="立即执行定时任务",
    description="立即执行指定的定时任务",
)
async def run_job_now_controller(
    id: Annotated[int, Path(description="定时任务ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:job:update"]))],
) -> JSONResponse:
    """
    立即执行定时任务

    参数:
    - id (int): 定时任务ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含操作结果的JSON响应
    """
    try:
        SchedulerUtil.run_job_now(job_id=id)
        log.info(f"立即执行定时任务成功: {id}")
        return SuccessResponse(msg="立即执行定时任务成功")
    except Exception as e:
        log.error(f"立即执行定时任务失败: {id}, 错误信息: {e!s}")
        return ErrorResponse(msg=f"立即执行定时任务失败: {e!s}")
