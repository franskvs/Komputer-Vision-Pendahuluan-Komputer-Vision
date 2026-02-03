# Rubrik Penilaian Tugas Video - Bab 3
## Pemrosesan Citra (Image Processing)

### Informasi Umum
- **Mata Kuliah:** Praktikum Computer Vision
- **Bab:** 3 - Pemrosesan Citra
- **Bobot Tugas Video:** 20% dari nilai Bab 3
- **Sifat:** Individu
- **Durasi Video:** 8-12 menit

---

## A. Spesifikasi Video

### Durasi dan Format
| Aspek | Requirement |
|-------|-------------|
| Durasi | 8-12 menit (toleransi ±1 menit) |
| Resolusi | Minimal 720p (1280x720) |
| Format | MP4 atau MKV |
| Audio | Jelas, tanpa noise berlebihan |
| Bahasa | Indonesia |

### Struktur Video yang Diharapkan

```
Timeline Video (10 menit):
├── 0:00-0:30  │ Pembukaan (perkenalan, topik)
├── 0:30-2:00  │ Penjelasan Konsep Teori
├── 2:00-4:00  │ Demo Program 1-2
├── 4:00-6:00  │ Demo Program 3-4
├── 6:00-8:00  │ Demo Program 5-6 atau Eksperimen
├── 8:00-9:00  │ Analisis dan Insight
└── 9:00-10:00 │ Kesimpulan dan Penutup
```

---

## B. Komponen Penilaian

### 1. Konten Teknis (40 poin)

| Kriteria | Excellent (36-40) | Good (28-35) | Satisfactory (20-27) | Needs Improvement (0-19) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Penjelasan Point Operations** | Menjelaskan brightness, contrast, gamma dengan formula dan visualisasi | Menjelaskan 2-3 operasi dengan benar | Penjelasan dasar | Tidak menjelaskan atau salah |
| **Demo Histogram Operations** | Demo equalization dan CLAHE dengan analisis histogram | Demo keduanya tanpa analisis mendalam | Demo salah satu | Tidak ada demo |
| **Demo Spatial Filtering** | Perbandingan filters dengan berbagai parameter | Demo 2-3 filter dengan parameter | Demo 1-2 filter | Tidak ada demo |
| **Demo Edge Detection** | Perbandingan Sobel, Laplacian, Canny dengan parameter tuning | Demo 2 metode dengan parameter | Demo 1 metode | Tidak ada demo |
| **Demo Morfologi** | Demo erosion, dilation, opening, closing dengan aplikasi | Demo 3 operasi | Demo 1-2 operasi | Tidak ada demo |

**Checklist Konten (harus ada di video):**

**Point Operations:**
- [ ] Demo brightness adjustment dengan berbagai nilai
- [ ] Demo contrast adjustment
- [ ] Demo gamma correction dengan visualisasi kurva
- [ ] Demo thresholding (binary, Otsu, adaptive)
- [ ] Perbandingan hasil dengan histogram

**Histogram Operations:**
- [ ] Demo cv2.equalizeHist()
- [ ] Demo CLAHE dengan variasi clip limit
- [ ] Demo CLAHE dengan variasi tile size
- [ ] Visualisasi histogram sebelum dan sesudah
- [ ] Penjelasan kapan menggunakan masing-masing

**Spatial Filtering:**
- [ ] Demo Gaussian blur
- [ ] Demo Median filter (untuk salt-pepper noise)
- [ ] Demo Bilateral filter (edge-preserving)
- [ ] Demo Unsharp masking (sharpening)
- [ ] Perbandingan efek kernel size

**Edge Detection:**
- [ ] Demo Sobel X dan Y
- [ ] Demo gradient magnitude
- [ ] Demo Canny dengan parameter tuning
- [ ] Penjelasan double thresholding
- [ ] Demo Laplacian

**Morfologi:**
- [ ] Demo erosion dengan iterasi berbeda
- [ ] Demo dilation
- [ ] Demo opening (noise removal)
- [ ] Demo closing (hole filling)
- [ ] Demo morphological gradient

---

### 2. Eksperimen dan Analisis (25 poin)

| Kriteria | Excellent (23-25) | Good (18-22) | Satisfactory (13-17) | Needs Improvement (0-12) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Variasi Parameter** | Mencoba 3+ variasi untuk setiap teknik dan menganalisis hasilnya | 2 variasi per teknik dengan analisis | 1 variasi per teknik | Tidak ada variasi |
| **Perbandingan Metode** | Perbandingan sistematis 3+ metode untuk masalah yang sama | Perbandingan 2 metode | Perbandingan sederhana | Tidak ada perbandingan |
| **Analisis Hasil** | Analisis mendalam mengapa suatu metode lebih baik | Analisis umum | Observasi tanpa analisis | Tidak ada analisis |
| **Insight dan Rekomendasi** | Memberikan rekomendasi kapan menggunakan teknik mana | Insight sederhana | Minimal insight | Tidak ada insight |

**Checklist Eksperimen:**
- [ ] Eksperimen dengan gambar gelap (underexposed)
- [ ] Eksperimen dengan gambar terang (overexposed)
- [ ] Eksperimen dengan gambar low contrast
- [ ] Eksperimen dengan gambar noisy
- [ ] Analisis trade-off (misal: blur vs detail preservation)
- [ ] Rekomendasi teknik untuk berbagai kondisi

---

### 3. Kualitas Presentasi (20 poin)

