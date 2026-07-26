import json
from collections.abc import Callable
from datetime import datetime
from typing import Any

from apscheduler.events import (
    EVENT_ALL,
    EVENT_ALL_JOBS_REMOVED,
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_SUBMITTED,
    JobEvent,
)
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app.config.setting import settings
from app.core.database import engine
from app.core.logger import logger

# 任务状态常量
JOB_STATUS_FAILED = 3

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={
        "default": RedisJobStore(
            host=settings.REDIS_HOST,
            port=int(settings.REDIS_PORT),
            username=settings.REDIS_USER or None,
            password=settings.REDIS_PASSWORD or None,
            db=int(settings.REDIS_DB_NAME),
        ),
        "sqlalchemy": SQLAlchemyJobStore(url=settings.DB_URI, engine=engine),
        "memory": MemoryJobStore(),
    },
    executors={
        "default": AsyncIOExecutor(),
        "threadpool": ThreadPoolExecutor(max_workers=10),
        "processpool": ProcessPoolExecutor(max_workers=1),
    },
    job_defaults={
        "coalesce": True,
        "max_instances": 5,
    },
    timezone="Asia/Shanghai",
)


class SchedulerUtil:
    """定时任务 SDK — 仅封装 APScheduler 核心操作，不含业务逻辑（无 ORM/实体引用）。"""

    redis_instance: Redis | None = None
    job_name_cache: dict[str, str | tuple[str, str]] = {}

    @classmethod
    def _get_trigger_type(cls, job_id: str) -> str:
        """获取任务的触发类型"""
        job = cls.get_job(job_id=job_id)
        if not job:
            return "manual"
        trigger = job.trigger
        if isinstance(trigger, CronTrigger):
            return "cron"
        if isinstance(trigger, IntervalTrigger):
            return "interval"
        if isinstance(trigger, DateTrigger):
            if trigger.run_date:
                now = datetime.now(trigger.run_date.tzinfo)
                diff = abs((trigger.run_date - now).total_seconds())
                if diff < 60:
                    return "manual"
            return "date"
        return "manual"

    @classmethod
    def _dispatch_job_event(cls, event: JobEvent) -> None:
        """APScheduler 事件统一处理（注册为 EVENT_ALL 回调），仅错误事件写入 DB。"""
        job_id = str(event.job_id) if hasattr(event, "job_id") else None
        if not job_id:
            return

        if event.code == EVENT_JOB_ERROR:
            exception = getattr(event, "exception", None)
            logger.error(f"任务 {job_id} 执行失败: {exception!s}")
            from app.api.v1.module_task.cronjob.job.model import JobModel
            try:
                job = SchedulerUtil.get_job(job_id=job_id)
                with Session(engine) as session:
                    job_log = JobModel(
                        job_id=job_id,
                        job_name=job.name if job else None,
                        trigger_type=SchedulerUtil._get_trigger_type(job_id) if job else "manual",
                        status=JOB_STATUS_FAILED,
                        error=str(exception),
                        next_run_time=str(job.next_run_time) if job and job.next_run_time else None,
                        job_state=SchedulerUtil._get_job_state(job) if job else None,
                    )
                    session.add(job_log)
                    session.commit()
                    logger.info(f"失败日志已记录: job_id={job_id}, id={job_log.id}")
            except Exception as e:
                logger.error(f"记录失败日志出错: job_id={job_id}, error={e}", exc_info=True)
        elif event.code == EVENT_JOB_MISSED:
            logger.warning(f"任务 {job_id} 错过执行时间")
        elif event.code == EVENT_JOB_EXECUTED:
            logger.info(f"任务 {job_id} 执行成功")
        elif event.code == EVENT_JOB_SUBMITTED:
            logger.info(f"任务 {job_id} 已提交执行")
        elif event.code == EVENT_JOB_REMOVED:
            logger.info(f"任务 {job_id} 已移除")
        elif event.code == EVENT_JOB_ADDED:
            logger.info(f"任务 {job_id} 已添加")
        elif event.code == EVENT_ALL_JOBS_REMOVED:
            logger.info("所有任务已从调度器中移除")

    @classmethod
    async def init_scheduler(cls, redis: Redis | None = None) -> None:
        """应用启动时初始化定时任务调度器（含系统级周期任务注册）。

        返回:
        - None
        """
        try:
            if redis:
                cls.redis_instance = redis
            scheduler.start()
            scheduler.add_listener(cls._dispatch_job_event, EVENT_ALL)
            scheduler.resume()

            # 注册系统级定时任务
            from app.api.v1.module_system.log.service import OperationLogService

            cls.register_system_job(
                "system_cleanup_operation_log", OperationLogService.cleanup_operation_log,
                trigger=CronTrigger(day_of_week="sun", hour=3, minute=0), name="操作日志清理",
            )
            logger.info("✅ 1 个系统周期任务已注册（操作日志清理）")
        except Exception as e:
            logger.error(f"❌ 定时任务调度器初始化失败: {e}")
            raise

    @classmethod
    def register_system_job(cls, job_id: str, func: Callable, trigger: Any, name: str) -> None:
        """外部注册系统级定时任务。"""
        scheduler.add_job(func, trigger=trigger, id=job_id, name=name, replace_existing=True)

    @classmethod
    def start(cls, paused: bool = False) -> None:
        scheduler.start(paused=paused)

    @classmethod
    def shutdown(cls, wait: bool = False) -> None:
        scheduler.shutdown(wait=wait)

    @classmethod
    def pause(cls) -> None:
        scheduler.pause()

    @classmethod
    def resume(cls) -> None:
        scheduler.resume()

    @classmethod
    def is_running(cls) -> bool:
        return scheduler.running

    @classmethod
    def get_scheduler_state(cls) -> int:
        return scheduler.state

    @classmethod
    def get_job(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        return scheduler.get_job(str(job_id), jobstore)

    @classmethod
    def get_jobs(cls, jobstore: str | None = None) -> list[Job]:
        return scheduler.get_jobs(jobstore)

    @classmethod
    def remove_job(cls, job_id: str | int, jobstore: str | None = None) -> None:
        scheduler.remove_job(str(job_id), jobstore)

    @classmethod
    def clear_jobs(cls) -> None:
        scheduler.remove_all_jobs()

    @classmethod
    def print_jobs(cls, jobstore: str | None = None) -> str:
        import io
        output = io.StringIO()
        scheduler.print_jobs(jobstore=jobstore, out=output)
        return output.getvalue()

    @classmethod
    def pause_job(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        return scheduler.pause_job(str(job_id), jobstore)

    @classmethod
    def resume_job(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        return scheduler.resume_job(str(job_id), jobstore)

    @classmethod
    def modify_job(cls, job_id: str | int, jobstore: str | None = None, **changes) -> Job | None:
        return scheduler.modify_job(str(job_id), jobstore, **changes)

    @classmethod
    def get_job_status(cls, job_id: str | int) -> int:
        """获取单个任务的当前状态。0=运行中 1=暂停中 2=已停止 3=未知"""
        job = cls.get_job(job_id=str(job_id))
        if not job:
            return 3
        if job.next_run_time is None:
            return 1
        if scheduler.state == 0:
            return 2
        return 0

    @classmethod
    def run_job_now(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        """立即执行任务（通过临时 Job，不修改原任务 trigger）。"""
        from datetime import timedelta

        job = cls.get_job(job_id=job_id, jobstore=jobstore)
        if not job:
            return None

        temp_job_id = f"{job_id}_run_now_{datetime.now().timestamp()}"
        cls.job_name_cache[temp_job_id] = (str(job_id), f"{job.name}(立即执行)")

        trigger = DateTrigger(run_date=datetime.now() + timedelta(seconds=0.1), timezone="Asia/Shanghai")
        temp_job = scheduler.add_job(
            func=job.func,
            trigger=trigger,
            args=job.args,
            kwargs=job.kwargs,
            id=temp_job_id,
            name=f"{job.name}(立即执行)",
            jobstore=jobstore or "default",
            executor=job.executor,
            max_instances=1,
        )
        logger.info(f"任务 {job_id} 已触发立即执行，临时任务 ID: {temp_job_id}")
        return temp_job

    @classmethod
    def _task_wrapper(cls, job_id: str | int, code_block: str | None, *args, **kwargs):
        """任务执行包装器，执行自定义代码块（同步版本，用于 ThreadPoolExecutor）"""
        import types

        def run_sync_handler():
            if not code_block:
                return None
            module = types.ModuleType(f"node_task_{job_id}")
            module.__dict__["__builtins__"] = __builtins__
            exec(code_block, module.__dict__)
            handler = module.__dict__.get("handler")
            if handler and callable(handler):
                return handler(*args, **kwargs)
            raise ValueError("代码块必须定义 handler(*args, **kwargs) 函数")

        try:
            return run_sync_handler()
        except Exception as e:
            logger.error(f"任务 {job_id} 执行失败: {e!s}")
            raise

    @classmethod
    def _get_job_state(cls, job) -> str | None:
        """获取任务状态（解析为可读的JSON格式）"""
        import pickle

        if not job:
            return None
        state = job.__getstate__()

        def serialize_value(obj):
            if obj is None:
                return None
            if isinstance(obj, (str, int, float, bool)):
                return obj
            if isinstance(obj, bytes):
                try:
                    return serialize_value(pickle.loads(obj))
                except Exception:
                    return obj.decode("utf-8", errors="replace")
            if isinstance(obj, dict):
                return {k: serialize_value(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [serialize_value(item) for item in obj]
            if hasattr(obj, "__dict__"):
                obj_dict = {}
                for k, v in obj.__dict__.items():
                    if not k.startswith("_"):
                        obj_dict[k] = serialize_value(v)
                return {"__class__": obj.__class__.__name__, **obj_dict}
            try:
                return str(obj)
            except Exception:
                return f"<{type(obj).__name__}>"

        return json.dumps(serialize_value(state), ensure_ascii=False, indent=2)
