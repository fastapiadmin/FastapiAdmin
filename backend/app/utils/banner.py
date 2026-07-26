from app.config.path_conf import BANNER_FILE


def worship() -> str:
    """读取启动 Banner（优先 `banner.txt`）。
    获取地址：https://patorjk.com/software/taag/#p=testall&f=Fire+Font-k&t=fastapiadmin%0A&x=none&v=4&h=4&w=80&we=false

    返回:
    - str: banner 文本。
    """
    if BANNER_FILE.exists():
        return BANNER_FILE.read_text(encoding="utf-8")
    return ""
