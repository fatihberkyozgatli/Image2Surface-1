"""
Depth Service - MVC Architecture

Service layer for depth estimation business logic.
"""

import torch
import cv2
import numpy as np
import sys
import os
from pathlib import Path

# Add depth_anything_v2 to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'depth_anything_v2'))

from depth_anything_v2.dpt import DepthAnythingV2
from models.depth_model import DepthEstimationModel


class DepthService:
    """Manages depth estimation operations."""
    
    DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    
    MODEL_CONFIGS = {
        'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
        'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
        'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
        'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
    }
    
    _model_cache = {}  # Cache loaded models
    
    @classmethod
    def load_model(cls, encoder='vits'):
        """Load depth estimation model (cached)."""
        if encoder in cls._model_cache:
            return cls._model_cache[encoder]
        
        backend_dir = Path(__file__).parent.parent
        checkpoint_path = backend_dir / 'checkpoints' / f'depth_anything_v2_{encoder}.pth'
        
        model = DepthAnythingV2(**cls.MODEL_CONFIGS[encoder])
        model.load_state_dict(torch.load(str(checkpoint_path), map_location='cpu'))
        model = model.to(cls.DEVICE).eval()
        
        cls._model_cache[encoder] = model
        return model
    
    @classmethod
    def estimate_depth(cls, image: np.ndarray, config: DepthEstimationModel) -> np.ndarray:
        """Estimate depth map from image."""
        if not config.validate():
            raise ValueError("Invalid depth estimation configuration")
        
        model = cls.load_model(config.encoder)
        
        depth = model.infer_image(image)
        
        return depth
    
    @classmethod
    def process_depth_map(cls, depth: np.ndarray, config: DepthEstimationModel) -> np.ndarray:
        """Apply processing to depth map (smoothing, downsampling, scaling)."""
        # Normalize
        depth_min = depth.min()
        depth_max = depth.max()
        if depth_max != depth_min:
            depth = (depth - depth_min) / (depth_max - depth_min)
        
        # Smooth
        if config.smooth_strength > 0:
            depth = cv2.GaussianBlur(depth, (config.smooth_strength, config.smooth_strength), 0)
        
        # Downsample
        if config.downsample_scale < 1.0:
            depth = cv2.resize(depth, None, fx=config.downsample_scale, fy=config.downsample_scale, 
                             interpolation=cv2.INTER_AREA)
        
        # Scale height
        depth = depth * config.z_scale
        
        return depth
    
    @classmethod
    def estimate_and_process(cls, image: np.ndarray, config: DepthEstimationModel) -> np.ndarray:
        """Run full depth estimation and processing pipeline."""
        depth = cls.estimate_depth(image, config)
        return cls.process_depth_map(depth, config)
