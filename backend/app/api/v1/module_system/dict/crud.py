# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence, Union, Any

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.dict.schema import DictDataCreateSchema, DictDataUpdateSchema, DictTypeCreateSchema, DictTypeUpdateSchema
from app.api.v1.module_system.auth.schema import AuthSchema


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

    async def get_obj_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[DictTypeModel]:
        """
        获取数据字典类型详情
        
        参数:
        - id (int): 数据字典类型ID
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[DictTypeModel]: 数据字典类型模型,如果不存在则为None
        """
        # 添加默认预加载字典数据关系
        if preload is None:
            preload = []
        return await self.get(id=id, preload=preload)
    
    async def get_obj_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[DictTypeModel]:
        """
        获取数据字典类型列表
        
        参数:
        - search (Optional[Dict]): 查询参数,默认值为None
        - order_by (Optional[List[Dict[str, str]]]): 排序参数,默认值为None
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DictTypeModel]: 数据字典类型模型序列
        """
        # 添加默认预加载字典数据关系
        if preload is None:
            preload = []
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_obj_crud(self, data: DictTypeCreateSchema) -> Optional[DictTypeModel]:
        """
        创建数据字典类型
        
        参数:
        - data (DictTypeCreateSchema): 数据字典类型创建模型
        
        返回:
        - Optional[DictTypeModel]: 创建的数据字典类型模型,如果创建失败则为None
        """
        return await self.create(data=data)
    
    async def update_obj_crud(self, id: int, data: DictTypeUpdateSchema) -> Optional[DictTypeModel]:
        """
        更新数据字典类型
        
        参数:
        - id (int): 数据字典类型ID
        - data (DictTypeUpdateSchema): 数据字典类型更新模型
        
        返回:
        - Optional[DictTypeModel]: 更新的数据字典类型模型,如果更新失败则为None
        """
        return await self.update(id=id, data=data)
    
    async def delete_obj_crud(self, ids: List[int]) -> None:
        """
        删除数据字典类型
        
        参数:
        - ids (List[int]): 数据字典类型ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_obj_available_crud(self, ids: List[int], status: str) -> None:
        """
        设置数据字典类型的可用状态
        
        参数:
        - ids (List[int]): 数据字典类型ID列表
        - status (bool): 可用状态,True表示可用,False表示不可用
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)
    
    async def batch_create_obj_crud(self, data_list: List[DictTypeCreateSchema]) -> List[DictTypeModel]:
        """
        批量创建数据字典类型
        
        参数:
        - data_list (List[DictTypeCreateSchema]): 数据字典类型创建模型列表
        
        返回:
        - List[DictTypeModel]: 创建的数据字典类型模型列表
        """
        return await self.batch_create(data_list=data_list)
    
    async def batch_update_obj_crud(self, ids: List[int], data: DictTypeUpdateSchema) -> int:
        """
        批量更新数据字典类型
        
        参数:
        - ids (List[int]): 数据字典类型ID列表
        - data (DictTypeUpdateSchema): 数据字典类型更新模型
        
        返回:
        - int: 更新的记录数量
        """
        return await self.batch_update(ids=ids, data=data)
    
    async def batch_delete_obj_crud(self, ids: List[int]) -> int:
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

    async def get_obj_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[DictDataModel]:
        """
        获取数据字典数据详情
        
        参数:
        - id (int): 数据字典数据ID
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[DictDataModel]: 数据字典数据模型,如果不存在则为None
        """
        # 添加默认预加载字典类型关系
        if preload is None:
            preload = []
        return await self.get(id=id, preload=preload)
    
    async def get_obj_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[DictDataModel]:
        """
        获取数据字典数据列表
        
        参数:
        - search (Optional[Dict]): 查询参数,默认值为None
        - order_by (Optional[List[Dict[str, str]]]): 排序参数,默认值为None
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DictDataModel]: 数据字典数据模型序列
        """
        # 添加默认预加载字典类型关系
        if preload is None:
            preload = []
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_obj_crud(self, data: DictDataCreateSchema) -> Optional[DictDataModel]:
        """
        创建数据字典数据
        
        参数:
        - data (DictDataCreateSchema): 数据字典数据创建模型
        
        返回:
        - Optional[DictDataModel]: 创建的数据字典数据模型,如果创建失败则为None
        """
        return await self.create(data=data)
    
    async def update_obj_crud(self, id: int, data: DictDataUpdateSchema) -> Optional[DictDataModel]:
        """
        更新数据字典数据
        
        参数:
        - id (int): 数据字典数据ID
        - data (DictDataUpdateSchema): 数据字典数据更新模型
        
        返回:
        - Optional[DictDataModel]: 更新的数据字典数据模型,如果更新失败则为None
        """
        return await self.update(id=id, data=data)
    
    async def delete_obj_crud(self, ids: List[int]) -> None:
        """
        删除数据字典数据
        
        参数:
        - ids (List[int]): 数据字典数据ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_obj_available_crud(self, ids: List[int], status: str) -> None:
        """
        设置数据字典数据的可用状态
        
        参数:
        - ids (List[int]): 数据字典数据ID列表
        - status (bool): 可用状态,True表示可用,False表示不可用
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)
    
    async def batch_create_obj_crud(self, data_list: List[DictDataCreateSchema]) -> List[DictDataModel]:
        """
        批量创建数据字典数据
        
        参数:
        - data_list (List[DictDataCreateSchema]): 数据字典数据创建模型列表
        
        返回:
        - List[DictDataModel]: 创建的数据字典数据模型列表
        """
        return await self.batch_create(data_list=data_list)
    
    async def batch_update_obj_crud(self, ids: List[int], data: DictDataUpdateSchema) -> int:
        """
        批量更新数据字典数据
        
        参数:
        - ids (List[int]): 数据字典数据ID列表
        - data (DictDataUpdateSchema): 数据字典数据更新模型
        
        返回:
        - int: 更新的记录数量
        """
        return await self.batch_update(ids=ids, data=data)
    
    async def batch_delete_obj_crud(self, ids: List[int], exclude_system: bool = True) -> int:
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
            system_data_filter = {"id__in": ids, "remark__contains": "系统默认"}
            system_data = await self.list(search=system_data_filter)
            system_ids = [item.id for item in system_data]
            # 从待删除ID列表中排除系统默认数据
            ids = [id for id in ids if id not in system_ids]
        
        if ids:
            await self.delete(ids=ids)
        return len(ids)
    
    async def get_obj_list_by_dict_type_crud(self, dict_type: str, status: Optional[str] = True) -> List[DictDataModel]:
        """
        根据字典类型获取字典数据列表
        
        参数:
        - dict_type (str): 字典类型
        - status (Optional[bool]): 状态过滤，None表示不过滤
        
        返回:
        - List[DictDataModel]: 数据字典数据模型列表
        """
        search = {"dict_type": dict_type}
        if status is not None:
            search["status"] = status
        order_by = [{"field": "sort", "direction": "asc"}]
        return await self.list(search=search, order_by=order_by)