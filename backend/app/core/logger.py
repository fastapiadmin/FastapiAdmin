import logging
import sys

from loguru import logger

from app.config.path_conf import LOG_DIR
from app.config.setting import settings
from app.core.request_context import get_correlation_id


def _context_patcher(record: dict) -> None:
    cid = get_correlation_id()
    record["extra"]["ctx"] = f" | cid={cid[:8]}" if cid else ""


class InterceptHandler(logging.Handler):
    """将标准库 logging 重定向到 Loguru"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, "{}", record.getMessage())


def setup_logger() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.configure(patcher=_context_patcher)

    LOG_FMT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
        "{extra[ctx]}"
    )
    logger.add(sys.stdout, format=LOG_FMT, level=settings.LOGGER_LEVEL)
    logger.add(
        str(LOG_DIR / "fastapiadmin.log"),
        format=LOG_FMT,
        level="INFO",
        rotation="00:00",
        retention=30,
        compression="gz",
        encoding="utf-8",
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=settings.LOGGER_LEVEL, force=True)
    for name in [k for k in logging.root.manager.loggerDict if isinstance(k, str)] + ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        std = logging.getLogger(name)
        std.handlers = [InterceptHandler()]
        std.propagate = False


setup_logger()
