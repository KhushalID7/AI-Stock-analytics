import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent

from apps.agents.tools import ALL_TOOLS
from apps.agents.prompt import STOCK_ANALYST_PROMPT

# Load env vars from .env
load_dotenv()


def _get_llm():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        api_key=api_key,
    )
    return llm


def create_stock_agent_executor() -> AgentExecutor:
    """
    Build and return an AgentExecutor that:
    - Uses Gemini (ChatGoogleGenerativeAI)
    - Uses our tools (ALL_TOOLS)
    - Uses the STOCK_ANALYST_PROMPT
    via LangChain's create_tool_calling_agent helper.
    """
    llm = _get_llm()

    agent = create_tool_calling_agent(
        llm=llm,
        tools=ALL_TOOLS,
        prompt=STOCK_ANALYST_PROMPT,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=True,
    )

    return agent_executor
