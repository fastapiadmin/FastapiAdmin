"""
保险管理 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

InsuranceRouter = APIRouter(prefix="/insurance", tags=["保险管理"])


@InsuranceRouter.get("/policies", summary="保单列表")
async def list_policies_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:insurance:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取保单列表"""
    return ResponseSchema(data=[])


@InsuranceRouter.get("/policies/{policy_id}", summary="保单详情")
async def get_policy_controller(
    policy_id: Annotated[int, Path(description="保单ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:insurance:query"]))],
) -> ResponseSchema[dict]:
    """获取单个保单详情"""
    return ResponseSchema(data={})


@InsuranceRouter.post("/policies/apply", summary="申请投保")
async def apply_insurance_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:insurance:apply"]))],
) -> ResponseSchema[dict]:
    """申请投保"""
    return ResponseSchema(data={})


@InsuranceRouter.get("/policies/{policy_id}/download", summary="下载保单")
async def download_policy_controller(
    policy_id: Annotated[int, Path(description="保单ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:insurance:download"]))],
) -> ResponseSchema[dict]:
    """下载保单"""
    return ResponseSchema(data={})
