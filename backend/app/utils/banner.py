from app.config.path_conf import BANNER_FILE
from app.core.logger import log


def worship(env: str) -> None:
    """
    获取项目启动Banner（优先读取 banner.txt）
    """
    if BANNER_FILE.exists():
        banner = BANNER_FILE.read_text(encoding="utf-8")
        banner = f"🚀 当前运行环境: {env}\n{banner}"
        log.info(banner)
