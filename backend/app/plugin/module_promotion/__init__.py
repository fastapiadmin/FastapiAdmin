"""
招生宣传活动管理模块

功能：组织架构管理、人员管理、目标学校管理、活动申请审批、物料管理、
行程报备、费用报销、活动打卡、总结上传、活动撰写、表彰评优
"""

from fastapi import APIRouter

from .activity_apply.controller import ActivityApplyRouter
from .checkin.controller import CheckinRouter
from .document.controller import DocumentRouter
from .evaluation.controller import EvaluationRouter
from .expense.controller import ExpenseRouter
from .material.controller import MaterialRouter
from .personnel.controller import PersonnelRouter
from .summary.controller import SummaryRouter
from .target_school.controller import TargetSchoolRouter
from .team.controller import TeamRouter
from .trip.controller import TripRouter

promotion_router = APIRouter()

promotion_router.include_router(TeamRouter)
promotion_router.include_router(PersonnelRouter)
promotion_router.include_router(TargetSchoolRouter)
promotion_router.include_router(ActivityApplyRouter)
promotion_router.include_router(MaterialRouter)
promotion_router.include_router(TripRouter)
promotion_router.include_router(ExpenseRouter)
promotion_router.include_router(CheckinRouter)
promotion_router.include_router(SummaryRouter)
promotion_router.include_router(DocumentRouter)
promotion_router.include_router(EvaluationRouter)