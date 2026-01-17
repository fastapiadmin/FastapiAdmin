from datetime import datetime

from rich import get_console
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from app.config.setting import settings

console = get_console()


def console_run(
    host: str,
    port: int,
    reload: bool,
    *,
    redis_ready: bool | None = None,
    scheduler_jobs: int | None = None,
    scheduler_status: str | None = None,
) -> None:
    """显示启动信息面板"""

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
        f"\n重载配置: {'✅ 开启' if reload else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(
        f"\n调试模式: {'✅ 开启' if settings.DEBUG else '❌ 关闭'}",
        style="bold italic",
    )
    service_info.append(f"\n数据库类型: {settings.DATABASE_TYPE} 数据库", style="bold italic")
    service_info.append(
        f"\nRedis: {'✅ 已连接' if redis_ready else '❌ 未连接'}",
        style="bold italic",
    )
    service_info.append(
        f"\n定时任务 {'✅ 运行中' if scheduler_status == 'running' else '⏸️ 暂停'} {scheduler_jobs}",
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


def console_close() -> None:
    """显示关闭信息"""
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
