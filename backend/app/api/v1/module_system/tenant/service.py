import json
import random
import string
from datetime import datetime

import sqlalchemy as sa
from redis.asyncio.client import Redis

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.role.crud import RoleCRUD
from app.api.v1.module_system.user.crud import UserCRUD
from app.common.enums import RedisInitKeyConfig
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.utils.hash_bcrpy_util import PwdUtil

from .crud import TenantCRUD
from .model import (
    TenantConfigModel,
    TenantMenuModel,
    TenantModel,
    TenantQuotaModel,
    TenantUserModel,
)
from .schema import (
    TenantConfigItem,
    TenantConfigOutSchema,
    TenantCreateSchema,
    TenantMenuSetSchema,
    TenantOutSchema,
    TenantQueryParam,
    TenantQuotaOutSchema,
    TenantQuotaUpdateSchema,
    TenantUpdateSchema,
    TenantUserAddSchema,
    TenantUserOutSchema,
)


class TenantService:
    """租户管理模块服务层"""

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="租户不存在")
        result = TenantOutSchema.model_validate(obj).model_dump()
        return result

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: TenantQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        return await TenantCRUD(auth).page_crud(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=search.__dict__ if search else {},
            out_schema=TenantOutSchema,
        )

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: TenantCreateSchema) -> dict:
        if await TenantCRUD(auth).get(name=data.name):
            raise CustomException(msg="创建失败，名称已存在")
        if await TenantCRUD(auth).get(code=data.code):
            raise CustomException(msg="创建失败，编码已存在")

        tenant_obj = await TenantCRUD(auth).create_crud(data=data)
        if not tenant_obj:
            raise CustomException(msg="创建租户失败")

        # 创建租户初始管理员
        # 1. 生成初始管理员用户名
        # 2. 检查用户名是否已存在
        # 3. 创建初始管理员用户
        username = f"{tenant_obj.code}_admin"
        if await UserCRUD(auth).get_by_username_crud(username=username):
            raise CustomException(msg=f"初始管理员用户名已存在: {username}，请更换租户编码后重试")

        password_length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(characters) for _ in range(password_length))
        admin_data = {
            "username": username,
            "password": PwdUtil.set_password_hash(password=password),
            "name": f"{tenant_obj.name}管理员",
            "tenant_id": tenant_obj.id,
            "status": "0",
            "is_superuser": False,
        }
        try:
            user_obj = await UserCRUD(auth).create(data=admin_data)
            if not user_obj:
                raise CustomException(msg="创建租户初始管理员失败")
            auth.db.add(
                TenantUserModel(
                    user_id=user_obj.id,
                    tenant_id=tenant_obj.id,
                    role="admin",
                    is_default=1,
                    create_time=datetime.now(),
                )
            )
            await auth.db.flush()
        except CustomException:
            raise
        except Exception as e:
            log.error(f"为租户[{tenant_obj.name}]创建初始管理员失败: {e!s}")
            raise CustomException(msg="创建租户初始管理员失败")

        log.info(
            f"为租户[{tenant_obj.name}]创建初始管理员成功，用户名: {username}，临时密码: {password}"
        )

        await auth.db.refresh(tenant_obj)
        result = TenantOutSchema.model_validate(tenant_obj).model_dump()

        # P1: 自动初始化租户配额
        quota = TenantQuotaModel(tenant_id=tenant_obj.id)
        auth.db.add(quota)
        await auth.db.flush()

        return result

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: TenantUpdateSchema) -> dict:
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="租户不存在")

        if id == 1:
            if data.code is not None and data.code != obj.code:
                raise CustomException(msg="系统租户编码不可修改")
            if data.status is not None and data.status == "1":
                raise CustomException(msg="系统租户不允许禁用")

        if data.name is not None:
            exist = await TenantCRUD(auth).get(name=data.name)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，名称重复")
        if data.code is not None:
            exist = await TenantCRUD(auth).get(code=data.code)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，编码重复")

        updated = await TenantCRUD(auth).update_crud(id=id, data=data)
        if not updated:
            raise CustomException(msg="更新失败")
        result = TenantOutSchema.model_validate(updated).model_dump()
        return result

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")
        if 1 in ids:
            raise CustomException(msg="系统租户不允许删除")
        for id in ids:
            obj = await TenantCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                continue
        for tid in ids:
            reasons: list[str] = []
            if await UserCRUD(auth).list(search={"tenant_id": tid}):
                reasons.append("用户")
            if await DeptCRUD(auth).list(search={"tenant_id": tid}):
                reasons.append("部门")
            if await RoleCRUD(auth).list(search={"tenant_id": tid}):
                reasons.append("角色")
            if await PositionCRUD(auth).list(search={"tenant_id": tid}):
                reasons.append("岗位")
            if reasons:
                raise CustomException(
                    msg=f"租户 ID={tid} 下仍有关联数据（{','.join(reasons)}），请先清理后再删除"
                )
        await TenantCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        if data.status == "1" and 1 in data.ids:
            raise CustomException(msg="系统租户不允许禁用")
        await TenantCRUD(auth).set_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def toggle_status_service(cls, auth: AuthSchema, id: int) -> None:
        """切换单个租户的启用/禁用状态"""
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="租户不存在")
        if id == 1:
            raise CustomException(msg="系统租户不允许禁用")
        new_status = "0" if obj.status == "1" else "1"
        await TenantCRUD(auth).set_available_crud(ids=[id], status=new_status)

    @classmethod
    async def get_tenant_users_service(
        cls, auth: AuthSchema, tenant_id: int
    ) -> list[dict]:
        """获取租户下的用户列表"""
        from sqlalchemy import select

        from app.api.v1.module_system.user.model import UserModel

        stmt = (
            select(TenantUserModel, UserModel)
            .join(UserModel, UserModel.id == TenantUserModel.user_id)
            .where(TenantUserModel.tenant_id == tenant_id)
            .order_by(TenantUserModel.is_default.desc(), TenantUserModel.id)
        )
        result = await auth.db.execute(stmt)
        rows = result.all()

        users = []
        for tu, u in rows:
            users.append(
                TenantUserOutSchema(
                    id=tu.id,
                    user_id=tu.user_id,
                    tenant_id=tu.tenant_id,
                    role=tu.role,
                    is_default=tu.is_default,
                    create_time=tu.create_time,
                    username=u.username,
                    name=u.name,
                ).model_dump()
            )
        return users

    @classmethod
    async def add_tenant_user_service(
        cls, auth: AuthSchema, tenant_id: int, data: TenantUserAddSchema
    ) -> None:
        """向租户添加用户"""
        # 验证租户存在
        tenant = await TenantCRUD(auth).get_by_id_crud(id=tenant_id)
        if not tenant:
            raise CustomException(msg="租户不存在")

        # 验证用户存在
        from app.api.v1.module_system.user.crud import UserCRUD

        user = await UserCRUD(auth).get_by_id_crud(id=data.user_id)
        if not user:
            raise CustomException(msg="用户不存在")

        # 检查是否已关联
        from sqlalchemy import select

        exist_stmt = (
            select(TenantUserModel)
            .where(
                TenantUserModel.user_id == data.user_id,
                TenantUserModel.tenant_id == tenant_id,
            )
            .limit(1)
        )
        result = await auth.db.execute(exist_stmt)
        if result.scalar_one_or_none():
            raise CustomException(msg="该用户已关联此租户")

        # 如果设为默认租户，先取消其他默认
        if data.is_default == 1:
            await auth.db.execute(
                sa.update(TenantUserModel)
                .where(TenantUserModel.user_id == data.user_id)
                .values(is_default=0)
            )
        elif data.is_default == 0:
            # 检查是否是该用户的第一个租户关联
            count_result = await auth.db.execute(
                select(sa.func.count()).select_from(TenantUserModel).where(
                    TenantUserModel.user_id == data.user_id
                )
            )
            count = count_result.scalar()
            if count == 0:
                # 第一个租户自动设为默认
                data.is_default = 1

        from datetime import datetime

        tu = TenantUserModel(
            user_id=data.user_id,
            tenant_id=tenant_id,
            role=data.role,
            is_default=data.is_default,
            create_time=datetime.now(),
        )
        auth.db.add(tu)
        await auth.db.flush()

        log.info(
            f"向租户[{tenant.name}]添加用户[{user.username}]成功, role={data.role}"
        )

    @classmethod
    async def remove_tenant_user_service(
        cls, auth: AuthSchema, tenant_id: int, user_id: int
    ) -> None:
        """从租户移除用户"""
        from sqlalchemy import select

        # 查找关联记录
        exist_stmt = (
            select(TenantUserModel)
            .where(
                TenantUserModel.user_id == user_id,
                TenantUserModel.tenant_id == tenant_id,
            )
            .limit(1)
        )
        result = await auth.db.execute(exist_stmt)
        tu = result.scalar_one_or_none()
        if not tu:
            raise CustomException(msg="该用户未关联此租户")

        # 不允许移除租户最后一个 owner
        if tu.role == "owner":
            count_result = await auth.db.execute(
                select(sa.func.count())
                .select_from(TenantUserModel)
                .where(
                    TenantUserModel.tenant_id == tenant_id,
                    TenantUserModel.role == "owner",
                )
            )
            owner_count = count_result.scalar()
            if owner_count <= 1:
                raise CustomException(msg="租户至少需要保留一个拥有者(owner)")

        await auth.db.delete(tu)
        await auth.db.flush()

        log.info(f"从租户[{tenant_id}]移除用户[{user_id}]成功")

    # ============ P1: 配额管理 ============

    @classmethod
    async def get_quota_service(cls, auth: AuthSchema, tenant_id: int) -> dict:
        """获取租户配额"""
        from sqlalchemy import select

        stmt = select(TenantQuotaModel).where(TenantQuotaModel.tenant_id == tenant_id).limit(1)
        result = await auth.db.execute(stmt)
        quota = result.scalar_one_or_none()
        if not quota:
            quota = TenantQuotaModel(tenant_id=tenant_id)
            auth.db.add(quota)
            await auth.db.flush()
        return TenantQuotaOutSchema.model_validate(quota).model_dump()

    @classmethod
    async def update_quota_service(cls, auth: AuthSchema, tenant_id: int, data: TenantQuotaUpdateSchema) -> dict:
        """更新租户配额"""
        from sqlalchemy import select

        stmt = select(TenantQuotaModel).where(TenantQuotaModel.tenant_id == tenant_id).limit(1)
        result = await auth.db.execute(stmt)
        quota = result.scalar_one_or_none()
        if not quota:
            quota = TenantQuotaModel(tenant_id=tenant_id)
            auth.db.add(quota)
            await auth.db.flush()

        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(quota, k, v)
        await auth.db.flush()
        log.info(f"租户[{tenant_id}]配额已更新: {update_data}")
        return TenantQuotaOutSchema.model_validate(quota).model_dump()

    # ============ P1: 租户配置 ============

    @classmethod
    async def get_config_service(cls, auth: AuthSchema, tenant_id: int) -> list[dict]:
        """获取租户所有配置（带 Redis 缓存）"""
        from sqlalchemy import select

        stmt = select(TenantConfigModel).where(TenantConfigModel.tenant_id == tenant_id)
        result = await auth.db.execute(stmt)
        configs = result.scalars().all()
        return [TenantConfigOutSchema.model_validate(c).model_dump() for c in configs]

    @classmethod
    async def get_config_cache_service(cls, redis: Redis, tenant_id: int) -> list[dict]:
        """
        从 Redis 缓存获取租户配置，缓存未命中则从 DB 加载并回写缓存

        参数:
        - redis (Redis): Redis 客户端实例
        - tenant_id (int): 租户ID

        返回:
        - list[dict]: 租户配置列表
        """
        redis_keys = await RedisCURD(redis).get_keys(
            f"{RedisInitKeyConfig.TENANT_CONFIG.key}:{tenant_id}:*"
        )
        redis_configs = await RedisCURD(redis).mget(redis_keys)
        configs = []
        for config in redis_configs:
            if not config:
                continue
            try:
                configs.append(json.loads(config))
            except Exception as e:
                log.error(f"解析租户配置数据失败: {e}")
                continue

        if not configs:
            log.info(f"Redis 中没有租户[{tenant_id}]配置数据，从数据库中加载")
            from app.core.database import async_db_session

            async with async_db_session() as session:
                async with session.begin():
                    from app.api.v1.module_system.auth.schema import AuthSchema

                    auth = AuthSchema(db=session, check_data_scope=False)
                    configs = await cls.get_config_service(auth, tenant_id)
                    await cls._sync_configs_to_redis(redis, tenant_id, configs)
                    log.info(f"✅ 已从数据库加载 {len(configs)} 条租户配置到缓存")

        return configs

    @classmethod
    async def _sync_configs_to_redis(
        cls, redis: Redis, tenant_id: int, configs: list[dict]
    ) -> None:
        """将租户配置列表批量写入 Redis 缓存"""
        for cfg in configs:
            redis_key = (
                f"{RedisInitKeyConfig.TENANT_CONFIG.key}:{tenant_id}:{cfg.get('config_key')}"
            )
            value = json.dumps(cfg, ensure_ascii=False)
            await RedisCURD(redis).set(key=redis_key, value=value, expire=None)

    @classmethod
    async def _del_configs_from_redis(
        cls, redis: Redis, tenant_id: int, keys: list[str]
    ) -> None:
        """删除租户配置的 Redis 缓存"""
        redis_keys = [
            f"{RedisInitKeyConfig.TENANT_CONFIG.key}:{tenant_id}:{k}" for k in keys
        ]
        if redis_keys:
            await RedisCURD(redis).delete(*redis_keys)

    @classmethod
    async def update_config_service(
        cls, auth: AuthSchema, redis: Redis, tenant_id: int, items: list[TenantConfigItem]
    ) -> list[dict]:
        """批量更新租户配置（同步 Redis 缓存）"""
        from sqlalchemy import select

        for item in items:
            stmt = (
                select(TenantConfigModel)
                .where(
                    TenantConfigModel.tenant_id == tenant_id,
                    TenantConfigModel.config_key == item.config_key,
                )
                .limit(1)
            )
            result = await auth.db.execute(stmt)
            cfg = result.scalar_one_or_none()
            if cfg:
                cfg.config_value = item.config_value
                if item.config_type:
                    cfg.config_type = item.config_type
            else:
                cfg = TenantConfigModel(
                    tenant_id=tenant_id,
                    config_key=item.config_key,
                    config_value=item.config_value,
                    config_type=item.config_type or "string",
                )
                auth.db.add(cfg)
        await auth.db.flush()

        # 刷新 DB 数据并同步到 Redis
        configs = await cls.get_config_service(auth, tenant_id)
        await cls._sync_configs_to_redis(redis, tenant_id, configs)
        log.info(f"租户[{tenant_id}]配置已更新, keys={[i.config_key for i in items]}")
        return configs

    # ============ P1: 租户菜单 ============

    @classmethod
    async def get_menus_service(cls, auth: AuthSchema, tenant_id: int) -> list[int]:
        """获取租户菜单权限（返回 menu_id 列表）"""
        from sqlalchemy import select

        stmt = select(TenantMenuModel.menu_id).where(TenantMenuModel.tenant_id == tenant_id)
        result = await auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    @classmethod
    async def set_menus_service(cls, auth: AuthSchema, tenant_id: int, data: TenantMenuSetSchema) -> None:
        """批量设置租户菜单权限（先清空再写入）"""
        from sqlalchemy import delete

        await auth.db.execute(
            delete(TenantMenuModel).where(TenantMenuModel.tenant_id == tenant_id)
        )
        for menu_id in data.menu_ids:
            auth.db.add(TenantMenuModel(tenant_id=tenant_id, menu_id=menu_id))
        await auth.db.flush()
        log.info(f"租户[{tenant_id}]菜单权限已设置, count={len(data.menu_ids)}")

    @staticmethod
    async def get_tenant_menu_ids(auth: AuthSchema, tenant_id: int) -> list[int] | None:
        """获取租户菜单权限ID列表（供角色/用户权限约束使用）"""
        from sqlalchemy import select

        stmt = select(TenantMenuModel.menu_id).where(
            TenantMenuModel.tenant_id == tenant_id,
        )
        result = await auth.db.execute(stmt)
        ids = [row[0] for row in result.all()]
        return ids if ids else None

    # ============ P1: 初始化缓存 ============

    @classmethod
    async def init_tenant_config_cache(cls, redis: Redis) -> None:
        """
        初始化所有租户配置到 Redis 缓存（应用启动时调用）。

        参数:
        - redis (Redis): Redis 客户端实例

        返回:
        - None
        """
        from sqlalchemy import select

        from app.core.database import async_db_session

        async with async_db_session() as session:
            async with session.begin():
                stmt = select(TenantModel)
                result = await session.execute(stmt)
                tenants = result.scalars().all()

                for tenant in tenants:
                    config_stmt = select(TenantConfigModel).where(
                        TenantConfigModel.tenant_id == tenant.id
                    )
                    config_result = await session.execute(config_stmt)
                    configs = config_result.scalars().all()
                    config_list = [
                        TenantConfigOutSchema.model_validate(c).model_dump() for c in configs
                    ]

                    if config_list:
                        await cls._sync_configs_to_redis(redis, tenant.id, config_list)
                        log.info(
                            f"✅ 租户[{tenant.name}](id={tenant.id}) {len(config_list)} 条配置已缓存到 Redis"
                        )
                    else:
                        log.warning(
                            f"⚠️ 租户[{tenant.name}](id={tenant.id}) 无配置数据，跳过缓存"
                        )

    # ============ P1: 到期提醒 ============

    @staticmethod
    async def check_tenant_expiry() -> None:
        """定时任务：检查租户到期并发送通知 / 自动禁用"""
        from datetime import datetime, timedelta

        from app.core.db_session import async_session_factory

        async with async_session_factory() as db:
            now = datetime.now()
            # 扫描所有启用的租户
            stmt = sa.select(TenantModel).where(
                TenantModel.status == "0",
                TenantModel.end_time.isnot(None),
            )
            result = await db.execute(stmt)
            tenants = result.scalars().all()

            for t in tenants:
                if t.end_time <= now:
                    # 已到期：自动禁用
                    await db.execute(
                        sa.update(TenantModel)
                        .where(TenantModel.id == t.id)
                        .values(status="1")
                    )
                    log.info(f"租户[{t.name}]已到期，自动禁用")
                elif t.end_time <= now + timedelta(days=1):
                    TenantService._notify_expiry(t, 1)
                elif t.end_time <= now + timedelta(days=7):
                    TenantService._notify_expiry(t, 7)
                elif t.end_time <= now + timedelta(days=30):
                    TenantService._notify_expiry(t, 30)

            await db.commit()

    @staticmethod
    async def _notify_expiry(tenant: TenantModel, days: int) -> None:
        """发送到期提醒通知"""
        log.info(f"租户[{tenant.name}]将在 {days} 天后到期，联系人: {tenant.contact_email}")
