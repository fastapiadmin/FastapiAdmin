# -*- coding: utf-8 -*-

import json
from redis.asyncio.client import Redis

from app.common.enums import RedisInitKeyConfig
from app.utils.excel_util import ExcelUtil
from app.core.database import async_db_session
from app.core.base_schema import BatchSetAvailable
from app.core.redis_crud import RedisCURD
from app.core.exceptions import CustomException
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import (
    DictDataCreateSchema,
    DictDataOutSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeOutSchema,
    DictTypeUpdateSchema,
    DictDataQueryParam, 
    DictTypeQueryParam
)
from .crud import DictDataCRUD, DictTypeCRUD


class DictTypeService:
    """
    字典类型管理模块服务层
    """
    
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取数据字典类型详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 数据字典类型ID
        
        返回:
        - dict: 数据字典类型详情字典
        """
        obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=id)
        return DictTypeOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: DictTypeQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """
        获取数据字典类型列表
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (DictTypeQueryParam | None): 搜索条件模型
        - order_by (list[dict] | None): 排序字段列表
        
        返回:
        - list[dict]: 数据字典类型详情字典列表
        """
        obj_list = await DictTypeCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [DictTypeOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictTypeCreateSchema) -> dict:
        """
        创建数据字典类型
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - data (DictTypeCreateSchema): 数据字典类型创建模型
        
        返回:
        - dict: 数据字典类型详情字典
        """
        exist_obj = await DictTypeCRUD(auth).get(dict_name=data.dict_name)
        if exist_obj:
            raise CustomException(msg='创建失败，该数据字典类型已存在')
        obj = await DictTypeCRUD(auth).create_obj_crud(data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj).model_dump()
        
        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        
        try:
            await RedisCURD(redis).set(
                    key=redis_key,
                    value="",
                )
            log.info(f"创建字典类型成功: {new_obj_dict}")
        except Exception as e:
            log.error(f"创建字典类型失败: {e}")
            raise CustomException(msg=f"创建字典类型失败 {e}")
        
        return new_obj_dict
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, id:int, data: DictTypeUpdateSchema) -> dict:
        """
        更新数据字典类型
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - id (int): 数据字典类型ID
        - data (DictTypeUpdateSchema): 数据字典类型更新模型
        
        返回:
        - dict: 数据字典类型详情字典
        """
        exist_obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该数据字典类型不存在')
        if exist_obj.dict_name != data.dict_name:
            raise CustomException(msg='更新失败，数据字典类型名称不可以修改')
        
        
        dict_data_list = []
        # 如果字典类型修改或状态变更，则修改对应字典数据的类型和状态，并更新Redis缓存
        if exist_obj.dict_type != data.dict_type or exist_obj.status != data.status:
            # 检查字典数据类型是否被修改
            exist_obj_type_list = await DictDataCRUD(auth).list(search={'dict_type': exist_obj.dict_type})
            if exist_obj_type_list:
                for item in exist_obj_type_list:
                    item.dict_type = data.dict_type
                    dict_data = DictDataUpdateSchema(
                        dict_sort=item.dict_sort,
                        dict_label=item.dict_label,
                        dict_value=item.dict_value,
                        dict_type=data.dict_type,
                        dict_type_id=item.dict_type_id,
                        css_class=item.css_class,
                        list_class=item.list_class,
                        is_default=item.is_default,
                        status=data.status,
                        description=item.description
                    )
                    obj = await DictDataCRUD(auth).update_obj_crud(id=item.id, data=dict_data)
                    dict_data_list.append(DictDataOutSchema.model_validate(obj).model_dump())
        
        obj = await DictTypeCRUD(auth).update_obj_crud(id=id, data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj).model_dump()

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据，确保包含最新状态
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
            log.info(f"更新字典类型成功并刷新缓存: {new_obj_dict}")
        except Exception as e:
            log.error(f"更新字典类型缓存失败: {e}")
            raise CustomException(msg=f"更新字典类型缓存失败 {e}")
        
        return new_obj_dict
    
    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, ids: list[int]) -> None:
        """
        删除数据字典类型
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - ids (list[int]): 数据字典类型ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            exist_obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg='删除失败，该数据字典类型不存在')
            # 检查是否有字典数据
            exist_obj_type_list = await DictDataCRUD(auth).list(search={'dict_type': id})
            if len(exist_obj_type_list) > 0:
                # 如果有字典数据，不能删除
                raise CustomException(msg='删除失败，该数据字典类型下存在字典数据')
            # 删除Redis缓存
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{exist_obj.dict_type}"
            try:
                await RedisCURD(redis).delete(redis_key)
                log.info(f"删除字典类型成功: {id}")
            except Exception as e:
                log.error(f"删除字典类型失败: {e}")
                raise CustomException(msg=f"删除字典类型失败")
        await DictTypeCRUD(auth).delete_obj_crud(ids=ids)
    
    @classmethod
    async def set_obj_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        设置数据字典类型状态
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置状态模型
        
        返回:
        - None
        """
        await DictTypeCRUD(auth).set_obj_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def export_obj_service(cls, data_list: list[dict]) -> bytes:
        """
        导出数据字典类型列表
        
        参数:
        - data_list (list[dict]): 数据字典类型列表
        
        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'dict_name': '字典名称', 
            'dict_type': '字典类型',
            'status': '状态',
            'description': '备注',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建者ID',
            'updated_id': '更新者ID',
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '启用' if item.get('status') == '0' else '停用'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
    

