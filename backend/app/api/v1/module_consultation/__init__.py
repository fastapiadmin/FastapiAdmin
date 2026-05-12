"""
招生咨询会管理模块

功能：全网聚合招生咨询会信息，智能筛选匹配，一键生成行程方案
"""

from fastapi import APIRouter

from .compliance.controller import ComplianceDiagnosisRouter, ComplianceRuleRouter
from .info_collection.controller import InfoCollectionRouter
from .itinerary.controller import ItineraryRouter
from .registration.controller import RegistrationRouter
from .screening.controller import ScreeningRouter
from .university.controller import UniversityRouter

consultation_router = APIRouter()

# 注册咨询会信息聚合路由
consultation_router.include_router(InfoCollectionRouter)

# 注册智能筛选路由
consultation_router.include_router(ScreeningRouter)

# 注册行程规划路由
consultation_router.include_router(ItineraryRouter)

# 注册报名管理路由
consultation_router.include_router(RegistrationRouter)

# 注册合规诊断路由
consultation_router.include_router(ComplianceDiagnosisRouter)
consultation_router.include_router(ComplianceRuleRouter)

# 注册高校管理路由
consultation_router.include_router(UniversityRouter)

__all__ = ["consultation_router"]
