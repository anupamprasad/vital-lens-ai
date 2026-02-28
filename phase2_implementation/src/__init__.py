"""
Vital Lens AI - Phase 2: ML Pipeline Implementation
Remote Photoplethysmography (rPPG) for Heart Rate Estimation
"""

from .preprocessing import FaceDetector, FaceDetectionResult
from .algorithms import POSMethod, POSResult
from .signal_processing import SignalProcessor, FilteredSignalResult
from .models import ModelOptimizer, QuantizationConfig

__version__ = "0.2.0"

__all__ = [
    # Preprocessing
    "FaceDetector",
    "FaceDetectionResult",
    # Algorithms
    "POSMethod",
    "POSResult",
    # Signal Processing
    "SignalProcessor",
    "FilteredSignalResult",
    # Models
    "ModelOptimizer",
    "QuantizationConfig",
]
