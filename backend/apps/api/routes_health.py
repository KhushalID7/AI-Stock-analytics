from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Simple health-check endpoint so you can verify the API is up.
    Does NOT touch the LLM or Alpha Vantage.
    """
    return {"status": "ok"}
