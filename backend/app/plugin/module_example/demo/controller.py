import urllib.parse
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import DemoCreateSchema, DemoOutSchema, DemoQueryParam, DemoUpdateSchema
from .service import DemoService

DemoRouter = APIRouter(route_class=OperationLogRoute, prefix="/demo", tags=["开发工具", "示例"])


@DemoRouter.get(
    "/detail/{id}",
    summary="获取示例详情",
    response_model=ResponseSchema[DemoOutSchema],
)
async def get_obj_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:detail"]))],
    id: Annotated[int, Path(description="示例ID")],
) -> JSONResponse:
    service = DemoService(auth)
    result_dict = await service.detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取示例详情成功")


@DemoRouter.get(
    "/list",
    summary="分页查询示例",
    response_model=ResponseSchema[PageResultSchema[DemoOutSchema]],
)
async def get_obj_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[DemoQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    service = DemoService(auth)
    result_dict = await service.page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询示例列表成功")


@DemoRouter.post(
    "/create",
    summary="创建示例",
    response_model=ResponseSchema[DemoOutSchema],
)
async def create_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:create"]))],
    data: Annotated[DemoCreateSchema, Body(description="创建参数")],
) -> JSONResponse:
    service = DemoService(auth)
    result_dict = await service.create(data=data)
    return SuccessResponse(data=result_dict, msg="创建示例成功")


@DemoRouter.put(
    "/update/{id}",
    summary="修改示例",
    response_model=ResponseSchema[DemoOutSchema],
)
async def update_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:update"]))],
    id: Annotated[int, Path(description="示例ID")],
    data: Annotated[DemoUpdateSchema, Body(description="修改参数")],
) -> JSONResponse:
    service = DemoService(auth)
    result_dict = await service.update(id=id, data=data)
    return SuccessResponse(data=result_dict, msg="修改示例成功")


@DemoRouter.delete(
    "/delete",
    summary="删除示例",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    service = DemoService(auth)
    await service.delete(ids=ids)
    return SuccessResponse(msg="删除示例成功")


@DemoRouter.patch(
    "/status/batch",
    summary="批量修改示例状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:patch"]))],
) -> JSONResponse:
    service = DemoService(auth)
    await service.set_available(data=data)
    return SuccessResponse(msg="批量修改示例状态成功")


@DemoRouter.post(
    "/export",
    summary="导出示例",
)
async def export_obj_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:export"]))],
    search: Annotated[DemoQueryParam, Query(description="查询参数")],
) -> StreamingResponse:
    service = DemoService(auth)
    result_dict_list = await service.get_list(search=search)
    export_result = DemoService.batch_export(obj_list=result_dict_list)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=demo.xlsx"},
    )


@DemoRouter.post(
    "/import",
    summary="导入示例",
    response_model=ResponseSchema[str],
)
async def import_obj_list_controller(
    file: Annotated[UploadFile, File(description="导入文件")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_example:demo:import"]))],
) -> JSONResponse:
    service = DemoService(auth)
    batch_import_result = await service.batch_import(
        file=file, update_support=True
    )
    return SuccessResponse(data=batch_import_result, msg="导入示例成功")


@DemoRouter.post(
    "/download/template",
    summary="获取示例导入模板",
    dependencies=[Depends(AuthPermission(["module_example:demo:download"]))],
)
async def export_obj_template_controller() -> StreamingResponse:
    import_template_result = DemoService.import_template_download()

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={urllib.parse.quote('示例导入模板.xlsx')}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
