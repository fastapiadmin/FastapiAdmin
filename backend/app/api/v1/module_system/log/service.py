
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import logger

from .crud import LoginLogCRUD, OperationLogCRUD
from .schema import (
    LoginLogCreateSchema,
    LoginLogDetailOutSchema,
    LoginLogOutSchema,
    LoginLogQueryParam,
    OperationLogCreateSchema,
    OperationLogDetailOutSchema,
    OperationLogOutSchema,
    OperationLogQueryParam,
)


class LoginLogService:
    """登录日志管理服务"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> LoginLogDetailOutSchema:
        return await LoginLogCRUD(self.auth).get_or_404(id=id, out_schema=LoginLogDetailOutSchema)

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: LoginLogQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        return await LoginLogCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"updated_time": "desc"}],
            search=vars(search) if search else None,
            out_schema=LoginLogOutSchema,
        )

    async def create(self, data: LoginLogCreateSchema) -> LoginLogDetailOutSchema:
        obj = await LoginLogCRUD(self.auth).create(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return LoginLogDetailOutSchema.model_validate(obj)

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        existing = await LoginLogCRUD(self.auth).get_list(search={"id": ("in", ids)})
        existing_map = {obj.id for obj in existing}
        for nid in ids:
            if nid not in existing_map:
                raise CustomException(msg=f"删除失败，ID为{nid}的数据不存在")

        await LoginLogCRUD(self.auth).delete(ids=ids)


class OperationLogService:
    """操作日志管理服务"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @staticmethod
    async def cleanup_operation_log() -> None:
        from datetime import datetime, timedelta

        from sqlalchemy import delete, select

        from app.core.database import async_db_session

        from .model import LoginLogModel, OperationLogModel

        retention_days = 90
        try:
            from app.api.v1.module_system.params.model import ParamsModel

            async with async_db_session() as _s:
                result = await _s.execute(select(ParamsModel.config_value).where(ParamsModel.config_key == "operation_log_retention_days").limit(1))
                row = result.scalar()
                if row is not None:
                    retention_days = int(row)
        except Exception:
            pass

        cutoff = datetime.now() - timedelta(days=retention_days)
        async with async_db_session() as session:
            op_stmt = delete(OperationLogModel).where(OperationLogModel.created_time < cutoff)
            op_result = await session.execute(op_stmt)

            login_stmt = delete(LoginLogModel).where(LoginLogModel.created_time < cutoff)
            login_result = await session.execute(login_stmt)

            await session.commit()
            logger.info(f"操作日志清理完成: 操作日志 {op_result.rowcount} 条, 登录日志 {login_result.rowcount} 条")
            return True

    async def create(self, data: OperationLogCreateSchema) -> OperationLogDetailOutSchema:
        crud = OperationLogCRUD(self.auth)
        obj = await crud.create(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return OperationLogDetailOutSchema.model_validate(obj)

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: OperationLogQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        crud = OperationLogCRUD(self.auth)
        return await crud.page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "desc"}],
            search=vars(search) if search else None,
            out_schema=OperationLogOutSchema,
        )

    async def detail(self, id: int) -> OperationLogDetailOutSchema:
        crud = OperationLogCRUD(self.auth)
        return await crud.get_or_404(id=id, out_schema=OperationLogDetailOutSchema)

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        existing = await OperationLogCRUD(self.auth).get_list(search={"id": ("in", ids)})
        existing_map = {obj.id for obj in existing}
        for nid in ids:
            if nid not in existing_map:
                raise CustomException(msg="删除失败，该数据不存在")
        crud = OperationLogCRUD(self.auth)
        await crud.delete(ids=ids)
