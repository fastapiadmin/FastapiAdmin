import json

from fastapi import UploadFile
from redis.asyncio.client import Redis

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.enums import RedisInitKeyConfig
from app.core.base_schema import UploadResponseSchema
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.utils.excel_util import ExcelUtil
from app.utils.upload_util import UploadUtil

from .crud import ParamsCRUD
from .schema import (
    ParamsCreateSchema,
    ParamsOutSchema,
    ParamsQueryParam,
    ParamsUpdateSchema,
)


class ParamsService:
    """
    配置管理模块服务层
    """

    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取配置详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 配置管理型ID

        返回:
        - dict: 配置管理型模型实例字典表示
        """
        obj = await ParamsCRUD(auth).get_obj_by_id_crud(id=id)
        return ParamsOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_obj_by_key_service(cls, auth: AuthSchema, config_key: str) -> dict:
        """
        根据配置键获取配置详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - config_key (str): 配置管理型key

        返回:
        - Dict: 配置管理型模型实例字典表示
        """
        obj = await ParamsCRUD(auth).get_obj_by_key_crud(key=config_key)
        if not obj:
            raise CustomException(msg=f"配置键 {config_key} 不存在")
        return ParamsOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_config_value_by_key_service(cls, auth: AuthSchema, config_key: str) -> str | None:
        """
        根据配置键获取配置值

        参数:
        - auth (AuthSchema): 认证信息模型
        - config_key (str): 配置管理型key

        返回:
        - str | None: 配置值字符串或None
        """
        obj = await ParamsCRUD(auth).get_obj_by_key_crud(key=config_key)
        if not obj:
            raise CustomException(msg=f"配置键 {config_key} 不存在")
        return obj.config_value

    @classmethod
    async def get_obj_list_service(
        cls,
        auth: AuthSchema,
        search: ParamsQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
        """
        获取配置管理型列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (ParamsQueryParam | None): 查询参数对象
        - order_by (list[dict] | None): 排序参数列表

        返回:
        - list[dict]: 配置管理型模型实例字典列表表示
        """
        obj_list = None
        if search:
            obj_list = await ParamsCRUD(auth).get_obj_list_crud(
                search=search.__dict__, order_by=order_by
            )
        else:
            obj_list = await ParamsCRUD(auth).get_obj_list_crud()
        return [ParamsOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_obj_service(
        cls, auth: AuthSchema, redis: Redis, data: ParamsCreateSchema
    ) -> dict:
        """
        创建配置管理型

        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis 客户端实例
        - data (ParamsCreateSchema): 配置管理型创建模型

        返回:
        - dict: 新创建的配置管理型模型实例字典表示
        """
        exist_obj = await ParamsCRUD(auth).get(config_key=data.config_key)
        if exist_obj:
            raise CustomException(msg="创建失败，该配置key已存在")
        obj = await ParamsCRUD(auth).create_obj_crud(data=data)

        new_obj_dict = ParamsOutSchema.model_validate(obj).model_dump()

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{data.config_key}"
        try:
            result = await RedisCURD(redis).set(
                key=redis_key,
                value="",
            )
            if not result:
                log.error(f"同步配置到缓存失败: {new_obj_dict}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            log.error(f"创建字典类型失败: {e}")
            raise CustomException(msg=f"创建字典类型失败 {e}")

        return new_obj_dict

    @classmethod
    async def update_obj_service(
        cls, auth: AuthSchema, redis: Redis, id: int, data: ParamsUpdateSchema
    ) -> dict:
        """
        更新配置管理型

        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis 客户端实例
        - id (int): 配置管理型ID
        - data (ParamsUpdateSchema): 配置管理型更新模型

        返回:
        - Dict: 更新后的配置管理型模型实例字典表示
        """
        exist_obj = await ParamsCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg="更新失败，该数系统配置不存在")
        if exist_obj.config_key != data.config_key:
            raise CustomException(msg="更新失败，系统配置key不允许修改")

        new_obj = await ParamsCRUD(auth).update_obj_crud(id=id, data=data)
        if not new_obj:
            raise CustomException(msg="更新失败，系统配置不存在")
        new_obj_dict = ParamsOutSchema.model_validate(new_obj).model_dump()

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{new_obj.config_key}"
        try:
            value = json.dumps(new_obj_dict, ensure_ascii=False)
            result = await RedisCURD(redis).set(
                key=redis_key,
                value=value,
            )
            if not result:
                log.error(f"同步配置到缓存失败: {new_obj_dict}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            log.error(f"更新系统配置失败: {e}")
            raise CustomException(msg="更新系统配置失败")

        return new_obj_dict

    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, ids: list[int]) -> None:
        """
        删除配置管理型

        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis 客户端实例
        - ids (list[int]): 配置管理型ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            exist_obj = await ParamsCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg="删除失败，该数据字典类型不存在")
            # 检查是否是否初始化类型
            if exist_obj.config_type:
                # 如果有字典数据，不能删除
                raise CustomException(
                    msg=f"{exist_obj.config_name} 删除失败，系统初始化配置不可以删除"
                )

        await ParamsCRUD(auth).delete_obj_crud(ids=ids)

        # 同步删除Redis缓存
        for id in ids:
            exist_obj = await ParamsCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                continue
            redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{exist_obj.config_key}"
            try:
                await RedisCURD(redis).delete(redis_key)
                log.info(f"删除系统配置成功: {id}")
            except Exception as e:
                log.error(f"删除系统配置失败: {e}")
                raise CustomException(msg="删除字典类型失败")

    @classmethod
    async def export_obj_service(cls, data_list: list[dict]) -> bytes:
        """
        导出系统配置列表

        参数:
        - data_list (list[dict]): 系统配置模型实例字典列表表示

        返回:
        - bytes: Excel文件二进制数据
        """
        mapping_dict = {
            "id": "编号",
            "config_name": "参数名称",
            "config_key": "参数键名",
            "config_value": "参数键值",
            "config_type": "系统内置((True:是 False:否))",
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
            item["config_type"] = "是" if item.get("config_type") else "否"
            item["creator"] = (
                item.get("creator", {}).get("name", "未知")
                if isinstance(item.get("creator"), dict)
                else "未知"
            )

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def upload_service(cls, base_url: str, file: UploadFile) -> dict:
        """
        上传文件

        参数:
        - base_url (str): 基础URL
        - file (UploadFile): 上传的文件对象

        返回:
        - dict: 上传文件的响应模型实例字典表示
        """
        filename, filepath, file_url = await UploadUtil.upload_file(file=file, base_url=base_url)

        return UploadResponseSchema(
            file_path=f"{filepath}",
            file_name=filename,
            origin_name=file.filename,
            file_url=f"{file_url}",
        ).model_dump()

    @classmethod
    async def init_config_service(cls, redis: Redis) -> None:
        """
        初始化系统配置

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - None
        """
        async with async_db_session() as session:
            async with session.begin():
                # 在初始化过程中，不需要检查数据权限
                auth = AuthSchema(db=session, check_data_scope=False)
                config_obj = await ParamsCRUD(auth).get_obj_list_crud()
                if not config_obj:
                    raise CustomException(msg="系统配置不存在")
                try:
                    # 保存到Redis并设置过期时间
                    for config in config_obj:
                        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{config.config_key}"
                        config_obj_dict = ParamsOutSchema.model_validate(config).model_dump()
                        value = json.dumps(config_obj_dict, ensure_ascii=False)
                        result = await RedisCURD(redis).set(
                            key=redis_key,
                            value=value,
                        )
                        if not result:
                            log.error(f"❌️ 初始化系统配置失败: {config_obj_dict}")
                            raise CustomException(msg="初始化系统配置失败")
                except Exception as e:
                    log.error(f"❌️ 初始化系统配置失败: {e}")
                    raise CustomException(msg="初始化系统配置失败")

    @classmethod
    async def get_init_config_service(cls, redis: Redis) -> list[dict]:
        """
        获取系统配置

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - list[dict]: 系统配置模型实例字典列表表示
        """
        redis_keys = await RedisCURD(redis).get_keys(f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:*")
        redis_configs = await RedisCURD(redis).mget(redis_keys)
        configs = []
        for config in redis_configs:
            if not config:
                continue
            try:
                new_config = json.loads(config)
                configs.append(new_config)
            except Exception as e:
                log.error(f"解析系统配置数据失败: {e}")
                continue

        return configs

    @classmethod
    async def get_system_config_for_middleware(cls, redis: Redis) -> dict:
        """
        获取中间件所需的系统配置

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - dict: 包含演示模式、IP白名单、API白名单和IP黑名单的配置字典
        """
        # 定义需要获取的配置键
        config_keys = [
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:demo_enable",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:ip_white_list",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:white_api_list_path",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:ip_black_list",
        ]

        # 批量获取配置
        config_values = await RedisCURD(redis).mget(config_keys)

        # 初始化默认配置
        config_result = {
            "demo_enable": False,
            "ip_white_list": [],
            "white_api_list_path": [],
            "ip_black_list": [],
        }

        # 解析演示模式配置
        if config_values[0]:
            try:
                demo_config = json.loads(config_values[0])
                config_result["demo_enable"] = (
                    demo_config.get("config_value", False)
                    if isinstance(demo_config, dict)
                    else False
                )
            except json.JSONDecodeError:
                log.error("解析演示模式配置失败")

        # 解析IP白名单配置
        if config_values[1]:
            try:
                ip_white_config = json.loads(config_values[1])
                # 确保是列表类型
                config_result["ip_white_list"] = json.loads(ip_white_config.get("config_value", []))
            except json.JSONDecodeError:
                log.error("解析IP白名单配置失败")
        # 解析IP黑名单
        # 解析API路径白名单
        if config_values[2]:
            try:
                white_api_config = json.loads(config_values[2])
                # 确保是列表类型
                config_result["white_api_list_path"] = json.loads(
                    white_api_config.get("config_value", [])
                )
            except json.JSONDecodeError:
                log.error("解析API白名单配置失败")

        # 解析IP黑名单
        if config_values[3]:
            try:
                black_ip_config = json.loads(config_values[3])
                # 确保是列表类型
                config_result["ip_black_list"] = json.loads(black_ip_config.get("config_value", []))
            except json.JSONDecodeError:
                log.error("解析IP黑名单配置失败")
        return config_result
