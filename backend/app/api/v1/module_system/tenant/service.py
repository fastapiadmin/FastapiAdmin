import random
import string

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.role.crud import RoleCRUD
from app.api.v1.module_system.user.crud import UserCRUD
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.hash_bcrpy_util import PwdUtil

from .crud import TenantCRUD
from .schema import TenantCreateSchema, TenantOutSchema, TenantQueryParam, TenantUpdateSchema


class TenantService:
    """租户管理模块服务层"""

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await TenantCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="租户不存在")
        return TenantOutSchema.model_validate(obj).model_dump()

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
        except CustomException:
            raise
        except Exception as e:
            log.error(f"为租户[{tenant_obj.name}]创建初始管理员失败: {e!s}")
            raise CustomException(msg="创建租户初始管理员失败")

        log.info(
            f"为租户[{tenant_obj.name}]创建初始管理员成功，用户名: {username}，临时密码: {password}"
        )

        await auth.db.refresh(tenant_obj)
        return TenantOutSchema.model_validate(tenant_obj).model_dump()

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
        return TenantOutSchema.model_validate(updated).model_dump()

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
