"""
咨询会信息聚合 - 网络爬虫基础设施

功能：微信公众号渠道抓取（搜狗微信搜索）
"""

from __future__ import annotations

import hashlib
import re
import urllib.parse
from abc import ABC, abstractmethod
from datetime import datetime
from html import unescape
from typing import Any

import httpx

from app.core.logger import log

# 微信公众号抓取固定关键词
WECHAT_SEARCH_KEYWORD = "2026高考咨询会"
WECHAT_SOGOU_SEARCH_URL = "https://weixin.sogou.com/weixin"

_PROVINCES = (
    "北京",
    "天津",
    "上海",
    "重庆",
    "河北",
    "山西",
    "辽宁",
    "吉林",
    "黑龙江",
    "江苏",
    "浙江",
    "安徽",
    "福建",
    "江西",
    "山东",
    "河南",
    "湖北",
    "湖南",
    "广东",
    "海南",
    "四川",
    "贵州",
    "云南",
    "陕西",
    "甘肃",
    "青海",
    "内蒙古",
    "广西",
    "西藏",
    "宁夏",
    "新疆",
    "香港",
    "澳门",
    "台湾",
)


class BaseCrawler(ABC):
    """爬虫基类"""

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
                "Referer": WECHAT_SOGOU_SEARCH_URL,
            },
            follow_redirects=True,
        )

    async def close(self) -> None:
        await self.client.aclose()

    @abstractmethod
    async def fetch(self) -> list[dict[str, Any]]:
        """抓取原始数据"""

    @abstractmethod
    def parse(self, raw_data: dict[str, Any]) -> dict[str, Any] | None:
        """解析单条原始数据为标准格式"""

    async def crawl(self) -> list[dict[str, Any]]:
        try:
            raw_list = await self.fetch()
            parsed_list = []
            for raw in raw_list:
                try:
                    parsed = self.parse(raw)
                    if parsed:
                        parsed["source_type"] = "crawler"
                        parsed["crawl_url"] = raw.get("article_url") or self.source_url
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


_MUNICIPALITIES = frozenset({"北京", "天津", "上海", "重庆"})


def _extract_province(text: str) -> str | None:
    for name in _PROVINCES:
        if name in text:
            if name in _MUNICIPALITIES:
                return f"{name}市"
            if name.endswith(("市", "省", "区")):
                return name
            return f"{name}省"
    return None


def _extract_date(text: str) -> str | None:
    m = re.search(r"(20\d{2})[年\-/](\d{1,2})[月\-/](\d{1,2})", text)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    m = re.search(r"(20\d{2})[年\-/](\d{1,2})[月]?", text)
    if m:
        y, mo = m.groups()
        return f"{y}-{int(mo):02d}-01"
    return None


