from datetime import datetime

import sqlalchemy as sa

from app.core.base_schema import AuthSchema
from app.core.dependencies import require_superadmin
from app.core.exceptions import CustomException
from app.core.logger import logger

from .crud import PluginCRUD
from .model import PluginModel, TenantPluginModel
from .schema import PluginCreateSchema, PluginOutSchema, PluginQueryParam, PluginUpdateSchema


class PluginService:
    """插件管理服务（仅超级管理员可操作 CRUD，租户通过 marketplace/install/uninstall/toggle/my 操作）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @require_superadmin
    async def page(
        self,
        page_no: int,
        page_size: int,
        search: PluginQueryParam | None = None,
        order_by: list | None = None,
    ) -> dict:
        return await PluginCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"sort": "asc"}],
            search=vars(search) if search else None,
            out_schema=PluginOutSchema,
        )

    @require_superadmin
    async def detail(self, id: int) -> PluginOutSchema:
        return await PluginCRUD(self.auth).get_or_404(id=id, out_schema=PluginOutSchema)

    @require_superadmin
    async def create(self, data: PluginCreateSchema) -> PluginOutSchema:
        if await PluginCRUD(self.auth).get(code=data.code):
            raise CustomException(msg="创建失败，插件编码已存在")
        obj = await PluginCRUD(self.auth).create(data=data)
        return PluginOutSchema.model_validate(obj)

    @require_superadmin
    async def update(self, id: int, data: PluginUpdateSchema) -> PluginOutSchema:
        _ = await PluginCRUD(self.auth).get_or_404(id=id)
        updated = await PluginCRUD(self.auth).update(id=id, data=data)
        return PluginOutSchema.model_validate(updated)

    @require_superadmin
    async def delete(self, ids: list[int]) -> None:
        await PluginCRUD(self.auth).delete(ids=ids)

    async def marketplace(self, page_no: int, page_size: int, category: str | None = None) -> dict:
        search: dict = {"status": ("eq", "0")}
        if category:
            search["category"] = ("eq", category)
        result = await PluginCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=[{"sort": "asc"}],
            search=search,
            out_schema=PluginOutSchema,
        )
        tenant_id = getattr(self.auth, "tenant_id", None) or self.auth.user.tenant_id
        if tenant_id and result.items:
            records = await self.auth.db.execute(
                sa.select(TenantPluginModel.plugin_id, TenantPluginModel.purchased).where(
                    TenantPluginModel.tenant_id == tenant_id,
                )
            )
            record_map = {r[0]: r[1] for r in records.all()}
            for item in result.items:
                pid = item["id"]
                item["installed"] = pid in record_map
                item["purchased"] = record_map.get(pid, False)
        return result

    async def install(self, plugin_id: int) -> None:
        tenant_id = getattr(self.auth, "tenant_id", None) or self.auth.user.tenant_id
        if not tenant_id:
            raise CustomException(msg="无法获取租户信息")

        if tenant_id != 1:
            from app.api.v1.module_platform.package.service import PackageService

            allowed_plugin_ids = await PackageService(self.auth).get_tenant_available_plugin_ids(tenant_id)
            if allowed_plugin_ids and plugin_id not in allowed_plugin_ids:
                raise CustomException(msg="当前套餐不支持安装此插件")

        plugin = await PluginCRUD(self.auth).get(id=plugin_id)
        if not plugin or plugin.status == 1:
            raise CustomException(msg="该数据不存在")

        if tenant_id != 1 and getattr(plugin, "price", 0) > 0:
            exist = await self.auth.db.execute(
                sa.select(TenantPluginModel)
                .where(
                    TenantPluginModel.tenant_id == tenant_id,
                    TenantPluginModel.plugin_id == plugin_id,
                )
                .limit(1)
            )
            tp_record = exist.scalar_one_or_none()
            if not tp_record or not tp_record.purchased:
                raise CustomException(msg="此插件为付费插件，请先购买后再安装")

        exist = await self.auth.db.execute(
            sa.select(TenantPluginModel)
            .where(
                TenantPluginModel.tenant_id == tenant_id,
                TenantPluginModel.plugin_id == plugin_id,
            )
            .limit(1)
        )
        if exist.scalar_one_or_none():
            await self.auth.db.execute(
                sa.update(TenantPluginModel)
                .where(
                    TenantPluginModel.tenant_id == tenant_id,
                    TenantPluginModel.plugin_id == plugin_id,
                )
                .values(enabled=False)
            )
        else:
            tp = TenantPluginModel(
                tenant_id=tenant_id,
                plugin_id=plugin_id,
                enabled=False,
                purchased=True if getattr(plugin, "price", 0) == 0 else False,
                installed_time=datetime.now(),
            )
            self.auth.db.add(tp)
        await self.auth.db.flush()
        logger.info(f"租户[{tenant_id}]安装插件[{plugin.name}]")

    async def uninstall(self, plugin_id: int) -> None:
        tenant_id = getattr(self.auth, "tenant_id", None) or self.auth.user.tenant_id
        if not tenant_id:
            raise CustomException(msg="无法获取租户信息")
        await self.auth.db.execute(
            sa.delete(TenantPluginModel).where(
                TenantPluginModel.tenant_id == tenant_id,
                TenantPluginModel.plugin_id == plugin_id,
            )
        )
        await self.auth.db.flush()
        logger.info(f"租户[{tenant_id}]卸载插件[{plugin_id}]")

    async def toggle(self, plugin_id: int) -> None:
        tenant_id = getattr(self.auth, "tenant_id", None) or self.auth.user.tenant_id
        tp = await self.auth.db.execute(
            sa.select(TenantPluginModel)
            .where(
                TenantPluginModel.tenant_id == tenant_id,
                TenantPluginModel.plugin_id == plugin_id,
            )
            .limit(1)
        )
        tp = tp.scalar_one_or_none()
        if not tp:
            raise CustomException(msg="未安装该插件")
        tp.enabled = not tp.enabled
        await self.auth.db.flush()
        logger.info(f"租户[{tenant_id}]插件[{plugin_id}]状态→{tp.enabled}")

    async def my_plugins(self) -> list[dict]:
        tenant_id = getattr(self.auth, "tenant_id", None) or self.auth.user.tenant_id
        if not tenant_id:
            return []
        result = await self.auth.db.execute(
            sa.select(PluginModel, TenantPluginModel).join(TenantPluginModel, TenantPluginModel.plugin_id == PluginModel.id).where(TenantPluginModel.tenant_id == tenant_id).order_by(PluginModel.sort)
        )
        plugins = []
        for p, tp in result.all():
            d = PluginOutSchema.model_validate(p)
            d["enabled"] = tp.enabled
            d["installed"] = True
            d["installed_time"] = tp.installed_time.strftime("%Y-%m-%d %H:%M") if tp.installed_time else ""
            plugins.append(d)
        return plugins

    @staticmethod
    def reload() -> str:
        from app.core.discover import reload_dynamic_router

        router = reload_dynamic_router()
        route_count = len(router.routes) if router and hasattr(router, "routes") else 0
        logger.info(f"插件热重载完成，动态路由共 {route_count} 条")
        return f"插件路由热重载完成，共注册 {route_count} 条路由"
