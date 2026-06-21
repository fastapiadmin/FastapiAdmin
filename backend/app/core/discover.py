"""
简化的动态路由发现与注册。

目录与命名规范（不满足则无法注册或导入失败）：
- 插件必须放在 ``app/plugin`` 下，且**顶级目录名**必须以 ``module_`` 开头，例如
  ``module_example``、``module_yourfeature``（扫描模式：``module_*/**/controller.py``）。
- 控制器文件名必须为 ``controller.py``（大小写敏感，Linux 上 ``Controller.py`` 无效）。
- 从 ``module_xxx`` 到 ``controller.py`` 的**每一级目录名**须为合法 Python 标识符
  （仅字母数字下划线、不以数字开头；不要使用中划线、空格、中文目录名等）。
- 每一级目录应可作为包导入：通常需有 ``__init__.py``（或符合 namespace package 规则）。
- 在 ``controller.py`` 的**模块顶层**定义 ``APIRouter`` 实例并赋值给变量
  （如 ``DemoRouter = APIRouter(...)``）；定义在函数内部的 router **不会被**扫描到。

路由前缀：顶级目录 ``module_xxx`` 映射为容器前缀 ``/xxx``（去掉前缀 ``module_`` 共 7 个字符）。

常见「路由没注册」原因：
- 目录不叫 ``module_*``，或 ``controller.py`` 不在该树下的任意子路径中。
- 包无法导入：缺 ``__init__.py``、目录名非法、拼写不一致。
- ``controller.py`` 无语法错误但模块内没有任何顶层 ``APIRouter`` 变量。
"""

# 标准库导入
import importlib
import sys
from pathlib import Path

# 第三方库导入
from fastapi import APIRouter, Depends
from fastapi import FastAPI as _FastAPI

# 内部库导入
from app.core.logger import logger

# 模块级缓存：最近一次构建的动态路由实例
_dynamic_router_cache: APIRouter | None = None
# 记录最近一次注册到 app 的插件路径前缀，用于热重载时精准移除
_registered_plugin_prefixes: set[str] = set()
# 运行时引用，由 init_app.py 设置
_app_ref: _FastAPI | None = None


def set_app_ref(app: _FastAPI) -> None:
    """由 init_app.py 在 app 创建后调用，存储引用供热重载使用。"""
    global _app_ref
    _app_ref = app


def _build_dynamic_router() -> APIRouter:
    """实际执行扫描，返回新的动态路由 APIRouter 实例。"""
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
                logger.error(
                    f"❌ 跳过异常顶级目录名（须为 module_ 前缀且后面还有名称）: {top_module!r}，"
                    f"文件: {file}"
                )
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
                        f"   原因：该文件中未找到**顶层** APIRouter 实例。\n"
                        f"   规范：在 controller.py 模块顶层定义，例如 "
                        f"`XxxRouter = APIRouter(route_class=..., prefix=..., tags=[...])`，"
                        f"不要仅在函数内创建 APIRouter。"
                    )

            except Exception as e:
                hint = _import_failure_hint(e)
                logger.error(f"❌ 处理模块失败: {module_path}\n   {hint}\n   异常: {e!s}")

        for prefix, container_router in sorted(container_routers.items()):
            route_count = len(container_router.routes)
            root_router.include_router(container_router)
            if route_count == 0:
                logger.warning(
                    f"⚠️ 容器前缀 {prefix} 下未挂载任何子路由（可能该 module 下所有 controller 均未导出 APIRouter）"
                )
            logger.info(f"✅ 注册容器: {prefix} (子路由数: {route_count})")

        # 记录本次注册的所有插件前缀，供热重载时精准移除
        global _registered_plugin_prefixes
        _registered_plugin_prefixes = set(container_routers.keys())

        logger.info(f"✅ 动态路由发现完成: 共 {len(container_routers)} 个容器前缀")
        return root_router

    except Exception as e:
        logger.error(f"❌ 动态路由发现整体失败: {e!s}")
        return root_router


def get_dynamic_router() -> APIRouter:
    """
    获取动态路由实例（带缓存）。

    返回:
    - APIRouter: 包含所有动态路由的根路由实例
    """
    global _dynamic_router_cache
    if _dynamic_router_cache is None:
        _dynamic_router_cache = _build_dynamic_router()
    return _dynamic_router_cache


