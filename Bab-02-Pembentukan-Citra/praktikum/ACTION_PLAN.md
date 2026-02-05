# ACTION PLAN: REVISI KOMENTAR LENGKAP SEMUA PROGRAM

## Overview
Menambahkan komentar detail dan edukatif ke setiap baris penting pada semua 15 program praktikum Bab-02.

## Prinsip Komentar
1. **SETIAP FUNGSI** harus dijelaskan parameternya (a apa, b apa, c apa)
2. **SETIAP VARIABEL PENTING** harus ada keterangan
3. **SETIAP OPERASI MATEMATIKA** harus dijelaskan rumusnya
4. **FORMAT BGR** selalu dijelaskan (B=Blue, G=Green, R=Red)
5. **KOORDINAT** selalu dijelaskan (x, y) atau (row, col)

## Status Program

| No | File | Status | Priority | Estimasi |
|----|------|--------|----------|----------|
| 1 | 01_translasi.py | 🔄 IN PROGRESS | HIGH | 30 min |
| 2 | 02_rotasi.py | ⏳ PENDING | HIGH | 30 min |
| 3 | 03_scaling.py | ⏳ PENDING | HIGH | 25 min |
| 4 | 04_affine_transform.py | ⏳ PENDING | HIGH | 35 min |
| 5 | 05_perspektif_transform.py | ⏳ PENDING | HIGH | 35 min |
| 6 | 05_perspektif_transform_auto.py | ⏳ PENDING | MEDIUM | 30 min |
| 7 | 06_document_scanner.py | ⏳ PENDING | HIGH | 40 min |
| 8 | 06_document_scanner_auto.py | ⏳ PENDING | MEDIUM | 35 min |
| 9 | 07_3d_rotations.py | ⏳ PENDING | HIGH | 45 min |
| 10 | 08_3d_projection.py | ⏳ PENDING | HIGH | 40 min |
| 11 | 09_camera_calibration.py | ⏳ PENDING | HIGH | 50 min |
| 12 | 10_lens_distortion.py | ⏳ PENDING | HIGH | 40 min |
| 13 | 11_sampling_aliasing.py | ⏳ PENDING | HIGH | 35 min |
| 14 | 12_phong_shading.py | ⏳ PENDING | HIGH | 45 min |
| 15 | 13_color_spaces.py | ⏳ PENDING | HIGH | 35 min |
| 16 | 14_gamma_correction.py | ⏳ PENDING | HIGH | 30 min |
| 17 | 15_compression_artifacts.py | ⏳ PENDING | HIGH | 30 min |
| 18 | setup_images.py | ⏳ PENDING | LOW | 40 min |

**Total Estimasi:** ~10 jam
**Prioritas:** Program 01-15 (HIGH), Automated versions (MEDIUM), setup_images (LOW)

## Referensi yang Sudah Dibuat

✅ **01_translasi_IMPROVED.py**
- Contoh lengkap komentar yang baik
- Referensi untuk program lainnya

✅ **PANDUAN_KOMENTAR_LENGKAP.md**
- Pedoman penulisan komentar
- Dokumentasi fungsi OpenCV
- Template dan best practices

✅ **MATERI_COVERAGE_VERIFICATION.md**
- Verifikasi semua materi tercakup
- Mapping program → materi PDF
- Checklist lengkap

## Strategi Revisi

### Batch 1: Geometric Transformations (Programs 01-06)
**Focus:** Transformation matrices, coordinate systems, border modes

Files:
- 01_translasi.py ← IMPROVED version sudah ada
- 02_rotasi.py
- 03_scaling.py
- 04_affine_transform.py
- 05_perspektif_transform.py
- 06_document_scanner.py

**Key Comments Needed:**
- Matriks transformasi (2x3 atau 3x3)
- Parameter cv2.warpAffine() / cv2.warpPerspective()
- Border modes
- Coordinate systems

### Batch 2: 3D & Camera (Programs 07-10)
**Focus:** 3D transformations, projections, camera models

Files:
- 07_3d_rotations.py
- 08_3d_projection.py
- 09_camera_calibration.py
- 10_lens_distortion.py

