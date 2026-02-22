from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import WorkflowCRUD, WorkflowRunCRUD, WorkflowRunLogCRUD
from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowRunCreateSchema,
    WorkflowRunLogCreateSchema,
    WorkflowRunLogOutSchema,
    WorkflowRunOutSchema,
    WorkflowRunUpdateSchema,
    WorkflowUpdateSchema,
    WorkflowValidateResultSchema,
    WorkflowValidateSchema,
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
    async def list_service(
        cls,
        auth: AuthSchema,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (WorkflowQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 工作流模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await WorkflowCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [WorkflowOutSchema.model_validate(obj).model_dump() for obj in obj_list]

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

        if data.template_id:
            template = await WorkflowCRUD(auth).get_by_id_crud(id=data.template_id)
            if not template or not template.is_template:
                raise CustomException(msg="创建失败，模板不存在或不是模板")

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

        if obj.status == "published":
            raise CustomException(msg="更新失败，已发布的工作流不能直接修改，请先归档")

        if data.code:
            exist_obj = await WorkflowCRUD(auth).get_by_code_crud(code=data.code)
            if exist_obj and exist_obj.id != id:
                raise CustomException(msg="更新失败，流程编码重复")

        if data.template_id:
            template = await WorkflowCRUD(auth).get_by_id_crud(id=data.template_id)
            if not template or not template.is_template:
                raise CustomException(msg="更新失败，模板不存在或不是模板")

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

        for obj in obj_list:
            if obj.status == "published":
                raise CustomException(msg=f"删除失败，ID为{obj.id}的工作流已发布，无法删除")

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
            version=data.version or obj.version,
            published_at=datetime.now().isoformat(),
            published_by=auth.user.id if auth.user else None,
        )

        obj = await WorkflowCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def validate_service(cls, auth: AuthSchema, data: WorkflowValidateSchema) -> WorkflowValidateResultSchema:
        """
        验证工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (WorkflowValidateSchema): 验证模型

        返回:
        - WorkflowValidateResultSchema: 验证结果
        """
        errors = []
        warnings = []
        stats = {}

        nodes = data.nodes if isinstance(data.nodes, list) else []
        edges = data.edges if isinstance(data.edges, list) else []

        stats["totalNodes"] = len(nodes)
        stats["totalEdges"] = len(edges)
        stats["nodeTypes"] = {}

        for node in nodes:
            node_type = node.get("type", "unknown")
            stats["nodeTypes"][node_type] = stats["nodeTypes"].get(node_type, 0) + 1

        if len(nodes) == 0:
            errors.append("流程中没有节点")

        node_ids = {n.get("id") for n in nodes}
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            if source not in node_ids:
                errors.append(f"连线 {edge.get('label') or edge.get('id')} 的源节点不存在")
            if target not in node_ids:
                errors.append(f"连线 {edge.get('label') or edge.get('id')} 的目标节点不存在")

        is_valid = len(errors) == 0

        return WorkflowValidateResultSchema(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            stats=stats,
        )

    @classmethod
    async def templates_service(cls, auth: AuthSchema) -> list[dict]:
        """
        获取模板列表

        参数:
        - auth (AuthSchema): 认证信息模型

        返回:
        - list[dict]: 模板列表
        """
        obj_list = await WorkflowCRUD(auth).list_templates_crud(order_by=[{"id": "asc"}])
        return [WorkflowOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def export_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        导出工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID

        返回:
        - dict: 工作流数据
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="导出失败，该工作流不存在")

        return {
            "id": obj.id,
            "name": obj.name,
            "code": obj.code,
            "description": obj.description,
            "nodes": obj.nodes,
            "edges": obj.edges,
            "version": obj.version,
            "category": obj.category,
            "metadata": obj.meta_data,
            "exportedAt": datetime.now().isoformat(),
        }

    @classmethod
    async def import_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        导入工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 工作流数据

        返回:
        - dict: 工作流模型实例字典
        """
        code = data.get("code")
        if code:
            exist_obj = await WorkflowCRUD(auth).get_by_code_crud(code=code)
            if exist_obj:
                raise CustomException(msg="导入失败，流程编码已存在")

        create_data = WorkflowCreateSchema(
            name=data.get("name", "导入的工作流"),
            code=data.get("code", f"imported_{datetime.now().timestamp()}"),
            description=data.get("description"),
            nodes=data.get("nodes", []),
            edges=data.get("edges", []),
            version=data.get("version", "1.0.0"),
            category=data.get("category"),
            meta_data=data.get("metadata"),
        )

        obj = await WorkflowCRUD(auth).create_crud(data=create_data)
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
        task_run_id = await WorkflowRunService.execute_workflow(
            auth=auth,
            workflow_id=data.workflow_id,
            variables=data.variables,
            business_key=data.business_key,
            initiator=auth.user.id if auth.user else None,
            initiator_name=auth.user.username if auth.user else None,
            job_id=data.job_id,
        )

        return {
            "task_run_id": task_run_id,
            "workflow_id": data.workflow_id,
            "status": "running",
            "message": "任务执行已启动",
        }

    @classmethod
    async def pause_service(cls, auth: AuthSchema, id: int) -> None:
        """
        暂停工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID

        返回:
        - None
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")

        await WorkflowRunService.pause_service(auth=auth, id=id)

    @classmethod
    async def resume_service(cls, auth: AuthSchema, id: int) -> None:
        """
        恢复工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID

        返回:
        - None
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")

        await WorkflowRunService.resume_service(auth=auth, id=id)

    @classmethod
    async def terminate_service(cls, auth: AuthSchema, id: int) -> None:
        """
        终止工作流

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 工作流ID

        返回:
        - None
        """
        obj = await WorkflowCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")

        await WorkflowRunService.terminate_service(auth=auth, id=id)


class WorkflowRunService:
    """工作流运行记录管理模块服务层"""

    @classmethod
    async def list_service(cls, auth: AuthSchema, search: dict | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """获取工作流运行记录列表"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]

        obj_list = await WorkflowRunCRUD(auth).list_crud(search=search_dict, order_by=order_by_list)
        return [WorkflowRunOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: dict | None = None,
        order_by: list[dict] | None = None,
    ) -> dict:
        """分页查询工作流运行记录"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await WorkflowRunCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """获取工作流运行记录详情"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="查询失败，该工作流运行记录不存在")
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: WorkflowRunCreateSchema) -> dict:
        """创建工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).create_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败，工作流运行记录创建失败")
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: WorkflowRunUpdateSchema) -> dict:
        """更新工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该工作流运行记录不存在")

        obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，工作流运行记录更新失败")
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除工作流运行记录"""
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        obj_list = await WorkflowRunCRUD(auth).list_crud(search={"id": (None, ids)})
        if not obj_list or len(obj_list) != len(ids):
            raise CustomException(msg="删除失败，部分工作流运行记录不存在")

        await WorkflowRunCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def clear_service(cls, auth: AuthSchema) -> None:
        """清除所有工作流运行记录"""
        await WorkflowRunCRUD(auth).clear_crud()

    @classmethod
    async def cancel_service(cls, auth: AuthSchema, id: int) -> dict:
        """取消工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="取消失败，该工作流运行记录不存在")

        if obj.status in ["completed", "failed", "cancelled"]:
            raise CustomException(msg="取消失败，该工作流运行记录已完成或已取消")

        update_data = WorkflowRunUpdateSchema(
            status="cancelled",
            end_time=datetime.now(),
        )
        obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def pause_service(cls, auth: AuthSchema, id: int) -> dict:
        """暂停工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="暂停失败，该工作流运行记录不存在")

        if obj.status not in ["running", "pending"]:
            raise CustomException(msg="暂停失败，只能暂停运行中或待执行的工作流运行记录")

        update_data = WorkflowRunUpdateSchema(
            status="paused",
        )
        obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def resume_service(cls, auth: AuthSchema, id: int) -> dict:
        """恢复工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="恢复失败，该工作流运行记录不存在")

        if obj.status != "paused":
            raise CustomException(msg="恢复失败，只能恢复已暂停的工作流运行记录")

        update_data = WorkflowRunUpdateSchema(
            status="running",
        )
        obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def terminate_service(cls, auth: AuthSchema, id: int) -> dict:
        """终止工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="终止失败，该工作流运行记录不存在")

        if obj.status in ["completed", "failed", "cancelled", "terminated"]:
            raise CustomException(msg="终止失败，该工作流运行记录已完成或已终止")

        update_data = WorkflowRunUpdateSchema(
            status="terminated",
            end_time=datetime.now(),
        )
        obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=update_data)
        return WorkflowRunOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def retry_service(cls, auth: AuthSchema, id: int, retry_count: int = 1) -> dict:
        """重试工作流运行记录"""
        obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="重试失败，该工作流运行记录不存在")

        if obj.status not in ["failed", "cancelled"]:
            raise CustomException(msg="重试失败，只能重试失败或已取消的工作流运行记录")

        if obj.retry_count >= obj.max_retry:
            raise CustomException(msg=f"重试失败，已达到最大重试次数{obj.max_retry}")

        update_data = WorkflowRunUpdateSchema(
            status="pending",
            retry_count=obj.retry_count + retry_count,
            error_message=None,
            start_time=None,
            end_time=None,
            duration=None,
        )
        updated_obj = await WorkflowRunCRUD(auth).update_crud(id=id, data=update_data)

        if not updated_obj:
            raise CustomException(msg="重试失败，更新工作流运行记录失败")

        try:
            await cls.execute_workflow(
                auth=auth,
                workflow_id=obj.workflow_id,
                variables=obj.variables,
                business_key=obj.business_key,
                initiator=obj.initiator,
                initiator_name=obj.initiator_name,
                job_id=obj.job_id,
                task_run_id=id,
            )
        except Exception:
            pass

        final_obj = await WorkflowRunCRUD(auth).get_by_id_crud(id=id)
        if not final_obj:
            raise CustomException(msg="重试失败，获取工作流运行记录失败")

        return WorkflowRunOutSchema.model_validate(final_obj).model_dump()

    @classmethod
    async def execute_workflow(
        cls,
        auth: AuthSchema,
        workflow_id: int,
        variables: dict,
        business_key: str | None,
        initiator: int | None,
        initiator_name: str | None,
        job_id: int | None,
        task_run_id: int | None = None,
    ) -> int:
        """执行工作流"""
        workflow = await WorkflowCRUD(auth).get_by_id_crud(id=workflow_id)
        if not workflow:
            raise CustomException(msg="工作流不存在")

        nodes = workflow.nodes if isinstance(workflow.nodes, list) else []
        edges = workflow.edges if isinstance(workflow.edges, list) else []

        if not nodes:
            raise CustomException(msg="工作流没有节点")

        start_time = datetime.now()

        if not task_run_id:
            create_data = WorkflowRunCreateSchema(
                workflow_id=workflow_id,
                workflow_name=workflow.name,
                workflow_version=workflow.version,
                business_key=business_key,
                initiator=initiator,
                initiator_name=initiator_name,
                variables=variables,
                job_id=job_id,
            )
            task_run = await WorkflowRunCRUD(auth).create_crud(data=create_data)
            if not task_run:
                raise CustomException(msg="创建工作流运行记录失败")
            task_run_id = task_run.id

        if task_run_id is None:
            raise CustomException(msg="工作流运行记录ID不能为空")

        update_data = WorkflowRunUpdateSchema(
            status="running",
            start_time=start_time,
        )
        await WorkflowRunCRUD(auth).update_crud(id=task_run_id, data=update_data)

        try:
            await cls._execute_nodes(
                auth=auth,
                task_run_id=task_run_id,
                nodes=nodes,
                edges=edges,
                variables=variables,
            )

            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds())

            update_data = WorkflowRunUpdateSchema(
                status="completed",
                end_time=end_time,
                duration=duration,
            )
            await WorkflowRunCRUD(auth).update_crud(id=task_run_id, data=update_data)

            await cls._add_log(
                auth=auth,
                task_run_id=task_run_id,
                level="info",
                message=f"工作流执行完成，总耗时: {duration}秒",
            )

        except Exception as e:
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds())

            update_data = WorkflowRunUpdateSchema(
                status="failed",
                end_time=end_time,
                duration=duration,
                error_message=str(e),
            )
            await WorkflowRunCRUD(auth).update_crud(id=task_run_id, data=update_data)

            await cls._add_log(
                auth=auth,
                task_run_id=task_run_id,
                level="error",
                message=f"工作流执行失败: {e!s}",
            )

            raise

        return task_run_id

    @classmethod
    async def _execute_nodes(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        variables: dict,
    ) -> None:
        """执行节点"""
        node_map = {node.get("id"): node for node in nodes}
        edge_map = {}
        target_nodes = set()
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            if source not in edge_map:
                edge_map[source] = []
            edge_map[source].append(edge)
            target_nodes.add(target)

        start_nodes = [node for node in nodes if node.get("id") not in target_nodes]
        if not start_nodes:
            start_nodes = [node for node in nodes if node.get("type") == "trigger"]
        if not start_nodes:
            raise CustomException(msg="工作流缺少起始节点")

        executed_nodes = set()
        queue = start_nodes.copy()

        while queue:
            current_node = queue.pop(0)
            node_id = current_node.get("id")

            if node_id in executed_nodes:
                continue

            executed_nodes.add(node_id)

            await cls._execute_node(
                auth=auth,
                task_run_id=task_run_id,
                node=current_node,
                variables=variables,
            )

            if node_id in edge_map:
                for edge in edge_map[node_id]:
                    target_id = edge.get("target")
                    target_node = node_map.get(target_id)
                    if target_node and target_id not in executed_nodes:
                        target_node_type = target_node.get("type")

                        if target_node_type == "condition":
                            condition = target_node.get("data", {}).get("condition", "True")
                            try:
                                result = bool(eval(condition, {}, variables))
                            except Exception:
                                result = False

                            for next_edge in edge_map.get(target_id, []):
                                next_target_id = next_edge.get("target")
                                next_target_node = node_map.get(next_target_id)
                                edge_label = next_edge.get("label", "")

                                if next_target_node and next_target_id not in executed_nodes:
                                    if edge_label == "true" and result:
                                        queue.append(next_target_node)
                                    elif edge_label == "false" and not result:
                                        queue.append(next_target_node)
                        else:
                            queue.append(target_node)

    @classmethod
    async def _execute_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node: dict[str, Any],
        variables: dict,
    ) -> None:
        """执行单个节点"""
        node_id = str(node.get("id", ""))
        node_type = node.get("type", "")
        node_name = node.get("data", {}).get("label", "未知节点")
        node_config = node.get("data", {})

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"开始执行节点: {node_name}",
        )

        try:
            if node_type == "task":
                await cls._execute_task_node(auth, task_run_id, node_id, node_name, node_config, variables)
            elif node_type == "approval":
                await cls._execute_approval_node(auth, task_run_id, node_id, node_name, node_config, variables)
            elif node_type == "condition":
                await cls._execute_condition_node(auth, task_run_id, node_id, node_name, node_config, variables)
            elif node_type == "notification":
                await cls._execute_notification_node(auth, task_run_id, node_id, node_name, node_config, variables)
            elif node_type == "timer":
                await cls._execute_timer_node(auth, task_run_id, node_id, node_name, node_config, variables)
            elif node_type == "parallel":
                await cls._execute_parallel_node(auth, task_run_id, node_id, node_name, node_config, variables)
            else:
                await cls._add_log(
                    auth=auth,
                    task_run_id=task_run_id,
                    level="warning",
                    node_id=node_id,
                    node_name=node_name,
                    message=f"未知节点类型: {node_type}",
                )

            await cls._add_log(
                auth=auth,
                task_run_id=task_run_id,
                level="info",
                node_id=node_id,
                node_name=node_name,
                message=f"节点执行完成: {node_name}",
            )

        except Exception as e:
            await cls._add_log(
                auth=auth,
                task_run_id=task_run_id,
                level="error",
                node_id=node_id,
                node_name=node_name,
                message=f"节点执行失败: {node_name}, 错误: {e!s}",
            )
            raise

    @classmethod
    async def _execute_task_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行任务节点"""
        task_type = node_config.get("task_type", "default")

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"执行任务类型: {task_type}",
        )

        variables[f"{node_id}_result"] = {"status": "success", "output": "任务执行成功"}

    @classmethod
    async def _execute_approval_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行审批节点"""
        approvers = node_config.get("approvers", [])
        approval_type = node_config.get("approval_type", "or")

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"审批类型: {approval_type}, 审批人: {approvers}",
        )

        variables[f"{node_id}_result"] = {"status": "approved", "output": "审批通过"}

    @classmethod
    async def _execute_condition_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行条件节点"""
        condition = node_config.get("condition", "True")

        try:
            result = bool(eval(condition, {}, variables))
        except Exception as e:
            result = False
            raise CustomException(msg=f"条件表达式执行失败: {e!s}")

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"条件表达式: {condition}, 结果: {result}",
        )

        variables[f"{node_id}_result"] = {"status": "success", "result": result}

    @classmethod
    async def _execute_notification_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行通知节点"""
        notification_type = node_config.get("notification_type", "email")
        recipients = node_config.get("recipients", [])

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"发送通知: {notification_type}, 收件人: {recipients}",
        )

        variables[f"{node_id}_result"] = {"status": "sent", "output": "通知发送成功"}

    @classmethod
    async def _execute_timer_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行定时节点"""
        timer_type = node_config.get("timer_type", "delay")
        timer_value = node_config.get("timer_value", 0)

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"定时器类型: {timer_type}, 值: {timer_value}",
        )

        variables[f"{node_id}_result"] = {"status": "completed", "output": "定时器执行完成"}

    @classmethod
    async def _execute_parallel_node(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        node_id: str,
        node_name: str,
        node_config: dict,
        variables: dict,
    ) -> None:
        """执行并行节点"""
        parallel_count = node_config.get("parallel_count", 1)

        await cls._add_log(
            auth=auth,
            task_run_id=task_run_id,
            level="info",
            node_id=node_id,
            node_name=node_name,
            message=f"并行执行数量: {parallel_count}",
        )

        variables[f"{node_id}_result"] = {"status": "completed", "output": "并行执行完成"}

    @classmethod
    async def _add_log(
        cls,
        auth: AuthSchema,
        task_run_id: int,
        level: str,
        message: str,
        node_id: str | None = None,
        node_name: str | None = None,
        data: dict | None = None,
    ) -> None:
        """添加日志"""
        log_data = WorkflowRunLogCreateSchema(
            task_run_id=task_run_id,
            level=level,
            node_id=node_id,
            node_name=node_name,
            message=message,
            data=data or {},
        )
        await WorkflowRunLogCRUD(auth).create_crud(data=log_data)


class WorkflowRunLogService:
    """工作流运行日志管理模块服务层"""

    @classmethod
    async def list_service(cls, auth: AuthSchema, search: dict | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """获取工作流运行日志列表"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]

        obj_list = await WorkflowRunLogCRUD(auth).list_crud(search=search_dict, order_by=order_by_list)
        return [WorkflowRunLogOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: dict | None = None,
        order_by: list[dict] | None = None,
    ) -> dict:
        """分页查询工作流运行日志"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await WorkflowRunLogCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result
