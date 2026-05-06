"""
活动撰写 - 服务层
"""

import json
import uuid
from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.ai_service import AIService
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import DocumentCRUD
from .model import DocumentStatus, PromotionDocumentModel
from .schema import (
    DocumentOutSchema,
    DocumentQuerySchema,
)


class DocumentService:
    """
    活动撰写服务层

    职责：活动文档增删改查、发布/归档、阅读计数、AI生成微信公众号内容
    状态机：draft(草稿) -> published(已发布) -> archived(已归档)
    约束：已发布文档需先撤销才能编辑；附件字段需JSON序列化/反序列化
    AI生成：状态机 pending -> generating -> success/failed
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID

        返回:
        - dict: 活动撰写模型实例字典
        """
        obj = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该文档不存在")
        return cls._format_document_output(obj)

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: DocumentQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (DocumentQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await DocumentCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建活动撰写

        自动生成文档编号，格式：DC + 12位大写随机字符
        附件字段(attachment_urls/names)若为list则自动序列化为JSON字符串存储
        """
        document_no = f"DC{uuid.uuid4().hex[:12].upper()}"
        data["document_no"] = document_no

        if "attachment_urls" in data and isinstance(data["attachment_urls"], list):
            data["attachment_urls"] = json.dumps(data["attachment_urls"])
        if "attachment_names" in data and isinstance(data["attachment_names"], list):
            data["attachment_names"] = json.dumps(data["attachment_names"])

        obj = await DocumentCRUD(auth).create_crud(data=data)
        log.info(f"创建活动撰写成功: {obj.id}")
        return cls._format_document_output(obj)

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新活动撰写

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的活动撰写模型实例字典
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        # 已发布文档需先撤销(变更为非published状态)才能编辑
        if existing.document_status == DocumentStatus.PUBLISHED.value:
            raise CustomException(msg="已发布的文档需要先撤销才能编辑")

        if "attachment_urls" in data and isinstance(data["attachment_urls"], list):
            data["attachment_urls"] = json.dumps(data["attachment_urls"])
        if "attachment_names" in data and isinstance(data["attachment_names"], list):
            data["attachment_names"] = json.dumps(data["attachment_names"])

        obj = await DocumentCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新活动撰写成功: {id}")
        return cls._format_document_output(obj)

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除活动撰写

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        await DocumentCRUD(auth).delete_crud(id=id)
        log.info(f"删除活动撰写成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除活动撰写

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 活动撰写ID列表
        """
        await DocumentCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除活动撰写成功: {ids}")

    @classmethod
    async def publish_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        发布文档

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID

        返回:
        - dict: 更新后的活动撰写模型实例字典
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        if existing.document_status == DocumentStatus.PUBLISHED.value:
            raise CustomException(msg="该文档已发布")

        update_data = {
            "document_status": DocumentStatus.PUBLISHED.value,
            "publish_time": datetime.now(),
        }

        obj = await DocumentCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"发布文档成功: {id}")
        return cls._format_document_output(obj)

    @classmethod
    async def archive_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        归档文档

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID

        返回:
        - dict: 更新后的活动撰写模型实例字典
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        update_data = {
            "document_status": DocumentStatus.ARCHIVED.value,
        }

        obj = await DocumentCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"归档文档成功: {id}")
        return cls._format_document_output(obj)

    @classmethod
    async def view_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        阅读文档（增加阅读量）

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动撰写ID

        返回:
        - dict: 更新后的活动撰写模型实例字典
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        update_data = {
            "view_count": existing.view_count + 1,
        }

        obj = await DocumentCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"阅读文档成功: {id}")
        return cls._format_document_output(obj)

    @classmethod
    async def generate_wechat_content_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        AI生成微信公众号格式化内容

        流程：
        1. 更新状态为 generating
        2. 调用 AIService.generate_wechat_content 生成内容
        3. 成功：写入 wechat_formatted_content，状态改为 success
        4. 失败：状态改为 failed，抛出异常
        """
        existing = await DocumentCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该文档不存在")

        if not existing.document_content:
            raise CustomException(msg="文档内容为空，无法生成")

        # 更新状态为生成中
        await DocumentCRUD(auth).update_crud(id=id, data={"ai_generation_status": "generating"})

        try:
            # 调用AI服务生成内容
            wechat_content = await AIService.generate_wechat_content(
                title=existing.document_title or "",
                content=existing.document_content,
                summary=existing.document_summary,
                activity_name=existing.activity_name,
            )

            # 更新文档内容和状态
            update_data = {
                "wechat_formatted_content": wechat_content,
                "ai_generation_status": "success",
            }

            obj = await DocumentCRUD(auth).update_crud(id=id, data=update_data)
            log.info(f"AI生成微信公众号内容成功: {id}")
            return cls._format_document_output(obj)

        except Exception as e:
            # 更新状态为失败
            await DocumentCRUD(auth).update_crud(id=id, data={"ai_generation_status": "failed"})
            log.error(f"AI生成失败: {id}, 错误: {str(e)}")
            raise CustomException(msg=f"AI生成失败: {str(e)}")

    @classmethod
    def _format_document_output(cls, obj: PromotionDocumentModel) -> dict:
        """格式化文档输出，将附件字段从JSON字符串反序列化为list"""
        result = DocumentOutSchema.model_validate(obj).model_dump()

        for field in ["attachment_urls", "attachment_names"]:
            if result.get(field) and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []

        return result
