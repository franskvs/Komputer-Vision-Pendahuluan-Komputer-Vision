# Rubrik Penilaian Tugas Video
## Bab 4: Model Fitting dan Feature Matching

### Informasi Umum
- **Total Nilai**: 100 poin
- **Durasi Video**: 5-10 menit
- **Format**: MP4 atau link YouTube (unlisted/public)
- **Deadline**: 1 minggu setelah praktikum

---

## A. Komponen Penilaian

### 1. Demonstrasi Program (30 poin)

| Nilai | Kriteria |
|-------|----------|
| 27-30 | Demonstrasi lengkap SEMUA 8 program praktikum. Setiap program dijalankan dan output ditunjukkan dengan jelas. Variasi parameter didemonstrasikan. |
| 22-26 | Demonstrasi 6-7 program dengan baik. Output jelas dan parameter variation ditunjukkan. |
| 17-21 | Demonstrasi 4-5 program. Output visible tapi kurang detail. |
| 12-16 | Demonstrasi 2-3 program saja. Penjelasan minimal. |
| 0-11 | Demonstrasi sangat minim atau tidak lengkap. |

**Program yang WAJIB didemonstrasikan:**
- [ ] 01_feature_detection.py - Perbandingan minimal 3 detector
- [ ] 02_feature_matching.py - BF dan FLANN comparison
- [ ] 03_ransac.py - Visualisasi RANSAC vs Least Squares
- [ ] 04_hough_lines.py - Deteksi garis
- [ ] 05_hough_circles.py - Deteksi lingkaran
- [ ] 06_homography.py - Estimasi homography
- [ ] 07_perspective_correction.py - Document scanning
- [ ] 08_optical_flow.py - Sparse dan Dense flow

### 2. Penjelasan Konsep (25 poin)

| Nilai | Kriteria |
|-------|----------|
| 23-25 | Penjelasan konsep sangat jelas dan mendalam. Mampu menjelaskan teori matematis di balik setiap algoritma. Memberikan insight dan intuisi yang baik. |
| 18-22 | Penjelasan konsep baik. Memahami prinsip dasar dan dapat menjelaskan dengan bahasa sendiri. |
| 13-17 | Penjelasan cukup. Memahami konsep dasar tapi kurang mendalam. |
| 8-12 | Penjelasan minimal. Terkesan membaca dari sumber tanpa pemahaman. |
| 0-7 | Tidak ada penjelasan konsep atau sangat tidak akurat. |

**Konsep yang HARUS dijelaskan:**
- [ ] Apa itu feature dan mengapa penting untuk matching
- [ ] Perbedaan feature detector (Harris, FAST, ORB, SIFT, AKAZE)
- [ ] Bagaimana RANSAC bekerja dan keuntungannya
- [ ] Prinsip Hough Transform untuk deteksi garis/lingkaran
- [ ] Apa itu homography matrix dan aplikasinya
- [ ] Konsep optical flow dan brightness constancy assumption
- [ ] Perbedaan sparse vs dense optical flow

### 3. Analisis dan Eksperimen (20 poin)

| Nilai | Kriteria |
|-------|----------|
| 18-20 | Melakukan eksperimen dengan variasi parameter yang systematic. Menganalisis pengaruh perubahan parameter. Memberikan rekomendasi parameter untuk berbagai kondisi. |
| 14-17 | Melakukan beberapa eksperimen dengan variasi parameter. Ada analisis sederhana. |
| 10-13 | Eksperimen minimal. Hanya menjalankan dengan default parameter. |
| 6-9 | Sangat sedikit eksperimen. Tidak ada analisis. |
| 0-5 | Tidak ada eksperimen sama sekali. |

**Eksperimen yang DIHARAPKAN:**
- [ ] Variasi parameter feature detector (nfeatures, threshold)
- [ ] Perbandingan akurasi dan kecepatan berbagai detector
- [ ] Pengaruh ratio threshold pada feature matching
- [ ] Pengaruh RANSAC threshold pada homography estimation
- [ ] Pengaruh parameter Hough pada deteksi garis/lingkaran
- [ ] Perbandingan Lucas-Kanade vs Farneback optical flow

### 4. Kualitas Video & Presentasi (15 poin)

| Nilai | Kriteria |
|-------|----------|
| 14-15 | Video berkualitas tinggi. Audio jelas. Layar terlihat dengan baik. Editing rapi. Durasi sesuai (5-10 menit). Pembukaan dan penutup profesional. |
| 11-13 | Video berkualitas baik. Audio dan visual cukup jelas. Editing acceptable. |
| 8-10 | Video cukup. Ada noise audio atau visual kurang jelas di beberapa bagian. |
| 5-7 | Video kurang berkualitas. Audio sulit didengar atau layar sulit dilihat. |
| 0-4 | Video sangat buruk atau tidak dapat diputar. |

**Checklist Kualitas:**
- [ ] Resolusi minimal 720p
- [ ] Audio jelas tanpa background noise berlebih
- [ ] Code dan output terlihat jelas (font cukup besar)
- [ ] Tidak ada bagian yang terpotong
- [ ] Durasi 5-10 menit

### 5. Kreativitas dan Insight (10 poin)

| Nilai | Kriteria |
|-------|----------|
| 9-10 | Memberikan insight unik atau aplikasi kreatif. Menunjukkan pemahaman mendalam dengan analogi atau visualisasi yang menarik. Menghubungkan dengan aplikasi real-world. |
| 7-8 | Ada beberapa insight menarik atau aplikasi tambahan yang relevan. |
| 5-6 | Kreativitas standar. Mengikuti instruksi dengan baik. |
| 3-4 | Sangat standar. Tidak ada nilai tambah. |
| 0-2 | Tidak ada kreativitas sama sekali. |

**Bonus Kreativitas:**
- [ ] Demo dengan data sendiri (foto/video sendiri)
- [ ] Aplikasi ke real-world problem
- [ ] Perbandingan dengan library/method lain
- [ ] Visualisasi tambahan yang informatif
- [ ] Tips dan tricks dari pengalaman

---

## B. Struktur Video yang Direkomendasikan

### Timeline Ideal (8 menit):

```
0:00 - 0:30   Pembukaan & Perkenalan
0:30 - 2:00   Feature Detection (01) - Demo & Penjelasan
2:00 - 3:00   Feature Matching (02) - Demo & Penjelasan
3:00 - 3:45   RANSAC (03) - Demo & Penjelasan
3:45 - 4:30   Hough Lines & Circles (04, 05) - Demo
4:30 - 5:30   Homography & Perspective Correction (06, 07) - Demo
5:30 - 6:30   Optical Flow (08) - Demo & Penjelasan
6:30 - 7:30   Eksperimen & Analisis
7:30 - 8:00   Kesimpulan & Penutup
```

### Skrip Pembukaan Contoh:
```
"Assalamualaikum/Selamat pagi/siang/malam,
Nama saya [NAMA], NIM [NIM].
Pada video ini saya akan mendemonstrasikan praktikum Computer Vision
Bab 4 tentang Model Fitting dan Feature Matching.
Materi ini mencakup feature detection, matching, RANSAC, 
Hough Transform, homography, dan optical flow.
Mari kita mulai dengan feature detection..."
```

### Skrip Penutup Contoh:
```
"Demikian demonstrasi praktikum Bab 4 Model Fitting.
Kesimpulan utama dari praktikum ini adalah:
1. Feature detection penting untuk image matching
2. RANSAC membuat estimasi robust terhadap outliers
3. Hough Transform powerful untuk deteksi shapes
4. Homography enables perspective transformation
5. Optical flow untuk motion analysis

Terima kasih atas perhatiannya.
Wassalamualaikum/Sekian dan terima kasih."
```

---

## C. Checklist Sebelum Submit

