from apscheduler.jobstores.base import JobLookupError

from app.core.ap_scheduler import SchedulerUtil
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException
from app.utils.cron_util import CronUtil

from .crud import NodeCRUD
from .schema import (
    NodeCreateSchema,
    NodeExecuteSchema,
    NodeOutSchema,
    NodeQueryParam,
    NodeUpdateSchema,
)


class NodeService:
    """节点管理模块服务层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def options(self) -> list[dict]:
        obj_list = await NodeCRUD(self.auth).get_obj_list_crud()
        return [
            {
                "id": obj.id,
                "name": obj.name,
                "code": obj.code,
                "func": obj.func,
                "args": obj.args,
                "kwargs": obj.kwargs,
            }
            for obj in obj_list
        ]

    async def detail(self, id: int) -> NodeOutSchema:
        obj = await NodeCRUD(self.auth).get_obj_by_id_crud(id=id)
        return NodeOutSchema.model_validate(obj)

    async def get_list(
        self,
        search: NodeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        obj_list = await NodeCRUD(self.auth).get_obj_list_crud(search=vars(search) if search else None, order_by=order_by)
        return [NodeOutSchema.model_validate(obj) for obj in obj_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: NodeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        return await NodeCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=NodeOutSchema,
        )

    async def create(self, data: NodeCreateSchema) -> NodeOutSchema:
        exist_obj = await NodeCRUD(self.auth).get(name=data.name)
        if exist_obj:
            raise CustomException(msg="创建失败，该节点已存在")

        obj = await NodeCRUD(self.auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return NodeOutSchema.model_validate(obj)

    async def update(self, id: int, data: NodeUpdateSchema) -> NodeOutSchema:
        exist_obj = await NodeCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg="更新失败，该节点不存在")

        obj = await NodeCRUD(self.auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败")
        return NodeOutSchema.model_validate(obj)

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for mid in ids:
            exist_obj = await NodeCRUD(self.auth).get_obj_by_id_crud(id=mid)
            if not exist_obj:
                raise CustomException(msg="删除失败，该节点不存在")
            try:
                SchedulerUtil.remove_job(job_id=mid)
            except JobLookupError:
                pass
        await NodeCRUD(self.auth).delete_obj_crud(ids=ids)

    async def clear(self) -> None:
        SchedulerUtil.clear_jobs()
        await NodeCRUD(self.auth).clear_obj_crud()

    async def execute(self, id: int, execute_data: NodeExecuteSchema) -> dict:
        obj = await NodeCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="调试失败，该节点不存在")

        trigger = execute_data.trigger
        trigger_args = execute_data.trigger_args
        start_date = execute_data.start_date
        end_date = execute_data.end_date

        if trigger == "now":
            SchedulerUtil.add_and_run_job_now(job_info=obj)
        elif trigger == "cron":
            if not trigger_args:
                raise CustomException(msg="Cron执行需要提供Cron表达式")
            if not CronUtil.validate_cron_expression(trigger_args):
                raise CustomException(msg=f"Cron表达式不正确: {trigger_args}")
            SchedulerUtil.add_cron_job(
                job_info=obj,
                trigger_args=trigger_args,
                start_date=start_date,
                end_date=end_date,
            )
        elif trigger == "interval":
            if not trigger_args:
                raise CustomException(msg="间隔执行需要提供间隔参数")
            SchedulerUtil.add_interval_job(
                job_info=obj,
                trigger_args=trigger_args,
                start_date=start_date,
                end_date=end_date,
            )
        elif trigger == "date":
            if not trigger_args:
                raise CustomException(msg="指定时间执行需要提供执行时间")
            SchedulerUtil.add_date_job(job_info=obj, run_date=trigger_args)
        else:
            raise CustomException(msg=f"不支持的触发方式: {trigger}")

        return {"job_id": id, "status": "executed", "trigger": trigger}

    async def batch_set_status(self, ids: list[int], status: int) -> None:
        if not ids:
            raise CustomException(msg="请选择要操作的数据")

        await NodeCRUD(self.auth).update_obj_crud(
            ids=ids,
            data={"status": status},
        )
