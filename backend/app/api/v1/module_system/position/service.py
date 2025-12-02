# -*- coding: utf-8 -*-

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil

from ..auth.schema import AuthSchema
from .crud import PositionCRUD
from .schema import (
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionOutSchema,
    PositionQueryParam
)


class PositionService:
    """岗位模块服务层"""

    @classmethod
    async def get_position_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取岗位详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 岗位ID
        
        返回:
        - Dict: 岗位详情对象
        """
        position = await PositionCRUD(auth).get_by_id_crud(id=id)
        return PositionOutSchema.model_validate(position).model_dump()

    @classmethod
    async def get_position_list_service(cls, auth: AuthSchema, search: PositionQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """
        获取岗位列表
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (PositionQueryParam | None): 查询参数对象
        - order_by (list[dict] | None): 排序参数列表
        
        返回:
        - list[dict]: 岗位列表对象
        """
        position_list = await PositionCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [PositionOutSchema.model_validate(position).model_dump() for position in position_list]

    @classmethod
    async def create_position_service(cls, auth: AuthSchema, data: PositionCreateSchema) -> dict:
        """
        创建岗位
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (PositionCreateSchema): 岗位创建模型
        
        返回:
        - Dict: 创建的岗位对象
        """
        position = await PositionCRUD(auth).get(name=data.name)
        if position:
            raise CustomException(msg='创建失败，该岗位已存在')
        new_position = await PositionCRUD(auth).create(data=data)
        return PositionOutSchema.model_validate(new_position).model_dump()

    @classmethod
    async def update_position_service(cls, auth: AuthSchema, id:int, data: PositionUpdateSchema) -> dict:
        """
        更新岗位
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 岗位ID
        - data (PositionUpdateSchema): 岗位更新模型
        
        返回:
        - dict: 更新的岗位对象
        """
        position = await PositionCRUD(auth).get_by_id_crud(id=id)
        if not position:
            raise CustomException(msg='更新失败，该岗位不存在')
        exist_position = await PositionCRUD(auth).get(name=data.name)
        if exist_position and exist_position.id != id:
            raise CustomException(msg='更新失败，岗位名称重复')
        updated_position = await PositionCRUD(auth).update(id=id, data=data)
        return PositionOutSchema.model_validate(updated_position).model_dump()

    @classmethod
    async def delete_position_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除岗位
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 岗位ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            position = await PositionCRUD(auth).get_by_id_crud(id=id)
            if not position:
                raise CustomException(msg='删除失败，该岗位不存在')
        await PositionCRUD(auth).delete(ids=ids)

    @classmethod
    async def set_position_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        设置岗位状态
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置状态模型
        
        返回:
        - None
        """
        await PositionCRUD(auth).set_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def export_position_list_service(cls, position_list: list[dict]) -> bytes:
        """
        导出岗位列表
        
        参数:
        - position_list (list[dict]): 岗位列表对象
        
        返回:
        - bytes: 导出的Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'name': '岗位名称', 
            'order': '显示顺序',
            'status': '状态',
            'description': '备注',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建者ID',
            'updated_id': '更新者ID',
        }

        # 复制数据并转换状态
        data = position_list.copy()
        for item in data:
            item['status'] = '启用' if item.get('status') == '0' else '停用'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)