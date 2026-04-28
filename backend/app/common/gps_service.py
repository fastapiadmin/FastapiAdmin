"""
GPS定位服务

提供GPS坐标验证、距离计算等功能
"""

import math
from typing import Any


class GPSService:
    """
    GPS服务

    提供GPS相关的验证和计算功能
    """

    # 地球半径（米）
    EARTH_RADIUS_METERS = 6371000

    # 默认允许偏差（米）
    DEFAULT_ALLOWED_RADIUS = 500

    @classmethod
    def haversine_distance(
        cls,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """
        使用Haversine公式计算两个GPS坐标之间的距离

        参数:
            lat1 (float): 第一个点的纬度
            lon1 (float): 第一个点的经度
            lat2 (float): 第二个点的纬度
            lon2 (float): 第二个点的经度

        返回:
            float: 两点之间的距离（米）
        """
        # 转换为弧度
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        # Haversine公式
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return cls.EARTH_RADIUS_METERS * c

    @classmethod
    def validate_location(
        cls,
        checkin_latitude: float,
        checkin_longitude: float,
        target_latitude: float,
        target_longitude: float,
        allowed_radius: float | None = None,
    ) -> dict[str, Any]:
        """
        验证打卡位置是否在允许范围内

        参数:
            checkin_latitude (float): 打卡纬度
            checkin_longitude (float): 打卡经度
            target_latitude (float): 目标纬度
            target_longitude (float): 目标经度
            allowed_radius (float | None): 允许半径（米），默认500米

        返回:
            dict: 包含验证结果的字典
                - is_valid (bool): 是否有效
                - distance (float): 实际距离（米）
                - allowed_radius (float): 允许半径（米）
                - message (str): 验证消息
        """
        radius = allowed_radius or cls.DEFAULT_ALLOWED_RADIUS

        # 验证坐标是否有效
        if not cls.validate_coordinate(checkin_latitude, checkin_longitude):
            return {
                "is_valid": False,
                "distance": 0,
                "allowed_radius": radius,
                "message": "打卡坐标无效",
            }

        if not cls.validate_coordinate(target_latitude, target_longitude):
            return {
                "is_valid": False,
                "distance": 0,
                "allowed_radius": radius,
                "message": "目标坐标无效",
            }

        # 计算距离
        distance = cls.haversine_distance(
            checkin_latitude, checkin_longitude, target_latitude, target_longitude
        )

        is_valid = distance <= radius

        if is_valid:
            message = f"打卡位置验证通过，距离目标地点 {distance:.1f} 米"
        else:
            message = f"打卡位置距离目标地点 {distance:.1f} 米，超出允许范围 {radius} 米"

        return {
            "is_valid": is_valid,
            "distance": round(distance, 2),
            "allowed_radius": radius,
            "message": message,
        }

    @classmethod
    def validate_coordinate(cls, latitude: float, longitude: float) -> bool:
        """
        验证GPS坐标是否有效

        参数:
            latitude (float): 纬度
            longitude (float): 经度

        返回:
            bool: 坐标是否有效
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (TypeError, ValueError):
            return False
