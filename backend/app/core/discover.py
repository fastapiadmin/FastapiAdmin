# -*- coding: utf-8 -*-
"""
集中式路由发现与注册

约定：
- 仅扫描 `app.api.v1` 包内，顶级目录以 `module_` 开头的模块。
- 在各模块任意子目录下的 `controller.py` 中定义的 `APIRouter` 实例会自动被注册。
- 顶级目录 `module_xxx` 会映射为容器路由前缀 `/<xxx>`。

设计目标：
- 稳定、可预测：有序扫描与注册，确定性日志输出。
- 简洁、易维护：职责拆分成小函数，类型提示与清晰注释。
- 安全、可控：去重处理、异常分层记录、可配置的前缀映射与忽略规则。
- 灵活、可扩展：基于类的设计，支持配置自定义和实例化多套路由系统。
"""

from __future__ import annotations

import importlib
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, Any
from functools import wraps
from fastapi import APIRouter

from app.core.logger import log


def _log_error_handling(func: Callable) -> Callable:
    """错误处理装饰器，用于统一捕获和记录方法执行过程中的异常"""
    @wraps(func)
    def wrapper(self: 'DiscoverRouter', *args: Any, **kwargs: Any) -> Any:
        method_name = func.__name__
        try:
            return func(self, *args, **kwargs)
        except ModuleNotFoundError as e:
            log.error(f"❌️ 模块未找到 [{method_name}]: {str(e)}")
            raise
        except ImportError as e:
            log.error(f"❌️ 导入错误 [{method_name}]: {str(e)}")
            raise
        except AttributeError as e:
            log.error(f"❌️ 属性错误 [{method_name}]: {str(e)}")
            raise
        except Exception as e:
            log.error(f"❌️ 未知错误 [{method_name}]: {str(e)}")
            # 在调试模式下打印完整堆栈信息
            if getattr(self, 'debug', False):
                import traceback
                log.error(traceback.format_exc())
            raise
    return wrapper


