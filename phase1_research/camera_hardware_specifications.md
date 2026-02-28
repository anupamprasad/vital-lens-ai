# Camera Hardware Specifications & Requirements - Phase 1

**Date:** February 28, 2026  
**Status:** Phase 1 Research

## Overview
This document defines the minimum and optimal camera specifications required for accurate rPPG (Remote Photoplethysmography) pulse detection across different deployment scenarios.

---

## Part 1: rPPG Technical Requirements

### 1.1 Core Camera Parameters for PPG Signal Detection

#### **Resolution Requirement**

**Minimum Viable Resolution:**
- **Mobile phones:** 1080 × 1920 (or equivalent, e.g., 1440 × 2560)
- **Tablets/Desktop:** 720 × 1280 (or higher)
- **Why:** PPG signal is extracted from subtle color variations in skin pixels. Very low resolution (< 480p) loses necessary detail.

**Optimal Resolution:**
- **Full HD (1080p):** 1920 × 1080 for smartphones
- **2K:** 2560 × 1440 for tablets/laptops
- **Better signal-to-noise ratio** with more pixels per face region

**Details:**
- Facial area should occupy **at least 200 × 200 pixels** (preferably 400 × 400+)
- Green channel needs sufficient pixel count for color variation detection
- Higher resolution = better PPG signal extraction, but demands more processing power

---

#### **Frame Rate (FPS) Requirement**

**Fundamental Constraint (Nyquist Theorem):**
- PPG signal captures heart rate variations
- Typical heart rate range: 40-180 bpm
- Maximum frequency of interest: ~3 Hz (180 bpm ÷ 60 = 3 Hz)
- **Minimum FPS needed: 6 FPS** (Nyquist: 2× max frequency)

**Practical Minimum:**
- **15 FPS:** Bare minimum for noisy environments
- **30 FPS:** Standard mobile phone frame rate (recommended minimum)

**Optimal Frame Rate:**
- **30-60 FPS:** Excellent signal quality
  - 30 FPS = 0.033 sec per frame = good temporal resolution
  - 60 FPS = 0.017 sec per frame = very smooth signal
  - Diminishing returns above 60 FPS for PPG

**Mobile Device Typical Specs:**
- Most modern phones: 30 FPS (standard), up to 60/120 FPS (high-end)
- Video codec stability important at chosen FPS

**Trade-offs:**
| FPS | Latency | Signal Quality | Mobile Battery | Recommended Use |
|-----|---------|---------------|----------------|----|
| 15 | 66 ms | Poor | ✅ Good | Emergency only |
| 30 | 33 ms | Good | ✅ Good | Standard (recommended) |
| 60 | 16 ms | Excellent | ⚠️ Moderate | High-accuracy scenarios |
| 120 | 8 ms | Overkill | ❌ Poor | Not recommended |

---

#### **Sensor Type & Color Depth**

**RGB vs. Grayscale:**
- ✅ **RGB (8-bit per channel):** REQUIRED
- ❌ Grayscale: Not suitable (loses color information needed for rPPG)
- **Reason:** PPG exploits differences in light absorption across R, G, B channels

**Color Depth Requirements:**
- **Minimum:** 24-bit color (8-bit R, 8-bit G, 8-bit B)
- **Recommended:** 24-bit or 32-bit (with alpha channel for compatibility)

**Sensor Characteristics:**

| Property | Requirement | Reasoning |
|----------|-------------|-----------|
| **Spectral Range** | Visible light (400-700 nm) | Standard RGB sensors; IR filtering may reduce signal |
| **Bayer Pattern** | Standard CFA (Color Filter Array) | All consumer cameras use this |
| **Dynamic Range** | ≥ 60 dB recommended | Handles shadows and bright areas |
| **Rolling vs. Global Shutter** | Global preferred, rolling acceptable | PPG works with both, but global shutter more stable |
| **Sensor Size** | Not critical | Compact phones to full-frame DSLRs all work |
| **Auto-exposure** | Disable or control | Constant brightness = stable PPG signal |

