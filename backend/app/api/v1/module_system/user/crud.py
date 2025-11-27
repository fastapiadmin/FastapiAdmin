# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence, Union, Any
from datetime import datetime

from app.core.base_crud import CRUDBase

from app.api.v1.module_system.auth.schema import AuthSchema
from .model import UserModel
from .schema import UserCreateSchema, UserForgetPasswordSchema, UserUpdateSchema
from ..role.crud import RoleCRUD
from ..position.crud import PositionCRUD


class UserCRUD(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    """用户模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化用户CRUD
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=UserModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[UserModel]:
        """
        根据id获取用户信息
        
        参数:
        - id (int): 用户ID
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[UserModel]: 用户信息,如果不存在则为None
        """
        return await self.get(
            preload=preload,
            id=id,
        )

    async def get_by_username_crud(self, username: str, preload: Optional[List[Union[str, Any]]] = None) -> Optional[UserModel]:
        """
        根据用户名获取用户信息
        
        参数:
        - username (str): 用户名
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[UserModel]: 用户信息,如果不存在则为None
        """
        return await self.get(
            preload=preload,
            username=username,
        )
    

    
    async def get_by_mobile_crud(self, mobile: str, preload: Optional[List[Union[str, Any]]] = None) -> Optional[UserModel]:
        """
        根据手机号获取用户信息
        
        参数:
        - mobile (str): 手机号
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[UserModel]: 用户信息,如果不存在则为None
        """
        return await self.get(
            preload=preload,
            mobile=mobile,
        )

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[UserModel]:
        """
        获取用户列表
        
        参数:
        - search (Dict | None): 查询参数对象。
        - order_by (List[Dict[str, str]] | None): 排序参数列表。
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
            Sequence[UserModel]: 用户列表
        """
        return await self.list(
            search=search,
            order_by=order_by,
            preload=preload,
        )

    async def update_last_login_crud(self, id: int) -> Optional[UserModel]:
        """
        更新用户最后登录时间
        
        参数:
        - id (int): 用户ID
        
        返回:
        - Optional[UserModel]: 更新后的用户信息
        """
        return await self.update(id=id, data={"last_login": datetime.now()})

    async def set_available_crud(self, ids: List[int], status: str) -> None:
        """
        批量设置用户可用状态
        
        参数:
        - ids (List[int]): 用户ID列表
        - status (bool): 可用状态
        
        返回:
        - None:
        """
        await self.set(ids=ids, status=status)

    async def set_user_roles_crud(self, user_ids: List[int], role_ids: List[int]) -> None:
        """
        批量设置用户角色
        
        参数:
        - user_ids (List[int]): 用户ID列表
        - role_ids (List[int]): 角色ID列表
        
        返回:
        - None:
        """
        user_objs = await self.list(search={"id": ("in", user_ids)})
        if role_ids:
            role_objs = await RoleCRUD(self.auth).get_list_crud(search={"id": ("in", role_ids)})
        else:
            role_objs = []
        
        for obj in user_objs:
            relationship = obj.roles
            relationship.clear()
            relationship.extend(role_objs)
        await self.db.flush()


    async def set_user_positions_crud(self, user_ids: List[int], position_ids: List[int]) -> None:
        """
        批量设置用户岗位
        
        参数:
        - user_ids (List[int]): 用户ID列表
        - position_ids (List[int]): 岗位ID列表
        
        返回:
        - None:
        """
        user_objs = await self.list(search={"id": ("in", user_ids)})
        if position_ids:
            position_objs = await PositionCRUD(self.auth).get_list_crud(search={"id": ("in", position_ids)})
        else:
            position_objs = []

        for obj in user_objs:
            relationship = obj.positions
            relationship.clear()
            relationship.extend(position_objs)
        await self.db.flush()

    async def change_password_crud(self, id: int, password_hash: str) -> Optional[UserModel]:
        """
        修改用户密码
        
        参数:
        - id (int): 用户ID
        - password_hash (str): 密码哈希值
        
        返回:
        - Optional[UserModel]: 更新后的用户信息
        """
        return await self.update(id=id, data=UserUpdateSchema(password=password_hash))



    async def forget_password_crud(self, id: int, password_hash: str) -> Optional[UserModel]:
        """
        重置密码
        
        参数:
        - id (int): 用户ID
        - password_hash (str): 密码哈希值
        
        返回:
        - Optional[UserModel]: 更新后的用户信息
        """
        return await self.update(id=id, data=UserUpdateSchema(password=password_hash))

    async def register_user_crud(self, data: UserForgetPasswordSchema) -> Optional[UserModel]:
        """
        用户注册
        
        参数:
        - data (UserForgetPasswordSchema): 用户注册信息
        
        返回:
        - Optional[UserModel]: 注册成功的用户信息,如果用户名已存在则返回None
        """
        if await self.get_by_username_crud(username=data.username):
            return None
        return await self.create(data=UserCreateSchema(**data.model_dump()))