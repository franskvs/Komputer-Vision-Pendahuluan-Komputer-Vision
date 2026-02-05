# Rubrik Penilaian Project: AutoStitch - Sistem Panorama Otomatis
## Bab 4: Model Fitting dan Feature Matching

### Informasi Umum
- **Total Nilai**: 100 poin
- **Passing Grade**: 70 poin
- **Waktu Pengerjaan**: 3 minggu

---

## A. Kriteria Penilaian Utama

### 1. Feature Detection & Extraction (20 poin)

| Nilai | Kriteria |
|-------|----------|
| 18-20 | Implementasi multiple detectors (ORB, SIFT, AKAZE) dengan pemilihan adaptif berdasarkan karakteristik gambar. Parameter teroptimasi untuk berbagai kondisi. Dokumentasi lengkap. |
| 15-17 | Implementasi 2-3 detectors dengan performa bagus. Parameter dapat dikonfigurasi. Error handling baik. |
| 12-14 | Implementasi 1-2 detectors dengan performa standar. Dapat mendeteksi features di berbagai kondisi. |
| 8-11 | Implementasi basic detector. Hanya bekerja untuk kondisi tertentu. |
| 0-7 | Detector tidak berfungsi atau sangat terbatas. |

**Checklist:**
- [ ] Implementasi minimal 2 feature detectors
- [ ] Keypoint visualization yang informatif
- [ ] Parameter yang dapat dikonfigurasi
- [ ] Handling untuk low-texture regions
- [ ] Descriptor computation yang efisien

### 2. Feature Matching (20 poin)

| Nilai | Kriteria |
|-------|----------|
| 18-20 | Implementasi BF dan FLANN matcher dengan pemilihan otomatis. Ratio test dan cross-check. Match filtering yang sophisticated. |
| 15-17 | Implementasi matcher yang baik dengan ratio test. Good match filtering. Performance yang baik. |
| 12-14 | Implementasi matcher standar. Ratio test basic. Hasil matching cukup reliable. |
| 8-11 | Matcher basic tanpa filtering yang baik. Banyak false matches. |
| 0-7 | Matcher tidak berfungsi atau hasil sangat buruk. |

**Checklist:**
- [ ] Implementasi Brute-Force matcher
- [ ] Implementasi FLANN matcher
- [ ] Lowe's ratio test
- [ ] Match visualization
- [ ] Statistik matching (inlier ratio, etc.)

### 3. Homography Estimation dengan RANSAC (20 poin)

| Nilai | Kriteria |
|-------|----------|
| 18-20 | RANSAC implementation yang robust. Parameter adaptif. Confidence estimation. Outlier analysis. Multiple model support. |
| 15-17 | RANSAC yang baik dengan parameter yang dapat disesuaikan. Inlier/outlier reporting yang jelas. |
| 12-14 | RANSAC standar yang berfungsi. Homography estimation reliable untuk kebanyakan kasus. |
| 8-11 | RANSAC basic. Bekerja hanya untuk kasus ideal. |
| 0-7 | RANSAC tidak berfungsi atau sangat tidak reliable. |

**Checklist:**
- [ ] Homography estimation dengan cv2.findHomography
- [ ] RANSAC threshold yang dapat dikonfigurasi
- [ ] Inlier mask analysis
- [ ] Homography matrix validation
- [ ] Error reporting untuk failed estimations

### 4. Image Warping & Blending (20 poin)

| Nilai | Kriteria |
|-------|----------|
| 18-20 | Warping yang smooth tanpa distorsi. Multi-band blending atau feathering yang excellent. Seam handling yang sophisticated. Output canvas calculation yang optimal. |
| 15-17 | Warping yang baik. Alpha blending atau feathering yang smooth. Seam visibility minimal. |
| 12-14 | Warping basic yang berfungsi. Simple blending dengan seam yang visible tapi acceptable. |
| 8-11 | Warping dengan distorsi noticeable. Blending kasar dengan seam yang obvious. |
| 0-7 | Warping gagal atau blending sangat buruk. |

**Checklist:**
- [ ] cv2.warpPerspective implementation
- [ ] Correct output canvas size calculation
- [ ] Basic alpha blending
- [ ] Feathering atau gradient blending
- [ ] Seam minimization attempt

### 5. Complete Pipeline & Integration (10 poin)

| Nilai | Kriteria |
|-------|----------|
| 9-10 | Pipeline yang seamless dari input ke output. Modular design. Easy to use API. Support untuk batch processing. |
| 7-8 | Pipeline yang berfungsi dengan baik. Cukup modular. Good error handling. |
| 5-6 | Pipeline basic yang berfungsi. Some integration issues. |
| 3-4 | Pipeline dengan banyak issues. Manual intervention required. |
| 0-2 | Pipeline tidak berfungsi end-to-end. |

**Checklist:**
- [ ] Single function call untuk panorama creation
- [ ] Support untuk 2+ image stitching
- [ ] Progress reporting
- [ ] Error handling dengan informative messages
- [ ] Output saving dengan quality options

### 6. Dokumentasi & Code Quality (10 poin)

| Nilai | Kriteria |
|-------|----------|
| 9-10 | Dokumentasi lengkap (README, docstrings, inline comments). Code clean dan well-organized. Type hints. Unit tests. |
| 7-8 | Dokumentasi baik. Code readable. Some comments. |
| 5-6 | Dokumentasi basic. Code cukup organized. |
| 3-4 | Dokumentasi minimal. Code sulit dibaca. |
| 0-2 | Tidak ada dokumentasi. Code tidak organized. |

