"""
团队管理 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

TeamRouter = APIRouter(prefix="/team", tags=["团队管理"])


@TeamRouter.get("", summary="团队列表")
async def list_team_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:team:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取团队列表"""
    return ResponseSchema(data=[])


@TeamRouter.get("/{team_id}", summary="团队详情")
async def get_team_controller(
    team_id: Annotated[int, Path(description="团队ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:team:query"]))],
) -> ResponseSchema[dict]:
    """获取单个团队详情"""
    return ResponseSchema(data={})


@TeamRouter.post("", summary="创建团队")
async def create_team_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:team:create"]))],
) -> ResponseSchema[dict]:
    """创建团队"""
    return ResponseSchema(data={})


@TeamRouter.put("/{team_id}", summary="更新团队")
async def update_team_controller(
    team_id: Annotated[int, Path(description="团队ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:team:update"]))],
) -> ResponseSchema[dict]:
    """更新团队"""
    return ResponseSchema(data={})


@TeamRouter.delete("/{team_id}", summary="删除团队")
async def delete_team_controller(
    team_id: Annotated[int, Path(description="团队ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:team:delete"]))],
) -> ResponseSchema[bool]:
    """删除团队"""
    return ResponseSchema(data=True)