class DictDataService:
    """
    字典数据管理模块服务层
    """
    
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取数据字典数据详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 数据字典数据ID
        
        返回:
        - dict: 数据字典数据详情字典
        """
        obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: DictDataQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """
        获取数据字典数据列表
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (DictDataQueryParam | None): 搜索条件模型
        - order_by (list[dict] | None): 排序字段列表
        
        返回:
        - list[dict]: 数据字典数据详情字典列表
        """
        obj_list = await DictDataCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [DictDataOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def init_dict_service(cls, redis: Redis):
        """
        应用初始化: 获取所有字典类型对应的字典数据信息并缓存service
        
        参数:
        - redis (Redis): Redis客户端
        
        返回:
        - None
        """
        try:
            async with async_db_session() as session:
                async with session.begin():
                    # 在初始化过程中，不需要检查数据权限
                    auth = AuthSchema(db=session, check_data_scope=False)
                    obj_list = await DictTypeCRUD(auth).get_obj_list_crud()
                    if not obj_list:
                        log.warning("未找到任何字典类型数据")
                        return
                    
                    success_count = 0
                    fail_count = 0
                    
                    for obj in obj_list:
                        dict_type = obj.dict_type
                        try:
                            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type})
                            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
                            # 保存到Redis并设置过期时间
                            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type}"
                            value = json.dumps(dict_data, ensure_ascii=False)
                            await RedisCURD(redis).set(
                                    key=redis_key,
                                    value=value,
                            )
                            success_count += 1
                            log.info(f"✅ 字典数据缓存成功: {dict_type}")
                            
                        except Exception as e:
                            fail_count += 1
                            log.error(f"❌ 初始化字典数据失败 [{dict_type}]: {e}")
                            # 继续处理其他字典类型，不中断整个初始化过程
                    
                    log.info(f"字典数据初始化完成 - 成功: {success_count}, 失败: {fail_count}")
                    
        except Exception as e:
            log.error(f"字典初始化过程发生错误: {e}")
            # 只在严重错误时抛出异常，允许单个字典加载失败
            raise CustomException(msg=f"字典数据初始化失败: {str(e)}")
    
    @classmethod
    async def get_init_dict_service(cls, redis: Redis, dict_type: str)->list[dict]:
        """
        从缓存获取字典数据列表信息service
        
        参数:
        - redis (Redis): Redis客户端
        - dict_type (str): 字典类型
        
        返回:
        - list[dict]: 字典数据列表
        """
        try:
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type}"
            obj_list_dict = await RedisCURD(redis).get(redis_key)
            
            # 确保返回数据正确序列化
            if obj_list_dict:
                if isinstance(obj_list_dict, str):
                    try:
                        return json.loads(obj_list_dict)
                    except json.JSONDecodeError:
                        log.warning(f"字典数据反序列化失败，尝试重新初始化缓存: {dict_type}")
                elif isinstance(obj_list_dict, list):
                    return obj_list_dict
                
            # 缓存不存在或格式错误时重新初始化
            await cls.init_dict_service(redis)
            obj_list_dict = await RedisCURD(redis).get(redis_key)
            if not obj_list_dict:
                raise CustomException(msg="数据字典不存在")
            
            # 再次确保返回数据正确序列化
            if isinstance(obj_list_dict, str):
                try:
                    return json.loads(obj_list_dict)
                except json.JSONDecodeError:
                    raise CustomException(msg="字典数据格式错误")
            return obj_list_dict
        except CustomException:
            raise
        except Exception as e:
            log.error(f"获取字典缓存失败: {str(e)}")
            raise CustomException(msg=f"获取字典数据失败: {str(e)}")

    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictDataCreateSchema) -> dict:
        """
        创建数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - data (DictDataCreateSchema): 数据字典数据创建模型
        
        返回:
        - dict: 数据字典数据详情字典
        """
        exist_obj = await DictDataCRUD(auth).get(dict_label=data.dict_label)
        if exist_obj:
            raise CustomException(msg='创建失败，该字典数据已存在')
        obj = await DictDataCRUD(auth).create_obj_crud(data=data)

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
            log.info(f"创建字典数据写入缓存成功: {obj}")
        except Exception as e:
            log.error(f"创建字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"创建字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, id:int, data: DictDataUpdateSchema) -> dict:
        """
        更新数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - id (int): 数据字典数据ID
        - data (DictDataUpdateSchema): 数据字典数据更新模型
        
        返回:
        - Dict: 数据字典数据详情字典
        """
        exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该字典数据不存在')

        if exist_obj.id != id:
            raise CustomException(msg='更新失败，数据字典数据重复')
            
        # 如果字典类型变更，仅刷新旧类型缓存，不联动字典类型状态
        if exist_obj.dict_type != data.dict_type:
            dict_type = await DictTypeCRUD(auth).get(dict_type=exist_obj.dict_type)
            if dict_type:
                redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type.dict_type}"
                try:
                    dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type.dict_type})
                    dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
                    value = json.dumps(dict_data, ensure_ascii=False)
                    await RedisCURD(redis).set(
                            key=redis_key,
                            value=value,
                        )
                except Exception as e:
                    log.error(f"更新字典数据类型变更时刷新旧缓存失败: {e}")
                
        obj = await DictDataCRUD(auth).update_obj_crud(id=id, data=data)
        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
            log.info(f"更新字典数据写入缓存成功: {obj}")
        except Exception as e:
            log.error(f"更新字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"更新字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, ids: list[int]) -> None:
        """
        删除数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - ids (list[int]): 数据字典数据ID列表
        
        返回:
        - None
        """
        try:
            if len(ids) < 1:
                raise CustomException(msg='删除失败，删除对象不能为空')
            
            # 首先检查是否包含系统默认数据
            for id in ids:
                exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
                if not exist_obj:
                    raise CustomException(msg=f'{id} 删除失败，该字典数据不存在')
                # 系统默认字典数据不允许删除
                if exist_obj.is_default:
                    raise CustomException(msg=f'删除失败，ID为{id}的系统默认字典数据不允许删除')
            
            # 获取所有需要清除的缓存键
            dict_types_to_clear = set()
            for id in ids:
                exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
                if exist_obj:
                    dict_types_to_clear.add(exist_obj.dict_type)
            
            # 执行删除操作
            await DictDataCRUD(auth).delete_obj_crud(ids=ids)
            
            # 清除缓存
            for dict_type in dict_types_to_clear:
                try:
                    redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type}"
                    await RedisCURD(redis).delete(redis_key)
                    log.info(f"清除字典缓存成功: {dict_type}")
                except Exception as e:
                    log.warning(f"清除字典缓存失败: {e}")
                    # 缓存清除失败不影响删除操作
            
            log.info(f"删除字典数据成功，ID列表: {ids}")
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"删除字典数据失败: {str(e)}")
            raise CustomException(msg=f"删除字典数据失败: {str(e)}")

    @classmethod
    async def set_obj_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量修改数据字典数据状态
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量修改数据字典数据状态负载模型
        
        返回:
        - None
        """
        await DictDataCRUD(auth).set_obj_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def export_obj_service(cls, data_list: list[dict]) -> bytes:
        """
        导出数据字典数据列表
        
        参数:
        - data_list (list[dict]): 数据字典数据列表
        
        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'dict_sort': '字典排序', 
            'dict_label': '字典标签', 
            'dict_value': '字典键值', 
            'dict_type': '字典类型',
            'css_class': '样式属性', 
            'list_class': '表格回显样式', 
            'is_default': '是否默认', 
            'status': '状态',
            'description': '备注',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建者ID',
            'updated_id': '更新者ID',
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '启用' if item.get('status') == '0' else '停用'
            # 处理是否默认
            item['is_default'] = '是' if item.get('is_default') else '否'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)