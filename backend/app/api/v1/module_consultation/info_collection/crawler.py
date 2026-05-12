"""
咨询会信息聚合 - 网络爬虫基础设施

功能：提供基础爬虫抽象类和咨询会信息抓取实现
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import httpx

from app.core.logger import log


class BaseCrawler(ABC):
    """
    爬虫基类

    子类需实现:
    - source_name: 来源名称
    - source_url: 来源基础URL
    - fetch(): 抓取数据并返回结构化列表
    - parse(): 解析原始数据为标准格式
    """

    source_name: str = ""
    source_url: str = ""
    timeout: int = 30

    def __init__(self) -> None:
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            },
        )

    async def close(self) -> None:
        """关闭 HTTP 客户端"""
        await self.client.aclose()

    @abstractmethod
    async def fetch(self) -> list[dict[str, Any]]:
        """
        抓取原始数据

        返回:
        - list[dict]: 原始数据列表
        """

    @abstractmethod
    def parse(self, raw_data: dict[str, Any]) -> dict[str, Any] | None:
        """
        解析单条原始数据为标准格式

        标准格式字段:
        - title (str): 咨询会标题
        - organizer (str): 主办方
        - organizer_nature (str): 主办机构性质
        - start_date (str): 开始日期 (YYYY-MM-DD)
        - end_date (str | None): 结束日期
        - province (str): 省份
        - city (str): 城市
        - address (str | None): 详细地址
        - venue_name (str | None): 场馆名称
        - booth_fee (float | None): 展位费用
        - fee_description (str | None): 费用说明
        - registration_email (str | None): 报名邮箱
        - source_url (str | None): 来源链接
        - external_id (str | None): 外部系统ID(用于去重)
        - description (str | None): 描述

        返回:
        - dict | None: 解析后的标准数据，解析失败返回 None
        """

    async def crawl(self) -> list[dict[str, Any]]:
        """
        完整抓取流程: fetch + parse

        返回:
        - list[dict]: 解析后的标准数据列表
        """
        try:
            raw_list = await self.fetch()
            parsed_list = []
            for raw in raw_list:
                try:
                    parsed = self.parse(raw)
                    if parsed:
                        parsed["source_type"] = "crawler"
                        parsed["crawl_url"] = self.source_url
                        parsed["crawl_time"] = datetime.now().isoformat()
                        parsed_list.append(parsed)
                except Exception as e:
                    log.warning(f"[{self.source_name}] 解析单条数据失败: {e}")
            log.info(
                f"[{self.source_name}] 抓取完成: 原始 {len(raw_list)} 条，有效 {len(parsed_list)} 条"
            )
            return parsed_list
        except Exception as e:
            log.error(f"[{self.source_name}] 抓取失败: {e}", exc_info=True)
            return []
        finally:
            await self.close()


class MockConsultationCrawler(BaseCrawler):
    """
    模拟爬虫 - 用于演示和测试

    实际生产环境应替换为真实的数据源爬虫
    """

    source_name = "mock_consultation_source"
    source_url = "https://example.com/consultations"

    async def fetch(self) -> list[dict[str, Any]]:
        """模拟抓取数据"""
        log.info(f"[{self.source_name}] 开始模拟抓取...")
        return [
            {
                "title": "2026年河北省高招咨询会",
                "organizer": "河北省教育考试院",
                "organizer_nature": "official_single",
                "start_date": "2026-06-20",
                "end_date": "2026-06-21",
                "province": "河北省",
                "city": "石家庄市",
                "address": "石家庄国际会展中心",
                "venue_name": "石家庄国际会展中心",
                "booth_fee": 2000.0,
                "fee_description": "标准展位费用",
                "registration_email": "consultation@example.com",
                "external_id": "mock_001",
                "description": "河北省年度高招咨询会",
            },
            {
                "title": "2026年天津市高校招生咨询会",
                "organizer": "天津市教育招生考试院",
                "organizer_nature": "official_single",
                "start_date": "2026-06-15",
                "end_date": None,
                "province": "天津市",
                "city": "天津市",
                "address": "天津梅江会展中心",
                "venue_name": "天津梅江会展中心",
                "booth_fee": 1500.0,
                "fee_description": "普通展位",
                "registration_email": "tjconsult@example.com",
                "external_id": "mock_002",
                "description": "天津市高校招生咨询会",
            },
        ]

    def parse(self, raw_data: dict[str, Any]) -> dict[str, Any] | None:
        """解析模拟数据"""
        required_fields = ["title", "organizer", "start_date", "province", "city"]
        for field in required_fields:
            if not raw_data.get(field):
                log.warning(f"[{self.source_name}] 缺少必填字段: {field}")
                return None
        return {
            "title": raw_data["title"],
            "organizer": raw_data["organizer"],
            "organizer_nature": raw_data.get("organizer_nature"),
            "start_date": raw_data["start_date"],
            "end_date": raw_data.get("end_date"),
            "province": raw_data["province"],
            "city": raw_data["city"],
            "address": raw_data.get("address"),
            "venue_name": raw_data.get("venue_name"),
            "booth_fee": raw_data.get("booth_fee"),
            "fee_description": raw_data.get("fee_description"),
            "registration_email": raw_data.get("registration_email"),
            "source_url": raw_data.get("source_url") or self.source_url,
            "external_id": raw_data.get("external_id"),
            "description": raw_data.get("description"),
        }


class CrawlerRegistry:
    """
    爬虫注册表

    管理所有可用的爬虫实例
    """

    _crawlers: dict[str, BaseCrawler] = {}

    @classmethod
    def register(cls, name: str, crawler: BaseCrawler) -> None:
        """注册爬虫"""
        cls._crawlers[name] = crawler
        log.info(f"爬虫已注册: {name}")

    @classmethod
    def get(cls, name: str) -> BaseCrawler | None:
        """获取爬虫实例"""
        return cls._crawlers.get(name)

    @classmethod
    def list_crawlers(cls) -> list[str]:
        """列出所有已注册的爬虫名称"""
        return list(cls._crawlers.keys())

    @classmethod
    async def run_all(cls) -> dict[str, list[dict[str, Any]]]:
        """
        运行所有已注册的爬虫

        返回:
        - dict: {爬虫名称: 抓取结果列表}
        """
        results = {}
        for name, crawler in cls._crawlers.items():
            try:
                results[name] = await crawler.crawl()
            except Exception as e:
                log.error(f"爬虫 {name} 执行失败: {e}", exc_info=True)
                results[name] = []
        return results


# 注册默认爬虫
CrawlerRegistry.register("mock_consultation", MockConsultationCrawler())
