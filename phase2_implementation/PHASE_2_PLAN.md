# Phase 2 Implementation Plan - AI Pipeline & Model Development

**Start Date:** March 1, 2026  
**Duration:** 12 weeks (March - May 2026)  
**Status:** 🚀 STARTING NOW

---

## Phase 2 Overview

**Primary Objective:** Implement the AI pipeline with POS algorithm, face detection, rPPG signal processing, and mobile optimization.

**Expected Deliverables:**
- POS algorithm implementation (Python reference)
- Face detection module (MediaPipe/YOLOv8)
- rPPG signal processing pipeline
- Validation on reference datasets (UBFC-rPPG, MMPD)
- Mobile optimization (TFLite models)
- Bias testing framework

**Success Criteria:**
- HR accuracy ≥ ±3 bpm on reference datasets
- Works across Fitzpatrick I-VI (error variance < 2%)
- TFLite model < 50 MB
- Inference latency < 20 FPS processing delay

---

## Week-by-Week Execution Plan

### WEEK 1-2: Project Setup & Data Acquisition
**Focus:** Foundation setup, dataset access, environment configuration

**Tasks:**
- [x] Create GitHub repository (vital-lens-ai/phase2-implementation)
- [ ] Request UBFC-rPPG dataset access (email: yannick.benezeth@univ-orleans.fr)
- [ ] Request PURE dataset access (contact UBC)
- [ ] Download FairFace dataset (108K images)
- [ ] Download MMPD dataset (1,280 PPG videos)
- [ ] Download HAM10000 dataset (10K images)
- [ ] Register & download from ISIC Archive (23K+ images)
- [ ] Setup DVC (Data Version Control) for dataset tracking
- [ ] Create project directory structure
- [ ] Setup virtual environment (Python 3.9+)
- [ ] Install dependencies (TensorFlow, OpenCV, NumPy, Pandas, Scikit-learn)

**Deliverables:**
- GitHub repository with CI/CD setup
- DVC tracking configuration
- All Priority 1 datasets downloaded locally
- Python environment ready

---

### WEEK 3-4: Core Dependencies & Library Setup
**Focus:** ML framework setup, data loading pipelines

**Tasks:**
- [ ] Install TensorFlow/PyTorch with GPU support (if available)
- [ ] Install OpenCV for video processing
- [ ] Install MediaPipe for face detection
- [ ] Install signal processing libraries (SciPy, NumPy)
- [ ] Install visualization libraries (Matplotlib, Seaborn)
- [ ] Create data loading utilities (video reader, image processor)
- [ ] Build dataset classes (PyTorch Dataset/DataLoader or TensorFlow Datasets)
- [ ] Setup logging & monitoring infrastructure
- [ ] Create configuration management system (YAML configs)
- [ ] Document environment setup (requirements.txt, setup.sh)

**Deliverables:**
- Complete Python environment with all ML dependencies
- Reusable data loading pipelines
- Configuration system for experiments

---

### WEEK 5-7: POS Algorithm Implementation
**Focus:** Core POS algorithm development & validation

**Tasks:**

**5.1 Face Detection & Preprocessing:**
- [ ] Implement face detection using MediaPipe (alternative: YOLOv8)
- [ ] Create face tracking module (maintain face region across frames)
- [ ] Implement face orientation check (ensure face is frontal, ±20° tolerance)
- [ ] Build ROI (Region of Interest) extraction pipeline
- [ ] Implement skin region segmentation
- [ ] Create preprocessing pipeline (resizing, normalization)

**5.2 POS Algorithm Core:**
- [ ] Implement RGB to chrominance conversion (Cb, Cr channels)
- [ ] Build spatial averaging over ROI (face region)
- [ ] Implement temporal filtering (bandpass 0.4-4 Hz for 24-240 bpm)
- [ ] Create POS-specific color space projection
- [ ] Implement signal extraction from video frames
- [ ] Build heart rate estimation from extracted signal

**5.3 Validation & Testing:**
- [ ] Test on MMPD dataset (1,280 videos)
- [ ] Evaluate accuracy metrics (MAE, RMSE, correlation)
- [ ] Test across different video qualities
- [ ] Validate on different lighting conditions
- [ ] Create performance benchmarking notebook
- [ ] Document algorithm parameters & tuning

**Deliverables:**
- Complete POS algorithm implementation
- Validation notebook with results
- Performance benchmarks on reference data
- Algorithm documentation

---

### WEEK 8-9: Chrom Fallback & Adaptive Switching
**Focus:** Fallback algorithm & runtime switching logic

**Tasks:**
- [ ] Implement Chrom (Chrominance-based) algorithm
- [ ] Build algorithm selector logic (when to use Chrom vs POS)
- [ ] Create performance comparison tests
- [ ] Implement adaptive switching based on signal quality
- [ ] Build confidence scoring system
- [ ] Test fallback scenarios

**Deliverables:**
- Chrom algorithm implementation
- Adaptive switching logic
- Comparative performance analysis

---