**Key Comments Needed:**
- 3D rotation matrices (Rx, Ry, Rz)
- Projection matrices
- Camera intrinsic/extrinsic parameters
- Distortion coefficients

### Batch 3: Image Formation (Programs 11-15)
**Focus:** Sampling, shading, color, compression

Files:
- 11_sampling_aliasing.py
- 12_phong_shading.py
- 13_color_spaces.py
- 14_gamma_correction.py
- 15_compression_artifacts.py

**Key Comments Needed:**
- Sampling theory
- BRDF, Phong model
- Color space conversions
- Gamma functions
- Compression parameters

## Template Sections untuk Setiap Program

```python
# ============================================================
# PROGRAM: [Nama]
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: [1-2 kalimat]
# 
# Tujuan Pembelajaran:
#   1. [Tujuan 1]
#   2. [Tujuan 2]
#   3. [Tujuan 3]
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
[... imports dengan komentar ...]

# ============================================================
# PANDUAN FUNGSI OPENCV - PENJELASAN DETAIL
# ============================================================
[... dokumentasi fungsi yang dipakai ...]

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================
[... constants dengan range nilai ...]

# ============================================================
# FUNGSI UTAMA
# ============================================================
[... fungsi dengan docstring lengkap ...]
```

## Checklist Komentar untuk Setiap Program

Setiap program harus memiliki:

### 1. Header & Metadata
- [ ] Nama program
- [ ] Deskripsi singkat
- [ ] Tujuan pembelajaran (minimal 3)
- [ ] Dependencies

### 2. Import Section
- [ ] Komentar untuk setiap library
- [ ] Penjelasan kenapa library dibutuhkan

### 3. Dokumentasi Fungsi OpenCV
- [ ] Daftar semua fungsi cv2.* yang dipakai
- [ ] Penjelasan setiap parameter
- [ ] Penjelasan return value
- [ ] Contoh nilai parameter

### 4. Variabel Konfigurasi
- [ ] Nama variabel yang jelas
- [ ] Komentar penjelasan
- [ ] Range nilai yang bisa dicoba
- [ ] Default value dengan alasan

### 5. Fungsi Custom
- [ ] Docstring lengkap
- [ ] Parameter types & descriptions
- [ ] Return type & description
- [ ] Contoh penggunaan

### 6. Code Logic
- [ ] Komentar sebelum operasi penting
- [ ] Penjelasan formula matematika
- [ ] Penjelasan array indexing
- [ ] Penjelasan loop logic

### 7. Matplotlib
- [ ] Penjelasan figsize
- [ ] Penjelasan subplot layout
- [ ] Penjelasan colormap
- [ ] Penjelasan savefig parameters

### 8. Output Section
- [ ] Ringkasan output files
- [ ] Next steps untuk user
- [ ] Tips eksperimen

## Common Patterns yang Perlu Dijelaskan

### 1. cv2.putText()
```python
# Tambahkan label teks pada gambar
# cv2.putText(img, text, org, fontFace, fontScale, color, thickness)
#   img: gambar yang akan ditambah teks (modified in-place)
#   text: "Label" = string yang ditampilkan
#   org: (x, y) = koordinat bottom-left teks
#   fontFace: FONT_HERSHEY_SIMPLEX = font simple readable
#   fontScale: 1.0 = ukuran normal
#   color: (B, G, R) = (255, 0, 0) biru penuh
#   thickness: 2 = ketebalan huruf dalam piksel
cv2.putText(img, "Label", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
            1.0, (255, 0, 0), 2)
```

### 2. cv2.warpAffine()
```python
# Terapkan transformasi affine pada gambar
# cv2.warpAffine(src, M, dsize, flags, borderMode, borderValue)
#   src: gambar sumber yang akan ditransformasi
#   M: matriks transformasi affine 2x3
#   dsize: (width, height) ukuran output
#   flags: cv2.INTER_LINEAR = bilinear interpolation
#   borderMode: cv2.BORDER_CONSTANT = isi dengan warna solid
#   borderValue: (50, 50, 50) = abu-abu gelap untuk area kosong
result = cv2.warpAffine(img, M, (w, h), 
                        flags=cv2.INTER_LINEAR,
                        borderMode=cv2.BORDER_CONSTANT,
                        borderValue=(50, 50, 50))
```

