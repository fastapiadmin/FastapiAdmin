# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from fastapi import UploadFile

from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil
from app.config.setting import settings

from .schema import (
    ResourceItemSchema,
    ResourceDirectorySchema,
    ResourceUploadSchema,
    ResourceMoveSchema,
    ResourceCopySchema,
    ResourceRenameSchema,
    ResourceCreateDirSchema,
    ResourceSearchQueryParam
)


class ResourceService:
    """
    资源管理模块服务层 - 管理系统静态文件目录
    """
    
    # 配置常量
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    MAX_SEARCH_RESULTS = 1000  # 最大搜索结果数
    MAX_PATH_DEPTH = 20  # 最大路径深度
    
    @classmethod
    def _get_resource_root(cls) -> str:
        """
        获取资源管理根目录
        
        返回:
        - str: 资源管理根目录路径。
        """
        if not settings.STATIC_ENABLE:
            raise CustomException(msg='静态文件服务未启用')
        return str(settings.STATIC_ROOT)
    
    @classmethod
    def _get_safe_path(cls, path: str | None = None) -> str:
        """
        获取安全的文件路径
        
        参数:
        - path (str | None): 原始文件路径。
        
        返回:
        - str: 安全的文件路径。
        """
        resource_root = cls._get_resource_root()
        
        if not path:
            return resource_root
        
        # 支持前端传递的完整URL或以STATIC_URL/ROOT_PATH+STATIC_URL开头的URL路径，转换为相对资源路径
        if isinstance(path, str):
            static_prefix = settings.STATIC_URL.rstrip('/')
            root_prefix = settings.ROOT_PATH.rstrip('/') if getattr(settings, 'ROOT_PATH', '') else ''
            root_static_prefix = f"{root_prefix}{static_prefix}" if root_prefix else static_prefix
            
            def strip_prefix(p: str) -> str:
                if p.startswith(root_static_prefix):
                    return p[len(root_static_prefix):].lstrip('/')
                if p.startswith(static_prefix):
                    return p[len(static_prefix):].lstrip('/')
                return p
            
            if path.startswith('http://') or path.startswith('https://'):
                parsed = urlparse(path)
                url_path = parsed.path or ''
                path = strip_prefix(url_path)
            else:
                path = strip_prefix(path)
        
        # 清理路径，移除危险字符
        path = path.strip().replace('..', '').replace('//', '/')
        
        # 规范化路径
        if os.path.isabs(path):
            safe_path = os.path.normpath(path)
        else:
            safe_path = os.path.normpath(os.path.join(resource_root, path))
        
        # 检查路径是否在允许的范围内
        resource_root_abs = os.path.normpath(os.path.abspath(resource_root))
        safe_path_abs = os.path.normpath(os.path.abspath(safe_path))
        
        if not safe_path_abs.startswith(resource_root_abs):
            raise CustomException(msg=f'访问路径不在允许范围内: {path}')
        
        # 防止路径遍历攻击
        if '..' in safe_path or safe_path.count('/') > cls.MAX_PATH_DEPTH:
            raise CustomException(msg=f'不安全的路径格式: {path}')
        
        return safe_path
    
    @classmethod
    def _path_exists(cls, path: str) -> bool:
        """
        检查路径是否存在
        
        参数:
        - path (str): 要检查的路径。
        
        返回:
        - bool: 如果路径存在则返回True，否则返回False。
        """
        try:
            safe_path = cls._get_safe_path(path)
            return os.path.exists(safe_path)
        except:
            return False
    
    @classmethod
    def _generate_http_url(cls, file_path: str, base_url: str | None = None) -> str:
        """
        生成文件的HTTP URL
        
        参数:
        - file_path (str): 文件的绝对路径。
        - base_url (str | None): 基础URL，用于生成完整URL。
        
        返回:
        - str: 文件的HTTP URL。
        """
        resource_root = cls._get_resource_root()
        try:
            relative_path = os.path.relpath(file_path, resource_root)
            # 确保路径使用正斜杠（URL格式）
            url_path = relative_path.replace(os.sep, '/')
        except ValueError:
            # 如果无法计算相对路径，使用文件名
            url_path = os.path.basename(file_path)
        
        # 如果提供了base_url，使用它生成完整URL，否则使用settings.STATIC_URL
        if base_url:
            # 修复URL生成逻辑
            base_part = base_url.rstrip('/')
            static_part = settings.STATIC_URL.lstrip('/')
            file_part = url_path.lstrip('/')
            if base_part.endswith(':') or (len(base_part) > 0 and base_part[-1] not in ['/', ':']):
                base_part += '/'
            http_url = f"{base_part}{static_part}/{file_part}".replace('//', '/').replace(':/', '://')
        else:
            http_url = f"{settings.STATIC_URL}/{url_path}".replace('//', '/')
        
        return http_url
    
    @classmethod
    def _get_file_info(cls, file_path: str, base_url: str | None = None) -> dict:
        """
        获取文件或目录的详细信息，如名称、大小、创建时间、修改时间、路径、深度、HTTP URL、是否隐藏、是否为目录等。
        
        参数:
        - file_path (str): 文件或目录的路径。
        - base_url (str | None): 基础URL，用于生成完整URL。
        
        返回:
        - dict: 文件或目录的详细信息字典。
        """
        try:
            safe_path = cls._get_safe_path(file_path)
            if not os.path.exists(safe_path):
                return {}
                
            stat = os.stat(safe_path)
            path_obj = Path(safe_path)
            resource_root = cls._get_resource_root()
            
            # 计算相对路径
            try:
                relative_path = os.path.relpath(safe_path, resource_root)
            except ValueError:
                relative_path = os.path.basename(safe_path)
            
            # 计算深度
            try:
                depth = len(Path(safe_path).relative_to(resource_root).parts)
            except ValueError:
                depth = 0
            
            # 生成HTTP URL路径而不是文件系统路径
            http_url = cls._generate_http_url(safe_path, base_url)
            
            # 检查是否为隐藏文件（文件名以点开头）
            is_hidden = path_obj.name.startswith('.')
            
            # 对于目录，设置is_directory字段（兼容前端）
            is_directory = os.path.isdir(safe_path)
            
            # 将datetime对象转换为ISO格式的字符串，确保JSON序列化成功
            created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
            modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            return {
                'name': path_obj.name,
                'file_url': http_url,  # 统一使用file_url字段
                'relative_path': relative_path,
                'is_file': os.path.isfile(safe_path),
                'is_dir': is_directory,
                'size': stat.st_size if os.path.isfile(safe_path) else None,
                'created_time': created_time,
                'modified_time': modified_time,
                'is_hidden': is_hidden
            }
        except Exception as e:
            log.error(f'获取文件信息失败: {str(e)}')
            return {}
    
    @classmethod
    async def get_directory_list_service(cls, path: str | None = None, include_hidden: bool = False, base_url: str | None = None) -> dict:
        """
        获取目录列表
        
        参数:
        - path (str | None): 目录路径。如果未指定，将使用静态文件根目录。
        - include_hidden (bool): 是否包含隐藏文件。
        - base_url (str | None): 基础URL，用于生成完整URL。
        
        返回:
        - dict: 包含目录列表和统计信息的字典。
        """
        try:
            # 如果没有指定路径，使用静态文件根目录
            if path is None:
                safe_path = cls._get_resource_root()
                display_path = cls._generate_http_url(safe_path, base_url)
            else:
                safe_path = cls._get_safe_path(path)
                display_path = cls._generate_http_url(safe_path, base_url)
            
            if not os.path.exists(safe_path):
                raise CustomException(msg='目录不存在')
                
            if not os.path.isdir(safe_path):
                raise CustomException(msg='路径不是目录')
            
            items = []
            total_files = 0
            total_dirs = 0
            total_size = 0
            
            try:
                for item_name in os.listdir(safe_path):
                    # 跳过隐藏文件
                    if not include_hidden and item_name.startswith('.'):
                        continue
                        
                    item_path = os.path.join(safe_path, item_name)
                    file_info = cls._get_file_info(item_path, base_url)
                    
                    if file_info:
                        items.append(ResourceItemSchema(**file_info))
                        
                        if file_info['is_file']:
                            total_files += 1
                            total_size += file_info.get('size', 0) or 0
                        elif file_info['is_dir']:
                            total_dirs += 1
                                
            except PermissionError:
                raise CustomException(msg='没有权限访问此目录')
            
            return ResourceDirectorySchema(
                path=display_path,  # 返回HTTP URL路径而不是文件系统路径
                name=os.path.basename(safe_path),
                items=items,
                total_files=total_files,
                total_dirs=total_dirs,
                total_size=total_size
            ).model_dump()
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f'获取目录列表失败: {str(e)}')
            raise CustomException(msg=f'获取目录列表失败: {str(e)}')

    @classmethod
    async def get_resources_list_service(cls, search: ResourceSearchQueryParam | None = None, order_by: str | None = None, base_url: str | None = None) -> list[dict]:
        """
        搜索资源列表（用于分页和导出）
        
        参数:
        - search (ResourceSearchQueryParam | None): 查询参数模型。
        - order_by (str | None): 排序参数。
        - base_url (str | None): 基础URL，用于生成完整URL。
        
        返回:
        - list[dict]: 资源详情字典列表。
        """
        try:
            # 确定搜索路径
            if search and hasattr(search, 'path') and search.path:
                resource_root = cls._get_safe_path(search.path)
            else:
                resource_root = cls._get_resource_root()
            
            # 检查路径是否存在
            if not os.path.exists(resource_root):
                raise CustomException(msg='目录不存在')
                
            if not os.path.isdir(resource_root):
                raise CustomException(msg='路径不是目录')
            
            # 收集资源
            all_resources = []
            
            try:
                for item_name in os.listdir(resource_root):
                    # 跳过隐藏文件
                    if item_name.startswith('.'):
                        continue
                    
                    item_path = os.path.join(resource_root, item_name)
                    file_info = cls._get_file_info(item_path, base_url)
                    
                    if file_info:
                        # 应用名称过滤
                        if search and hasattr(search, 'name') and search.name and search.name[1]:
                            search_keyword = search.name[1].lower()
                            if search_keyword not in file_info.get('name', '').lower():
                                continue
                        
                        all_resources.append(file_info)
                                
            except PermissionError:
                raise CustomException(msg='没有权限访问此目录')
            
            # 应用排序
            sorted_resources = cls._sort_results(all_resources, order_by)
            
            # 限制最大结果数
            if len(sorted_resources) > cls.MAX_SEARCH_RESULTS:
                sorted_resources = sorted_resources[:cls.MAX_SEARCH_RESULTS]
                
            return sorted_resources
            
        except Exception as e:
            log.error(f'搜索资源失败: {str(e)}')
            raise CustomException(msg=f'搜索资源失败: {str(e)}')

    @classmethod
    async def export_resource_service(cls, data_list: list[dict]) -> bytes:
        """
        导出资源列表
        
        参数:
        - data_list (list[dict]): 资源详情字典列表。
        
        返回:
        - bytes: Excel文件的二进制数据。
        """
        mapping_dict = {
            'name': '文件名',
            'path': '文件路径',
            'size': '文件大小',
            'created_time': '创建时间',
            'modified_time': '修改时间',
            'parent_path': '父目录'
        }

        # 复制数据并转换状态
        export_data = data_list.copy()
            
        # 格式化文件大小
        for item in export_data:
            if item.get('size'):
                item['size'] = cls._format_file_size(item['size'])

        return ExcelUtil.export_list2excel(list_data=export_data, mapping_dict=mapping_dict)

    @classmethod
    async def _get_directory_stats(cls, path: str, include_hidden: bool = False) -> dict[str, int]:
        """
        递归获取目录统计信息
        
        参数:
        - path (str): 目录路径。
        - include_hidden (bool): 是否包含隐藏文件。
        
        返回:
        - dict[str, int]: 包含文件数、目录数和总大小的字典。
        """
        stats = {'files': 0, 'dirs': 0, 'size': 0}
        
        try:
            for root, dirs, files in os.walk(path):
                # 过滤隐藏目录
                if not include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                stats['dirs'] += len(dirs)
                stats['files'] += len(files)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stats['size'] += os.path.getsize(file_path)
                    except (OSError, IOError):
                        continue
                        
        except Exception:
            pass
            
        return stats
    
    @classmethod
    def _sort_results(cls, results: list[dict], order_by: str | None = None) -> list[dict]:
        """
        排序搜索结果
        
        参数:
        - results (list[dict]): 资源详情字典列表。
        - order_by (str | None): 排序参数。
        
        返回:
        - list[dict]: 排序后的资源详情字典列表。
        """
        try:
            # 默认按名称升序排序
            if not order_by:
                return sorted(results, key=lambda x: x.get('name', ''), reverse=False)
            
            # 解析order_by参数，格式: [{'field':'asc/desc'}]
            try:
                sort_conditions = eval(order_by)
                if isinstance(sort_conditions, list):
                    # 构建排序键函数
                    def sort_key(item):
                        keys = []
                        for cond in sort_conditions:
                            field = cond.get('field', 'name')
                            direction = cond.get('direction', 'asc')
                            # 获取字段值，默认为空字符串
                            value = item.get(field, '')
                            # 如果是日期字段，转换为可比较的格式
                            if field in ['created_time', 'modified_time', 'accessed_time'] and value:
                                value = datetime.fromisoformat(value)
                            keys.append(value)
                        return keys
                    
                    # 确定排序方向（这里只支持单一方向，多个条件时使用第一个条件的方向）
                    reverse = False
                    if sort_conditions and isinstance(sort_conditions[0], dict):
                        direction = sort_conditions[0].get('direction', '').lower()
                        reverse = direction == 'desc'
                    
                    return sorted(results, key=sort_key, reverse=reverse)
            except:
                # 如果解析失败，使用默认排序
                pass
            
            return sorted(results, key=lambda x: x.get('name', ''), reverse=False)
        except:
            return results

    @classmethod
    async def upload_file_service(cls,  file: UploadFile, target_path: str | None = None, base_url: str | None = None) -> dict:
        """
        上传文件到指定目录
        
        参数:
        - file (UploadFile): 上传的文件对象。
        - target_path (str | None): 目标目录路径。
        - base_url (str | None): 基础URL，用于生成完整URL。
        
        返回:
        - dict: 包含文件信息的字典。
        """
        if not file or not file.filename:
            raise CustomException(msg="请选择要上传的文件")
        
        # 文件名安全检查
        if '..' in file.filename or '/' in file.filename or '\\' in file.filename:
            raise CustomException(msg="文件名包含不安全字符")
        
        try:
            # 检查文件大小
            content = await file.read()
            if len(content) > cls.MAX_UPLOAD_SIZE:
                raise CustomException(msg=f"文件太大，最大支持{cls.MAX_UPLOAD_SIZE // (1024*1024)}MB")
            
            # 确定上传目录，如果没有指定目标路径，使用静态文件根目录
            if target_path is None:
                safe_dir = cls._get_resource_root()
            else:
                safe_dir = cls._get_safe_path(target_path)
            
            # 创建目录（如果不存在）
            os.makedirs(safe_dir, exist_ok=True)
            
            # 生成文件路径
            filename = file.filename
            file_path = os.path.join(safe_dir, filename)
            
            # 检查文件是否已存在
            if os.path.exists(file_path):
                # 生成唯一文件名
                base_name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(file_path):
                    new_filename = f"{base_name}_{counter}{ext}"
                    file_path = os.path.join(safe_dir, new_filename)
                    counter += 1
                filename = os.path.basename(file_path)
            
            # 保存文件（使用已读取的内容）
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # 获取文件信息
            file_info = cls._get_file_info(file_path, base_url)
            
            # 生成文件URL
            file_url = cls._generate_http_url(file_path, base_url)
            
            log.info(f"文件上传成功: {filename}")
            
            return ResourceUploadSchema(
                filename=filename,
                file_url=file_url,
                file_size=file_info.get('size', 0),
                upload_time=datetime.now()
            ).model_dump(mode='json')
            
        except Exception as e:
            log.error(f"文件上传失败: {str(e)}")
            raise CustomException(msg=f"文件上传失败: {str(e)}")

    @classmethod
    async def download_file_service(cls, file_path: str, base_url: str | None = None) -> str:
        """
        下载文件（返回本地文件系统路径）
        
        参数:
        - file_path (str): 文件路径（可为相对路径、绝对路径或完整URL）。
        - base_url (str | None): 基础URL，用于生成完整URL（不再直接返回URL）。
        
        返回:
        - str: 本地文件系统路径。
        """
        try:
            safe_path = cls._get_safe_path(file_path)
            
            if not os.path.exists(safe_path):
                raise CustomException(msg='文件不存在')
            
            if not os.path.isfile(safe_path):
                raise CustomException(msg='路径不是文件')
            
            # 返回本地文件路径给 FileResponse 使用
            log.info(f"定位文件路径: {safe_path}")
            return safe_path
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"下载文件失败: {str(e)}")
            raise CustomException(msg=f"下载文件失败: {str(e)}")

    @classmethod
    async def delete_file_service(cls, paths: list[str]) -> None:
        """
        删除文件或目录
        
        参数:
        - paths (list[str]): 文件或目录路径列表。
        
        返回:
        - None
        """
        if not paths:
            raise CustomException(msg='删除失败，删除路径不能为空')
        
        for path in paths:
            try:
                safe_path = cls._get_safe_path(path)
                
                if not os.path.exists(safe_path):
                    log.error(f"路径不存在，跳过: {path}")
                    continue
                
                if os.path.isfile(safe_path):
                    os.remove(safe_path)
                    log.info(f"删除文件成功: {safe_path}")
                elif os.path.isdir(safe_path):
                    shutil.rmtree(safe_path)
                    log.info(f"删除目录成功: {safe_path}")
                    
            except Exception as e:
                log.error(f"删除失败 {path}: {str(e)}")
                raise CustomException(msg=f"删除失败 {path}: {str(e)}")

    @classmethod
    async def batch_delete_service(cls, paths: list[str]) -> dict[str, list[str]]:
        """
        批量删除文件或目录
        
        参数:
        - paths (List[str]): 文件或目录路径列表。
        
        返回:
        - Dict[str, List[str]]: 包含成功删除路径和失败删除路径的字典。
        """
        if not paths:
            raise CustomException(msg='删除失败，删除路径不能为空')
        
        success_paths = []
        failed_paths = []
        
        for path in paths:
            try:
                safe_path = cls._get_safe_path(path)
                
                if not os.path.exists(safe_path):
                    failed_paths.append(path)
                    continue
                
                if os.path.isfile(safe_path):
                    os.remove(safe_path)
                    success_paths.append(path)
                    log.info(f"删除文件成功: {safe_path}")
                elif os.path.isdir(safe_path):
                    shutil.rmtree(safe_path)
                    success_paths.append(path)
                    log.info(f"删除目录成功: {safe_path}")
                    
            except Exception as e:
                log.error(f"删除失败 {path}: {str(e)}")
                failed_paths.append(path)
        
        return {
            "success": success_paths,
            "failed": failed_paths
        }

    @classmethod
    async def move_file_service(cls, data: ResourceMoveSchema) -> None:
        """
        移动文件或目录
        
        参数:
        - data (ResourceMoveSchema): 包含源路径和目标路径的模型。
        
        返回:
        - None
        """
        try:
            source_path = cls._get_safe_path(data.source_path)
            target_path = cls._get_safe_path(data.target_path)
            
            if not os.path.exists(source_path):
                raise CustomException(msg='源路径不存在')
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path):
                if not data.overwrite:
                    raise CustomException(msg='目标路径已存在')
                else:
                    # 删除目标路径
                    if os.path.isfile(target_path):
                        os.remove(target_path)
                    else:
                        shutil.rmtree(target_path)
            
            # 确保目标目录存在
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # 移动文件
            shutil.move(source_path, target_path)
            log.info(f"移动成功: {source_path} -> {target_path}")
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"移动失败: {str(e)}")
            raise CustomException(msg=f"移动失败: {str(e)}")

    @classmethod
    async def copy_file_service(cls, data: ResourceCopySchema) -> None:
        """
        复制文件或目录
        
        参数:
        - data (ResourceCopySchema): 包含源路径和目标路径的模型。
        
        返回:
        - None
        """
        try:
            source_path = cls._get_safe_path(data.source_path)
            target_path = cls._get_safe_path(data.target_path)
            
            if not os.path.exists(source_path):
                raise CustomException(msg='源路径不存在')
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path) and not data.overwrite:
                raise CustomException(msg='目标路径已存在')
            
            # 确保目标目录存在
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制文件或目录
            if os.path.isfile(source_path):
                shutil.copy2(source_path, target_path)
            else:
                shutil.copytree(source_path, target_path, dirs_exist_ok=data.overwrite)
            
            log.info(f"复制成功: {source_path} -> {target_path}")
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"复制失败: {str(e)}")
            raise CustomException(msg=f"复制失败: {str(e)}")

    @classmethod
    async def rename_file_service(cls, data: ResourceRenameSchema) -> None:
        """
        重命名文件或目录
        
        参数:
        - data (ResourceRenameSchema): 包含旧路径和新名称的模型。
        
        返回:
        - None
        """
        try:
            old_path = cls._get_safe_path(data.old_path)
            
            if not os.path.exists(old_path):
                raise CustomException(msg='文件或目录不存在')
            
            # 生成新路径
            parent_dir = os.path.dirname(old_path)
            new_path = os.path.join(parent_dir, data.new_name)
            
            if os.path.exists(new_path):
                raise CustomException(msg='目标名称已存在')
            
            # 重命名
            os.rename(old_path, new_path)
            log.info(f"重命名成功: {old_path} -> {new_path}")
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"重命名失败: {str(e)}")
            raise CustomException(msg=f"重命名失败: {str(e)}")

    @classmethod
    async def create_directory_service(cls, data: ResourceCreateDirSchema) -> None:
        """
        创建目录
        
        参数:
        - data (ResourceCreateDirSchema): 包含父目录路径和目录名称的模型。
        
        返回:
        - None
        """
        try:
            parent_path = cls._get_safe_path(data.parent_path)
            
            if not os.path.exists(parent_path):
                raise CustomException(msg='父目录不存在')
            
            if not os.path.isdir(parent_path):
                raise CustomException(msg='父路径不是目录')
            
            # 生成新目录路径
            new_dir_path = os.path.join(parent_path, data.dir_name)
            
            # 安全检查：确保新目录名称不包含路径遍历字符
            if '..' in data.dir_name or '/' in data.dir_name or '\\' in data.dir_name:
                raise CustomException(msg='目录名称包含不安全字符')
            
            if os.path.exists(new_dir_path):
                raise CustomException(msg='目录已存在')
            
            # 创建目录
            os.makedirs(new_dir_path)
            log.info(f"创建目录成功: {new_dir_path}")
            
        except CustomException:
            raise
        except Exception as e:
            log.error(f"创建目录失败: {str(e)}")
            raise CustomException(msg=f"创建目录失败: {str(e)}")

    @classmethod
    def _format_file_size(cls, size_bytes: int) -> str:
        """
        格式化文件大小
        
        参数:
        - size_bytes (int): 文件大小（字节）
        
        返回:
        - str: 格式化后的文件大小字符串（例如："123.45MB"）
        """
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes = int(size_bytes / 1024)
            i += 1
        
        return f"{size_bytes:.2f}{size_names[i]}"
