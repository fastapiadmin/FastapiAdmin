"""系统日志维护任务的内置处理器。

默认的「日志保留清理」节点以前把 async 清理函数包在 ``asyncio.run`` 里，
但调度器在线程池执行，异步数据库引擎绑定的是主事件循环，会触发
``Future attached to a different loop``。这里改用同步 engine，专供
APScheduler 线程池调用，避免跨事件循环复用 AsyncSession。
"""

from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.database import engine
from app.core.logger import logger
from app.modules.system.log.model import LoginLogModel, OperationLogModel


def cleanup_expired_logs(days: int = 90) -> dict:
    """物理清理过期操作日志/登录日志。

    参数:
    - days (int): 保留天数，必须大于 0。

    返回:
    - dict: 各表清理条数统计。
    """
    days = int(days)
    if days <= 0:
        raise ValueError("日志保留天数必须大于 0")

    cutoff = datetime.now() - timedelta(days=days)
    with Session(engine) as session:
        op_result = session.execute(delete(OperationLogModel).where(OperationLogModel.created_time < cutoff))
        login_result = session.execute(delete(LoginLogModel).where(LoginLogModel.created_time < cutoff))
        session.commit()
        stats = {
            "days": days,
            "operation_deleted": op_result.rowcount or 0,
            "login_deleted": login_result.rowcount or 0,
        }

    logger.info(
        f"日志保留清理完成（保留 {days} 天）: 操作日志 {stats['operation_deleted']} 条，登录日志 {stats['login_deleted']} 条"
    )
    return stats
