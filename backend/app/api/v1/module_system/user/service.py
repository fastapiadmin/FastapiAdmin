import io
from typing import Any

from fastapi import UploadFile

from app.api.v1.module_platform.menu.crud import MenuCRUD
from app.api.v1.module_platform.menu.schema import MenuOutSchema
from app.api.v1.module_platform.package.service import PackageService
from app.api.v1.module_platform.tenant.service import TenantService
from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.role.crud import RoleCRUD
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.utils.common_util import traversal_to_tree
from app.utils.excel_util import ExcelUtil
from app.utils.hash_bcrpy_util import PwdUtil

from .crud import UserCRUD
from .schema import (
    CurrentUserUpdateSchema,
    ResetPasswordSchema,
    UserChangePasswordSchema,
    UserCreateSchema,
    UserForgetPasswordSchema,
    UserOutSchema,
    UserQueryParam,
    UserRegisterSchema,
    UserUpdateSchema,
)


class UserService:
    """用户管理服务"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> UserOutSchema:
        user = await UserCRUD(self.auth).get_or_404(id=id)
        result = UserOutSchema.model_validate(user)
        if user.dept_id:
            dept = await DeptCRUD(self.auth).get(id=user.dept_id)
            result.dept_name = dept.name if dept else None
        return result

    async def get_list(
        self,
        search: UserQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[UserOutSchema]:
        user_list = await UserCRUD(self.auth).get_list(search=vars(search) if search else None, order_by=order_by)
        return [UserOutSchema.model_validate(user) for user in user_list]

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: UserQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        return await UserCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=UserOutSchema,
        )

    async def create(self, data: UserCreateSchema) -> UserOutSchema:
        if not data.username:
            raise CustomException(msg="用户名不能为空")
        if data.is_superuser:
            raise CustomException(msg="不允许创建超级管理员")
        user = await UserCRUD(self.auth).get(username=data.username)
        if user:
            raise CustomException(msg="已存在相同用户名称的账号")

        if data.dept_id:
            dept = await DeptCRUD(self.auth).get(id=data.dept_id)
            if not dept:
                raise CustomException(msg="该数据不存在")

        await TenantService(self.auth).check_quota(self.auth.tenant_id, "user")

        if data.password:
            data.password = PwdUtil.hash_password(password=data.password)
        user_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        new_user = await UserCRUD(self.auth).create(data=user_dict)
        if data.role_ids and len(data.role_ids) > 0:
            await UserCRUD(self.auth).set_user_roles(user_ids=[new_user.id], role_ids=data.role_ids)
        if data.position_ids and len(data.position_ids) > 0:
            await UserCRUD(self.auth).set_user_positions(user_ids=[new_user.id], position_ids=data.position_ids)
        return UserOutSchema.model_validate(new_user)

    async def update(self, id: int, data: UserUpdateSchema) -> UserOutSchema:
        if not data.username:
            raise CustomException(msg="账号不能为空")

        user = await UserCRUD(self.auth).get_or_404(id=id)
        if user.is_superuser:
            raise CustomException(msg="超级管理员不允许修改")

        exist_user = await UserCRUD(self.auth).get(username=data.username)
        if exist_user and exist_user.id != id:
            raise CustomException(msg="更新失败，账号已存在")
        if data.mobile:
            exist_mobile_user = await UserCRUD(self.auth).get(mobile=data.mobile)
            if exist_mobile_user and exist_mobile_user.id != id:
                raise CustomException(msg="该数据已存在")
        if data.email:
            exist_email_user = await UserCRUD(self.auth).get(email=data.email)
            if exist_email_user and exist_email_user.id != id:
                raise CustomException(msg="该数据已存在")
        if data.dept_id:
            dept = await DeptCRUD(self.auth).get(id=data.dept_id)
            if not dept:
                raise CustomException(msg="该数据不存在")
            if dept.status == 1:
                raise CustomException(msg="部门已被禁用")

        new_user = await UserCRUD(self.auth).update(id=id, data=data)

        if data.role_ids and len(data.role_ids) > 0:
            roles = await RoleCRUD(self.auth).get_list(search={"id": ("in", data.role_ids)})
            if len(roles) != len(data.role_ids):
                raise CustomException(msg="更新失败，部分角色不存在")
            if not all(role.status == 0 for role in roles):
                raise CustomException(msg="更新失败，部分角色已被禁用")
            await UserCRUD(self.auth).set_user_roles(user_ids=[id], role_ids=data.role_ids)

        if data.position_ids and len(data.position_ids) > 0:
            positions = await PositionCRUD(self.auth).get_list(search={"id": ("in", data.position_ids)})
            if len(positions) != len(data.position_ids):
                raise CustomException(msg="更新失败，部分岗位不存在")
            if not all(position.status == 0 for position in positions):
                raise CustomException(msg="更新失败，部分岗位已被禁用")
            await UserCRUD(self.auth).set_user_positions(user_ids=[id], position_ids=data.position_ids)

        return UserOutSchema.model_validate(new_user)

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        users = await UserCRUD(self.auth).get_list(search={"id": ("in", ids)})
        user_map = {u.id: u for u in users}
        for uid in ids:
            user = user_map.get(uid)
            if not user:
                raise CustomException(msg="该数据不存在")
            if user.is_superuser:
                raise CustomException(msg="超级管理员不能删除")
            if user.status == 0:
                raise CustomException(msg="用户已启用,不能删除")
            if self.auth.user and self.auth.user.id == uid:
                raise CustomException(msg="不能删除当前登陆用户")

        await UserCRUD(self.auth).set_user_roles(user_ids=ids, role_ids=[])
        await UserCRUD(self.auth).set_user_positions(user_ids=ids, position_ids=[])
        await UserCRUD(self.auth).delete(ids=ids)

    async def current_info(self) -> UserOutSchema:
        if not self.auth.user or not self.auth.user.id:
            raise CustomException(msg="该数据不存在")
        user = await UserCRUD(self.auth).get(id=self.auth.user.id)
        user_dict = UserOutSchema.model_validate(user)
        if user and user.dept:
            user_dict.dept_name = user.dept.name

        _pc_only = {"client": "pc"}
        if self.auth.user and self.auth.user.is_superuser:
            menu_all = await MenuCRUD(self.auth).tree_list(
                search={"type": ("in", [1, 2, 3, 4]), "status": 0, **_pc_only},
                order_by=[{"order": "asc"}],
            )
            menus = [MenuOutSchema.model_validate(menu) for menu in menu_all]
        else:
            menu_ids = {menu.id for role in self.auth.user.roles or [] for menu in role.menus if menu.status == 0 and getattr(menu, "client", "pc") == "pc"}

            if menu_ids and self.auth.tenant_id:
                allowed_ids = await PackageService(self.auth).get_tenant_available_menu_ids(self.auth.tenant_id)
                allowed_set = set(allowed_ids)
                menu_ids = menu_ids & allowed_set

            menus = (
                [
                    MenuOutSchema.model_validate(menu)
                    for menu in await MenuCRUD(self.auth).tree_list(
                        search={"id": ("in", list(menu_ids)), **_pc_only},
                        order_by=[{"order": "asc"}],
                    )
                ]
                if menu_ids
                else []
            )
        user_dict.menus = traversal_to_tree([menu.model_dump() for menu in menus])
        return user_dict

    async def update_current_info(self, data: CurrentUserUpdateSchema) -> UserOutSchema:
        if not self.auth.user or not self.auth.user.id:
            raise CustomException(msg="该数据不存在")
        user = await UserCRUD(self.auth).get(id=self.auth.user.id)
        if not user:
            raise CustomException(msg="该数据不存在")
        if user.is_superuser:
            raise CustomException(msg="超级管理员不能修改个人信息")
        if data.mobile:
            exist_mobile_user = await UserCRUD(self.auth).get(mobile=data.mobile)
            if exist_mobile_user and exist_mobile_user.id != self.auth.user.id:
                raise CustomException(msg="该数据已存在")
        if data.email:
            exist_email_user = await UserCRUD(self.auth).get(email=data.email)
            if exist_email_user and exist_email_user.id != self.auth.user.id:
                raise CustomException(msg="该数据已存在")
        user_update_data = UserUpdateSchema(**data.model_dump())
        new_user = await UserCRUD(self.auth).update(id=self.auth.user.id, data=user_update_data)
        return UserOutSchema.model_validate(new_user)

    async def set_available(self, data: BatchSetAvailable) -> None:
        for mid in data.ids:
            user = await UserCRUD(self.auth).get_or_404(id=mid)
            if user.is_superuser:
                raise CustomException(msg="超级管理员状态不能修改")
        await UserCRUD(self.auth).set(ids=data.ids, status=data.status)

    async def change_password(self, data: UserChangePasswordSchema) -> UserOutSchema:
        if not self.auth.user or not self.auth.user.id:
            raise CustomException(msg="该数据不存在")
        if not data.old_password or not data.new_password:
            raise CustomException(msg="密码不能为空")

        user = await UserCRUD(self.auth).get(id=self.auth.user.id)
        if not user:
            raise CustomException(msg="该数据不存在")
        if not PwdUtil.verify_password(plain_password=data.old_password, password_hash=user.password):
            raise CustomException(msg="原密码输入错误")

        new_password_hash = PwdUtil.hash_password(password=data.new_password)
        new_user = await UserCRUD(self.auth).change_password(id=user.id, password_hash=new_password_hash)
        return UserOutSchema.model_validate(new_user)

    async def reset_password(self, data: ResetPasswordSchema) -> UserOutSchema:
        if not data.password:
            raise CustomException(msg="密码不能为空")

        user = await UserCRUD(self.auth).get(id=data.id)
        if not user:
            raise CustomException(msg="该数据不存在")

        if user.is_superuser:
            raise CustomException(msg="超级管理员密码不能重置")

        new_password_hash = PwdUtil.hash_password(password=data.password)
        new_user = await UserCRUD(self.auth).change_password(id=data.id, password_hash=new_password_hash)
        return UserOutSchema.model_validate(new_user)

    async def register(self, data: UserRegisterSchema) -> UserOutSchema:
        username_ok = await UserCRUD(self.auth).get(username=data.username)
        if username_ok:
            raise CustomException(msg="该数据已存在")

        data.password = PwdUtil.hash_password(password=data.password)
        data.name = data.username
        create_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})

        if self.auth.user and self.auth.user.id:
            create_dict["created_id"] = self.auth.user.id

        result = await UserCRUD(self.auth).create(data=create_dict)
        if data.role_ids:
            await UserCRUD(self.auth).set_user_roles(user_ids=[result.id], role_ids=data.role_ids)
        return UserOutSchema.model_validate(result)

    async def forget_password(self, data: UserForgetPasswordSchema) -> UserOutSchema:
        user = await UserCRUD(self.auth).get(username=data.username)
        if not user:
            raise CustomException(msg="该数据不存在")
        if user.status == 1:
            raise CustomException(msg="用户已停用")

        if user.is_superuser:
            raise CustomException(msg="超级管理员密码不能重置")

        if data.mobile and user.mobile != data.mobile:
            raise CustomException(msg="手机号不匹配")

        new_password_hash = PwdUtil.hash_password(password=data.new_password)
        new_user = await UserCRUD(self.auth).forget_password(id=user.id, password_hash=new_password_hash)
        return UserOutSchema.model_validate(new_user)

    async def batch_import(self, file: UploadFile, update_support: bool = False) -> str:
        header_dict = {
            "部门编号": "dept_id",
            "账号": "username",
            "昵称": "name",
            "邮箱": "email",
            "手机号": "mobile",
            "性别": "gender",
            "状态": "status",
        }

        try:
            contents = await file.read()
            rows = ExcelUtil.read_excel_to_dicts(contents)
            await file.close()

            if not rows:
                raise CustomException(msg="导入文件为空")

            missing_headers = [h for h in header_dict if h not in rows[0]]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")

            # 将中文字段名映射为英文字段
            mapped_rows = []
            for row in rows:
                mapped_rows.append({en: row.get(ch) for ch, en in header_dict.items()})

            required_fields = ["username", "name", "dept_id"]
            errors = []
            for field in required_fields:
                missing_count = sum(1 for r in mapped_rows if r.get(field) is None)
                if missing_count:
                    errors.append(f"字段'{field}'有{missing_count}行缺少数据")

            if errors:
                raise CustomException(msg="\n".join(errors))

            success_count = 0
            error_msgs = []

            for i, row in enumerate(mapped_rows, start=2):
                try:
                    username = (str(row["username"]) if row["username"] is not None else "").strip()
                    name = (str(row["name"]) if row["name"] is not None else "").strip()
                    if not username:
                        error_msgs.append(f"第{i}行: 账号不能为空")
                        continue
                    if not name:
                        error_msgs.append(f"第{i}行: 昵称不能为空")
                        continue

                    user_data = {
                        "username": username,
                        "name": name,
                        "email": str(row["email"]).strip() if row.get("email") is not None else None,
                        "mobile": str(row["mobile"]).strip() if row.get("mobile") is not None else None,
                        "gender": str(row["gender"]).strip() if row.get("gender") is not None else "1",
                        "status": 0 if str(row["status"]).strip() == "正常" else 1,
                        "dept_id": int(row["dept_id"]),
                        "password": PwdUtil.hash_password(password="123456"),
                    }

                    exists_user = await UserCRUD(self.auth).get(username=user_data["username"])
                    if exists_user:
                        if exists_user.is_superuser:
                            error_msgs.append(f"第{i}行: 超级管理员不允许修改")
                            continue
                        if update_support:
                            user_update_data = UserUpdateSchema(**user_data)
                            await UserCRUD(self.auth).update(id=exists_user.id, data=user_update_data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{i}行: 用户 {user_data['username']} 已存在")
                    else:
                        user_create_schema = UserCreateSchema(**user_data)
                        user_create_data = user_create_schema.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
                        new_user = await UserCRUD(self.auth).create(data=user_create_data)
                        if user_create_schema.role_ids and len(user_create_schema.role_ids) > 0:
                            await UserCRUD(self.auth).set_user_roles(user_ids=[new_user.id], role_ids=user_create_schema.role_ids)
                        if user_create_schema.position_ids and len(user_create_schema.position_ids) > 0:
                            await UserCRUD(self.auth).set_user_positions(user_ids=[new_user.id], position_ids=user_create_schema.position_ids)
                        success_count += 1

                except Exception as e:
                    error_msgs.append(f"第{i}行: 异常{e!s}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result

        except Exception as e:
            logger.error(f"批量导入用户失败: {e!s}")
            raise CustomException(msg=f"导入失败: {e!s}") from e

    @staticmethod
    def get_import_template() -> bytes:
        header_list = [
            "部门编号",
            "账号",
            "昵称",
            "邮箱",
            "手机号",
            "性别",
            "状态",
        ]
        selector_header_list = ["性别", "状态"]
        option_list = [
            {"性别": ["男", "女", "未知"]},
            {"状态": ["正常", "停用"]},
        ]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list,
        )

    @staticmethod
    def export_list(user_list: list[dict[str, Any]]) -> bytes:
        if not user_list:
            raise CustomException(msg="没有数据可导出")

        mapping_dict = {
            "id": "用户编号",
            "avatar": "头像",
            "username": "用户名称",
            "name": "用户昵称",
            "dept_name": "部门",
            "email": "邮箱",
            "mobile": "手机号",
            "gender": "性别",
            "status": "状态",
            "is_superuser": "是否超级管理员",
            "last_login": "最后登录时间",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "updated_id": "更新者ID",
        }

        data = user_list.copy()
        for item in data:
            item["status"] = "启用" if item.get("status") == 0 else "停用"
            gender = item.get("gender")
            item["gender"] = "男" if gender == "1" else ("女" if gender == "2" else "未知")
            item["is_superuser"] = "是" if item.get("is_superuser") else "否"
            item["creator"] = item.get("created_by", {}).get("name", "未知") if isinstance(item.get("created_by"), dict) else "未知"

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
