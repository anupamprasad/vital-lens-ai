# Dataset Sourcing Research - Phase 1

**Date:** February 28, 2026  
**Status:** Phase 1 Research

## Overview
This document catalogs diverse, high-quality datasets for training and validating the AI Face Scanner, with emphasis on skin tone diversity (Fitzpatrick Scale) and dermatological conditions.

---

## Part 1: Diverse Skin Tone Datasets (Fitzpatrick Scale Diversity)

### 1.1 UBFC-rPPG Dataset ⭐ **RECOMMENDED**
**Type:** Remote Photoplethysmography (PPG) Reference Dataset  
**URL:** https://sites.google.com/view/ybenezeth/ubfc-rppg

**Key Details:**
- **Size:** 42 videos × 8 subjects (336 total video clips)
- **Skin Tones:** Diverse (includes Fitzpatrick Types I-VI)
- **HR Reference:** Ground truth from FDA-approved pulse oximeter
- **Video specs:** 1920×1080, 30-60 FPS, RGB video + annotated PPG signal
- **Recording conditions:** Multiple lighting conditions (natural, fluorescent, LED)
- **Facial area:** Full face visible in frame

**Why it's valuable:**
- ✅ Direct rPPG validation dataset
- ✅ Diverse skin tones with known HR ground truth
- ✅ Multiple lighting conditions
- ✅ Open for research use
- ✅ Published in IEEE journals

**License:** Research use (check with authors for redistribution)  
**Download:** Available upon request from authors  
**Reference Paper:** Benezeth et al., 2015

---

### 1.2 PURE Dataset
**Type:** Face Video + PPG (Pulse rate) Annotation  
**URL:** https://www.cs.ubc.ca/labs/lci/face_anti_spoofing/

**Key Details:**
- **Size:** 10 subjects, 60 videos
- **Duration:** ~1 minute each
- **Resolution:** 640×480, 30 FPS
- **Skin Tones:** Limited diversity (primarily Western European)
- **Heart Rate Ground Truth:** Annotated from ECG during recording
- **Conditions:** Sitting, controlled lighting

**Why it's valuable:**
- ✅ High-quality PPG annotations
- ✅ Clean, controlled setup
- ✅ Good for algorithm benchmarking
- ✅ Widely used in literature

**Limitations:**
- ❌ Limited skin tone diversity (need supplementary datasets)
- ❌ Small subject pool
- ❌ Controlled conditions only

**License:** Academic research  
**Reference Paper:** Wang et al., 2016

---

### 1.3 FairFace Dataset ⭐ **RECOMMENDED for Skin Tone Diversity**
**Type:** Facial Attribute Dataset with Skin Tone Labels  
**URL:** https://github.com/dchen236/FairFace

**Key Details:**
- **Size:** 108,501 face images
- **Skin Tones:** Labeled in 6 categories:
  - Light
  - Medium
  - Tan
  - Olive
  - Deep Brown
  - Black
- **Demographics:** Age, gender, ethnicity annotations
- **Image Quality:** Diverse real-world conditions
- **License:** Non-commercial research

**Why it's valuable:**
- ✅ Largest skin-tone labeled dataset
- ✅ Real-world diversity
- ✅ Fitzpatrick-aligned skin tone labels
- ✅ Multiple demographic attributes
- ✅ Can be used to create balanced test sets

**Use Case:** Bias testing, model validation across skin tones  
**Reference Paper:** Karkkainen & Joo, 2021

---

### 1.4 UTKFace Dataset
**Type:** Large-scale face database with demographic labels  
**URL:** https://susanqq.github.io/UTKFace/

**Key Details:**
- **Size:** 20,000+ face images
- **Labels:** Age, gender, ethnicity (races 0-4)
- **Age Range:** 1-116 years
- **Image Format:** 200×200 aligned face crops
- **Resolution:** Varies (original images larger)

**Why it's valuable:**
- ✅ Large sample size
- ✅ Diverse ethnicity/skin tones
- ✅ Age and gender variation
- ✅ Aligned face crops ready for processing
- ✅ Open source

**Limitations:**
- ❌ No video data (static images only)
- ❌ Ethnicity labels less granular than skin tone
- ❌ Age may be inaccurate (crowdsourced labels)

**Use Case:** Training face detection/segmentation models  
**License:** Research use

---

### 1.5 MMPD Dataset (Multi-Modal Photoplethysmography Database)
**Type:** PPG + Video Multi-Modal Dataset  
**URL:** https://github.com/rmcquar/MMPD

**Key Details:**
- **Size:** 40 subjects, 1280 video clips
- **Duration:** 1-2 minutes per clip
- **Video specs:** 640×480, 20-30 FPS, RGB
- **PPG Ground Truth:** Contact-based fingertip PPG sensor (reference)
- **Skin Tones:** Moderate diversity
- **Metadata:** Subject ID, activity level, lighting conditions