class WechatOfficialAccountCrawler(BaseCrawler):
    """
    微信公众号渠道爬虫

    通过搜狗微信搜索「2026高考咨询会」相关文章并结构化入库。
    """

    source_name = "wechat_official_account"
    source_url = WECHAT_SOGOU_SEARCH_URL
    search_keyword = WECHAT_SEARCH_KEYWORD
    max_pages = 2

    async def fetch(self) -> list[dict[str, Any]]:
        log.info(f"[{self.source_name}] 微信公众号搜索: {self.search_keyword}")
        articles: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        for page in range(1, self.max_pages + 1):
            params = {
                "type": "2",
                "query": self.search_keyword,
                "ie": "utf8",
                "page": str(page),
            }
            url = f"{self.source_url}?{urllib.parse.urlencode(params)}"
            try:
                resp = await self.client.get(url)
                resp.raise_for_status()
            except Exception as e:
                log.warning(f"[{self.source_name}] 请求第 {page} 页失败: {e}")
                break

            page_items = self._parse_sogou_html(resp.text)
            for item in page_items:
                link = item.get("article_url") or ""
                if not link or link in seen_urls:
                    continue
                seen_urls.add(link)
                articles.append(item)

            if not page_items:
                break

        log.info(f"[{self.source_name}] 共获取 {len(articles)} 条微信文章")
        return articles

    def _parse_sogou_html(self, html: str) -> list[dict[str, Any]]:
        """从搜狗微信搜索结果页解析文章列表"""
        items: list[dict[str, Any]] = []
        blocks = re.split(r"<div[^>]*class=\"[^\"]*txt-box[^\"]*\"[^>]*>", html)
        for block in blocks[1:]:
            title_m = re.search(
                r"<h3[^>]*>\s*<a[^>]*href=\"([^\"]+)\"[^>]*>([\s\S]*?)</a>",
                block,
                re.I,
            )
            if not title_m:
                continue
            href, title_html = title_m.group(1), title_m.group(2)
            title = unescape(re.sub(r"<[^>]+>", "", title_html)).strip()
            if not title or self.search_keyword not in title and "咨询会" not in title:
                continue

            account_m = re.search(
                r"<span[^>]*class=\"[^\"]*all-time-y2[^\"]*\"[^>]*>([^<]+)</span>",
                block,
                re.I,
            )
            account = unescape(account_m.group(1)).strip() if account_m else "微信公众号"

            snippet_m = re.search(
                r"<p[^>]*class=\"[^\"]*txt-info[^\"]*\"[^>]*>([\s\S]*?)</p>",
                block,
                re.I,
            )
            snippet = ""
            if snippet_m:
                snippet = unescape(re.sub(r"<[^>]+>", "", snippet_m.group(1))).strip()

            article_url = (
                href if href.startswith("http") else urllib.parse.urljoin(self.source_url, href)
            )

            items.append({
                "title": title,
                "article_url": article_url,
                "account_name": account,
                "snippet": snippet,
                "search_keyword": self.search_keyword,
            })

        if items:
            return items

        # 降级：整页正则匹配标题链接
        for href, title_html in re.findall(
            r"<a[^>]*href=\"([^\"]+)\"[^>]*uigs=\"article_title[^\"]*\"[^>]*>([\s\S]*?)</a>",
            html,
            re.I,
        ):
            title = unescape(re.sub(r"<[^>]+>", "", title_html)).strip()
            if not title or ("咨询会" not in title and self.search_keyword not in title):
                continue
            article_url = (
                href if href.startswith("http") else urllib.parse.urljoin(self.source_url, href)
            )
            items.append({
                "title": title,
                "article_url": article_url,
                "account_name": "微信公众号",
                "snippet": "",
                "search_keyword": self.search_keyword,
            })
        return items

    def parse(self, raw_data: dict[str, Any]) -> dict[str, Any] | None:
        title = (raw_data.get("title") or "").strip()
        if not title:
            return None

        snippet = (raw_data.get("snippet") or "").strip()
        account = (raw_data.get("account_name") or "微信公众号").strip()
        combined = f"{title} {snippet}"
        province = _extract_province(combined)
        start_date = _extract_date(combined) or "2026-06-01"
        article_url = raw_data.get("article_url") or self.source_url
        external_id = hashlib.md5(article_url.encode("utf-8")).hexdigest()

        organizer = account if account != "微信公众号" else "微信公众号"
        if province:
            auto_title = f"{province}-{title[:80]}"
        else:
            auto_title = title[:200]

        return {
            "title": auto_title[:200],
            "organizer": organizer[:200],
            "organizer_nature": "third_party_single",
            "start_date": start_date,
            "province": province,
            "city": province,
            "address": snippet[:500] if snippet else None,
            "guidance_unit": account,
            "event_time_text": snippet[:2000] if snippet else None,
            "fee_description": None,
            "source_url": article_url,
            "external_id": external_id,
            "description": f"渠道：微信公众号\n关键词：{self.search_keyword}\n{snippet}".strip(),
            "search_keywords": f"{self.search_keyword} {title} {account} {province or ''}".strip(),
        }


class CrawlerRegistry:
    """爬虫注册表"""

    _crawlers: dict[str, BaseCrawler] = {}

    @classmethod
    def register(cls, name: str, crawler: BaseCrawler) -> None:
        cls._crawlers[name] = crawler
        log.info(f"爬虫已注册: {name}")

    @classmethod
    def get(cls, name: str) -> BaseCrawler | None:
        return cls._crawlers.get(name)

    @classmethod
    def list_crawlers(cls) -> list[str]:
        return list(cls._crawlers.keys())

    @classmethod
    async def run(cls, names: list[str] | None = None) -> dict[str, list[dict[str, Any]]]:
        """运行指定爬虫（默认全部已注册）"""
        targets = names if names is not None else list(cls._crawlers.keys())
        results: dict[str, list[dict[str, Any]]] = {}
        for name in targets:
            crawler = cls._crawlers.get(name)
            if not crawler:
                log.warning(f"爬虫未注册: {name}")
                results[name] = []
                continue
            try:
                results[name] = await crawler.crawl()
            except Exception as e:
                log.error(f"爬虫 {name} 执行失败: {e}", exc_info=True)
                results[name] = []
        return results


CrawlerRegistry.register("wechat_official_account", WechatOfficialAccountCrawler())
