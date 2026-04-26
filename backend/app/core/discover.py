"""
简化的动态路由发现与注册

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
from pathlib import Path

# 第三方库导入
from fastapi import APIRouter

# 内部库导入
from app.core.logger import log


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


def _scan_controllers(
    base_package_name: str,
    base_dir: Path,
    glob_pattern: str,
    module_prefix: str,
    container_routers: dict[str, APIRouter],
    seen_router_ids: set[int],
    root_router: APIRouter,
) -> None:
    """
    扫描指定目录下的 controller 文件并注册路由

    参数:
    - base_package_name: 基础包名 (如 "app.plugin")
    - base_dir: 基础目录路径
    - glob_pattern: glob 匹配模式 (如 "module_*/**/controller.py")
    - module_prefix: 模块导入路径前缀 (如 "app.plugin")
    - container_routers: 容器路由映射
    - seen_router_ids: 已注册的路由ID集合
    - root_router: 根路由实例
    """
    # 查找所有符合条件的controller.py文件
    controller_files = list(base_dir.glob(glob_pattern))

    # 按路径排序，确保注册顺序一致
    controller_files.sort()

    for file in controller_files:
        # 解析文件路径
        rel_path = file.relative_to(base_dir)
        path_parts = rel_path.parts

        # 获取顶级模块名
        top_module = path_parts[0]

        # 生成路由前缀 (module_xxx -> /xxx)
        suffix = top_module[7:] if top_module.startswith("module_") else ""
        if not suffix:
            log.error(
                f"❌ 跳过异常顶级目录名（须为 module_ 前缀且后面还有名称）: {top_module!r}，"
                f"文件: {file}"
            )
            continue
        prefix = f"/{suffix}"

        # 获取或创建容器路由
        if prefix not in container_routers:
            container_routers[prefix] = APIRouter(prefix=prefix)
        container_router = container_routers[prefix]

        # 生成模块导入路径
        module_path = f"{module_prefix}.{'.'.join(path_parts[:-1])}.controller"

        try:
            # 动态导入模块
            module = importlib.import_module(module_path)

            # 查找并注册所有APIRouter实例
            registered_here = 0
            for attr_name in dir(module):
                attr_value = getattr(module, attr_name, None)

                # 只注册APIRouter实例，且避免重复注册
                if isinstance(attr_value, APIRouter):
                    router_id = id(attr_value)
                    if router_id not in seen_router_ids:
                        seen_router_ids.add(router_id)
                        container_router.include_router(attr_value)
                        registered_here += 1
                        log.debug(f"  ↳ 注册 APIRouter 变量 `{attr_name}` ← {module_path}")

            if registered_here == 0:
                log.warning(
                    f"⚠️ 模块已加载但未注册任何路由: {module_path}\n"
                    f"   原因：该文件中未找到**顶层** APIRouter 实例。\n"
                    f"   规范：在 controller.py 模块顶层定义，例如 "
                    f"`XxxRouter = APIRouter(route_class=..., prefix=..., tags=[...])`，"
                    f"不要仅在函数内创建 APIRouter。"
                )

        except Exception as e:
            hint = _import_failure_hint(e)
            log.exception(
                f"❌ 处理模块失败: {module_path}\n   {hint}\n   异常: {e!s}"
            )


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

    # 容器路由映射 {prefix: container_router}
    container_routers: dict[str, APIRouter] = {}

    try:
        # 1. 扫描 app.plugin 目录
        log.info("📂 扫描 app.plugin 目录...")
        base_package = importlib.import_module("app.plugin")
        base_dir = Path(next(iter(base_package.__path__)))
        _scan_controllers(
            base_package_name="app.plugin",
            base_dir=base_dir,
            glob_pattern="module_*/**/controller.py",
            module_prefix="app.plugin",
            container_routers=container_routers,
            seen_router_ids=seen_router_ids,
            root_router=root_router,
        )

        # 2. 扫描 app.api.v1 目录
        log.info("📂 扫描 app.api.v1 目录...")
        api_package = importlib.import_module("app.api.v1")
        api_dir = Path(next(iter(api_package.__path__)))
        _scan_controllers(
            base_package_name="app.api.v1",
            base_dir=api_dir,
            glob_pattern="module_*/**/controller.py",
            module_prefix="app.api.v1",
            container_routers=container_routers,
            seen_router_ids=seen_router_ids,
            root_router=root_router,
        )

        # 将所有容器路由注册到根路由
        for prefix, container_router in sorted(container_routers.items()):
            route_count = len(container_router.routes)
            root_router.include_router(container_router)
            if route_count == 0:
                log.warning(
                    f"⚠️ 容器前缀 {prefix} 下未挂载任何子路由（可能该 module 下所有 controller 均未导出 APIRouter）"
                )
            log.info(f"✅️ 注册容器: {prefix} (子路由数: {route_count})")

        log.info(f"✅️ 动态路由发现完成: 共 {len(container_routers)} 个容器前缀")
        return root_router

    except Exception as e:
        log.exception(f"❌ 动态路由发现整体失败: {e!s}")
        # 如果失败，返回一个空的路由实例
        return root_router


# 重新导出函数供外部使用
__all__ = ["get_dynamic_router"]
