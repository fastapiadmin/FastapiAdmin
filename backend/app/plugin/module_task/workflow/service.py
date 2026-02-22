
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import WorkflowCRUD
from .engine import WorkflowEngine
from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)


class WorkflowService:
    """
    工作流管理模块服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID

        返回:
        - dict: 工作流模型实例字典
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该工作流不存在")
        return WorkflowOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (WorkflowQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "asc"}]
        offset = (page_no - 1) * page_size

        result = await WorkflowCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: WorkflowCreateSchema) -> dict:
        """
        创建

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (WorkflowCreateSchema): 工作流创建模型

        返回:
        - dict: 工作流模型实例字典
        """
        obj = await WorkflowCRUD(auth).get_by_code_crud(code=data.code)
        if obj:
            raise CustomException(msg="创建失败，流程编码已存在")

        obj = await WorkflowCRUD(auth).create_crud(data=data)
        return WorkflowOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: WorkflowUpdateSchema) -> dict:
        """
        更新

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID
        - data (WorkflowUpdateSchema): 工作流更新模型

        返回:
        - dict: 工作流模型实例字典
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该工作流不存在")

        if data.code:
            exist_obj = await WorkflowCRUD(auth).get_by_code_crud(code=data.code)
            if exist_obj and exist_obj.id != id:
                raise CustomException(msg="更新失败，流程编码重复")

        obj = await WorkflowCRUD(auth).update_crud(id=id, data=data)
        return WorkflowOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 工作流ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        obj_list = await WorkflowCRUD(auth).list_crud(search={"id": (None, ids)})

        if len(obj_list) != len(ids):
            existing_ids = {obj.id for obj in obj_list}
            missing_ids = set(ids) - existing_ids
            raise CustomException(msg=f"删除失败，ID为{missing_ids}的工作流不存在")

        await WorkflowCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def publish_service(cls, auth: AuthSchema, id: int, data: WorkflowPublishSchema) -> dict:
        """
        发布工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID
        - data (WorkflowPublishSchema): 发布模型

        返回:
        - dict: 工作流模型实例字典
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="发布失败，该工作流不存在")

        if obj.status == "published":
            raise CustomException(msg="发布失败，该工作流已发布")

        update_data = WorkflowUpdateSchema(
            status="published",
        )

        obj = await WorkflowCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def execute_service(cls, auth: AuthSchema, data: WorkflowExecuteSchema) -> dict:
        """
        执行工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (WorkflowExecuteSchema): 执行模型

        返回:
        - dict: 执行结果
        """
        workflow = await WorkflowCRUD(auth).get_by_id_crud(id=data.workflow_id)
        if not workflow:
            raise CustomException(msg="工作流不存在")

        if workflow.status != "published":
            raise CustomException(msg="工作流未发布，无法执行")

        context = await WorkflowEngine.execute(
            workflow=workflow,
            variables=data.variables,
            business_key=data.business_key,
        )

        return {
            "workflow_id": data.workflow_id,
            "workflow_name": workflow.name,
            "status": context.status,
            "start_time": context.start_time.isoformat() if context.start_time else None,
            "end_time": context.end_time.isoformat() if context.end_time else None,
            "variables": context.variables,
            "node_results": {
                node_id: {
                    "status": ctx.status,
                    "output": ctx.output_data,
                    "error": ctx.error,
                }
                for node_id, ctx in context.node_contexts.items()
            },
        }
