# BAB 2: PEMBENTUKAN CITRA - PRAKTIKUM
## Computer Vision - Image Formation

### 📋 RINGKASAN

Praktikum ini mencakup **15 program** yang mendemonstrasikan konsep-konsep fundamental dalam pembentukan citra, mulai dari transformasi geometri hingga fotometri.

**Status:** ✅ **SEMUA PROGRAM TERVERIFIKASI & BERFUNGSI**
- **15/15 programs** berjalan dengan sukses
- **22 output files** telah di-generate
- **Execution time:** ~23 detik total

---

### 🎯 STRUKTUR PRAKTIKUM

#### 1. **Transformasi Geometri** (Programs 01-06)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 01 | Translasi | Pergeseran 2D | Stabilisasi video, image alignment |
| 02 | Rotasi | Rotation matrix | Photo straightening, AR |
| 03 | Scaling | Interpolasi | Thumbnail generation, zoom |
| 04 | Affine Transform | Kombinasi transformasi | Photo warping, face alignment |
| 05 | Perspektif Transform | Koreksi perspektif | Document scanning, KTP reader |
| 06 | Document Scanner | Auto-detection | Mobile scanner apps (CamScanner) |

#### 2. **Kalibrasi & Proyeksi** (Programs 07-10)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 07 | Kalibrasi Kamera | Intrinsic parameters | Self-driving cars, robotics |
| 08 | 3D Rotation | Rodrigues formula | 3D graphics, AR/VR |
| 09 | Projection | Ortografik vs perspektif | CAD software, game engines |
| 10 | Lens Distortion | Radial distortion | GoPro correction, wide-angle lens |

#### 3. **Sampling & Color** (Programs 11-12)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 11 | Sampling & Aliasing | Nyquist theorem | Display technology, downsampling |
| 12 | Color Spaces | RGB, HSV, LAB | Photo editing, color grading |

#### 4. **Fotometri** (Programs 13-15)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 13 | Gamma Correction | Gamma encode/decode | Display calibration, HDR |
| 14 | Photometric Shading | Lambertian + Phong | 3D rendering, game graphics |
| 15 | Compression Artifacts | JPEG quality | Image optimization, web publishing |

---

### 🚀 CARA MENJALANKAN

#### Setup Awal (Hanya Sekali)
```bash
# 1. Generate semua gambar untuk praktikum
python3 setup_images.py

# Output: 10 gambar berkualitas tinggi di folder data/images/
```

#### Menjalankan Program Individual
```bash
# Contoh: Jalankan program translasi
python3 01_translasi.py

# Output akan tersimpan di: output/output1/
```

#### Automated Testing (Semua Program Sekaligus)
```bash
# Test semua 15 program secara otomatis
python3 run_all_tests.py

# Output: 
# - Verification report
# - Execution statistics
# - Error detection (jika ada)
```

---

### 📁 STRUKTUR DIREKTORI

```
Bab-02-Pembentukan-Citra/praktikum/
│
├── data/
│   └── images/               # 10 gambar praktikum
│       ├── portrait.jpg      # Face untuk transformasi
│       ├── document.jpg      # Dokumen untuk scanning
│       ├── building.jpg      # Perspektif correction
│       ├── coins.jpg         # Object detection
│       └── ... (6 more)
│
├── output/
│   ├── output1/             # Hasil translasi
│   ├── output2/             # Hasil rotasi
│   ├── ... (15 folders)
│   └── output15/            # Hasil compression
│
├── 01_translasi.py          # Program 1
├── 02_rotasi.py             # Program 2
├── ... (13 more)
├── 15_compression_artifacts.py
│
├── setup_images.py          # Image generator
├── run_all_tests.py         # Automated testing
└── VERIFICATION_REPORT.txt  # Test results
```

---

### 🖼️ GAMBAR YANG DIGUNAKAN

Semua gambar adalah **synthetic/generated** untuk menghindari masalah copyright:

