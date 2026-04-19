"""
Mesh Model - MVC Architecture

Represents a 3D mesh structure with vertices and faces.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np


@dataclass
class Vertex:
    """Represents a single vertex in a 3D mesh."""
    x: float
    y: float
    z: float
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert vertex to tuple format."""
        return (self.x, self.y, self.z)
    
    def to_list(self) -> List[float]:
        """Convert vertex to list format."""
        return [self.x, self.y, self.z]


@dataclass
class Face:
    """Represents a triangular face in a 3D mesh."""
    v0: int  # Vertex index 0
    v1: int  # Vertex index 1
    v2: int  # Vertex index 2
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert face to tuple format."""
        return (self.v0, self.v1, self.v2)
    
    def to_list(self) -> List[int]:
        """Convert face to list format."""
        return [self.v0, self.v1, self.v2]


@dataclass
class MeshModel:
    """Domain model representing a 3D mesh."""
    
    vertices: List[Vertex] = field(default_factory=list)
    faces: List[Face] = field(default_factory=list)
    vertex_colors: np.ndarray = field(default_factory=lambda: np.array([]))
    original_vertices: List[Vertex] = field(default_factory=list)
    
    def get_vertex_count(self) -> int:
        """Get number of vertices in mesh."""
        return len(self.vertices)
    
    def get_face_count(self) -> int:
        """Get number of faces in mesh."""
        return len(self.faces)
    
    def get_bounds(self) -> dict:
        """Get bounding box of mesh."""
        if not self.vertices:
            return {'min': [0, 0, 0], 'max': [0, 0, 0]}
        
        vertices_array = np.array([v.to_list() for v in self.vertices])
        return {
            'min': vertices_array.min(axis=0).tolist(),
            'max': vertices_array.max(axis=0).tolist()
        }
    
    def to_dict(self) -> dict:
        """Convert mesh to dictionary format for JSON serialization."""
        return {
            'vertices': [v.to_list() for v in self.vertices],
            'indices': [f.to_list() for f in self.faces],
            'vertex_count': self.get_vertex_count(),
            'face_count': self.get_face_count(),
            'bounds': self.get_bounds()
        }
    
    def reset_to_original(self) -> None:
        """Reset mesh to original state before edits."""
        if self.original_vertices:
            self.vertices = self.original_vertices.copy()
    
    def save_original(self) -> None:
        """Save current state as original for undo operations."""
        self.original_vertices = [Vertex(v.x, v.y, v.z) for v in self.vertices]
