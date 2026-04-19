"""
Image Model - MVC Architecture

Represents an uploaded image in the system.
"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class ImageModel:
    """Domain model for an uploaded image."""
    
    image_id: str
    filename: str
    file_path: Path
    width: int
    height: int
    format: str
    
    def get_file_content(self) -> bytes:
        """Load image file content from disk."""
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def exists(self) -> bool:
        """Check if image file exists on disk."""
        return self.file_path.exists()
    
    def delete(self) -> None:
        """Delete image file from disk."""
        if self.exists():
            self.file_path.unlink()
