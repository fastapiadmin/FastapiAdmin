from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException

from .crud import ApplicationCRUD
from .plugin_manifest import list_plugin_infos
from .schema import (
    ApplicationCreateSchema,
    ApplicationOutSchema,
    ApplicationQueryParam,
    ApplicationUpdateSchema,
    PluginInfoOut,
)


class ApplicationService:
    """
    应用系统管理服务层
    """

    @classmethod
    async def list_plugins_service(cls) -> list[dict]:
        """
        列出 ``app/plugin/module_*`` 插件元数据（含可选 ``plugin.toml``）。

        返回:
        - list[dict]: ``PluginInfoOut`` 字典列表。
        """
        rows = list_plugin_infos()
        return [PluginInfoOut.model_validate(row).model_dump() for row in rows]

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取应用详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 应用ID

        返回:
        - dict: 应用详情字典
        """
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="应用不存在")
        return ApplicationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ApplicationQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取应用列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (ApplicationQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数，支持字符串或字典列表

        返回:
        - list[dict]: 应用详情字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await ApplicationCRUD(auth).list_crud(
            search=search_dict, order_by=order_by
        )
        return [ApplicationOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ApplicationQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询应用（数据库 OFFSET/LIMIT）。

        参数:
        - auth (AuthSchema): 认证信息。
        - page_no (int): 页码。
        - page_size (int): 每页条数。
        - search (ApplicationQueryParam | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。

        返回:
        - dict: 分页结果。
        """
        return await ApplicationCRUD(auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=search.__dict__ if search else {},
            out_schema=ApplicationOutSchema,
        )

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: ApplicationCreateSchema) -> dict:
        """
        创建应用

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (ApplicationCreateSchema): 应用创建模型

        返回:
        - Dict: 应用详情字典
        """
        # 检查名称是否重复
        obj = await ApplicationCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg="创建失败，应用名称已存在")

        obj = await ApplicationCRUD(auth).create_crud(data=data)
        if not obj:
            raise CustomException(msg="创建应用失败")
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=obj.id)
        if not obj:
            raise CustomException(msg="创建应用失败")
        return ApplicationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: ApplicationUpdateSchema) -> dict:
        """
        更新应用

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 应用ID
        - data (ApplicationUpdateSchema): 应用更新模型

        返回:
        - Dict: 应用详情字典
        """
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该应用不存在")

        # 检查名称重复
        exist_obj = await ApplicationCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg="更新失败，应用名称重复")

        obj = await ApplicationCRUD(auth).update_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，该应用不存在")
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=obj.id)
        if not obj:
            raise CustomException(msg="更新应用失败")
        return ApplicationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除应用

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 应用ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，应用 {id} 不存在")
        await ApplicationCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量设置应用状态

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置应用状态模型

        返回:
        - None
        """
        await ApplicationCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
