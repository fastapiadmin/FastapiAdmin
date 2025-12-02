# -*- coding: utf-8 -*-

import os
from typing import Annotated
import uvicorn
import typer
from fastapi import FastAPI
from alembic import command
from alembic.config import Config

from app.common.enums import EnvironmentEnum


fastapiadmin_cli = typer.Typer()

# 初始化 Alembic 配置
alembic_cfg = Config("alembic.ini")


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    from app.plugin.init_app import (
        register_middlewares,
        register_exceptions,
        register_routers,
        register_files,
        reset_api_docs,
        lifespan
    )
    from app.config.setting import settings
    # 创建FastAPI应用
    app = FastAPI(**settings.FASTAPI_CONFIG, lifespan=lifespan)
    
    from app.core.logger import setup_logging
    # 初始化日志
    setup_logging()
    # 注册各种组件
    register_exceptions(app)
    # 注册中间件
    register_middlewares(app)
    # 注册路由
    register_routers(app)
    # 注册静态文件
    register_files(app)
    # 重设API文档
    reset_api_docs(app)

    return app

# typer.Option是非必填；typer.Argument是必填
@fastapiadmin_cli.command(name="run", help="启动 FastapiAdmin 服务, 运行 python main.py run --env=dev 不加参数默认 dev 环境")
def run(env: Annotated[EnvironmentEnum, typer.Option("--env", help="运行环境 (dev, prod)")] = EnvironmentEnum.DEV) -> None:
    """启动FastAPI服务"""

    try:
        # 设置环境变量
        os.environ["ENVIRONMENT"] = env.value
        typer.echo("项目启动中...")
        
        # 清除配置缓存，确保重新加载配置
        from app.config.setting import get_settings
        get_settings.cache_clear()
        settings = get_settings()
        
        from app.core.logger import setup_logging
        setup_logging()

        # 显示启动横幅
        from app.utils.banner import worship
        worship(env.value)
        
        # 启动uvicorn服务
        uvicorn.run(
            app=f'main:create_app', 
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True if env.value == EnvironmentEnum.DEV.value else False,
            factory=True,
            log_config=None
        )
        
    except KeyboardInterrupt:
        from app.utils.console import display_shutdown_info
        display_shutdown_info()
    except Exception as e:
        raise

@fastapiadmin_cli.command(name="revision", help="生成新的 Alembic 迁移脚本, 运行 python main.py revision --env=dev")
def revision(env: Annotated[EnvironmentEnum, typer.Option("--env", help="运行环境 (dev, prod)")] = EnvironmentEnum.DEV) -> None:
    """生成新的 Alembic 迁移脚本"""
    os.environ["ENVIRONMENT"] = env.value
    command.revision(alembic_cfg, autogenerate=True, message="迁移脚本")
    typer.echo(f"迁移脚本已生成")

@fastapiadmin_cli.command(name="upgrade", help="应用最新的 Alembic 迁移, 运行 python main.py upgrade --env=dev")
def upgrade(env: Annotated[EnvironmentEnum, typer.Option("--env", help="运行环境 (dev, prod)")] = EnvironmentEnum.DEV) -> None:
    """应用最新的 Alembic 迁移"""
    os.environ["ENVIRONMENT"] = env.value
    command.upgrade(alembic_cfg, "head")
    typer.echo("所有迁移已应用。")


if __name__ == '__main__':
    
    fastapiadmin_cli()