def reload_dynamic_router() -> APIRouter:
    """
    清除插件模块缓存并重新扫描，同时更新已挂载到 FastAPI app 的路由。

    工作机制：
    1. 根据 _registered_plugin_prefixes 精准移除 app.routes 中已注册的插件路由
    2. 清除 sys.modules 中缓存的插件模块
    3. 重新扫描并构建新的动态路由
    4. 将新路由挂载回 app（include_router）

    要求：init_app.py 在创建 app 后调用 discover.set_app_ref(app)，
    否则路由重载仅重建 Router 对象，不会更新运行中的 app。

    返回:
    - APIRouter: 重新构建后的动态路由实例
    """
    global _dynamic_router_cache, _registered_plugin_prefixes, _app_ref

    app = _app_ref
    rate_deps = []

    # ── 1. 从运行中的 app 移除旧的插件路由 ──
    if app and _registered_plugin_prefixes:
        before = len(app.routes)
        app.routes = [
            r for r in app.routes
            if not any(
                getattr(r, "path", "").startswith(p)
                for p in _registered_plugin_prefixes
            )
        ]
        removed = before - len(app.routes)
        logger.info(f"🧹 已移除 {removed} 条旧插件路由（前缀: {_registered_plugin_prefixes}）")
    elif not app:
        logger.warning("⚠️ _app_ref 未设置，无法更新运行中的 app 路由；请确认 init_app.py 已调用 discover.set_app_ref(app)")

    # ── 2. 清除插件模块缓存，迫使 importlib 重新执行模块代码 ──
    _purge_plugin_modules()

    # ── 3. 将新路由挂载回 app ──
    if app:
        # 构造与 init_app.py 中相同的依赖项
        app.include_router(_build_dynamic_router())
        logger.info("✅ 新插件路由已挂载到运行中的 app")

    logger.info("✅ 插件动态路由热重载完成")
    return _build_dynamic_router()


def _purge_plugin_modules() -> None:
    """
    从 sys.modules 中清除所有 app.plugin.module_* 模块，
    使下一次 importlib.import_module 时重新执行模块代码。
    """
    prefix = "app.plugin.module_"
    purged: list[str] = []
    for mod_name in list(sys.modules):
        if mod_name.startswith(prefix):
            del sys.modules[mod_name]
            purged.append(mod_name)

    if purged:
        logger.info(f"🧹 已清除 {len(purged)} 个插件模块缓存，将重新导入")
    else:
        logger.info("🧹 未发现需要清除的插件模块缓存")


def _import_failure_hint(exc: BaseException) -> str:
    """根据异常类型给出简短排查提示（中文日志）。"""
    if isinstance(exc, ModuleNotFoundError):
        missing = getattr(exc, "name", None) or str(exc)
        return (
            f"无法解析模块（ModuleNotFoundError: {missing}）。"
            "常见原因：① 从 app.plugin 到 controller 的某级目录缺少 __init__.py；"
            "② 目录名不是合法 Python 标识符（禁用连字符、空格、中文等）；"
            "③ 磁盘路径与 import 路径不一致（大小写、子目录名拼写）。"
        )
    if isinstance(exc, ImportError):
        return (
            "导入失败（ImportError）。常见原因：controller 或其依赖模块循环导入、"
            "第三方依赖未安装、或相对导入路径错误。"
        )
    if isinstance(exc, SyntaxError):
        return f"controller.py 存在语法错误：{exc.msg}（约第 {exc.lineno} 行）。"
    if isinstance(exc, PermissionError):
        return (
            "权限错误（PermissionError）。多见于受限环境（沙箱、部分 CI）："
            "import 链上某模块初始化时调用了被禁止的系统能力（如进程池），与目录命名无关。"
            "在完整操作系统下重试；若仍失败再结合堆栈排查。"
        )
    return (
        f"未分类异常（{type(exc).__name__}）。请查看下方堆栈；"
        "若与命名/包结构无关，可能是 controller 顶层 import 的依赖在加载时失败。"
    )


# 重新导出函数供外部使用
__all__ = ["get_dynamic_router", "reload_dynamic_router"]
