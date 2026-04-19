"""
Controllers Layer - MVC Architecture

Controllers handle HTTP requests and coordinate business logic.
"""

from .health_controller import router as health_router
from .image_controller import router as image_router
from .surface_controller import router as surface_router

all_routers = [health_router, image_router, surface_router]

__all__ = ['all_routers']
