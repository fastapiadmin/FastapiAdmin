# -*- coding: utf-8 -*-

from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil

from ..auth.schema import AuthSchema
from .crud import OperationLogCRUD
from .schema import (
    OperationLogCreateSchema,
    OperationLogOutSchema,
    OperationLogQueryParam
)


class OperationLogService:
    """
    日志模块服务层
    """

    @classmethod
    async def get_log_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取日志详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 日志 ID
        
        返回:
        - dict: 日志详情字典
        """
        log = await OperationLogCRUD(auth).get_by_id_crud(id=id)
        log_dict = OperationLogOutSchema.model_validate(log).model_dump()
        return log_dict

    @classmethod
    async def get_log_list_service(cls, auth: AuthSchema, search: OperationLogQueryParam | None = None, order_by: list | None = None) -> list[dict]:
        """
        获取日志列表
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (OperationLogQueryParam | None): 日志查询参数模型
        - order_by (list | None): 排序字段列表
        
        返回:
        - list[dict]: 日志详情字典列表
        """
            
        log_list = await OperationLogCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        log_dict_list = [OperationLogOutSchema.model_validate(log).model_dump() for log in log_list]
        return log_dict_list

    @classmethod
    async def create_log_service(cls, auth: AuthSchema, data: OperationLogCreateSchema) -> dict:
        """
        创建日志
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (OperationLogCreateSchema): 日志创建模型
        
        返回:
        - dict: 日志详情字典
        """
        new_log = await OperationLogCRUD(auth).create(data=data)
        new_log_dict = OperationLogOutSchema.model_validate(new_log).model_dump()
        return new_log_dict
    
    @classmethod
    async def delete_log_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除日志
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 日志 ID 列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        await OperationLogCRUD(auth).delete(ids=ids)

    @classmethod
    async def export_log_list_service(cls, operation_log_list: list[dict]) -> bytes:
        """
        导出日志信息

        参数:
        - operation_log_list (list[dict]): 操作日志信息列表
        
        返回:
        - bytes: 操作日志信息excel的二进制数据
        """
        # 操作日志字段映射
        mapping_dict = {
            'id': '编号',
            'type': '日志类型',
            'request_path': '请求URL',
            'request_method': '请求方式',
            'request_payload': '请求参数',
            'request_ip': '操作地址',
            'login_location': '登录位置',
            'request_os': '操作系统',
            'request_browser': '浏览器',
            'response_json': '返回参数',
            'response_code': '相应状态',
            'process_time': '处理时间',
            'description': '备注',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建者ID',
            'updated_id': '更新者ID',
        }

        # 处理数据
        data = operation_log_list.copy()
        for item in data:
            # 处理状态
            item['response_code'] = '成功' if item.get('response_code') == 200 else '失败'
            # 处理日志类型 - 修正与schema.py保持一致
            item['type'] = '登录日志' if item.get('type') == 1 else '操作日志'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)