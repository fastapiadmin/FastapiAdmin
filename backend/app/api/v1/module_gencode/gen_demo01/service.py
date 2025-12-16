# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import GenDemo01CreateSchema, GenDemo01UpdateSchema, GenDemo01OutSchema, GenDemo01QueryParam
from .crud import GenDemo01CRUD


class GenDemo01Service:
    """
    示例服务层
    """
    
    @classmethod
    async def detail_gen_demo01_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await GenDemo01CRUD(auth).get_by_id_gen_demo01_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return GenDemo01OutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_gen_demo01_service(cls, auth: AuthSchema, search: GenDemo01QueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await GenDemo01CRUD(auth).list_gen_demo01_crud(search=search_dict, order_by=order_by)
        return [GenDemo01OutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_gen_demo01_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: GenDemo01QueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await GenDemo01CRUD(auth).page_gen_demo01_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_gen_demo01_service(cls, auth: AuthSchema, data: GenDemo01CreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await GenDemo01CRUD(auth).create_gen_demo01_crud(data=data)
        return GenDemo01OutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_gen_demo01_service(cls, auth: AuthSchema, id: int, data: GenDemo01UpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await GenDemo01CRUD(auth).get_by_id_gen_demo01_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await GenDemo01CRUD(auth).update_gen_demo01_crud(id=id, data=data)
        return GenDemo01OutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_gen_demo01_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await GenDemo01CRUD(auth).get_by_id_gen_demo01_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await GenDemo01CRUD(auth).delete_gen_demo01_crud(ids=ids)
    
    @classmethod
    async def set_available_gen_demo01_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await GenDemo01CRUD(auth).set_available_gen_demo01_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_gen_demo01_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '主键ID',
            'uuid': 'UUID全局唯一标识',
            'name': '名称',
            'status': '是否启用(0:启用 1:禁用)',
            'description': '备注/描述',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建人ID',
            'updated_id': '更新人ID',
            'updated_id': '更新者ID',
        }

        data = obj_list.copy()
        for item in data:
            # 状态转换
            if 'status' in item:
                item['status'] = '启用' if item.get('status') == '0' else '停用'
            # 创建者转换
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            elif creator_info is None:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_gen_demo01_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '主键ID': 'id',
            'UUID全局唯一标识': 'uuid',
            '名称': 'name',
            '是否启用(0:启用 1:禁用)': 'status',
            '备注/描述': 'description',
            '创建时间': 'created_time',
            '更新时间': 'updated_time',
            '创建人ID': 'created_id',
            '更新人ID': 'updated_id',
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            
            error_msgs = []
            success_count = 0
            count = 0
            
            for index, row in df.iterrows():
                count += 1
                try:
                    data = {
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "name": row['name'],
                        "status": row['status'],
                        "description": row['description'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = GenDemo01CreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await GenDemo01CRUD(auth).create_gen_demo01_crud(data=create_schema)
                    success_count += 1
                except Exception as e:
                    error_msgs.append(f"第{count}行: {str(e)}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            log.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")
    
    @classmethod
    async def import_template_download_gen_demo01_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '主键ID',
            'UUID全局唯一标识',
            '名称',
            '是否启用(0:启用 1:禁用)',
            '备注/描述',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )