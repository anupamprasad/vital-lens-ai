"""
rPPG Algorithm Implementations
Multiple algorithms for heart rate estimation from video
"""

from .pos_method import POSMethod, POSResult

__all__ = [
    "POSMethod",
    "POSResult",
]
