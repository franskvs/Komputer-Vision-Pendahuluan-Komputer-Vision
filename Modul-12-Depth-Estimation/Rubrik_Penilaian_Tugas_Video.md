# RUBRIK PENILAIAN TUGAS VIDEO
## BAB 12: DEPTH ESTIMATION

---

## 📹 Spesifikasi Video

| Aspek | Ketentuan |
|-------|-----------|
| **Durasi** | 7-10 menit |
| **Format** | MP4 (H.264) |
| **Resolusi** | Minimal 720p (1280×720) |
| **Audio** | Narasi dalam Bahasa Indonesia |
| **Konten** | Penjelasan konsep + demonstrasi kode |

---

## 📋 Struktur Video yang Diharapkan

### Bagian 1: Pendahuluan (1-2 menit)
- Perkenalan diri
- Judul topik
- Overview singkat materi

### Bagian 2: Penjelasan Teori (3-4 menit)
- Konsep stereo vision dan depth estimation
- Penjelasan disparity dan hubungannya dengan depth
- Algoritma stereo matching (Block Matching, SGM)
- Monocular depth estimation (opsional)

### Bagian 3: Demonstrasi Praktis (3-4 menit)
- Penjelasan kode program
- Running program dan hasil
- Analisis output

### Bagian 4: Penutup (1 menit)
- Kesimpulan
- Tantangan dan solusi
- Referensi

---

## 📊 Rubrik Penilaian Detail

### 1. Konten Materi (40%)

| Kriteria | Excellent (36-40) | Good (28-35) | Fair (20-27) | Poor (0-19) |
|----------|------------------|--------------|--------------|-------------|
| **Akurasi Teknis** | Semua penjelasan akurat, terminologi tepat | Sebagian besar akurat | Ada beberapa kesalahan | Banyak kesalahan |
| **Kedalaman** | Penjelasan mendalam, contoh relevan | Cukup mendalam | Permukaan saja | Sangat dangkal |
| **Kelengkapan** | Semua aspek penting tercakup | Sebagian besar tercakup | Beberapa aspek missing | Tidak lengkap |
| **Contoh/Ilustrasi** | Ilustrasi jelas, diagram membantu | Cukup ilustratif | Minimal ilustrasi | Tidak ada |

#### Checklist Konten untuk Bab 12:

- [ ] Penjelasan konsep stereo vision
- [ ] Rumus disparity ke depth
- [ ] Penjelasan algoritma Block Matching
- [ ] Penjelasan Semi-Global Matching (SGM)
- [ ] Parameter tuning (numDisparities, blockSize)
- [ ] Post-processing (WLS filter)
- [ ] Konsep monocular depth (MiDaS)
- [ ] Aplikasi depth estimation

### 2. Demonstrasi Kode (25%)

| Kriteria | Excellent (22-25) | Good (18-21) | Fair (13-17) | Poor (0-12) |
|----------|------------------|--------------|--------------|-------------|
| **Penjelasan Kode** | Setiap bagian penting dijelaskan | Sebagian besar dijelaskan | Penjelasan minimal | Tidak ada penjelasan |
| **Running Demo** | Program berjalan lancar, output jelas | Berjalan dengan minor issue | Beberapa error | Tidak bisa run |
| **Variasi Input** | Demo dengan berbagai input | Beberapa variasi | Input tunggal | Tidak ada variasi |
| **Troubleshooting** | Menjelaskan error handling | Sedikit troubleshooting | Tidak ada | - |

### 3. Kualitas Presentasi (20%)

| Kriteria | Excellent (18-20) | Good (14-17) | Fair (10-13) | Poor (0-9) |
|----------|------------------|--------------|--------------|------------|
| **Kejelasan Audio** | Suara jernih, volume konsisten | Cukup jelas | Kadang tidak jelas | Sulit didengar |
| **Kecepatan Bicara** | Pace tepat, mudah diikuti | Sedikit cepat/lambat | Terlalu cepat/lambat | Sangat sulit diikuti |
| **Bahasa** | Bahasa Indonesia baku, lancar | Cukup baik | Ada grammatical error | Sulit dipahami |
| **Kepercayaan Diri** | Percaya diri, natural | Cukup percaya diri | Nervous, banyak filler | Sangat nervous |

