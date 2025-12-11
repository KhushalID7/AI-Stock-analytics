
import json
import logging
import re
from functools import lru_cache
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.api_core.exceptions import ServiceUnavailable

from apps.agents.agent import create_stock_agent_executor

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/agent",
    tags=["agent"],
)


class AgentQuery(BaseModel):
    input: str


@lru_cache(maxsize=1)
def get_agent_executor():
    # Lazily instantiate the (expensive) agent executor
    return create_stock_agent_executor()


def _extract_chart_urls(text: str):
    """Find any /static/charts/... URLs in the text."""
    pattern = r"/static/charts/[^\s\"']+"
    return list(dict.fromkeys(re.findall(pattern, text)))  # unique, preserve order


def _safe_serialize(obj: Any) -> Any:
    """
    Try to return a JSON-serializable version of obj.
    - If obj is already serializable, return it.
    - Otherwise, return a string representation.
    """
    try:
        # Try to dump->load to ensure serializable
        json.dumps(obj)
        return obj
    except Exception:
        try:
            # If it's a dict-like from LangChain, try to coerce values to strings
            if isinstance(obj, dict):
                safe = {}
                for k, v in obj.items():
                    try:
                        json.dumps(v)
                        safe[k] = v
                    except Exception:
                        safe[k] = str(v)
                return safe
        except Exception:
            pass
    # fallback to string
    return str(obj)


@router.post("/query")
async def query_agent(payload: AgentQuery):
    agent_executor = get_agent_executor()

    try:
        # Run the agent synchronously (AgentExecutor.invoke)
        result = agent_executor.invoke({"input": payload.input})
        logger.debug("Raw agent result: %s", result)

        # Decide summary (human-friendly) and raw_result (safe serialized)
        if isinstance(result, dict):
            summary = (
                result.get("output")
                or result.get("result")
                or result.get("final_answer")
                or result.get("answer")
                or result.get("response")
                or ""
            )
            # Make raw_result JSON-safe
            raw_result = _safe_serialize(result)
        else:
            summary = str(result)
            raw_result = summary

        # Ensure summary is a string
        if not isinstance(summary, str):
            summary = str(summary)

        # Extract chart URLs from summary + raw_result string
        combined_text = summary + "\n" + str(raw_result)
        chart_urls = _extract_chart_urls(combined_text)

        response = {
            "summary": summary,
            "raw_result": raw_result,
            "chart_urls": chart_urls,
        }

        return response

    except ServiceUnavailable as e:
        # LLM temporarily down / overloaded
        logger.warning("LLM ServiceUnavailable: %s", e)
        raise HTTPException(status_code=503, detail=f"LLM service temporarily unavailable: {e}")

    except Exception as e:
        logger.exception("Error while calling agent")
        # Return a cleaner error message but log full traceback
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

