"""
配置咨询会信息爬虫定时任务

使用方法:
    python scripts/setup_crawler_cronjob.py
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.ap_scheduler import scheduler
from app.core.logger import log


async def setup_crawler_job():
    """
    配置咨询会信息爬虫定时任务

    默认配置：每天凌晨2点执行
    """
    from app.api.v1.module_consultation.info_collection.crawler_service import (
        run_crawler_task,
    )

    job_id = "consultation_crawler_daily"

    # 检查是否已存在该任务
    existing_job = scheduler.get_job(job_id)
    if existing_job:
        log.info(f"定时任务 {job_id} 已存在，跳过配置")
        return

    # 添加定时任务：每天凌晨2点执行
    scheduler.add_job(
        run_crawler_task,
        trigger="cron",
        hour=2,
        minute=0,
        id=job_id,
        name="咨询会信息每日抓取",
        description="每天凌晨2点自动抓取全网高招类咨询会信息",
        replace_existing=True,
    )

    log.info(f"定时任务 {job_id} 配置成功")
    log.info("执行计划：每天凌晨 02:00")


if __name__ == "__main__":
    log.info("开始配置咨询会信息爬虫定时任务...")
    asyncio.run(setup_crawler_job())
    log.info("定时任务配置完成")
