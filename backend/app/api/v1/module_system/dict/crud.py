from collections.abc import Sequence

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.dict.schema import (
    DictDataCreateSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeUpdateSchema,
)
from app.core.base_crud import CRUDBase


class DictTypeCRUD(CRUDBase[DictTypeModel, DictTypeCreateSchema, DictTypeUpdateSchema]):
    """数据字典类型数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化数据字典类型CRUD

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=DictTypeModel, auth=auth)

    async def get_obj_by_id_crud(
        self, id: int, preload: list | None = None
    ) -> DictTypeModel | None:
        """
        获取数据字典类型详情

        参数:
        - id (int): 数据字典类型ID
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - DictTypeModel | None: 数据字典类型模型,如果不存在则为None
        """
        # 添加默认预加载字典数据关系
        if preload is None:
            preload = []
        return await self.get(id=id, preload=preload)

    async def get_obj_list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list | None = None,
    ) -> Sequence[DictTypeModel]:
        """
        获取数据字典类型列表

        参数:
        - search (dict | None): 查询参数,默认值为None
        - order_by (list[dict] | None): 排序参数,默认值为None
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[DictTypeModel]: 数据字典类型模型序列
        """
        # 添加默认预加载字典数据关系
        if preload is None:
            preload = []
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_obj_crud(self, data: DictTypeCreateSchema) -> DictTypeModel | None:
        """
        创建数据字典类型

        参数:
        - data (DictTypeCreateSchema): 数据字典类型创建模型

        返回:
        - DictTypeModel | None: 创建的数据字典类型模型,如果创建失败则为None
        """
        return await self.create(data=data)

    async def update_obj_crud(self, id: int, data: DictTypeUpdateSchema) -> DictTypeModel | None:
        """
        更新数据字典类型

        参数:
        - id (int): 数据字典类型ID
        - data (DictTypeUpdateSchema): 数据字典类型更新模型

        返回:
        - DictTypeModel | None: 更新的数据字典类型模型,如果更新失败则为None
        """
        return await self.update(id=id, data=data)

    async def delete_obj_crud(self, ids: list[int]) -> None:
        """
        删除数据字典类型

        参数:
        - ids (list[int]): 数据字典类型ID列表

        返回:
        - None
        """
        return await self.delete(ids=ids)

    async def set_obj_available_crud(self, ids: list[int], status: str) -> None:
        """
        设置数据字典类型的可用状态

        参数:
        - ids (list[int]): 数据字典类型ID列表
        - status (str): 可用状态,0表示正常,1表示停用

        返回:
        - None
        """
        return await self.set(ids=ids, status=status)

    async def batch_delete_obj_crud(self, ids: list[int]) -> int:
        """
        批量删除数据字典类型

        参数:
        - ids (List[int]): 数据字典类型ID列表

        返回:
        - int: 删除的记录数量
        """
        await self.delete(ids=ids)
        return len(ids)


class DictDataCRUD(CRUDBase[DictDataModel, DictDataCreateSchema, DictDataUpdateSchema]):
    """数据字典数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化数据字典数据CRUD

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=DictDataModel, auth=auth)

    async def get_obj_by_id_crud(
        self, id: int, preload: list | None = None
    ) -> DictDataModel | None:
        """
        获取数据字典数据详情

        参数:
        - id (int): 数据字典数据ID
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - DictDataModel | None: 数据字典数据模型,如果不存在则为None
        """
        # 添加默认预加载字典类型关系
        if preload is None:
            preload = []
        return await self.get(id=id, preload=preload)

    async def get_obj_list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list | None = None,
    ) -> Sequence[DictDataModel]:
        """
        获取数据字典数据列表

        参数:
        - search (dict | None): 查询参数,默认值为None
        - order_by (list[dict] | None): 排序参数,默认值为None
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[DictDataModel]: 数据字典数据模型序列
        """
        # 添加默认预加载字典类型关系
        if preload is None:
            preload = []
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_obj_crud(self, data: DictDataCreateSchema) -> DictDataModel | None:
        """
        创建数据字典数据

        参数:
        - data (DictDataCreateSchema): 数据字典数据创建模型

        返回:
        - DictDataModel | None: 创建的数据字典数据模型,如果创建失败则为None
        """
        return await self.create(data=data)

    async def update_obj_crud(self, id: int, data: DictDataUpdateSchema) -> DictDataModel | None:
        """
        更新数据字典数据

        参数:
        - id (int): 数据字典数据ID
        - data (DictDataUpdateSchema): 数据字典数据更新模型

        返回:
        - DictDataModel | None: 更新的数据字典数据模型,如果更新失败则为None
        """
        return await self.update(id=id, data=data)

    async def delete_obj_crud(self, ids: list[int]) -> None:
        """
        删除数据字典数据

        参数:
        - ids (list[int]): 数据字典数据ID列表

        返回:
        - None
        """
        return await self.delete(ids=ids)

    async def set_obj_available_crud(self, ids: list[int], status: str) -> None:
        """
        设置数据字典数据的可用状态

        参数:
        - ids (list[int]): 数据字典数据ID列表
        - status (str): 可用状态,0表示正常,1表示停用

        返回:
        - None
        """
        return await self.set(ids=ids, status=status)

    async def batch_delete_obj_crud(self, ids: list[int], exclude_system: bool = True) -> int:
        """
        批量删除数据字典数据

        参数:
        - ids (List[int]): 数据字典数据ID列表
        - exclude_system (bool): 是否排除系统默认数据，默认为True

        返回:
        - int: 删除的记录数量
        """
        # 如果需要排除系统默认数据，可以在这里添加过滤逻辑
        # 假设系统默认数据在remark字段中包含"系统默认"字符串
        if exclude_system:
            # 获取非系统默认数据的ID
            system_data_filter = {
                "id__in": ids,
                "remark__contains": "系统默认",
            }
            system_data = await self.list(search=system_data_filter)
            system_ids = [item.id for item in system_data]
            # 从待删除ID列表中排除系统默认数据
            ids = [id for id in ids if id not in system_ids]

        if ids:
            await self.delete(ids=ids)
        return len(ids)

    async def get_obj_list_by_dict_type_crud(
        self, dict_type: str, status: str | None = "0"
    ) -> Sequence[DictDataModel]:
        """
        根据字典类型获取字典数据列表

        参数:
        - dict_type (str): 字典类型
        - status (str | None): 状态过滤，None表示不过滤

        返回:
        - Sequence[DictDataModel]: 数据字典数据模型序列
        """
        search = {"dict_type": dict_type}
        if status is not None:
            search["status"] = status
        order_by = [{"id": "asc"}]
        return await self.list(search=search, order_by=order_by)
