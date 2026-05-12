"""
合规诊断 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ComplianceCheckResultSchema,
    ComplianceDiagnosisCreateSchema,
    ComplianceDiagnosisOutSchema,
    ComplianceDiagnosisQuerySchema,
    ComplianceDiagnosisUpdateSchema,
    ComplianceRuleCreateSchema,
    ComplianceRuleOutSchema,
    ComplianceRuleQuerySchema,
    ComplianceRuleUpdateSchema,
)
from .service import ComplianceDiagnosisService, ComplianceRuleService

ComplianceDiagnosisRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/diagnosis",
    tags=["招生咨询会 - 合规诊断"],
)


@ComplianceDiagnosisRouter.get(
    "/detail/{id}",
    summary="获取诊断详情",
    description="获取诊断详情",
    response_model=ResponseSchema[ComplianceDiagnosisOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="诊断ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:detail"]))],
) -> JSONResponse:
    """获取诊断详情"""
    result_dict = await ComplianceDiagnosisService.detail_service(auth=auth, id=id)
    log.info(f"获取诊断详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ComplianceDiagnosisRouter.get(
    "/list",
    summary="查询诊断列表",
    description="查询诊断列表",
    response_model=ResponseSchema[list[ComplianceDiagnosisOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ComplianceDiagnosisQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:query"]))],
) -> JSONResponse:
    """查询诊断列表"""
    result_dict = await ComplianceDiagnosisService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询诊断列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ComplianceDiagnosisRouter.post(
    "/create",
    summary="创建诊断记录",
    description="创建诊断记录",
    response_model=ResponseSchema[ComplianceDiagnosisOutSchema],
)
async def create_obj_controller(
    data: ComplianceDiagnosisCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:create"]))],
) -> JSONResponse:
    """创建诊断记录"""
    result_dict = await ComplianceDiagnosisService.create_service(auth=auth, data=data)
    log.info("创建诊断记录成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ComplianceDiagnosisRouter.put(
    "/update/{id}",
    summary="更新诊断记录",
    description="更新诊断记录",
    response_model=ResponseSchema[ComplianceDiagnosisOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="诊断ID")],
    data: ComplianceDiagnosisUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:update"]))],
) -> JSONResponse:
    """更新诊断记录"""
    result_dict = await ComplianceDiagnosisService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新诊断记录成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ComplianceDiagnosisRouter.delete(
    "/delete/{id}",
    summary="删除诊断记录",
    description="删除诊断记录",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="诊断ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:delete"]))],
) -> JSONResponse:
    """删除诊断记录"""
    await ComplianceDiagnosisService.delete_service(auth=auth, id=id)
    log.info(f"删除诊断记录成功 {id}")
    return SuccessResponse(msg="删除成功")


@ComplianceDiagnosisRouter.delete(
    "/batch-delete",
    summary="批量删除诊断记录",
    description="批量删除诊断记录",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:delete"]))],
) -> JSONResponse:
    """批量删除诊断记录"""
    await ComplianceDiagnosisService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除诊断记录成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ComplianceDiagnosisRouter.get(
    "/latest/{consultation_id}",
    summary="获取最新诊断",
    description="获取某咨询会的最新诊断",
    response_model=ResponseSchema[ComplianceDiagnosisOutSchema],
)
async def get_latest_controller(
    consultation_id: Annotated[int, Path(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:query"]))],
) -> JSONResponse:
    """获取最新诊断"""
    result_dict = await ComplianceDiagnosisService.get_latest_by_consultation_service(
        auth=auth, consultation_id=consultation_id
    )
    log.info(f"获取咨询会 {consultation_id} 最新诊断成功")
    return SuccessResponse(data=result_dict, msg="获取成功")


@ComplianceDiagnosisRouter.post(
    "/check",
    summary="执行合规检查",
    description="执行合规检查并生成诊断",
    response_model=ResponseSchema[ComplianceCheckResultSchema],
)
async def check_compliance_controller(
    consultation_id: Annotated[int, Path(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:create"]))],
) -> JSONResponse:
    """执行合规检查"""
    result_dict = await ComplianceDiagnosisService.check_compliance_service(
        auth=auth, consultation_id=consultation_id
    )
    log.info(f"执行合规检查成功 {consultation_id}")
    return SuccessResponse(data=result_dict, msg="检查成功")


@ComplianceDiagnosisRouter.post(
    "/score/{consultation_id}",
    summary="执行合规评分(v1.0)",
    description="根据主办机构性质对咨询会进行合规性评估和评分(1.0版评分规则)",
    response_model=ResponseSchema[dict],
)
async def score_consultation_controller(
    consultation_id: Annotated[int, Path(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:create"]))],
) -> JSONResponse:
    """
    执行合规评分(v1.0)

    评分规则：
    - 单一省、市、区级官方机构：8-10分
    - 单一高中、高校：5-8分
    - 单一第三方机构：0-3分
    - 多所高中联合、无第三方机构：8-10分
    - 多所高中联合、有第三方机构：6-9分
    - 多家第三方机构：3-6分
    """
    from app.core.database import async_db_session

    from ..info_collection.model import ConsultationInfoModel
    from .scoring_service import ComplianceScoringServiceV1

    async with async_db_session() as session:
        # 获取咨询会信息
        consultation = await session.get(ConsultationInfoModel, consultation_id)
        if not consultation:
            return SuccessResponse(data=None, msg="咨询会不存在")

        # 执行评分
        result = await ComplianceScoringServiceV1.diagnose_consultation(consultation)

        # 保存诊断结果
        await ComplianceScoringServiceV1.save_diagnosis_result(consultation_id, result)

        log.info(f"咨询会 {consultation_id} 合规评分完成: {result.score}分, 等级: {result.level}")

        return SuccessResponse(
            data={
                "consultation_id": consultation_id,
                "score": result.score,
                "level": result.level,
                "is_high_risk": result.is_high_risk,
                "risk_factors": result.risk_factors,
                "improvement_suggestions": result.improvement_suggestions,
                "diagnosis_details": result.diagnosis_details,
            },
            msg="合规评分完成",
        )


@ComplianceDiagnosisRouter.post(
    "/batch-score",
    summary="批量合规评分",
    description="对多个咨询会进行批量合规评分",
    response_model=ResponseSchema[dict],
)
async def batch_score_controller(
    consultation_ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:create"]))],
) -> JSONResponse:
    """
    批量合规评分

    参数:
    - consultation_ids (list[int]): 咨询会ID列表

    返回:
    - JSONResponse: 包含评分结果的JSON响应
    """
    from .scoring_service import ComplianceScoringServiceV1

    results = await ComplianceScoringServiceV1.batch_diagnose_consultations(consultation_ids)

    # 统计结果
    high_risk_count = sum(1 for r in results.values() if r.is_high_risk)
    avg_score = sum(r.score for r in results.values()) / len(results) if results else 0

    log.info(
        f"批量合规评分完成，共{len(results)}条，高风险{high_risk_count}条，平均分{avg_score:.1f}"
    )

    return SuccessResponse(
        data={
            "total_count": len(results),
            "high_risk_count": high_risk_count,
            "average_score": round(avg_score, 1),
            "results": {
                consultation_id: {
                    "score": r.score,
                    "level": r.level,
                    "is_high_risk": r.is_high_risk,
                }
                for consultation_id, r in results.items()
            },
        },
        msg=f"批量评分完成，共{len(results)}条",
    )


ComplianceRuleRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/rule",
    tags=["招生咨询会 - 合规规则"],
)


@ComplianceRuleRouter.get(
    "/detail/{id}",
    summary="获取规则详情",
    description="获取规则详情",
    response_model=ResponseSchema[ComplianceRuleOutSchema],
)
async def get_rule_detail_controller(
    id: Annotated[int, Path(description="规则ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:detail"]))],
) -> JSONResponse:
    """获取规则详情"""
    result_dict = await ComplianceRuleService.detail_service(auth=auth, id=id)
    log.info(f"获取规则详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ComplianceRuleRouter.get(
    "/list",
    summary="查询规则列表",
    description="查询规则列表",
    response_model=ResponseSchema[list[ComplianceRuleOutSchema]],
)
async def get_rule_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ComplianceRuleQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:query"]))],
) -> JSONResponse:
    """查询规则列表"""
    result_dict = await ComplianceRuleService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询规则列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ComplianceRuleRouter.post(
    "/create",
    summary="创建规则",
    description="创建规则",
    response_model=ResponseSchema[ComplianceRuleOutSchema],
)
async def create_rule_controller(
    data: ComplianceRuleCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:create"]))],
) -> JSONResponse:
    """创建规则"""
    result_dict = await ComplianceRuleService.create_service(auth=auth, data=data)
    log.info("创建规则成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ComplianceRuleRouter.put(
    "/update/{id}",
    summary="更新规则",
    description="更新规则",
    response_model=ResponseSchema[ComplianceRuleOutSchema],
)
async def update_rule_controller(
    id: Annotated[int, Path(description="规则ID")],
    data: ComplianceRuleUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:update"]))],
) -> JSONResponse:
    """更新规则"""
    result_dict = await ComplianceRuleService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新规则成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ComplianceRuleRouter.delete(
    "/delete/{id}",
    summary="删除规则",
    description="删除规则",
)
async def delete_rule_controller(
    id: Annotated[int, Path(description="规则ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:delete"]))],
) -> JSONResponse:
    """删除规则"""
    await ComplianceRuleService.delete_service(auth=auth, id=id)
    log.info(f"删除规则成功 {id}")
    return SuccessResponse(msg="删除成功")


@ComplianceRuleRouter.delete(
    "/batch-delete",
    summary="批量删除规则",
    description="批量删除规则",
)
async def batch_delete_rule_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:delete"]))],
) -> JSONResponse:
    """批量删除规则"""
    await ComplianceRuleService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除规则成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ComplianceRuleRouter.post(
    "/toggle/{id}",
    summary="切换启用状态",
    description="切换规则启用状态",
    response_model=ResponseSchema[ComplianceRuleOutSchema],
)
async def toggle_status_controller(
    id: Annotated[int, Path(description="规则ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:compliance:update"]))],
) -> JSONResponse:
    """切换启用状态"""
    result_dict = await ComplianceRuleService.toggle_status_service(auth=auth, id=id)
    log.info(f"切换规则启用状态 {id}")
    return SuccessResponse(data=result_dict, msg="切换成功")
