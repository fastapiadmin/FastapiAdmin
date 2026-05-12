"""
高校信息管理模块
"""

from .controller import UniversityRouter
from .model import UniversityModel
from .schema import (
    UniversityCreateSchema,
    UniversityOutSchema,
    UniversityQuerySchema,
    UniversityUpdateSchema,
)

__all__ = [
    "UniversityRouter",
    "UniversityModel",
    "UniversityCreateSchema",
    "UniversityUpdateSchema",
    "UniversityOutSchema",
    "UniversityQuerySchema",
]
