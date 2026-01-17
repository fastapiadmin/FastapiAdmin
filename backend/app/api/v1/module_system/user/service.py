import io
from typing import Any

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.api.v1.module_system.menu.schema import MenuOutSchema
from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.role.crud import RoleCRUD
from app.core.base_schema import BatchSetAvailable, UploadResponseSchema
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.common_util import traversal_to_tree
from app.utils.excel_util import ExcelUtil
from app.utils.hash_bcrpy_util import PwdUtil
from app.utils.upload_util import UploadUtil

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
    """用户模块服务层"""

    @classmethod
    async def get_detail_by_id_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        根据ID获取用户详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 用户ID

        返回:
        - dict: 用户详情字典
        """
        user = await UserCRUD(auth).get_by_id_crud(id=id)
        if not user:
            raise CustomException(msg="用户不存在")

        # 如果用户绑定了部门,则获取部门名称
        if user.dept_id:
            dept = await DeptCRUD(auth).get_by_id_crud(id=user.dept_id)
            UserOutSchema.dept_name = dept.name if dept else None
        else:
            UserOutSchema.dept_name = None

        return UserOutSchema.model_validate(user).model_dump()

    @classmethod
    async def get_user_list_service(
        cls,
        auth: AuthSchema,
        search: UserQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取用户列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (UserQueryParam | None): 查询参数对象。
        - order_by (list[dict[str, str]] | None): 排序参数列表。

        返回:
        - list[dict]: 用户详情字典列表
        """
        user_list = await UserCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        user_dict_list = []
        for user in user_list:
            user_dict = UserOutSchema.model_validate(user).model_dump()
            user_dict_list.append(user_dict)

        return user_dict_list

    @classmethod
    async def create_user_service(cls, data: UserCreateSchema, auth: AuthSchema) -> dict:
        """
        创建用户

        参数:
        - data (UserCreateSchema): 用户创建信息
        - auth (AuthSchema): 认证信息模型

        返回:
        - dict: 创建后的用户详情字典
        """
        if not data.username:
            raise CustomException(msg="用户名不能为空")
        # 检查是否试图创建超级管理员
        if data.is_superuser:
            raise CustomException(msg="不允许创建超级管理员")
        # 检查用户名是否存在
        user = await UserCRUD(auth).get_by_username_crud(username=data.username)
        if user:
            raise CustomException(msg="已存在相同用户名称的账号")

        # 检查部门是否存在
        if data.dept_id:
            dept = await DeptCRUD(auth).get_by_id_crud(id=data.dept_id)
            if not dept:
                raise CustomException(msg="部门不存在")
        # 创建用户
        if data.password:
            data.password = PwdUtil.set_password_hash(password=data.password)
        user_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        # 创建用户
        new_user = await UserCRUD(auth).create(data=user_dict)
        # 设置角色
        if data.role_ids and len(data.role_ids) > 0:
            await UserCRUD(auth).set_user_roles_crud(user_ids=[new_user.id], role_ids=data.role_ids)
        # 设置岗位
        if data.position_ids and len(data.position_ids) > 0:
            await UserCRUD(auth).set_user_positions_crud(
                user_ids=[new_user.id], position_ids=data.position_ids
            )

        new_user_dict = UserOutSchema.model_validate(new_user).model_dump()
        return new_user_dict

    @classmethod
    async def update_user_service(cls, id: int, data: UserUpdateSchema, auth: AuthSchema) -> dict:
        """
        更新用户

        参数:
        - id (int): 用户ID
        - data (UserUpdateSchema): 用户更新信息
        - auth (AuthSchema): 认证信息模型

        返回:
        - Dict: 更新后的用户详情字典
        """
        if not data.username:
            raise CustomException(msg="账号不能为空")

        # 检查用户是否存在
        user = await UserCRUD(auth).get_by_id_crud(id=id)
        if not user:
            raise CustomException(msg="用户不存在")

        # 检查是否尝试修改超级管理员
        if user.is_superuser:
            raise CustomException(msg="超级管理员不允许修改")

        # 检查用户名是否重复
        exist_user = await UserCRUD(auth).get_by_username_crud(username=data.username)
        if exist_user and exist_user.id != id:
            raise CustomException(msg="已存在相同的账号")
        # 新增：检查手机号是否重复
        if data.mobile:
            exist_mobile_user = await UserCRUD(auth).get_by_mobile_crud(mobile=data.mobile)
            if exist_mobile_user and exist_mobile_user.id != id:
                raise CustomException(msg="更新失败，手机号已存在")
        # 新增：检查邮箱是否重复
        if data.email:
            exist_email_user = await UserCRUD(auth).get(email=data.email)
            if exist_email_user and exist_email_user.id != id:
                raise CustomException(msg="更新失败，邮箱已存在")
        # 检查部门是否存在且可用
        if data.dept_id:
            dept = await DeptCRUD(auth).get_by_id_crud(id=data.dept_id)
            if not dept:
                raise CustomException(msg="部门不存在")
            if dept.status == "1":
                raise CustomException(msg="部门已被禁用")

        # 更新用户 - 排除不应被修改的字段, 更新不更新密码
        user_dict = data.model_dump(
            exclude_unset=True,
            exclude={"role_ids", "position_ids", "last_login", "password"},
        )
        new_user = await UserCRUD(auth).update(id=id, data=user_dict)

        # 更新角色和岗位
        if data.role_ids and len(data.role_ids) > 0:
            # 检查角色是否都存在且可用
            roles = await RoleCRUD(auth).get_list_crud(search={"id": ("in", data.role_ids)})
            if len(roles) != len(data.role_ids):
                raise CustomException(msg="部分角色不存在")
            if not all(role.status for role in roles):
                raise CustomException(msg="部分角色已被禁用")
            await UserCRUD(auth).set_user_roles_crud(user_ids=[id], role_ids=data.role_ids)

        if data.position_ids and len(data.position_ids) > 0:
            # 检查岗位是否都存在且可用
            positions = await PositionCRUD(auth).get_list_crud(
                search={"id": ("in", data.position_ids)}
            )
            if len(positions) != len(data.position_ids):
                raise CustomException(msg="部分岗位不存在")
            if not all(position.status for position in positions):
                raise CustomException(msg="部分岗位已被禁用")
            await UserCRUD(auth).set_user_positions_crud(
                user_ids=[id], position_ids=data.position_ids
            )

        user_dict = UserOutSchema.model_validate(new_user).model_dump()
        return user_dict

    @classmethod
    async def delete_user_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除用户

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 用户ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            user = await UserCRUD(auth).get_by_id_crud(id=id)
            if not user:
                raise CustomException(msg="用户不存在")
            if user.is_superuser:
                raise CustomException(msg="超级管理员不能删除")
            if user.status == "0":
                raise CustomException(msg="用户已启用,不能删除")
            if auth.user and auth.user.id == id:
                raise CustomException(msg="不能删除当前登陆用户")
        # 删除用户角色关联数据
        await UserCRUD(auth).set_user_roles_crud(user_ids=ids, role_ids=[])

        # 删除用户岗位关联数据
        await UserCRUD(auth).set_user_positions_crud(user_ids=ids, position_ids=[])

        # 删除用户
        await UserCRUD(auth).delete(ids=ids)

    @classmethod
    async def get_current_user_info_service(cls, auth: AuthSchema) -> dict:
        """
        获取当前用户信息

        参数:
        - auth (AuthSchema): 认证信息模型

        返回:
        - Dict: 当前用户详情字典
        """
        # 获取用户基本信息
        if not auth.user or not auth.user.id:
            raise CustomException(msg="用户不存在")
        user = await UserCRUD(auth).get_by_id_crud(id=auth.user.id)
        # 获取部门名称
        if user and user.dept:
            UserOutSchema.dept_name = user.dept.name
        user_dict = UserOutSchema.model_validate(user).model_dump()

        # 获取菜单权限
        if auth.user and auth.user.is_superuser:
            # 使用树形结构查询，预加载children关系
            menu_all = await MenuCRUD(auth).get_tree_list_crud(
                search={"type": ("in", [1, 2, 4]), "status": "0"},
                order_by=[{"order": "asc"}],
            )
            menus = [MenuOutSchema.model_validate(menu).model_dump() for menu in menu_all]

        else:
            # 收集用户所有角色的菜单ID，使用列表推导式优化代码
            menu_ids = {
                menu.id
                for role in auth.user.roles or []
                for menu in role.menus
                if menu.status == "0" and menu.type in [1, 2, 4]
            }

            # 使用树形结构查询，预加载children关系
            menus = (
                [
                    MenuOutSchema.model_validate(menu).model_dump()
                    for menu in await MenuCRUD(auth).get_tree_list_crud(
                        search={"id": ("in", list(menu_ids))},
                        order_by=[{"order": "asc"}],
                    )
                ]
                if menu_ids
                else []
            )
        user_dict["menus"] = traversal_to_tree(menus)
        return user_dict

    @classmethod
    async def update_current_user_info_service(
        cls, auth: AuthSchema, data: CurrentUserUpdateSchema
    ) -> dict:
        """
        更新当前用户信息

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (CurrentUserUpdateSchema): 当前用户更新信息

        返回:
        - Dict: 更新后的当前用户详情字典
        """
        if not auth.user or not auth.user.id:
            raise CustomException(msg="用户不存在")
        user = await UserCRUD(auth).get_by_id_crud(id=auth.user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        if user.is_superuser:
            raise CustomException(msg="超级管理员不能修改个人信息")
        # 新增：检查手机号是否重复
        if data.mobile:
            exist_mobile_user = await UserCRUD(auth).get_by_mobile_crud(mobile=data.mobile)
            if exist_mobile_user and exist_mobile_user.id != auth.user.id:
                raise CustomException(msg="更新失败，手机号已存在")
        # 新增：检查邮箱是否重复
        if data.email:
            exist_email_user = await UserCRUD(auth).get(email=data.email)
            if exist_email_user and exist_email_user.id != auth.user.id:
                raise CustomException(msg="更新失败，邮箱已存在")
        user_update_data = UserUpdateSchema(**data.model_dump())
        new_user = await UserCRUD(auth).update(id=auth.user.id, data=user_update_data)
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def set_user_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        设置用户状态

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置用户状态数据

        返回:
        - None
        """
        for id in data.ids:
            user = await UserCRUD(auth).get_by_id_crud(id=id)
            if not user:
                raise CustomException(msg=f"用户ID {id} 不存在")
            if user.is_superuser:
                raise CustomException(msg="超级管理员状态不能修改")
        await UserCRUD(auth).set_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def upload_avatar_service(cls, base_url: str, file: UploadFile) -> dict:
        """
        上传用户头像

        参数:
        - base_url (str): 基础URL
        - file (UploadFile): 上传的文件

        返回:
        - Dict: 上传头像响应字典
        """
        filename, filepath, file_url = await UploadUtil.upload_file(file=file, base_url=base_url)

        return UploadResponseSchema(
            file_path=f"{filepath}",
            file_name=filename,
            origin_name=file.filename,
            file_url=f"{file_url}",
        ).model_dump()

    @classmethod
    async def change_user_password_service(
        cls, auth: AuthSchema, data: UserChangePasswordSchema
    ) -> dict:
        """
        修改用户密码

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (UserChangePasswordSchema): 用户密码修改数据

        返回:
        - Dict: 更新后的当前用户详情字典
        """
        if not auth.user or not auth.user.id:
            raise CustomException(msg="用户不存在")
        if not data.old_password or not data.new_password:
            raise CustomException(msg="密码不能为空")

        # 验证原密码
        user = await UserCRUD(auth).get_by_id_crud(id=auth.user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        if not PwdUtil.verify_password(
            plain_password=data.old_password, password_hash=user.password
        ):
            raise CustomException(msg="原密码输入错误")

        # 更新密码
        new_password_hash = PwdUtil.set_password_hash(password=data.new_password)
        new_user = await UserCRUD(auth).change_password_crud(
            id=user.id, password_hash=new_password_hash
        )
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def reset_user_password_service(cls, auth: AuthSchema, data: ResetPasswordSchema) -> dict:
        """
        重置用户密码

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (ResetPasswordSchema): 用户密码重置数据

        返回:
        - Dict: 更新后的当前用户详情字典
        """
        if not data.password:
            raise CustomException(msg="密码不能为空")

        # 验证用户
        user = await UserCRUD(auth).get_by_id_crud(id=data.id)
        if not user:
            raise CustomException(msg="用户不存在")

        # 检查是否是超级管理员
        if user.is_superuser:
            raise CustomException(msg="超级管理员密码不能重置")

        # 更新密码
        new_password_hash = PwdUtil.set_password_hash(password=data.password)
        new_user = await UserCRUD(auth).change_password_crud(
            id=data.id, password_hash=new_password_hash
        )
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def register_user_service(cls, auth: AuthSchema, data: UserRegisterSchema) -> dict:
        """
        用户注册

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (UserRegisterSchema): 用户注册数据

        返回:
        - Dict: 注册后的用户详情字典
        """
        # 检查用户名是否存在
        username_ok = await UserCRUD(auth).get_by_username_crud(username=data.username)
        if username_ok:
            raise CustomException(msg="账号已存在")

        data.password = PwdUtil.set_password_hash(password=data.password)
        data.name = data.username
        create_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})

        # 设置创建人ID
        if auth.user and auth.user.id:
            create_dict["created_id"] = auth.user.id

        result = await UserCRUD(auth).create(data=create_dict)
        if data.role_ids:
            await UserCRUD(auth).set_user_roles_crud(user_ids=[result.id], role_ids=data.role_ids)
        return UserOutSchema.model_validate(result).model_dump()

    @classmethod
    async def forget_password_service(
        cls, auth: AuthSchema, data: UserForgetPasswordSchema
    ) -> dict:
        """
        用户忘记密码

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (UserForgetPasswordSchema): 用户忘记密码数据

        返回:
        - Dict: 更新后的当前用户详情字典
        """
        user = await UserCRUD(auth).get_by_username_crud(username=data.username)
        if not user:
            raise CustomException(msg="用户不存在")
        if user.status == "1":
            raise CustomException(msg="用户已停用")

        # 检查是否是超级管理员
        if user.is_superuser:
            raise CustomException(msg="超级管理员密码不能重置")

        new_password_hash = PwdUtil.set_password_hash(password=data.new_password)
        new_user = await UserCRUD(auth).forget_password_crud(
            id=user.id, password_hash=new_password_hash
        )
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def batch_import_user_service(
        cls, auth: AuthSchema, file: UploadFile, update_support: bool = False
    ) -> str:
        """
        批量导入用户

        参数:
        - auth (AuthSchema): 认证信息模型
        - file (UploadFile): 上传的Excel文件
        - update_support (bool, optional): 是否支持更新已存在用户. 默认值为False.

        返回:
        - str: 导入结果消息
        """

        header_dict = {
            "部门编号": "dept_id",
            "用户名": "username",
            "名称": "name",
            "邮箱": "email",
            "手机号": "mobile",
            "性别": "gender",
            "状态": "status",
        }

        try:
            # 读取Excel文件
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()

            if df.empty:
                raise CustomException(msg="导入文件为空")

            # 检查表头是否完整
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")

            # 重命名列名
            df.rename(columns=header_dict, inplace=True)

            # 验证必填字段
            required_fields = ["username", "name", "dept_id"]
            errors = []
            for field in required_fields:
                missing_rows = df[df[field].isnull()].index.tolist()
                if missing_rows:
                    field_name = next(k for k, v in header_dict.items() if v == field)
                    rows_str = "、".join([str(i + 1) for i in missing_rows])
                    errors.append(f"{field_name}不能为空，第{rows_str}行")

            if errors:
                raise CustomException(msg="；".join(errors))

            error_msgs = []
            success_count = 0
            count = 0

            # 处理每一行数据
            for _index, row in df.iterrows():
                try:
                    count = count + 1
                    # 数据转换
                    gender = 1 if row["gender"] == "男" else (2 if row["gender"] == "女" else 1)
                    status = "0" if row["status"] == "正常" else "1"

                    # 构建用户数据
                    user_data = {
                        "username": str(row["username"]).strip(),
                        "name": str(row["name"]).strip(),
                        "email": str(row["email"]).strip(),
                        "mobile": str(row["mobile"]).strip(),
                        "gender": gender,
                        "status": status,
                        "dept_id": int(row["dept_id"]),
                        "password": PwdUtil.set_password_hash(password="123456"),  # 设置默认密码
                    }

                    # 处理用户导入
                    exists_user = await UserCRUD(auth).get_by_username_crud(
                        username=user_data["username"]
                    )
                    if exists_user:
                        # 检查是否是超级管理员
                        if exists_user.is_superuser:
                            error_msgs.append(f"第{count}行: 超级管理员不允许修改")
                            continue
                        if update_support:
                            user_update_data = UserUpdateSchema(**user_data)
                            await UserCRUD(auth).update(id=exists_user.id, data=user_update_data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{count}行: 用户 {user_data['username']} 已存在")
                    else:
                        user_create_data = UserCreateSchema(**user_data)
                        await UserCRUD(auth).create(data=user_create_data)
                        success_count += 1

                except Exception as e:
                    error_msgs.append(f"第{count}行: 异常{e!s}")
                    continue

            # 返回详细的导入结果
            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result

        except Exception as e:
            log.error(f"批量导入用户失败: {e!s}")
            raise CustomException(msg=f"导入失败: {e!s}")

    @classmethod
    async def get_import_template_user_service(cls) -> bytes:
        """
        获取用户导入模板

        返回:
        - bytes: Excel文件字节流
        """
        header_list = [
            "部门编号",
            "用户名",
            "名称",
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

    @classmethod
    async def export_user_list_service(cls, user_list: list[dict[str, Any]]) -> bytes:
        """
        导出用户列表为Excel文件

        参数:
        - user_list (List[Dict[str, Any]]): 用户列表

        返回:
        - bytes: Excel文件字节流
        """
        if not user_list:
            raise CustomException(msg="没有数据可导出")

        # 定义字段映射
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

        # 复制数据并转换
        # creator = {'id': 1, 'name': '管理员', 'username': 'admin'}
        data = user_list.copy()
        for item in data:
            item["status"] = "启用" if item.get("status") == "0" else "停用"
            gender = item.get("gender")
            item["gender"] = "男" if gender == "1" else ("女" if gender == "2" else "未知")
            item["is_superuser"] = "是" if item.get("is_superuser") else "否"
            item["creator"] = (
                item.get("creator", {}).get("name", "未知")
                if isinstance(item.get("creator"), dict)
                else "未知"
            )

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