### 4. Kualitas Teknis Video (10%)

| Kriteria | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|----------|-----------------|------------|------------|------------|
| **Resolusi** | 1080p atau lebih | 720p | 480p | Lebih rendah |
| **Stabilitas** | Video stabil, tidak goyang | Minor shaking | Cukup goyang | Sangat tidak stabil |
| **Lighting** | Pencahayaan baik, wajah terlihat jelas | Cukup terang | Agak gelap | Terlalu gelap/terang |
| **Editing** | Transisi smooth, zoom tepat | Editing cukup | Minimal editing | Tidak ada editing |

### 5. Kreativitas dan Orisinalitas (5%)

| Kriteria | Excellent (5) | Good (4) | Fair (3) | Poor (0-2) |
|----------|--------------|----------|----------|------------|
| **Pendekatan Unik** | Penjelasan kreatif, analogi menarik | Cukup kreatif | Standar | Copy-paste |
| **Contoh Original** | Contoh kasus sendiri | Modifikasi contoh | Contoh dari referensi | Tidak ada contoh |

---

## ⏱️ Panduan Durasi per Bagian

| Bagian | Durasi | Konten |
|--------|--------|--------|
| Intro | 30-60 detik | Perkenalan, judul |
| Teori Stereo | 2-3 menit | Disparity, depth formula |
| Algoritma | 2-3 menit | BM, SGM, parameter |
| Demo Kode | 2-3 menit | Running, output |
| Analisis | 1-2 menit | Perbandingan, kualitas |
| Penutup | 30-60 detik | Kesimpulan |

---

## 📝 Poin Penalti

| Pelanggaran | Penalti |
|-------------|---------|
| Durasi < 5 menit | -20% |
| Durasi > 12 menit | -10% |
| Tidak ada demonstrasi kode | -30% |
| Audio tidak ada/tidak jelas | -25% |
| Plagiarisme konten | Nilai 0 |
| Terlambat submit | -10% per hari (max 3 hari) |

---

## 🏆 Bonus Poin (Maksimal +10%)

| Achievement | Bonus |
|-------------|-------|
| Subtitle/CC disediakan | +3% |
| Perbandingan lebih dari 2 metode | +3% |
| Implementasi real-time demo | +5% |
| Analisis depth accuracy kuantitatif | +4% |
| Penjelasan hardware stereo (ZED, RealSense) | +2% |

---

## 📊 Konversi Nilai Akhir

| Total Skor | Nilai |
|------------|-------|
| 95-100+ | A (dengan bonus) |
| 90-94 | A |
| 85-89 | A- |
| 80-84 | B+ |
| 75-79 | B |
| 70-74 | B- |
| 65-69 | C+ |
| 60-64 | C |
| 55-59 | D |
| < 55 | E |

---

## 📌 Contoh Outline Video yang Baik

```
00:00 - 00:30  Intro dan perkenalan
00:30 - 01:30  Apa itu depth estimation?
01:30 - 02:30  Konsep stereo vision dan disparity
02:30 - 03:30  Rumus depth = (f × B) / d
03:30 - 04:30  Algoritma Block Matching
04:30 - 05:30  Algoritma SGM dan perbandingan
05:30 - 06:30  Demo kode stereo matching
06:30 - 07:30  Analisis output dan parameter tuning
07:30 - 08:30  Demo monocular depth (MiDaS)
08:30 - 09:00  Kesimpulan dan penutup
```

---

## ⚠️ Catatan Penting

1. **Upload**: Upload ke platform yang ditentukan (Google Drive/YouTube unlisted)
2. **Nama File**: `Bab12_NIM_NamaLengkap.mp4`
3. **Deadline**: Sesuai jadwal yang diberikan
4. **Link Sharing**: Pastikan link bisa diakses oleh penilai
