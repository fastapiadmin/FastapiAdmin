import json
from collections.abc import Callable
from datetime import datetime
from typing import Any

from apscheduler.events import (
    EVENT_ALL,
    EVENT_ALL_JOBS_REMOVED,
    EVENT_EXECUTOR_ADDED,
    EVENT_EXECUTOR_REMOVED,
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_MISSED,
    EVENT_JOB_MODIFIED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_SUBMITTED,
    EVENT_JOBSTORE_ADDED,
    EVENT_JOBSTORE_REMOVED,
    EVENT_SCHEDULER_PAUSED,
    EVENT_SCHEDULER_RESUMED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_SCHEDULER_START,
    EVENT_SCHEDULER_STARTED,
    JobEvent,
    JobExecutionEvent,
    JobSubmissionEvent,
    SchedulerEvent,
)
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from redis.asyncio import Redis

from app.config.setting import settings
from app.core.database import engine
from app.core.logger import log
from app.plugin.module_task.node.model import NodeModel
from app.utils.cron_util import CronUtil

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={
        "default": MemoryJobStore(),
        "sqlalchemy": SQLAlchemyJobStore(url=settings.DB_URI, engine=engine),
        "redis": RedisJobStore(
            host=settings.REDIS_HOST,
            port=int(settings.REDIS_PORT),
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
            db=int(settings.REDIS_DB_NAME),
        )
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
    """
    定时任务相关方法
    """

    redis_instance: Redis | None = None

    @classmethod
    def scheduler_event_listener(cls, event: JobEvent | JobExecutionEvent) -> None:
        """
        监听任务执行事件，记录执行日志
        每次执行都创建新记录，保留所有历史执行记录
        """
        try:
            # 事件处理器映射
            event_handlers: dict[int, Callable] = {
                # 调度器事件
                EVENT_SCHEDULER_STARTED: cls._handle_scheduler_started,
                EVENT_SCHEDULER_START: cls._handle_scheduler_started,
                EVENT_SCHEDULER_SHUTDOWN: cls._handle_scheduler_shutdown,
                EVENT_SCHEDULER_PAUSED: cls._handle_scheduler_paused,
                EVENT_SCHEDULER_RESUMED: cls._handle_scheduler_resumed,
                # 执行器事件
                EVENT_EXECUTOR_ADDED: cls._handle_executor_added,
                EVENT_EXECUTOR_REMOVED: cls._handle_executor_removed,
                # JobStore 事件
                EVENT_JOBSTORE_ADDED: cls._handle_jobstore_added,
                EVENT_JOBSTORE_REMOVED: cls._handle_jobstore_removed,
                EVENT_ALL_JOBS_REMOVED: cls._handle_all_jobs_removed,
                # 任务事件
                EVENT_JOB_ADDED: cls._handle_job_added,
                EVENT_JOB_REMOVED: cls._handle_job_removed,
                EVENT_JOB_MODIFIED: cls._handle_job_modified,
                EVENT_JOB_SUBMITTED: cls._handle_job_submitted,
                EVENT_JOB_EXECUTED: cls._handle_job_executed,
                EVENT_JOB_ERROR: cls._handle_job_error,
                EVENT_JOB_MISSED: cls._handle_job_missed,
                EVENT_JOB_MAX_INSTANCES: cls._handle_job_max_instances,
            }

            # 处理事件
            if event.code in event_handlers:
                handler = event_handlers[event.code]
                handler(event)
            else:
                # 处理其他事件
                cls._handle_other_event(event)

        except Exception as e:
            log.error(f"处理任务执行事件失败: {e!s}", exc_info=True)

    @classmethod
    def _handle_job_submitted(cls, event: JobSubmissionEvent) -> None:
        """
        处理任务提交事件
        """
        job_id = str(event.job_id)
        job = cls.get_job(job_id=job_id)

        if job:
            log.info(f"任务 {job_id} ({job.name}) 已提交执行")

            # 创建执行日志
            cls._create_job_log(
                job_id=job_id,
                job_name=job.name,
                trigger_type=cls._get_trigger_type(job_id),
                status="running",
            )
        else:
            log.warning(f"任务 {job_id} 提交执行，但未找到任务信息")

    @classmethod
    def _handle_job_executed(cls, event: JobExecutionEvent) -> None:
        """
        处理任务执行成功事件
        """
        job_id = str(event.job_id)
        retval = getattr(event, "retval", None)
        scheduled_run_time = getattr(event, "scheduled_run_time", None)

        log.info(f"任务 {job_id} 执行成功")
        if retval:
            log.debug(f"任务 {job_id} 返回值: {retval}")
        if scheduled_run_time:
            log.debug(f"任务 {job_id} 计划执行时间: {scheduled_run_time}")

        # 更新执行日志
        cls._update_latest_job_log(
            job_id=job_id,
            status="success",
            result=str(retval) if retval else None,
        )

    @classmethod
    def _handle_job_error(cls, event: JobExecutionEvent) -> None:
        """
        处理任务执行失败事件
        """
        job_id = str(event.job_id)
        exception = getattr(event, "exception", None)
        traceback = getattr(event, "traceback", None)
        scheduled_run_time = getattr(event, "scheduled_run_time", None)

        log.error(f"任务 {job_id} 执行失败: {exception!s}")
        if traceback:
            log.debug(f"任务 {job_id} 错误堆栈: {traceback}")
        if scheduled_run_time:
            log.debug(f"任务 {job_id} 计划执行时间: {scheduled_run_time}")

        # 更新执行日志
        cls._update_latest_job_log(
            job_id=job_id,
            status="failed",
            result="failed",
            error=str(exception) if exception else "未知错误",
        )

    @classmethod
    def _handle_job_missed(cls, event: JobEvent) -> None:
        """
        处理任务错过执行时间事件
        """
        job_id = str(event.job_id)
        job = cls.get_job(job_id=job_id)

        log.warning(f"任务 {job_id} 错过执行时间")
        if job:
            log.debug(f"任务 {job_id} ({job.name}) 错过执行")

        # 更新执行日志
        cls._update_latest_job_log(
            job_id=job_id,
            status="timeout",
            result="timeout",
            error="任务错过执行时间",
        )

    @classmethod
    def _handle_job_removed(cls, event: JobEvent) -> None:
        """
        处理任务被移除事件
        """
        job_id = str(event.job_id)
        jobstore = getattr(event, "jobstore", "unknown")

        log.info(f"任务 {job_id} 从 {jobstore} 存储器中移除")

        # 更新执行日志
        cls._update_job_log_on_removed(job_id=job_id)

    @classmethod
    def _handle_job_added(cls, event: JobEvent) -> None:
        """
        处理任务添加事件
        """
        job_id = str(event.job_id)
        jobstore = event.jobstore
        job = cls.get_job(job_id=job_id)

        if job:
            log.info(f"任务 {job_id} ({job.name}) 已添加到 {jobstore} 存储器")
        else:
            log.info(f"任务 {job_id} 已添加到 {jobstore} 存储器")

    @classmethod
    def _handle_job_modified(cls, event: JobEvent) -> None:
        """
        处理任务修改事件
        """
        job_id = str(event.job_id)
        jobstore = event.jobstore
        job = cls.get_job(job_id=job_id)

        if job:
            log.info(f"任务 {job_id} ({job.name}) 已在 {jobstore} 存储器中修改")
        else:
            log.info(f"任务 {job_id} 已在 {jobstore} 存储器中修改")

    @classmethod
    def _handle_scheduler_started(cls, event: SchedulerEvent) -> None:
        """
        处理调度器启动事件
        """
        log.info("调度器已启动")
        cls._update_scheduler_status("running")

    @classmethod
    def _handle_scheduler_shutdown(cls, event: SchedulerEvent) -> None:
        """
        处理调度器关闭事件
        """
        log.info("调度器已关闭")
        cls._update_scheduler_status("stopped")

    @classmethod
    def _handle_scheduler_paused(cls, event: SchedulerEvent) -> None:
        """
        处理调度器暂停事件
        """
        log.info("调度器已暂停")
        cls._update_scheduler_status("paused")

    @classmethod
    def _handle_scheduler_resumed(cls, event: SchedulerEvent) -> None:
        """
        处理调度器恢复事件
        """
        log.info("调度器已恢复运行")
        cls._update_scheduler_status("running")

    @classmethod
    def _handle_executor_added(cls, event: SchedulerEvent) -> None:
        """
        处理执行器添加事件
        """
        alias = event.alias
        if alias:
            log.info(f"执行器 {alias} 已添加到调度器")
            cls._update_executor_info(alias, "added")
        else:
            log.warning("执行器添加事件，但别名为空")

    @classmethod
    def _handle_executor_removed(cls, event: SchedulerEvent) -> None:
        """
        处理执行器移除事件
        """
        alias = event.alias
        if alias:
            log.info(f"执行器 {alias} 已从调度器中移除")
            cls._update_executor_info(alias, "removed")
        else:
            log.warning("执行器移除事件，但别名为空")

    @classmethod
    def _handle_jobstore_added(cls, event: SchedulerEvent) -> None:
        """
        处理 JobStore 添加事件
        """
        alias = event.alias
        if alias:
            log.info(f"JobStore {alias} 已添加到调度器")
            cls._update_jobstore_info(alias, "added")
        else:
            log.warning("JobStore 添加事件，但别名为空")

    @classmethod
    def _handle_jobstore_removed(cls, event: SchedulerEvent) -> None:
        """
        处理 JobStore 移除事件
        """
        alias = event.alias
        if alias:
            log.info(f"JobStore {alias} 已从调度器中移除")
            cls._update_jobstore_info(alias, "removed")
        else:
            log.warning("JobStore 移除事件，但别名为空")

    @classmethod
    def _handle_all_jobs_removed(cls, event: SchedulerEvent) -> None:
        """
        处理所有任务移除事件
        """
        log.info("所有任务已从调度器中移除")
        cls._clear_all_job_logs()

    @classmethod
    def _handle_job_max_instances(cls, event: JobEvent) -> None:
        """
        处理任务达到最大实例数事件
        """
        job_id = str(event.job_id)
        log.warning(f"任务 {job_id} 已达到最大实例数限制，无法启动新实例")

    @classmethod
    def _handle_other_event(cls, event: SchedulerEvent | JobEvent | JobExecutionEvent | JobSubmissionEvent) -> None:
        """
        处理其他事件
        """
        event_code = event.code
        event_type = type(event).__name__
        log.debug(f"收到未处理的事件: {event_type} (code: {event_code})")

    @classmethod
    def _update_scheduler_status(cls, status: str) -> None:
        """
        更新调度器状态到系统参数

        参数:
        - status (str): 调度器状态 (running/stopped/paused)
        """
        try:
            from sqlalchemy.orm import Session

            from app.api.v1.module_system.params.model import ParamsModel

            with Session(engine) as session:
                param = session.query(ParamsModel).filter(ParamsModel.config_key == "scheduler_status").first()
                if param:
                    param.config_value = status
                else:
                    param = ParamsModel(
                        config_name="调度器状态",
                        config_key="scheduler_status",
                        config_value=status,
                        config_type=True,
                    )
                    session.add(param)
                session.commit()
                log.debug(f"调度器状态已更新: {status}")
        except Exception as e:
            log.error(f"更新调度器状态失败: {e!s}", exc_info=True)

    @classmethod
    def _update_executor_info(cls, alias: str | None, action: str) -> None:
        """
        更新执行器信息到系统参数

        参数:
        - alias (str | None): 执行器别名
        - action (str): 操作 (added/removed)
        """
        if not alias:
            log.warning("执行器别名为空，跳过更新")
            return

        try:
            from sqlalchemy.orm import Session

            from app.api.v1.module_system.params.model import ParamsModel

            key = f"executor_{alias}"
            with Session(engine) as session:
                param = session.query(ParamsModel).filter(ParamsModel.config_key == key).first()
                if action == "added":
                    if param:
                        param.config_value = "active"
                    else:
                        param = ParamsModel(
                            config_name=f"执行器 {alias}",
                            config_key=key,
                            config_value="active",
                            config_type=True,
                        )
                        session.add(param)
                    log.debug(f"执行器 {alias} 已标记为活跃")
                elif action == "removed":
                    if param:
                        param.config_value = "inactive"
                    log.debug(f"执行器 {alias} 已标记为非活跃")
                session.commit()
        except Exception as e:
            log.error(f"更新执行器信息失败: {e!s}", exc_info=True)

    @classmethod
    def _update_jobstore_info(cls, alias: str | None, action: str) -> None:
        """
        更新 JobStore 信息到系统参数

        参数:
        - alias (str | None): JobStore 别名
        - action (str): 操作 (added/removed)
        """
        if not alias:
            log.warning("JobStore 别名为空，跳过更新")
            return

        try:
            from sqlalchemy.orm import Session

            from app.api.v1.module_system.params.model import ParamsModel

            key = f"jobstore_{alias}"
            with Session(engine) as session:
                param = session.query(ParamsModel).filter(ParamsModel.config_key == key).first()
                if action == "added":
                    if param:
                        param.config_value = "active"
                    else:
                        param = ParamsModel(
                            config_name=f"JobStore {alias}",
                            config_key=key,
                            config_value="active",
                            config_type=True,
                        )
                        session.add(param)
                    log.debug(f"JobStore {alias} 已标记为活跃")
                elif action == "removed":
                    if param:
                        param.config_value = "inactive"
                    log.debug(f"JobStore {alias} 已标记为非活跃")
                session.commit()
        except Exception as e:
            log.error(f"更新 JobStore 信息失败: {e!s}", exc_info=True)

    @classmethod
    def _clear_all_job_logs(cls) -> None:
        """
        清空所有任务日志
        """
        try:
            from sqlalchemy.orm import Session

            from app.plugin.module_task.job.model import JobModel

            with Session(engine) as session:
                session.query(JobModel).delete()
                session.commit()
                log.info("所有任务日志已清空")
        except Exception as e:
            log.error(f"清空任务日志失败: {e!s}", exc_info=True)

    @classmethod
    def _get_trigger_type(cls, job_id: str) -> str:
        """
        获取任务的触发类型
        """
        job = cls.get_job(job_id=job_id)
        if not job:
            return "manual"
        trigger = job.trigger
        if isinstance(trigger, CronTrigger):
            return "cron"
        elif isinstance(trigger, IntervalTrigger):
            return "interval"
        elif isinstance(trigger, DateTrigger):
            if trigger.run_date:
                now = datetime.now(trigger.run_date.tzinfo)
                diff = abs((trigger.run_date - now).total_seconds())
                if diff < 60:
                    return "manual"
            return "date"
        return "manual"

    @classmethod
    async def init_scheduler(cls, redis: Redis | None = None) -> None:
        """
        应用启动时初始化定时任务。
        """
        if redis:
            cls.redis_instance = redis
        scheduler.start()
        scheduler.add_listener(cls.scheduler_event_listener, EVENT_ALL)
        scheduler.resume()

    @classmethod
    def _task_wrapper(cls, job_id: str | int, code_block: str | None, *args, **kwargs):
        """
        任务执行包装器，执行自定义代码块（同步版本，用于 ThreadPoolExecutor）
        """

        def run_sync_handler():
            if code_block:
                local_vars = {}
                exec(code_block, {"__builtins__": __builtins__}, local_vars)
                handler = local_vars.get("handler")
                if handler and callable(handler):
                    return handler(*args, **kwargs)
                raise ValueError("代码块必须定义 handler(*args, **kwargs) 函数")
            return None

        try:
            result = run_sync_handler()
            return result
        except Exception as e:
            log.error(f"任务 {job_id} 执行失败: {e!s}")
            raise

    @classmethod
    def _get_job_state(cls, job) -> str | None:
        """
        获取任务状态（解析为可读的JSON格式）
        """
        import json
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
                    decoded = pickle.loads(obj)
                    return serialize_value(decoded)
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

        parsed_state = serialize_value(state)
        return json.dumps(parsed_state, ensure_ascii=False, indent=2)

    @classmethod
    def get_job_state_from_blob(cls, blob_data: bytes) -> Any:
        """
        从 BLOB 数据反序列化任务状态

        参数:
        - blob_data: apscheduler_jobs 表中的 job_state 字段（BLOB 类型）

        返回:
        - 反序列化后的任务状态
        """
        import pickle

        if not blob_data:
            return None

        def serialize_value(obj: Any) -> Any:
            if obj is None:
                return None
            if isinstance(obj, (str, int, float, bool)):
                return obj
            if isinstance(obj, bytes):
                try:
                    decoded = pickle.loads(obj)
                    return serialize_value(decoded)
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

        try:
            state = pickle.loads(blob_data)
            return serialize_value(state)
        except Exception as e:
            return {"error": str(e), "raw_data": str(blob_data[:200])}

    @classmethod
    def _create_job_log(cls, job_id: str, job_name: str | None = None, trigger_type: str = "manual", status: str = "running") -> int:
        """
        创建执行日志
        """
        from sqlalchemy.orm import Session

        from app.plugin.module_task.job.model import JobModel

        job = cls.get_job(job_id=job_id)
        next_run_time = str(job.next_run_time) if job and job.next_run_time else None
        job_state = cls._get_job_state(job)

        with Session(engine) as session:
            job_log = JobModel(
                job_id=job_id,
                job_name=job_name,
                trigger_type=trigger_type,
                status=status,
                next_run_time=next_run_time,
                job_state=job_state,
            )
            session.add(job_log)
            session.commit()
            return job_log.id

    @classmethod
    def _update_job_log(cls, job_id: str, status: str, result: str | None = None, error: str | None = None) -> None:
        """
        更新执行日志（更新该 job_id 最新的 pending 或 running 状态日志）
        """
        from sqlalchemy.orm import Session

        from app.plugin.module_task.job.model import JobModel

        job = cls.get_job(job_id=job_id)
        next_run_time = str(job.next_run_time) if job and job.next_run_time else None
        job_state = cls._get_job_state(job)

        with Session(engine) as session:
            job_log = (
                session.query(JobModel)
                .filter(JobModel.job_id == job_id, JobModel.status.in_(['pending', 'running']))
                .order_by(JobModel.created_time.desc())
                .first()
            )
            if job_log:
                job_log.status = status
                if next_run_time:
                    job_log.next_run_time = next_run_time
                if job_state:
                    job_log.job_state = job_state
                if result:
                    job_log.result = result
                if error:
                    job_log.error = error
                session.commit()

    @classmethod
    def _update_latest_job_log(cls, job_id: str, status: str, result: str | None = None, error: str | None = None) -> None:
        """
        更新最新的执行日志（更新该 job_id 最新的一条 running 状态日志）
        用于每次执行完成后更新状态
        """
        from sqlalchemy.orm import Session

        from app.plugin.module_task.job.model import JobModel

        job = cls.get_job(job_id=job_id)
        next_run_time = str(job.next_run_time) if job and job.next_run_time else None
        job_state = cls._get_job_state(job)

        with Session(engine) as session:
            job_log = (
                session.query(JobModel)
                .filter(JobModel.job_id == job_id, JobModel.status == "running")
                .order_by(JobModel.created_time.desc())
                .first()
            )
            if job_log:
                job_log.status = status
                if next_run_time:
                    job_log.next_run_time = next_run_time
                if job_state:
                    job_log.job_state = job_state
                if result:
                    job_log.result = result
                if error:
                    job_log.error = error
                session.commit()

    @classmethod
    def _update_job_log_on_removed(cls, job_id: str) -> None:
        """
        任务被移除时，更新最新的 pending 状态日志为 cancelled
        注意：
        - 只有当任务还在 pending 状态时才更新为 cancelled
        - 一次性任务（trigger_type 为 date 或 manual）执行后会自动触发 REMOVED 事件，此时不应该标记为 cancelled
        - REMOVED 事件可能在 SUBMITTED 之前触发，此时状态还是 pending
        """
        from sqlalchemy.orm import Session

        from app.plugin.module_task.job.model import JobModel

        with Session(engine) as session:
            job_log = (
                session.query(JobModel)
                .filter(JobModel.job_id == job_id, JobModel.status == "pending")
                .order_by(JobModel.created_time.desc())
                .first()
            )
            if job_log:
                if job_log.trigger_type in ("date", "manual"):
                    return
                job_log.status = "cancelled"
                session.commit()

    @classmethod
    def get_job_status(cls, job_id: str | int) -> str:
        """
        获取单个任务的当前状态。
        """
        job = cls.get_job(job_id=str(job_id))
        if not job:
            return "未知"

        if job_id in scheduler._jobstores[job._jobstore_alias]._paused_jobs:
            return "暂停中"

        if scheduler.state == 0:
            return "已停止"

        return "运行中"

    @classmethod
    def add_and_run_job_now(cls, job_info: NodeModel) -> Job:
        """
        立即执行任务（添加到调度器并立即运行）
        """
        trigger = DateTrigger(run_date=datetime.now())
        return cls._add_job_with_trigger(job_info, trigger)

    @classmethod
    def add_cron_job(
        cls,
        job_info: NodeModel,
        trigger_args: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Job:
        """
        创建Cron定时任务

        参数:
        - job_info: 任务信息
        - trigger_args: Cron表达式
        - start_date: 开始时间
        - end_date: 结束时间
        """
        cron_expr = trigger_args or job_info.trigger_args
        if not cron_expr:
            raise ValueError("Cron触发器缺少参数")

        fields = cron_expr.strip().split()
        if len(fields) not in (6, 7):
            raise ValueError("无效的 Cron 表达式")
        if not CronUtil.validate_cron_expression(cron_expr):
            raise ValueError(f"Cron表达式不正确: {cron_expr}")

        parsed_fields = [field if field != "?" else "*" for field in fields]
        if len(fields) == 6:
            parsed_fields.append("*")

        second, minute, hour, day, month, day_of_week, year = tuple(parsed_fields)

        if second == "*" and minute == "*" and hour == "*" and day == "*" and month == "*" and day_of_week in ("*", "?"):
            raise ValueError("Cron表达式不允许每秒执行，请至少指定秒数（如：0 * * * * ? * 表示每分钟执行）")

        trigger = CronTrigger(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            year=year,
            start_date=start_date or job_info.start_date,
            end_date=end_date or job_info.end_date,
            timezone="Asia/Shanghai",
        )
        return cls._add_job_with_trigger(job_info, trigger)

    @classmethod
    def add_interval_job(
        cls,
        job_info: NodeModel,
        trigger_args: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Job:
        """
        创建间隔执行任务

        参数:
        - job_info: 任务信息
        - trigger_args: 间隔参数 (秒 分 时 天 周)
        - start_date: 开始时间
        - end_date: 结束时间
        """
        interval_args = trigger_args or job_info.trigger_args
        if not interval_args:
            raise ValueError("interval触发器缺少参数")

        fields = interval_args.strip().split()
        if len(fields) != 5:
            raise ValueError("无效的 interval 表达式，格式: 秒 分 时 天 周")

        second, minute, hour, day, week = tuple(
            int(field) if field != "*" else 0 for field in fields
        )
        trigger = IntervalTrigger(
            weeks=week,
            days=day,
            hours=hour,
            minutes=minute,
            seconds=second,
            start_date=start_date or job_info.start_date,
            end_date=end_date or job_info.end_date,
            timezone="Asia/Shanghai",
        )
        return cls._add_job_with_trigger(job_info, trigger)

    @classmethod
    def add_date_job(cls, job_info: NodeModel, run_date: str | None = None) -> Job:
        """
        创建指定时间执行任务

        参数:
        - job_info: 任务信息
        - run_date: 执行时间
        """
        date_str = run_date or job_info.trigger_args
        if not date_str:
            raise ValueError("date触发器缺少执行时间参数")

        trigger = DateTrigger(run_date=date_str, timezone="Asia/Shanghai")
        return cls._add_job_with_trigger(job_info, trigger)

    @classmethod
    def _add_job_with_trigger(cls, job_info: NodeModel, trigger) -> Job:
        """
        添加任务到调度器
        """
        code_block = job_info.func
        if not code_block or not code_block.strip():
            raise ValueError("任务代码块不能为空")

        jobstore = job_info.jobstore or "sqlalchemy"
        executor = job_info.executor or "threadpool"

        job_args = []
        if job_info.args:
            args_str = str(job_info.args).strip()
            if args_str:
                job_args = [arg.strip() for arg in args_str.split(",") if arg.strip()]

        job_kwargs = {}
        if job_info.kwargs:
            kwargs_str = str(job_info.kwargs).strip()
            if kwargs_str:
                try:
                    job_kwargs = json.loads(kwargs_str)
                except json.JSONDecodeError:
                    raise ValueError(f"关键字参数JSON格式无效: {kwargs_str}")

        try:
            job = scheduler.add_job(
                func=cls._task_wrapper,
                trigger=trigger,
                args=[str(job_info.id), code_block, *job_args],
                kwargs=job_kwargs,
                id=str(job_info.id),
                name=job_info.name,
                coalesce=job_info.coalesce,
                max_instances=1,
                jobstore=jobstore,
                executor=executor,
            )
            log.info(f"任务 {job_info.id} 添加到 {jobstore} 存储器成功")
            return job
        except ConflictingIdError:
            scheduler.remove_job(job_id=str(job_info.id), jobstore=jobstore)
            job = scheduler.add_job(
                func=cls._task_wrapper,
                trigger=trigger,
                args=[str(job_info.id), code_block, *job_args],
                kwargs=job_kwargs,
                id=str(job_info.id),
                name=job_info.name,
                coalesce=job_info.coalesce,
                max_instances=1,
                jobstore=jobstore,
                executor=executor,
            )
            log.info(f"任务 {job_info.id} 已存在，已移除旧任务并重新添加")
            return job

    @classmethod
    def start(cls, paused: bool = False) -> None:
        scheduler.start(paused=paused)

    @classmethod
    async def shutdown(cls, wait: bool = False):
        return scheduler.shutdown(wait=wait)

    @classmethod
    def configure(cls, gconfig: dict | None = None, prefix: str = "apscheduler.", **options) -> None:
        scheduler.configure(gconfig or {}, prefix, **options)

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
    def get_scheduler_state(cls) -> str:
        if scheduler.state == 0:
            return "停止"
        if scheduler.state == 1:
            return "运行中"
        if scheduler.state == 2:
            return "暂停"
        return "未知"

    @classmethod
    def get_job(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        return scheduler.get_job(str(job_id), jobstore)

    @classmethod
    def get_jobs(cls, jobstore: str | None = None) -> list[Job]:
        return scheduler.get_jobs(jobstore)

    @classmethod
    def get_all_jobs(cls) -> list[Job]:
        return scheduler.get_jobs()

    @classmethod
    def remove_job(cls, job_id: str | int, jobstore: str | None = None) -> None:
        scheduler.remove_job(str(job_id), jobstore)

    @classmethod
    def clear_jobs(cls) -> None:
        scheduler.remove_all_jobs()

    @classmethod
    def print_jobs(cls, jobstore: str | None = None) -> str:
        """
        打印调度器任务信息

        参数:
        - jobstore: 存储器别名，None 表示所有存储器

        返回:
        - str: 格式化的任务信息
        """
        import io

        output = io.StringIO()
        scheduler.print_jobs(jobstore=jobstore, out=output)
        return output.getvalue()

    @classmethod
    def sync_jobs_to_db(cls) -> int:
        """
        将调度器中的任务同步到数据库

        返回:
        - int: 同步的任务数量
        """
        from sqlalchemy.orm import Session

        from app.plugin.module_task.job.model import JobModel

        jobs = cls.get_all_jobs()
        sync_count = 0

        with Session(engine) as session:
            for job in jobs:
                existing_log = (
                    session.query(JobModel)
                    .filter(JobModel.job_id == str(job.id), JobModel.status == "pending")
                    .first()
                )
                if not existing_log:
                    job_log = JobModel(
                        job_id=str(job.id),
                        job_name=job.name,
                        trigger_type=cls._get_trigger_type(str(job.id)),
                        status="pending",
                        next_run_time=str(job.next_run_time) if job.next_run_time else None,
                        job_state=cls._get_job_state(job),
                    )
                    session.add(job_log)
                    sync_count += 1
            session.commit()

        return sync_count

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
    def run_job_now(cls, job_id: str | int, jobstore: str | None = None) -> Job | None:
        job = cls.get_job(job_id=job_id, jobstore=jobstore)
        if not job:
            return None
        trigger = DateTrigger(run_date=datetime.now(), timezone="Asia/Shanghai")
        return scheduler.modify_job(str(job_id), jobstore, trigger=trigger)
