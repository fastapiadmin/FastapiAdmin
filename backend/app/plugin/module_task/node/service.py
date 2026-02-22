from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.utils.cron_util import CronUtil
from app.core.ap_scheduler import SchedulerUtil

from .crud import NodeCRUD
from .schema import (
    NodeCreateSchema,
    NodeExecuteSchema,
    NodeOutSchema,
    NodeQueryParam,
    NodeUpdateSchema,
)


class NodeService:
    """
    节点管理模块服务层

    设计原则:
    1. 节点CRUD只操作数据库，不直接操作调度器
    2. 调度器节点通过"执行"操作来创建和管理
    3. 支持预设函数和自定义代码块两种执行方式
    """

    @classmethod
    async def get_node_options_service(cls, auth: AuthSchema) -> list[dict]:
        """
        获取节点类型选项列表，用于流程编排

        参数:
        - auth (AuthSchema): 认证信息模型

        返回:
        - list[dict]: 节点类型选项列表
        """
        obj_list = await NodeCRUD(auth).get_obj_list_crud()
        return [
            {
                "id": obj.id,
                "name": obj.name,
                "code": obj.code,
                "category": obj.category,
                "config_schema": obj.config_schema if obj.config_schema else {"fields": []},
                "func": obj.func,
                "args": obj.args,
                "kwargs": obj.kwargs,
            }
            for obj in obj_list
        ]

    @classmethod
    async def get_node_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取节点详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 节点ID

        返回:
        - Dict: 节点详情字典
        """
        obj = await NodeCRUD(auth).get_obj_by_id_crud(id=id)
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_node_list_service(
        cls,
        auth: AuthSchema,
        search: NodeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取节点列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (NodeQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数列表

        返回:
        - List[Dict]: 节点详情字典列表
        """
        obj_list = await NodeCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [NodeOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_node_service(cls, auth: AuthSchema, data: NodeCreateSchema) -> dict:
        """
        创建节点 - 只保存到数据库，不创建调度器任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (NodeCreateSchema): 节点创建模型

        返回:
        - Dict: 节点详情字典
        """
        exist_obj = await NodeCRUD(auth).get(name=data.name)
        if exist_obj:
            raise CustomException(msg="创建失败，该节点已存在")

        obj = await NodeCRUD(auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_node_service(cls, auth: AuthSchema, id: int, data: NodeUpdateSchema) -> dict:
        """
        更新节点 - 只更新数据库，不修改调度器任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 节点ID
        - data (NodeUpdateSchema): 节点更新模型

        返回:
        - dict: 节点详情字典
        """
        exist_obj = await NodeCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg="更新失败，该节点不存在")

        obj = await NodeCRUD(auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败")
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_node_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除节点 - 只删除数据库记录，同时移除调度器中的任务

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 节点ID列表
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            exist_obj = await NodeCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg="删除失败，该节点不存在")
            SchedulerUtil.remove_job(job_id=id)
        await NodeCRUD(auth).delete_obj_crud(ids=ids)

    @classmethod
    async def clear_node_service(cls, auth: AuthSchema) -> None:
        """
        清空所有节点

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        SchedulerUtil.clear_jobs()
        await NodeCRUD(auth).clear_obj_crud()

    @classmethod
    async def execute_node_service(cls, auth: AuthSchema, id: int, execute_data: NodeExecuteSchema) -> dict:
        """
        调试节点 - 根据任务配置创建调度器任务并执行

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 节点ID
        - execute_data (NodeExecuteSchema): 执行参数模型

        返回:
        - dict: 调试结果
        """
        obj = await NodeCRUD(auth).get_obj_by_id_crud(id=id)
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
