"""
Image Service - MVC Architecture

Service layer for image handling business logic.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple
import uuid

from models.image_model import ImageModel


class ImageService:
    """Manages image operations and storage."""
    
    UPLOAD_DIR = Path(__file__).parent.parent / 'uploads'
    ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    @classmethod
    def save_uploaded_image(cls, file_content: bytes, original_filename: str) -> ImageModel:
        """Save uploaded image to disk and create ImageModel."""
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        
        image_id = str(uuid.uuid4())
        file_path = cls.UPLOAD_DIR / f"{image_id}.png"
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Read image to get dimensions
        img = cv2.imdecode(np.frombuffer(file_content, np.uint8), cv2.IMREAD_COLOR)
        height, width = img.shape[:2]
        
        return ImageModel(
            image_id=image_id,
            filename=original_filename,
            file_path=file_path,
            width=width,
            height=height,
            format='png'
        )
    
    @classmethod
    def load_image(cls, image_id: str) -> Tuple[np.ndarray, ImageModel]:
        """Load image from disk."""
        file_path = cls.UPLOAD_DIR / f"{image_id}.png"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Image {image_id} not found")
        
        img = cv2.imread(str(file_path))
        height, width = img.shape[:2]
        
        model = ImageModel(
            image_id=image_id,
            filename="",
            file_path=file_path,
            width=width,
            height=height,
            format='png'
        )
        
        return img, model
    
    @classmethod
    def delete_image(cls, image_id: str) -> bool:
        """Delete image from disk."""
        file_path = cls.UPLOAD_DIR / f"{image_id}.png"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    @classmethod
    def validate_image_format(cls, filename: str) -> bool:
        """Validate that file has allowed format."""
        ext = Path(filename).suffix.lower()
        return ext in cls.ALLOWED_FORMATS
