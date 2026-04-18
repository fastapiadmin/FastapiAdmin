"""
招生咨询会管理模块

功能：全网聚合招生咨询会信息，智能筛选匹配，一键生成行程方案
"""

from .info_collection import controller as info_collection_controller
from .screening import controller as screening_controller
from .itinerary import controller as itinerary_controller
from .registration import controller as registration_controller
from .compliance import controller as compliance_controller

__all__ = [
    "info_collection_controller",
    "screening_controller",
    "itinerary_controller",
    "registration_controller",
    "compliance_controller",
]
