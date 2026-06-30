from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    InvoiceApplySchema,
    InvoiceIssueSchema,
    InvoiceOutSchema,
    InvoiceQueryParam,
    InvoiceVoidSchema,
)
from .service import InvoicePlatformService, InvoiceTenantService

TenantInvoiceRouter = APIRouter(prefix="/tenant/invoice", route_class=OperationLogRoute, tags=["平台管理", "发票管理"])


@TenantInvoiceRouter.post("/apply", summary="申请开票", response_model=ResponseSchema[InvoiceOutSchema])
async def invoice_apply_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    data: Annotated[InvoiceApplySchema, Body(description="发票申请参数")],
) -> JSONResponse:
    result = await InvoiceTenantService.apply(auth, data, auth.tenant_id)
    return SuccessResponse(data=result, msg="发票申请成功")


@TenantInvoiceRouter.get("/list", summary="我的发票列表", response_model=ResponseSchema[PageResultSchema[InvoiceOutSchema]])
async def invoice_list_my_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[InvoiceQueryParam, Query(description="发票查询参数")],
) -> JSONResponse:
    result = await InvoiceTenantService.list_my(
        auth=auth,
        tenant_id=auth.tenant_id,
        page_no=page.page_no,
        page_size=page.page_size,
        order_by=page.order_by,
        search=search,
    )
    return SuccessResponse(data=result, msg="查询成功")


@TenantInvoiceRouter.get("/{id}/download", summary="下载发票PDF与授权函", response_model=ResponseSchema[dict])
async def invoice_download_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    id: Annotated[int, Path(description="发票ID", ge=1)],
) -> JSONResponse:
    pdf_url = await InvoiceTenantService.download(auth, id, auth.tenant_id)
    oss_license_pdf_url = await InvoiceTenantService.download_license(auth, id, auth.tenant_id)
    return SuccessResponse(
        msg="下载地址",
        data={"pdf_url": pdf_url, "oss_license_pdf_url": oss_license_pdf_url},
    )


@TenantInvoiceRouter.get("/{id}/license/download", summary="下载开源授权函PDF", response_model=ResponseSchema[dict])
async def invoice_license_download_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    id: Annotated[int, Path(description="发票ID", ge=1)],
) -> JSONResponse:
    oss_license_pdf_url = await InvoiceTenantService.download_license(auth, id, auth.tenant_id)
    return SuccessResponse(msg="授权函下载地址", data={"oss_license_pdf_url": oss_license_pdf_url})


PlatformInvoiceRouter = APIRouter(prefix="/invoice", route_class=OperationLogRoute, tags=["平台管理", "发票管理"])


@PlatformInvoiceRouter.get("/list", summary="全部发票列表", response_model=ResponseSchema[PageResultSchema[InvoiceOutSchema]])
async def invoice_list_all_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[InvoiceQueryParam, Query(description="发票查询参数")],
) -> JSONResponse:
    result = await InvoicePlatformService.list_all(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        order_by=page.order_by,
        search=search,
    )
    return SuccessResponse(data=result, msg="查询成功")


@PlatformInvoiceRouter.put("/issue/{id}", summary="开具发票", response_model=ResponseSchema[InvoiceOutSchema])
async def invoice_issue_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    id: Annotated[int, Path(description="发票ID", ge=1)],
    data: Annotated[InvoiceIssueSchema, Body(description="发票开具参数")],
) -> JSONResponse:
    result = await InvoicePlatformService.issue(
        auth,
        id,
        data.pdf_url or "",
        data.api_response or "",
        data.oss_license_pdf_url or "",
    )
    return SuccessResponse(data=result, msg="发票开具成功")


@PlatformInvoiceRouter.put("/void/{id}", summary="作废发票", response_model=ResponseSchema[InvoiceOutSchema])
async def invoice_void_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["*:*:*"]))],
    id: Annotated[int, Path(description="发票ID", ge=1)],
    data: Annotated[InvoiceVoidSchema, Body(description="发票作废参数")] = InvoiceVoidSchema(),
) -> JSONResponse:
    result = await InvoicePlatformService.void(auth, id, data)
    return SuccessResponse(data=result, msg="发票已作废")
