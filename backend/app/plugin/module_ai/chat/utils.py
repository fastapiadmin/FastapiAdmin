from typing import Any

from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.team import Team

from app.config.setting import settings


class AgnoFactory:
    """Agno 工厂类 - 统一管理 Agent、Team 创建逻辑"""

    # 配置常量
    AGENT_DESCRIPTION = "你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。"
    AGENT_INSTRUCTIONS = ["保持回答简洁明了", "如果不确定，请说明"]
    AGENT_EXPECTED_OUTPUT = "中文回答"
    AGENT_TEMPERATURE = 0.7
    NUM_HISTORY_RUNS = 3

    def create_agent(self, user_id: str, dept_id: str, session_id: str, db: Any | None = None) -> Team:
        """
        创建带 Agent 的 Team 实例。

        参数:
        - user_id (str): 用户标识。
        - dept_id (str): 部门/团队标识。
        - session_id (str): 会话 ID。
        - db (Any | None): Agno 持久化数据库实例，可选。

        返回:
        - Team: 配置好的 Team。
        """

        # 创建 Agent
        fastapiadmin_agent = Agent(
            id=user_id,
            name="fastapiadmin_agent",
            role="You are a helpful AI assistant",
            description=self.AGENT_DESCRIPTION,
            tools=[],
        )

        # 创建 Team
        fastapiadmin_team = Team(
            id=dept_id,
            user_id=user_id,
            session_id=session_id,
            model=OpenAILike(
                id=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                temperature=self.AGENT_TEMPERATURE,
            ),
            members=[fastapiadmin_agent],
            instructions=self.AGENT_INSTRUCTIONS,
            expected_output=self.AGENT_EXPECTED_OUTPUT,
            add_datetime_to_context=True,
            add_history_to_context=True,
            markdown=True,
            num_history_runs=self.NUM_HISTORY_RUNS,
            input_schema=None,
            output_schema=None,
            parse_response=True,
            read_chat_history=True,
            db=db,
        )

        return fastapiadmin_team
