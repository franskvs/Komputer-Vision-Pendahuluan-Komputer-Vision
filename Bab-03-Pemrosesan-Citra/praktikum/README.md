# BAB 3: PEMROSESAN CITRA - PRAKTIKUM
## Computer Vision - Image Processing

### 📋 RINGKASAN

Praktikum ini mencakup **16 program** yang mendemonstrasikan teknik-teknik pemrosesan citra, mulai dari operasi dasar hingga teknik lanjutan.

**Status:** ✅ **PROGRAM TERVERIFIKASI**
- **16 programs** untuk pembelajaran image processing
- Output tersimpan di folder `output/`

---

### 🎯 STRUKTUR PRAKTIKUM

#### 1. **Operasi Dasar** (Programs 01-04)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 01 | Brightness & Contrast | Point operations | Photo enhancement |
| 02 | Gamma Correction | Gamma encoding | Display calibration |
| 03 | Thresholding | Binarization | Document scanning |
| 04 | Histogram Equalization | Contrast enhancement | Medical imaging |

#### 2. **Filtering & Edge Detection** (Programs 05-07)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 05 | Spatial Filtering | Convolution, blur, sharpen | Noise reduction |
| 06 | Edge Detection | Sobel, Canny | Object detection |
| 07 | Morphological Operations | Erosion, dilation | Shape analysis |

#### 3. **Enhancement Pipeline** (Programs 08-09)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 08 | Enhancement Pipeline | Multi-stage processing | Photo editing apps |
| 09 | Compositing & Matting | Alpha blending | Video effects |

#### 4. **Frequency Domain** (Programs 10-11)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 10 | Fourier Transform | FFT, frequency filtering | Signal processing |
| 11 | Pyramids & Wavelets | Multi-resolution | Compression |

#### 5. **Advanced Techniques** (Programs 12-16)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 12 | Geometric Transformations | Warp, affine | AR/VR effects |
| 13 | Steerable Filters | Oriented filters | Feature extraction |
| 14 | Interpolation & Decimation | Resampling | Video scaling |
| 15 | Advanced Blending | Seamless cloning | Photo manipulation |
| 16 | Mesh Warping & Morphing | Face morphing | Animation |

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
# Contoh: Jalankan program brightness contrast
python3 01_brightness_contrast.py

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
Bab-03-Pemrosesan-Citra/praktikum/
│
├── data/
│   └── images/               # Gambar praktikum
│       ├── portrait.jpg      # Gambar wajah
│       ├── landscape.jpg     # Pemandangan
│       └── ...
│
├── output/
│   ├── output1/             # Hasil brightness/contrast
│   ├── output2/             # Hasil gamma correction
│   └── ... (16 folders)
│
├── 01_brightness_contrast.py
├── 02_gamma_correction.py
├── ... (16 programs)
│
├── CV2_FUNCTIONS_REFERENCE.py  # Referensi fungsi OpenCV
├── setup_images.py             # Setup gambar
├── run_all_tests.py            # Test runner
├── README.md                   # Dokumentasi ini
└── QUICKSTART.md               # Panduan cepat
```

---

### 📚 KONSEP YANG DIPELAJARI

1. **Point Operations** - Brightness, contrast, gamma
2. **Thresholding** - Binary, Otsu, adaptive
3. **Histogram** - Equalization, CLAHE
4. **Filtering** - Gaussian, median, bilateral
5. **Edge Detection** - Sobel, Laplacian, Canny
6. **Morphology** - Erosion, dilation, opening, closing
7. **Frequency Domain** - FFT, filtering
8. **Pyramids** - Gaussian, Laplacian
9. **Blending** - Seamless cloning, Poisson

---

### 🔧 TROUBLESHOOTING

**Q: Gambar tidak ditemukan?**
```bash
python3 setup_images.py
```

**Q: Error "No module named cv2"?**
```bash
pip install opencv-python numpy matplotlib
```

---

### 📖 REFERENSI

- [OpenCV Image Processing](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [Szeliski Book - Chapter 3](http://szeliski.org/Book/)
- File: `CV2_FUNCTIONS_REFERENCE.py` - Dokumentasi fungsi lengkap