### WEEK 10-11: Mobile Optimization & Model Conversion
**Focus:** Prepare models for iOS/Android deployment

**Tasks:**

**10.1 Model Optimization:**
- [ ] Profile algorithm performance on mobile CPUs
- [ ] Optimize NumPy/SciPy operations for mobile
- [ ] Implement memory-efficient processing
- [ ] Create streaming/online processing version (no need to load full video)
- [ ] Optimize for various mobile hardware

**10.2 TFLite Conversion (if using neural networks in Phase 2+):**
- [ ] Convert face detection model to TFLite
- [ ] Quantize models (int8 quantization for mobile)
- [ ] Test TFLite models on reference devices
- [ ] Optimize model size (target: < 50 MB total)
- [ ] Measure inference latency on mobile

**10.3 ONNX Export (for cross-platform):**
- [ ] Export core algorithm components to ONNX format
- [ ] Create ONNX inference wrapper
- [ ] Verify ONNX model accuracy

**Deliverables:**
- Optimized mobile-ready models
- TFLite + ONNX model formats
- Performance benchmarks on mobile hardware

---

### WEEK 12: Bias Testing & Final Validation
**Focus:** Comprehensive bias testing across skin tones

**Tasks:**
- [ ] Organize test set by Fitzpatrick skin types (I-VI)
- [ ] Run accuracy benchmarks per skin tone
- [ ] Calculate error variance across skin types
- [ ] Identify and document bias sources
- [ ] Create bias mitigation strategies (if needed)
- [ ] Test on diverse demographic datasets (FairFace)
- [ ] Generate bias assessment report

**Deliverables:**
- Comprehensive bias test report
- Accuracy metrics per Fitzpatrick type
- Bias mitigation recommendations
- Final Phase 2 validation report

---

## Technical Architecture

### Project Structure

```
vital-lens-ai/
├── phase2-implementation/
│   ├── README.md (Phase 2 overview)
│   ├── requirements.txt (Python dependencies)
│   ├── environment.yml (Conda environment)
│   ├── setup.sh (Setup script)
│   │
│   ├── config/
│   │   ├── algorithm_params.yaml
│   │   ├── dataset_paths.yaml
│   │   └── training_config.yaml
│   │
│   ├── src/
│   │   ├── __init__.py
│   │   ├── preprocessing/
│   │   │   ├── face_detection.py (MediaPipe)
│   │   │   ├── face_tracking.py
│   │   │   ├── skin_segmentation.py
│   │   │   └── normalization.py
│   │   ├── algorithms/
│   │   │   ├── pos_method.py (POS algorithm)
│   │   │   ├── chrom_method.py (Chrom algorithm)
│   │   │   └── algorithm_selector.py
│   │   ├── signal_processing/
│   │   │   ├── filtering.py (bandpass, temporal)
│   │   │   ├── peak_detection.py
│   │   │   └── hr_extraction.py
│   │   └── models/
│   │       ├── model_export.py (TFLite, ONNX)
│   │       └── quantization.py
│   │
│   ├── datasets/
│   │   ├── mmpd_loader.py
│   │   ├── ubfc_loader.py
│   │   ├── fairface_loader.py
│   │   └── dataset_utils.py
│   │
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_pos_algorithm_validation.ipynb
│   │   ├── 03_bias_testing.ipynb
│   │   └── 04_mobile_optimization.ipynb
│   │
│   ├── tests/
│   │   ├── test_face_detection.py
│   │   ├── test_pos_algorithm.py
│   │   ├── test_accuracy_metrics.py
│   │   └── test_bias_fairness.py
│   │
│   ├── results/
│   │   ├── benchmark_results/
│   │   ├── bias_analysis/
│   │   └── model_exports/
│   │
│   └── .github/
│       └── workflows/
│           ├── ci_tests.yml
│           └── performance_benchmarks.yml
```

---

## Key Implementation Details

### 1. Face Detection (MediaPipe)
```python
# Pseudocode for face detection module
import mediapipe as mp
import cv2

class FaceDetector:
    def __init__(self):
        self.face_detection = mp.solutions.face_detection
        self.detector = self.face_detection.FaceDetection()
    
    def detect_and_track(self, frame):
        # Returns: face_bbox, landmarks, confidence
        # Validates: face is centered (within ±20° yaw/pitch)
        pass
    
    def get_roi(self, frame, face_bbox):
        # Returns: ROI (Region of Interest) for signal extraction
        pass
```

### 2. POS Algorithm Core
```python
# Pseudocode for POS implementation
class POSMethod:
    def __init__(self, fps=30, seconds=10):
        self.fps = fps
        self.buffer_size = fps * seconds
        self.color_buffer = []
    
    def process_frame(self, frame_rgb):
        # 1. Extract ROI (face region)
        # 2. Calculate chrominance (C = [R-G, B-G])
        # 3. Spatial averaging
        # 4. Temporal filtering
        # 5. POS projection
        pass
    
    def extract_heart_rate(self):
        # 1. FFT on filtered signal
        # 2. Find dominant frequency (0.4-4 Hz)
        # 3. Convert to BPM (frequency * 60)
        pass
```

