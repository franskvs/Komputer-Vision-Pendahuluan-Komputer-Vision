# JOBSHEET PRAKTIKUM
## BAB 10: COMPUTATIONAL PHOTOGRAPHY

---

## INFORMASI PRAKTIKUM

| Item | Keterangan |
|------|------------|
| Mata Kuliah | Praktikum Computer Vision |
| Bab | 10 - Computational Photography |
| Durasi | 2 x 110 menit |
| Metode | Hands-on + Eksperimen |

---

## A. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa mampu:
1. Memahami konsep High Dynamic Range (HDR) imaging
2. Mengimplementasikan exposure fusion dengan berbagai metode
3. Menerapkan teknik image denoising
4. Membuat synthetic bokeh (depth-based blur)
5. Memahami super resolution dan image enhancement
6. Mengembangkan aplikasi computational photography praktis

---

## B. ALAT DAN BAHAN

### Software:
- Python 3.8+
- OpenCV 4.5+
- NumPy
- Matplotlib

### Hardware:
- Komputer dengan minimum 4GB RAM
- Kamera digital/smartphone (untuk capture gambar)
- GPU (opsional, untuk deep learning methods)

### Data:
- Multi-exposure image sets
- Noisy images untuk denoising
- Portrait images dengan depth
- Low-resolution images

---

## C. DASAR TEORI

### C.1 Computational Photography

Computational photography menggabungkan teknik komputasi dengan capture hardware untuk menghasilkan gambar yang melampaui kemampuan kamera konvensional.

### C.2 Key Concepts

| Konsep | Deskripsi | Aplikasi |
|--------|-----------|----------|
| HDR | Extended dynamic range | Landscape, architecture |
| Denoising | Noise reduction | Low-light, astrophotography |
| Bokeh | Depth-based blur | Portrait mode |
| Super Resolution | Resolution enhancement | Zoom, enhancement |
| Exposure Fusion | Multi-exposure blending | HDR alternative |

---

## D. EKSPERIMEN

### EKSPERIMEN 1: HDR IMAGING
**File: `01_hdr_imaging.py`**

**Tujuan**: Memahami proses pembuatan dan tone mapping HDR

**Langkah**:
1. Load multiple exposure images
2. Align images jika diperlukan
3. Merge ke HDR menggunakan Debevec method
4. Apply berbagai tone mapping operators
5. Compare hasil

**Parameter yang Dimodifikasi**:
| Parameter | Range | Efek |
|-----------|-------|------|
| Gamma | 1.0-3.0 | Brightness adjustment |
| Saturation | 0.5-2.0 | Color intensity |
| Contrast | 0.0-2.0 | Dynamic range compression |

**Pertanyaan**:
1. Mengapa perlu multiple exposures?
2. Apa perbedaan tone mapping operators?
3. Bagaimana mengatasi ghosting pada HDR?

---

### EKSPERIMEN 2: EXPOSURE FUSION
**File: `02_exposure_fusion.py`**

**Tujuan**: Mengimplementasikan Mertens fusion tanpa HDR intermediate

**Langkah**:
1. Load bracket exposures
2. Compute quality measures (contrast, saturation, well-exposedness)
3. Calculate weight maps
4. Laplacian pyramid blending
5. Compare dengan HDR tone mapping

**Parameter yang Dimodifikasi**:
| Parameter | Range | Efek |
|-----------|-------|------|
| contrast_weight | 0.0-1.0 | Emphasis pada local contrast |
| saturation_weight | 0.0-1.0 | Emphasis pada color saturation |
| exposure_weight | 0.0-1.0 | Emphasis pada proper exposure |

**Pertanyaan**:
1. Kapan exposure fusion lebih baik dari HDR?
2. Bagaimana weight maps mempengaruhi hasil?
3. Apa keuntungan pyramid blending?

---

### EKSPERIMEN 3: IMAGE DENOISING
**File: `03_denoising.py`**

**Tujuan**: Membandingkan berbagai metode denoising

**Metode yang Diimplementasikan**:
1. Gaussian blur
2. Bilateral filter
3. Non-local means
4. Morphological operations

