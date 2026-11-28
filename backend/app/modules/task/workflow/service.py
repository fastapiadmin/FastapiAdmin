from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.exceptions import CustomException

from .model import WorkflowInstanceModel, WorkflowModel, WorkflowTaskModel
from .schema import (
    WorkflowActionSchema,
    WorkflowCreateSchema,
    WorkflowInstanceOutSchema,
    WorkflowOutSchema,
    WorkflowQueryParam,
    WorkflowRunSchema,
    WorkflowTaskOutSchema,
    WorkflowUpdateSchema,
)

OPERATORS = {
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "contains": lambda a, b: str(b) in str(a),
}


def _value(context: dict, path: str) -> Any:
    current: Any = context
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _condition_matches(context: dict, step: dict) -> bool:
    field = str(step.get("field") or "")
    if not field or not step.get("operator"):
        return False
    left = _value(context, field)
    right = step.get("value")
    op = step.get("operator")
    fn = OPERATORS.get(str(op))
    if fn is None:
        return False
    try:
        return bool(fn(left, right))
    except TypeError:
        return False


class WorkflowService:
    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        self.auth = auth
        self.db = db

    async def page(self, page_no: int, page_size: int, search: WorkflowQueryParam | None = None) -> PageResultSchema[WorkflowOutSchema]:
        conditions = [WorkflowModel.is_deleted.is_(False)]
        if search and search.name:
            conditions.append(WorkflowModel.name.like(f"%{search.name}%"))
        if search and search.status is not None:
            conditions.append(WorkflowModel.status == search.status)
        total = await self.db.scalar(select(func.count()).select_from(WorkflowModel).where(*conditions))
        rows = (await self.db.scalars(
            select(WorkflowModel).where(*conditions).order_by(WorkflowModel.id.desc()).offset((page_no - 1) * page_size).limit(page_size)
        )).all()
        return PageResultSchema(
            page_no=page_no,
            page_size=page_size,
            total=total or 0,
            items=[WorkflowOutSchema.model_validate(row) for row in rows],
        )

    async def detail(self, id: int) -> WorkflowOutSchema:
        obj = await self._get_workflow(id)
        return WorkflowOutSchema.model_validate(obj)

    async def create(self, data: WorkflowCreateSchema) -> WorkflowOutSchema:
        obj = WorkflowModel(
            name=data.name.strip(),
            description=data.description,
            status=data.status,
            steps=[step.model_dump() for step in data.steps],
            created_id=self._user_id,
            updated_id=self._user_id,
        )
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return WorkflowOutSchema.model_validate(obj)

    async def update(self, id: int, data: WorkflowUpdateSchema) -> WorkflowOutSchema:
        obj = await self._get_workflow(id)
        obj.name = data.name.strip()
        obj.description = data.description
        obj.status = data.status
        obj.steps = [step.model_dump() for step in data.steps]
        obj.updated_id = self._user_id
        await self.db.flush()
        await self.db.refresh(obj)
        return WorkflowOutSchema.model_validate(obj)

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除对象不能为空")
        rows = (await self.db.scalars(select(WorkflowModel).where(WorkflowModel.id.in_(ids), WorkflowModel.is_deleted.is_(False)))).all()
        if len(rows) != len(set(ids)):
            raise CustomException(msg="存在不存在的流程")
        for row in rows:
            row.is_deleted = True
            row.deleted_id = self._user_id
            row.deleted_time = datetime.now(UTC)
        await self.db.flush()

    async def execute(self, id: int, data: WorkflowRunSchema) -> WorkflowInstanceOutSchema:
        workflow = await self._get_workflow(id)
        if workflow.status != 0:
            raise CustomException(msg="流程已停用，不能发起")
        instance = WorkflowInstanceModel(
            workflow_id=workflow.id,
            workflow_name=workflow.name,
            steps=workflow.steps,
            context=data.context,
            current_index=0,
            status="running",
            created_id=self._user_id,
            updated_id=self._user_id,
        )
        self.db.add(instance)
        await self.db.flush()
        await self._advance(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return WorkflowInstanceOutSchema.model_validate(instance)

    async def instances(self, page_no: int, page_size: int, workflow_id: int | None = None, status: str | None = None) -> PageResultSchema[WorkflowInstanceOutSchema]:
        conditions = [WorkflowInstanceModel.is_deleted.is_(False)]
        if workflow_id:
            conditions.append(WorkflowInstanceModel.workflow_id == workflow_id)
        if status:
            conditions.append(WorkflowInstanceModel.status == status)
        total = await self.db.scalar(select(func.count()).select_from(WorkflowInstanceModel).where(*conditions))
        rows = (await self.db.scalars(
            select(WorkflowInstanceModel).where(*conditions).order_by(WorkflowInstanceModel.id.desc()).offset((page_no - 1) * page_size).limit(page_size)
        )).all()
        return PageResultSchema(page_no=page_no, page_size=page_size, total=total or 0, items=[WorkflowInstanceOutSchema.model_validate(row) for row in rows])

    async def instance_detail(self, id: int) -> WorkflowInstanceOutSchema:
        obj = await self.db.get(WorkflowInstanceModel, id)
        if not obj or obj.is_deleted:
            raise CustomException(msg="流程实例不存在")
        return WorkflowInstanceOutSchema.model_validate(obj)

    async def pending_tasks(self) -> list[WorkflowTaskOutSchema]:
        conditions = [WorkflowTaskModel.status == "pending", WorkflowTaskModel.is_deleted.is_(False)]
        if not self._is_superuser:
            conditions.append(WorkflowTaskModel.assignee_id == self._user_id)
        rows = (await self.db.scalars(select(WorkflowTaskModel).where(*conditions).order_by(WorkflowTaskModel.id.desc()))).all()
        return [WorkflowTaskOutSchema.model_validate(row) for row in rows]

    async def act(self, task_id: int, data: WorkflowActionSchema) -> WorkflowTaskOutSchema:
        task = await self.db.get(WorkflowTaskModel, task_id)
        if not task or task.is_deleted:
            raise CustomException(msg="审批任务不存在")
        if task.status != "pending":
            raise CustomException(msg="该任务已处理")
        if not self._is_superuser and task.assignee_id != self._user_id:
            raise CustomException(msg="无权处理该审批任务")
        task.status = "approved" if data.approved else "rejected"
        task.comment = data.comment
        task.acted_at = datetime.now(UTC)
        task.updated_id = self._user_id
        instance = await self.db.get(WorkflowInstanceModel, task.instance_id)
        if not instance or instance.is_deleted:
            raise CustomException(msg="流程实例不存在")
        if data.approved:
            instance.current_index = task.step_index + 1
            instance.updated_id = self._user_id
            await self._advance(instance)
        else:
            instance.status = "rejected"
            instance.error = data.comment or f"{task.step_name} 未通过"
            instance.updated_id = self._user_id
        await self.db.flush()
        await self.db.refresh(task)
        return WorkflowTaskOutSchema.model_validate(task)

    async def _advance(self, instance: WorkflowInstanceModel) -> None:
        steps = instance.steps or []
        while instance.current_index < len(steps):
            step = steps[instance.current_index]
            if step.get("type") == "condition":
                if not _condition_matches(instance.context or {}, step):
                    instance.status = "rejected"
                    instance.error = f"条件不满足：{step.get('name')}"
                    return
                instance.current_index += 1
                continue
            if step.get("type") == "approval":
                existing = await self.db.scalar(
                    select(WorkflowTaskModel).where(
                        WorkflowTaskModel.instance_id == instance.id,
                        WorkflowTaskModel.step_index == instance.current_index,
                        WorkflowTaskModel.status == "pending",
                        WorkflowTaskModel.is_deleted.is_(False),
                    )
                )
                if existing:
                    return
                assignee = step.get("assignee_id") or self._user_id
                self.db.add(WorkflowTaskModel(
                    instance_id=instance.id,
                    step_index=instance.current_index,
                    step_name=str(step.get("name") or "审批"),
                    assignee_id=assignee,
                    status="pending",
                    created_id=self._user_id,
                    updated_id=self._user_id,
                ))
                return
            instance.current_index += 1
        instance.status = "completed"
        instance.error = None

    async def _get_workflow(self, id: int) -> WorkflowModel:
        obj = await self.db.get(WorkflowModel, id)
        if not obj or obj.is_deleted:
            raise CustomException(msg="流程不存在")
        return obj

    @property
    def _user_id(self) -> int | None:
        return self.auth.user.id if self.auth.user else None

    @property
    def _is_superuser(self) -> bool:
        return bool(self.auth.user and self.auth.user.is_superuser)
