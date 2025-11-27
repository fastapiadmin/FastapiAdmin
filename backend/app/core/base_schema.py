# -*- coding: utf-8 -*-

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.validator import DateTimeStr


class UserInfoSchema(BaseModel):
    """用户信息模型"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="用户ID")
    name: str = Field(description="用户姓名")
    username: str = Field(description="用户名")


class CommonSchema(BaseModel):
    """通用信息模型"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="编号ID")
    name: str = Field(description="名称")


class BaseSchema(BaseModel):
    """通用输出模型，包含基础字段和审计字段"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, description="主键ID")
    uuid: Optional[str] = Field(default=None, description="UUID")
    status: Optional[str] = Field(default=None, description="状态")
    description: Optional[str] = Field(default=None, description="描述")
    created_time: Optional[DateTimeStr] = Field(default=None, description="创建时间")
    updated_time: Optional[DateTimeStr] = Field(default=None, description="更新时间")

class UserBySchema(BaseModel):
    """通用创建模型，包含基础字段和审计字段"""
    model_config = ConfigDict(from_attributes=True)

    created_id: Optional[int] = Field(default=None, description="创建人ID")
    created_by: Optional[UserInfoSchema] = Field(default=None, description="创建人信息")
    updated_id: Optional[int] = Field(default=None, description="更新人ID")
    updated_by: Optional[UserInfoSchema] = Field(default=None, description="更新人信息")

class TenantSchema(BaseModel):
    """租户模型"""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: Optional[int] = Field(default=None, description="所属租户ID")
    tenant: Optional[CommonSchema] = Field(default=None, description="租户信息")


class CustomerSchema(BaseModel):
    """客户模型"""
    model_config = ConfigDict(from_attributes=True)

    customer_id: Optional[int] = Field(default=None, description="所属客户ID")
    customer: Optional[CommonSchema] = Field(default=None, description="客户信息")


class BatchSetAvailable(BaseModel):
    """批量设置可用状态的请求模型"""
    ids: List[int] = Field(default_factory=list, description="ID列表")
    status: str = Field(default=True, description="是否可用")


class UploadResponseSchema(BaseModel):
    """上传响应模型"""
    model_config = ConfigDict(from_attributes=True)

    file_path: Optional[str] = Field(default=None, description='新文件映射路径')
    file_name: Optional[str] = Field(default=None, description='新文件名称') 
    origin_name: Optional[str] = Field(default=None, description='原文件名称')
    file_url: Optional[str] = Field(default=None, description='新文件访问地址')


class DownloadFileSchema(BaseModel):
    """下载文件模型"""
    file_path: str = Field(..., description='新文件映射路径')
    file_name: str = Field(..., description='新文件名称')
