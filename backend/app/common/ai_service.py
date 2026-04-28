"""
通用AI服务

提供异步AI内容生成功能，支持OpenAI兼容API
"""

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

from app.config.setting import settings
from app.core.logger import log


class AIService:
    """
    异步AI服务

    使用 httpx 调用 OpenAI 兼容 API 生成内容
    """

    @classmethod
    async def generate_content(
        cls,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        生成内容

        参数:
            prompt (str): 用户提示词
            system_prompt (str | None): 系统提示词
            temperature (float): 温度参数，控制随机性
            max_tokens (int): 最大生成token数

        返回:
            str: 生成的内容
        """
        if not HAS_HTTPX:
            raise ImportError("httpx is required for AI service")

        if not settings.OPENAI_API_KEY or not settings.OPENAI_BASE_URL:
            raise ValueError("AI服务未配置，请检查 OPENAI_BASE_URL 和 OPENAI_API_KEY 配置")

        system_msg = (
            system_prompt
            or "你是一个专业的招生宣传活动文案撰写专家，擅长撰写适合微信公众号发布的宣传文章。"
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ]

        payload = {
            "model": settings.OPENAI_MODEL or "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{settings.OPENAI_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            log.error(f"AI服务HTTP错误: {e.response.status_code} - {e.response.text}")
            raise Exception(f"AI服务请求失败: {e.response.status_code}")
        except Exception as e:
            log.error(f"AI服务调用异常: {str(e)}")
            raise Exception(f"AI服务调用异常: {str(e)}")

    @classmethod
    async def generate_wechat_content(
        cls,
        title: str,
        content: str,
        summary: str | None = None,
        activity_name: str | None = None,
    ) -> str:
        """
        生成微信公众号格式化内容

        参数:
            title (str): 文档标题
            content (str): 原始内容
            summary (str | None): 摘要
            activity_name (str | None): 活动名称

        返回:
            str: 格式化后的HTML内容
        """
        prompt = f"""请将以下招生宣传活动文案转换为适合微信公众号发布的HTML格式。

活动名称：{activity_name or "招生宣传活动"}
文章标题：{title}
文章摘要：{summary or "无"}
正文内容：
{content}

要求：
1. 使用标准的微信公众号HTML格式
2. 包含合适的标题、段落、列表等标签
3. 可以添加适当的emoji增加可读性
4. 保持原文的核心信息不变
5. 输出纯HTML代码，不要包含```html```标记
"""
        return await cls.generate_content(
            prompt=prompt,
            system_prompt="你是一个专业的微信公众号运营专家，擅长将普通文章转换为适合微信公众号发布的精美HTML格式内容。",
            temperature=0.7,
            max_tokens=4000,
        )
