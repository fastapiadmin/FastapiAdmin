import json
import time

from redis.asyncio.client import Redis

from app.common.enums import RedisInitKeyConfig
from app.core.base_schema import AuthSchema
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.utils.excel_util import ExcelUtil

from .crud import ParamsCRUD
from .schema import (
    ParamsCreateSchema,
    ParamsOutSchema,
    ParamsQueryParam,
    ParamsUpdateSchema,
)

# 中间件系统配置内存缓存（避免每请求查 Redis）
_MID_CONFIG_TTL: float = 60.0  # 缓存 60 秒
_mid_config_cache: dict = {"ts": 0.0, "data": None}


class ParamsService:
    """
    参数管理服务

    设计：实例方法承载「当前用户上下文 (auth)」，``redis`` 仍是方法参数
    （因为不是每个端点都用到）。调用方写法由
    ``ParamsService.method_service(auth=...)`` 改为 ``ParamsService(auth).method(...)``。
    """

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> ParamsOutSchema:
        """
        获取参数详情

        参数:
        - id (int): 参数ID

        返回:
        - ParamsOutSchema: 参数响应模型
        """
        return await ParamsCRUD(self.auth).get_or_404(id=id, out_schema=ParamsOutSchema)

    async def get_by_key(self, config_key: str) -> ParamsOutSchema:
        """
        根据配置键获取参数详情

        参数:
        - config_key (str): 参数键名

        返回:
        - ParamsOutSchema: 参数响应模型
        """
        obj = await ParamsCRUD(self.auth).get(config_key=config_key)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return ParamsOutSchema.model_validate(obj)

    async def get_config_value_by_key(self, config_key: str) -> str | None:
        """
        根据配置键获取参数值

        参数:
        - config_key (str): 参数键名

        返回:
        - str | None: 参数键值字符串或 None
        """
        obj = await ParamsCRUD(self.auth).get(config_key=config_key)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return obj.config_value

    async def get_list(
        self,
        search: ParamsQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[ParamsOutSchema]:
        """
        获取配置管理型列表

        参数:
        - search (ParamsQueryParam | None): 查询参数对象
        - order_by (list[dict] | None): 排序参数列表

        返回:
        - list[ParamsOutSchema]: 参数响应模型列表
        """
        obj_list = await ParamsCRUD(self.auth).get_list(search=vars(search) if search else None, order_by=order_by)
        return [ParamsOutSchema.model_validate(obj) for obj in obj_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: ParamsQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询系统参数（数据库 OFFSET/LIMIT）。

        参数:
        - page_no (int): 页码（从 1 开始）
        - page_size (int): 每页条数
        - search (ParamsQueryParam | None): 查询条件
        - order_by (list[dict[str, str]] | None): 排序字段列表

        返回:
        - dict: 分页结果（结构由 ``CRUD.page`` 返回约定）
        """
        offset = (page_no - 1) * page_size
        return await ParamsCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=ParamsOutSchema,
        )

    async def create(self, redis: Redis, data: ParamsCreateSchema) -> ParamsOutSchema:
        """
        创建配置管理型

        参数:
        - redis (Redis): Redis 客户端实例
        - data (ParamsCreateSchema): 配置管理型创建模型

        返回:
        - ParamsOutSchema: 新创建的参数响应模型
        """
        exist_obj = await ParamsCRUD(self.auth).get(config_key=data.config_key)
        if exist_obj:
            raise CustomException(msg="创建失败，该数据已存在")
        obj = await ParamsCRUD(self.auth).create(data=data)

        out = ParamsOutSchema.model_validate(obj)

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{self.auth.user.tenant_id}:{data.config_key}"
        try:
            redis_payload = out.model_dump(mode="json")
            value = json.dumps(redis_payload, ensure_ascii=False)
            result = await RedisCURD(redis).set(
                key=redis_key,
                value=value,
                expire=None,
            )
            if not result:
                logger.error(f"同步配置到缓存失败: {out}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            logger.error(f"创建字典类型失败: {e}")
            raise CustomException(msg="同步配置到缓存失败") from e

        return out

    async def update(self, redis: Redis, id: int, data: ParamsUpdateSchema) -> ParamsOutSchema:
        """
        更新参数

        参数:
        - redis (Redis): Redis 客户端实例
        - id (int): 参数ID
        - data (ParamsUpdateSchema): 参数更新模型

        返回:
        - ParamsOutSchema: 更新后的参数响应模型
        """
        exist_obj = await ParamsCRUD(self.auth).get_or_404(id=id, msg="更新失败，该数据不存在")
        if exist_obj.config_key != data.config_key:
            raise CustomException(msg="更新失败，系统配置key不允许修改")

        new_obj = await ParamsCRUD(self.auth).update(id=id, data=data)
        if not new_obj:
            raise CustomException(msg="更新失败，系统配置不存在")
        out = ParamsOutSchema.model_validate(new_obj)
        redis_payload = out.model_dump(mode="json")

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{self.auth.user.tenant_id}:{new_obj.config_key}"
        try:
            value = json.dumps(redis_payload, ensure_ascii=False)
            result = await RedisCURD(redis).set(
                key=redis_key,
                value=value,
                expire=None,
            )
            if not result:
                logger.error(f"同步配置到缓存失败: {out}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            logger.error(f"更新系统配置失败: {e}")
            raise CustomException(msg="同步配置到缓存失败") from e

        return out

    async def delete(self, redis: Redis, ids: list[int]) -> None:
        """
        删除配置管理型

        参数:
        - redis (Redis): Redis 客户端实例
        - ids (list[int]): 配置管理型ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        # 批量校验参数存在性
        objs = await ParamsCRUD(self.auth).get_list(search={"id": ("in", ids)})
        obj_map = {o.id: o for o in objs}
        for pid in ids:
            obj = obj_map.get(pid)
            if not obj:
                raise CustomException(msg="删除失败，该数据不存在")
            if obj.config_type:
                raise CustomException(msg=f"{obj.config_name} 删除失败，系统初始化配置不可以删除")

        await ParamsCRUD(self.auth).delete(ids=ids)

        # 同步删除Redis缓存（使用删除前已获取的对象信息）
        for obj in objs:
            redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{self.auth.user.tenant_id}:{obj.config_key}"
            try:
                await RedisCURD(redis).delete(redis_key)
            except Exception as e:
                logger.error(f"删除系统配置失败: {e}")
                raise CustomException(msg="同步删除缓存失败") from e

    async def batch_set_status(self, ids: list[int], status: int) -> None:
        """
        批量设置系统参数状态

        参数:
        - ids (list[int]): 系统参数ID列表
        - status (str): 状态值

        返回:
        - None
        """
        if not ids:
            raise CustomException(msg="请选择要操作的数据")

        await ParamsCRUD(self.auth).set(ids=ids, status=status)

    @staticmethod
    def export(data_list: list[dict]) -> bytes:
        """
        导出参数列表（无状态工具方法）

        参数:
        - data_list (list[dict]): 参数字典列表

        返回:
        - bytes: Excel 文件字节流
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

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @staticmethod
    async def init_cache(redis: Redis) -> None:
        """
        初始化系统参数并按租户缓存（无 auth）。

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - None
        """
        async with async_db_session() as session:
            async with session.begin():
                init_auth = AuthSchema(db=session, check_data_scope=False)
                config_obj = await ParamsCRUD(init_auth).get_list()
                if not config_obj:
                    raise CustomException(msg="该数据不存在")
                try:
                    for config in config_obj:
                        tenant_id = config.tenant_id
                        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{tenant_id}:{config.config_key}"
                        out = ParamsOutSchema.model_validate(config)
                        redis_payload = out.model_dump(mode="json")
                        value = json.dumps(redis_payload, ensure_ascii=False)
                        result = await RedisCURD(redis).set(
                            key=redis_key,
                            value=value,
                            expire=None,
                        )
                        if not result:
                            logger.error(f"❌️ 初始化系统配置失败: {redis_key}")
                            raise CustomException(msg="初始化系统配置失败")
                except Exception as e:
                    logger.error(f"❌️ 初始化系统配置失败: {e}")
                    raise CustomException(msg="初始化系统配置失败") from e

    @staticmethod
    async def get_init_cache(redis: Redis, tenant_id: int = 1) -> list[dict]:
        """
        获取系统配置（无 auth）。

        参数:
        - redis (Redis): Redis 客户端实例
        - tenant_id (int): 租户ID

        返回:
        - list[dict]: 系统配置字典列表
        """
        redis_keys = await RedisCURD(redis).get_keys(f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{tenant_id}:*")
        redis_configs = await RedisCURD(redis).mget(redis_keys)
        configs = []
        for config in redis_configs:
            if not config:
                continue
            try:
                new_config = json.loads(config)
                configs.append(new_config)
            except Exception as e:
                logger.error(f"解析系统配置数据失败: {e}")
                continue

        # 如果 Redis 中没有数据，从数据库中加载并缓存
        if not configs:
            async with async_db_session() as session:
                async with session.begin():
                    init_auth = AuthSchema(db=session, check_data_scope=False)
                    config_obj = await ParamsCRUD(init_auth).get_list()
                    if config_obj:
                        try:
                            for config in config_obj:
                                redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{tenant_id}:{config.config_key}"
                                out = ParamsOutSchema.model_validate(config)
                                config_obj_dict = out.model_dump()
                                redis_payload = out.model_dump(mode="json")
                                value = json.dumps(redis_payload, ensure_ascii=False)
                                result = await RedisCURD(redis).set(
                                    key=redis_key,
                                    value=value,
                                    expire=None,
                                )
                                if not result:
                                    logger.error(f"❌️ 缓存系统配置失败: {config_obj_dict}")
                                configs.append(config_obj_dict)
                        except Exception as e:
                            logger.error(f"❌️ 加载系统配置失败: {e}")

        return configs

    @staticmethod
    async def get_system_config_for_middleware(redis: Redis) -> dict:
        """
        获取中间件所需的系统配置（带 60 秒内存缓存，避免每请求查 Redis）。

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - dict: 包含演示模式、IP白名单、API白名单和IP黑名单的配置字典
        """
        now = time.monotonic()
        if _mid_config_cache["data"] and now - _mid_config_cache["ts"] < _MID_CONFIG_TTL:
            return _mid_config_cache["data"]

        config_result = await ParamsService._fetch_system_config_for_middleware(redis)
        _mid_config_cache["data"] = config_result
        _mid_config_cache["ts"] = now
        return config_result

    @staticmethod
    async def _fetch_system_config_for_middleware(redis: Redis) -> dict:
        # 定义需要获取的配置键
        config_keys = [
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:1:demo_enable",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:1:ip_white_list",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:1:white_api_list_path",
            f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:1:ip_black_list",
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
                    demo_config.get("config_value", False) if isinstance(demo_config, dict) else False
                )
            except json.JSONDecodeError:
                logger.error("解析演示模式配置失败")

        # 解析IP白名单配置
        if config_values[1]:
            try:
                ip_white_config = json.loads(config_values[1])
                # 确保是列表类型
                config_result["ip_white_list"] = json.loads(ip_white_config.get("config_value", []))
            except json.JSONDecodeError:
                logger.error("解析IP白名单配置失败")
        # 解析IP黑名单
        # 解析API路径白名单
        if config_values[2]:
            try:
                white_api_config = json.loads(config_values[2])
                # 确保是列表类型
                config_result["white_api_list_path"] = json.loads(white_api_config.get("config_value", []))
            except json.JSONDecodeError:
                logger.error("解析API白名单配置失败")

        # 解析IP黑名单
        if config_values[3]:
            try:
                black_ip_config = json.loads(config_values[3])
                # 确保是列表类型
                config_result["ip_black_list"] = json.loads(black_ip_config.get("config_value", []))
            except json.JSONDecodeError:
                logger.error("解析IP黑名单配置失败")
        return config_result
