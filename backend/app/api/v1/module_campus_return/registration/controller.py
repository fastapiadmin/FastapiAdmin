"""
报名管理 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

RegistrationRouter = APIRouter(prefix="/registration", tags=["报名管理"])


@RegistrationRouter.get("", summary="报名列表")
async def list_registration_controller(
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:query"]))
    ],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取报名列表"""
    return ResponseSchema(data=[])


@RegistrationRouter.get("/{registration_id}", summary="报名详情")
async def get_registration_controller(
    registration_id: Annotated[int, Path(description="报名ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:query"]))
    ],
) -> ResponseSchema[dict]:
    """获取单个报名详情"""
    return ResponseSchema(data={})


@RegistrationRouter.post("", summary="创建报名")
async def create_registration_controller(
    data: dict,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:create"]))
    ],
) -> ResponseSchema[dict]:
    """创建报名"""
    return ResponseSchema(data={})


@RegistrationRouter.put("/{registration_id}", summary="更新报名")
async def update_registration_controller(
    registration_id: Annotated[int, Path(description="报名ID")],
    data: dict,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:update"]))
    ],
) -> ResponseSchema[dict]:
    """更新报名"""
    return ResponseSchema(data={})


@RegistrationRouter.delete("/{registration_id}", summary="删除报名")
async def delete_registration_controller(
    registration_id: Annotated[int, Path(description="报名ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:delete"]))
    ],
) -> ResponseSchema[bool]:
    """删除报名"""
    return ResponseSchema(data=True)


@RegistrationRouter.post("/{registration_id}/review", summary="审核报名")
async def review_registration_controller(
    registration_id: Annotated[int, Path(description="报名ID")],
    data: dict,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_campus_return:registration:review"]))
    ],
) -> ResponseSchema[dict]:
    """审核报名"""
    return ResponseSchema(data={})