**Langkah**:
1. Add synthetic noise ke clean image
2. Apply berbagai denoising methods
3. Calculate metrics (PSNR, SSIM)
4. Visual comparison

**Metrics**:
| Metric | Formula | Interpretasi |
|--------|---------|--------------|
| PSNR | $10 \log_{10}(\frac{MAX^2}{MSE})$ | Higher = better |
| SSIM | Structural similarity | 1.0 = identical |

**Pertanyaan**:
1. Apa trade-off noise reduction vs detail preservation?
2. Mengapa non-local means lebih baik untuk textures?
3. Bagaimana parameter strength mempengaruhi hasil?

---

### EKSPERIMEN 4: SYNTHETIC BOKEH
**File: `04_synthetic_bokeh.py`**

**Tujuan**: Membuat efek bokeh seperti smartphone portrait mode

**Langkah**:
1. Load image dan depth map (atau estimate)
2. Define focus distance
3. Calculate blur amount berdasarkan depth
4. Apply depth-dependent blur
5. Blend dengan original

**Parameter yang Dimodifikasi**:
| Parameter | Range | Efek |
|-----------|-------|------|
| focal_distance | 0.0-1.0 | Focus depth |
| aperture | 1.4-16.0 | Blur strength |
| blur_type | gaussian/disk | Bokeh shape |

**Pertanyaan**:
1. Bagaimana depth estimation bekerja?
2. Mengapa hasilnya berbeda dari optical bokeh?
3. Bagaimana mengatasi edge artifacts?

---

### EKSPERIMEN 5: IMAGE ENHANCEMENT
**File: `05_image_enhancement.py`**

**Tujuan**: Meningkatkan kualitas gambar dengan berbagai teknik

**Teknik yang Diimplementasikan**:
1. Contrast enhancement (CLAHE)
2. Color correction (white balance)
3. Sharpening
4. Auto-levels

**Langkah**:
1. Analyze image statistics
2. Apply enhancement techniques
3. Preserve natural look
4. Before/after comparison

**Pertanyaan**:
1. Kapan CLAHE lebih baik dari histogram equalization?
2. Bagaimana auto white balance bekerja?
3. Apa risiko over-sharpening?

---

### EKSPERIMEN 6: MULTI-FRAME ENHANCEMENT
**File: `06_multi_frame_enhancement.py`**

**Tujuan**: Menggabungkan multiple frames untuk quality improvement

**Teknik**:
1. Multi-frame averaging untuk noise reduction
2. Alignment untuk burst images
3. Best frame selection

**Langkah**:
1. Capture/load burst images
2. Align frames (handle motion)
3. Weighted averaging
4. Compare dengan single frame

**Parameter**:
| Parameter | Range | Efek |
|-----------|-------|------|
| num_frames | 2-16 | Noise reduction amount |
| alignment_method | ECC/feature | Registration accuracy |
| weight_type | uniform/quality | Frame contribution |

**Pertanyaan**:
1. Mengapa SNR meningkat dengan lebih banyak frames?
2. Bagaimana handling moving objects?
3. Berapa optimal number of frames?

---

## E. TUGAS PRAKTIKUM

### Tugas 1: HDR Photography (30%)
Ambil 3+ exposure images dari scene high dynamic range dan buat HDR composite. Document proses dan hasil.

### Tugas 2: Algorithm Comparison (30%)
Bandingkan minimal 3 denoising methods pada berbagai noise levels. Present quantitative metrics dan qualitative analysis.

### Tugas 3: Enhancement Pipeline (40%)
Buat complete image enhancement pipeline yang dapat:
- Auto-detect dan correct exposure
- Reduce noise while preserving detail
- Enhance colors and contrast
- Save optimized output

---

## F. RUBRIK PENILAIAN

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| Eksperimen | 40% | Completion, understanding |
| Tugas | 40% | Quality, creativity |
| Laporan | 20% | Documentation, analysis |

---

## G. REFERENSI

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Ed. Chapter 10.
2. OpenCV Documentation - Computational Photography
3. Reinhard et al. (2010). High Dynamic Range Imaging.
