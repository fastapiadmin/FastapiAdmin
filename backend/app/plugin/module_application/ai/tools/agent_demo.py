from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    after_model,
    before_model,
    dynamic_prompt,
    wrap_model_call,
)
from langchain.agents.structured_output import (
    MultipleStructuredOutputsError,
    StructuredOutputValidationError,
    ToolStrategy,
)
from langchain.chat_models import init_chat_model
from langchain.messages import (
    AIMessage,
    HumanMessage,
    RemoveMessage,
    SystemMessage,
)
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime
from pydantic import BaseModel, Field

# =================定义提示词=================
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.
"""


# =================定义工具=================
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@dataclass
class Context:
    """Custom runtime context schema."""

    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


# =================定义模型=================
model = init_chat_model("claude-sonnet-4-5-20250929", temperature=0.5, timeout=10, max_tokens=1000)


# =================定义响应模型=================
class ResponseFormat(BaseModel):
    """Response schema for the agent."""

    rating: int | None = Field(description="Rating from 1-5", ge=1, le=5)
    comment: str = Field(description="Review comment")
    punny_response: str
    weather_conditions: str | None = None


# =================定义存储记忆=================
checkpointer = InMemorySaver()


# =================定义动态提示词=================
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = getattr(request.runtime.context, "user_name", "User")
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt


@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None  # No changes needed

    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg, *recent_messages]

    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *new_messages]}


@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove messages containing sensitive words."""
    last_message = state["messages"][-1]
    if any(word in last_message.content for word in ["password", "secret"]):
        return {"messages": [RemoveMessage(id=last_message.id or "")]}
    return None


@wrap_model_call
def inject_file_context(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Inject context about files user has uploaded this session."""
    # Read from State: get uploaded files metadata
    uploaded_files = request.state.get("uploaded_files", [])

    if uploaded_files:
        # Build context about available files
        file_descriptions = [
            f"- {file['name']} ({file['type']}): {file['summary']}" for file in uploaded_files
        ]

        file_context = f"""Files you have access to in this conversation:
{chr(10).join(file_descriptions)}

Reference these files when answering questions."""

        # Inject file context before recent messages
        messages = [
            *request.messages,
            {"role": "user", "content": file_context},
        ]
        request = request.override(messages=messages)


def custom_error_handler(error: Exception) -> str:
    if isinstance(error, StructuredOutputValidationError):
        return "There was an issue with the format. Try again."
    if isinstance(error, MultipleStructuredOutputsError):
        return "Multiple structured outputs were returned. Pick the most relevant one."
    return f"Error: {error!s}"


# =================定义智能体=================
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    middleware=[
        dynamic_system_prompt,
        trim_messages,
        validate_response,
        inject_file_context,
    ],
    context_schema=Context,
    response_format=ToolStrategy(
        schema=ResponseFormat,
        handle_errors=(ValueError, TypeError, custom_error_handler),
    ),
    checkpointer=checkpointer,
)

# =================定义线程=================
config = {"configurable": {"thread_id": "1"}}

messages = [
    SystemMessage("You are a poetry expert"),
    HumanMessage("Write a haiku about spring"),
    AIMessage("Cherry blossoms bloom..."),
]

# =================运行智能体=================
response = agent.invoke(input=messages, config=config, context=Context(user_id="1"))

# =================解析响应=================
print(response["structured_response"])
# ResponseFormat(
#     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
#     weather_conditions="It's always sunny in Florida!"
# )