class DiscoverRouter:
    """
    路由自动发现与注册器
    
    提供基于约定的路由自动发现与注册功能，支持自定义配置和灵活扩展。
    """
    
    def __init__(
        self,
        module_prefix: str = "module_",
        base_package: str = "app.api.v1",
        prefix_map: dict[str, str] | None = None,
        exclude_dirs: set[str] | None = None,
        exclude_files: set[str] | None = None,
        auto_discover: bool = True,
        debug: bool = False
    ) -> None:
        """
        初始化路由发现注册器
        
        参数:
        - module_prefix: 模块目录前缀，默认为 "module_"
        - base_package: 基础包名，默认为 "app.api.v1"
        - prefix_map: 前缀映射字典，用于自定义路由前缀
        - exclude_dirs: 排除的目录集合
        - exclude_files: 排除的文件集合
        - auto_discover: 是否在初始化时自动执行发现和注册，默认为 True
        - debug: 是否启用调试模式，在调试模式下会输出更详细的错误信息，默认为 False
        """
        self.module_prefix = module_prefix
        self.base_package = base_package
        self.prefix_map = prefix_map or {}
        self.exclude_dirs = exclude_dirs or set()
        self.exclude_files = exclude_files or set()
        self.debug = debug
        self._router = APIRouter()
        self._seen_router_ids: set[int] = set()
        self._discovery_stats: dict[str, int] = {
            "scanned_files": 0,
            "imported_modules": 0,
            "included_routers": 0,
            "container_count": 0
        }
        
        # 自动执行发现和注册
        if auto_discover:
            self.discover_and_register()
    
    @property
    def router(self) -> APIRouter:
        """获取根路由实例"""
        return self._router
    
    @property
    def discovery_stats(self) -> dict[str, int]:
        """获取路由发现统计信息"""
        return self._discovery_stats.copy()
    
    @_log_error_handling
    def _get_base_dir_and_pkg(self) -> tuple[Path, str]:
        """定位基础包的文件系统路径与包名。

        返回:
        - (Path, str): (包的路径, 包名)
        """
        base_pkg = importlib.import_module(self.base_package)
        base_dir = Path(next(iter(base_pkg.__path__)))
        log.info(f"📁 基础包路径: {base_dir}, 包名: {base_pkg.__name__}")
        return base_dir, base_pkg.__name__
    
    def _iter_controller_files(self, base_dir: Path) -> Iterable[Path]:
        """递归查找并返回所有 `controller.py` 文件，按路径排序保证确定性。"""
        try:
            files = sorted(base_dir.rglob("controller.py"), key=lambda p: p.as_posix())
            log.info(f"🔍 发现 {len(files)} 个控制器文件")
            return files
        except PermissionError as e:
            log.error(f"❌️ 权限错误: 无法访问目录 {base_dir}: {str(e)}")
            return []
        except Exception as e:
            log.error(f"❌️ 查找控制器文件失败: {str(e)}")
            return []
    
    def _resolve_prefix(self, top_module: str) -> str | None:
        """将顶级模块目录名解析为容器前缀。"""
        if top_module in self.exclude_dirs:
            if self.debug:
                log.warning(f"⚠️ 目录 {top_module} 被排除")
            return None
        if not top_module.startswith(self.module_prefix):
            if self.debug:
                log.warning(f"⚠️ 目录 {top_module} 不符合前缀约定 {self.module_prefix}")
            return None
        
        mapped = self.prefix_map.get(top_module)
        if mapped:
            log.info(f"🔄 模块 {top_module} 映射到前缀 {mapped}")
            return mapped
        
        prefix = f"/{top_module[len(self.module_prefix):]}"
        if self.debug:
            log.debug(f"📋 模块 {top_module} 使用默认前缀 {prefix}")
        return prefix
    
    @_log_error_handling
    def _include_module_routers(self, mod: object, container: APIRouter) -> int:
        """将模块中的所有 `APIRouter` 实例包含到指定容器路由中。

        返回:
        - int: 新增注册的路由数量
        """
        from fastapi import APIRouter as _APIRouter

        added = 0
        mod_name = getattr(mod, "__name__", "<unknown>")
        router_count = 0
        
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name, None)
            if isinstance(attr, _APIRouter):
                router_count += 1
                rid = id(attr)
                if rid in self._seen_router_ids:
                    log.warning(f"⚠️ 路由 {attr_name} 在模块 {mod_name} 中已注册，跳过重复注册")
                    continue
                
                self._seen_router_ids.add(rid)
                container.include_router(attr)
                added += 1
                log.info(f"➕ 注册路由 {attr_name} 到容器")
        
        if router_count == 0:
            log.warning(f"⚠️ 模块 {mod_name} 中未发现 APIRouter 实例")
        
        return added
    
    @_log_error_handling
    def discover_and_register(self) -> dict[str, int]:
        """
        执行路由发现与注册
        
        返回:
        - dict[str, int]: 包含发现统计信息的字典
            - scanned_files: 扫描的文件数量
            - imported_modules: 导入的模块数量
            - included_routers: 注册的路由数量
            - container_count: 容器数量
        """
        log.info("🚀 开始路由发现与注册...")
        base_dir, base_pkg = self._get_base_dir_and_pkg()
        containers: dict[str, APIRouter] = {}
        container_counts: dict[str, int] = {}

        scanned_files = 0
        imported_modules = 0
        included_routers = 0

        try:
            for file in self._iter_controller_files(base_dir):
                rel_path = file.relative_to(base_dir).as_posix()
                scanned_files += 1

                if rel_path in self.exclude_files:
                    log.warning(f"⚠️ 文件 {rel_path} 被排除")
                    continue

                parts = file.relative_to(base_dir).parts
                if len(parts) < 2:
                    log.warning(f"⚠️ 文件路径不完整: {rel_path}，跳过")
                    continue

                top_module = parts[0]
                prefix = self._resolve_prefix(top_module)
                if not prefix:
                    continue

                # 拼接模块导入路径
                mod_path = ".".join((base_pkg,) + tuple(parts[:-1]) + ("controller",))
                try:
                    mod = importlib.import_module(mod_path)
                    imported_modules += 1
                    log.info(f"📥 导入模块: {mod_path}")
                except ModuleNotFoundError:
                    log.error(f"❌️ 未找到控制器模块: {mod_path}")
                    continue
                except ImportError as e:
                    log.error(f"❌️ 导入控制器失败: {mod_path} -> {str(e)}")
                    continue

                container = containers.setdefault(prefix, APIRouter(prefix=prefix))
                try:
                    added = self._include_module_routers(mod, container)
                    included_routers += added
                    container_counts[prefix] = container_counts.get(prefix, 0) + added
                except Exception as e:
                    log.error(f"❌️ 注册控制器路由失败: {mod_path} -> {str(e)}")

            # 将容器路由按前缀名称排序后注册到根路由，保证顺序稳定
            for prefix in sorted(containers.keys()):
                container = containers[prefix]
                rid = id(container)
                if rid in self._seen_router_ids:
                    continue
                self._seen_router_ids.add(rid)
                self._router.include_router(container)
                # 更丰富的注册日志（含路由数量）
                count = container_counts.get(prefix, 0)
                log.info(f"✅️ 已注册模块容器: {prefix} (路由数: {count})")

            # 更新统计信息
            stats = {
                "scanned_files": scanned_files,
                "imported_modules": imported_modules,
                "included_routers": included_routers,
                "container_count": len(containers)
            }
            self._discovery_stats = stats

            # 生成总结日志
            log.info(
                (
                    f"✅️ 路由发现完成: 扫描文件 {scanned_files}, "
                    f"导入模块 {imported_modules}, 注册路由 {included_routers}, "
                    f"容器 {len(containers)}"
                )
            )
            
            return stats
        except Exception as e:
            log.error(f"❌️ 路由发现与注册过程失败: {str(e)}")
            # 确保返回统计信息，即使过程中出错
            return self._discovery_stats
    
    def set_debug(self, debug: bool) -> 'DiscoverRouter':
        """设置调试模式
        
        参数:
        - debug: 是否开启调试模式
        
        返回:
        - self: 支持链式调用
        """
        self.debug = debug
        log_level = "DEBUG" if debug else "INFO"
        log.info(f"⚙️ 调试模式已{'开启' if debug else '关闭'}，日志级别: {log_level}")
        return self
    
    def add_exclude_dir(self, dir_name: str) -> 'DiscoverRouter':
        """添加排除的目录
        
        参数:
        - dir_name: 要排除的目录名称
        
        返回:
        - self: 支持链式调用
        """
        self.exclude_dirs.add(dir_name)
        log.info(f"📝 添加排除目录: {dir_name}")
        return self
    
    def add_prefix_map(self, module_name: str, prefix: str) -> 'DiscoverRouter':
        """添加前缀映射
        
        参数:
        - module_name: 模块名称
        - prefix: 对应的路由前缀
        
        返回:
        - self: 支持链式调用
        """
        self.prefix_map[module_name] = prefix
        log.info(f"📝 添加前缀映射: {module_name} -> {prefix}")
        return self
    
    @_log_error_handling
    def register_router(self, router: APIRouter, tags: list[str | Enum] | None = None) -> None:
        """手动注册一个路由实例
        
        参数:
        - router: 要注册的 APIRouter 实例
        - tags: 路由标签，用于 API 文档分组
        """
        rid = id(router)
        if rid not in self._seen_router_ids:
            self._seen_router_ids.add(rid)
            self._router.include_router(router, tags=tags)
            log.info(f"📌 手动注册路由，标签: {tags}")
        else:
            log.warning(f"⚠️ 路由已存在，跳过重复注册")


# 创建默认实例并执行自动发现注册
_discoverer = DiscoverRouter()

# 保持向后兼容，导出原始的 router 变量
router = _discoverer.router

# 导出 DiscoverRouter 类供外部使用
__all__ = ["DiscoverRouter", "router"]


# 执行自动发现注册（已由 DiscoverRouter 实例内部处理）