# Rubrik Penilaian Project - Bab 6: Recognition

## Informasi Project

| Komponen | Keterangan |
|----------|------------|
| **Judul Project** | Sistem Pengenalan (Recognition System) |
| **Bab** | 6 - Recognition |
| **Bobot** | 40% dari nilai praktikum |
| **Deadline** | 2 minggu setelah materi selesai |

---

## Kategori Project

### Kategori A: Face Recognition System
Sistem absensi atau verifikasi identitas berbasis wajah

### Kategori B: Object Classification System
Sistem klasifikasi objek untuk domain spesifik (tanaman, hewan, produk)

### Kategori C: Scene Recognition Application
Aplikasi pengenalan scene untuk foto/video

### Kategori D: OCR Application
Aplikasi pembaca teks dari gambar (dokumen, plat nomor, dll)

---

## Rubrik Penilaian Detail

### 1. Fungsionalitas Sistem (25 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 25 | Sangat Baik | Semua fitur berfungsi sempurna, akurasi tinggi (>90%), handling error excellent |
| 20 | Baik | Semua fitur utama berfungsi, akurasi baik (80-90%), error handling baik |
| 15 | Cukup | Fitur utama berfungsi dengan masalah minor, akurasi cukup (70-80%) |
| 10 | Kurang | Beberapa fitur tidak berfungsi, akurasi rendah (<70%) |
| 5 | Sangat Kurang | Banyak fitur error, sistem tidak dapat digunakan dengan baik |

**Checklist Fungsionalitas:**
- [ ] Detection berfungsi dengan baik
- [ ] Recognition/classification akurat
- [ ] Database management (jika ada) berfungsi
- [ ] Real-time processing (jika ada) lancar
- [ ] Error handling implementasi

### 2. Implementasi Teknis (25 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 25 | Sangat Baik | Algoritma optimal, arsitektur modular, code reusable, best practices |
| 20 | Baik | Algoritma tepat, struktur baik, minor improvements possible |
| 15 | Cukup | Algoritma dasar berfungsi, struktur cukup baik |
| 10 | Kurang | Algoritma tidak optimal, struktur code kurang baik |
| 5 | Sangat Kurang | Algoritma salah atau tidak efisien, code tidak terstruktur |

**Aspek Teknis yang Dinilai:**

#### Face Recognition:
- [ ] Pre-processing wajah (alignment, normalization)
- [ ] Feature extraction method (LBPH/embeddings)
- [ ] Distance metric implementation
- [ ] Threshold optimization
- [ ] Multi-face handling

#### Object Classification:
- [ ] Model selection dan loading
- [ ] Pre-processing pipeline
- [ ] Batch processing capability
- [ ] Confidence thresholding
- [ ] Top-K predictions

#### Scene Recognition:
- [ ] Scene category hierarchy
- [ ] Attribute prediction
- [ ] Indoor/outdoor classification
- [ ] Scene understanding depth

#### OCR:
- [ ] Pre-processing untuk OCR
- [ ] Text detection accuracy
- [ ] Character recognition rate
- [ ] Post-processing (spell check)
- [ ] Multiple language support

### 3. User Interface (15 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 15 | Sangat Baik | UI intuitif, responsif, visualisasi excellent, user feedback clear |
| 12 | Baik | UI baik, responsif, visualisasi informatif |
| 9 | Cukup | UI fungsional, visualisasi dasar ada |
| 6 | Kurang | UI minimal, sulit digunakan |
| 3 | Sangat Kurang | Tidak ada UI atau sangat sulit digunakan |

**Elemen UI yang Dinilai:**
- [ ] Menu navigasi jelas
- [ ] Visualisasi hasil recognition
- [ ] Confidence score display
- [ ] Progress indicator (untuk batch processing)
- [ ] Error message informatif
- [ ] Help/instruction tersedia

### 4. Dokumentasi (15 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 15 | Sangat Baik | Dokumentasi lengkap, jelas, dengan contoh dan diagram |
| 12 | Baik | Dokumentasi baik, mencakup semua aspek penting |
| 9 | Cukup | Dokumentasi dasar ada, beberapa bagian kurang detail |
| 6 | Kurang | Dokumentasi minimal atau tidak lengkap |
| 3 | Sangat Kurang | Tidak ada dokumentasi atau sangat minim |

**Komponen Dokumentasi:**
- [ ] README dengan instalasi dan usage
- [ ] Docstring di semua fungsi
- [ ] Komentar kode yang informatif
- [ ] Penjelasan algoritma yang digunakan
- [ ] Contoh input/output
- [ ] Troubleshooting guide

### 5. Inovasi dan Kreativitas (10 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 10 | Sangat Baik | Fitur inovatif, pendekatan kreatif, value-add signifikan |
| 8 | Baik | Beberapa fitur tambahan yang berguna |
| 6 | Cukup | Implementasi standar dengan sedikit variasi |
| 4 | Kurang | Implementasi minimal tanpa inovasi |
| 2 | Sangat Kurang | Copy-paste tanpa modifikasi |

**Contoh Inovasi:**
- Ensemble multiple recognition methods
- Adaptive thresholding berdasarkan lighting
- Real-time performance optimization
- Mobile/edge deployment
- Integration dengan sistem lain
- Custom training pada dataset lokal

