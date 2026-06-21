
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

from agno.run.team import TeamRunOutput
from agno.session.team import TeamSession
from agno.team.team import Team

from app.api.v1.module_system.dept.service import DeptService
from app.common.request import PaginationService
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import logger

from .crud import ChatSessionCRUD
from .schema import (
    ChatQuerySchema,
    ChatSessionCreateSchema,
    ChatSessionQueryParam,
    ChatSessionUpdateSchema,
)
from .utils import AgnoFactory


async def _format_session_data(session: TeamSession, auth: AuthSchema | None = None) -> dict[str, Any]:
    """格式化会话数据，添加前端需要的字段"""
    if hasattr(session, "to_dict"):
        session_dict = session.to_dict()
    else:
        session_dict = {
            "session_id": getattr(session, "session_id", ""),
            "agent_id": getattr(session, "agent_id", None),
            "team_id": getattr(session, "team_id", None),
            "workflow_id": getattr(session, "workflow_id", None),
            "user_id": getattr(session, "user_id", None),
            "session_data": getattr(session, "session_data", None),
            "agent_data": getattr(session, "agent_data", None),
            "team_data": getattr(session, "team_data", None),
            "workflow_data": getattr(session, "workflow_data", None),
            "metadata": getattr(session, "metadata", None),
            "runs": getattr(session, "runs", []),
            "summary": getattr(session, "summary", None),
            "created_at": getattr(session, "created_at", None),
            "updated_at": getattr(session, "updated_at", None),
        }

    session_data = session_dict.get("session_data") or {}
    runs = session_dict.get("runs") or []
    messages = _extract_messages(runs)

    # 从 session_data 中获取 session_name 作为标题
    session_name = session_data.get("session_name") if session_data else None

    result = {
        **session_dict,
        "id": session_dict.get("session_id"),
        "title": session_name or session_dict.get("session_id", "")[:8] or "未命名会话",
        "created_time": _unix_to_datetime(session_dict.get("created_at")),
        "updated_time": _unix_to_datetime(session_dict.get("updated_at")),
        "message_count": len(messages),
        "messages": messages,
    }

    # 如果有 auth，查询部门名称
    if auth and session_dict.get("team_id"):
        try:
            team_id = session_dict.get("team_id")
            if isinstance(team_id, str):
                dept_name = await DeptService(auth).detail(id=int(team_id))
                result["team_name"] = dept_name.get("name")
            elif isinstance(team_id, int):
                dept_name = await DeptService(auth).detail(id=team_id)
                result["team_name"] = dept_name.get("name")
            else:
                result["team_name"] = None
        except Exception:
            result["team_name"] = None
    else:
        result["team_name"] = None

    # 如果 summary 是 SessionSummary 对象，提取 summary 字段
    summary = session_dict.get("summary")
    if summary:
        if isinstance(summary, dict):
            result["summary"] = summary.get("summary")
        else:
            result["summary"] = str(summary)

    return result


def _unix_to_datetime(timestamp: int | None) -> str | None:
    """将Unix时间戳转换为日期时间字符串"""
    if timestamp is None:
        return None
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError, OSError):
        return None


