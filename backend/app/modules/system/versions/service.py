from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.exceptions import CustomException
from app.modules.system.notice.model import NoticeModel
from app.utils.common_util import search_to_dict

from .crud import VersionCRUD
from .model import VersionModel
from .schema import (
    VersionCreateSchema,
    VersionOutSchema,
    VersionQueryParam,
    VersionStatusSchema,
    VersionUpdateSchema,
)


class VersionService:
    """版本管理模块服务层"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        self.auth = auth
        self.db = db

    async def detail(self, id: int) -> VersionOutSchema:
        obj = await VersionCRUD(self.auth, self.db).get(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return VersionOutSchema.model_validate(obj)

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: VersionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> PageResultSchema[VersionOutSchema]:
        offset = (page_no - 1) * page_size
        return await VersionCRUD(self.auth, self.db).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"sort": "asc"}, {"id": "desc"}],
            search=search_to_dict(search, {}),
            out_schema=VersionOutSchema,
        )

    async def _sync_release_notice(self, version: VersionModel) -> None:
        """Publish one release notice for a published version; keep it idempotent."""
        if version.status != 1:
            return
        title = f"{version.version} 版本更新"
        result = await self.db.execute(
            select(NoticeModel).where(
                NoticeModel.notice_title == title,
                NoticeModel.is_deleted.is_(False),
            )
        )
        notice = result.scalar_one_or_none()
        content = version.content or version.description or version.title
        if notice is None:
            notice = NoticeModel(
                notice_title=title,
                notice_type="2",
                notice_content=content,
                status=1,
                description=f"版本发布自动生成（{version.version}）",
                created_id=self.auth.user.id if self.auth.user else None,
                updated_id=self.auth.user.id if self.auth.user else None,
            )
            self.db.add(notice)
        else:
            notice.notice_content = content
            notice.status = 1
            notice.updated_id = self.auth.user.id if self.auth.user else None
        await self.db.commit()

    async def create(self, data: VersionCreateSchema) -> VersionOutSchema:
        obj = await VersionCRUD(self.auth, self.db).create(data=data)
        await self._sync_release_notice(obj)
        return VersionOutSchema.model_validate(obj)

    async def update(self, id: int, data: VersionUpdateSchema) -> VersionOutSchema:
        obj = await VersionCRUD(self.auth, self.db).get(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该数据不存在")
        obj = await VersionCRUD(self.auth, self.db).update(id=id, data=data)
        await self._sync_release_notice(obj)
        return VersionOutSchema.model_validate(obj)

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")
        objs = await VersionCRUD(self.auth, self.db).get_list(search={"id": ("in", ids)})
        obj_map = {o.id: o for o in objs}
        for id_ in ids:
            if id_ not in obj_map:
                raise CustomException(msg="删除失败，该数据不存在")
        await VersionCRUD(self.auth, self.db).delete(ids=ids)

    async def set_status(self, id: int, data: VersionStatusSchema) -> VersionOutSchema:
        obj = await VersionCRUD(self.auth, self.db).update(id=id, data={"status": data.status})
        await self._sync_release_notice(obj)
        return VersionOutSchema.model_validate(obj)

    async def get_published(self) -> list[VersionOutSchema]:
        objs = await VersionCRUD(self.auth, self.db).get_list(
            search={"status": ("eq", 1)},
            order_by=[{"sort": "asc"}],
        )
        return [VersionOutSchema.model_validate(obj) for obj in objs]
