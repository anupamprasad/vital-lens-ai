"""
POS (Plane-Orthogonal-to-Skin) Algorithm Implementation
Remote Photoplethysmography (rPPG) for Heart Rate Estimation
Vital Lens AI Phase 2

Reference:
Wang, W., et al. "Algorithmic Principles of Remote Photoplethysmographic Imaging"
"""

import numpy as np
from collections import deque
from typing import Optional, Tuple
from scipy import signal
from dataclasses import dataclass


@dataclass
class POSResult:
    """Result from POS algorithm"""
    heart_rate: Optional[float]  # Estimated HR in BPM
    confidence: float  # Confidence score (0-1)
    signal: Optional[np.ndarray]  # Extracted PPG signal
    filtered_signal: Optional[np.ndarray]  # Filtered PPG signal
    is_valid: bool  # Whether result is valid


class POSMethod:
    """
    POS (Plane-Orthogonal-to-Skin) method for rPPG.
    
    Extracts heart rate from facial video by:
    1. Computing chrominance components
    2. Spatial averaging over face ROI
    3. Temporal filtering
    4. Heart rate estimation via spectral analysis
    """
    
    def __init__(
        self,
        fps: int = 30,
        window_seconds: int = 10,
        hr_min: int = 40,
        hr_max: int = 200,
    ):
        """
        Initialize POS algorithm.
        
        Args:
            fps: Frames per second of video
            window_seconds: Window size for processing
            hr_min: Minimum heart rate (BPM)
            hr_max: Maximum heart rate (BPM)
        """
        self.fps = fps
        self.window_seconds = window_seconds
        self.window_size = fps * window_seconds
        self.hr_min = hr_min
        self.hr_max = hr_max
        
        # Signal buffers
        self.rgb_buffer = deque(maxlen=self.window_size)
        self.signal_buffer = deque(maxlen=self.window_size)
        self.hr_buffer = deque(maxlen=60)  # Last 60 HR estimates
        
        # Create bandpass filter (0.4-4 Hz for 24-240 BPM)
        self.filter_b, self.filter_a = self._create_bandpass_filter()
        self.filter_state = None  # For stateful filtering
    
    def process_frame(self, frame_rgb: np.ndarray, roi_mask: Optional[np.ndarray] = None) -> POSResult:
        """
        Process a single frame and extract PPG signal.
        
        Args:
            frame_rgb: Input frame in RGB format (H, W, 3)
            roi_mask: Optional mask for face region
            
        Returns:
            POSResult with extracted signal and heart rate
        """
        # Extract ROI mean color
        mean_rgb = self._extract_mean_color(frame_rgb, roi_mask)
        self.rgb_buffer.append(mean_rgb)
        
        # Compute chrominance-based signal
        if len(self.rgb_buffer) < 2:
            return POSResult(
                heart_rate=None,
                confidence=0.0,
                signal=None,
                filtered_signal=None,
                is_valid=False,
            )
        
        # Extract PPG signal
        ppg_signal = self._extract_ppg_signal()
        
        # Filter signal
        filtered_signal = self._filter_signal(ppg_signal)
        
        # Extract heart rate if buffer is full enough
        if len(self.signal_buffer) >= self.window_size // 2:
            heart_rate, confidence = self._estimate_heart_rate(filtered_signal)
            is_valid = self._is_valid_estimate(heart_rate)
        else:
            heart_rate = None
            confidence = 0.0
            is_valid = False
        
        return POSResult(
            heart_rate=heart_rate,
            confidence=confidence,
            signal=np.array(ppg_signal) if len(ppg_signal) > 0 else None,
            filtered_signal=np.array(filtered_signal) if len(filtered_signal) > 0 else None,
            is_valid=is_valid,
        )
    
    def _extract_mean_color(
        self,
        frame: np.ndarray,
        roi_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Extract mean RGB color from ROI."""
        if roi_mask is not None:
            # Masked mean
            roi_frame = frame[roi_mask > 0]
            mean_rgb = np.mean(roi_frame.reshape(-1, 3), axis=0)
        else:
            # Full frame mean
            mean_rgb = np.mean(frame.reshape(-1, 3), axis=0)
        
        return mean_rgb.astype(np.float32)
    
    def _extract_ppg_signal(self) -> list:
        """
        Extract PPG signal using POS method.
        
        POS projects RGB variations onto the plane perpendicular to skin tone.
        """
        if len(self.rgb_buffer) < 2:
            return []
        
        # Convert to numpy array
        rgb_array = np.array(list(self.rgb_buffer), dtype=np.float32)
        
        # Normalize RGB
        rgb_norm = rgb_array / (np.linalg.norm(rgb_array, axis=1, keepdims=True) + 1e-6)
        
        # POS method: compute orthogonal projection
        # Compute temporal gradients
        rgb_grad = np.diff(rgb_norm, axis=0)
        
        # Compute skin tone direction (mean direction)
        mean_rgb = np.mean(rgb_norm, axis=0)
        mean_rgb = mean_rgb / (np.linalg.norm(mean_rgb) + 1e-6)
        
        # Project gradients onto plane perpendicular to skin tone
        projection = rgb_grad - np.outer(
            np.dot(rgb_grad, mean_rgb),
            mean_rgb
        )
        
        # Combine projections (weighted sum)
        signal = np.dot(projection, np.array([1, -1, 0], dtype=np.float32))
        
        self.signal_buffer.extend(signal.tolist())
        
        return list(self.signal_buffer)
    
    def _filter_signal(self, signal_data: list) -> list:
        """Apply bandpass filter to extract PPG signal."""
        if len(signal_data) < 5:
            return []
        
        signal_array = np.array(signal_data, dtype=np.float32)
        
        # Apply stateful filtering using scipy.signal.lfilter
        # This maintains filter state across frames for streaming processing
        if self.filter_state is None:
            self.filter_state = signal.lfilter_zi(self.filter_b, self.filter_a) * signal_array[0]
        
        filtered, self.filter_state = signal.lfilter(
            self.filter_b,
            self.filter_a,
            signal_array,
            zi=self.filter_state
        )
        
        return filtered.tolist()
    
    def _estimate_heart_rate(self, filtered_signal: np.ndarray) -> Tuple[Optional[float], float]:
        """
        Estimate heart rate from filtered PPG signal.
        
        Uses FFT to find dominant frequency in HR range.
        """
        if len(filtered_signal) < self.window_size // 4:
            return None, 0.0
        
        signal_array = np.array(filtered_signal, dtype=np.float32)
        
        # Apply window to reduce spectral leakage
        windowed_signal = signal_array * np.hanning(len(signal_array))
        
        # Compute FFT
        fft = np.fft.fft(windowed_signal)
        freqs = np.fft.fftfreq(len(windowed_signal), 1.0 / self.fps)
        
        # Get positive frequencies
        positive_mask = freqs > 0
        freqs_positive = freqs[positive_mask]
        fft_magnitude = np.abs(fft[positive_mask])
        
        # Find dominant frequency in HR range
        hr_range_mask = (freqs_positive >= self.hr_min / 60) & (freqs_positive <= self.hr_max / 60)
        
        if not np.any(hr_range_mask):
            return None, 0.0
        
        dominant_freq = freqs_positive[hr_range_mask][
            np.argmax(fft_magnitude[hr_range_mask])
        ]
        
        # Convert frequency to BPM
        heart_rate = dominant_freq * 60
        
        # Calculate confidence based on peak prominence
        peak_magnitude = np.max(fft_magnitude[hr_range_mask])
        noise_magnitude = np.mean(fft_magnitude[~hr_range_mask])
        confidence = min(peak_magnitude / (noise_magnitude + 1e-6), 1.0)
        
        # Store in buffer
        self.hr_buffer.append(heart_rate)
        
        return heart_rate, confidence
    
    def _is_valid_estimate(self, heart_rate: Optional[float]) -> bool:
        """Check if heart rate estimate is valid."""
        if heart_rate is None:
            return False
        
        # Check if within physiological range
        if not (self.hr_min <= heart_rate <= self.hr_max):
            return False
        
        # Check stability (if multiple estimates available)
        if len(self.hr_buffer) >= 3:
            recent_hrs = list(self.hr_buffer)[-3:]
            std_dev = np.std(recent_hrs)
            
            # HR should be relatively stable (std < 10 BPM)
            if std_dev > 10:
                return False
        
        return True
    
    def get_smoothed_heart_rate(self, window: int = 5) -> Optional[float]:
        """Get smoothed heart rate from recent estimates."""
        if len(self.hr_buffer) < window:
            return None
        
        recent_hrs = list(self.hr_buffer)[-window:]
        return np.median(recent_hrs)
    
    def _create_bandpass_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create bandpass filter for HR extraction.
        
        Passes 0.4-4 Hz (24-240 BPM range).
        """
        nyquist = self.fps / 2
        
        # Normalized frequencies (0-1, where 1 is Nyquist)
        low_freq = 0.4 / nyquist
        high_freq = 4.0 / nyquist
        
        # Clamp to valid range [0, 1)
        low_freq = np.clip(low_freq, 0.001, 0.999)
        high_freq = np.clip(high_freq, 0.001, 0.999)
        
        # Design Butterworth bandpass filter
        b, a = signal.butter(4, [low_freq, high_freq], btype='band')
        
        return b, a
    
    def reset(self):
        """Reset algorithm state (for new video/subject)."""
        self.rgb_buffer.clear()
        self.signal_buffer.clear()
        self.hr_buffer.clear()
        self.filter_state = None


# Example usage
if __name__ == "__main__":
    # Initialize POS method
    pos = POSMethod(fps=30, window_seconds=10)
    
    # Process frames from video
    # for frame_rgb in video_frames:
    #     roi_mask = ...  # Get from face detection
    #     result = pos.process_frame(frame_rgb, roi_mask)
    #     
    #     if result.is_valid:
    #         print(f"HR: {result.heart_rate:.1f} BPM (confidence: {result.confidence:.2f})")
    #     
    #     # Get smoothed estimate
    #     smoothed_hr = pos.get_smoothed_heart_rate(window=5)
    #     if smoothed_hr is not None:
    #         print(f"Smoothed HR: {smoothed_hr:.1f} BPM")
    
    print("POS Algorithm ready for integration with face detection module.")
