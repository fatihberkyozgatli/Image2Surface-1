"""
Image2Surface MVC Application

Main FastAPI application using Model-View-Controller architecture.

Architecture Pattern:
- Models: Domain objects representing core business entities
- Views: Frontend (Next.js React application)
- Controllers: HTTP route handlers that coordinate models and services

Data Flow:
HTTP Request -> Controller -> Services -> Models -> Response -> View
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import all_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app with metadata
app = FastAPI(
    title="Image2Surface API (MVC Architecture)",
    description="Convert images to 3D surfaces using depth estimation (MVC Pattern)",
    version="1.0.0-mvc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all controllers
for router in all_routers:
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Application startup handler."""
    logger.info("Image2Surface API (MVC) starting up...")
    logger.info("Models, Services, and Controllers initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown handler."""
    logger.info("Image2Surface API (MVC) shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
