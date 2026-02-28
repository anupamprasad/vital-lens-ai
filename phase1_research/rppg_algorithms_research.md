# rPPG (Remote Photoplethysmography) Algorithms Research

**Date:** February 28, 2026  
**Status:** Phase 1 Research

## Overview
Remote Photoplethysmography (rPPG) is a non-contact method to estimate blood volume variations from facial videos using optical sensors (standard RGB cameras). This document evaluates the most promising rPPG methods for heart rate (HR) and oxygen saturation (SpO2) detection.

---

## 1. Core rPPG Methods

### 1.1 Chrom (Chrominance-based) Method
**Authors:** De Haan & Jeanne, 2013

**How it works:**
- Extracts color changes in the face using chrominance components (based on the assumption that skin reflects light differently in red, green, and blue channels)
- Uses color space transformation to isolate PPG signals
- Decomposes RGB signals into orthogonal chrominance components

**Advantages:**
- ✅ Robust to slight head movements
- ✅ Handles lighting variations reasonably well
- ✅ Computational efficiency (real-time capable)
- ✅ Works across diverse skin tones better than green-channel only methods

**Disadvantages:**
- ❌ Moderate accuracy (±5-8 bpm error range)
- ❌ Sensitive to shadows on face
- ❌ Requires adequate lighting
- ❌ Struggles with large head rotations

**Use Case:** General-purpose HR detection, mobile apps
**Complexity:** Medium

---

### 1.2 OMIT (Orthogonal Moving Average Integrated Transparency) Method
**Status:** Emerging, optimized variant

**How it works:**
- Improves upon Chrom by using orthogonal transformation
- Applies temporal filtering to reduce noise
- Integrates multiple color channels more effectively

**Advantages:**
- ✅ Better noise rejection than Chrom
- ✅ Improved accuracy in low-light conditions
- ✅ Stable HR estimation across video durations
- ✅ Suitable for wearable applications

**Disadvantages:**
- ❌ Slightly more computationally intensive than Chrom
- ❌ Requires minimum video length for stability
- ❌ Sensitive to sudden lighting changes

**Use Case:** Mobile health apps, smartwatch integration
**Complexity:** Medium-High

---

### 1.3 POS (Plane-Orthogonal-to-Skin) Method
**Authors:** Wang et al., 2016

**How it works:**
- Models skin as a 2D plane in RGB space
- Extracts PPG signal perpendicular to this plane
- Projects color variations onto the direction perpendicular to skin tones

**Advantages:**
- ✅ Excellent accuracy for HR (±2-3 bpm error range)
- ✅ Works well with diverse skin tones
- ✅ Robust to lighting variations
- ✅ Handles moderate head movements

**Disadvantages:**
- ❌ Requires face segmentation preprocessing
- ❌ More computationally demanding
- ❌ Requires stable reference (works better with larger face regions)

**Use Case:** High-accuracy HR/SpO2 detection, clinical-grade wellness apps
**Complexity:** High

---

### 1.4 Green Channel Method (Simple ICA-based)
**Status:** Traditional baseline

**How it works:**
- Focuses on green channel variations (highest penetration into skin)
- Applies Independent Component Analysis (ICA) to extract PPG
- Uses bandpass filtering to isolate pulse frequency

**Advantages:**
- ✅ Simplest to implement
- ✅ Very fast computation
- ✅ Minimal memory footprint
- ✅ Good baseline for comparison

**Disadvantages:**
- ❌ Lowest accuracy among modern methods (±8-10 bpm)
- ❌ Very poor performance on dark skin tones
- ❌ Sensitive to lighting conditions
- ❌ Struggles with any head movement

**Use Case:** Educational projects, baseline testing only
**Complexity:** Low

---

### 1.5 Deep Learning-based Methods
**Examples:** CNN-based, LSTM, PhysNet, DeepPhys

**How it works:**
- End-to-end neural networks learn PPG signals directly from video frames
- Can incorporate temporal sequences for improved accuracy
- Models learn optimal feature extraction automatically

**Advantages:**
- ✅ Highest accuracy achievable (±1-2 bpm)
- ✅ Handles diverse conditions well (skin tone, lighting, movement)
- ✅ Can predict multiple vitals simultaneously
- ✅ Better generalization across scenarios

