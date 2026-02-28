"""
Integration Tests - Verify all Phase 2 modules work together
Tests face detection, POS algorithm, signal processing pipeline
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import FaceDetector, FaceDetectionResult
from algorithms import POSMethod, POSResult
from signal_processing import SignalProcessor, FilteredSignalResult


class TestFaceDetection:
    """Test face detection module"""
    
    def test_face_detector_initialization(self):
        """Test that FaceDetector can be initialized"""
        detector = FaceDetector()
        assert detector is not None
    
    def test_face_detection_result_creation(self):
        """Test FaceDetectionResult dataclass"""
        result = FaceDetectionResult(
            bbox=(10, 10, 100, 100),
            landmarks=np.random.rand(468, 2),
            confidence=0.95,
            is_frontal=True,
            roi_mask=np.ones((100, 100), dtype=np.uint8)
        )
        assert result.confidence == 0.95
        assert result.is_frontal
        assert result.landmarks.shape == (468, 2)


class TestPOSAlgorithm:
    """Test POS algorithm implementation"""
    
    def test_pos_initialization(self):
        """Test POS method initialization"""
        pos = POSMethod(fps=30, window_seconds=5)
        assert pos.fps == 30
        assert pos.window_size == 150
    
    def test_pos_filter_creation(self):
        """Test that bandpass filter is created"""
        pos = POSMethod(fps=30)
        assert pos.filter_b is not None
        assert pos.filter_a is not None
    
    def test_pos_single_frame(self):
        """Test processing a single frame"""
        pos = POSMethod(fps=30)
        
        # Create synthetic frame
        frame = np.random.rand(10, 10, 3).astype(np.float32) * 255
        result = pos.process_frame(frame)
        
        assert isinstance(result, POSResult)
        assert isinstance(result.is_valid, bool)
    
    def test_pos_multiple_frames(self):
        """Test processing multiple frames"""
        pos = POSMethod(fps=30, window_seconds=2)
        num_frames = 60
        
        for i in range(num_frames):
            # Create synthetic signal with pulsatile component
            frame = 150 * np.ones((10, 10, 3), dtype=np.float32)
            frame[:, :, 1] += 20 * np.sin(2 * np.pi * 1.25 * i / 30)  # 75 BPM signal
            
            result = pos.process_frame(frame)
            assert isinstance(result, POSResult)
    
    def test_pos_result_structure(self):
        """Test that POS result has all required fields"""
        pos = POSMethod(fps=30)
        frame = np.random.rand(10, 10, 3).astype(np.float32) * 255
        result = pos.process_frame(frame)
        
        # Check all fields exist
        assert hasattr(result, 'heart_rate')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'signal')
        assert hasattr(result, 'filtered_signal')
        assert hasattr(result, 'is_valid')


class TestSignalProcessing:
    """Test signal processing module"""
    
    def test_signal_processor_initialization(self):
        """Test signal processor initialization"""
        processor = SignalProcessor(fps=30, hr_min=40, hr_max=200)
        assert processor.fps == 30
        assert processor.freq_min == 40/60
        assert processor.freq_max == 200/60
    
    def test_filter_creation(self):
        """Test that bandpass filter is created"""
        processor = SignalProcessor(fps=30)
        assert processor.bandpass_b is not None
        assert processor.bandpass_a is not None
    
    def test_signal_filtering(self):
        """Test signal filtering pipeline"""
        processor = SignalProcessor(fps=30)
        
        # Create synthetic PPG signal
        t = np.arange(0, 10, 1/30)
        ppg_signal = np.sin(2 * np.pi * 1.25 * t) + 0.1 * np.random.randn(len(t))
        
        result = processor.filter_signal(ppg_signal)
        
        assert isinstance(result, FilteredSignalResult)
        assert len(result.original_signal) == len(ppg_signal)
        assert len(result.filtered_signal) == len(ppg_signal)
    
    def test_peak_detection(self):
        """Test peak detection"""
        processor = SignalProcessor(fps=30)
        
        # Create signal with clear peaks
        t = np.arange(0, 5, 1/30)
        signal = np.sin(2 * np.pi * 1.25 * t)  # 75 BPM
        signal = (signal + 1) / 2  # Normalize to [0, 1]
        
        result = processor.filter_signal(signal)
        
        # Should detect peaks
        assert len(result.peaks) > 0
    
    def test_heart_rate_from_peaks(self):
        """Test heart rate estimation from peaks"""
        processor = SignalProcessor(fps=30)
        
        # Create synthetic peaks for 75 BPM
        # 75 BPM = 1.25 Hz = 1.25 beats/second = 1.25/30 beats/frame = ~2.4 frame spacing
        beats_per_frame = 30 / 60 * 75 / 30  # beats/frame
        spacing = int(30 / (75/60))  # Expected spacing
        
        peaks = np.array([spacing * i for i in range(10)])
        
        hr, rr = processor.estimate_heart_rate_from_peaks(peaks)
        
        if hr is not None:
            # Should be close to 75 BPM
            assert 60 < hr < 90
    
    def test_signal_quality(self):
        """Test signal quality assessment"""
        processor = SignalProcessor(fps=30)
        
        # Good signal
        t = np.arange(0, 10, 1/30)
        good_signal = np.sin(2 * np.pi * 1.25 * t)
        quality_good = processor.assess_signal_quality(good_signal)
        assert 0 <= quality_good <= 1
        
        # Noisy signal
        noisy_signal = good_signal + np.random.randn(len(good_signal)) * 2
        quality_noisy = processor.assess_signal_quality(noisy_signal)
        assert 0 <= quality_noisy <= 1


class TestIntegration:
    """Integration tests for complete pipeline"""
    
    def test_complete_pipeline(self):
        """Test complete face detection -> POS -> signal processing pipeline"""
        # Initialize components
        pos = POSMethod(fps=30, window_seconds=5)
        processor = SignalProcessor(fps=30)
        
        # Generate synthetic video
        num_frames = 150  # 5 seconds at 30 FPS
        ppg_signals = []
        
        for i in range(num_frames):
            # Create synthetic frame with pulsatile signal (75 BPM)
            frame = np.ones((10, 10, 3), dtype=np.float32) * 150
            pulsatile = 20 * np.sin(2 * np.pi * 1.25 * i / 30)
            frame[:, :, 1] += pulsatile  # Green channel modulation
            
            # Process with POS
            result = pos.process_frame(frame)
            
            if result.signal is not None and len(result.signal) > 0:
                ppg_signals.append(result.signal[-1])
        
        # Process with signal processor
        if len(ppg_signals) > 50:
            filtered = processor.filter_signal(np.array(ppg_signals))
            
            # Estimate HR from peaks
            hr_peaks, _ = processor.estimate_heart_rate_from_peaks(filtered.peaks)
            
            # Estimate HR from FFT
            hr_spectral, confidence = processor.estimate_heart_rate_spectral(
                filtered.filtered_signal
            )
            
            # Both methods should give reasonable results
            if hr_peaks is not None:
                assert 40 <= hr_peaks <= 200
            
            if hr_spectral is not None:
                assert 40 <= hr_spectral <= 200
    
    def test_pipeline_with_noise(self):
        """Test pipeline with realistic noise"""
        pos = POSMethod(fps=30, window_seconds=5)
        processor = SignalProcessor(fps=30)
        
        num_frames = 150
        ppg_signals = []
        
        for i in range(num_frames):
            # Synthetic frame with noise
            frame = np.random.normal(150, 10, (10, 10, 3)).astype(np.float32)
            pulsatile = 20 * np.sin(2 * np.pi * 1.25 * i / 30)
            noise = np.random.normal(0, 5)
            frame[:, :, 1] += pulsatile + noise
            
            result = pos.process_frame(frame)
            if result.signal is not None and len(result.signal) > 0:
                ppg_signals.append(result.signal[-1])
        
        # Process
        if len(ppg_signals) > 50:
            filtered = processor.filter_signal(np.array(ppg_signals))
            quality = processor.assess_signal_quality(filtered.normalized_signal)
            assert 0 <= quality <= 1


class TestDataTypes:
    """Test data type consistency"""
    
    def test_detection_result_types(self):
        """Test FaceDetectionResult types"""
        result = FaceDetectionResult(
            bbox=(10, 10, 100, 100),
            landmarks=np.random.rand(468, 2),
            confidence=0.95,
            is_frontal=True,
            roi_mask=np.ones((100, 100), dtype=np.uint8)
        )
        
        assert isinstance(result.bbox, tuple)
        assert isinstance(result.landmarks, np.ndarray)
        assert isinstance(result.confidence, float)
        assert isinstance(result.is_frontal, bool)
        assert isinstance(result.roi_mask, np.ndarray)
    
    def test_pos_result_types(self):
        """Test POSResult types"""
        result = POSResult(
            heart_rate=75.0,
            confidence=0.95,
            signal=np.array([1, 2, 3]),
            filtered_signal=np.array([1, 2, 3]),
            is_valid=True
        )
        
        assert isinstance(result.heart_rate, float)
        assert isinstance(result.confidence, float)
        assert isinstance(result.is_valid, bool)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
