from datetime import UTC, datetime

from sqlalchemy import false, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.utils.common_util import search_to_dict

from .crud import NoticeCRUD
from .model import NoticeModel, NoticeReadModel
from .schema import NoticeCreateSchema, NoticeOutSchema, NoticeQueryParam, NoticeUpdateSchema
from .stream import notice_stream_manager


async def _broadcast_notice_update() -> None:
    """公告变更后广播轻量信号（尽力而为）：客户端收到后拉取 available 以库为准。

    广播发生在请求事务提交前（db_getter 请求级事务在依赖退出时 commit），
    但变更信号与内容读取解耦，毫秒级窗口内的竞态由客户端拉取兜底。
    """
    try:
        await notice_stream_manager.broadcast({"type": "notice_update"})
    except Exception as e:
        logger.warning("公告变更广播失败（不影响业务）: {}", e)


class NoticeService:
    """公告管理服务

    提供公告 CRUD、状态切换、已启用公告分页查询、Excel 导出等业务能力。
    """

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        self.auth = auth
        self.db = db

    async def detail(self, id: int) -> NoticeOutSchema:
        """获取公告详情

        参数:
        - id (int): 公告 ID

        返回:
        - NoticeOutSchema: 公告响应模型
        """
        obj = await NoticeCRUD(self.auth, self.db).get_or_404(id=id)
        return NoticeOutSchema.model_validate(obj)

    async def get_list(
        self,
        search: NoticeQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[NoticeOutSchema]:
        """获取公告列表

        参数:
        - search (NoticeQueryParam | None): 查询参数
        - order_by (list[dict] | None): 排序规则

        返回:
        - list[NoticeOutSchema]: 公告列表
        """
        notice_obj_list = await NoticeCRUD(self.auth, self.db).get_list(search=search_to_dict(search), order_by=order_by)
        return [NoticeOutSchema.model_validate(notice_obj) for notice_obj in notice_obj_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: NoticeQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> PageResultSchema[NoticeOutSchema]:
        """分页查询公告

        参数:
        - page_no (int): 当前页码
        - page_size (int): 每页条数
        - search (NoticeQueryParam | None): 查询参数
        - order_by (list[dict] | None): 排序规则

        返回:
        - PageResultSchema[NoticeOutSchema]: 分页结果
        """
        offset = (page_no - 1) * page_size
        return await NoticeCRUD(self.auth, self.db).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=search_to_dict(search),
            out_schema=NoticeOutSchema,
        )

    async def available_page(self) -> PageResultSchema[NoticeOutSchema]:
        """获取已启用的公告（首页展示用，最多 10 条）

        **公开内容必须绕过 CRUD 的数据权限**：``CRUDBase`` 会给非超管叠加
        ``created_id = 当前用户`` 的数据范围条件，公告由运营创建，普通用户据此查询会一条都看不到。
        这里显式直查；``created_by/updated_by`` 需预加载，否则异步序列化触发 MissingGreenlet。
        """
        conditions = self._enabled_condition()
        total = int((await self.db.scalar(select(func.count(NoticeModel.id)).where(*conditions))) or 0)
        rows = (
            await self.db.scalars(
                select(NoticeModel)
                .where(*conditions)
                .order_by(NoticeModel.id.asc())
                .limit(10)
                .options(selectinload(NoticeModel.created_by), selectinload(NoticeModel.updated_by))
            )
        ).all()
        return PageResultSchema(
            page_no=1, page_size=10, total=total, has_next=False, items=[NoticeOutSchema.model_validate(r) for r in rows]
        )

    @staticmethod
    def _enabled_condition() -> tuple:
        """对外可见的公告：启用(0) 且未删除。

        ``available_page`` 走 ``NoticeCRUD.page``，会被基座的 created_id 数据范围再过滤一层，
        所以这里做「未读数 / 全部已读」时统一用直查，保证口径与 C 端看到的一致。
        """
        return (NoticeModel.status == 0, NoticeModel.is_deleted == false())

    async def unread_count(self, user_id: int) -> int:
        """未读公告数 = 启用公告总数 − 我读过的（已读集合里若公告已停用则不参与相减）"""
        read_ids = select(NoticeReadModel.notice_id).where(NoticeReadModel.user_id == user_id)
        stmt = select(func.count(NoticeModel.id)).where(*self._enabled_condition(), NoticeModel.id.not_in(read_ids))
        return int((await self.db.scalar(stmt)) or 0)

    async def read_ids(self, user_id: int) -> list[int]:
        """我已读的公告 ID（供列表页判断哪条未读）"""
        rows = await self.db.scalars(select(NoticeReadModel.notice_id).where(NoticeReadModel.user_id == user_id))
        return [int(x) for x in rows.all()]

    async def mark_read(self, user_id: int, notice_ids: list[int] | None = None) -> int:
        """标记已读（不传 notice_ids 表示全部启用公告），返回剩余未读数。

        只记录仍然存在的启用公告；已存在则跳过，重复调用是幂等的。
        """
        stmt = select(NoticeModel.id).where(*self._enabled_condition())
        if notice_ids is not None:
            # 显式空数组表示“不标记任何公告”，不能退化成“全部已读”
            if not notice_ids:
                return await self.unread_count(user_id)
            stmt = stmt.where(NoticeModel.id.in_(notice_ids))
        target_ids = [int(x) for x in (await self.db.scalars(stmt)).all()]
        if target_ids:
            existing = set(await self.read_ids(user_id))
            now = datetime.now(UTC)
            for notice_id in target_ids:
                if notice_id in existing:
                    continue
                self.db.add(NoticeReadModel(user_id=user_id, notice_id=notice_id, read_at=now))
            await self.db.flush()
        return await self.unread_count(user_id)

    async def create(self, data: NoticeCreateSchema) -> NoticeOutSchema:
        """创建公告

        参数:
        - data (NoticeCreateSchema): 公告创建模型

        返回:
        - NoticeOutSchema: 公告响应模型
        """
        notice = await NoticeCRUD(self.auth, self.db).get(notice_title=data.notice_title)
        if notice:
            raise CustomException(msg="创建失败，该数据已存在")
        notice_obj = await NoticeCRUD(self.auth, self.db).create(data=data)
        await _broadcast_notice_update()
        return await self.detail(id=notice_obj.id)

    async def update(self, id: int, data: NoticeUpdateSchema) -> NoticeOutSchema:
        """更新公告

        参数:
        - id (int): 公告 ID
        - data (NoticeUpdateSchema): 公告更新模型

        返回:
        - NoticeOutSchema: 公告响应模型
        """
        _ = await NoticeCRUD(self.auth, self.db).get_or_404(id=id, msg="更新失败，该数据不存在")
        exist_notice = await NoticeCRUD(self.auth, self.db).get(notice_title=data.notice_title)
        if exist_notice and exist_notice.id != id:
            raise CustomException(msg="更新失败，标题已存在")
        await NoticeCRUD(self.auth, self.db).update(id=id, data=data)
        await _broadcast_notice_update()
        return await self.detail(id=id)

    async def delete(self, ids: list[int]) -> None:
        """删除公告

        参数:
        - ids (list[int]): 公告 ID 列表
        """
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")
        notices = await NoticeCRUD(self.auth, self.db).get_list(search={"id": ("in", ids)})
        notice_map = {n.id: n for n in notices}
        for nid in ids:
            if nid not in notice_map:
                raise CustomException(msg="删除失败，该数据不存在")
        await NoticeCRUD(self.auth, self.db).delete(ids=ids)

    async def set_available(self, data: BatchSetAvailable) -> None:
        """批量启用/禁用公告

        参数:
        - data (BatchSetAvailable): 批量设置状态模型
        """
        await NoticeCRUD(self.auth, self.db).set(ids=data.ids, status=data.status)
        await _broadcast_notice_update()