**Disadvantages:**
- ❌ Requires significant labeled training data
- ❌ High computational cost (GPU needed for training)
- ❌ Black-box interpretability issues
- ❌ Longer inference time on mobile devices
- ❌ Model optimization complex for edge deployment

**Use Case:** High-end healthcare apps, research
**Complexity:** Very High

---

## 2. Recommended Algorithm Selection for Vital Lens AI

### Primary Algorithm: **POS Method**
**Rationale:**
- Excellent balance of accuracy (±2-3 bpm), robustness, and computational efficiency
- Performs well across diverse skin tones (critical for bias reduction)
- Moderate computational complexity suitable for mobile optimization
- Proven in research and production environments

### Secondary/Fallback Algorithm: **Chrom Method**
**Rationale:**
- Faster fallback for low-power scenarios
- Good robustness to lighting variations
- Can provide real-time feedback during calibration

### Tertiary/Enhancement: **Deep Learning Ensemble**
**Rationale (Phase 3+):**
- Use small CNN model (quantized to TFLite) as confidence validator
- Ensemble predictions from POS + DL model for highest accuracy
- Only deploy if Phase 1 datasets support training

---

## 3. SpO2 (Oxygen Saturation) Extraction

### Challenge:
SpO2 requires ratios between different wavelengths (typically red:IR), but standard RGB cameras only provide R:G:B:

### Approach Options:

**Option A: Ratio-based Estimation (Limited)**
- Use R/G ratio as proxy for SpO2
- **Limitation:** Theoretical SpO2 prediction; accuracy typically ±4-6%
- **Suitable for:** Wellness-grade only, not clinical

**Option B: Chromatic Aberration Modeling**
- Model camera lens properties to infer near-IR information
- Complex calibration required; hardware-dependent

**Option C: Hardware Solution (Recommended for Phase 3+)**
- Integrate multi-wavelength LEDs or IR-capable camera
- Most reliable path to clinical-grade SpO2

### Interim Phase 1 Recommendation:
- **Focus on accurate HR first** with POS method
- Document SpO2 limitations clearly in compliance materials
- Position as "Wellness Indicator" not clinical measurement
- Plan Phase 3+ hardware integration for true SpO2

---

## 4. Implementation Roadmap

### Phase 1 Deliverable:
- [ ] Implement **POS algorithm** in Python with OpenCV
- [ ] Create test suite with reference HR data
- [ ] Benchmark across 3+ skin tone types
- [ ] Document preprocessing pipeline (face detection, ROI selection)

### Phase 2 Deliverable:
- [ ] Integrate **YOLOv8-Face** for face detection
- [ ] Add **Chrom method** as real-time fallback
- [ ] Optimize for mobile deployment (TFLite)

### Phase 3+ Deliverable:
- [ ] Train lightweight CNN model for ensemble
- [ ] Implement dual-wavelength camera support for SpO2
- [ ] Clinical validation against reference standards

---

## 5. References & Resources

### Key Papers:
1. De Haan, G., & Jeanne, V. (2013). "Robust Pulse Rate from Chrominance-based rPPG"
2. Wang, W., et al. (2016). "Algorithmic Principles of Remote Photoplethysmographic Imaging"
3. Song, R., et al. (2020). "Robust PPG Assessment Using Morphological and Chrominance-based Features"

### Open Source Projects:
- **PyPPG:** https://github.com/Jeremy-Tan/PyPPG
- **Face-Anti-Spoofing:** Resources for face liveness detection
- **MediaPipe Face:** Google's face detection solution

### Datasets for Validation:
- UBFC-rPPG (multi-skin-tone, annotated HR)
- PURE Dataset
- MMPD Dataset

---

## 6. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| SpO2 from RGB only | Accuracy limited to ±4-6% | Document wellness-only disclaimer; plan hardware upgrade |
| Skin tone bias | Higher error on dark skin | Use POS method; validate with diverse test data |
| Lighting variation | Accuracy degradation | Implement adaptive preprocessing; user feedback system |
| Head movement | Signal corruption | Combine POS with face tracking; establish stability threshold |
| Real-time performance | Battery drain on mobile | Optimize code; use face ROI only, not full frame |

---

**Next Steps:** Proceed to Task 2 - Dataset Sourcing
