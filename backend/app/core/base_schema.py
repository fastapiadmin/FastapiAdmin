# -*- coding: utf-8 -*-

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

    id: int | None = Field(default=None, description="主键ID")
    uuid: str | None = Field(default=None, description="UUID")
    status: str = Field(default="0", description="状态")
    description: str | None = Field(default=None, description="描述")
    created_time: DateTimeStr | None = Field(default=None, description="创建时间")
    updated_time: DateTimeStr | None = Field(default=None, description="更新时间")


class UserBySchema(BaseModel):
    """通用创建模型，包含基础字段和审计字段"""
    model_config = ConfigDict(from_attributes=True)

    created_id: int | None = Field(default=None, description="创建人ID")
    created_by: UserInfoSchema | None = Field(default=None, description="创建人信息")
    updated_id: int | None = Field(default=None, description="更新人ID")
    updated_by: UserInfoSchema | None = Field(default=None, description="更新人信息")


class BatchSetAvailable(BaseModel):
    """批量设置可用状态的请求模型"""
    ids: list[int] = Field(default_factory=list, description="ID列表")
    status: str = Field(default="0", description="是否可用")


class UploadResponseSchema(BaseModel):
    """上传响应模型"""
    model_config = ConfigDict(from_attributes=True)

    file_path: str | None = Field(default=None, description='新文件映射路径')
    file_name: str | None = Field(default=None, description='新文件名称') 
    origin_name: str | None = Field(default=None, description='原文件名称')
    file_url: str | None = Field(default=None, description='新文件访问地址')


class DownloadFileSchema(BaseModel):
    """下载文件模型"""
    file_path: str = Field(..., description='新文件映射路径')
    file_name: str = Field(..., description='新文件名称')
