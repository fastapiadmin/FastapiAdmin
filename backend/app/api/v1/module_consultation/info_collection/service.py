"""
咨询会信息聚合 - 服务层
"""

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import InfoCollectionCRUD
from .schema import (
    InfoCollectionCreateSchema,
    InfoCollectionOutSchema,
    InfoCollectionQueryParam,
    InfoCollectionUpdateSchema,
)


class InfoCollectionService:
    """
    咨询会信息管理模块服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID

        返回:
        - dict: 咨询会信息模型实例字典
        """
        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return InfoCollectionOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: InfoCollectionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (InfoCollectionQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 咨询会信息模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await InfoCollectionCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [InfoCollectionOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: InfoCollectionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (InfoCollectionQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await InfoCollectionCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: InfoCollectionCreateSchema) -> dict:
        """
        创建

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (InfoCollectionCreateSchema): 咨询会信息创建模型

        返回:
        - dict: 创建咨询会信息详情的字典
        """
        create_data = data.model_dump(exclude_unset=True)

        # 生成搜索关键词
        search_keywords = f"{create_data.get('title', '')} {create_data.get('organizer', '')} {create_data.get('city', '')}"
        create_data["search_keywords"] = search_keywords

        # 参与高校数量
        if create_data.get("participating_universities"):
            create_data["university_count"] = len(create_data["participating_universities"])

        obj = await InfoCollectionCRUD(auth).create_crud(create_data)
        return InfoCollectionOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: InfoCollectionUpdateSchema
    ) -> dict:
        """
        更新

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID
        - data (InfoCollectionUpdateSchema): 咨询会信息更新模型

        返回:
        - dict: 更新后咨询会信息详情的字典
        """
        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        update_data = data.model_dump(exclude_unset=True)

        # 更新搜索关键词
        if any(k in update_data for k in ["title", "organizer", "city"]):
            search_keywords = f"{update_data.get('title', obj.title)} {update_data.get('organizer', obj.organizer)} {update_data.get('city', obj.city or '')}"
            update_data["search_keywords"] = search_keywords

        # 更新参与高校数量
        if update_data.get("participating_universities") is not None:
            update_data["university_count"] = len(update_data["participating_universities"])

        updated_obj = await InfoCollectionCRUD(auth).update_crud(id, update_data)
        return InfoCollectionOutSchema.model_validate(updated_obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID
        """
        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        await InfoCollectionCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 咨询会信息ID列表
        """
        await InfoCollectionCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def approve_service(
        cls, auth: AuthSchema, id: int, review_comment: str | None = None
    ) -> dict:
        """
        审核通过

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID
        - review_comment (str | None): 审核意见

        返回:
        - dict: 更新后咨询会信息详情的字典
        """
        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        updated_obj = await InfoCollectionCRUD(auth).approve_crud(id, review_comment)
        return InfoCollectionOutSchema.model_validate(updated_obj).model_dump()

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, review_comment: str) -> dict:
        """
        审核拒绝

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID
        - review_comment (str): 审核意见

        返回:
        - dict: 更新后咨询会信息详情的字典
        """
        if not review_comment:
            raise CustomException(msg="拒绝时必须填写审核意见")

        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        updated_obj = await InfoCollectionCRUD(auth).reject_crud(id, review_comment)
        return InfoCollectionOutSchema.model_validate(updated_obj).model_dump()

    @classmethod
    async def archive_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        归档

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID

        返回:
        - dict: 更新后咨询会信息详情的字典
        """
        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        updated_obj = await InfoCollectionCRUD(auth).archive_crud(id)
        return InfoCollectionOutSchema.model_validate(updated_obj).model_dump()

    @classmethod
    async def update_compliance_score_service(
        cls,
        auth: AuthSchema,
        id: int,
        compliance_score: int,
        compliance_level: str,
        risk_factors: list | None = None,
    ) -> dict:
        """
        更新合规评分

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 咨询会信息ID
        - compliance_score (int): 合规评分(0-100)
        - compliance_level (str): 合规等级
        - risk_factors (list | None): 风险因素列表

        返回:
        - dict: 更新后咨询会信息详情的字典
        """
        if not 0 <= compliance_score <= 100:
            raise CustomException(msg="合规评分必须在0-100之间")

        obj = await InfoCollectionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        update_data = {
            "compliance_score": compliance_score,
            "compliance_level": compliance_level,
            "risk_factors": risk_factors or [],
        }

        updated_obj = await InfoCollectionCRUD(auth).update_crud(id, update_data)
        return InfoCollectionOutSchema.model_validate(updated_obj).model_dump()

    @classmethod
    async def preview_list_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        title: str | None = None,
        organizer: str | None = None,
        province: str | None = None,
        city: str | None = None,
        organizer_nature: str | None = None,
        compliance_level: str | None = None,
        source_type: str | None = None,
        status: str | None = None,
        start_date_begin: str | None = None,
        start_date_end: str | None = None,
    ) -> dict:
        """
        全部咨询会预览列表（带筛选）

        直接在列表页按多维度筛选，无需先保存筛选条件

        参数:
        - auth: 认证信息
        - page_no: 页码
        - page_size: 每页数量
        - title: 咨询会标题（模糊搜索）
        - organizer: 主办方（模糊搜索）
        - province: 省份
        - city: 城市
        - organizer_nature: 主办机构性质
        - compliance_level: 合规等级
        - source_type: 信息来源
        - status: 状态
        - start_date_begin: 开始日期-起
        - start_date_end: 开始日期-止

        返回:
        - dict: 分页数据
        """
        from app.common.enums import QueueEnum

        search = {}

        if title:
            search["title"] = (QueueEnum.like.value, title)
        if organizer:
            search["organizer"] = (QueueEnum.like.value, organizer)
        if province:
            search["province"] = (QueueEnum.eq.value, province)
        if city:
            search["city"] = (QueueEnum.eq.value, city)
        if organizer_nature:
            search["organizer_nature"] = (QueueEnum.eq.value, organizer_nature)
        if compliance_level:
            search["compliance_level"] = (QueueEnum.eq.value, compliance_level)
        if source_type:
            search["source_type"] = (QueueEnum.eq.value, source_type)
        if status:
            search["status"] = (QueueEnum.eq.value, status)

        if start_date_begin and start_date_end:
            search["start_date"] = (QueueEnum.between.value, (start_date_begin, start_date_end))
        elif start_date_begin:
            search["start_date"] = (QueueEnum.ge.value, start_date_begin)
        elif start_date_end:
            search["start_date"] = (QueueEnum.le.value, start_date_end)

        offset = (page_no - 1) * page_size
        return await InfoCollectionCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=[{"id": "desc"}],
            search=search,
        )