**Why it's valuable:**
- ✅ Largest rPPG video dataset
- ✅ Synchronized PPG reference data
- ✅ Different activity levels (rest, exercise, post-exercise)
- ✅ Various lighting conditions
- ✅ Publicly available

**Use Case:** rPPG algorithm validation and benchmarking  
**License:** Open source (MIT-like)  
**Reference Paper:** Quar et al., 2022

---

### 1.6 CelebA Dataset
**Type:** Face image dataset with attribute labels  
**URL:** http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html

**Key Details:**
- **Size:** 200,000+ face images
- **Attributes:** 40 attributes (age, gender, expression, etc.)
- **Diversity:** High (celebrities from worldwide)
- **Resolution:** 178×218 minimum
- **Alignment:** Aligned face crops included

**Why it's valuable:**
- ✅ Massive diversity
- ✅ Multiple attribute annotations
- ✅ High-quality faces
- ✅ Useful for pre-training face models

**Limitations:**
- ❌ Primarily celebrities (bias)
- ❌ No PPG/vitals data
- ❌ No explicit skin tone labels (need to infer)

**Use Case:** Transfer learning for face detection/landmark models  
**License:** Non-commercial research

---

## Part 2: Annotated Dermatological Datasets

### 2.1 HAM10000 Dataset ⭐ **RECOMMENDED**
**Type:** Skin Lesion Classification Dataset  
**URL:** https://www.kaggle.com/datasets/kmader/skin-cancer-malignant-vs-benign

**Key Details:**
- **Size:** 10,015 dermatoscopic images
- **Classes:** 7 categories including:
  - Melanoma
  - Melanocytic Nevi
  - Benign Keratosis
  - Basal Cell Carcinoma
  - Actinic Keratosis
  - Vascular Lesions
  - Dermatofibroma
- **Image specs:** 450×600 (various), RGB
- **Metadata:** Age, sex, location on body, diagnosis method
- **Skin Tones:** Diverse (includes dark skin lesions)

**Why it's valuable:**
- ✅ Large, well-annotated dataset
- ✅ Includes diverse skin tones
- ✅ Professional dermatologist annotations
- ✅ Widely used in literature
- ✅ Good for detecting skin abnormalities

**Use Case:** Training skin condition detection models (Acne, Rosacea adjacent conditions)  
**License:** CC-BY-NC (non-commercial research)

---

### 2.2 ISIC Archive Dataset
**Type:** Melanoma and Skin Lesion Dataset  
**URL:** https://www.isic-archive.com/

**Key Details:**
- **Size:** 23,000+ annotated images
- **Focus:** Melanoma detection
- **Classes:** Melanoma, Nevus, Lentigines, Other
- **Image Quality:** Dermatoscopic (high magnification)
- **Metadata:** Age, sex, anatomical site, diagnosis
- **Skin Tones:** Diverse (important for bias reduction)

**Why it's valuable:**
- ✅ Largest public skin lesion dataset
- ✅ Multiple imaging modalities (dermoscopy, RGB, etc.)
- ✅ Diverse skin tones
- ✅ Professional medical annotations
- ✅ Actively maintained

**Use Case:** Skin anomaly detection, melanoma screening  
**License:** CC-0 (public domain) / CC-BY-NC (restrictions apply per image)

---

### 2.3 Acne7 Dataset
**Type:** Acne Severity Classification  
**URL:** https://github.com/xiaohanliu/Acne7

**Key Details:**
- **Size:** 1,000+ facial images
- **Focus:** Acne severity grading (0-7 scale)
- **Image specs:** RGB, face-focused
- **Skin Tones:** Limited diversity (mostly light-medium)
- **Annotations:** Severity score and acne location maps

**Why it's valuable:**
- ✅ Acne-specific dataset (relevant to project)
- ✅ Severity grading labels
- ✅ Face-centric views

**Limitations:**
- ❌ Limited skin tone diversity
- ❌ Smaller dataset size
- ❌ May need supplementation

**Use Case:** Acne detection and severity assessment  
**License:** Research use

---

### 2.4 ASNR (Acne Severity and Skin redness) Dataset
**Type:** Skin Condition & Redness Detection  
**URL:** Research-specific (may need to contact authors)

**Key Details:**
- **Focus:** Rosacea and skin redness detection
- **Annotations:** Redness intensity, affected area
- **Modality:** RGB face images + thermal imaging (some variants)

**Status:** Emerging datasets; specific URLs vary by research group

---

### 2.5 Makeup/Pigmentation Variation Dataset
**Type:** Skin Pigmentation & Color Variation  
**Resources:**
- **MSFVV (Makeup and Shade Face Visual Vocabulary):** Research dataset for makeup/pigmentation
- **Custom augmentation:** Use FairFace + CelebA with synthetic pigmentation variations

**Why valuable:**
- ✅ Addresses pigmentation variations
- ✅ Represents diverse skin tones

---

## Part 3: Supplementary Datasets for Bias Testing

