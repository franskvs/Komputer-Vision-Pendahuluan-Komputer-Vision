# RUBRIK PENILAIAN PROJECT
## BAB 1: PENDAHULUAN COMPUTER VISION
### Project: Sistem Pencatat Kehadiran Digital Berbasis Kartu Identitas

---

## 📊 RUBRIK PENILAIAN DETAIL

### 1. FUNGSIONALITAS (40%)

#### 1.1 Load/Capture Image (8%)

| Skor | Kriteria |
|------|----------|
| **8** (Excellent) | Dapat load berbagai format (jpg, png, bmp), ada validasi file, error handling baik, BONUS: webcam capture berfungsi |
| **6-7** (Good) | Dapat load jpg dan png dengan baik, ada validasi dasar |
| **4-5** (Fair) | Dapat load gambar tapi terbatas format, tidak ada error handling |
| **2-3** (Poor) | Hanya bisa load 1 format, sering error |
| **0-1** (Fail) | Tidak berfungsi atau tidak dikerjakan |

#### 1.2 Resize & Processing (10%)

| Skor | Kriteria |
|------|----------|
| **9-10** (Excellent) | Resize dengan menjaga aspect ratio, ada opsi interpolation, kualitas output bagus |
| **7-8** (Good) | Resize berfungsi baik ke ukuran standar, hasil visual acceptable |
| **5-6** (Fair) | Resize berfungsi tapi gambar terdistorsi atau kualitas menurun |
| **3-4** (Poor) | Resize tidak konsisten, sering error |
| **0-2** (Fail) | Tidak berfungsi |

#### 1.3 Annotation - Timestamp & Border (8%)

| Skor | Kriteria |
|------|----------|
| **8** (Excellent) | Timestamp akurat & readable, border rapi, watermark terintegrasi, posisi dinamis |
| **6-7** (Good) | Timestamp dan border berfungsi dengan baik |
| **4-5** (Fair) | Annotation ada tapi posisi tidak optimal atau susah dibaca |
| **2-3** (Poor) | Hanya sebagian yang berfungsi |
| **0-1** (Fail) | Tidak ada annotation |

#### 1.4 Save dengan Organisasi Folder (7%)

| Skor | Kriteria |
|------|----------|
| **7** (Excellent) | Naming convention konsisten, folder terorganisir per tanggal, ada metadata |
| **5-6** (Good) | Naming dan folder struktur sesuai spesifikasi |
| **3-4** (Fair) | Save berfungsi tapi organisasi tidak rapi |
| **1-2** (Poor) | Save ke lokasi acak, tidak ada organisasi |
| **0** (Fail) | Tidak bisa menyimpan |

#### 1.5 Collage Generator (7%)

| Skor | Kriteria |
|------|----------|
| **7** (Excellent) | Collage 2x2 rapi, ada judul, spacing konsisten, visual menarik |
| **5-6** (Good) | Collage berfungsi dengan baik, layout sesuai |
| **3-4** (Fair) | Collage jadi tapi tidak rapi atau ada gambar yang terpotong |
| **1-2** (Poor) | Collage partial atau banyak bug |
| **0** (Fail) | Tidak dikerjakan |

---

### 2. CODE QUALITY (20%)

| Skor | Kriteria |
|------|----------|
| **18-20** (Excellent) | Kode modular, PEP8 compliant, docstring lengkap, variable naming deskriptif, no redundancy |
| **14-17** (Good) | Struktur baik, ada komentar, minor style issues |
| **10-13** (Fair) | Kode berfungsi tapi kurang terstruktur, komentar minim |
| **6-9** (Poor) | Kode berantakan, sulit dibaca, banyak redundancy |
| **0-5** (Fail) | Kode tidak bisa dijalankan atau plagiat |

**Checklist Code Quality:**
- [ ] Menggunakan function/class dengan baik
- [ ] Nama variabel dan fungsi deskriptif
- [ ] Ada docstring untuk setiap fungsi
- [ ] Tidak ada hardcoded value (gunakan config)
- [ ] Import terorganisir
- [ ] Tidak ada unused code

