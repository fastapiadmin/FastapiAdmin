# -*- coding: utf-8 -*-

import io
from typing import Any
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log

from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import DemoCreateSchema, DemoUpdateSchema, DemoOutSchema, DemoQueryParam
from .crud import DemoCRUD


class DemoService:
    """
    示例管理模块服务层
    """
    
    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 示例ID
        
        返回:
        - dict: 示例模型实例字典
        """
        obj = await DemoCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_service(cls, auth: AuthSchema, search: DemoQueryParam | None = None, order_by: list[dict[str, str]] | None = None) -> list[dict]:
        """
        列表查询
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (DemoQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数
        
        返回:
        - list[dict]: 示例模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await DemoCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [DemoOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def page_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: DemoQueryParam | None = None, order_by: list[dict[str, str]] | None = None) -> dict:
        """
        分页查询
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (DemoQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数
        
        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        
        result = await DemoCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_service(cls, auth: AuthSchema, data: DemoCreateSchema) -> dict:
        """
        创建
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (DemoCreateSchema): 示例创建模型
        
        返回:
        - dict: 示例模型实例字典
        """
        obj = await DemoCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，名称已存在')
        obj = await DemoCRUD(auth).create_crud(data=data)
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: DemoUpdateSchema) -> dict:
        """
        更新
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 示例ID
        - data (DemoUpdateSchema): 示例更新模型
        
        返回:
        - dict: 示例模型实例字典
        """
        # 检查数据是否存在
        obj = await DemoCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查名称是否重复
        exist_obj = await DemoCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，名称重复')
            
        obj = await DemoCRUD(auth).update_crud(id=id, data=data)
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 示例ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        
        # 检查所有要删除的数据是否存在
        for id in ids:
            obj = await DemoCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
                
        await DemoCRUD(auth).delete_crud(ids=ids)
    
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
        await DemoCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_service(cls, obj_list: list[dict[str, Any]]) -> bytes:
        """
        批量导出
        
        参数:
        - obj_list (list[dict[str, Any]]): 示例模型实例字典列表
        
        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'name': '名称', 
            'status': '状态',
            'description': '备注',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建者',
        }

        # 复制数据并转换状态
        data = obj_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '启用' if item.get('status') == '0' else '停用'
            # 处理创建者
            creator_info = item.get('created_id')
            if isinstance(creator_info, dict):
                item['created_id'] = creator_info.get('name', '未知')
            else:
                item['created_id'] = '未知'

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
                    exists_obj = await DemoCRUD(auth).get(name=data["name"])
                    if exists_obj:
                        if update_support:
                            await DemoCRUD(auth).update(id=exists_obj.id, data=data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{count}行: 对象 {data['name']} 已存在")
                    else:
                        await DemoCRUD(auth).create(data=data)
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