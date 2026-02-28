"""
Signal Processing Module
rPPG signal extraction, filtering, and analysis
"""

from .filtering import (
    SignalProcessor,
    FilteredSignalResult,
    remove_baseline_wander,
    compute_rr_intervals,
)

__all__ = [
    "SignalProcessor",
    "FilteredSignalResult",
    "remove_baseline_wander",
    "compute_rr_intervals",
]
