"""
Surface Controller - MVC Architecture

Handles surface/mesh generation and editing endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import cv2

from services.image_service import ImageService
from services.depth_service import DepthService
from services.mesh_service import MeshService
from models.depth_model import DepthEstimationModel

router = APIRouter(prefix="/api/surface", tags=["surface"])

# Cache for session meshes
_mesh_cache = {}


class MeshData(BaseModel):
    vertices: List[List[float]]
    indices: List[List[int]]


class SurfaceGenerateRequest(BaseModel):
    image_id: str
    z_scale: float = 1.0
    smooth_strength: int = 5
    downsample_scale: float = 0.5


class SurfaceGenerateResponse(BaseModel):
    status: str
    mesh: Optional[MeshData] = None
    message: Optional[str] = None


class EditRequest(BaseModel):
    image_id: str
    operation: str
    intensity: float = 1.0


class EditResponse(BaseModel):
    status: str
    mesh: Optional[MeshData] = None
    message: Optional[str] = None


class ResetResponse(BaseModel):
    status: str
    mesh: Optional[MeshData] = None
    message: Optional[str] = None


@router.post("/generate", response_model=SurfaceGenerateResponse)
async def generate_surface(request: SurfaceGenerateRequest):
    """Generate 3D surface mesh from depth estimation.
    
    - Loads uploaded image
    - Runs depth estimation
    - Generates mesh from depth map
    - Caches mesh for editing
    """
    try:
        # Load image
        image, image_model = ImageService.load_image(request.image_id)
        
        # Create depth estimation config
        depth_config = DepthEstimationModel(
            z_scale=request.z_scale,
            smooth_strength=request.smooth_strength,
            downsample_scale=request.downsample_scale
        )
        
        # Perform depth estimation and processing
        depth = DepthService.estimate_and_process(image, depth_config)
        
        # Generate mesh from depth
        mesh = MeshService.generate_mesh_from_depth(depth)
        
        # Cache mesh for editing
        _mesh_cache[request.image_id] = mesh
        
        # Convert to response format
        mesh_data = MeshData(
            vertices=[v.to_list() for v in mesh.vertices],
            indices=[f.to_list() for f in mesh.faces]
        )
        
        return {
            "status": "success",
            "mesh": mesh_data
        }
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit", response_model=EditResponse)
async def edit_surface(request: EditRequest):
    """Apply editing operation to generated mesh.
    
    - Supports: smooth, sharpen, scale
    - Returns updated mesh
    """
    try:
        if request.image_id not in _mesh_cache:
            raise HTTPException(status_code=404, detail="Mesh not found. Generate surface first.")
        
        mesh = _mesh_cache[request.image_id]
        
        # Apply edit operation
        if request.operation == "smooth":
            mesh = MeshService.smooth_mesh(mesh, request.intensity)
        elif request.operation == "sharpen":
            mesh = MeshService.sharpen_mesh(mesh, request.intensity)
        elif request.operation == "scale":
            mesh = MeshService.scale_mesh(mesh, 1.0 + request.intensity * 0.1)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {request.operation}")
        
        # Update cache
        _mesh_cache[request.image_id] = mesh
        
        # Convert to response format
        mesh_data = MeshData(
            vertices=[v.to_list() for v in mesh.vertices],
            indices=[f.to_list() for f in mesh.faces]
        )
        
        return {
            "status": "success",
            "mesh": mesh_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=ResetResponse)
async def reset_surface(request: dict):
    """Reset mesh to original generated state."""
    try:
        image_id = request.get("image_id")
        
        if image_id not in _mesh_cache:
            raise HTTPException(status_code=404, detail="Mesh not found")
        
        mesh = _mesh_cache[image_id]
        mesh.reset_to_original()
        
        # Convert to response format
        mesh_data = MeshData(
            vertices=[v.to_list() for v in mesh.vertices],
            indices=[f.to_list() for f in mesh.faces]
        )
        
        return {
            "status": "success",
            "mesh": mesh_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
