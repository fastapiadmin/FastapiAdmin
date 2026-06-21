import json

from redis.asyncio.client import Redis

from app.common.enums import RedisInitKeyConfig
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.utils.excel_util import ExcelUtil

from .crud import DictDataCRUD, DictTypeCRUD
from .schema import (
    DictDataCreateSchema,
    DictDataOutSchema,
    DictDataQueryParam,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeOutSchema,
    DictTypeQueryParam,
    DictTypeUpdateSchema,
)


class DictTypeService:
    """
    字典类型管理服务

    设计：实例方法承载「当前用户上下文 (auth)」，``redis`` 仍是方法参数
    （因为不是每个端点都用到）。调用方写法由 ``XxxService.method_service(auth=...)``
    改为 ``XxxService(auth).method(...)``。
    """

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> DictTypeOutSchema:
        """
        获取数据字典类型详情

        参数:
        - id (int): 数据字典类型ID

        返回:
        - DictTypeOutSchema: 字典类型响应模型
        """
        return await DictTypeCRUD(self.auth).get_or_404(id=id, out_schema=DictTypeOutSchema)

    async def get_list(
        self,
        search: DictTypeQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[DictTypeOutSchema]:
        """
        获取数据字典类型列表

        参数:
        - search (DictTypeQueryParam | None): 搜索条件模型
        - order_by (list[dict] | None): 排序字段列表

        返回:
        - list[DictTypeOutSchema]: 字典类型响应模型列表
        """
        obj_list = await DictTypeCRUD(self.auth).get_list(search=vars(search) if search else None, order_by=order_by)
        return [DictTypeOutSchema.model_validate(obj) for obj in obj_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: DictTypeQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> dict:
        """
        分页查询字典类型（数据库 OFFSET/LIMIT）。

        参数:
        - page_no (int): 页码（从 1 开始）
        - page_size (int): 每页条数
        - search (DictTypeQueryParam | None): 查询条件
        - order_by (list[dict] | None): 排序字段列表

        返回:
        - dict: 分页结果（结构由 ``CRUD.page`` 返回约定）
        """
        offset = (page_no - 1) * page_size
        return await DictTypeCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=DictTypeOutSchema,
        )

    async def create(self, redis: Redis, data: DictTypeCreateSchema) -> DictTypeOutSchema:
        """
        创建数据字典类型

        参数:
        - redis (Redis): Redis客户端
        - data (DictTypeCreateSchema): 数据字典类型创建模型

        返回:
        - DictTypeOutSchema: 字典类型响应模型
        """
        exist_obj = await DictTypeCRUD(self.auth).get(dict_name=data.dict_name)
        if exist_obj:
            raise CustomException(msg="创建失败，该数据已存在")
        obj = await DictTypeCRUD(self.auth).create(data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj)

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{data.dict_type}"

        try:
            await RedisCURD(redis).set(
                key=redis_key,
                value="[]",
                expire=None,
            )
            logger.info(f"创建字典类型成功: {new_obj_dict}")
        except Exception as e:
            logger.error(f"创建字典类型失败: {e}")
            raise CustomException(msg="同步字典类型缓存失败") from e

        return new_obj_dict

    async def update(
        self,
        redis: Redis,
        id: int,
        data: DictTypeUpdateSchema,
    ) -> DictTypeOutSchema:
        """
        更新数据字典类型

        参数:
        - redis (Redis): Redis客户端
        - id (int): 数据字典类型ID
        - data (DictTypeUpdateSchema): 数据字典类型更新模型

        返回:
        - DictTypeOutSchema: 字典类型响应模型
        """
        exist_obj = await DictTypeCRUD(self.auth).get_or_404(id=id, msg="更新失败，该数据不存在")
        if exist_obj.dict_name != data.dict_name:
            raise CustomException(msg="更新失败，数据字典类型名称不可以修改")

        # 如果字典类型修改或状态变更，则修改对应字典数据的类型和状态
        if exist_obj.dict_type != data.dict_type or exist_obj.status != data.status:
            exist_obj_type_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": exist_obj.dict_type})
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
                        description=item.description,
                    )
                    await DictDataCRUD(self.auth).update(id=item.id, data=dict_data)

        obj = await DictTypeCRUD(self.auth).update(id=id, data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj)

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据，确保包含最新状态
            dict_data_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump(mode="json") for row in dict_data_list if row]

            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                key=redis_key,
                value=value,
                expire=None,
            )
            logger.info(f"更新字典类型成功并刷新缓存: {new_obj_dict}")
        except Exception as e:
            logger.error(f"更新字典类型缓存失败: {e}")
            raise CustomException(msg="同步字典类型缓存失败") from e

        return new_obj_dict

    async def delete(self, redis: Redis, ids: list[int]) -> None:
        """
        删除数据字典类型

        参数:
        - redis (Redis): Redis客户端
        - ids (list[int]): 数据字典类型ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        existing = await DictTypeCRUD(self.auth).get_list(search={"id": ("in", ids)})
        existing_map = {obj.id: obj for obj in existing}
        for nid in ids:
            if nid not in existing_map:
                raise CustomException(msg="删除失败，该数据不存在")
            exist_obj = existing_map[nid]
            # 检查是否有字典数据
            exist_obj_type_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": exist_obj.dict_type})
            if len(exist_obj_type_list) > 0:
                # 如果有字典数据，不能删除
                raise CustomException(msg="删除失败，该数据字典类型下存在字典数据")
            # 删除Redis缓存
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{exist_obj.dict_type}"
            try:
                await RedisCURD(redis).delete(redis_key)
                logger.info(f"删除字典类型成功: {nid}")
            except Exception as e:
                logger.error(f"删除字典类型失败: {e}")
                raise CustomException(msg="同步删除字典缓存失败") from e
        await DictTypeCRUD(self.auth).delete(ids=ids)

    async def set_available(self, data: BatchSetAvailable) -> None:
        """
        设置数据字典类型状态

        参数:
        - data (BatchSetAvailable): 批量设置状态模型

        返回:
        - None
        """
        await DictTypeCRUD(self.auth).set(ids=data.ids, status=data.status)

    @staticmethod
    def export(data_list: list[dict]) -> bytes:
        """
        导出数据字典类型列表（无状态工具方法）

        参数:
        - data_list (list[dict]): 数据字典类型列表

        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            "id": "编号",
            "dict_name": "字典名称",
            "dict_type": "字典类型",
            "status": "状态",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "created_id": "创建者ID",
            "updated_id": "更新者ID",
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item["status"] = "启用" if item.get("status") == 0 else "停用"

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)


