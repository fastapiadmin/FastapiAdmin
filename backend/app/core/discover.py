"""
简化的动态路由发现与注册

约定：
- 扫描 `app.plugin` 下所有以 `module_` 开头的顶级目录
- 在各模块任意子目录下的 `controller.py` 中定义的 `APIRouter` 实例会自动被注册
- 顶级目录 `module_xxx` 会映射为容器路由前缀 `/<xxx>`
"""

# 标准库导入
import importlib
from pathlib import Path

# 第三方库导入
from fastapi import APIRouter

# 内部库导入
from app.core.logger import log


def get_dynamic_router() -> APIRouter:
    """
    执行动态路由发现与注册，返回包含所有动态路由的根路由实例

    返回:
    - APIRouter: 包含所有动态路由的根路由实例
    """
    log.info("🚀 开始动态路由发现与注册")

    # 创建根路由实例
    root_router = APIRouter()

    # 已注册的路由ID集合，用于避免重复注册
    seen_router_ids: set[int] = set()

    try:
        # 获取app.plugin包的路径
        base_package = importlib.import_module("app.plugin")
        base_dir = Path(next(iter(base_package.__path__)))

        # 查找所有符合条件的controller.py文件
        # 只扫描module_*目录下的文件
        controller_files = list(base_dir.glob("module_*/**/controller.py"))

        # 按路径排序，确保注册顺序一致
        controller_files.sort()

        # 容器路由映射 {prefix: container_router}
        container_routers: dict[str, APIRouter] = {}

        for file in controller_files:
            # 解析文件路径
            rel_path = file.relative_to(base_dir)
            path_parts = rel_path.parts

            # 获取顶级模块名
            top_module = path_parts[0]

            # 生成路由前缀 (module_xxx -> /xxx)
            prefix = f"/{top_module[7:]}"

            # 获取或创建容器路由
            if prefix not in container_routers:
                container_routers[prefix] = APIRouter(prefix=prefix)
            container_router = container_routers[prefix]

            # 生成模块导入路径
            module_path = f"app.plugin.{'.'.join(path_parts[:-1])}.controller"

            try:
                # 动态导入模块
                module = importlib.import_module(module_path)

                # 查找并注册所有APIRouter实例
                for attr_name in dir(module):
                    attr_value = getattr(module, attr_name, None)

                    # 只注册APIRouter实例，且避免重复注册
                    if isinstance(attr_value, APIRouter):
                        router_id = id(attr_value)
                        if router_id not in seen_router_ids:
                            seen_router_ids.add(router_id)
                            container_router.include_router(attr_value)
                            log.debug(f"📌 注册路由 {attr_name} 到容器 {prefix}")

            except Exception as e:
                log.error(f"❌️ 处理模块 {module_path} 失败: {e!s}")

        # 将所有容器路由注册到根路由
        for prefix, container_router in sorted(container_routers.items()):
            root_router.include_router(container_router)
            log.info(f"✅️ 注册容器: {prefix} (路由数: {len(container_router.routes)})")

        log.info(f"✅️ 动态路由发现完成: 注册了 {len(container_routers)} 个容器路由")
        return root_router

    except Exception as e:
        log.error(f"❌️ 动态路由发现失败: {e!s}")
        # 如果失败，返回一个空的路由实例
        return root_router


# 重新导出函数供外部使用
__all__ = ["get_dynamic_router"]
