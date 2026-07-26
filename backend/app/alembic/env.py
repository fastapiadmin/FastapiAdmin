import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.path_conf import ALEMBIC_VERSION_DIR
from app.config.setting import settings
from app.core.base_model import MappedBase
from app.utils.import_util import ImportUtil

# 确保 alembic 版本目录存在
ALEMBIC_VERSION_DIR.mkdir(parents=True, exist_ok=True)

# 清除MappedBase.metadata中的表定义，避免重复注册
if hasattr(MappedBase, "metadata") and MappedBase.metadata.tables:
    print(f"🧹 清除已存在的表定义，当前有 {len(MappedBase.metadata.tables)} 个表")
    # 创建一个新的空metadata对象
    from sqlalchemy import MetaData

    MappedBase.metadata = MetaData()
    print("✅️ 已重置metadata")

# 自动查找所有模型
print("🔍 开始查找模型...")
found_models = ImportUtil.find_models(MappedBase)
print(f"📊 找到 {len(found_models)} 个有效模型")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = MappedBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
alembic_config.set_main_option("sqlalchemy.url", settings.ASYNC_DB_URI)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    返回:
    - None
    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    # 确保URL不为None
    if url is None:
        raise ValueError("数据库URL未正确配置，请检查环境配置文件")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    返回:
    - None
    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    # 确保URL不为None
    if url is None:
        raise ValueError("数据库URL未正确配置，请检查环境配置文件")

    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    def do_run_migrations(connection: Connection) -> None:
        def process_revision_directives(context, revision, directives) -> None:
            script = directives[0]

            # 检查所有操作集是否为空
            all_empty = all(ops.is_empty() for ops in script.upgrade_ops_list)

            if all_empty:
                # 如果没有实际变更，不生成迁移文件
                directives[:] = []
                print("❎️ 未检测到模型变更，不生成迁移文件")
            else:
                print("✅️ 检测到模型变更，生成迁移文件")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            transaction_per_migration=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
