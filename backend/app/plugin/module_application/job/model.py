from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin


class JobModel(ModelMixin, UserMixin):
    """
    定时任务调度表
    - 0: 运行中
    - 1: 暂停中
    """

    __tablename__: str = "app_job"
    __table_args__: dict[str, str] = {"comment": "定时任务调度表"}
    __loader_options__: list[str] = ["job_logs", "created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(
        String(64), nullable=True, default="", comment="任务名称"
    )
    jobstore: Mapped[str | None] = mapped_column(
        String(64), nullable=True, default="default", comment="存储器"
    )
    executor: Mapped[str | None] = mapped_column(
        String(64), nullable=True, default="default", comment="执行器"
    )
    trigger: Mapped[str] = mapped_column(String(64), nullable=False, comment="触发器")
    trigger_args: Mapped[str | None] = mapped_column(Text, nullable=True, comment="触发器参数")
    func: Mapped[str] = mapped_column(Text, nullable=False, comment="任务函数")
    args: Mapped[str | None] = mapped_column(Text, nullable=True, comment="位置参数")
    kwargs: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关键字参数")
    coalesce: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        comment="是否合并运行",
    )
    max_instances: Mapped[int] = mapped_column(
        Integer, nullable=True, default=1, comment="最大实例数"
    )
    start_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="开始时间")
    end_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="结束时间")

    # 关联关系
    job_logs: Mapped[list["JobLogModel"] | None] = relationship(
        back_populates="job", lazy="selectin"
    )


class JobLogModel(ModelMixin):
    """
    定时任务调度日志表
    """

    __tablename__: str = "app_job_log"
    __table_args__: dict[str, str] = {"comment": "定时任务调度日志表"}
    __loader_options__: list[str] = ["job"]

    job_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="任务名称")
    job_group: Mapped[str] = mapped_column(String(64), nullable=False, comment="任务组名")
    job_executor: Mapped[str] = mapped_column(String(64), nullable=False, comment="任务执行器")
    invoke_target: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="调用目标字符串"
    )
    job_args: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default="", comment="位置参数"
    )
    job_kwargs: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default="", comment="关键字参数"
    )
    job_trigger: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default="", comment="任务触发器"
    )
    job_message: Mapped[str | None] = mapped_column(
        String(500), nullable=True, default="", comment="日志信息"
    )
    exception_info: Mapped[str | None] = mapped_column(
        String(2000), nullable=True, default="", comment="异常信息"
    )

    # 任务关联
    job_id: Mapped[int | None] = mapped_column(
        ForeignKey("app_job.id", ondelete="CASCADE"), nullable=True, index=True, comment="任务ID"
    )

    job: Mapped["JobModel | None"] = relationship(back_populates="job_logs", lazy="selectin")
