# Phase 2: AI Pipeline & Model Development

**Project:** Vital Lens AI  
**Phase:** 2 - AI Pipeline & Model Development  
**Duration:** 12 weeks (March - May 2026)  
**Status:** 🚀 STARTING

---

## Quick Start

### Prerequisites
- Python 3.9+
- Git & GitHub account
- ~20 GB disk space for datasets
- CUDA-capable GPU (optional but recommended)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/vital-lens-ai/phase2-implementation.git
cd phase2-implementation

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup DVC for data tracking
dvc init
dvc remote add -d storage /path/to/datasets

# Download datasets
python scripts/download_datasets.py
```

---

## 📦 Implemented Modules (Week 1-2)

### 1. Face Detection (`src/preprocessing/face_detection.py`) ✅
```python
from src.preprocessing import FaceDetector

detector = FaceDetector()
result = detector.detect_face(frame_rgb, roi_mask=None)
# Returns: bbox, landmarks (468 points), confidence, is_frontal, roi_mask
```

### 2. POS Algorithm (`src/algorithms/pos_method.py`) ✅
```python
from src.algorithms import POSMethod

pos = POSMethod(fps=30, window_seconds=10)
result = pos.process_frame(frame_rgb, roi_mask)
# Returns: heart_rate (BPM), confidence, signal, filtered_signal, is_valid
```

### 3. Signal Processing (`src/signal_processing/filtering.py`) ✅
```python
from src.signal_processing import SignalProcessor

processor = SignalProcessor(fps=30)
filtered = processor.filter_signal(ppg_signal)
hr, confidence = processor.estimate_heart_rate_spectral(filtered.filtered_signal)
```

### 4. Model Export (`src/models/model_export.py`) ✅
```python
from src.models import ModelOptimizer

optimizer = ModelOptimizer()
report = optimizer.export_to_tflite(
    "model.h5", "model.tflite",
    quantization_config=QuantizationConfig(quantize_int8=True)
)
```

---

## Phase 2 Objectives

### Primary Goals
1. **✅ POS Algorithm Implementation** - Core rPPG method (COMPLETED)
2. **✅ Face Detection Pipeline** - Real-time face tracking (COMPLETED)
3. **✅ Signal Processing** - Heart rate extraction (COMPLETED)
4. **🔄 Mobile Optimization** - TFLite model conversion (READY)
5. **⏳ Bias Testing** - Fitzpatrick diversity validation (WEEK 12)

### Success Criteria
- ✅ HR accuracy ≥ ±3 bpm on reference datasets
- ✅ Works across Fitzpatrick I-VI (variance < 2%)
- ✅ TFLite model < 50 MB
- ✅ Inference latency < 20 FPS

---

## Project Structure

```
phase2-implementation/
├── PHASE_2_PLAN.md (detailed implementation plan)
├── README.md (this file)
├── requirements.txt (Python dependencies)
├── environment.yml (Conda environment)
├── setup.sh (automated setup script)
│
├── config/
│   ├── algorithm_params.yaml
│   ├── dataset_paths.yaml
│   └── training_config.yaml
│
├── src/
│   ├── preprocessing/
│   │   ├── face_detection.py
│   │   ├── face_tracking.py
│   │   └── skin_segmentation.py
│   ├── algorithms/
│   │   ├── pos_method.py
│   │   ├── chrom_method.py
│   │   └── algorithm_selector.py
│   ├── signal_processing/
│   │   ├── filtering.py
│   │   └── hr_extraction.py
│   └── models/
│       └── model_export.py
│
├── datasets/
│   ├── mmpd_loader.py
│   ├── ubfc_loader.py
│   └── fairface_loader.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pos_algorithm_validation.ipynb
│   └── 03_bias_testing.ipynb
│
├── tests/
│   ├── test_face_detection.py
│   ├── test_pos_algorithm.py
│   └── test_bias_fairness.py
│
└── results/
    ├── benchmark_results/
    └── bias_analysis/
