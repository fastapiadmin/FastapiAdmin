from collections.abc import Sequence

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import ParamsModel
from .schema import ParamsCreateSchema, ParamsUpdateSchema


class ParamsCRUD(CRUDBase[ParamsModel, ParamsCreateSchema, ParamsUpdateSchema]):
    """配置管理数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化配置CRUD

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=ParamsModel, auth=auth)

    async def get_obj_by_id_crud(self, id: int, preload: list | None = None) -> ParamsModel | None:
        """
        获取配置管理型详情

        参数:
        - id (int): 配置管理型ID
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - ParamsModel | None: 配置管理型模型实例
        """
        return await self.get(id=id, preload=preload)

    async def get_obj_by_key_crud(
        self, key: str, preload: list | None = None
    ) -> ParamsModel | None:
        """
        根据key获取配置管理型详情

        参数:
        - key (str): 配置管理型key
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - ParamsModel | None: 配置管理型模型实例
        """
        return await self.get(config_key=key, preload=preload)

    async def get_obj_list_crud(
        self,
        search: dict | None = None,
        order_by: list | None = None,
        preload: list | None = None,
    ) -> Sequence[ParamsModel]:
        """
        获取配置管理型列表

        参数:
        - search (dict | None): 查询参数对象。
        - order_by (list | None): 排序参数列表。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[ParamsModel]: 配置管理型模型实例列表
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_obj_crud(self, data: ParamsCreateSchema) -> ParamsModel | None:
        """
        创建配置管理型

        参数:
        - data (ParamsCreateSchema): 创建配置管理型负载模型

        返回:
        - ParamsModel | None: 配置管理型模型实例
        """
        return await self.create(data=data)

    async def update_obj_crud(self, id: int, data: ParamsUpdateSchema) -> ParamsModel | None:
        """
        更新配置管理型

        参数:
        - id (int): 配置管理型ID
        - data (ParamsUpdateSchema): 更新配置管理型负载模型

        返回:
        - ParamsModel | None: 配置管理型模型实例
        """
        return await self.update(id=id, data=data)

    async def delete_obj_crud(self, ids: list[int]) -> None:
        """
        删除配置管理型

        参数:
        - ids (list[int]): 配置管理型ID列表

        返回:
        - None
        """
        return await self.delete(ids=ids)
