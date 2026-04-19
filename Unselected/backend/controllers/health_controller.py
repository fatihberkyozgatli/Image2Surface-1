"""
Health Controller - MVC Architecture

Handles health check and system status endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return {
        "status": "healthy",
        "message": "Image2Surface API is running"
    }