### 3. Signal Processing Pipeline
```python
# Bandpass filtering (0.4-4 Hz for HR extraction)
from scipy import signal

def create_bandpass_filter(fps=30):
    # Nyquist frequency = fps/2
    nyquist = fps / 2
    low_freq = 0.4 / nyquist
    high_freq = 4.0 / nyquist
    
    b, a = signal.butter(5, [low_freq, high_freq], btype='band')
    return b, a
```

### 4. Bias Testing Framework
```python
# Pseudocode for bias evaluation
class BiasTestSuite:
    def __init__(self, model, test_data_by_skin_tone):
        self.model = model
        self.test_data = test_data_by_skin_tone
    
    def evaluate_per_skin_tone(self):
        results = {}
        for skin_tone in ['I', 'II', 'III', 'IV', 'V', 'VI']:
            mae = calculate_mae(test_data[skin_tone])
            rmse = calculate_rmse(test_data[skin_tone])
            results[skin_tone] = {'mae': mae, 'rmse': rmse}
        return results
    
    def calculate_fairness_metrics(self):
        # Calculate maximum error variance
        # Goal: < 2% variance across all skin tones
        pass
```

---

## Dependencies & Tools

### Core ML/Data Science
- **TensorFlow 2.11+** - Neural network framework (if using DL models)
- **PyTorch 2.0+** - Alternative DL framework
- **OpenCV 4.7+** - Video processing
- **MediaPipe 0.8+** - Face detection & landmarks
- **NumPy 1.24+** - Numerical computing
- **SciPy 1.10+** - Signal processing
- **Pandas 2.0+** - Data handling
- **Scikit-learn 1.2+** - ML utilities

### Optimization & Deployment
- **TFLite Converter** - Mobile model conversion
- **ONNX Runtime** - Cross-platform inference
- **Netron** - Model visualization

### Testing & Validation
- **Pytest** - Unit testing
- **Pytest-cov** - Code coverage
- **Scikit-learn metrics** - Performance evaluation

### Visualization & Notebooks
- **Jupyter Lab** - Interactive notebooks
- **Matplotlib** - Plotting
- **Seaborn** - Statistical visualization

### Data Management
- **DVC (Data Version Control)** - Dataset tracking
- **Git** - Code version control

---

## Success Metrics & Checkpoints

### Week 2 Checkpoint
- [ ] GitHub repo created & initialized
- [ ] All Priority 1 datasets downloaded
- [ ] Python environment ready
- [ ] DVC configured

### Week 4 Checkpoint
- [ ] All dependencies installed
- [ ] Data loading pipelines working
- [ ] Configuration system ready

### Week 7 Checkpoint
- [ ] POS algorithm implemented
- [ ] Validation on MMPD complete
- [ ] Accuracy ≥ ±3 bpm achieved
- [ ] Performance benchmarks documented

### Week 9 Checkpoint
- [ ] Chrom algorithm implemented
- [ ] Algorithm switching logic complete
- [ ] Fallback scenarios tested

### Week 11 Checkpoint
- [ ] TFLite models created
- [ ] Model size < 50 MB
- [ ] Latency < 20 FPS achieved
- [ ] Mobile hardware tested

### Week 12 Checkpoint
- [ ] Bias testing complete
- [ ] Fitzpatrick I-VI validated
- [ ] Error variance < 2% achieved
- [ ] Phase 2 report complete

---

## Phase 2 → Phase 3 Transition

**Deliverables for Phase 3 Team:**
1. Trained POS algorithm (Python reference + TFLite models)
2. Face detection module (MediaPipe)
3. Signal processing pipeline
4. Bias testing results & recommendations
5. Performance benchmarks on mobile hardware
6. Algorithm documentation & implementation guide
7. Test data & validation notebooks

**Handoff Documents:**
- Algorithm specification document
- Mobile optimization guide
- API documentation
- Performance benchmark report
- Bias assessment & mitigation strategies

---

## Notes & Risk Mitigation

### Key Risks in Phase 2

**Risk 1: Dataset Delay (UBFC-rPPG)**
- Mitigation: Start with MMPD dataset first (already available), validate fully before UBFC arrives

**Risk 2: Accuracy Not Meeting ±3 bpm Target**
- Mitigation: Have Chrom method as fallback, ensemble both methods, explore hyperparameter tuning

**Risk 3: Mobile Latency Issues**
- Mitigation: Profile early (Week 6), optimize bottlenecks incrementally, target streaming inference

**Risk 4: Bias Issues in Specific Skin Tones**
- Mitigation: Test iteratively per week, document issues early, adjust preprocessing if needed

**Risk 5: Model Size Exceeds 50 MB**
- Mitigation: Aggressive quantization, pruning, knowledge distillation as backup

---

**Phase 2 Start Date:** March 1, 2026  
**Expected Completion:** May 31, 2026  
**Next Phase:** Phase 3 - Application Engineering (June 2026)
