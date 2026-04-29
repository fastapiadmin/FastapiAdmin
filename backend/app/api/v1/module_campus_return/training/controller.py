"""
培训考核 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

TrainingRouter = APIRouter(prefix="/training", tags=["培训考核"])


@TrainingRouter.get("/courses", summary="课程列表")
async def list_courses_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:training:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取培训课程列表"""
    return ResponseSchema(data=[])


@TrainingRouter.get("/courses/{course_id}", summary="课程详情")
async def get_course_controller(
    course_id: Annotated[int, Path(description="课程ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:training:query"]))],
) -> ResponseSchema[dict]:
    """获取单个课程详情"""
    return ResponseSchema(data={})


@TrainingRouter.post("/courses", summary="创建课程")
async def create_course_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:training:create"]))],
) -> ResponseSchema[dict]:
    """创建培训课程"""
    return ResponseSchema(data={})


@TrainingRouter.put("/courses/{course_id}", summary="更新课程")
async def update_course_controller(
    course_id: Annotated[int, Path(description="课程ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:training:update"]))],
) -> ResponseSchema[dict]:
    """更新培训课程"""
    return ResponseSchema(data={})


@TrainingRouter.delete("/courses/{course_id}", summary="删除课程")
async def delete_course_controller(
    course_id: Annotated[int, Path(description="课程ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:training:delete"]))],
) -> ResponseSchema[bool]:
    """删除培训课程"""
    return ResponseSchema(data=True)
