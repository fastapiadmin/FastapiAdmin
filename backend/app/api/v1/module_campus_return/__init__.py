"""
学生返校宣讲管理系统

功能：大学生寒假返母校宣讲活动的全链条管理系统
包括批次管理、报名管理、团队管理、培训考核、物料领取、保险管理、高中对接、行程管理、打卡总结、志愿服务时长、表彰评优等
"""

from fastapi import APIRouter

from .award.controller import AwardRouter
from .batch.controller import BatchRouter
from .checkin.controller import CheckInRouter
from .highschool.controller import HighSchoolRouter
from .insurance.controller import InsuranceRouter
from .itinerary.controller import ItineraryRouter
from .material.controller import MaterialRouter
from .registration.controller import RegistrationRouter
from .team.controller import TeamRouter
from .training.controller import TrainingRouter
from .volunteer.controller import VolunteerRouter

campus_return_router = APIRouter()

campus_return_router.include_router(BatchRouter)
campus_return_router.include_router(RegistrationRouter)
campus_return_router.include_router(TeamRouter)
campus_return_router.include_router(TrainingRouter)
campus_return_router.include_router(MaterialRouter)
campus_return_router.include_router(InsuranceRouter)
campus_return_router.include_router(HighSchoolRouter)
campus_return_router.include_router(ItineraryRouter)
campus_return_router.include_router(CheckInRouter)
campus_return_router.include_router(VolunteerRouter)
campus_return_router.include_router(AwardRouter)

__all__ = ["campus_return_router"]