**Checklist:**
- [ ] README.md dengan instructions lengkap
- [ ] Docstrings untuk semua functions
- [ ] Inline comments untuk complex logic
- [ ] Consistent code style
- [ ] Example usage

---

## B. Bonus Points (Maksimal +15 poin)

| Bonus | Poin | Deskripsi |
|-------|------|-----------|
| GPU Acceleration | +5 | CUDA implementation atau OpenCL |
| Exposure Compensation | +3 | Automatic exposure matching antar images |
| Multi-row Panorama | +4 | Support untuk panorama 2D (horizontal + vertical) |
| Real-time Preview | +3 | Live preview saat processing |
| Mobile Optimization | +3 | Optimized untuk low-memory devices |

---

## C. Penalti

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Late submission (per hari) | -5 poin |
| Plagiarism | -50 poin atau nilai 0 |
| No source code | Nilai 0 |
| Cannot run/compile | -20 poin |
| Missing required features | -10 poin per feature |

---

## D. Rubrik Per Modul

### Modul 1: Feature Detector
| Komponen | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| Accuracy | >90% keypoints match ground truth | 70-90% | 50-70% | <50% |
| Speed | <100ms per image | 100-500ms | 500ms-1s | >1s |
| Robustness | Works across all conditions | Most conditions | Limited conditions | Very limited |

### Modul 2: Feature Matcher
| Komponen | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Precision | >95% correct matches | 85-95% | 70-85% | <70% |
| Recall | >80% true matches found | 60-80% | 40-60% | <40% |
| Speed | <200ms | 200-500ms | 500ms-1s | >1s |

### Modul 3: Homography Estimator
| Komponen | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Accuracy | Reprojection error <1px | 1-3px | 3-5px | >5px |
| Robustness | Works with 50%+ outliers | 30-50% | 10-30% | <10% |
| Consistency | Same result 95%+ | 85-95% | 70-85% | <70% |

### Modul 4: Image Warper
| Komponen | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Quality | No visible artifacts | Minor artifacts | Noticeable artifacts | Severe artifacts |
| Alignment | <1px misalignment | 1-3px | 3-5px | >5px |

### Modul 5: Image Blender
| Komponen | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Seam Visibility | Invisible | Barely visible | Noticeable | Very obvious |
| Color Consistency | Perfect match | Minor differences | Noticeable differences | Severe mismatch |

### Modul 6: Panorama Pipeline
| Komponen | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| Success Rate | >95% panoramas succeed | 85-95% | 70-85% | <70% |
| Processing Time | <5s for 3 images | 5-15s | 15-30s | >30s |
| Output Quality | Professional grade | Good quality | Acceptable | Poor quality |

---

## E. Contoh Penilaian

### Contoh: Nilai A (92 poin)
```
Feature Detection:     18/20 (Multiple detectors, optimized)
Feature Matching:      17/20 (Good filtering, FLANN + BF)
Homography:           18/20 (Robust RANSAC, good analysis)
Warping & Blending:   17/20 (Smooth blending, minor seams)
Pipeline:              9/10 (Clean API, batch support)
Documentation:         8/10 (Good docs, missing unit tests)
Bonus:                +5 (Exposure compensation)
Total:                92/100 + 5 bonus = 97
```

### Contoh: Nilai B (78 poin)
```
Feature Detection:     15/20 (Working detectors)
Feature Matching:      14/20 (Basic ratio test)
Homography:           15/20 (Working RANSAC)
Warping & Blending:   14/20 (Basic blending, visible seams)
Pipeline:              7/10 (Works but not polished)
Documentation:         8/10 (Good documentation)
Total:                73/100
```

---

## F. Submission Requirements

### Wajib Ada:
1. Source code (Python files)
2. README.md dengan:
   - Installation instructions
   - Usage examples
   - Sample output screenshots
3. Requirements.txt
4. Minimal 3 sample panorama results
5. Brief report (1-2 pages) explaining approach

### Format Submission:
```
NIM_Nama_Project_Bab4/
├── README.md
├── requirements.txt
├── src/
│   ├── feature_detector.py
│   ├── feature_matcher.py
│   ├── homography_estimator.py
│   ├── image_warper.py
│   ├── image_blender.py
│   └── panorama_pipeline.py
├── examples/
│   ├── demo.py
│   └── sample_images/
├── output/
│   └── sample_panoramas/
└── docs/
    └── report.pdf
```

---

## G. Timeline Pengerjaan

| Minggu | Target | Deliverable |
|--------|--------|-------------|
| 1 | Feature Detection & Matching | Modul 1-2 working |
| 2 | Homography & Warping | Modul 3-4 integrated |
| 3 | Blending & Pipeline | Complete system + documentation |

---

## H. Catatan Penting

1. **Originalitas**: Code harus original, boleh reference tapi harus paham dan bisa jelaskan
2. **Testing**: Test dengan berbagai image conditions (indoor, outdoor, low-light)
3. **Edge Cases**: Handle cases seperti no matches found, degenerate homography
4. **Performance**: Optimize untuk reasonable processing time
5. **User Experience**: Provide clear feedback dan error messages
