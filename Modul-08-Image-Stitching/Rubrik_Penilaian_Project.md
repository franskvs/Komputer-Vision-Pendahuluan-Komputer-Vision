# RUBRIK PENILAIAN PROJECT
# BAB 8: SISTEM PEMBUATAN VIRTUAL TOUR (QuickPano)

---

## 📊 KOMPONEN PENILAIAN

| No | Komponen | Bobot |
|----|----------|-------|
| 1 | Fungsionalitas Program | 40% |
| 2 | Kualitas Hasil | 20% |
| 3 | Kualitas Kode | 20% |
| 4 | Dokumentasi | 10% |
| 5 | Demo Video | 10% |
| **Total** | | **100%** |

---

## 1. FUNGSIONALITAS PROGRAM (40%)

### 1.1 Input & Validation (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Load multiple images sempurna, validasi lengkap (format, ukuran, overlap detection), error handling baik |
| 8 | Load dan validasi berfungsi dengan minor issues |
| 6 | Load berfungsi, validasi dasar ada |
| 4 | Load berfungsi minimal |
| 2 | Load sering error |
| 0 | Tidak bisa load gambar |

### 1.2 Feature Matching (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Feature detection robust, matching akurat, ratio test dan RANSAC diimplementasi dengan baik |
| 8 | Matching berfungsi baik di kebanyakan kasus |
| 6 | Matching berfungsi tapi kadang gagal |
| 4 | Matching tidak konsisten |
| 2 | Matching sering gagal |
| 0 | Matching tidak berfungsi |

### 1.3 Warping & Stitching (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Warping akurat, alignment sempurna, handle multiple images dengan baik |
| 8 | Warping dan alignment baik |
| 6 | Warping berfungsi dengan beberapa misalignment |
| 4 | Warping basic berfungsi |
| 2 | Warping sering error |
| 0 | Warping tidak berfungsi |

### 1.4 Output Generation (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Output berkualitas tinggi, thumbnail generated, metadata lengkap, format benar |
| 8 | Output baik dengan semua fitur |
| 6 | Output tersimpan dengan kualitas cukup |
| 4 | Output basic tersimpan |
| 2 | Output kadang gagal save |
| 0 | Output tidak bisa disimpan |

---

## 2. KUALITAS HASIL (20%)

### 2.1 Seam Visibility (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Tidak ada seam yang terlihat, transisi sempurna |
| 8 | Seam hampir tidak terlihat |
| 6 | Seam sedikit terlihat jika diperhatikan |
| 4 | Seam cukup terlihat |
| 2 | Seam sangat terlihat |
| 0 | Seam sangat mengganggu |

### 2.2 Alignment & Distortion (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Alignment sempurna, tidak ada ghosting atau distorsi |
| 8 | Alignment baik, minimal artifacts |
| 6 | Ada sedikit misalignment atau ghosting |
| 4 | Misalignment cukup terlihat |
| 2 | Banyak alignment issues |
| 0 | Alignment sangat buruk |

---

## 3. KUALITAS KODE (20%)

### 3.1 Struktur & Modularitas (7%)

| Skor | Kriteria |
|------|----------|
| 7 | Kode terorganisir dalam modul terpisah dengan tanggung jawab jelas |
| 5-6 | Kode terorganisir dengan baik |
| 3-4 | Kode cukup terorganisir |
| 1-2 | Kode kurang terorganisir |
| 0 | Kode berantakan |

### 3.2 Readability & Style (6%)

| Skor | Kriteria |
|------|----------|
| 6 | Kode mudah dibaca, naming baik, PEP8 compliant |
| 4-5 | Kode mudah dibaca |
| 2-3 | Kode cukup mudah dibaca |
| 1 | Kode sulit dibaca |
| 0 | Kode sangat sulit dibaca |

### 3.3 Error Handling (7%)

| Skor | Kriteria |
|------|----------|
| 7 | Error handling komprehensif, pesan informatif, tidak crash |
| 5-6 | Error handling baik |
| 3-4 | Error handling cukup |
| 1-2 | Error handling minimal |
| 0 | Tidak ada error handling |

---

## 4. DOKUMENTASI (10%)

### 4.1 README (5%)

| Skor | Kriteria |
|------|----------|
| 5 | README lengkap: deskripsi, instalasi, usage, examples, troubleshooting |
| 4 | README baik |
| 3 | README cukup |
| 2 | README minimal |
| 1 | README sangat singkat |
| 0 | Tidak ada README |

### 4.2 Code Documentation (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Docstring lengkap, komentar informatif di bagian kompleks |
| 4 | Dokumentasi baik |
| 3 | Dokumentasi cukup |
| 2 | Dokumentasi minimal |
| 1 | Dokumentasi sangat kurang |
| 0 | Tidak ada dokumentasi |

---

## 5. DEMO VIDEO (10%)

### 5.1 Kelengkapan Demo (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Demo lengkap: load, process, hasil sukses, error handling |
| 4 | Demo mencakup hampir semua fitur |
| 3 | Demo mencakup fitur utama |
| 2 | Demo minimal |
| 0 | Tidak ada demo |

### 5.2 Kualitas Presentasi (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Presentasi jelas, narasi informatif, profesional |
| 4 | Presentasi baik |
| 3 | Presentasi cukup |
| 2 | Presentasi kurang jelas |
| 0 | Kualitas sangat buruk |

---

## 🌟 BONUS POINTS (Maksimal +20%)

| Fitur Bonus | Poin |
|-------------|------|
| Exposure compensation otomatis | +5 |
| Auto crop area hitam | +5 |
| HTML 360° viewer | +5 |
| Batch processing multiple folders | +5 |
| GUI dengan preview | +5 |
| Cylindrical projection | +5 |

---

## 📝 PENALTI

| Pelanggaran | Penalti |
|-------------|---------|
| Plagiarisme | -100% (nilai 0) |
| Terlambat 1 hari | -10% |
| Terlambat 2 hari | -20% |
| Terlambat >3 hari | Tidak diterima |
| Program crash tanpa error message | -10% |
| Tidak bisa run di OS lain | -5% |

---

## ✅ CHECKLIST PENGUMPULAN

Sebelum submit, pastikan:
- [ ] Semua file program ada dan bisa dijalankan
- [ ] requirements.txt lengkap
- [ ] README.md informatif
- [ ] Contoh input tersedia (minimal 2 set)
- [ ] Contoh output tersedia
- [ ] Demo video tersedia
- [ ] Tested di clean environment
