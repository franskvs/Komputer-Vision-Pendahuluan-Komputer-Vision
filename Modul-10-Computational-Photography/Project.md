# PROJECT BAB 10: COMPUTATIONAL PHOTOGRAPHY
## "PhotoEnhance Pro" - Intelligent Photo Enhancement System

---

## 📌 DESKRIPSI PROJECT

### Overview
Mahasiswa akan mengembangkan **PhotoEnhance Pro**, sebuah sistem enhancement foto cerdas yang menggabungkan berbagai teknik computational photography untuk menghasilkan foto berkualitas profesional secara otomatis.

### Latar Belakang
Fotografi smartphone telah menjadi ubiquitous, namun banyak foto yang diambil dalam kondisi tidak ideal (low-light, high contrast, noisy). Sistem ini bertujuan untuk automatically enhance foto sehingga terlihat seperti diambil dengan equipment profesional.

---

## 🎯 TUJUAN PROJECT

1. Mengembangkan pipeline enhancement foto otomatis
2. Mengimplementasikan multiple computational photography techniques
3. Membuat UI yang user-friendly untuk photo enhancement
4. Memahami trade-offs dalam image processing

---

## 📋 SPESIFIKASI SISTEM

### A. Fitur Utama

#### 1. Auto Enhancement Mode
```
Input Image → Analysis → Enhancement Selection → Processing → Output
```

| Analysis | Enhancement Applied |
|----------|---------------------|
| Dark/underexposed | Exposure boost, shadow recovery |
| Noisy | Denoising (NLM/BM3D) |
| Low contrast | CLAHE, auto-levels |
| Color cast | White balance correction |
| Soft/blurry | Sharpening |

#### 2. Manual Enhancement Mode
- Exposure adjustment (-3 to +3 EV)
- Contrast control (0-200%)
- Saturation adjustment (0-200%)
- Sharpness (0-100%)
- Noise reduction (0-100%)
- White balance (temperature/tint)

#### 3. HDR Mode
- Load multiple exposures
- Auto-alignment
- Exposure fusion atau HDR merge
- Tone mapping options
- Ghost removal

#### 4. Portrait Mode
- Face/subject detection
- Depth estimation (neural network atau traditional)
- Adjustable bokeh strength
- Foreground/background separation
- Edge refinement

#### 5. Batch Processing
- Process multiple photos with same settings
- Preset creation dan management
- Export dalam berbagai formats dan qualities

### B. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PhotoEnhance Pro                       │
├──────────────────┬──────────────────┬───────────────────┤
│   Image Loader   │   Analyzer       │   UI Controller   │
├──────────────────┼──────────────────┼───────────────────┤
│                  Processing Pipeline                      │
│  ┌────────────┬────────────┬────────────┬─────────────┐ │
│  │ Exposure   │ Denoising  │ Color      │ Sharpening  │ │
│  │ Control    │ Module     │ Correction │ Module      │ │
│  └────────────┴────────────┴────────────┴─────────────┘ │
├──────────────────────────────────────────────────────────┤
│  ┌────────────┬────────────┬────────────┬─────────────┐ │
│  │ HDR        │ Portrait   │ Batch      │ Preset      │ │
│  │ Module     │ Mode       │ Processor  │ Manager     │ │
│  └────────────┴────────────┴────────────┴─────────────┘ │
├──────────────────────────────────────────────────────────┤
│                    Output Manager                         │
│         (Save, Export, Format Conversion)                 │
└──────────────────────────────────────────────────────────┘
```

### C. Technical Requirements

| Component | Requirement |
|-----------|-------------|
| Language | Python 3.8+ |
| Framework | OpenCV, NumPy, Pillow |
| UI | Tkinter/PyQt atau Web (Flask) |
| ML (optional) | TensorFlow/PyTorch untuk depth |
| Format Support | JPEG, PNG, TIFF, RAW (bonus) |

---

## 📊 FASE PENGERJAAN

### Fase 1: Foundation (Minggu 1)
**Deliverable**: Basic enhancement pipeline

Tasks:
- [ ] Setup project structure
- [ ] Implement image loading/saving
- [ ] Basic exposure adjustment
- [ ] Contrast dan brightness control
- [ ] Simple UI untuk testing

### Fase 2: Core Features (Minggu 2)
**Deliverable**: Full enhancement suite

Tasks:
- [ ] Denoising implementation (multiple methods)
- [ ] Color correction (white balance, saturation)
- [ ] Sharpening dengan control
- [ ] Auto-enhancement logic
- [ ] Quality metrics (PSNR, SSIM)

### Fase 3: Advanced Features (Minggu 3)
**Deliverable**: HDR dan Portrait mode

Tasks:
- [ ] HDR/Exposure fusion
- [ ] Tone mapping options
- [ ] Portrait mode dengan depth
- [ ] Edge-aware processing
- [ ] Preset system

### Fase 4: Polish & Integration (Minggu 4)
**Deliverable**: Complete application

Tasks:
- [ ] Complete UI
- [ ] Batch processing
- [ ] Performance optimization
- [ ] Testing dan debugging
- [ ] Documentation

---

## 💻 PSEUDOCODE

### Auto Enhancement

```python
def auto_enhance(image):
    # Analyze image
    analysis = analyze_image(image)
    
    # Build enhancement chain
    enhanced = image.copy()
    
    # Fix exposure
    if analysis.is_underexposed:
        enhanced = boost_exposure(enhanced, analysis.exposure_correction)
    elif analysis.is_overexposed:
        enhanced = reduce_exposure(enhanced, analysis.exposure_correction)
    
    # Fix contrast
    if analysis.is_low_contrast:
        enhanced = apply_clahe(enhanced)
    
    # Reduce noise
    if analysis.noise_level > threshold:
        enhanced = denoise(enhanced, strength=analysis.noise_level)
    
    # Color correction
    if analysis.color_cast_detected:
        enhanced = auto_white_balance(enhanced)
    
    # Subtle sharpening
    enhanced = sharpen(enhanced, amount=0.3)
    
    return enhanced

