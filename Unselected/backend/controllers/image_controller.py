"""
Image Controller - MVC Architecture

Handles image upload and management endpoints.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.image_service import ImageService

router = APIRouter(prefix="/api/image", tags=["image"])


class ImageUploadResponse(BaseModel):
    status: str
    image: Optional[dict] = None
    message: Optional[str] = None


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload an image for processing.
    
    - Validates file type
    - Saves to disk
    - Returns image ID for subsequent operations
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if not ImageService.validate_image_format(file.filename):
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Read file content
        contents = await file.read()
        
        # Save image using service
        image_model = ImageService.save_uploaded_image(contents, file.filename)
        
        return {
            "status": "success",
            "image": {
                "imageId": image_model.image_id,
                "filename": image_model.filename,
                "width": image_model.width,
                "height": image_model.height
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
