from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.role.crud import RoleCRUD
from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import UserModel
from .schema import UserCreateSchema, UserUpdateSchema


class UserCRUD(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    """用户模块数据层"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        super().__init__(model=UserModel, auth=auth, db=db)

    async def create_obj_crud(self, data: UserCreateSchema) -> UserModel | None:
        """创建用户

        参数:
        - data (UserCreateSchema): 创建模型。

        返回:
        - UserModel | None: 新建实体。
        """
        return await self.create(data=data)

    async def update_last_login(self, id: int) -> None:
        """更新用户最后登录时间

        参数:
        - id (int): 用户ID
        """
        await self.set([id], last_login=datetime.now())

    async def set_user_roles(self, user_ids: list[int], role_ids: list[int]) -> None:
        """批量设置用户角色"""
        user_objs = await self.get_list(search={"id": ("in", user_ids)}, preload=["roles"])
        role_objs = [] if not role_ids else await RoleCRUD(self.auth, self.db).get_list(search={"id": ("in", role_ids)})

        for obj in user_objs:
            obj.roles.clear()
            obj.roles.extend(role_objs)
        await self.db.flush()

    async def set_user_positions(self, user_ids: list[int], position_ids: list[int]) -> None:
        """批量设置用户岗位"""
        user_objs = await self.get_list(search={"id": ("in", user_ids)}, preload=["positions"])
        position_objs = [] if not position_ids else await PositionCRUD(self.auth, self.db).get_list(search={"id": ("in", position_ids)})

        for obj in user_objs:
            obj.positions.clear()
            obj.positions.extend(position_objs)
        await self.db.flush()

    async def change_password(self, id: int, password_hash: str) -> UserModel:
        """修改用户密码

        参数:
        - id (int): 用户ID
        - password_hash (str): 密码哈希值

        返回:
        - UserModel: 更新后的用户信息
        """
        return await self.update(id=id, data=UserUpdateSchema(password=password_hash))

    async def forget_password(self, id: int, password_hash: str) -> UserModel:
        """重置密码（与 change_password 逻辑相同）"""
        return await self.change_password(id=id, password_hash=password_hash)
