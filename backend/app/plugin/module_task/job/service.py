from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.ap_scheduler import SchedulerUtil
from app.core.exceptions import CustomException

from .crud import JobCRUD
from .schema import JobCreateSchema, JobOutSchema, JobQueryParam, JobUpdateSchema


class JobService:
    """
    调度器监控模块服务层

    职责:
    1. 执行日志的 CRUD 操作
    2. 调度器状态和任务列表的获取
    3. 任务操作（暂停、恢复、执行、移除）
    """

    @classmethod
    async def get_job_log_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取执行日志详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 日志ID

        返回:
        - Dict: 执行日志详情字典
        """
        obj = await JobCRUD(auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="执行日志不存在")
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_job_log_list_service(
        cls,
        auth: AuthSchema,
        search: JobQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取执行日志列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (JobQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数列表

        返回:
        - List[Dict]: 执行日志详情字典列表
        """
        if order_by is None:
            order_by = [{"created_time": "desc"}]
        obj_list = await JobCRUD(auth).get_obj_list_crud(
            search=search.__dict__ if search else None, order_by=order_by
        )
        return [JobOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_job_log_service(
        cls,
        auth: AuthSchema,
        job_id: str,
        job_name: str | None = None,
        trigger_type: str | None = None,
    ) -> dict:
        """
        创建执行日志

        参数:
        - auth (AuthSchema): 认证信息模型
        - job_id (str): 任务ID
        - job_name (str | None): 任务名称
        - trigger_type (str | None): 触发方式

        返回:
        - Dict: 执行日志详情字典
        """
        data = JobCreateSchema(
            job_id=job_id,
            job_name=job_name,
            trigger_type=trigger_type,
            status="running",
        )
        obj = await JobCRUD(auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建执行日志失败")
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_job_log_service(
        cls,
        auth: AuthSchema,
        id: int,
        status: str,
        result: str | None = None,
        error: str | None = None,
    ) -> dict:
        """
        更新执行日志

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 日志ID
        - status (str): 执行状态
        - result (str | None): 执行结果
        - error (str | None): 错误信息

        返回:
        - Dict: 执行日志详情字典
        """
        data = JobUpdateSchema(
            status=status,
            result=result,
            error=error,
        )
        obj = await JobCRUD(auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新执行日志失败")
        return JobOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_job_log_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除执行日志

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 日志ID列表
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        await JobCRUD(auth).delete_obj_crud(ids=ids)

    @classmethod
    async def clear_job_log_service(cls, auth: AuthSchema) -> None:
        """
        清空所有执行日志

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        await JobCRUD(auth).clear_obj_crud()

    @classmethod
    def get_scheduler_status_service(cls) -> dict:
        """
        获取调度器状态

        返回:
        - Dict: 调度器状态信息
        """
        status = SchedulerUtil.get_scheduler_state()
        is_running = SchedulerUtil.is_running()
        jobs = SchedulerUtil.get_all_jobs()

        return {
            "status": status,
            "is_running": is_running,
            "job_count": len(jobs),
        }

    @classmethod
    def get_scheduler_jobs_service(cls) -> list[dict]:
        """
        获取调度器中的任务列表

        返回:
        - List[Dict]: 任务列表
        """
        jobs = SchedulerUtil.get_all_jobs()
        return [
            {
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": str(job.next_run_time) if job.next_run_time else None,
                "status": SchedulerUtil.get_job_status(job_id=job.id),
            }
            for job in jobs
        ]
