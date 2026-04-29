"""
表彰评优 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

AwardRouter = APIRouter(prefix="/award", tags=["表彰评优"])


@AwardRouter.get("", summary="表彰列表")
async def list_award_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取表彰列表"""
    return ResponseSchema(data=[])


@AwardRouter.get("/{award_id}", summary="表彰详情")
async def get_award_controller(
    award_id: Annotated[int, Path(description="表彰ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:query"]))],
) -> ResponseSchema[dict]:
    """获取单个表彰详情"""
    return ResponseSchema(data={})


@AwardRouter.post("", summary="创建表彰")
async def create_award_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:create"]))],
) -> ResponseSchema[dict]:
    """创建表彰"""
    return ResponseSchema(data={})


@AwardRouter.put("/{award_id}", summary="更新表彰")
async def update_award_controller(
    award_id: Annotated[int, Path(description="表彰ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:update"]))],
) -> ResponseSchema[dict]:
    """更新表彰"""
    return ResponseSchema(data={})


@AwardRouter.delete("/{award_id}", summary="删除表彰")
async def delete_award_controller(
    award_id: Annotated[int, Path(description="表彰ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:delete"]))],
) -> ResponseSchema[bool]:
    """删除表彰"""
    return ResponseSchema(data=True)


@AwardRouter.post("/{award_id}/issue", summary="颁发表彰")
async def issue_award_controller(
    award_id: Annotated[int, Path(description="表彰ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:award:issue"]))],
) -> ResponseSchema[dict]:
    """颁发表彰"""
    return ResponseSchema(data={})
