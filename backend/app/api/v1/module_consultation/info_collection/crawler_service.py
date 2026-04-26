"""
咨询会信息爬虫服务

提供全网抓取高招类咨询会信息的功能
"""
import asyncio
import random
from datetime import date, timedelta
from typing import Any

from app.core.logger import log

from .model import ConsultationInfoModel, InfoSource, InfoStatus, OrganizerNature


class ConsultationCrawlerService:
    """
    咨询会信息爬虫服务

    模拟全网抓取高招类咨询会信息
    实际项目中应替换为真实的爬虫实现
    """

    # 模拟数据源
    MOCK_PROVINCES = [
        "北京", "上海", "广东", "江苏", "浙江", "山东", "河南", "四川",
        "湖北", "湖南", "河北", "福建", "安徽", "辽宁", "陕西", "重庆"
    ]

    MOCK_CITIES = {
        "北京": ["北京市"],
        "上海": ["上海市"],
        "广东": ["广州", "深圳", "佛山", "东莞"],
        "江苏": ["南京", "苏州", "无锡", "常州"],
        "浙江": ["杭州", "宁波", "温州", "绍兴"],
        "山东": ["济南", "青岛", "烟台", "潍坊"],
    }

    MOCK_ORGANIZERS = [
        {"name": "北京市教育考试院", "nature": OrganizerNature.OFFICIAL_SINGLE, "score_range": (8, 10)},
        {"name": "山东省教育厅", "nature": OrganizerNature.OFFICIAL_SINGLE, "score_range": (8, 10)},
        {"name": "江苏省高校招生就业指导服务中心", "nature": OrganizerNature.OFFICIAL_SINGLE, "score_range": (8, 10)},
        {"name": "衡水中学", "nature": OrganizerNature.HIGH_SCHOOL_SINGLE, "score_range": (5, 8)},
        {"name": "人大附中", "nature": OrganizerNature.HIGH_SCHOOL_SINGLE, "score_range": (5, 8)},
        {"name": "黄冈中学", "nature": OrganizerNature.HIGH_SCHOOL_SINGLE, "score_range": (5, 8)},
        {"name": "清华大学", "nature": OrganizerNature.UNIVERSITY_SINGLE, "score_range": (5, 8)},
        {"name": "北京大学", "nature": OrganizerNature.UNIVERSITY_SINGLE, "score_range": (5, 8)},
        {"name": "复旦大学", "nature": OrganizerNature.UNIVERSITY_SINGLE, "score_range": (5, 8)},
        {"name": "新东方教育科技集团", "nature": OrganizerNature.THIRD_PARTY_SINGLE, "score_range": (0, 3)},
        {"name": "学而思教育", "nature": OrganizerNature.THIRD_PARTY_SINGLE, "score_range": (0, 3)},
        {"name": "北京四中、人大附中、北师大附中联合举办", "nature": OrganizerNature.HIGH_SCHOOL_UNION, "score_range": (8, 10)},
        {"name": "南京外国语学校、南师附中、金陵中学联合举办", "nature": OrganizerNature.HIGH_SCHOOL_UNION, "score_range": (8, 10)},
        {"name": "杭州二中、学军中学、杭十四中联合举办", "nature": OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD, "score_range": (6, 9)},
        {"name": "成都七中、树德中学、石室中学联合举办", "nature": OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD, "score_range": (6, 9)},
        {"name": "中国教育在线、新浪教育、腾讯教育联合举办", "nature": OrganizerNature.THIRD_PARTY_MULTIPLE, "score_range": (3, 6)},
    ]

    MOCK_TITLES = [
        "{province}2024年高招咨询会",
        "{city}高校招生咨询会",
        "{province}省重点高校招生宣讲会",
        "{city}市高考志愿填报咨询会",
        "{province}省2024年普通高校招生咨询会",
        "{city}高招咨询会暨志愿填报指导会",
    ]

    @classmethod
    async def crawl_consultation_info(cls, days_ahead: int = 30) -> list[dict[str, Any]]:
        """
        抓取咨询会信息

        参数:
        - days_ahead (int): 抓取未来多少天的咨询会信息

        返回:
        - list[dict]: 抓取的咨询会信息列表
        """
        log.info(f"开始抓取未来{days_ahead}天的咨询会信息...")

        # 模拟抓取延迟
        await asyncio.sleep(random.uniform(1, 3))

        results = []
        num_results = random.randint(5, 15)  # 每次抓取5-15条

        for _ in range(num_results):
            info = cls._generate_mock_consultation(days_ahead)
            results.append(info)

        log.info(f"成功抓取{len(results)}条咨询会信息")
        return results

    @classmethod
    def _generate_mock_consultation(cls, days_ahead: int) -> dict[str, Any]:
        """生成模拟咨询会数据"""
        province = random.choice(cls.MOCK_PROVINCES)
        city = random.choice(cls.MOCK_CITIES.get(province, [province]))

        organizer_info = random.choice(cls.MOCK_ORGANIZERS)

        # 生成日期
        days_offset = random.randint(1, days_ahead)
        start_date = date.today() + timedelta(days=days_offset)

        # 生成标题
        title_template = random.choice(cls.MOCK_TITLES)
        title = title_template.format(province=province, city=city)

        # 判断是否有第三方机构
        has_third_party = organizer_info["nature"] in [
            OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD,
            OrganizerNature.THIRD_PARTY_MULTIPLE,
            OrganizerNature.THIRD_PARTY_SINGLE
        ]

        # 生成参与高校列表
        university_count = random.randint(10, 100)
        participating_universities = [
            {"name": f"大学{i}", "level": random.choice(["985", "211", "普通本科"])}
            for i in range(min(university_count, 20))  # 最多存20个示例
        ]

        return {
            "title": title,
            "description": f"{title}，欢迎广大考生和家长参加。届时将有{university_count}所高校招生负责人现场解答招生政策、专业设置、录取分数线等问题。",
            "organizer": organizer_info["name"],
            "organizer_type": cls._get_organizer_type(organizer_info["nature"]),
            "organizer_nature": organizer_info["nature"].value,
            "organizer_detail": {
                "nature": organizer_info["nature"].value,
                "expected_score_min": organizer_info["score_range"][0],
                "expected_score_max": organizer_info["score_range"][1],
            },
            "has_third_party": has_third_party,
            "third_party_info": cls._generate_third_party_info(has_third_party, organizer_info["nature"]),
            "start_date": start_date,
            "end_date": start_date,  # 单日活动
            "start_time": "09:00",
            "end_time": "17:00",
            "province": province,
            "city": city,
            "district": random.choice(["朝阳区", "海淀区", "浦东新区", "天河区", ""]),
            "address": f"{city}{random.choice(['国际会展中心', '体育馆', '会议中心', '学校操场'])}",
            "participating_universities": participating_universities,
            "university_count": university_count,
            "estimated_visitors": random.randint(1000, 10000),
            "booth_fee": random.choice([0, 500, 800, 1000, 1500, 2000]),
            "source_type": InfoSource.CRAWLER.value,
            "source_url": f"https://example.com/consultation/{random.randint(10000, 99999)}",
            "status": InfoStatus.PENDING.value,
        }

    @classmethod
    def _get_organizer_type(cls, nature: OrganizerNature) -> str:
        """根据机构性质获取机构类型"""
        type_mapping = {
            OrganizerNature.OFFICIAL_SINGLE: "教育部门",
            OrganizerNature.HIGH_SCHOOL_SINGLE: "中学",
            OrganizerNature.UNIVERSITY_SINGLE: "高校",
            OrganizerNature.THIRD_PARTY_SINGLE: "机构",
            OrganizerNature.HIGH_SCHOOL_UNION: "中学",
            OrganizerNature.HIGH_SCHOOL_UNION_WITH_THIRD: "中学",
            OrganizerNature.THIRD_PARTY_MULTIPLE: "机构",
        }
        return type_mapping.get(nature, "其他")

    @classmethod
    def _generate_third_party_info(cls, has_third_party: bool, nature: OrganizerNature) -> dict | None:
        """生成第三方机构信息"""
        if not has_third_party:
            return None

        third_parties = [
            {"name": "中国教育在线", "type": "教育媒体"},
            {"name": "新浪教育", "type": "互联网媒体"},
            {"name": "腾讯教育", "type": "互联网媒体"},
            {"name": "高考志愿填报指导中心", "type": "咨询服务"},
        ]

        if nature == OrganizerNature.THIRD_PARTY_SINGLE:
            return {"primary": random.choice(third_parties)}
        elif nature == OrganizerNature.THIRD_PARTY_MULTIPLE:
            return {
                "primary": random.choice(third_parties),
                "secondary": random.sample(third_parties, k=random.randint(1, 2))
            }
        else:
            return {"primary": random.choice(third_parties)}

    @classmethod
    async def save_crawled_data(cls, data_list: list[dict[str, Any]]) -> int:
        """
        保存抓取的数据到数据库

        参数:
        - data_list (list[dict]): 抓取的咨询会信息列表

        返回:
        - int: 保存成功的记录数
        """
        from app.core.database import async_session

        saved_count = 0
        async with async_session() as session:
            for data in data_list:
                try:
                    # 检查是否已存在相同标题和日期的咨询会
                    existing = await cls._check_existing(session, data["title"], data["start_date"])
                    if existing:
                        log.debug(f"咨询会已存在，跳过: {data['title']}")
                        continue

                    # 创建新记录
                    obj = ConsultationInfoModel(**data)
                    session.add(obj)
                    saved_count += 1

                except Exception as e:
                    log.error(f"保存咨询会信息失败: {e}")
                    continue

            await session.commit()

        log.info(f"成功保存{saved_count}条咨询会信息")
        return saved_count

    @classmethod
    async def _check_existing(cls, session, title: str, start_date: date) -> bool:
        """检查是否已存在相同的咨询会"""
        from sqlalchemy import select
        result = await session.execute(
            select(ConsultationInfoModel).where(
                ConsultationInfoModel.title == title,
                ConsultationInfoModel.start_date == start_date
            )
        )
        return result.scalar_one_or_none() is not None


async def run_crawler_task():
    """
    定时任务：运行爬虫抓取咨询会信息

    建议配置：每天凌晨2点执行
    """
    log.info("开始执行咨询会信息抓取定时任务...")

    try:
        # 抓取数据
        data_list = await ConsultationCrawlerService.crawl_consultation_info(days_ahead=60)

        # 保存数据
        saved_count = await ConsultationCrawlerService.save_crawled_data(data_list)

        log.info(f"咨询会信息抓取任务完成，新增{saved_count}条记录")

    except Exception as e:
        log.error(f"咨询会信息抓取任务失败: {e}")
        raise
