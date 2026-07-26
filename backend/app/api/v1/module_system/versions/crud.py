from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException

from .model import VersionModel
from .schema import VersionCreateSchema, VersionUpdateSchema


class VersionCRUD(CRUDBase[VersionModel, VersionCreateSchema, VersionUpdateSchema]):
    """版本数据层"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        super().__init__(model=VersionModel, auth=auth, db=db)

    async def set_status(self, id: int, status: int) -> VersionModel:
        """更新版本状态"""
        obj = await self.get(id=id)
        if not obj:
            raise CustomException(msg="版本不存在")
        obj.status = status
        await self.db.flush()
        await self.db.refresh(obj)
        return obj
