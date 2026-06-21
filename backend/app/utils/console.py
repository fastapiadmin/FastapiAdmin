from datetime import datetime

from rich import get_console
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from app.config.setting import settings

console = get_console()


def console_start(
    host: str,
    port: int,
    reload: bool,
    *,
    database_ready: bool | None = None,
    redis_ready: bool | None = None,
    scheduler_ready: bool | None = None,
    limiter_ready: bool | None = None,
) -> None:
    """
    在终端输出 Rich 面板：服务信息、组件就绪状态与文档链接。

    参数:
    - host (str): 监听主机。
    - port (int): 监听端口。
    - reload (bool): 是否开启热重载。
    - database_ready (bool | None): 数据库是否就绪。
    - redis_ready (bool | None): Redis 是否就绪。
    - scheduler_ready (bool | None): 调度器是否就绪。
    - limiter_ready (bool | None): 限流器是否就绪。

    返回:
    - None
    """

    url = f"http://{host}:{port}"
    base_url = f"{url}{settings.ROOT_PATH}"
    docs_url = base_url + settings.DOCS_URL
    redoc_url = base_url + settings.REDOC_URL

    # 核心服务信息
    service_info = Text()
    service_info.append(f"服务名称 {settings.TITLE} • 优雅 • 简洁 • 高效", style="bold magenta")
    service_info.append(f"\n当前版本 v{settings.VERSION}", style="bold green")
    service_info.append(f"\n服务地址 {url}", style="bold blue")
    service_info.append(
        f"\n运行环境 {settings.ENVIRONMENT.value if hasattr(settings.ENVIRONMENT, 'value') else settings.ENVIRONMENT}",
        style="bold red",
    )
    service_info.append(
        f"\n重载配置: {'✅ 启动' if reload else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\n调试模式: {'✅ 启动' if settings.DEBUG else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\n{settings.DATABASE_TYPE}: {'✅ 启动' if database_ready else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\nRedis: {'✅ 启动' if redis_ready else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\n调度器: {'✅ 启动' if scheduler_ready else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\n限流器: {'✅ 启动' if limiter_ready else '❌ 关闭'}",
        style="bold italic",
    )

    docs_info = Text()
    docs_info.append("📖 文档", style="bold magenta")
    docs_info.append(f"\n🔗 Swagger: {docs_url}", style="blue link")
    docs_info.append(f"\n🔗 ReDoc: {redoc_url}", style="blue link")

    final_content = Group(
        service_info,
        "\n" + "─" * 40,
        docs_info,
    )

    result = Panel(
        renderable=final_content,
        title="[bold purple]🚀 服务启动完成[/]",
        border_style="green",
        padding=(1, 2),
    )

    console.print(result)


def console_end() -> None:
    """
    在终端输出服务关闭提示面板。

    返回:
    - None
    """
    shutdown_content = Text()
    shutdown_content.append("🛑 ", style="bold red")
    shutdown_content.append("FastapiAdmin 服务关闭")
    shutdown_content.append(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
    shutdown_content.append("\n👋 感谢使用！", style="dim")

    result = Panel(
        shutdown_content,
        title="[bold red]服务关闭[/]",
        border_style="red",
        padding=(1, 2),
    )

    console.print(result)
