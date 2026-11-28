"""数据库/Redis 连接串特殊字符转义测试。"""

from sqlalchemy.engine import make_url

from app.config.db_url import build_redis_url
from app.config.setting import Settings


def test_settings_url_handles_password_special_chars() -> None:
    settings = Settings(
        DATABASE_TYPE="mysql",
        DATABASE_USER="user@corp",
        DATABASE_PASSWORD="p@ss!word#1/中文",
        DATABASE_HOST="db.internal",
        DATABASE_PORT=3306,
        DATABASE_NAME="fastapiadmin",
        ENVIRONMENT="dev",
    )
    url = settings.ASYNC_DB_URI
    parsed = make_url(url)
    assert parsed.username == "user@corp"
    assert parsed.password == "p@ss!word#1/中文"
    assert parsed.database == "fastapiadmin"
    assert "%40" in url and "%21" in url


def test_redis_url_handles_password_special_chars() -> None:
    url = build_redis_url(username="", password="p@ss!中文", host="redis", port=6379, db=1)
    assert "%40" in url and "%21" in url
    assert "p@ss!" not in url