### 3.1 CelebA-HQ
**Type:** High-resolution face image dataset  
**Details:** Upscaled version of CelebA (1024×1024)  
**Use:** High-fidelity face analysis

### 3.2 VGGFace2
**Type:** Face recognition dataset with high diversity  
**Size:** 3.31M images of 9,131 subjects  
**Diversity:** 60+ countries  
**Use:** Transfer learning, face embedding pre-training

### 3.3 Tufts Face Database
**Type:** Multimodal face database  
**Features:** RGB, thermal, depth data  
**Use:** Multi-modal validation (if integrating thermal imaging)

---

## Part 4: Dataset Sourcing Strategy & Licensing

### Recommended Acquisition Order:

**Priority 1 (Immediately Accessible):**
1. **FairFace** - Skin tone diversity labeling
2. **MMPD** - rPPG video + ground truth (GitHub open)
3. **HAM10000** - Dermatological baseline (Kaggle, free registration)
4. **ISIC Archive** - Extended dermatology (free registration)

**Priority 2 (Controlled Access):**
1. **UBFC-rPPG** - Contact authors (typically grants access for research)
2. **PURE Dataset** - Request from UBC (may have restrictions)

**Priority 3 (Supplementary):**
1. **CelebA** / **CelebA-HQ** - High-quality faces (Kaggle)
2. **UTKFace** - Aligned face crops
3. **VGGFace2** - For pre-training (requires registration)

---

## Part 5: Data Privacy & Licensing Compliance

### License Categories Summary:

| Dataset | License | Commercial? | Redistribution? | Notes |
|---------|---------|-------------|-----------------|-------|
| FairFace | CC-BY-NC | ❌ No | ❌ No | Research only |
| MMPD | MIT | ✅ Yes | ✅ Yes | Most permissive |
| HAM10000 | CC-BY-NC | ❌ No | ❌ No | Medical data |
| ISIC Archive | Mixed (per image) | Varies | Varies | Check each image |
| UBFC-rPPG | Custom (contact) | Negotiate | Contact authors | Typically for research |
| PURE | Academic | ❌ No | ❌ No | Research use |
| CelebA | Custom (non-commercial) | ❌ No | ❌ Limited | Academic use |
| UTKFace | Unclear / Open | ✅ Likely | ✅ Likely | Verify usage terms |
| VGGFace2 | Custom (research) | ❌ No | Restrict | Face recognition focus |

### Key Compliance Considerations:
- **Non-commercial focus:** Most datasets are "research only"
- **Public health exception:** Medical/health datasets often have special exemptions
- **Licensing strategy:** For commercial product, plan to:
  - Use open datasets (MMPD, possibly UTKFace) for primary development
  - Obtain commercial licenses for dermatology datasets
  - Consider synthetic data generation for augmentation
  - Document all data lineage for HIPAA compliance

---

## Part 6: Recommended Test Set Composition

### For Phase 1 Validation:

**Diverse Skin Tone Test Set (for algorithm bias testing):**
- 100+ samples from each Fitzpatrick category (I-VI)
- Multiple lighting conditions (natural, fluorescent, LED)
- Source: UBFC-rPPG (primary), MMPD (secondary), FairFace (tertiary)

**Dermatological Condition Test Set:**
- 50+ acne images (varying severity)
- 30+ rosacea/redness indicators
- 30+ pigmentation variations
- Source: HAM10000, ISIC, Acne7

**Hardware/Mobile Compatibility Test:**
- 200+ images at standard phone resolutions (1080×1920)
- Various face angles (-45° to +45°)
- Various distances (30cm - 1m)

---

## Part 7: Next Steps & Implementation Plan

**Phase 1 Deliverables:**
- [ ] Download & inventory all Priority 1 datasets
- [ ] Create dataset documentation (access paths, licensing, sample sizes)
- [ ] Build bias-diverse test set (500+ images across skin tones)
- [ ] Create data versioning system (DVC or similar)

**Phase 2 Deliverables:**
- [ ] Obtain Priority 2 datasets (contact authors)
- [ ] Create balanced training set
- [ ] Implement data augmentation pipeline

**Phase 3+ Deliverables:**
- [ ] Negotiate commercial licenses (if pivoting to product)
- [ ] Integrate synthetic data generation
- [ ] Establish continuous evaluation with bias metrics

---

## References

### Dataset Papers:
1. Benezeth, Y., et al. (2015) - UBFC-rPPG
2. Wang, W., et al. (2016) - PURE Dataset
3. Karkkainen, K., & Joo, H. (2021) - FairFace
4. Tschandl, P., et al. (2018) - HAM10000
5. Rotemberg, V., et al. (2021) - ISIC Archive
6. Liu, Z., et al. (2015) - CelebA

### Skin Tone Standards:
- Fitzpatrick Scale: Fitzpatrick, T. B. (1975) - Dermatologic Clinics

---

**Status:** Ready for acquisition and setup  
**Next Task:** Task 4 - Define camera hardware specifications
