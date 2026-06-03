"""
招生咨询会管理系统 - 定时任务注册模块

功能：在应用启动时自动注册以下定时任务到 APScheduler:
1. 咨询会信息抓取 (每日)     - 0 0 * * * (每天凌晨)
2. 咨询会状态更新 (每小时)   - 0 * * * * (每小时的第0分钟)
3. 自动去重 (每日)           - 0 2 * * * (每天凌晨2点)
4. 行程提醒 (每日)           - 0 8 * * * (每天早上8点)
"""

from app.core.ap_scheduler import scheduler
from app.core.database import async_db_session
from app.core.logger import log


async def _get_system_auth():
    """获取系统级认证信息(用于定时任务)"""
    from app.api.v1.module_system.auth.schema import AuthSchema

    async with async_db_session() as db:
        return AuthSchema(db=db, check_data_scope=False)


async def task_crawl_consultation() -> dict:
    """
    定时任务: 抓取咨询会信息

    触发: 每日凌晨
    """
    from app.api.v1.module_consultation.info_collection.service import InfoCollectionService

    log.info("[定时任务] 开始抓取咨询会信息...")
    auth = await _get_system_auth()
    result = await InfoCollectionService.crawl_and_save_service(
        auth=auth,
        crawler_names=["wechat_official_account"],
    )
    log.info(f"[定时任务] 抓取咨询会信息完成: {result}")
    return result


async def task_update_expired_consultation() -> dict:
    """
    定时任务: 更新过期咨询会状态

    触发: 每小时
    """
    from app.api.v1.module_consultation.info_collection.service import InfoCollectionService

    log.info("[定时任务] 开始更新过期咨询会状态...")
    auth = await _get_system_auth()
    result = await InfoCollectionService.update_expired_service(auth=auth)
    log.info(f"[定时任务] 更新过期咨询会状态完成: {result}")
    return result


async def task_deduplicate_consultation() -> dict:
    """
    定时任务: 自动去重咨询会信息

    触发: 每日凌晨2点
    """
    from app.api.v1.module_consultation.info_collection.service import InfoCollectionService

    log.info("[定时任务] 开始自动去重咨询会信息...")
    auth = await _get_system_auth()
    result = await InfoCollectionService.deduplicate_service(auth=auth)
    log.info(f"[定时任务] 自动去重完成: {result}")
    return result


async def task_send_itinerary_reminders() -> dict:
    """
    定时任务: 发送行程提醒

    触发: 每天早上8点
    """
    from app.api.v1.module_consultation.itinerary.service import ItineraryService

    log.info("[定时任务] 开始发送行程提醒...")
    auth = await _get_system_auth()
    result = await ItineraryService.send_reminders_service(auth=auth, days_before=1)
    log.info(f"[定时任务] 发送行程提醒完成: {result}")
    return result


def register_consultation_cron_jobs() -> None:
    """
    注册招生咨询会管理系统的定时任务到 APScheduler

    在应用启动时调用，将4个定时任务注册到调度器
    """
    jobs = [
        {
            "id": "consultation_crawl_daily",
            "name": "咨询会信息抓取(每日)",
            "func": task_crawl_consultation,
            "trigger": "cron",
            "hour": 0,
            "minute": 0,
            "second": 0,
        },
        {
            "id": "consultation_update_expired_hourly",
            "name": "咨询会状态更新(每小时)",
            "func": task_update_expired_consultation,
            "trigger": "cron",
            "hour": "*",
            "minute": 0,
            "second": 0,
        },
        {
            "id": "consultation_deduplicate_daily",
            "name": "自动去重(每日)",
            "func": task_deduplicate_consultation,
            "trigger": "cron",
            "hour": 2,
            "minute": 0,
            "second": 0,
        },
        {
            "id": "itinerary_reminder_daily",
            "name": "行程提醒(每日)",
            "func": task_send_itinerary_reminders,
            "trigger": "cron",
            "hour": 8,
            "minute": 0,
            "second": 0,
        },
    ]

    registered_count = 0
    for job_config in jobs:
        job_id = job_config["id"]
        try:
            existing = scheduler.get_job(job_id)
            if existing:
                scheduler.remove_job(job_id)
                log.info(f"定时任务 {job_id} 已存在，已移除旧任务")

            scheduler.add_job(
                func=job_config["func"],
                trigger=job_config["trigger"],
                hour=job_config["hour"],
                minute=job_config["minute"],
                second=job_config["second"],
                id=job_id,
                name=job_config["name"],
                coalesce=True,
                max_instances=1,
                jobstore="default",
                executor="default",
            )
            registered_count += 1
            log.info(f"定时任务已注册: {job_id} ({job_config['name']})")
        except Exception as e:
            log.error(f"定时任务注册失败 {job_id}: {e}", exc_info=True)

    log.info(f"招生咨询会定时任务注册完成: {registered_count}/{len(jobs)} 个")
