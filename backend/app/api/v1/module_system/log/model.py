from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class OperationLogModel(ModelMixin, UserMixin):
    """
    系统日志模型
    日志类型:
    - 1: 登录日志
    - 2: 操作日志
    """

    __tablename__: str = "sys_log"
    __table_args__: dict[str, str] = {"comment": "系统日志表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    type: Mapped[int] = mapped_column(Integer, comment="日志类型(1登录日志 2操作日志)")
    request_path: Mapped[str] = mapped_column(String(255), comment="请求路径")
    request_method: Mapped[str] = mapped_column(String(10), comment="请求方式")
    request_payload: Mapped[str | None] = mapped_column(Text, comment="请求体")
    request_ip: Mapped[str | None] = mapped_column(String(50), comment="请求IP地址")
    login_location: Mapped[str | None] = mapped_column(String(255), comment="登录位置")
    request_os: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="操作系统")
    request_browser: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="浏览器")
    response_code: Mapped[int] = mapped_column(Integer, comment="响应状态码")
    response_json: Mapped[str | None] = mapped_column(Text, nullable=True, comment="响应体")
    process_time: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="处理时间")
