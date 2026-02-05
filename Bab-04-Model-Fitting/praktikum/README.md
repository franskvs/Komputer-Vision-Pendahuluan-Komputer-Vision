# BAB 4: MODEL FITTING - PRAKTIKUM
## Computer Vision - Feature Detection & Model Fitting

### 📋 RINGKASAN

Praktikum ini mencakup **11 program** yang mendemonstrasikan teknik feature detection, matching, dan model fitting.

**Status:** ✅ **PROGRAM TERVERIFIKASI**
- **11 programs** untuk pembelajaran model fitting
- Output tersimpan di folder `output/`

---

### 🎯 STRUKTUR PRAKTIKUM

#### 1. **Feature Detection** (Programs 01-02)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 01 | Feature Detection | Harris, ORB, SIFT, AKAZE | Keypoint detection |
| 02 | Feature Matching | Brute-force, FLANN | Image matching |

#### 2. **Robust Estimation** (Program 03)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 03 | RANSAC | Random Sample Consensus | Outlier rejection |

#### 3. **Hough Transform** (Programs 04-05)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 04 | Hough Lines | Line detection | Lane detection |
| 05 | Hough Circles | Circle detection | Coin detection |

#### 4. **Geometric Estimation** (Programs 06-08)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 06 | Homography | Planar transformation | Image stitching |
| 07 | Perspective Correction | View correction | Document scanner |
| 08 | Optical Flow | Motion estimation | Video tracking |

#### 5. **Advanced Fitting** (Programs 09-11)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 09 | Scattered Interpolation (RBF) | Radial basis function | Surface fitting |
| 10 | Variational Regularization | Denoising | Image restoration |
| 11 | MRF Denoising (ICM) | Markov Random Field | Smoothing |

---

### 🚀 CARA MENJALANKAN

#### Setup Awal (Hanya Sekali)
```bash
# 1. Generate semua gambar untuk praktikum
python3 setup_images.py

# Output: Gambar di folder data/images/
```

#### Menjalankan Program Individual
```bash
# Contoh: Jalankan program feature detection
python3 01_feature_detection.py

# Output akan tersimpan di: output/output1/
```

#### Automated Testing (Semua Program Sekaligus)
```bash
# Test semua program secara otomatis
python3 run_all_tests.py

# Output: 
# - Verification report
# - Execution statistics
```

---

### 📁 STRUKTUR DIREKTORI

```
Bab-04-Model-Fitting/praktikum/
│
├── data/
│   └── images/               # Gambar praktikum
│       ├── portrait.jpg      # Feature detection
│       ├── building.jpg      # Line detection
│       ├── coins.jpg         # Circle detection
│       └── ...
│
├── output/
│   ├── output1/             # Hasil feature detection
│   ├── output2/             # Hasil feature matching
│   └── ... (11 folders)
│
├── 01_feature_detection.py
├── 02_feature_matching.py
├── ... (11 programs)
│
├── CV2_FUNCTIONS_REFERENCE.py  # Referensi fungsi OpenCV
├── setup_images.py             # Setup gambar
├── run_all_tests.py            # Test runner
├── README.md                   # Dokumentasi ini
└── QUICKSTART.md               # Panduan cepat
```

---

### 📚 KONSEP YANG DIPELAJARI

1. **Feature Detectors** - Harris, ORB, SIFT, AKAZE, FAST
2. **Feature Descriptors** - Binary, floating-point
3. **Feature Matching** - Brute-force, FLANN
4. **RANSAC** - Robust estimation
5. **Hough Transform** - Line, circle detection
6. **Homography** - Perspective transformation
7. **Optical Flow** - Lucas-Kanade, Farneback
8. **Interpolation** - RBF, scattered data
9. **Regularization** - Variational methods
10. **MRF** - Markov Random Fields

---

### 🔧 TROUBLESHOOTING

**Q: Gambar tidak ditemukan?**
```bash
python3 setup_images.py
```

**Q: Error "No module named cv2"?**
```bash
pip install opencv-python opencv-contrib-python numpy matplotlib scipy
```

**Q: SIFT tidak tersedia?**
```bash
pip install opencv-contrib-python
```

---

### 📖 REFERENSI

- [OpenCV Feature Detection](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)
- [Szeliski Book - Chapter 4](http://szeliski.org/Book/)
- File: `CV2_FUNCTIONS_REFERENCE.py` - Dokumentasi fungsi lengkap