---

### 3. DOKUMENTASI (15%)

| Skor | Kriteria |
|------|----------|
| **14-15** (Excellent) | README lengkap (instalasi, usage, screenshot), komentar kode detail, ada diagram alur |
| **11-13** (Good) | README cukup lengkap, screenshot ada |
| **8-10** (Fair) | Dokumentasi dasar ada, kurang screenshot |
| **4-7** (Poor) | Dokumentasi minimal, tidak ada README yang proper |
| **0-3** (Fail) | Tidak ada dokumentasi |

**Checklist Dokumentasi:**
- [ ] README.md dengan format proper
- [ ] Cara instalasi jelas
- [ ] Cara menjalankan program jelas
- [ ] Screenshot output minimal 3
- [ ] Penjelasan setiap modul

---

### 4. KREATIVITAS & FITUR BONUS (15%)

| Skor | Kriteria |
|------|----------|
| **14-15** (Excellent) | Minimal 3 fitur bonus, implementasi original dan useful |
| **11-13** (Good) | 2 fitur bonus, implementasi baik |
| **8-10** (Fair) | 1 fitur bonus, cukup baik |
| **4-7** (Poor) | Mencoba fitur bonus tapi tidak complete |
| **0-3** (Fail) | Tidak ada fitur tambahan |

**Fitur Bonus yang Dinilai:**
- [ ] GUI dengan Tkinter/PyQt (+5)
- [ ] Webcam capture real-time (+3)
- [ ] Auto-detect orientasi kartu (+3)
- [ ] Histogram equalization (+2)
- [ ] Batch processing (+2)
- [ ] Export ke PDF (+2)
- [ ] Fitur lain yang relevan (+1-3)

---

### 5. PRESENTASI & DEMO (10%)

| Skor | Kriteria |
|------|----------|
| **9-10** (Excellent) | Dapat menjelaskan semua kode, demo lancar, menjawab pertanyaan dengan baik |
| **7-8** (Good) | Penjelasan baik, demo berfungsi |
| **5-6** (Fair) | Penjelasan cukup, ada kesulitan saat demo |
| **3-4** (Poor) | Tidak bisa menjelaskan beberapa bagian kode |
| **0-2** (Fail) | Tidak bisa menjelaskan atau tidak presentasi |

---

## 📈 REKAPITULASI NILAI

| Komponen | Bobot | Nilai | Nilai Tertimbang |
|----------|-------|-------|------------------|
| Fungsionalitas | 40% |   /40 |                  |
| Code Quality | 20% |   /20 |                  |
| Dokumentasi | 15% |   /15 |                  |
| Kreativitas | 15% |   /15 |                  |
| Presentasi | 10% |   /10 |                  |
| **TOTAL** | **100%** | **/100** |              |

---

## 🏆 KONVERSI NILAI

| Range Nilai | Grade | Keterangan |
|-------------|-------|------------|
| 90-100 | A | Excellent - Melebihi ekspektasi |
| 80-89 | B+ | Very Good - Sangat baik |
| 70-79 | B | Good - Baik, memenuhi semua requirement |
| 60-69 | C+ | Fair - Cukup, perlu perbaikan |
| 50-59 | C | Acceptable - Minimum acceptable |
| < 50 | D/E | Perlu mengulang |

---

## ⚠️ CATATAN PENALTI

| Pelanggaran | Penalti |
|-------------|---------|
| Terlambat submit 1 hari | -5 points |
| Terlambat submit 2-3 hari | -10 points |
| Terlambat submit >3 hari | -20 points |
| Plagiarisme terdeteksi | 0 (Zero) + Laporan ke Prodi |
| File tidak bisa dijalankan | Max 50% dari total |
| Tidak ada source code | 0 (Zero) |

---

## 📝 FEEDBACK FORM

### Kekuatan Project:
_____________________________________

### Area yang Perlu Diperbaiki:
_____________________________________

### Saran untuk Pengembangan:
_____________________________________

---

**Penilai:** _____________________

**Tanggal:** _____________________

**Tanda Tangan:** _____________________
