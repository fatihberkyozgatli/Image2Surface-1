"""
Mesh Service - MVC Architecture

Service layer for mesh generation and editing business logic.
"""

import cv2
import numpy as np
from typing import Tuple

from models.mesh_model import MeshModel, Vertex, Face


class MeshService:
    """Manages mesh generation and editing operations."""
    
    @classmethod
    def generate_mesh_from_depth(cls, depth: np.ndarray, vertex_colors: np.ndarray = None) -> MeshModel:
        """Generate mesh from depth map."""
        h, w = depth.shape
        
        # Generate vertices
        vertices = []
        for y in range(h):
            for x in range(w):
                z = float(depth[y, x])
                vertices.append(Vertex(float(x), float(y), z))
        
        # Generate faces (quads as two triangles)
        faces = []
        for y in range(h - 1):
            for x in range(w - 1):
                # Get vertex indices for quad
                v0 = y * w + x
                v1 = y * w + (x + 1)
                v2 = (y + 1) * w + (x + 1)
                v3 = (y + 1) * w + x
                
                # Create two triangles from quad
                faces.append(Face(v0, v1, v2))
                faces.append(Face(v0, v2, v3))
        
        # Normalize coordinate space
        vertices = cls._normalize_vertices(vertices)
        
        mesh = MeshModel(vertices=vertices, faces=faces)
        if vertex_colors is not None:
            mesh.vertex_colors = vertex_colors
        mesh.save_original()
        
        return mesh
    
    @classmethod
    def _normalize_vertices(cls, vertices: list) -> list:
        """Normalize vertex coordinates."""
        if not vertices:
            return vertices
        
        # Convert to array for computation
        vert_array = np.array([v.to_list() for v in vertices])
        
        # Flip Y axis
        vert_array[:, 1] *= -1
        
        # Center mesh
        min_vals = vert_array.min(axis=0)
        max_vals = vert_array.max(axis=0)
        center = (min_vals + max_vals) / 2
        vert_array -= center
        
        # Normalize range
        ranges = max_vals - min_vals
        max_range = ranges.max()
        if max_range > 0:
            vert_array = vert_array / (max_range / 2)
        
        # Convert back to Vertex objects
        return [Vertex(float(v[0]), float(v[1]), float(v[2])) for v in vert_array]
    
    @classmethod
    def smooth_mesh(cls, mesh: MeshModel, intensity: float = 1.0) -> MeshModel:
        """Apply smoothing to mesh vertices."""
        if not mesh.vertices:
            return mesh
        
        # Simple Laplacian smoothing
        new_vertices = mesh.vertices.copy()
        adj_list = cls._build_adjacency(mesh)
        
        for i in range(len(new_vertices)):
            if i in adj_list and adj_list[i]:
                neighbors = adj_list[i]
                avg_pos = np.mean([mesh.vertices[n].to_list() for n in neighbors], axis=0)
                current_pos = np.array(mesh.vertices[i].to_list())
                new_pos = current_pos + (avg_pos - current_pos) * intensity * 0.1
                new_vertices[i] = Vertex(float(new_pos[0]), float(new_pos[1]), float(new_pos[2]))
        
        mesh.vertices = new_vertices
        return mesh
    
    @classmethod
    def sharpen_mesh(cls, mesh: MeshModel, intensity: float = 1.0) -> MeshModel:
        """Apply sharpening to mesh by exaggerating differences."""
        if not mesh.vertices:
            return mesh
        
        new_vertices = mesh.vertices.copy()
        adj_list = cls._build_adjacency(mesh)
        
        for i in range(len(new_vertices)):
            if i in adj_list and adj_list[i]:
                neighbors = adj_list[i]
                avg_pos = np.mean([mesh.vertices[n].to_list() for n in neighbors], axis=0)
                current_pos = np.array(mesh.vertices[i].to_list())
                new_pos = current_pos + (current_pos - avg_pos) * intensity * 0.1
                new_vertices[i] = Vertex(float(new_pos[0]), float(new_pos[1]), float(new_pos[2]))
        
        mesh.vertices = new_vertices
        return mesh
    
    @classmethod
    def scale_mesh(cls, mesh: MeshModel, scale_factor: float) -> MeshModel:
        """Scale mesh uniformly."""
        new_vertices = []
        for v in mesh.vertices:
            scaled_v = Vertex(v.x * scale_factor, v.y * scale_factor, v.z * scale_factor)
            new_vertices.append(scaled_v)
        
        mesh.vertices = new_vertices
        return mesh
    
    @staticmethod
    def _build_adjacency(mesh: MeshModel) -> dict:
        """Build vertex adjacency list from mesh faces."""
        adj_list = {}
        
        for face in mesh.faces:
            for v in [face.v0, face.v1, face.v2]:
                if v not in adj_list:
                    adj_list[v] = set()
            
            adj_list[face.v0].add(face.v1)
            adj_list[face.v0].add(face.v2)
            adj_list[face.v1].add(face.v0)
            adj_list[face.v1].add(face.v2)
            adj_list[face.v2].add(face.v0)
            adj_list[face.v2].add(face.v1)
        
        # Convert sets to lists
        return {k: list(v) for k, v in adj_list.items()}
