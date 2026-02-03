# Rubrik Penilaian Project - Bab 3
## PhotoFix AI - Sistem Peningkatan Kualitas Citra Otomatis

### Informasi Umum
- **Mata Kuliah:** Praktikum Computer Vision
- **Bab:** 3 - Pemrosesan Citra (Image Processing)
- **Bobot Project:** 40% dari nilai Bab 3
- **Sifat:** Kelompok (2-3 orang)
- **Durasi:** 2 minggu

---

## A. Komponen Penilaian

### 1. Image Analyzer Module (25 poin)

| Kriteria | Excellent (23-25) | Good (18-22) | Satisfactory (13-17) | Needs Improvement (0-12) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Brightness Analysis** | Analisis akurat dengan kategorisasi lengkap (dark/normal/bright) dan saran adjustment yang presisi | Analisis akurat dengan kategorisasi, saran kurang optimal | Analisis dasar, kategorisasi terbatas | Analisis tidak akurat atau tidak ada |
| **Contrast Analysis** | Analisis standar deviasi akurat, rekomendasi contrast factor sesuai | Analisis benar, rekomendasi kurang presisi | Analisis dasar tanpa rekomendasi | Tidak mengimplementasikan |
| **Noise Estimation** | Estimasi noise dengan metode yang valid, klasifikasi akurat | Estimasi noise dengan satu metode, klasifikasi benar | Deteksi noise sederhana | Tidak ada deteksi noise |
| **Color Balance** | Deteksi color cast dengan multiple methods, koreksi otomatis | Deteksi color cast dengan satu metode | Analisis warna dasar | Tidak ada analisis warna |

**Checklist Analyzer:**
- [ ] Fungsi `analyze_brightness()` dengan return assessment + suggested adjustment
- [ ] Fungsi `analyze_contrast()` dengan return std_dev + suggested factor
- [ ] Fungsi `analyze_noise()` dengan noise estimation
- [ ] Fungsi `analyze_color_balance()` dengan color cast detection
- [ ] Summary function yang menggabungkan semua analisis
- [ ] Unit tests untuk setiap fungsi analisis

---

### 2. Image Enhancer Module (35 poin)

| Kriteria | Excellent (32-35) | Good (25-31) | Satisfactory (18-24) | Needs Improvement (0-17) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Point Operations** | Implementasi brightness, contrast, gamma dengan parameter tunable | Implementasi 3 operasi dengan parameter standar | Implementasi 2 operasi | Implementasi minimal |
| **Histogram Operations** | CLAHE dengan parameter adaptif + histogram equalization | CLAHE dan equalization dengan parameter default | Salah satu metode | Tidak ada |
| **Spatial Filtering** | Multiple filters (denoise, sharpen) dengan strength control | Denoise dan sharpen dengan parameter fixed | Satu jenis filter | Tidak ada filter |
| **Color Correction** | White balance dengan multiple methods | White balance dengan satu metode | Color adjustment sederhana | Tidak ada |
| **Code Quality** | Clean, modular, well-documented, efficient | Modular dengan dokumentasi baik | Fungsional dengan beberapa dokumentasi | Code tidak terstruktur |

**Checklist Enhancer:**
- [ ] `adjust_brightness_contrast(img, brightness, contrast)`
- [ ] `gamma_correction(img, gamma)` dengan LUT optimization
- [ ] `clahe_enhancement(img, clip_limit, tile_size)`
- [ ] `denoise(img, strength)` dengan cv2.fastNlMeansDenoising
- [ ] `sharpen(img, strength)` dengan unsharp masking
- [ ] `adjust_saturation(img, factor)`
- [ ] `white_balance(img, method)` dengan minimal 2 metode
- [ ] Parameter validation untuk semua fungsi
- [ ] Optimasi performance (tidak lebih dari 2 detik per gambar HD)

---

### 3. Enhancement Pipeline (25 poin)

| Kriteria | Excellent (23-25) | Good (18-22) | Satisfactory (13-17) | Needs Improvement (0-12) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Auto Mode** | Pipeline otomatis berdasarkan analisis dengan hasil konsisten | Auto pipeline dengan hasil baik untuk kebanyakan kasus | Auto mode fungsional dengan hasil bervariasi | Auto mode tidak konsisten |
| **Manual Mode** | Semua parameter dapat di-tune dengan preview real-time | Parameter tunable dengan preview | Parameter tunable tanpa preview | Parameter tidak dapat diubah |
| **Presets** | Minimal 5 presets dengan karakteristik berbeda | 3-4 presets | 2 presets | Tidak ada preset |
| **Pipeline Order** | Urutan operasi optimal dan dapat dijelaskan | Urutan benar | Urutan sebagian benar | Urutan salah mempengaruhi hasil |

**Checklist Pipeline:**
- [ ] `enhancement_pipeline_auto(img)` dengan analisis terintegrasi
- [ ] `enhancement_pipeline_manual(img, params)` dengan semua parameter
- [ ] `enhancement_pipeline_preset(img, preset_name)`
- [ ] Minimal 5 presets: natural, vivid, dramatic, vintage, cinematic
- [ ] Urutan pipeline yang benar:
  1. Denoise
  2. White Balance
  3. CLAHE
  4. Brightness/Contrast
  5. Gamma
  6. Saturation
  7. Sharpening (terakhir!)