| Kriteria | Excellent (18-20) | Good (14-17) | Satisfactory (10-13) | Needs Improvement (0-9) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Narasi** | Jelas, terstruktur, mudah diikuti | Cukup jelas dengan minor issues | Bisa diikuti tapi kurang terstruktur | Sulit diikuti |
| **Visual** | Screen recording jelas, zoom ke area penting, annotations | Recording jelas, beberapa annotations | Recording bisa dilihat | Kualitas visual buruk |
| **Pace** | Tempo tepat, tidak terlalu cepat/lambat | Umumnya baik, kadang terlalu cepat | Pace tidak konsisten | Terlalu cepat atau lambat |
| **Engagement** | Menarik, antusias, contoh relatable | Cukup engaging | Monoton tapi informatif | Membosankan |

---

### 4. Kualitas Teknis Video (15 poin)

| Kriteria | Excellent (14-15) | Good (11-13) | Satisfactory (8-10) | Needs Improvement (0-7) |
|----------|-------------------|--------------|----------------------|--------------------------|
| **Audio** | Jelas, tanpa noise, volume konsisten | Jelas dengan sedikit noise | Bisa didengar tapi ada gangguan | Sulit didengar |
| **Video** | Resolusi tinggi, smooth, tidak lag | Resolusi baik, minor lag | Resolusi rendah tapi watchable | Kualitas buruk |
| **Editing** | Professional, transisi smooth, timestamps | Editing rapi | Editing minimal | Tidak ada editing |

---

## C. Bonus Points (Maksimal +10)

| Bonus | Poin |
|-------|------|
| Implementasi pipeline lengkap (enhancement workflow) | +5 |
| Demo aplikasi real-world (medical, satellite, dll) | +3 |
| Perbandingan dengan software komersial (Photoshop, GIMP) | +2 |
| Visualisasi interaktif (slider untuk parameter) | +2 |
| Thumbnail dan intro yang profesional | +1 |
| Subtitles/closed captions | +1 |

---

## D. Penalti

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Durasi < 7 menit | -10 |
| Durasi > 14 menit | -5 |
| Tidak ada demo code | -20 |
| Audio tidak dapat didengar | -15 |
| Plagiarisme (video orang lain) | -100 |
| Terlambat submit (per hari) | -5 per hari |
| Hanya screen recording tanpa narasi | -15 |
| Tidak menggunakan teknik dari materi | -10 |

---

## E. Perhitungan Nilai Akhir

```
Nilai Akhir = Konten (40) + Eksperimen (25) + Presentasi (20) + Teknis (15) + Bonus - Penalti
              ----------------------------------------------------------------------------------
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

## F. Format Pengumpulan

### Nama File
```
Bab3_Video_NIM_Nama.mp4
```

### Yang Harus Dikumpulkan
1. **Video** (MP4/MKV)
2. **Source Code** yang digunakan dalam demo (ZIP)
3. **Sample Images** yang digunakan

### Platform Upload
- YouTube (Unlisted) dengan link submit ke LMS
- atau Google Drive dengan akses terbuka
- atau langsung ke LMS (jika ukuran < 500MB)

---

## G. Contoh Skenario Demo yang Baik

### Skenario 1: "Memperbaiki Foto Gelap"
```
1. Tunjukkan foto underexposed
2. Analisis histogram (skewed ke kiri)
3. Coba brightness adjustment → jelaskan limitasi
4. Coba gamma correction → jelaskan kenapa lebih baik
5. Coba histogram equalization → analisis hasil
6. Coba CLAHE → bandingkan dengan equalization
7. Kesimpulan: kapan pakai masing-masing
```

### Skenario 2: "Menghilangkan Noise"
```
1. Tunjukkan foto noisy (Gaussian noise)
2. Coba Average filter → blur edges
3. Coba Gaussian filter → masih blur
4. Coba Median filter → tidak cocok untuk Gaussian
5. Coba Bilateral filter → edge-preserving
6. Coba fastNlMeansDenoising → best result
7. Kesimpulan: trade-off antara noise removal dan detail
```

### Skenario 3: "Pipeline Enhancement"
```
1. Mulai dengan gambar "bermasalah"
2. Step 1: Denoise (jelaskan kenapa pertama)
3. Step 2: CLAHE (adaptive contrast)
4. Step 3: Gamma correction (brightness fine-tune)
5. Step 4: Saturation adjustment
6. Step 5: Sharpening (jelaskan kenapa terakhir)
7. Before-after comparison
8. Analisis histogram setiap step
```

---

## H. Tips untuk Mendapat Nilai Tinggi

### DO:
- ✅ Siapkan script sebelum recording
- ✅ Gunakan zoom untuk menunjukkan detail
- ✅ Jelaskan "kenapa" bukan hanya "apa"
- ✅ Gunakan gambar yang jelas menunjukkan efek
- ✅ Berikan timestamps di description
- ✅ Test audio dan video sebelum upload

### DON'T:
- ❌ Membaca langsung dari slide
- ❌ Demo tanpa penjelasan
- ❌ Skip parameter tuning
- ❌ Menggunakan gambar yang tidak menunjukkan efek jelas
- ❌ Recording terlalu panjang tanpa editing
- ❌ Audio terlalu pelan atau terlalu keras

---

## I. Topik Opsional untuk Nilai Bonus

1. **Medical Image Enhancement**
   - Demo dengan X-ray atau MRI images
   - Fokus pada CLAHE dan edge enhancement

2. **Document Image Processing**
   - Adaptive thresholding untuk OCR prep
   - Morphology untuk noise removal

3. **Satellite Image Processing**
   - Band processing
   - Enhancement untuk analisis

4. **Photo Editing Workflow**
   - Replicate Instagram filters
   - Comparison dengan Photoshop

---

*Rubrik ini dapat disesuaikan berdasarkan kesepakatan dengan dosen pengampu*
