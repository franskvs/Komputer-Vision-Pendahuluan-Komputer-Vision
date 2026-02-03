# RUBRIK PENILAIAN PROJECT
# BAB 7: SISTEM PENGENALAN KARTU IDENTITAS

---

## 📊 KOMPONEN PENILAIAN

| No | Komponen | Bobot |
|----|----------|-------|
| 1 | Fungsionalitas Program | 40% |
| 2 | Akurasi Sistem | 20% |
| 3 | Kualitas Kode | 20% |
| 4 | Dokumentasi | 10% |
| 5 | Demo Video | 10% |
| **Total** | | **100%** |

---

## 1. FUNGSIONALITAS PROGRAM (40%)

### 1.1 Mode Registrasi Kartu (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Registrasi sempurna: input dari webcam/file, ekstraksi fitur otomatis, penyimpanan ke database terstruktur, feedback visual lengkap |
| 8 | Registrasi berfungsi baik dengan minor bugs, semua fitur utama bekerja |
| 6 | Registrasi berfungsi, namun ada beberapa fitur yang tidak bekerja sempurna |
| 4 | Registrasi berfungsi minimal, hanya dapat menyimpan 1 kartu |
| 2 | Registrasi ada tapi banyak error |
| 0 | Mode registrasi tidak berfungsi |

### 1.2 Mode Verifikasi (15%)

| Skor | Kriteria |
|------|----------|
| 15 | Verifikasi sempurna: matching akurat, threshold optimal, status jelas (VERIFIED/REJECTED), similarity score ditampilkan |
| 12 | Verifikasi berfungsi baik, semua fitur utama bekerja |
| 9 | Verifikasi berfungsi, threshold perlu penyesuaian manual |
| 6 | Verifikasi berfungsi minimal, akurasi rendah |
| 3 | Verifikasi ada tapi banyak error |
| 0 | Mode verifikasi tidak berfungsi |

### 1.3 Visualisasi Matching (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Visualisasi lengkap: matched features ditandai jelas, inlier/outlier dibedakan warna, informasi score ditampilkan |
| 8 | Visualisasi baik, matched features terlihat jelas |
| 6 | Visualisasi ada, namun kurang informatif |
| 4 | Visualisasi minimal |
| 2 | Visualisasi ada tapi sulit dipahami |
| 0 | Tidak ada visualisasi |

### 1.4 User Interface (5%)

| Skor | Kriteria |
|------|----------|
| 5 | UI intuitif, menu jelas, feedback untuk setiap aksi, handling error baik |
| 4 | UI berfungsi dengan baik |
| 3 | UI berfungsi, namun kurang user-friendly |
| 2 | UI minimal, text-based |
| 1 | UI membingungkan |
| 0 | Tidak ada UI/interface |

---

## 2. AKURASI SISTEM (20%)

### 2.1 True Positive Rate (10%)

| Skor | Kriteria |
|------|----------|
| 10 | TPR ≥ 95%: Kartu valid selalu dikenali sebagai VERIFIED |
| 8 | TPR 85-94% |
| 6 | TPR 75-84% |
| 4 | TPR 65-74% |
| 2 | TPR 50-64% |
| 0 | TPR < 50% |

### 2.2 True Negative Rate (10%)

| Skor | Kriteria |
|------|----------|
| 10 | TNR ≥ 90%: Kartu tidak terdaftar selalu REJECTED |
| 8 | TNR 80-89% |
| 6 | TNR 70-79% |
| 4 | TNR 60-69% |
| 2 | TNR 50-59% |
| 0 | TNR < 50% |

---

## 3. KUALITAS KODE (20%)

### 3.1 Struktur dan Organisasi (7%)

| Skor | Kriteria |
|------|----------|
| 7 | Kode terorganisir dalam modul terpisah, fungsi terdefinisi dengan baik, folder structure rapi |
| 5-6 | Kode terorganisir dengan baik |
| 3-4 | Kode cukup terorganisir |
| 1-2 | Kode kurang terorganisir |
| 0 | Kode berantakan |

### 3.2 Readability dan Style (6%)

