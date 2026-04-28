"""
招生组推送服务

利用现有通知公告系统，将咨询会行程信息推送给招生组
"""

from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.notice.model import NoticeModel
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import log


class RegistrationPushService:
    """
    招生组推送服务

    将报名行程信息通过通知公告推送给招生组组长
    """

    @classmethod
    async def forward_to_team_service(
        cls,
        auth: AuthSchema,
        registration_id: int,
        team_leader_id: int,
        assignee_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        一键转发行程到招生组

        1. 获取报名记录和咨询会信息
        2. 构建通知内容
        3. 创建通知公告

        参数:
            auth: 认证信息
            registration_id: 报名记录ID
            team_leader_id: 招生组组长ID
            assignee_ids: 指派人员ID列表

        返回:
            dict: 发送结果
        """
        from app.api.v1.module_consultation.info_collection.crud import InfoCollectionCRUD
        from app.api.v1.module_consultation.registration.crud import RegistrationCRUD

        # 获取报名记录
        registration = await RegistrationCRUD(auth).get_by_id_crud(registration_id)
        if not registration:
            raise CustomException(msg="该报名记录不存在")

        # 获取咨询会信息
        consultation = await InfoCollectionCRUD(auth).get_by_id_crud(registration.consultation_id)
        if not consultation:
            raise CustomException(msg="关联的咨询会信息不存在")

        # 构建通知内容
        title = f"【行程安排】{consultation.title} - {registration.university_name or '待分配'}"

        content_parts = [
            f"咨询会名称：{consultation.title}",
            f"举办时间：{consultation.start_date} {consultation.start_time or ''}",
            f"举办地点：{consultation.city or ''} {consultation.address or ''}",
        ]

        if registration.booth_number:
            content_parts.append(f"展位号：{registration.booth_number}")

        if registration.contact_person:
            content_parts.append(f"联系人：{registration.contact_person}")
            content_parts.append(f"联系电话：{registration.contact_phone or ''}")

        if assignee_ids:
            content_parts.append(f"\n指派人员ID：{', '.join(str(id) for id in assignee_ids)}")

        content_parts.append(f"\n报名时间：{registration.registration_time}")
        content_parts.append(f"审核时间：{registration.approval_time}")

        notice_content = "\n".join(content_parts)

        # 创建通知公告
        async with async_db_session() as session:
            notice = NoticeModel(
                notice_title=title,
                notice_type="1",  # 1=通知
                notice_content=notice_content,
                created_id=auth.user.id if auth.user else None,
            )
            session.add(notice)
            await session.commit()
            await session.refresh(notice)

            notice_id = notice.id

        log.info(f"创建行程通知公告成功，通知ID: {notice_id}, 招生组组长ID: {team_leader_id}")

        return {
            "notice_id": notice_id,
            "title": title,
            "registration_id": registration_id,
            "team_leader_id": team_leader_id,
            "assignee_ids": assignee_ids or [],
        }

    @classmethod
    async def send_batch_notification(
        cls,
        auth: AuthSchema,
        registration_ids: list[int],
        team_leader_ids: list[int],
    ) -> dict[str, Any]:
        """
        批量发送行程通知

        参数:
            auth: 认证信息
            registration_ids: 报名记录ID列表
            team_leader_ids: 招生组组长ID列表

        返回:
            dict: 发送结果统计
        """
        success_count = 0
        fail_count = 0
        results = []

        for registration_id in registration_ids:
            for team_leader_id in team_leader_ids:
                try:
                    result = await cls.forward_to_team_service(
                        auth=auth,
                        registration_id=registration_id,
                        team_leader_id=team_leader_id,
                    )
                    success_count += 1
                    results.append(result)
                except Exception as e:
                    fail_count += 1
                    log.error(f"发送通知失败: {e}")
                    results.append({"registration_id": registration_id, "error": str(e)})

        return {
            "total": len(registration_ids) * len(team_leader_ids),
            "success_count": success_count,
            "fail_count": fail_count,
            "results": results,
        }