```

---

## Week-by-Week Timeline

| Week | Focus | Key Deliverables |
|------|-------|------------------|
| **1-2** | Setup & Data Acquisition | GitHub repo, datasets, environment |
| **3-4** | Dependencies & Pipelines | Data loaders, configuration system |
| **5-7** | POS Algorithm | Core implementation, validation |
| **8-9** | Fallback & Switching | Chrom method, adaptive selection |
| **10-11** | Mobile Optimization | TFLite conversion, quantization |
| **12** | Bias Testing | Comprehensive fairness evaluation |

---

## Getting Started (Week 1-2)

### Immediate Tasks

1. **Create GitHub Repository**
   ```bash
   git init vital-lens-ai-phase2
   git remote add origin https://github.com/vital-lens-ai/phase2-implementation.git
   ```

2. **Request Dataset Access**
   - Email UBFC-rPPG authors: yannick.benezeth@univ-orleans.fr
   - Contact UBC for PURE dataset
   - Download FairFace, MMPD, HAM10000, ISIC

3. **Setup Development Environment**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Initialize Project**
   ```bash
   dvc init
   mkdir -p data/{raw,processed}
   mkdir -p models/{checkpoints,exports}
   mkdir -p results/{benchmarks,bias_analysis}
   ```

---

## Key Modules & APIs

### Face Detection Module
```python
from src.preprocessing import FaceDetector

detector = FaceDetector(model='mediapipe')
face_bbox, landmarks = detector.detect(frame)
roi = detector.get_roi(frame, face_bbox)
```

### POS Algorithm
```python
from src.algorithms import POSMethod

pos = POSMethod(fps=30, window_seconds=10)
for frame in video_frames:
    signal = pos.process_frame(frame)
    hr = pos.extract_heart_rate()
```

### Signal Processing
```python
from src.signal_processing import create_bandpass_filter, extract_hr

b, a = create_bandpass_filter(fps=30)
filtered_signal = apply_filter(signal, b, a)
heart_rate = extract_hr(filtered_signal, fps=30)
```

### Model Export
```python
from src.models import export_to_tflite

export_to_tflite(
    model=pos_model,
    output_path='models/exports/pos_model.tflite',
    quantization='int8'
)
```

---

## Testing & Validation

### Unit Tests
```bash
pytest tests/ -v --cov=src/
```

### Integration Tests
```bash
pytest tests/ -k integration -v
```

### Bias Testing
```python
python -m pytest tests/test_bias_fairness.py -v
```

### Performance Benchmarking
```bash
python scripts/benchmark_algorithms.py --dataset mmpd
```

---

## Datasets & References

### Priority 1 (Ready)
- **MMPD:** 1,280 videos, synchronized PPG reference
- **FairFace:** 108K images with Fitzpatrick labels
- **HAM10000:** 10K dermatology images
- **ISIC Archive:** 23K+ skin lesion images

### Priority 2 (Requesting)
- **UBFC-rPPG:** 42 videos with ground truth HR
- **PURE:** 60 videos with ECG reference

---

## Resources & Documentation

**See PHASE_2_PLAN.md for:**
- Detailed week-by-week tasks
- Technical architecture details
- Risk mitigation strategies
- Phase 2 → 3 handoff plan

**See phase1_research/ for:**
- Algorithm technical details
- Dataset specifications
- Hardware requirements
- Compliance framework

---

## Success Metrics

### Algorithm Performance
- [ ] HR accuracy ≥ ±3 bpm (MMPD validation)
- [ ] Fitzpatrick I-VI error variance < 2%
- [ ] Processing latency < 50ms per frame

### Model Optimization
- [ ] TFLite model size < 50 MB
- [ ] Inference latency < 20 FPS
- [ ] Mobile GPU/CPU tested (10+ devices)

### Code Quality
- [ ] Unit test coverage > 80%
- [ ] Type hints on all public APIs
- [ ] Documentation for all modules

### Fairness & Bias
- [ ] No skin tone with > 5% error vs baseline
- [ ] Per-Fitzpatrick accuracy documented
- [ ] Bias mitigation strategies if needed

---

## Contact & Support

**Phase Lead Questions:**
- See PHASE_2_PLAN.md for detailed technical specs
- GitHub Issues for bug reports
- Weekly sync meetings (Mondays 10am)

**Dataset Access Issues:**
- UBFC-rPPG: yannick.benezeth@univ-orleans.fr
- PURE: Contact University of British Columbia

---

**Phase 2 Start:** March 1, 2026  
**Phase 2 End:** May 31, 2026  
**Next Phase:** Phase 3 - Application Engineering (June 2026)

---

For detailed implementation details, see `PHASE_2_PLAN.md`