class DictDataService:
    """
    字典数据管理服务

    设计同 DictTypeService：实例方法 + ``__init__(auth)``。
    """

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> DictDataOutSchema:
        """
        获取数据字典数据详情

        参数:
        - id (int): 数据字典数据ID

        返回:
        - DictDataOutSchema: 字典数据响应模型
        """
        return await DictDataCRUD(self.auth).get_or_404(id=id, out_schema=DictDataOutSchema)

    async def get_list(
        self,
        search: DictDataQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[DictDataOutSchema]:
        """
        获取数据字典数据列表

        参数:
        - search (DictDataQueryParam | None): 搜索条件模型
        - order_by (list[dict] | None): 排序字段列表

        返回:
        - list[DictDataOutSchema]: 字典数据响应模型列表
        """
        obj_list = await DictDataCRUD(self.auth).get_list(search=vars(search) if search else None, order_by=order_by)
        return [DictDataOutSchema.model_validate(obj) for obj in obj_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: DictDataQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> dict:
        """
        分页查询字典数据（数据库 OFFSET/LIMIT）。

        参数:
        - page_no (int): 页码（从 1 开始）
        - page_size (int): 每页条数
        - search (DictDataQueryParam | None): 查询条件
        - order_by (list[dict] | None): 排序字段列表

        返回:
        - dict: 分页结果（结构由 ``CRUD.page`` 返回约定）
        """
        offset = (page_no - 1) * page_size
        return await DictDataCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=DictDataOutSchema,
        )

    @staticmethod
    async def init_cache(redis: Redis) -> None:
        """
        应用初始化: 获取所有字典类型对应的字典数据信息并按租户缓存（无 auth）。

        参数:
        - redis (Redis): Redis客户端

        返回:
        - None
        """
        try:
            async with async_db_session() as session:
                async with session.begin():
                    init_auth = AuthSchema(db=session, check_data_scope=False)
                    obj_list = await DictTypeCRUD(init_auth).get_list()
                    if not obj_list:
                        logger.warning("未找到任何字典类型数据")
                        return

                    for obj in obj_list:
                        dict_type = obj.dict_type
                        tenant_id = obj.tenant_id
                        try:
                            dict_data_list = await DictDataCRUD(init_auth).get_list(
                                search={"dict_type": dict_type, "tenant_id": tenant_id}
                            )
                            dict_data = [
                                DictDataOutSchema.model_validate(row).model_dump(mode="json")
                                for row in dict_data_list
                                if row
                            ]
                            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{tenant_id}:{dict_type}"
                            value = json.dumps(dict_data, ensure_ascii=False)
                            await RedisCURD(redis).set(
                                key=redis_key,
                                value=value,
                                expire=None,
                            )
                        except Exception as e:
                            logger.error(f"❌ 初始化字典数据失败 [{dict_type}]: {e}")

        except Exception as e:
            logger.error(f"字典初始化过程发生错误: {e}")
            raise CustomException(msg="字典数据初始化失败") from e

    @staticmethod
    async def get_init_cache(redis: Redis, dict_type: str, tenant_id: int = 1) -> list[dict]:
        """
        从缓存获取字典数据列表信息（无 auth）。

        参数:
        - redis (Redis): Redis客户端
        - dict_type (str): 字典类型
        - tenant_id (int): 租户ID

        返回:
        - list[dict]: 字典数据列表
        """
        try:
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{tenant_id}:{dict_type}"
            obj_list_dict = await RedisCURD(redis).get(redis_key)

            if obj_list_dict:
                if isinstance(obj_list_dict, str):
                    try:
                        return json.loads(obj_list_dict)
                    except json.JSONDecodeError:
                        logger.warning(f"字典数据反序列化失败，尝试重新初始化缓存: {dict_type}")
                elif isinstance(obj_list_dict, list):
                    return obj_list_dict

            await DictDataService.init_cache(redis)
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{tenant_id}:{dict_type}"
            obj_list_dict = await RedisCURD(redis).get(redis_key)
            if not obj_list_dict:
                raise CustomException(msg="该数据不存在")

            if isinstance(obj_list_dict, str):
                try:
                    return json.loads(obj_list_dict)
                except json.JSONDecodeError:
                    raise CustomException(msg="字典数据格式错误") from None
            return obj_list_dict
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"获取字典缓存失败: {e!s}")
            raise CustomException(msg="获取字典数据失败") from e

    async def create(self, redis: Redis, data: DictDataCreateSchema) -> DictDataOutSchema:
        """
        创建数据字典数据

        参数:
        - redis (Redis): Redis客户端
        - data (DictDataCreateSchema): 数据字典数据创建模型

        返回:
        - DictDataOutSchema: 字典数据响应模型
        """
        # 检查相同字典类型下dict_label是否已存在
        exist_label_obj = await DictDataCRUD(self.auth).get(dict_type=data.dict_type, dict_label=data.dict_label)
        if exist_label_obj:
            raise CustomException(msg=f'创建失败，该字典类型下的字典标签"{data.dict_label}"已存在')

        # 检查相同字典类型下dict_value是否已存在
        exist_value_obj = await DictDataCRUD(self.auth).get(dict_type=data.dict_type, dict_value=data.dict_value)
        if exist_value_obj:
            raise CustomException(msg=f'创建失败，该字典类型下的字典键值"{data.dict_value}"已存在')

        obj = await DictDataCRUD(self.auth).create(data=data)

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump(mode="json") for row in dict_data_list if row]

            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                key=redis_key,
                value=value,
                expire=None,
            )
            logger.info(f"创建字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"创建字典数据写入缓存失败: {e}")
            raise CustomException(msg="同步字典数据缓存失败") from e

        return DictDataOutSchema.model_validate(obj)

    async def update(
        self,
        redis: Redis,
        id: int,
        data: DictDataUpdateSchema,
    ) -> DictDataOutSchema:
        """
        更新数据字典数据

        参数:
        - redis (Redis): Redis客户端
        - id (int): 数据字典数据ID
        - data (DictDataUpdateSchema): 数据字典数据更新模型

        返回:
        - DictDataOutSchema: 字典数据响应模型
        """
        exist_obj = await DictDataCRUD(self.auth).get_or_404(id=id, msg="更新失败，该数据不存在")

        # 检查相同字典类型下dict_label是否已存在（排除当前记录）
        if exist_obj.dict_label != data.dict_label:
            exist_label_obj = await DictDataCRUD(self.auth).get(dict_type=data.dict_type, dict_label=data.dict_label)
            if exist_label_obj:
                raise CustomException(msg=f'更新失败，该字典类型下的字典标签"{data.dict_label}"已存在')

        # 检查相同字典类型下dict_value是否已存在（排除当前记录）
        if exist_obj.dict_value != data.dict_value:
            exist_value_obj = await DictDataCRUD(self.auth).get(dict_type=data.dict_type, dict_value=data.dict_value)
            if exist_value_obj:
                raise CustomException(msg=f'更新失败，该字典类型下的字典键值"{data.dict_value}"已存在')

        # 如果字典类型变更，仅刷新旧类型缓存，不联动字典类型状态
        if exist_obj.dict_type != data.dict_type:
            dict_type = await DictTypeCRUD(self.auth).get(dict_type=exist_obj.dict_type)
            if dict_type:
                redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{dict_type.dict_type}"
                try:
                    dict_data_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": dict_type.dict_type})
                    dict_data = [DictDataOutSchema.model_validate(row).model_dump(mode="json") for row in dict_data_list if row]
                    value = json.dumps(dict_data, ensure_ascii=False)
                    await RedisCURD(redis).set(
                        key=redis_key,
                        value=value,
                        expire=None,
                    )
                except Exception as e:
                    logger.error(f"刷新旧字典缓存失败: {e}")
                    raise CustomException(msg="同步旧字典数据缓存失败") from e

        obj = await DictDataCRUD(self.auth).update(id=id, data=data)

        # 刷新新字典类型缓存
        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{data.dict_type}"
        try:
            dict_data_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump(mode="json") for row in dict_data_list if row]
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                key=redis_key,
                value=value,
                expire=None,
            )
            logger.info(f"更新字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"更新字典数据写入缓存失败: {e}")
            raise CustomException(msg="同步字典数据缓存失败") from e

        return DictDataOutSchema.model_validate(obj)

    async def delete(self, redis: Redis, ids: list[int]) -> None:
        """
        删除数据字典数据

        参数:
        - redis (Redis): Redis客户端
        - ids (list[int]): 数据字典数据ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        existing = await DictDataCRUD(self.auth).get_list(search={"id": ("in", ids)})
        existing_map = {obj.id: obj for obj in existing}
        for nid in ids:
            if nid not in existing_map:
                raise CustomException(msg="删除失败，该数据不存在")
            exist_obj = existing_map[nid]
            # 删除该字典类型缓存中的对应项
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{self.auth.user.tenant_id}:{exist_obj.dict_type}"
            try:
                # 重新拉取该类型所有字典数据并写回缓存（保持一致）
                dict_data_list = await DictDataCRUD(self.auth).get_list(search={"dict_type": exist_obj.dict_type})
                dict_data = [DictDataOutSchema.model_validate(row).model_dump(mode="json") for row in dict_data_list if row]
                value = json.dumps(dict_data, ensure_ascii=False)
                await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=None,
                )
                logger.info(f"删除字典数据并刷新缓存: {nid}")
            except Exception as e:
                logger.error(f"删除字典数据刷新缓存失败: {e}")
                raise CustomException(msg="同步删除字典数据缓存失败") from e
        await DictDataCRUD(self.auth).delete(ids=ids)

    async def set_available(self, data: BatchSetAvailable) -> None:
        """
        设置数据字典数据状态

        参数:
        - data (BatchSetAvailable): 批量设置状态模型

        返回:
        - None
        """
        await DictDataCRUD(self.auth).set(ids=data.ids, status=data.status)

    @staticmethod
    def export(data_list: list[dict]) -> bytes:
        """
        导出数据字典数据列表（无状态工具方法）

        参数:
        - data_list (list[dict]): 数据字典数据列表

        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            "id": "编号",
            "dict_type": "字典类型",
            "dict_label": "字典标签",
            "dict_value": "字典键值",
            "dict_sort": "字典排序",
            "status": "状态",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "created_id": "创建者ID",
            "updated_id": "更新者ID",
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            item["status"] = "启用" if item.get("status") == 0 else "停用"
            if item.get("is_default") is True:
                item["is_default"] = "是"
            else:
                item["is_default"] = "否"

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