def analyze_image(image):
    analysis = ImageAnalysis()
    
    # Histogram analysis
    hist = cv2.calcHist([image], [0], None, [256], [0,256])
    analysis.mean_brightness = np.mean(image)
    analysis.contrast = np.std(image)
    
    # Noise estimation (Laplacian variance method)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    analysis.noise_level = estimate_noise(gray)
    
    # Color cast detection
    analysis.color_cast = detect_color_cast(image)
    
    return analysis
```

### HDR Processing

```python
def create_hdr(exposures, exposure_times):
    # Align images
    aligned = align_images(exposures)
    
    # Option 1: Debevec HDR
    merge_debevec = cv2.createMergeDebevec()
    hdr = merge_debevec.process(aligned, exposure_times)
    
    # Tone mapping
    tonemap = cv2.createTonemap(gamma=2.2)
    ldr = tonemap.process(hdr)
    
    # Option 2: Mertens fusion (no HDR intermediate)
    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(aligned)
    
    return ldr, fusion
```

### Portrait Mode

```python
def portrait_mode(image, depth_map=None, blur_strength=1.0):
    if depth_map is None:
        # Estimate depth (placeholder for neural network)
        depth_map = estimate_depth(image)
    
    # Normalize depth
    depth_normalized = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX)
    
    # Create blur map (blur increases with depth)
    blur_map = depth_normalized * blur_strength * 30  # max 30 pixel blur
    
    # Apply variable blur
    output = np.zeros_like(image, dtype=np.float32)
    
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            blur_radius = int(blur_map[y, x])
            if blur_radius > 0:
                # Apply local blur (simplified)
                kernel_size = blur_radius * 2 + 1
                output[y, x] = local_blur(image, x, y, kernel_size)
            else:
                output[y, x] = image[y, x]
    
    return output.astype(np.uint8)
```

---

## 🏆 KRITERIA PENILAIAN

### Breakdown Nilai

| Komponen | Bobot | Detail |
|----------|-------|--------|
| Core Enhancement | 25% | Exposure, contrast, color, sharpening |
| Denoising Quality | 20% | PSNR improvement, detail preservation |
| HDR/Fusion | 15% | Proper implementation, tone mapping |
| Portrait Mode | 15% | Depth estimation, blur quality |
| UI/UX | 10% | Usability, design |
| Code Quality | 10% | Structure, documentation |
| Performance | 5% | Processing speed |

### Grading Scale

| Grade | Score | Criteria |
|-------|-------|----------|
| A | 85-100 | All features excellent, bonus features |
| B | 70-84 | All features good, minor issues |
| C | 55-69 | Core features work, some issues |
| D | 40-54 | Basic functionality only |
| E | <40 | Incomplete or non-functional |

---

## 🌟 BONUS FEATURES (+5% each, max 15%)

1. **RAW Processing**: Support for camera RAW files
2. **AI Enhancement**: Neural network-based enhancement
3. **Real-time Preview**: Live preview of adjustments
4. **Compare Mode**: Before/after slider comparison
5. **Cloud Integration**: Save/load from cloud storage

---

## 📝 DELIVERABLES

### Minggu ke-4 (Final Submission)

1. **Source Code**
   - Complete Python project
   - Requirements.txt
   - README dengan installation instructions

2. **Documentation**
   - Technical documentation (algorithm explanations)
   - User manual
   - API reference (if applicable)

3. **Demo**
   - Video demo (3-5 menit)
   - Sample results dengan before/after

4. **Report**
   - Implementation details
   - Challenges dan solutions
   - Future improvements

---

## 💡 TIPS PENGERJAAN

1. **Start Simple**: Get basic pipeline working first
2. **Test Incrementally**: Test each module separately
3. **Use Existing Libraries**: OpenCV has many built-in functions
4. **Optimize Later**: Get it working, then make it fast
5. **Document As You Go**: Don't leave documentation to the end

---

## 📚 RESOURCES

### Libraries:
- OpenCV: Main image processing
- scikit-image: Additional algorithms
- rawpy: RAW file handling
- Pillow: Format conversion

### References:
- OpenCV Computational Photography Tutorial
- Google Research - Night Sight Paper
- Adobe Research - Photography Enhancement

### Sample Datasets:
- HDR Image Database (Mark Fairchild)
- SIDD Dataset (noise)
- DIV2K (super resolution)
