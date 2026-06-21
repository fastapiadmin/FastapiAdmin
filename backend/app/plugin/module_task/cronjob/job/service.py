
from app.core.ap_scheduler import SchedulerUtil
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import JobCRUD
from .schema import JobCreateSchema, JobOutSchema, JobQueryParam, JobUpdateSchema


class JobService:
    """调度器监控模块服务层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def get_job_log_detail(self, id: int) -> JobOutSchema:
        obj = await JobCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="执行日志不存在")
        return JobOutSchema.model_validate(obj)

    async def get_job_log_list(
        self,
        search: JobQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        if order_by is None:
            order_by = [{"created_time": "desc"}]
        obj_list = await JobCRUD(self.auth).get_obj_list_crud(search=vars(search) if search else None, order_by=order_by)
        return [JobOutSchema.model_validate(obj) for obj in obj_list]

    async def get_job_log_page(
        self,
        page_no: int,
        page_size: int,
        search: JobQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        ob = order_by or [{"created_time": "desc"}]
        return await JobCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=ob,
            search=vars(search) if search else None,
            out_schema=JobOutSchema,
        )

    async def create_job_log(
        self,
        job_id: str,
        job_name: str | None = None,
        trigger_type: str | None = None,
    ) -> dict:
        data = JobCreateSchema(
            job_id=job_id,
            job_name=job_name,
            trigger_type=trigger_type,
            status=1,  # 执行中
        )
        obj = await JobCRUD(self.auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建执行日志失败")
        return JobOutSchema.model_validate(obj)

    async def update_job_log(
        self,
        id: int,
        status: int,
        result: str | None = None,
        error: str | None = None,
    ) -> dict:
        data = JobUpdateSchema(
            status=status,
            result=result,
            error=error,
        )
        obj = await JobCRUD(self.auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新执行日志失败")
        return JobOutSchema.model_validate(obj)

    async def delete_job_log(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        await JobCRUD(self.auth).delete_obj_crud(ids=ids)

    async def clear_job_log(self) -> None:
        await JobCRUD(self.auth).clear_obj_crud()

    @staticmethod
    def get_scheduler_status() -> dict:
        status = SchedulerUtil.get_scheduler_state()
        is_running = SchedulerUtil.is_running()
        jobs = SchedulerUtil.get_all_jobs()
        return {
            "status": status,
            "is_running": is_running,
            "job_count": len(jobs),
        }

    @staticmethod
    def get_scheduler_jobs() -> list[dict]:
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
