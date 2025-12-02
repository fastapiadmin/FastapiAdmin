# -*- coding: utf-8 -*-

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from urllib.parse import urlparse
from fastapi import Query


class ResourceItemSchema(BaseModel):
    """资源项目模型"""
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., description="文件名")
    file_url: str = Field(..., description="文件URL路径")
    relative_path: str = Field(..., description="相对路径")
    is_file: bool = Field(..., description="是否为文件")
    is_dir: bool = Field(..., description="是否为目录")
    size: int | None = Field(None, description="文件大小(字节)")
    created_time: datetime | None = Field(None, description="创建时间")
    modified_time: datetime | None = Field(None, description="修改时间")
    is_hidden: bool = Field(False, description="是否为隐藏文件")

    @field_validator('file_url')
    @classmethod
    def _validate_file_url(cls, v: str) -> str:
        v = v.strip()
        parsed = urlparse(v)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError('文件URL必须为 http/https')
        return v

    @field_validator('relative_path')
    @classmethod
    def _validate_relative_path(cls, v: str) -> str:
        v = v.strip()
        if '..' in v or v.startswith('\\'):
            raise ValueError('相对路径包含不安全字符')
        return v

    @model_validator(mode='after')
    def _validate_flags(self):
        if self.is_file and self.is_dir:
            raise ValueError('不能同时为文件和目录')
        if not self.is_file and not self.is_dir:
            raise ValueError('必须是文件或目录之一')
        # 根据名称自动修正隐藏标记
        self.is_hidden = self.name.startswith('.')
        return self


class ResourceDirectorySchema(BaseModel):
    """资源目录模型"""
    model_config = ConfigDict(from_attributes=True)
    
    path: str = Field(..., description="目录路径")
    name: str = Field(..., description="目录名称")
    items: list[ResourceItemSchema] = Field(default_factory=list, description="目录项")
    total_files: int = Field(0, description="文件总数")
    total_dirs: int = Field(0, description="目录总数")
    total_size: int = Field(0, description="总大小")


class ResourceUploadSchema(BaseModel):
    """资源上传响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    filename: str = Field(..., description="文件名")
    file_url: str = Field(..., description="访问URL")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(..., description="上传时间")


class ResourceMoveSchema(BaseModel):
    """资源移动模型"""
    model_config = ConfigDict(from_attributes=True)
    
    source_path: str = Field(..., description="源路径")
    target_path: str = Field(..., description="目标路径")
    overwrite: bool = Field(False, description="是否覆盖")
    
    @field_validator('source_path', 'target_path')
    @classmethod
    def validate_paths(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("路径不能为空")
        return value.strip()


class ResourceCopySchema(ResourceMoveSchema):
    """资源复制模型"""
    pass


class ResourceRenameSchema(BaseModel):
    """资源重命名模型"""
    model_config = ConfigDict(from_attributes=True)
    
    old_path: str = Field(..., description="原路径")
    new_name: str = Field(..., description="新名称")
    
    @field_validator('old_path', 'new_name')
    @classmethod
    def validate_inputs(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("参数不能为空")
        return value.strip()

    @field_validator('new_name')
    @classmethod
    def _validate_new_name(cls, v: str) -> str:
        v = v.strip()
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('新名称包含不安全字符')
        return v


class ResourceCreateDirSchema(BaseModel):
    """创建目录模型"""
    model_config = ConfigDict(from_attributes=True)
    
    parent_path: str = Field(..., description="父目录路径")
    dir_name: str = Field(..., description="目录名称", max_length=255)
    
    @field_validator('parent_path', 'dir_name')
    @classmethod
    def validate_inputs(cls, value: str, info):
        # 对于parent_path允许为空字符串（表示根目录）或 '/'，其他情况必须非空
        if info.field_name == 'parent_path':
            # 允许空字符串或 '/' 表示根目录
            if value is None:
                raise ValueError("参数不能为空")
            # 对于parent_path仍然严格检查路径遍历
            if '..' in value or value.startswith('\\'):
                raise ValueError("参数包含不安全字符")
        else:  # 对于dir_name仍然严格检查
            if not value or len(value.strip()) == 0:
                raise ValueError("参数不能为空")
            if '..' in value or value.startswith('/') or value.startswith('\\'):
                raise ValueError("参数包含不安全字符")
        return value.strip()


class ResourceSearchQueryParam:
    """资源搜索查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="搜索关键词"),
        path: str | None = Query(None, description="目录路径"),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name) if name else None
        
        # 精确查询字段
        self.path = path