### Konten:
- [ ] Semua 8 program didemonstrasikan
- [ ] Setiap program berjalan tanpa error
- [ ] Output terlihat jelas
- [ ] Penjelasan konsep untuk setiap topik
- [ ] Minimal 3 eksperimen variasi parameter

### Teknis:
- [ ] Durasi 5-10 menit
- [ ] Resolusi minimal 720p
- [ ] Audio jelas
- [ ] File dapat diputar (test dulu sebelum submit)
- [ ] Ukuran file reasonable (<500MB untuk upload)

### Format Submission:
- Nama file: `NIM_Nama_Bab4_Video.mp4`
- Atau link YouTube dengan format: `NIM_Nama_Bab4_LinkVideo.txt`

---

## D. Contoh Penilaian

### Contoh Nilai A (90):
```
Demonstrasi Program:    28/30 (Lengkap, jelas)
Penjelasan Konsep:      23/25 (Mendalam, paham)
Analisis & Eksperimen:  17/20 (Banyak variasi)
Kualitas Video:         14/15 (Profesional)
Kreativitas:             8/10 (Demo dengan data sendiri)
Total:                  90/100
```

### Contoh Nilai B (75):
```
Demonstrasi Program:    22/30 (6 program)
Penjelasan Konsep:      18/25 (Cukup baik)
Analisis & Eksperimen:  14/20 (Beberapa eksperimen)
Kualitas Video:         12/15 (Baik)
Kreativitas:             9/10 (Aplikasi menarik)
Total:                  75/100
```

### Contoh Nilai C (65):
```
Demonstrasi Program:    18/30 (5 program, kurang detail)
Penjelasan Konsep:      15/25 (Basic)
Analisis & Eksperimen:  12/20 (Minimal)
Kualitas Video:         12/15 (Cukup)
Kreativitas:             8/10 (Standar plus sedikit)
Total:                  65/100
```

---

## E. Tips untuk Video Berkualitas

### Recording:
1. Gunakan screen recorder yang baik (OBS, Camtasia, atau built-in)
2. Set resolusi minimal 1080p saat recording
3. Gunakan microphone external jika memungkinkan
4. Record di ruangan yang tenang
5. Close unnecessary applications untuk performance

### Presentation:
1. Latihan dulu sebelum recording
2. Siapkan skrip atau bullet points
3. Bicara dengan pace yang tidak terlalu cepat
4. Pause sebentar saat menunjukkan output penting
5. Zoom in pada code atau output yang penting

### Editing:
1. Cut bagian yang tidak perlu (loading, error yang diperbaiki)
2. Add text annotations jika perlu
3. Normalize audio levels
4. Add intro/outro slides
5. Review seluruh video sebelum export

### Code Display:
1. Increase font size di IDE (minimal 14pt)
2. Gunakan tema dengan kontras tinggi
3. Highlight line yang sedang dibahas
4. Show output di window yang visible

---

## F. Penalti

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Video > 15 menit | -5 poin |
| Video < 3 menit | -15 poin |
| Late submission (per hari) | -5 poin |
| Plagiarism (copy video orang) | Nilai 0 |
| Video tidak dapat dibuka | Tidak dinilai (resubmit) |
| Audio tidak ada | -20 poin |
| Program tidak berjalan | -10 poin per program |

---

## G. FAQ

**Q: Boleh menggunakan bahasa Inggris?**
A: Boleh, tapi bahasa Indonesia lebih diutamakan.

**Q: Apakah harus menunjukkan wajah?**
A: Tidak wajib, tapi direkomendasikan untuk intro dan outro.

**Q: Boleh edit video?**
A: Sangat dianjurkan untuk hasil yang lebih profesional.

**Q: Bagaimana jika program error saat recording?**
A: Edit bagian tersebut atau record ulang bagian itu saja.

**Q: Boleh menggunakan slide/PPT?**
A: Boleh untuk menjelaskan konsep, tapi mayoritas harus demo live.

**Q: Maksimal berapa kali boleh submit?**
A: 1 kali, pastikan sudah final sebelum submit.