| Skor | Kriteria |
|------|----------|
| 6 | Kode mudah dibaca, naming convention konsisten, indentasi rapi, mengikuti PEP8 |
| 4-5 | Kode mudah dibaca dengan style yang baik |
| 2-3 | Kode cukup mudah dibaca |
| 1 | Kode sulit dibaca |
| 0 | Kode sangat sulit dibaca |

### 3.3 Dokumentasi Kode (7%)

| Skor | Kriteria |
|------|----------|
| 7 | Semua fungsi memiliki docstring, komentar informatif, type hints digunakan |
| 5-6 | Dokumentasi kode baik |
| 3-4 | Dokumentasi kode cukup |
| 1-2 | Dokumentasi kode minimal |
| 0 | Tidak ada dokumentasi kode |

---

## 4. DOKUMENTASI (10%)

### 4.1 README File (5%)

| Skor | Kriteria |
|------|----------|
| 5 | README lengkap: deskripsi project, cara instalasi, cara penggunaan, screenshot, troubleshooting |
| 4 | README baik dengan sebagian besar informasi |
| 3 | README cukup, informasi dasar ada |
| 2 | README minimal |
| 1 | README sangat singkat |
| 0 | Tidak ada README |

### 4.2 Laporan Testing (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Laporan testing lengkap: test cases, hasil testing, analisis performa, confusion matrix |
| 4 | Laporan testing baik |
| 3 | Laporan testing cukup |
| 2 | Laporan testing minimal |
| 1 | Laporan testing sangat singkat |
| 0 | Tidak ada laporan testing |

---

## 5. DEMO VIDEO (10%)

### 5.1 Kelengkapan Demo (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Demo lengkap: registrasi, verifikasi valid, verifikasi invalid, visualisasi, penjelasan algoritma |
| 4 | Demo mencakup hampir semua fitur |
| 3 | Demo mencakup fitur utama |
| 2 | Demo mencakup beberapa fitur |
| 1 | Demo sangat singkat |
| 0 | Tidak ada demo |

### 5.2 Kualitas Presentasi (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Presentasi jelas, audio jernih, visual berkualitas, narasi informatif |
| 4 | Presentasi baik |
| 3 | Presentasi cukup |
| 2 | Presentasi kurang jelas |
| 1 | Presentasi sulit dipahami |
| 0 | Kualitas sangat buruk |

---

## 🌟 BONUS POINTS (Maksimal +20%)

| Fitur Bonus | Poin |
|-------------|------|
| Multi-card database dengan pencarian otomatis | +5 |
| Real-time webcam verification (≥10 FPS) | +5 |
| Anti-spoofing detection | +5 |
| Report generation (PDF/HTML) | +5 |
| GUI dengan tkinter/PyQt | +3 |
| Deployment ke web (Flask/Streamlit) | +5 |

---

## 📝 CATATAN PENILAIAN

### Penalti
| Pelanggaran | Penalti |
|-------------|---------|
| Plagiarisme | -100% (nilai 0) |
| Terlambat 1 hari | -10% |
| Terlambat 2 hari | -20% |
| Terlambat >3 hari | Tidak diterima |
| File tidak lengkap | -5% per file |

### Nilai Akhir
```
Nilai Akhir = (Fungsionalitas × 0.4) + (Akurasi × 0.2) + (Kode × 0.2) + (Dokumentasi × 0.1) + (Demo × 0.1) + Bonus
```

### Konversi Nilai
| Rentang | Grade |
|---------|-------|
| 85-100 | A |
| 80-84 | A- |
| 75-79 | B+ |
| 70-74 | B |
| 65-69 | B- |
| 60-64 | C+ |
| 55-59 | C |
| 50-54 | D |
| <50 | E |

---

## ✅ CHECKLIST PENGUMPULAN

Sebelum submit, pastikan:
- [ ] Semua file program ada dan bisa dijalankan
- [ ] Folder structure sesuai spesifikasi
- [ ] README.md lengkap
- [ ] requirements.txt ada
- [ ] Test images tersedia
- [ ] Output/results folder ada
- [ ] Demo video tersedia
- [ ] Tidak ada informasi pribadi yang tidak disensor
