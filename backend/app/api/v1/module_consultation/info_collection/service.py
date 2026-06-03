"""
咨询会信息聚合 - 服务层
"""

from difflib import SequenceMatcher

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import InfoCollectionCRUD
from .model import InfoStatus
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
    async def run_compliance_diagnosis_background(cls, consultation_id: int) -> None:
        """
        审核通过后后台合规诊断（独立会话，避免与审核请求争抢行锁）
        """
        try:
            from app.core.database import async_db_session

            from ..compliance.scoring_service import ComplianceScoringServiceV1
            from .model import ConsultationInfoModel

            async with async_db_session() as session:
                consultation = await session.get(ConsultationInfoModel, consultation_id)
                if not consultation:
                    return
                result = await ComplianceScoringServiceV1.diagnose_consultation(consultation)
                await ComplianceScoringServiceV1.save_diagnosis_result(consultation_id, result)
                log.info(f"后台合规诊断完成，咨询会ID: {consultation_id}, 评分: {result.score}")
        except Exception as e:
            log.warning(f"后台合规诊断失败，咨询会ID: {consultation_id}: {e}")

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

    @classmethod
    async def deduplicate_service(cls, auth: AuthSchema, similarity_threshold: float = 0.8) -> dict:
        """
        自动去重 - 基于名称+时间+地点的相似度去重合并

        参数:
        - auth (AuthSchema): 认证信息
        - similarity_threshold (float): 相似度阈值(0-1, 默认0.8)

        返回:
        - dict: 去重结果统计
        """
        all_items = await InfoCollectionCRUD(auth).list_crud(order_by=[{"id": "asc"}])
        non_duplicate_items = [item for item in all_items if not item.is_duplicate]

        duplicate_groups = []
        processed_ids = set()

        for i, item in enumerate(non_duplicate_items):
            if item.id in processed_ids:
                continue

            group = [item]
            for j in range(i + 1, len(non_duplicate_items)):
                other = non_duplicate_items[j]
                if other.id in processed_ids:
                    continue

                if cls._calculate_similarity(item, other) >= similarity_threshold:
                    group.append(other)
                    processed_ids.add(other.id)

            if len(group) > 1:
                duplicate_groups.append(group)
                processed_ids.add(item.id)

        # 标记重复记录(保留最早创建的作为原始记录)
        marked_count = 0
        for group in duplicate_groups:
            original = min(group, key=lambda x: x.id)
            for dup in group:
                if dup.id != original.id and not dup.is_duplicate:
                    await InfoCollectionCRUD(auth).update_crud(
                        dup.id,
                        {
                            "is_duplicate": True,
                            "duplicate_of_id": original.id,
                        },
                    )
                    marked_count += 1

        log.info(
            f"自动去重完成: 检查 {len(non_duplicate_items)} 条，发现 {len(duplicate_groups)} 组重复，标记 {marked_count} 条"
        )
        return {
            "total_checked": len(non_duplicate_items),
            "duplicate_groups": len(duplicate_groups),
            "marked_duplicates": marked_count,
        }

    @classmethod
    def _calculate_similarity(cls, item1, item2) -> float:
        """计算两条咨询会记录的相似度"""
        title_sim = SequenceMatcher(None, item1.title or "", item2.title or "").ratio()

        # 时间相同加分
        time_match = 0.0
        if item1.start_date and item2.start_date and item1.start_date == item2.start_date:
            time_match = 1.0

        # 地点相同加分
        location_match = 0.0
        if item1.city and item2.city and item1.city == item2.city:
            location_match = 0.8
        if item1.address and item2.address:
            addr_sim = SequenceMatcher(None, item1.address, item2.address).ratio()
            location_match = max(location_match, addr_sim)

        # 加权平均: 标题权重0.5, 时间0.25, 地点0.25
        return title_sim * 0.5 + time_match * 0.25 + location_match * 0.25

    @classmethod
    async def update_expired_service(cls, auth: AuthSchema) -> dict:
        """
        定时更新已过期的咨询会状态

        将 end_date < 今天的 approved 状态咨询会自动更新为 expired

        返回:
        - dict: 更新结果统计
        """
        from datetime import date

        from app.common.enums import QueueEnum

        today = date.today()
        search = {
            "status": (QueueEnum.eq.value, InfoStatus.APPROVED.value),
            "end_date": (QueueEnum.lt.value, today.isoformat()),
        }
        expired_items = await InfoCollectionCRUD(auth).list_crud(search=search)

        updated_count = 0
        for item in expired_items:
            await InfoCollectionCRUD(auth).update_crud(
                item.id, {"status": InfoStatus.EXPIRED.value}
            )
            updated_count += 1

        log.info(f"定时更新过期咨询会: 更新 {updated_count} 条")
        return {"updated_count": updated_count}

    @classmethod
    async def crawl_and_save_service(
        cls,
        auth: AuthSchema,
        crawler_names: list[str] | None = None,
    ) -> dict:
        """
        执行爬虫抓取并保存到数据库

        参数:
        - crawler_names: 指定爬虫名称列表，默认仅微信公众号渠道

        返回:
        - dict: 抓取结果统计
        """
        from .crawler import CrawlerRegistry

        names = crawler_names or ["wechat_official_account"]
        crawl_auth = AuthSchema(db=auth.db, check_data_scope=False)
        all_results = await CrawlerRegistry.run(names)

        total_fetched = 0
        total_saved = 0
        total_skipped = 0

        for source_name, items in all_results.items():
            total_fetched += len(items)
            for item in items:
                try:
                    external_id = item.get("external_id")
                    if external_id:
                        existing = await InfoCollectionCRUD(crawl_auth).list_crud(
                            search={"external_id": ("eq", external_id)}
                        )
                        if existing:
                            total_skipped += 1
                            continue

                    create_data = {
                        "title": item["title"],
                        "organizer": item["organizer"],
                        "organizer_nature": item.get("organizer_nature"),
                        "start_date": item["start_date"],
                        "end_date": item.get("end_date"),
                        "province": item.get("province"),
                        "city": item.get("city"),
                        "address": item.get("address"),
                        "venue_name": item.get("venue_name"),
                        "booth_fee": item.get("booth_fee"),
                        "fee_description": item.get("fee_description"),
                        "registration_email": item.get("registration_email"),
                        "guidance_unit": item.get("guidance_unit"),
                        "route_arrangement": item.get("route_arrangement"),
                        "event_time_text": item.get("event_time_text"),
                        "source_type": item.get("source_type", "crawler"),
                        "source_url": item.get("source_url"),
                        "external_id": item.get("external_id"),
                        "description": item.get("description"),
                        "status": InfoStatus.PENDING.value,
                        "search_keywords": item.get("search_keywords")
                        or (
                            f"{item.get('title', '')} {item.get('organizer', '')} "
                            f"{item.get('city', '')}"
                        ),
                    }
                    await InfoCollectionCRUD(crawl_auth).create_crud(create_data)
                    total_saved += 1
                except Exception as e:
                    log.warning(f"[{source_name}] 保存单条数据失败: {e}")

        log.info(
            f"爬虫抓取完成: 抓取 {total_fetched} 条，保存 {total_saved} 条，跳过 {total_skipped} 条"
        )
        return {
            "total_fetched": total_fetched,
            "total_saved": total_saved,
            "total_skipped": total_skipped,
        }

    @classmethod
    async def import_excel_service(cls, auth: AuthSchema, file) -> dict:
        """Excel 批量导入全网抓取咨询会信息"""
        from .excel_import import import_excel_file

        return await import_excel_file(auth=auth, file=file)

    @classmethod
    def import_template_bytes_service(cls) -> bytes:
        """下载 Excel 导入模板"""
        from .excel_import import get_import_template_bytes

        return get_import_template_bytes()

    @classmethod
    async def get_approved_list_service(cls, auth: AuthSchema) -> list[dict]:
        """
        获取已审核的咨询会列表（用于报名下拉选择）

        参数:
        - auth (AuthSchema): 认证信息模型

        返回:
        - list[dict]: 已审核咨询会简要信息列表
        """
        from app.common.enums import QueueEnum

        from .schema import InfoCollectionSimpleOutSchema

        search = {"status": (QueueEnum.eq.value, InfoStatus.APPROVED.value)}
        obj_list = await InfoCollectionCRUD(auth).list_crud(
            search=search,
            order_by=[{"start_date": "asc"}],
        )
        return [InfoCollectionSimpleOutSchema.model_validate(obj).model_dump() for obj in obj_list]
