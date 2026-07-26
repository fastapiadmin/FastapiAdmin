"""简化的动态路由发现与注册。

目录与命名规范：
- 插件放在 ``app/plugin`` 下，顶级目录名以 ``module_`` 开头（如 ``module_example``）。
- 控制器文件必须为 ``controller.py``。
- 从 ``module_xxx`` 到 ``controller.py`` 的每级目录名须为合法 Python 标识符。
- 每级目录应有 ``__init__.py``（或符合 namespace package 规则）。
- 在 ``controller.py`` 模块顶层定义 ``APIRouter`` 实例并赋值给变量。

路由前缀：``module_xxx`` 映射为 ``/xxx``。
"""

import importlib
from pathlib import Path

from fastapi import APIRouter, FastAPI

from app.core.logger import logger


class DynamicRouterRegistry:
    """动态路由注册器，管理插件路由的扫描与注册。"""

    def __init__(self) -> None:
        self._cache: APIRouter | None = None

    def init_app(self, app: FastAPI) -> "DynamicRouterRegistry":
        """构建动态路由、注册到 app——返回 self 支持链式调用。"""
        router = self._build()
        app.include_router(router)
        return self

    def _build(self) -> APIRouter:
        """扫描并构建动态路由（带缓存）。"""
        if self._cache is not None:
            return self._cache

        logger.info("🚀 开始动态路由发现与注册")

        root_router = APIRouter()
        seen_router_ids: set[int] = set()
        try:
            base_package = importlib.import_module("app.plugin")
            base_dir = Path(next(iter(base_package.__path__)))

            controller_files = list(base_dir.glob("module_*/**/controller.py"))
            controller_files.sort()

            container_routers: dict[str, APIRouter] = {}

            for file in controller_files:
                rel_path = file.relative_to(base_dir)
                path_parts = rel_path.parts
                top_module = path_parts[0]

                suffix = top_module[7:] if top_module.startswith("module_") else ""
                if not suffix:
                    logger.error(f"❌ 跳过异常顶级目录名（须为 module_ 前缀）: {top_module!r}，文件: {file}")
                    continue
                prefix = f"/{suffix}"

                if prefix not in container_routers:
                    container_routers[prefix] = APIRouter(prefix=prefix)
                container_router = container_routers[prefix]

                module_path = f"app.plugin.{'.'.join(path_parts[:-1])}.controller"
                try:
                    module = importlib.import_module(module_path)
                    registered_here = 0
                    for attr_name in dir(module):
                        attr_value = getattr(module, attr_name, None)
                        if isinstance(attr_value, APIRouter):
                            router_id = id(attr_value)
                            if router_id not in seen_router_ids:
                                seen_router_ids.add(router_id)
                                container_router.include_router(attr_value)
                                registered_here += 1
                                logger.info(f"  ↳ 注册 APIRouter 变量 `{attr_name}` ← {module_path}")

                    if registered_here == 0:
                        logger.warning(
                            f"⚠️ 模块已加载但未注册任何路由: {module_path}\n"
                            f"   文件中未找到顶层 APIRouter 实例",
                        )

                except Exception as e:
                    hint = _import_failure_hint(e)
                    logger.error(f"❌ 处理模块失败: {module_path}\n   {hint}\n   异常: {e!s}")

            for prefix, container_router in sorted(container_routers.items()):
                route_count = len(container_router.routes)
                root_router.include_router(container_router)
                if route_count == 0:
                    logger.warning(f"⚠️ 容器前缀 {prefix} 下未挂载任何子路由")
                logger.info(f"✅ 注册容器: {prefix} (子路由数: {route_count})")

            logger.info(f"✅ 动态路由发现完成: 共 {len(container_routers)} 个容器前缀")
            self._cache = root_router
            return root_router

        except Exception as e:
            logger.error(f"❌ 动态路由发现整体失败: {e!s}")
            return root_router


# 模块级单例
dynamic_router = DynamicRouterRegistry()


def _import_failure_hint(exc: BaseException) -> str:
    """根据异常类型给出简短排查提示。"""
    if isinstance(exc, ModuleNotFoundError):
        missing = getattr(exc, "name", None) or str(exc)
        return (
            f"无法解析模块（ModuleNotFoundError: {missing}）。"
            "常见原因："
            "① 从 app.plugin 到 controller 的某级目录缺少 __init__.py;"
            "② 目录名不是合法 Python 标识符；"
            "③ 磁盘路径与 import 路径不一致。"
        )
    if isinstance(exc, ImportError):
        return "导入失败（ImportError），常见原因：循环导入、依赖未安装、或相对导入路径错误。"
    if isinstance(exc, SyntaxError):
        return f"controller.py 存在语法错误：{exc.msg}（约第 {exc.lineno} 行）。"
    if isinstance(exc, PermissionError):
        return (
            "权限错误（PermissionError）。多见于受限环境：import 链上某模块初始化时调用了被禁止的系统能力。"
            "在完整操作系统下重试；若仍失败再结合堆栈排查。"
        )
    return f"未分类异常（{type(exc).__name__}）。请查看下方堆栈排查。"