def _extract_messages(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """从 runs 中提取消息"""
    messages = []
    if not runs:
        return messages
    for run in runs:
        if not isinstance(run, dict):
            continue
        run_messages = run.get("messages", [])
        if run_messages and isinstance(run_messages, list):
            for msg in run_messages:
                if isinstance(msg, dict):
                    role = msg.get("role")
                    if role in ("user", "assistant"):
                        messages.append(
                            {
                                "id": msg.get("id"),
                                "role": role,
                                "content": msg.get("content", ""),
                                "created_at": msg.get("created_at"),
                            }
                        )
    return messages


class ChatService:
    """聊天会话管理模块服务层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def chat_query(self, query: ChatQuerySchema) -> AsyncGenerator[str, None]:
        """流式 AI 对话"""
        try:
            crud = ChatSessionCRUD(self.auth)

            session_id = query.session_id
            if not session_id:
                import uuid

                session_id = str(uuid.uuid4())
                session: TeamSession | None = await crud.create_crud(data=ChatSessionCreateSchema(title="新对话"))
                if not session:
                    raise CustomException(msg="创建会话失败")
                session_id = session.session_id

            agno_factory = AgnoFactory()
            dept_id = str(self.auth.user.dept_id) if self.auth and self.auth.user and hasattr(self.auth.user, "dept_id") and self.auth.user.dept_id else "default"
            agent = agno_factory.create_agent(
                user_id=self.auth.user.username if self.auth and self.auth.user else "user",
                dept_id=dept_id,
                session_id=session_id,
                db=crud.db,
            )

            async for chunk in agent.arun(input=query.message, stream=True):
                if chunk and chunk.content:
                    yield chunk.content

        except Exception as e:
            logger.error(f"聊天查询失败: {e}")
            yield f"抱歉，处理您的请求时出现错误：{str(e)}"

    async def chat_non_stream(self, message: str, session_id: str | None) -> dict[str, Any]:
        """非流式 AI 对话"""
        try:
            crud = ChatSessionCRUD(self.auth)

            if not session_id:
                import uuid

                session_id = str(uuid.uuid4())
                session: TeamSession | None = await crud.create_crud(data=ChatSessionCreateSchema(title="新对话"))
                if not session:
                    raise CustomException(msg="创建会话失败")
                session_id = session.session_id

            agno_factory = AgnoFactory()
            dept_id = str(self.auth.user.dept_id) if self.auth and self.auth.user and hasattr(self.auth.user, "dept_id") and self.auth.user.dept_id else "default"
            agent: Team = agno_factory.create_agent(
                user_id=self.auth.user.username if self.auth and self.auth.user else "user",
                dept_id=dept_id,
                session_id=session_id,
                db=crud.db,
            )

            response: TeamRunOutput = await agent.arun(input=message)

            response_text = ""
            action = None

            if response and response.content:
                response_text = response.content
                import json

                try:
                    if response_text.strip().startswith("{") and response_text.strip().endswith("}"):
                        action = json.loads(response_text)
                    elif "```json" in response_text:
                        json_start = response_text.find("```json") + 7
                        json_end = response_text.find("```", json_start)
                        if json_end > json_start:
                            json_str = response_text[json_start:json_end].strip()
                            action = json.loads(json_str)
                except (json.JSONDecodeError, Exception):
                    pass

                if not action:
                    action = self._parse_action_from_response(response_text)

            return {
                "response": response_text,
                "session_id": session_id,
                "function_calls": None,
                "action": action,
            }

        except Exception as e:
            logger.error(f"聊天查询失败: {e}")
            return {
                "response": f"抱歉，处理您的请求时出现错误：{str(e)}",
                "session_id": session_id,
                "function_calls": None,
                "action": None,
            }

    @staticmethod
    def _parse_action_from_response(response_text: str) -> dict[str, Any] | None:
        """从响应文本中解析操作建议"""

        route_config = {
            "用户管理": {"path": "/system/user", "name": "用户管理"},
            "角色管理": {"path": "/system/role", "name": "角色管理"},
            "菜单管理": {"path": "/system/menu", "name": "菜单管理"},
            "部门管理": {"path": "/system/dept", "name": "部门管理"},
            "字典管理": {"path": "/system/dict", "name": "字典管理"},
            "系统日志": {"path": "/system/log", "name": "系统日志"},
        }

        navigation_keywords = ["跳转", "打开", "进入", "前往", "去", "浏览", "查看"]
        has_navigation = any(keyword in response_text for keyword in navigation_keywords)

        if not has_navigation:
            return None

        for page_name, route_info in route_config.items():
            if page_name in response_text:
                return {
                    "type": "navigate",
                    "path": route_info["path"],
                    "name": route_info["name"],
                }

        keyword_mapping = {
            "用户": {"path": "/system/user", "name": "用户管理"},
            "角色": {"path": "/system/role", "name": "角色管理"},
            "菜单": {"path": "/system/menu", "name": "菜单管理"},
            "部门": {"path": "/system/dept", "name": "部门管理"},
            "字典": {"path": "/system/dict", "name": "字典管理"},
            "日志": {"path": "/system/log", "name": "系统日志"},
        }

        for keyword, route_info in keyword_mapping.items():
            if keyword in response_text:
                return {
                    "type": "navigate",
                    "path": route_info["path"],
                    "name": route_info["name"],
                }

        return None

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        crud = ChatSessionCRUD(self.auth)
        session: TeamSession | None = await crud.get_by_id_crud(session_id=session_id)
        if session:
            return await _format_session_data(session, self.auth)
        return None

    async def create(self, data: ChatSessionCreateSchema) -> dict[str, Any] | None:
        crud = ChatSessionCRUD(self.auth)
        session = await crud.create_crud(data=data)
        if session:
            return await _format_session_data(session, self.auth)
        return None

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: ChatSessionQueryParam,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        crud = ChatSessionCRUD(self.auth)
        sessions = await crud.list_crud()
        items = [await _format_session_data(s, self.auth) for s in sessions]
        return await PaginationService.paginate(
            data_list=items,
            page_no=page_no,
            page_size=page_size,
        )

    async def update(self, session_id: str, data: ChatSessionUpdateSchema) -> bool:
        crud = ChatSessionCRUD(self.auth)
        return await crud.update_crud(session_id=session_id, data=data)

    async def delete(self, session_ids: list[str]) -> None:
        await ChatSessionCRUD(self.auth).delete_crud(session_ids=session_ids)