### 3. np.float32 Matrix
```python
# Buat matriks translasi 2x3 dengan tipe float32
# Format: [[1, 0, tx], [0, 1, ty]]
# Persamaan: x' = x + tx, y' = y + ty
# tx: pergeseran horizontal (positif=kanan, negatif=kiri)
# ty: pergeseran vertikal (positif=bawah, negatif=atas)
M = np.float32([
    [1, 0, tx],  # Baris transformasi x
    [0, 1, ty]   # Baris transformasi y
])
```

### 4. Array Indexing
```python
# Ambil dimensi gambar dari shape
# shape mengembalikan tuple (height, width, channels)
# [:2] mengambil hanya 2 elemen pertama (h, w), abaikan channels
h, w = img.shape[:2]

# Akses piksel pada posisi (row=100, col=200)
# Format: img[row, col] untuk grayscale
# Format: img[row, col, channel] untuk BGR
pixel = img[100, 200]  # Ambil nilai piksel BGR
blue = img[100, 200, 0]  # Ambil channel Blue saja
```

### 5. Color Format
```python
# Definisikan warna dalam format BGR (bukan RGB!)
# OpenCV menggunakan BGR, matplotlib menggunakan RGB
# Format: (B, G, R) dimana setiap nilai 0-255
COLOR_BLUE = (255, 0, 0)    # Biru penuh (B=255, G=0, R=0)
COLOR_GREEN = (0, 255, 0)   # Hijau penuh (B=0, G=255, R=0)
COLOR_RED = (0, 0, 255)     # Merah penuh (B=0, G=0, R=255)
COLOR_CYAN = (255, 255, 0)  # Cyan = Biru + Hijau
COLOR_WHITE = (255, 255, 255)  # Putih = semua maksimal
COLOR_BLACK = (0, 0, 0)     # Hitam = semua 0
```

## Progress Tracking

### Week 1: Batch 1 (Geometric)
- [ ] 01_translasi.py (DONE - IMPROVED version)
- [ ] 02_rotasi.py
- [ ] 03_scaling.py
- [ ] 04_affine_transform.py
- [ ] 05_perspektif_transform.py
- [ ] 06_document_scanner.py

### Week 2: Batch 2 (3D & Camera)
- [ ] 07_3d_rotations.py
- [ ] 08_3d_projection.py
- [ ] 09_camera_calibration.py
- [ ] 10_lens_distortion.py

### Week 3: Batch 3 (Image Formation)
- [ ] 11_sampling_aliasing.py
- [ ] 12_phong_shading.py
- [ ] 13_color_spaces.py
- [ ] 14_gamma_correction.py
- [ ] 15_compression_artifacts.py

### Week 4: Finalization
- [ ] Automated versions (05_auto, 06_auto)
- [ ] setup_images.py
- [ ] Final testing & verification
- [ ] Documentation update

## Quality Assurance

Setiap program yang sudah direvisi harus:
1. ✅ Run without errors
2. ✅ Generate expected output
3. ✅ Have complete header documentation
4. ✅ Have function parameter documentation
5. ✅ Have inline comments for critical operations
6. ✅ Have example values for abstract parameters
7. ✅ Have educational explanations (not just technical)
8. ✅ Use consistent comment style
9. ✅ Follow PANDUAN_KOMENTAR_LENGKAP.md

## Final Deliverables

1. **15 Program Files** dengan komentar lengkap
2. **PANDUAN_KOMENTAR_LENGKAP.md** (DONE)
3. **MATERI_COVERAGE_VERIFICATION.md** (DONE)
4. **ACTION_PLAN.md** (THIS FILE)
5. **README.md** (Updated with comment guidelines)
6. **Test results** showing all programs pass

## Success Metrics

- ✅ Setiap fungsi OpenCV terdokumentasi lengkap
- ✅ Setiap parameter dijelaskan (a apa, b apa, c apa)
- ✅ Pemula bisa belajar tanpa sumber eksternal
- ✅ Kode tetap clean dan readable
- ✅ Semua program tested dan verified

---

**Status:** 🟡 IN PROGRESS (1/17 files completed)
**Last Updated:** 2024
**Next Action:** Continue with 02_rotasi.py
