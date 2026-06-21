
import sqlalchemy as sa
from sqlalchemy import func, select

from app.api.v1.module_platform.tenant.model import TenantModel
from app.core.base_schema import AuthSchema
from app.core.dependencies import require_superadmin
from app.core.exceptions import CustomException
from app.core.logger import logger

from .crud import PackageCRUD
from .model import PackageMenuModel, PackageModel, PackagePluginModel
from .schema import (
    PackageCreateSchema,
    PackageMenuSetSchema,
    PackageOutSchema,
    PackagePluginSetSchema,
    PackageQueryParam,
    PackageUpdateSchema,
)


class PackageService:
    """套餐管理服务（仅超级管理员可操作）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @require_superadmin
    async def detail(self, id: int) -> PackageOutSchema:
        return await PackageCRUD(self.auth).get_or_404(id=id, out_schema=PackageOutSchema, msg="该数据不存在")

    @require_superadmin
    async def page(
        self,
        page_no: int,
        page_size: int,
        search: PackageQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        return await PackageCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"sort": "asc"}, {"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=PackageOutSchema,
        )

    @require_superadmin
    async def create(self, data: PackageCreateSchema) -> PackageOutSchema:
        if await PackageCRUD(self.auth).get(name=data.name):
            raise CustomException(msg="创建失败，套餐名称已存在")
        if await PackageCRUD(self.auth).get(code=data.code):
            raise CustomException(msg="创建失败，套餐编码已存在")

        obj = await PackageCRUD(self.auth).create(data=data)
        result = PackageOutSchema.model_validate(obj)
        logger.info(f"创建套餐成功: {result.name}")
        return result

    @require_superadmin
    async def update(self, id: int, data: PackageUpdateSchema) -> PackageOutSchema:
        obj = await PackageCRUD(self.auth).get_or_404(id=id)

        if data.name is not None:
            exist = await PackageCRUD(self.auth).get(name=data.name)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，名称重复")
        if data.code is not None:
            exist = await PackageCRUD(self.auth).get(code=data.code)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，编码重复")

        if data.status is not None and data.status == 1 and obj.status == 0:
            await self.disable_cascade(package_id=id)

        updated = await PackageCRUD(self.auth).update(id=id, data=data)
        return PackageOutSchema.model_validate(updated)

    @require_superadmin
    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")

        for pid in ids:
            stmt = select(func.count()).select_from(TenantModel).where(TenantModel.package_id == pid)
            result = await self.auth.db.execute(stmt)
            count = result.scalar()
            if count and count > 0:
                raise CustomException(msg=f"套餐 ID={pid} 已被 {count} 个租户使用，无法删除")

        await PackageCRUD(self.auth).delete(ids=ids)

    async def disable_cascade(self, package_id: int) -> None:
        stmt = select(TenantModel.id, TenantModel.name).where(
            TenantModel.package_id == package_id,
            TenantModel.status == 0,
        )
        result = await self.auth.db.execute(stmt)
        rows = result.all()
        if rows:
            tenant_ids = [row[0] for row in rows]
            logger.warning(f"套餐[{package_id}]已禁用，影响租户: {tenant_ids}")

    async def get_menus(self, package_id: int) -> list[int]:
        stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == package_id)
        result = await self.auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    async def set_menus(self, package_id: int, data: PackageMenuSetSchema) -> None:
        await self.auth.db.execute(sa.delete(PackageMenuModel).where(PackageMenuModel.package_id == package_id))
        for menu_id in data.menu_ids:
            self.auth.db.add(PackageMenuModel(package_id=package_id, menu_id=menu_id))
        await self.auth.db.flush()
        logger.info(f"套餐[{package_id}]菜单权限已设置, count={len(data.menu_ids)}")

    async def get_package_menu_ids(self, package_id: int) -> list[int]:
        stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == package_id)
        result = await self.auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_tenant_available_menu_ids(self, tenant_id: int) -> list[int]:
        from app.api.v1.module_platform.menu.model import MenuModel
        from app.api.v1.module_platform.tenant.model import TenantModel

        if tenant_id == 1:
            menu_stmt = select(MenuModel.id).where(MenuModel.status == 0)
            result = await self.auth.db.execute(menu_stmt)
            return [row[0] for row in result.all()]

        stmt = select(TenantModel).where(TenantModel.id == tenant_id).limit(1)
        result = await self.auth.db.execute(stmt)
        tenant = result.scalar_one_or_none()
        if not tenant:
            return []

        if not tenant.package_id:
            return []

        pkg_stmt = select(PackageModel.status).where(PackageModel.id == tenant.package_id).limit(1)
        pkg_result = await self.auth.db.execute(pkg_stmt)
        pkg_status = pkg_result.scalar_one_or_none()
        if pkg_status != 0:
            return []

        menu_stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == tenant.package_id)
        result = await self.auth.db.execute(menu_stmt)
        return [row[0] for row in result.all()]

    async def get_tenant_available_plugin_ids(self, tenant_id: int) -> list[int]:
        from app.api.v1.module_platform.tenant.model import TenantModel

        stmt = select(TenantModel).where(TenantModel.id == tenant_id).limit(1)
        result = await self.auth.db.execute(stmt)
        tenant = result.scalar_one_or_none()
        if not tenant or not tenant.package_id:
            return []

        pkg_stmt = select(PackageModel.status).where(PackageModel.id == tenant.package_id).limit(1)
        pkg_result = await self.auth.db.execute(pkg_stmt)
        pkg_status = pkg_result.scalar_one_or_none()
        if pkg_status != 0:
            return []

        plugin_stmt = select(PackagePluginModel.plugin_id).where(PackagePluginModel.plugin_id == tenant.package_id)
        result = await self.auth.db.execute(plugin_stmt)
        return [row[0] for row in result.all()]

    async def get_plugins(self, package_id: int) -> list[int]:
        stmt = select(PackagePluginModel.plugin_id).where(PackagePluginModel.plugin_id == package_id)
        result = await self.auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    async def set_plugins(self, package_id: int, data: PackagePluginSetSchema) -> None:
        await self.auth.db.execute(sa.delete(PackagePluginModel).where(PackagePluginModel.package_id == package_id))
        for plugin_id in data.plugin_ids:
            self.auth.db.add(PackagePluginModel(package_id=package_id, plugin_id=plugin_id))
        await self.auth.db.flush()