- [ ] Timing/performance metrics
- [ ] Before/after comparison visualization

---

### 4. Testing & Documentation (15 poin)

| Kriteria | Excellent (14-15) | Good (11-13) | Satisfactory (8-10) | Needs Improvement (0-7) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Test Coverage** | Unit tests untuk semua fungsi, integration tests, edge cases | Unit tests untuk fungsi utama, beberapa integration tests | Unit tests untuk sebagian fungsi | Minimal atau tidak ada tests |
| **Documentation** | Docstrings lengkap, README komprehensif, contoh penggunaan | Docstrings untuk fungsi utama, README | Dokumentasi parsial | Dokumentasi minimal |
| **Test Results** | Semua tests pass, test dengan berbagai jenis gambar | 90%+ tests pass | 75%+ tests pass | <75% tests pass |

**Checklist Testing & Documentation:**
- [ ] README.md dengan instruksi lengkap
- [ ] Docstrings untuk setiap fungsi
- [ ] Unit tests dengan pytest
- [ ] Test dengan berbagai jenis gambar:
  - Gambar gelap (underexposed)
  - Gambar terang (overexposed)
  - Gambar low contrast
  - Gambar noisy
  - Gambar dengan color cast
- [ ] Performance benchmarks
- [ ] Known limitations documented

---

## B. Bonus Points (Maksimal +10)

| Bonus | Poin |
|-------|------|
| GUI dengan Tkinter/PyQt | +5 |
| Batch processing untuk multiple images | +3 |
| Comparison side-by-side dengan zoom | +2 |
| Export settings ke JSON/YAML | +2 |
| Undo/Redo functionality | +2 |
| Histogram visualization real-time | +2 |
| Additional creative presets | +1 per preset (max +3) |

---

## C. Penalti

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Terlambat submit (per hari) | -5 per hari |
| Plagiarisme | -50 hingga -100 |
| Program tidak dapat dijalankan | -20 |
| Tidak menggunakan teknik dari materi | -15 |
| Tidak ada dokumentasi | -10 |
| Hardcoded paths (tidak portable) | -5 |
| Memory leak atau infinite loops | -10 |

---

## D. Perhitungan Nilai Akhir

```
Nilai Akhir = Analyzer (25) + Enhancer (35) + Pipeline (25) + Testing (15) + Bonus - Penalti
             -----------------------------------------------------------------------------------
                                                 100

Nilai Maksimal: 100 + 10 (bonus) = 110 (dikonversi ke 100)
```

### Konversi ke Huruf:
| Nilai | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B+ |
| 70-79 | B |
| 60-69 | C+ |
| 50-59 | C |
| <50 | D |

---

## E. Panduan Pengumpulan

### Format Pengumpulan
```
PhotoFix_NamaKelompok/
├── src/
│   ├── analyzer.py          # Image analyzer module
│   ├── enhancer.py          # Image enhancer module
│   ├── pipeline.py          # Enhancement pipeline
│   ├── presets.py           # Preset configurations
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_analyzer.py
│   ├── test_enhancer.py
│   └── test_pipeline.py
├── examples/
│   ├── input/               # Sample input images
│   └── output/              # Sample output images
├── docs/
│   └── report.pdf           # Laporan project
├── main.py                  # Entry point
├── requirements.txt
└── README.md
```

### Deadline
- **Submission:** Minggu ke-2 setelah pemberian tugas
- **Presentasi:** Minggu ke-3
- **Format:** ZIP file via LMS

---

## F. Rubrik Penilaian Presentasi (10% dari nilai project)

| Kriteria | Excellent (9-10) | Good (7-8) | Satisfactory (5-6) | Needs Improvement (0-4) |
|----------|------------------|------------|---------------------|------------------------|
| Demo | Demo lancar, semua fitur ditunjukkan | Demo lancar, fitur utama ditunjukkan | Demo dengan minor issues | Demo tidak berhasil |
| Penjelasan Teknis | Dapat menjelaskan algoritma dengan detail | Penjelasan cukup detail | Penjelasan umum | Tidak dapat menjelaskan |
| Q&A | Menjawab semua pertanyaan dengan baik | Menjawab sebagian besar pertanyaan | Menjawab pertanyaan dasar | Tidak dapat menjawab |
| Teamwork | Semua anggota berkontribusi merata | Kontribusi tidak merata tapi semua aktif | Beberapa anggota tidak aktif | Hanya satu anggota yang presentasi |

---

## G. Contoh Test Cases

### Test Case 1: Underexposed Image
```python
# Input: Gambar dengan mean brightness < 60
# Expected: 
#   - Analyzer mendeteksi "dark"
#   - Auto mode meningkatkan brightness
#   - Hasil: mean brightness antara 100-150
```

### Test Case 2: Noisy Image
```python
# Input: Gambar dengan noise level tinggi
# Expected:
#   - Analyzer mendeteksi noise level
#   - Denoise step berjalan
#   - Noise berkurang tanpa kehilangan detail signifikan
```

### Test Case 3: Color Cast
```python
# Input: Gambar dengan color cast (misal terlalu kuning)
# Expected:
#   - Analyzer mendeteksi color cast
#   - White balance correction
#   - Hasil: channel RGB lebih seimbang
```

---

*Rubrik ini dapat disesuaikan berdasarkan kesepakatan dengan dosen pengampu*
