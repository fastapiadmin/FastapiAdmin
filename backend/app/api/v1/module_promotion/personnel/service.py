"""
人员管理 - 服务层
"""
import uuid
from datetime import datetime, timedelta

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import PersonnelCRUD
from .model import PersonnelStatus, PersonnelType
from .schema import (
    PersonnelOutSchema,
    PersonnelQuerySchema,
)


class PersonnelService:
    """
    招生人员管理服务层
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
            code_existing = await PersonnelCRUD(auth).get_by_personnel_code_crud(data["personnel_code"])
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

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 邀请数据

        返回:
        - dict: 邀请信息
        """
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
        招生人员加入

        参数:
        - auth (AuthSchema): 认证信息模型
        - invite_code (str): 邀请码
        - user_id (int): 用户ID

        返回:
        - dict: 更新后的招生人员模型实例字典
        """
        result = await PersonnelCRUD(auth).get(row_key="invite_code", row_value=invite_code)
        if not result:
            raise CustomException(msg="邀请码无效")

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
