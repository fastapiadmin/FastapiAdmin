"""
人员管理 - 服务层
"""

import io
import uuid
from datetime import datetime, timedelta

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil

from .crud import PersonnelCRUD
from .model import PersonnelStatus, PersonnelType
from .schema import (
    PersonnelOutSchema,
    PersonnelQuerySchema,
)


class PersonnelService:
    """
    招生人员管理服务层

    职责：招生人员增删改查、邀请码邀请加入、状态切换(在岗/离岗)、按组查询
    约束：一个用户只能关联一个招生人员记录；邀请码7天过期；离岗时自动记录离开日期
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生人员ID

        返回:
        - dict: 招生人员模型实例字典
        """
        obj = await PersonnelCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该招生人员不存在")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: PersonnelQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (PersonnelQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 招生人员模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await PersonnelCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [PersonnelOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: PersonnelQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (PersonnelQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await PersonnelCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建招生人员

        校验规则：
        - 人员编号(personnel_code)唯一
        - 同一用户(user_id)不可重复关联
        """
        """
        创建招生人员

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的招生人员模型实例字典
        """
        if data.get("personnel_code"):
            existing = await PersonnelCRUD(auth).get_by_personnel_code_crud(data["personnel_code"])
            if existing:
                raise CustomException(msg="人员编号已存在")

        if data.get("user_id"):
            existing = await PersonnelCRUD(auth).get_by_user_id_crud(data["user_id"])
            if existing:
                raise CustomException(msg="该用户已是招生人员")

        obj = await PersonnelCRUD(auth).create_crud(data=data)
        log.info(f"创建招生人员成功: {obj.id}")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新招生人员

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生人员ID
        - data (dict): 更新数据

        返回:
        - dict: 更新的招生人员模型实例字典
        """
        existing = await PersonnelCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生人员不存在")

        if data.get("personnel_code") and data["personnel_code"] != existing.personnel_code:
            code_existing = await PersonnelCRUD(auth).get_by_personnel_code_crud(
                data["personnel_code"]
            )
            if code_existing:
                raise CustomException(msg="人员编号已存在")

        if data.get("user_id") and data["user_id"] != existing.user_id:
            user_existing = await PersonnelCRUD(auth).get_by_user_id_crud(data["user_id"])
            if user_existing:
                raise CustomException(msg="该用户已是招生人员")

        obj = await PersonnelCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新招生人员成功: {id}")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除招生人员

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生人员ID
        """
        existing = await PersonnelCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生人员不存在")

        await PersonnelCRUD(auth).delete_crud(id=id)
        log.info(f"删除招生人员成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除招生人员

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 招生人员ID列表
        """
        await PersonnelCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除招生人员成功: {ids}")

    @classmethod
    async def invite_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        邀请招生人员

        生成12位邀请码，有效期7天，状态设为 invited
        被邀请人通过 /join/{invite_code} 接口完成加入
        """
        # 生成12位随机邀请码
        invite_code = str(uuid.uuid4()).replace("-", "")[:12]
        expire_time = datetime.now() + timedelta(days=7)

        invite_data = {
            "personnel_name": data.get("personnel_name"),
            "personnel_type": PersonnelType.INVITE.value,
            "phone": data.get("phone"),
            "email": data.get("email"),
            "team_id": data.get("team_id"),
            "team_name": data.get("team_name"),
            "province": data.get("province"),
            "city": data.get("city"),
            "position": data.get("position"),
            "status": PersonnelStatus.INVITED.value,
            "invite_code": invite_code,
            "invite_time": datetime.now(),
            "invite_expire_time": expire_time,
        }

        obj = await PersonnelCRUD(auth).create_crud(data=invite_data)
        log.info(f"邀请招生人员成功: {obj.id}")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def join_service(cls, auth: AuthSchema, invite_code: str, user_id: int) -> dict:
        """
        招生人员通过邀请码加入

        校验：邀请码存在 -> 状态为invited -> 未过期 -> 未被使用
        加入后状态变为 active，记录加入日期
        """
        result = await PersonnelCRUD(auth).get(row_key="invite_code", row_value=invite_code)
        if not result:
            raise CustomException(msg="邀请码无效")

        # 以下四种情况均视为无效邀请
        if result.status != PersonnelStatus.INVITED.value:
            raise CustomException(msg="邀请已失效")

        if result.invite_expire_time and result.invite_expire_time < datetime.now():
            raise CustomException(msg="邀请码已过期")

        if result.user_id:
            raise CustomException(msg="该邀请已被使用")

        from datetime import date

        update_data = {
            "user_id": user_id,
            "status": PersonnelStatus.ACTIVE.value,
            "join_date": date.today(),
        }

        obj = await PersonnelCRUD(auth).update_crud(id=result.id, data=update_data)
        log.info(f"招生人员加入成功: {obj.id}")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def set_status_service(cls, auth: AuthSchema, id: int, status: str) -> dict:
        """
        设置招生人员状态

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生人员ID
        - status (str): 状态

        返回:
        - dict: 更新后的招生人员模型实例字典
        """
        existing = await PersonnelCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生人员不存在")

        # 离岗时自动记录离开日期
        update_data = {"status": status}
        if status == PersonnelStatus.INACTIVE.value:
            from datetime import date

            update_data["leave_date"] = date.today()

        obj = await PersonnelCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"设置招生人员状态成功: {id}, status={status}")
        return PersonnelOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_by_team_service(cls, auth: AuthSchema, team_id: int) -> list[dict]:
        """
        获取招生组下所有人员

        参数:
        - auth (AuthSchema): 认证信息模型
        - team_id (int): 招生组ID

        返回:
        - list[dict]: 招生人员列表
        """
        obj_list = await PersonnelCRUD(auth).get_by_team_id_crud(team_id=team_id)
        return [PersonnelOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def batch_import_service(
        cls, auth: AuthSchema, file: UploadFile, update_support: bool = False
    ) -> str:
        """
        批量导入招生人员

        去重规则：name + phone 组合
        """
        header_dict = {
            "人员姓名": "name",
            "手机号": "phone",
            "邮箱": "email",
            "招生组ID": "team_id",
            "角色": "role",
            "省份": "province",
            "城市": "city",
            "负责区域": "responsible_area",
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()

            if df.empty:
                raise CustomException(msg="导入文件为空")

            # 检查表头是否完整
            missing_headers = [h for h in header_dict.keys() if h not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")

            df.rename(columns=header_dict, inplace=True)

            # 验证必填字段
            required_fields = ["name"]
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

            for _index, row in df.iterrows():
                try:
                    count += 1

                    name = str(row["name"]).strip() if pd.notna(row["name"]) else None
                    if not name:
                        error_msgs.append(f"第{count}行: 人员姓名不能为空")
                        continue

                    phone = str(row["phone"]).strip() if pd.notna(row["phone"]) else None
                    email = str(row["email"]).strip() if pd.notna(row["email"]) else None
                    team_id = int(row["team_id"]) if pd.notna(row["team_id"]) else None
                    role = str(row["role"]).strip() if pd.notna(row["role"]) else None
                    province = str(row["province"]).strip() if pd.notna(row["province"]) else None
                    city = str(row["city"]).strip() if pd.notna(row["city"]) else None
                    responsible_area = (
                        str(row["responsible_area"]).strip()
                        if pd.notna(row["responsible_area"])
                        else None
                    )

                    personnel_data = {
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "team_id": team_id,
                        "role": role,
                        "province": province,
                        "city": city,
                        "responsible_area": responsible_area,
                        "status": PersonnelStatus.ACTIVE.value,
                    }

                    # 按 name+phone 去重
                    if phone:
                        existing_list = await PersonnelCRUD(auth).list_crud(
                            search={"name": ("eq", name), "phone": ("eq", phone)}
                        )
                        if existing_list:
                            if update_support:
                                await PersonnelCRUD(auth).update_crud(
                                    id=existing_list[0].id, data=personnel_data
                                )
                                success_count += 1
                            else:
                                error_msgs.append(f"第{count}行: 人员 {name}({phone}) 已存在")
                            continue

                    await PersonnelCRUD(auth).create_crud(data=personnel_data)
                    success_count += 1

                except Exception as e:
                    error_msgs.append(f"第{count}行: 异常{e!s}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result

        except CustomException:
            raise
        except Exception as e:
            log.error(f"批量导入招生人员失败: {e!s}")
            raise CustomException(msg=f"导入失败: {e!s}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """获取招生人员导入模板"""
        header_list = ["人员姓名", "手机号", "邮箱", "招生组ID", "角色", "省份", "城市", "负责区域"]
        selector_header_list = ["角色"]
        option_list = [
            {"角色": ["组长", "副组长", "组员"]},
        ]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list,
        )