### 6. Presentasi dan Demo (10 poin)

| Skor | Kriteria | Deskripsi |
|------|----------|-----------|
| 10 | Sangat Baik | Presentasi jelas, demo lancar, Q&A excellent |
| 8 | Baik | Presentasi baik, demo minor issues, Q&A baik |
| 6 | Cukup | Presentasi cukup, demo dengan beberapa masalah |
| 4 | Kurang | Presentasi kurang jelas, demo banyak masalah |
| 2 | Sangat Kurang | Tidak dapat presentasi atau demo |

---

## Skenario Penilaian per Kategori

### Kategori A: Face Recognition System

| Komponen | Bobot | Kriteria Khusus |
|----------|-------|-----------------|
| Face Detection | 15% | Multi-face, various poses, lighting |
| Face Recognition | 25% | Accuracy, database management |
| Performance | 15% | Real-time capability |
| Application | 20% | Attendance/verification flow |
| UI/UX | 15% | Usability |
| Documentation | 10% | Completeness |

**Minimum Requirements:**
- Dapat detect wajah dalam berbagai kondisi
- Recognition accuracy > 85% pada dataset test
- Database minimal 5 orang, 5 foto/orang
- Aplikasi attendance/verification fungsional

### Kategori B: Object Classification

| Komponen | Bobot | Kriteria Khusus |
|----------|-------|-----------------|
| Model Selection | 15% | Appropriate model for task |
| Classification | 30% | Accuracy, Top-K |
| Preprocessing | 15% | Proper image handling |
| Application | 20% | Domain-specific features |
| UI/UX | 10% | Visualization |
| Documentation | 10% | Completeness |

**Minimum Requirements:**
- Classification accuracy > 80% pada domain
- Minimal 10 categories
- Confidence visualization
- Batch processing capability

### Kategori C: Scene Recognition

| Komponen | Bobot | Kriteria Khusus |
|----------|-------|-----------------|
| Scene Classification | 30% | Category accuracy |
| Attributes | 20% | Multi-attribute prediction |
| Hierarchy | 15% | Level classification |
| Application | 15% | Photo organization/search |
| UI/UX | 10% | Visualization |
| Documentation | 10% | Completeness |

**Minimum Requirements:**
- Indoor/outdoor classification > 90%
- Fine-grained scene > 70%
- Minimal 5 scene attributes
- Photo tagging application

### Kategori D: OCR Application

| Komponen | Bobot | Kriteria Khusus |
|----------|-------|-----------------|
| Text Detection | 20% | Accuracy, orientation |
| Text Recognition | 30% | Character accuracy |
| Preprocessing | 15% | Enhancement quality |
| Application | 20% | Document/plate reading |
| UI/UX | 10% | User interface |
| Documentation | 5% | Completeness |

**Minimum Requirements:**
- Text detection accuracy > 85%
- Character recognition > 90% (clean images)
- Support multiple document types
- Post-processing (spell check) implemented

---

## Pengurangan Nilai

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Terlambat 1-3 hari | -10% |
| Terlambat 4-7 hari | -25% |
| Terlambat > 7 hari | -50% |
| Plagiarisme partial | -50% |
| Plagiarisme total | -100% + sanksi akademik |
| Tidak dapat demo | -20% |
| Code tidak berjalan | -30% |

---

## Bonus Nilai

| Achievement | Bonus |
|-------------|-------|
| Akurasi > 95% | +5% |
| Real-time processing | +5% |
| Cross-platform compatibility | +5% |
| Deploy ke cloud/edge | +10% |
| Custom model training | +10% |
| Integration dengan hardware | +10% |

**Maksimum bonus: 20%**

---

## Format Pengumpulan

### Struktur Folder:
```
NIM_Nama_Bab6_Project/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── detection.py
│   ├── recognition.py
│   └── utils.py
├── models/
│   └── (pre-trained models)
├── data/
│   ├── train/
│   └── test/
├── docs/
│   ├── report.pdf
│   └── presentation.pptx
└── demo/
    └── demo_video.mp4
```

### Deliverables:
1. Source code lengkap
2. Pre-trained models (atau link download)
3. Sample data untuk testing
4. Laporan teknis (PDF)
5. Video demo (2-5 menit)
6. Slide presentasi

---

## Jadwal Penilaian

| Tahap | Waktu | Bobot |
|-------|-------|-------|
| Progress Report 1 | Minggu 1 | 10% |
| Progress Report 2 | Minggu 2 | 10% |
| Final Submission | End Minggu 2 | 60% |
| Presentasi | Minggu 3 | 20% |

---

## Contoh Penilaian

### Contoh: Face Recognition Attendance System

| Kriteria | Skor | Keterangan |
|----------|------|------------|
| Fungsionalitas | 22/25 | Semua fitur OK, minor bug |
| Teknis | 20/25 | Good implementation, bisa improve |
| UI | 12/15 | Clean UI, bisa lebih responsif |
| Dokumentasi | 12/15 | Lengkap, kurang diagram |
| Inovasi | 8/10 | Anti-spoofing feature |
| Presentasi | 8/10 | Demo lancar |
| **Total** | **82/100** | **A-** |

---

*Rubrik ini dapat disesuaikan oleh dosen pengampu sesuai kebutuhan kelas*
