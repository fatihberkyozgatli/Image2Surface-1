"""
MVC Architecture - Domain Models

Models represent the core domain objects and data structures in the application.
They encapsulate the essential data and business rules for Image2Surface.
"""

from .image_model import ImageModel
from .mesh_model import MeshModel, Vertex, Face
from .depth_model import DepthEstimationModel

__all__ = ['ImageModel', 'MeshModel', 'Vertex', 'Face', 'DepthEstimationModel']