---

### 1.2 Lighting Conditions Impact

#### **Illumination Level Requirement**

**Minimum Illumination:**
- **50 lux:** Dim indoor (dusk lighting)
- **500 lux:** Standard indoor (office fluorescent)
- **1,000+ lux:** Bright indoor or outdoor (daylight)

**Practical Requirement:**
- **Minimum 100 lux:** For reliable PPG detection
- **Optimal: 300-1,000 lux:** Best signal quality
- **Above 1,500 lux:** May cause overexposure; requires exposure control

**Environmental Lighting Types:**
| Light Source | Characteristics | PPG Impact | Mitigation |
|--------------|-----------------|-----------|-----------|
| **Incandescent (2,700K)** | Warm, stable, low flicker | ✅ Excellent | Baseline reference |
| **Fluorescent (4,000K)** | Cool, 50/60 Hz flicker | ⚠️ Moderate | Requires 100+ FPS to reject flicker |
| **LED (5,000-6,500K)** | Cool, low flicker if quality | ✅ Good | Preferred for modern apps |
| **Sunlight (5,500-6,500K)** | High intensity, direct/diffuse | ⚠️ High noise | Requires face tracking & adaptive exposure |
| **Mixed (multiple sources)** | Unstable color cast | ❌ Poor | Real-time white balance adjustment needed |

---

### 1.3 Motion & Stability Requirements

**Face Movement Tolerance:**

| Movement Type | Acceptable Range | Algorithm Robustness |
|--------------|------------------|----------------------|
| **Pitch (up/down)** | ±15° | POS method: Good; Chrom: Moderate |
| **Yaw (left/right)** | ±20° | POS method: Good; Chrom: Moderate |
| **Roll (head tilt)** | ±10° | Most algorithms: Good |
| **Micro-motion** | < 5 pixels/frame | Most algorithms: Excellent |
| **Rapid movement** | > 10 pixels/frame | Most algorithms: Fail |

**Stability Metrics:**
- **Acceleration threshold:** < 50 pixels/frame² for reliable signal
- **Jitter tolerance:** ± 5 pixels (acceptable)
- **Hold-still requirement:** 10-15 seconds recommended for accuracy

---

## Part 2: Mobile Device Specifications

### 2.1 Smartphone Minimum Requirements

**CPU/GPU:**
- **Minimum:** Quad-core processor, 2+ GHz (e.g., Snapdragon 636 or equivalent)
- **Recommended:** Octa-core, 2.5+ GHz with GPU acceleration
- **Why:** Real-time video processing + ML inference on-device

**RAM:**
- **Minimum:** 2 GB RAM
- **Recommended:** 4+ GB RAM (for smooth processing + background system tasks)

**Storage:**
- **Minimum:** 500 MB free space (for app + temporary buffers)
- **Recommended:** 1+ GB free space

**Camera Hardware:**
- **Rear camera resolution:** ≥ 12 MP (for high-quality captures)
- **Front camera resolution:** ≥ 5 MP (typically sufficient)
- **Video capabilities:** ≥ 30 FPS at 1080p (mandatory)
- **Auto-focus:** Optional but helpful
- **Flash/LED:** Not required (can interfere with PPG)

**Battery:**
- **Minimum:** 2,500 mAh (sufficient for 15-20 min session)
- **Recommended:** 3,500+ mAh

**Operating Systems & Versions:**
- **iOS:** 12+ (for iPhone 6s and later)
  - Front camera capability (Face ID hardware optional)
  - Metal or CoreVideo framework for efficient processing
- **Android:** 8.0+ (API level 26+)
  - Camera2 API access
  - OpenGL ES 3.0 or Vulkan support

---

### 2.2 Tablet/Desktop Specifications

**Display-based/External Camera:**
- **Resolution:** 1080p minimum (2K+ preferred)
- **FPS:** 30+ FPS
- **Sensor:** Standard RGB CMOS
- **Connection:** USB 3.0+ for laptop/desktop integration

