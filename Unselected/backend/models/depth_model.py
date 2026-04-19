"""
Depth Estimation Model - MVC Architecture

Represents configuration and results of depth estimation.
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class DepthEstimationModel:
    """Domain model for depth estimation parameters and results."""
    
    z_scale: float = 1.0  # Height scale multiplier
    smooth_strength: int = 5  # Smoothing filter strength
    downsample_scale: float = 0.5  # Downsampling factor
    encoder: str = 'vits'  # Model encoder type
    depth_map: Optional[np.ndarray] = None  # Estimated depth map
    
    def validate(self) -> bool:
        """Validate depth estimation parameters."""
        if self.z_scale <= 0:
            return False
        if self.smooth_strength < 0:
            return False
        if not 0 < self.downsample_scale <= 1.0:
            return False
        if self.encoder not in ['vits', 'vitb', 'vitl', 'vitg']:
            return False
        return True
    
    def get_config(self) -> dict:
        """Get configuration as dictionary."""
        return {
            'z_scale': self.z_scale,
            'smooth_strength': self.smooth_strength,
            'downsample_scale': self.downsample_scale,
            'encoder': self.encoder
        }
