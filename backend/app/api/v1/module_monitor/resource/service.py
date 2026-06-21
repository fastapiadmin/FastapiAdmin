import ast
import os
import re
import shutil
import urllib.parse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.utils.excel_util import ExcelUtil

from .schema import (
    ResourceCopySchema,
    ResourceCreateDirSchema,
    ResourceDirectorySchema,
    ResourceItemSchema,
    ResourceMoveSchema,
    ResourceRenameSchema,
    ResourceSearchQueryParam,
)


class ResourceService:
    """资源管理模块服务层 - 管理系统静态文件目录（仅管理 upload 目录）"""

    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    MAX_SEARCH_RESULTS = 1000
    MAX_PATH_DEPTH = 20

    @staticmethod
    def _get_resource_root() -> str:
        if not settings.STATIC_ENABLE:
            raise CustomException(msg="静态文件服务未启用")
        resource_root = os.path.join(str(settings.STATIC_ROOT), "upload", "resource")
        os.makedirs(resource_root, exist_ok=True)
        return resource_root

    @staticmethod
    def _get_safe_path(path: str | None = None) -> str:
        resource_root = ResourceService._get_resource_root()

        if not path or not isinstance(path, str):
            return resource_root

        static_prefix = settings.STATIC_URL.rstrip("/")
        root_prefix = settings.ROOT_PATH.rstrip("/") if getattr(settings, "ROOT_PATH", "") else ""
        root_static_prefix = f"{root_prefix}{static_prefix}" if root_prefix else static_prefix

        def strip_prefix(p: str) -> str:
            if p.startswith(root_static_prefix):
                return p[len(root_static_prefix):].lstrip("/")
            if p.startswith(static_prefix):
                return p[len(static_prefix):].lstrip("/")
            return p

        if path.startswith(("http://", "https://")):
            parsed = urlparse(path)
            url_path = parsed.path or ""
            path = strip_prefix(url_path)
        else:
            path = strip_prefix(path)

        path = path.strip().replace("//", "/").replace("\\\\\\\\", "/").replace("\\\\", "/")

        if path.startswith("/"):
            path = path[1:]

        if path.startswith("upload/"):
            path = path[7:]

        if ".." in path or "\x00" in path:
            logger.error(f"检测到路径遍历攻击尝试: {path}")
            raise CustomException(msg="非法的路径格式")

        decoded_path = urllib.parse.unquote(path)
        if ".." in decoded_path:
            logger.error(f"检测到编码后的路径遍历攻击: {path}")
            raise CustomException(msg="非法的路径格式")

        safe_path = os.path.normpath(os.path.join(resource_root, path))

        resource_root_abs = os.path.normpath(os.path.abspath(resource_root))
        safe_path_abs = os.path.normpath(os.path.abspath(safe_path))

        if not safe_path_abs.startswith(resource_root_abs + os.sep) and safe_path_abs != resource_root_abs:
            logger.error(f"路径遍历攻击被阻止: 尝试访问 {safe_path_abs}, 但根目录是 {resource_root_abs}")
            raise CustomException(msg="访问路径不在允许范围内")

        try:
            relative_path = os.path.relpath(safe_path_abs, resource_root_abs)
            if relative_path.count(os.sep) > ResourceService.MAX_PATH_DEPTH:
                raise CustomException(msg="路径深度超过限制")
        except ValueError:
            raise CustomException(msg="无效的路径")

        return safe_path_abs

    @staticmethod
    def _path_exists(path: str) -> bool:
        try:
            safe_path = ResourceService._get_safe_path(path)
            return os.path.exists(safe_path)
        except Exception as e:
            raise CustomException(msg=f"检查路径是否存在失败: {e!s}")

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        if not filename:
            return f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        dangerous_patterns = [
            r"\.\.",
            r"[\/]",
            r"\x00",
            r"%2e%2e",
            r"%252e%252e",
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                logger.error(f"检测到文件名路径遍历攻击: {filename}")
                return f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        decoded = urllib.parse.unquote(filename)
        decoded_twice = urllib.parse.unquote(decoded)
        for check in [decoded, decoded_twice]:
            if ".." in check or "/" in check or "\\" in check:
                logger.error(f"检测到编码后的文件名攻击: {filename}")
                return f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        filename = os.path.basename(filename)
        filename = re.sub(r'[<>:"|?*\x00-\x1f]', "", filename)
        filename = re.sub(r"\.{2,}", ".", filename)
        filename = filename.strip(". ")

        if not filename:
            filename = f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return filename

    @staticmethod
    def _detect_file_type(content: bytes) -> str | None:
        if content.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if content.startswith(b"GIF87a") or content.startswith(b"GIF89a"):
            return "image/gif"
        if content.startswith(b"PK\x03\x04"):
            if b"[Content_Types].xml" in content[:1000]:
                return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return "application/zip"
        if content.startswith(b"%PDF"):
            return "application/pdf"
        if content.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
            return "application/msword"
        return None

    @staticmethod
    def _generate_http_url(file_path: str, base_url: str | None = None) -> str:
        static_root = str(settings.STATIC_ROOT)
        try:
            relative_path = os.path.relpath(file_path, static_root)
            url_path = relative_path.replace(os.sep, "/")
        except ValueError:
            url_path = os.path.basename(file_path)

        if base_url:
            base_part = base_url.rstrip("/")
            static_part = settings.STATIC_URL.lstrip("/")
            file_part = url_path.lstrip("/")
            http_url = f"{base_part}/{static_part}/{file_part}".replace("//", "/").replace(":/", "://")
        else:
            http_url = f"{settings.STATIC_URL}/{url_path}".replace("//", "/")

        return http_url

    @staticmethod
    def _get_file_info(file_path: str, base_url: str | None = None) -> ResourceItemSchema | None:
        try:
            safe_path = file_path
            if not os.path.exists(safe_path):
                return None

            stat = os.stat(safe_path)
            path_obj = Path(safe_path)
            resource_root = ResourceService._get_resource_root()

            try:
                relative_path = os.path.relpath(safe_path, resource_root)
            except ValueError:
                relative_path = os.path.basename(safe_path)

            http_url = ResourceService._generate_http_url(safe_path, base_url)
            is_hidden = path_obj.name.startswith(".")

            return ResourceItemSchema(
                name=path_obj.name,
                file_url=http_url,
                relative_path=relative_path,
                is_file=os.path.isfile(safe_path),
                is_dir=os.path.isdir(safe_path),
                size=stat.st_size if os.path.isfile(safe_path) else None,
                created_time=datetime.fromtimestamp(stat.st_ctime),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                is_hidden=is_hidden,
            )
        except Exception as e:
            logger.error(f"获取文件信息失败: {e!s}")
            return None

    @staticmethod
    async def get_directory_list(
        path: str | None = None,
        include_hidden: bool = False,
        base_url: str | None = None,
    ) -> ResourceDirectorySchema:
        try:
            if path is None:
                safe_path = ResourceService._get_resource_root()
                display_path = ResourceService._generate_http_url(safe_path, base_url)
            else:
                safe_path = ResourceService._get_safe_path(path)
                display_path = ResourceService._generate_http_url(safe_path, base_url)

            if not os.path.exists(safe_path):
                raise CustomException(msg="目录不存在")

            if not os.path.isdir(safe_path):
                raise CustomException(msg="路径不是目录")

            items = []
            total_files = 0
            total_dirs = 0
            total_size = 0

            try:
                for item_name in os.listdir(safe_path):
                    if not include_hidden and item_name.startswith("."):
                        continue

                    item_path = os.path.join(safe_path, item_name)
                    file_info = ResourceService._get_file_info(item_path, base_url)

                    if file_info:
                        items.append(file_info)
                        if file_info.is_file:
                            total_files += 1
                            total_size += file_info.size or 0
                        elif file_info.is_dir:
                            total_dirs += 1

            except PermissionError:
                raise CustomException(msg="没有权限访问此目录")

            return ResourceDirectorySchema(
                path=display_path,
                name=os.path.basename(safe_path),
                items=items,
                total_files=total_files,
                total_dirs=total_dirs,
                total_size=total_size,
            )

        except CustomException:
            raise
        except Exception as e:
            logger.error(f"获取目录列表失败: {e!s}")
            raise CustomException(msg=f"获取目录列表失败: {e!s}")

    @staticmethod
    async def get_resources_list(
        search: ResourceSearchQueryParam | None = None,
        order_by: str | None = None,
        base_url: str | None = None,
    ) -> list[ResourceItemSchema]:
        try:
            if search and hasattr(search, "path") and search.path and isinstance(search.path, str):
                resource_root = ResourceService._get_safe_path(search.path)
            else:
                resource_root = ResourceService._get_resource_root()

            if not os.path.exists(resource_root):
                raise CustomException(msg="目录不存在")

            if not os.path.isdir(resource_root):
                raise CustomException(msg="路径不是目录")

            all_resources = []

            try:
                for item_name in os.listdir(resource_root):
                    if item_name.startswith("."):
                        continue

                    item_path = os.path.join(resource_root, item_name)
                    file_info = ResourceService._get_file_info(item_path, base_url)

                    if file_info:
                        if search and hasattr(search, "name") and search.name and search.name[1]:
                            search_keyword = search.name[1].lower()
                            if search_keyword not in file_info.name.lower():
                                continue
                        all_resources.append(file_info)

            except PermissionError:
                raise CustomException(msg="没有权限访问此目录")

            sorted_resources = ResourceService._sort_results(all_resources, order_by)

            if len(sorted_resources) > ResourceService.MAX_SEARCH_RESULTS:
                sorted_resources = sorted_resources[: ResourceService.MAX_SEARCH_RESULTS]

            return sorted_resources

        except Exception as e:
            logger.error(f"搜索资源失败: {e!s}")
            raise CustomException(msg=f"搜索资源失败: {e!s}")

    @staticmethod
    async def export_resource(data_list: list[ResourceItemSchema]) -> bytes:
        mapping_dict = {
            "name": "文件名",
            "path": "文件路径",
            "size": "文件大小",
            "created_time": "创建时间",
            "modified_time": "修改时间",
            "parent_path": "父目录",
        }

        export_data = [item.model_dump() for item in data_list]

        for item in export_data:
            if item.get("size"):
                item["size"] = ResourceService._format_file_size(item["size"])

        return ExcelUtil.export_list2excel(list_data=export_data, mapping_dict=mapping_dict)

    @staticmethod
    async def download_file(file_path: str) -> str:
        safe_path = ResourceService._get_safe_path(file_path)
        if not os.path.exists(safe_path):
            raise CustomException(msg="文件不存在")
        if not os.path.isfile(safe_path):
            raise CustomException(msg="路径不是文件")
        return safe_path

    @staticmethod
    async def delete_file(paths: list[str]) -> None:
        for path_item in paths:
            safe_path = ResourceService._get_safe_path(path_item)

            if not os.path.exists(safe_path):
                raise CustomException(msg=f"文件不存在: {path_item}")

            try:
                if os.path.isfile(safe_path):
                    os.remove(safe_path)
                elif os.path.isdir(safe_path):
                    shutil.rmtree(safe_path)
                else:
                    raise CustomException(msg=f"无法识别的文件类型: {path_item}")
            except PermissionError:
                raise CustomException(msg=f"没有权限删除: {path_item}")
            except OSError as e:
                raise CustomException(msg=f"删除失败: {path_item} - {e!s}")

            logger.info(f"成功删除: {path_item}")

    @staticmethod
    async def move_file(data: ResourceMoveSchema) -> None:
        source_safe = ResourceService._get_safe_path(data.source_path)
        target_dir_safe = ResourceService._get_safe_path(data.target_dir)

        if not os.path.exists(source_safe):
            raise CustomException(msg=f"源文件不存在: {data.source_path}")

        if not os.path.isdir(target_dir_safe):
            raise CustomException(msg=f"目标目录不存在: {data.target_dir}")

        filename = os.path.basename(source_safe)
        target_path = os.path.join(target_dir_safe, filename)

        if os.path.exists(target_path):
            raise CustomException(msg=f"目标位置已存在同名文件: {filename}")

        try:
            shutil.move(source_safe, target_path)
        except PermissionError:
            raise CustomException(msg=f"没有权限移动文件: {data.source_path}")
        except OSError as e:
            raise CustomException(msg=f"移动文件失败: {e!s}")

        logger.info(f"成功移动文件: {data.source_path} -> {data.target_dir}")

    @staticmethod
    async def copy_file(data: ResourceCopySchema) -> None:
        source_safe = ResourceService._get_safe_path(data.source_path)
        target_dir_safe = ResourceService._get_safe_path(data.target_dir)

        if not os.path.exists(source_safe):
            raise CustomException(msg=f"源文件不存在: {data.source_path}")

        if not os.path.isdir(target_dir_safe):
            raise CustomException(msg=f"目标目录不存在: {data.target_dir}")

        filename = os.path.basename(source_safe)
        target_path = os.path.join(target_dir_safe, filename)

        if os.path.exists(target_path):
            raise CustomException(msg=f"目标位置已存在同名文件: {filename}")

        try:
            if os.path.isdir(source_safe):
                shutil.copytree(source_safe, target_path)
            else:
                shutil.copy2(source_safe, target_path)
        except PermissionError:
            raise CustomException(msg=f"没有权限复制文件: {data.source_path}")
        except OSError as e:
            raise CustomException(msg=f"复制文件失败: {e!s}")

        logger.info(f"成功复制文件: {data.source_path} -> {data.target_dir}")

    @staticmethod
    async def rename_file(data: ResourceRenameSchema) -> None:
        safe_path = ResourceService._get_safe_path(data.file_path)
        parent_dir = os.path.dirname(safe_path)
        safe_name = ResourceService._sanitize_filename(data.new_name)

        new_path = os.path.join(parent_dir, safe_name)

        if os.path.exists(new_path):
            raise CustomException(msg=f"目标文件名已存在: {safe_name}")

        try:
            os.rename(safe_path, new_path)
        except PermissionError:
            raise CustomException(msg=f"没有权限重命名: {data.file_path}")
        except OSError as e:
            raise CustomException(msg=f"重命名失败: {e!s}")

        logger.info(f"成功重命名: {data.file_path} -> {safe_name}")

    @staticmethod
    async def create_directory(data: ResourceCreateDirSchema) -> None:
        parent_dir = ResourceService._get_safe_path(data.parent_path)

        if not os.path.isdir(parent_dir):
            raise CustomException(msg=f"父目录不存在: {data.parent_path}")

        safe_name = ResourceService._sanitize_filename(data.dir_name)
        new_dir = os.path.join(parent_dir, safe_name)

        if os.path.exists(new_dir):
            raise CustomException(msg=f"目录已存在: {data.dir_name}")

        try:
            os.makedirs(new_dir, exist_ok=False)
        except PermissionError:
            raise CustomException(msg=f"没有权限创建目录: {data.dir_name}")
        except OSError as e:
            raise CustomException(msg=f"创建目录失败: {e!s}")

        logger.info(f"成功创建目录: {data.parent_path}/{safe_name}")

    @staticmethod
    async def _get_directory_stats(path: str, include_hidden: bool = False) -> dict[str, int]:
        stats = {"files": 0, "dirs": 0, "size": 0}

        try:
            for root, dirs, files in os.walk(path):
                if not include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith(".")]
                    files = [f for f in files if not f.startswith(".")]

                stats["dirs"] += len(dirs)
                stats["files"] += len(files)

                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stats["size"] += os.path.getsize(file_path)
                    except OSError:
                        continue
        except Exception:
            pass

        return stats

    @staticmethod
    def _sort_results(results: list[ResourceItemSchema], order_by: str | None = None) -> list[ResourceItemSchema]:
        try:
            if not order_by:
                return sorted(results, key=lambda x: x.name, reverse=False)

            sort_conditions = ast.literal_eval(order_by)
            if isinstance(sort_conditions, list):

                def sort_key(item):
                    keys = []
                    for cond in sort_conditions:
                        field = cond.get("field", "name")
                        value = getattr(item, field, "")
                        if field in ["created_time", "modified_time", "accessed_time"] and value:
                            if isinstance(value, str):
                                value = datetime.fromisoformat(value)
                        keys.append(value)
                    return keys

                reverse = False
                if sort_conditions and isinstance(sort_conditions[0], dict):
                    order = sort_conditions[0].get("order", "asc")
                    reverse = order.lower() == "desc"

                return sorted(results, key=sort_key, reverse=reverse)

            return sorted(results, key=lambda x: x.name, reverse=False)

        except (ValueError, SyntaxError):
            return sorted(results, key=lambda x: x.name, reverse=False)

    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