**Processing Power:**
- **CPU:** Multi-core processor (≥ 4 cores)
- **GPU:** Dedicated GPU preferred (e.g., NVIDIA GeForce, Apple GPU)
- **RAM:** 4+ GB (8+ GB recommended)

**Use Case:** Clinical/wellness stations, research settings

---

## Part 3: Hardware-Specific Recommendations

### 3.1 Recommended Mobile Phones (as of Feb 2026)

**Budget-Friendly (< $300):**
- Xiaomi Redmi Note series
- Samsung Galaxy A series
- **Camera:** 1080p @ 30 FPS, decent lighting

**Mid-Range ($300-700):**
- OnePlus Nord series
- Google Pixel 6a / 7
- Samsung Galaxy S22/S23 (older flagships)
- **Camera:** Excellent low-light, 1080p @ 60 FPS

**Premium ($700+):**
- iPhone 14/15 Pro
- Google Pixel 8 Pro
- Samsung Galaxy S24
- **Camera:** Advanced computational photography, thermal sensors (future option)

### 3.2 Desktop/Webcam Setups

**Recommended Webcams:**
- **Logitech C920 HD Pro (1080p, 30 FPS):** Solid baseline
- **Logitech C922 (1080p, 30/60 FPS):** With background replacement
- **Microsoft LifeCam HD-3000 (720p, 30 FPS):** Lower-cost option
- **Razer Kiyo (1080p, 30/60 FPS):** Gaming-grade quality

**External USB Cameras (for research):**
- **IDS Ensenso:** Industrial-grade RGB cameras
- **Allied Vision:** Professional machine vision cameras

---

## Part 4: Software/Codec Considerations

### 4.1 Video Codec Impact on PPG Signal

**H.264 (AVC):**
- ✅ Universal support
- ✅ Good compression
- ⚠️ Compression artifacts can introduce noise in PPG signal

**H.265 (HEVC):**
- ✅ Better compression (smaller files)
- ✅ Lower bandwidth for streaming
- ⚠️ More complex decoding (higher CPU usage)

**VP9 / AV1:**
- ✅ Open source
- ⚠️ Less hardware acceleration on mobile

**Recommendation:**
- **For research:** Use lossless codec or RAW if possible
- **For production mobile app:** H.264 (widely supported)
- **Trade-off:** Quality vs. file size/bandwidth

### 4.2 Color Space Considerations

**RGB vs. YUV:**
- **RGB:** Direct access to R, G, B channels (preferred for rPPG)
- **YUV:** More efficient storage; requires conversion (adds latency)

**Recommendation:**
- Capture in **RGB** natively if possible
- If YUV is enforced by device, convert during preprocessing

---

## Part 5: Phase 1 Implementation Specifications

### 5.1 Target Device Profiles

**Profile A: Standard Modern Smartphone**
- Resolution: 1080 × 1920
- FPS: 30
- Sensor: Standard RGB CMOS
- Color: 24-bit RGB
- Face size: 300-500 pixels (optimal)
- Lighting: 200-1,500 lux
- Stability: ±15° pitch/yaw, ±10° roll

**Profile B: Tablet/Desktop (for wellness stations)**
- Resolution: 1440 × 2560 or 1920 × 1080 (monitor-based)
- FPS: 30-60
- Camera: Dedicated USB or built-in
- Lighting: Controlled (500-1,000 lux)

**Profile C: Research/Reference Grade**
- Resolution: 2K+ (2560 × 1440)
- FPS: 60
- Codec: Lossless or RAW
- Lighting: Controlled, calibrated
- Reference ground truth: ECG/pulse oximeter synchronized

---

### 5.2 Minimum Viable Product (MVP) Camera Requirements

**For Phase 1 Prototype:**
```
Resolution: ≥ 720p (1280 × 720 minimum, 1080p recommended)
Frame Rate: ≥ 30 FPS (stable)
Color: RGB (24-bit minimum)
Lighting: ≥ 100 lux (preferably 200-1,000 lux)
Face Region: ≥ 200 × 200 pixels (preferably ≥ 400 × 400)
Movement Tolerance: ±15° yaw, ±10° pitch
```

