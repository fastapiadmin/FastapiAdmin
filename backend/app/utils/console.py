from datetime import datetime

from rich import box, get_console
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
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
) -> None:
    """在终端输出 Rich 面板：服务信息、组件就绪状态与文档链接。

    参数:
    - host (str): 监听主机。
    - port (int): 监听端口。
    - reload (bool): 是否开启热重载。
    - database_ready (bool | None): 数据库是否就绪。
    - redis_ready (bool | None): Redis 是否就绪。
    - scheduler_ready (bool | None): 调度器是否就绪。

    返回:
    - None
    """
    env_label = settings.ENVIRONMENT.value if hasattr(settings.ENVIRONMENT, 'value') else settings.ENVIRONMENT
    url = f"http://{host}:{port}"
    base_url = f"{url}{settings.ROOT_PATH}"
    docs_url = base_url + settings.DOCS_URL
    frontend_url = base_url + settings.WEB_URL

    def _status_text(ready: bool | None) -> str:
        return "✅ 就绪" if ready else "❌ 失败"

    # 标题
    title_text = Text(f"\n{settings.TITLE} v{settings.VERSION}", style="bold green")

    # 服务信息
    info_grid = Table.grid(padding=(0, 1))
    info_grid.add_column(justify="right")
    info_grid.add_column()
    info_grid.add_row("服务地址", url, style="bold blue")
    info_grid.add_row("运行环境", env_label, style="bold yellow")
    info_grid.add_row("重载配置", "✅ 启动" if reload else "❌ 关闭")

    # 组件状态 — 一行四个，│ 分隔分组
    sep = Text(" │ ", style="dim")
    status_grid = Table.grid(padding=(0, 1))
    status_grid.add_column(justify="right")
    status_grid.add_column()
    status_grid.add_column(justify="right")
    status_grid.add_column()
    status_grid.add_column(justify="right")
    status_grid.add_column()
    status_grid.add_column(justify="right")
    status_grid.add_column()
    status_grid.add_row(
        "MySQL", _status_text(database_ready),
        sep,
        "Redis", _status_text(redis_ready),
        sep,
        "调度器", _status_text(scheduler_ready),
    )

    # 文档链接
    docs_grid = Table.grid(padding=(0, 1))
    docs_grid.add_column(justify="right")
    docs_grid.add_column()
    docs_grid.add_row("Swagger", Text(docs_url, style=f"blue link {docs_url}"))
    docs_grid.add_row("前端", Text(frontend_url, style=f"blue link {frontend_url}"))

    final_content = Group(
        title_text,
        info_grid,
        Rule(style="dim"),
        status_grid,
        Rule(style="dim"),
        docs_grid,
    )

    result = Panel(
        renderable=final_content,
        title=f"[bold purple]🚀 FastapiAdmin v{settings.VERSION}[/]",
        border_style="green",
        box=box.HEAVY,
        padding=(0, 2),
    )

    console.print(result)


def console_end() -> None:
    """在终端输出服务关闭提示面板。

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
