from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil

from .crud import PositionCRUD
from .schema import (
    PositionCreateSchema,
    PositionOutSchema,
    PositionQueryParam,
    PositionUpdateSchema,
)


class PositionService:
    """
    岗位管理服务

    提供岗位 CRUD、批量启/禁用、Excel 导出等业务能力。
    """

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> PositionOutSchema:
        return await PositionCRUD(self.auth).get_or_404(id=id, out_schema=PositionOutSchema)

    async def get_list(
        self,
        search: PositionQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[PositionOutSchema]:
        position_list = await PositionCRUD(self.auth).get_list(search=vars(search) if search else None, order_by=order_by)
        return [PositionOutSchema.model_validate(position) for position in position_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: PositionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        return await PositionCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=PositionOutSchema,
        )

    async def create(self, data: PositionCreateSchema) -> PositionOutSchema:
        position = await PositionCRUD(self.auth).get(name=data.name)
        if position:
            raise CustomException(msg="创建失败，该数据已存在")
        new_position = await PositionCRUD(self.auth).create(data=data)
        return PositionOutSchema.model_validate(new_position)

    async def update(self, id: int, data: PositionUpdateSchema) -> PositionOutSchema:
        _ = await PositionCRUD(self.auth).get_or_404(id=id, msg="更新失败，该数据不存在")
        exist_position = await PositionCRUD(self.auth).get(name=data.name)
        if exist_position and exist_position.id != id:
            raise CustomException(msg="更新失败，名称已存在")
        updated_position = await PositionCRUD(self.auth).update(id=id, data=data)
        return PositionOutSchema.model_validate(updated_position)

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        positions = await PositionCRUD(self.auth).get_list(search={"id": ("in", ids)})
        position_map = {p.id: p for p in positions}
        for pid in ids:
            if pid not in position_map:
                raise CustomException(msg="删除失败，该数据不存在")
        await PositionCRUD(self.auth).delete(ids=ids)

    async def set_available(self, data: BatchSetAvailable) -> None:
        positions = await PositionCRUD(self.auth).get_list(search={"id": ("in", data.ids)})
        position_map = {p.id: p for p in positions}
        for pid in data.ids:
            if pid not in position_map:
                raise CustomException(msg="该数据不存在")
        await PositionCRUD(self.auth).set(ids=data.ids, status=data.status)

    @staticmethod
    def export_list(position_list: list[dict]) -> bytes:
        mapping_dict = {
            "id": "编号",
            "name": "岗位名称",
            "order": "显示顺序",
            "status": "状态",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "created_id": "创建者ID",
            "updated_id": "更新者ID",
        }
        data = position_list.copy()
        for item in data:
            item["status"] = "启用" if item.get("status") == 0 else "停用"
            item["creator"] = item.get("created_by", {}).get("name", "未知") if isinstance(item.get("created_by"), dict) else "未知"
        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
