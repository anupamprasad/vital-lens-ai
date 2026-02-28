"""
Signal Processing Pipeline for rPPG
Bandpass filtering, normalization, and peak detection
Vital Lens AI Phase 2
"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class FilteredSignalResult:
    """Result from signal filtering"""
    original_signal: np.ndarray
    filtered_signal: np.ndarray
    normalized_signal: np.ndarray
    peaks: np.ndarray  # Indices of detected peaks
    peak_values: np.ndarray  # Values at peak indices


class SignalProcessor:
    """
    Signal processing for PPG (photoplethysmogram) signals.
    
    Handles:
    - Bandpass filtering (0.4-4 Hz for HR range)
    - Normalization and detrending
    - Peak detection for beat detection
    - Signal quality assessment
    """
    
    def __init__(
        self,
        fps: int = 30,
        hr_min: int = 40,
        hr_max: int = 200,
    ):
        """
        Initialize signal processor.
        
        Args:
            fps: Frames per second
            hr_min: Minimum heart rate (BPM)
            hr_max: Maximum heart rate (BPM)
        """
        self.fps = fps
        self.hr_min = hr_min
        self.hr_max = hr_max
        
        # Calculate frequency boundaries
        self.freq_min = hr_min / 60.0  # Hz
        self.freq_max = hr_max / 60.0  # Hz
        
        # Create filters
        self.bandpass_b, self.bandpass_a = self._create_bandpass_filter()
        self.detrend_filter_b, self.detrend_filter_a = self._create_detrend_filter()
    
    def filter_signal(self, signal_data: np.ndarray) -> FilteredSignalResult:
        """
        Apply complete filtering pipeline to signal.
        
        Args:
            signal_data: Input PPG signal
            
        Returns:
            FilteredSignalResult with filtered and normalized signals
        """
        # Input validation
        if len(signal_data) < 10:
            return self._empty_result(signal_data)
        
        signal_data = np.array(signal_data, dtype=np.float32)
        
        # Remove DC component (detrending)
        detrended = self._detrend_signal(signal_data)
        
        # Apply bandpass filter
        filtered = self._apply_bandpass(detrended)
        
        # Normalize signal
        normalized = self._normalize_signal(filtered)
        
        # Detect peaks (heartbeats)
        peaks, peak_values = self._detect_peaks(normalized)
        
        return FilteredSignalResult(
            original_signal=signal_data,
            filtered_signal=filtered,
            normalized_signal=normalized,
            peaks=peaks,
            peak_values=peak_values,
        )
    
    def _create_bandpass_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create bandpass filter (0.4-4 Hz)."""
        nyquist = self.fps / 2.0
        
        # Normalize frequencies
        low = self.freq_min / nyquist
        high = self.freq_max / nyquist
        
        # Clamp to valid range
        low = np.clip(low, 0.001, 0.999)
        high = np.clip(high, 0.001, 0.999)
        
        # Design Butterworth filter (order 4)
        b, a = signal.butter(4, [low, high], btype='band')
        return b, a
    
    def _create_detrend_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create highpass filter for detrending (0.02 Hz)."""
        nyquist = self.fps / 2.0
        
        # Very low cutoff (0.02 Hz) to remove slow drift
        cutoff = 0.02 / nyquist
        cutoff = np.clip(cutoff, 0.001, 0.999)
        
        # Design highpass filter
        b, a = signal.butter(3, cutoff, btype='high')
        return b, a
    
    def _detrend_signal(self, signal_data: np.ndarray) -> np.ndarray:
        """Remove DC and slow drift from signal."""
        # Apply highpass filter
        detrended = signal.filtfilt(self.detrend_filter_b, self.detrend_filter_a, signal_data)
        return detrended
    
    def _apply_bandpass(self, signal_data: np.ndarray) -> np.ndarray:
        """Apply bandpass filter."""
        filtered = signal.filtfilt(self.bandpass_b, self.bandpass_a, signal_data)
        return filtered
    
    def _normalize_signal(self, signal_data: np.ndarray) -> np.ndarray:
        """Normalize signal to [0, 1] range."""
        signal_min = np.min(signal_data)
        signal_max = np.max(signal_data)
        
        # Avoid division by zero
        if signal_max - signal_min < 1e-6:
            return np.zeros_like(signal_data)
        
        normalized = (signal_data - signal_min) / (signal_max - signal_min)
        return normalized
    
    def _detect_peaks(
        self,
        signal_data: np.ndarray,
        height: Optional[float] = None,
        distance: Optional[int] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect peaks (heartbeats) in signal.
        
        Args:
            signal_data: Normalized signal
            height: Minimum peak height (None = auto)
            distance: Minimum distance between peaks in samples
            
        Returns:
            (peak_indices, peak_values)
        """
        if len(signal_data) < 5:
            return np.array([]), np.array([])
        
        # Auto-threshold if not provided
        if height is None:
            height = np.mean(signal_data) + np.std(signal_data)
        
        # Auto-distance if not provided
        # Minimum distance = time for minimum HR
        if distance is None:
            distance = int(self.fps * 60 / self.hr_max)
            distance = max(distance, 1)
        
        # Detect peaks
        peaks, _ = signal.find_peaks(
            signal_data,
            height=height,
            distance=distance,
            prominence=np.std(signal_data) * 0.5,
        )
        
        peak_values = signal_data[peaks]
        
        return peaks, peak_values
    
    def estimate_heart_rate_from_peaks(
        self,
        peaks: np.ndarray,
    ) -> Tuple[Optional[float], Optional[np.ndarray]]:
        """
        Estimate heart rate from detected peaks.
        
        Args:
            peaks: Indices of detected peaks
            
        Returns:
            (heart_rate_bpm, rr_intervals)
        """
        if len(peaks) < 2:
            return None, None
        
        # Calculate intervals between peaks
        rr_intervals = np.diff(peaks)
        rr_intervals_ms = (rr_intervals / self.fps) * 1000  # Convert to ms
        
        # Calculate mean RR interval
        mean_rr = np.mean(rr_intervals_ms)
        
        # Convert to BPM
        heart_rate = 60000 / mean_rr if mean_rr > 0 else None
        
        return heart_rate, rr_intervals_ms
    
    def estimate_heart_rate_spectral(
        self,
        signal_data: np.ndarray,
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Estimate heart rate using FFT (spectral) method.
        
        Args:
            signal_data: Input signal (filtered)
            
        Returns:
            (heart_rate_bpm, confidence)
        """
        if len(signal_data) < 10:
            return None, 0.0
        
        # Apply window to reduce spectral leakage
        windowed = signal_data * np.hanning(len(signal_data))
        
        # Compute FFT
        fft = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(windowed), 1.0 / self.fps)
        
        # Get positive frequencies only
        positive_mask = freqs > 0
        freqs_positive = freqs[positive_mask]
        magnitude = np.abs(fft[positive_mask])
        
        # Find peak in HR range
        hr_mask = (freqs_positive >= self.freq_min) & (freqs_positive <= self.freq_max)
        
        if not np.any(hr_mask):
            return None, 0.0
        
        # Get dominant frequency
        hr_freqs = freqs_positive[hr_mask]
        hr_magnitudes = magnitude[hr_mask]
        
        dominant_idx = np.argmax(hr_magnitudes)
        dominant_freq = hr_freqs[dominant_idx]
        
        # Convert to BPM
        heart_rate = dominant_freq * 60
        
        # Calculate confidence
        peak_power = np.max(hr_magnitudes)
        noise_power = np.mean(magnitude[~hr_mask]) if np.any(~hr_mask) else 1e-6
        confidence = min(peak_power / (noise_power + 1e-6), 1.0)
        
        return heart_rate, confidence
    
    def assess_signal_quality(self, signal_data: np.ndarray) -> float:
        """
        Assess signal quality (0-1).
        
        Metrics:
        - SNR (signal-to-noise ratio)
        - Power in HR band vs out
        """
        if len(signal_data) < 10:
            return 0.0
        
        # Compute FFT
        windowed = signal_data * np.hanning(len(signal_data))
        fft = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(windowed), 1.0 / self.fps)
        magnitude = np.abs(fft[np.abs(freqs) > 0])
        
        # Power in HR band
        hr_mask = (np.abs(freqs) >= self.freq_min) & (np.abs(freqs) <= self.freq_max)
        hr_power = np.sum(magnitude[hr_mask]) if np.any(hr_mask) else 0
        
        # Power outside HR band
        noise_power = np.sum(magnitude[~hr_mask])
        
        # SNR
        snr = hr_power / (noise_power + 1e-6)
        quality = min(snr / 10.0, 1.0)  # Normalize (10 is good SNR)
        
        return quality
    
    def _empty_result(self, signal_data: np.ndarray) -> FilteredSignalResult:
        """Return empty result for short signals."""
        return FilteredSignalResult(
            original_signal=signal_data,
            filtered_signal=np.array([]),
            normalized_signal=np.array([]),
            peaks=np.array([], dtype=int),
            peak_values=np.array([]),
        )


# Utility functions for common operations
def remove_baseline_wander(
    signal_data: np.ndarray,
    fps: int,
    cutoff_hz: float = 0.02,
) -> np.ndarray:
    """Remove slow baseline drift (highpass filter)."""
    nyquist = fps / 2.0
    normalized_cutoff = cutoff_hz / nyquist
    normalized_cutoff = np.clip(normalized_cutoff, 0.001, 0.999)
    
    b, a = signal.butter(3, normalized_cutoff, btype='high')
    filtered = signal.filtfilt(b, a, signal_data)
    
    return filtered


def compute_rr_intervals(
    peaks: np.ndarray,
    fps: int,
) -> Tuple[np.ndarray, float]:
    """
    Compute RR intervals from peak indices.
    
    Returns:
        (rr_intervals_ms, mean_rr_ms)
    """
    if len(peaks) < 2:
        return np.array([]), 0.0
    
    intervals = np.diff(peaks)
    intervals_ms = (intervals / fps) * 1000
    mean_rr = np.mean(intervals_ms)
    
    return intervals_ms, mean_rr


# Example usage
if __name__ == "__main__":
    # Create sample signal
    processor = SignalProcessor(fps=30, hr_min=40, hr_max=200)
    
    # Generate synthetic PPG signal (60 BPM)
    t = np.arange(0, 10, 1/30)  # 10 seconds
    signal_data = np.sin(2 * np.pi * 1.0 * t) + 0.1 * np.random.randn(len(t))
    
    # Filter and analyze
    result = processor.filter_signal(signal_data)
    print(f"Peaks detected: {len(result.peaks)}")
    
    # Estimate heart rate from peaks
    hr_peaks, rr = processor.estimate_heart_rate_from_peaks(result.peaks)
    print(f"HR from peaks: {hr_peaks:.1f} BPM")
    
    # Estimate heart rate from FFT
    hr_spectral, confidence = processor.estimate_heart_rate_spectral(result.filtered_signal)
    print(f"HR from FFT: {hr_spectral:.1f} BPM (confidence: {confidence:.2f})")
    
    # Signal quality
    quality = processor.assess_signal_quality(result.normalized_signal)
    print(f"Signal quality: {quality:.2f}")
