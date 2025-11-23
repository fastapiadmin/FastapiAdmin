# -*- coding: utf-8 -*-

import io
from typing import Any, List, Dict, Optional
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log

from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import TenantCreateSchema, TenantUpdateSchema, TenantOutSchema
from .param import TenantQueryParam
from .crud import TenantCRUD


class TenantService:
    """
    租户管理模块服务层
    """
    
    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """
        详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 租户ID
        
        返回:
        - Dict: 租户模型实例字典
        """
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return TenantOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_service(cls, auth: AuthSchema, search: Optional[TenantQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """
        列表查询
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (Optional[TenantQueryParam]): 查询参数
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        
        返回:
        - List[Dict]: 租户模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await TenantCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [TenantOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def page_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: Optional[TenantQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Dict:
        """
        分页查询
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (Optional[TenantQueryParam]): 查询参数
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        
        返回:
        - Dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        
        result = await TenantCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_service(cls, auth: AuthSchema, data: TenantCreateSchema) -> Dict:
        """
        创建
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (TenantCreateSchema): 租户创建模型
        
        返回:
        - Dict: 租户模型实例字典
        """
        obj = await TenantCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，名称已存在')
        obj = await TenantCRUD(auth).get(code=data.code)
        if obj:
            raise CustomException(msg='创建失败，编码已存在')
        obj = await TenantCRUD(auth).create_crud(data=data)
        return TenantOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: TenantUpdateSchema) -> Dict:
        """
        更新
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 租户ID
        - data (TenantUpdateSchema): 租户更新模型
        
        返回:
        - Dict: 租户模型实例字典
        """
        # 检查数据是否存在
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查名称是否重复
        exist_obj = await TenantCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，名称重复')
            
        obj = await TenantCRUD(auth).update_crud(id=id, data=data)
        return TenantOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """
        删除
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (List[int]): 租户ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        
        # 检查所有要删除的数据是否存在
        for id in ids:
            obj = await TenantCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
                
        await TenantCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量设置状态
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置状态模型
        
        返回:
        - None
        """
        await TenantCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_service(cls, obj_list: List[Dict[str, Any]]) -> bytes:
        """
        批量导出
        
        参数:
        - obj_list (List[Dict[str, Any]]): 租户模型实例字典列表
        
        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'name': '名称', 
            'status': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = obj_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '正常' if item.get('status') else '停用'
            # 处理创建者
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            else:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """
        批量导入
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - file (UploadFile): 上传的Excel文件
        - update_support (bool): 是否支持更新存在数据
        
        返回:
        - str: 导入结果信息
        """
        
        header_dict = {
            '名称': 'name',
            '状态': 'status',
            '描述': 'description'
        }

        try:
            # 读取Excel文件
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            # 检查表头是否完整
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            # 重命名列名
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            required_fields = ['name', 'status']
            for field in required_fields:
                missing_rows = df[df[field].isnull()].index.tolist()
                raise CustomException(msg=f"{[k for k,v in header_dict.items() if v == field][0]}不能为空，第{[i+1 for i in missing_rows]}行")
            
            error_msgs = []
            success_count = 0
            count = 0
            
            # 处理每一行数据
            for index, row in df.iterrows():
                count += 1
                try:
                    # 数据转换前的类型检查
                    try:
                        status = True if row['status'] == '正常' else False
                    except ValueError:
                        error_msgs.append(f"第{count}行: 状态必须是'正常'或'停用'")
                        continue
                    
                    # 构建用户数据
                    data = {
                        "name": str(row['name']),
                        "status": status,
                        "description": str(row['description']),
                    }

                    # 处理用户导入
                    exists_obj = await TenantCRUD(auth).get(name=data["name"])
                    if exists_obj:
                        if update_support:
                            await TenantCRUD(auth).update(id=exists_obj.id, data=data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{count}行: 对象 {data['name']} 已存在")
                    else:
                        await TenantCRUD(auth).create(data=data)
                        success_count += 1
                        
                except Exception as e:
                    error_msgs.append(f"第{count}行: {str(e)}")
                    continue

            # 返回详细的导入结果
            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            log.error(f"批量导入用户失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """
        下载导入模板
        
        返回:
        - bytes: Excel文件字节流
        """
        header_list = ['名称', '状态', '描述']
        selector_header_list = ['状态'] 
        option_list = [{'状态': ['正常', '停用']}]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )