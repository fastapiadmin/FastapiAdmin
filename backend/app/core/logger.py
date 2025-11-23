# -*- coding: utf-8 -*-

import logging
import sys
from typing_extensions import override
from loguru import logger

from app.config.path_conf import LOG_DIR
from app.config.setting import settings


class InterceptHandler(logging.Handler):
    """
    日志拦截处理器：将所有 Python 标准日志重定向到 Loguru
    
    工作原理：
    1. 继承自 logging.Handler
    2. 重写 emit 方法处理日志记录
    3. 将标准库日志转换为 Loguru 格式
    """
    @override
    def emit(self, record: logging.LogRecord) -> None:
        # 尝试获取日志级别名称
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 获取调用帧信息，增加None检查
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # 使用 Loguru 记录日志
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage()
        )
        

def setup_logging():
    """
    配置日志系统
    
    功能：
    1. 控制台彩色输出
    2. 文件日志轮转
    3. 错误日志单独存储
    4. 异步日志记录
    """
    # 添加上下文信息
    _ = logger.configure(extra={"app_name": "FastapiAdmin"})
    # 步骤1：移除默认处理器
    logger.remove()

    # 步骤2：定义日志格式
    log_format = (
        # 时间信息
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        # 日志级别，居中对齐
        "<level>{level: <8}</level> | "
        # 文件、函数和行号
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        # 日志消息
        "<level>{message}</level>"
    )

    # 步骤3：配置控制台输出
    _ = logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else "INFO",
        enqueue=True,        # 启用异步写入
        backtrace=True,      # 显示完整的异常回溯
        diagnose=True,       # 显示变量值等诊断信息
        colorize=True        # 启用彩色输出
    )

    # 步骤4：创建日志目录
    log_dir = LOG_DIR
    # 确保日志目录存在,如果不存在则创建
    log_dir.mkdir(parents=True, exist_ok=True)

    # 步骤5：配置常规日志文件
    _ = logger.add(
        str(log_dir / "info.log"),
        format=log_format,
        level="INFO",
        rotation="00:00",  # 每天午夜轮转
        retention=30,      # 日志保留天数，超过此天数的日志文件将被自动清理
        compression="gz",
        encoding="utf-8",
        enqueue=True
    )

    # 步骤6：配置错误日志文件
    _ = logger.add(
        str(log_dir / "error.log"),
        format=log_format,
        level="ERROR",
        rotation="00:00",  # 每天午夜轮转
        retention=30,      # 日志保留天数，超过此天数的日志文件将被自动清理
        compression="gz",
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

    # 步骤7：配置标准库日志
    logging.basicConfig(handlers=[InterceptHandler()], level="DEBUG" if settings.DEBUG else "INFO", force=True)
    logger_name_list = [name for name in logging.root.manager.loggerDict]
    # 步骤8：配置第三方库日志
    for logger_name in logger_name_list:
        _logger = logging.getLogger(logger_name)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

log = logger