1. **portrait.jpg** (512×512) - Synthetic face dengan detail realistis
2. **cameraman.jpg** (256×256) - High-frequency content untuk aliasing demo
3. **peppers.jpg** (512×512) - Vibrant colors untuk color space
4. **checkerboard.png** (512×512) - Camera calibration pattern
5. **building.jpg** (400×500) - Facade dengan perspektif
6. **document.jpg** (600×800) - Receipt/struk untuk scanner
7. **baboon.jpg** (512×512) - Complex texture untuk shading
8. **coins.jpg** (300×400) - Metallic objects dengan 3D effect
9. **grid.jpg** (400×400) - Perspective grid pattern
10. **rainbow.jpg** (512×512) - Color spectrum gradient

---

### 💡 TIPS & BEST PRACTICES

#### Untuk Mahasiswa:
1. **Jalankan program satu per satu** untuk memahami konsep
2. **Lihat output images** di folder output/
3. **Baca komentar di kode** untuk penjelasan detail
4. **Eksperimen dengan parameter** yang disediakan
5. **Coba dengan gambar sendiri** untuk aplikasi nyata

#### Untuk Dosen/Asisten:
1. **Run `run_all_tests.py`** sebelum praktikum untuk verifikasi
2. **Check VERIFICATION_REPORT.txt** untuk memastikan semua OK
3. **Gunakan automated versions** (05_auto, 06_auto) untuk demo
4. **Semua program non-interactive** - tidak perlu window management

---

### 🔧 TROUBLESHOOTING

#### Problem: Images tidak ditemukan
**Solution:**
```bash
python3 setup_images.py
```

#### Problem: Output kosong
**Solution:** Check apakah folder output/ memiliki permission write

#### Problem: Import error (cv2, matplotlib, numpy)
**Solution:**
```bash
pip install opencv-python matplotlib numpy
```

---

### 📊 VERIFICATION REPORT

**Last Run:** 2026-02-05 07:13:56

```
Total Programs: 15
Passed: 15/15 ✅
Failed: 0/15
Output Files: 22
Total Time: 23.09s
Average: 1.54s per program
```

---

### 🎓 KONSEP YANG DIPELAJARI

#### Transformasi Geometri
- [x] Translation matrix (2×3)
- [x] Rotation matrix dengan cv2.getRotationMatrix2D()
- [x] Scaling & interpolation methods
- [x] Affine transform (3 point mapping)
- [x] Perspective transform (4 point mapping)
- [x] Homography matrix (3×3)

#### Computer Vision Pipeline
- [x] Edge detection (Canny)
- [x] Contour detection & filtering
- [x] Adaptive thresholding
- [x] Camera calibration dengan checkerboard
- [x] Lens distortion correction

#### Representasi Warna & Intensitas
- [x] Color space conversions (RGB↔HSV↔LAB)
- [x] Gamma correction
- [x] Photometric models (Lambertian, Phong)
- [x] Image compression artifacts

#### Sampling & Projection
- [x] Nyquist theorem & aliasing
- [x] Anti-aliasing techniques
- [x] Orthographic vs perspective projection
- [x] 3D rotation (Rodrigues formula)

---

### 🌟 REAL-WORLD APPLICATIONS

**Mobile Apps:**
- CamScanner, Adobe Scan (Programs 05-06)
- Instagram filters (Programs 01-04)
- Face AR filters (Programs 02, 08)

**Automotive:**
- Self-driving car cameras (Program 07)
- Parking assistance (Program 10)
- Lane detection (Program 05)

**Industry:**
- Quality control (Program 11)
- Document digitization (Programs 05-06)
- 3D scanning (Programs 08-09)

**Media & Entertainment:**
- Video stabilization (Program 01)
- HDR photography (Program 13)
- Game rendering (Program 14)

---

### 📞 SUPPORT

Jika menemukan bug atau ada pertanyaan:
1. Check VERIFICATION_REPORT.txt untuk error details
2. Review comments di source code
3. Run individual program untuk debugging

---

### 📄 LICENSE

Semua gambar: **Public Domain / Generated**
Code: Educational use

**No copyrighted material used** ✅

---

**Created:** February 2026  
**Status:** Production Ready ✅  
**Tested:** All 15 programs verified