**Reference Ground Truth:**
- Smartphone camera (front/rear at 1080p @ 30 FPS)
- Optional: Medical-grade pulse oximeter for validation

---

### 5.3 Performance Benchmarks (Target)

**For Optimal PPG Detection:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Heart Rate Accuracy** | ± 3 bpm | Comparison vs. reference oximeter |
| **Latency** | < 2 seconds | Time from start video to first HR estimate |
| **Stability** | < 5 bpm drift | After 15-second stabilization |
| **Lighting Robustness** | Works 50-1,500 lux | Performance across illumination range |
| **Skin Tone Invariance** | ≤ 2% error difference | Between Fitzpatrick types I & VI |
| **Motion Robustness** | Tolerates ±15° movement | Head movement during capture |

---

## Part 6: Hardware-Software Integration Checklist

### Phase 1 Testing Protocol

**Mobile Device Testing:**
- [ ] Test with 5+ different smartphone models (various brands/generations)
- [ ] Verify 1080p @ 30 FPS capture stability
- [ ] Test in lighting conditions: dim (100 lux), standard (500 lux), bright (1,500 lux)
- [ ] Test with different skin tones (Fitzpatrick I-VI)
- [ ] Validate battery consumption (target: < 20 mA during video capture)

**Camera Parameter Validation:**
- [ ] Disable/lock auto-exposure (constant brightness required)
- [ ] Disable/lock white balance (consistent color channels)
- [ ] Disable facial recognition features (may alter camera access)
- [ ] Test with face angles: frontal (0°), ±15° pitch, ±20° yaw

**Software Optimization Targets:**
- [ ] GPU acceleration (if available): Process green channel on GPU
- [ ] Memory efficiency: Stream processing (don't load entire video)
- [ ] Battery optimization: Reduce FPS dynamically if CPU throttled
- [ ] Fail-safe: Revert to Chrom method if POS struggles (fallback)

---

## Part 7: Risk Assessment & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| **Low light (< 100 lux)** | PPG signal degradation | High | Adaptive exposure + user guidance |
| **High motion** | Signal loss | Medium | Face tracking + stability threshold |
| **Skin tone bias** | Algorithm error variance | Medium | Validate across Fitzpatrick types |
| **Cheap camera quality** | Noise in signal | Low | Set minimum device specs |
| **Encoding artifacts** | PPG noise | Low | Use lossless codec for research |
| **Processing lag** | User experience | Medium | Optimize for target devices early |

---

## Part 8: Next Steps

**Phase 1 Deliverables:**
- [ ] Create reference camera specification document
- [ ] Build hardware compatibility matrix
- [ ] Test POS algorithm on 3+ device profiles
- [ ] Document camera API requirements (iOS/Android)

**Phase 2 Deliverables:**
- [ ] Implement adaptive exposure control
- [ ] Add multi-device optimization layer
- [ ] Create device capability detection system

**Phase 3+ Deliverables:**
- [ ] Integrate multi-wavelength LED (for SpO2)
- [ ] Support thermal imaging (for advanced diagnostics)
- [ ] Implement cloud offload option (for low-power devices)

---

## References

### Technical Standards:
- **ITU-R BT.709:** RGB color space definition
- **NTSC/PAL:** Video frame rate standards
- **Nyquist-Shannon:** Sampling theorem

### Relevant Papers:
1. De Haan & Jeanne (2013) - Chrominance-based rPPG
2. Wang et al. (2016) - Plane-Orthogonal-to-Skin method
3. Verkruysse, W., et al. (2008) - Detecting pulse rate changes

### Device Specifications:
- iPhone technical specs: apple.com
- Android Camera2 API: developer.android.com
- USB camera standards: usb.org

---

**Status:** Complete  
**Next Task:** Task 5 - Draft HIPAA/GDPR compliance architecture
