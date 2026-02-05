# JOBSHEET PRAKTIKUM
# BAB 7: DETEKSI FITUR DAN PENCOCOKAN

---

## 📋 INFORMASI PRAKTIKUM
| Item | Keterangan |
|------|------------|
| Mata Kuliah | Praktikum Computer Vision |
| Materi | Deteksi Fitur dan Pencocokan |
| Pertemuan | Bab 7 |
| Waktu | 150 menit |

---

## 1. TUJUAN PRAKTIKUM

### 1.1 Tujuan Umum
Mahasiswa mampu memahami dan mengimplementasikan teknik deteksi fitur serta pencocokan fitur pada citra digital.

### 1.2 Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan |
|----|-----------|--------|
| 1 | Harris Corner Detection | Mendeteksi sudut/corner menggunakan metode Harris dengan memahami pengaruh parameter blockSize dan k |
| 2 | Shi-Tomasi Corner Detection | Membandingkan metode Shi-Tomasi dengan Harris untuk tracking fitur |
| 3 | SIFT Feature Detection | Mengekstrak fitur invariant terhadap skala dan rotasi |
| 4 | ORB Feature Detection | Mengimplementasikan deteksi fitur yang cepat dan gratis |
| 5 | Feature Matching Brute Force | Mencocokkan fitur antara dua gambar dengan metode brute-force |
| 6 | Feature Matching FLANN | Menggunakan FLANN untuk matching yang lebih efisien |
| 7 | Homography dengan RANSAC | Mengestimasi transformasi perspektif dengan filtering outlier |
| 8 | Aplikasi Nyata: Document Scanner | Menerapkan homography untuk koreksi perspektif dokumen |
| 9 | AKAZE Feature Detection | Menyeimbangkan kecepatan dan akurasi deteksi fitur |
| 10 | FAST Feature Detection | Mendeteksi keypoint sangat cepat untuk aplikasi real-time |

---

## 2. ALAT DAN BAHAN

### 2.1 Perangkat Keras
| No | Alat | Spesifikasi Minimum |
|----|------|---------------------|
| 1 | Komputer/Laptop | RAM 8GB, Processor i5 atau setara |
| 2 | Webcam (opsional) | Resolusi 720p |
| 3 | Mouse dan Keyboard | Standard |

### 2.2 Perangkat Lunak
| No | Software | Versi |
|----|----------|-------|
| 1 | Python | 3.8+ |
| 2 | OpenCV | 4.5+ |
| 3 | NumPy | 1.19+ |
| 4 | Matplotlib | 3.3+ |
| 5 | VS Code / PyCharm | Terbaru |

### 2.3 Bahan Praktikum
| No | Bahan | Keterangan |
|----|-------|------------|
| 1 | Gambar `checkerboard.png` | Untuk deteksi corner |
| 2 | Gambar `building.jpg` | Objek dengan fitur jelas |
| 3 | Gambar `object1.jpg` dan `object2.jpg` | Pasangan untuk matching |
| 4 | Script Python praktikum | 10 file program |

---

## 3. LANGKAH KERJA

### 3.1 Persiapan Environment

#### Langkah 1: Instalasi Dependencies
```bash
# Buka terminal/command prompt
cd "Praktikum Komputer Vision"

# Install requirements
pip install -r requirements.txt
```

#### Langkah 2: Verifikasi Instalasi
```python
import cv2
import numpy as np
print(f"OpenCV Version: {cv2.__version__}")
print(f"NumPy Version: {np.__version__}")
```

#### Langkah 3: Download Data Sampel
```bash
cd Bab-07-Deteksi-Fitur-dan-Pencocokan
python download_sample_data.py
```

#### Langkah 4: Struktur Folder
Pastikan struktur folder seperti berikut:
```
Bab-07-Deteksi-Fitur-dan-Pencocokan/
├── praktikum/
│   ├── 01_harris_corner.py
│   ├── 02_shi_tomasi.py
│   ├── 03_sift_detection.py
│   ├── 04_orb_detection.py
│   ├── 05_bf_matching.py
│   ├── 06_flann_matching.py
│   ├── 07_homography_ransac.py
│   └── output/
├── data/
│   └── images/
└── download_sample_data.py
```

---

### 3.2 Pelaksanaan Percobaan

#### PERCOBAAN 1: Harris Corner Detection

**Langkah-langkah:**
1. Buka file `01_harris_corner.py`
2. Pelajari kode dan parameter yang ada
3. Jalankan program:
   ```bash
   python praktikum/01_harris_corner.py
   ```
4. Amati output di folder `output/`
5. **Variasi Parameter:**
   - Ubah `BLOCK_SIZE` dari 2 ke 5, 7
   - Ubah `K_VALUE` dari 0.04 ke 0.06, 0.08
   - Catat perubahan yang terjadi

#### PERCOBAAN 2: Shi-Tomasi Corner Detection

**Langkah-langkah:**
1. Buka file `02_shi_tomasi.py`
2. Jalankan program:
   ```bash
   python praktikum/02_shi_tomasi.py
   ```
3. **Variasi Parameter:**
   - Ubah `MAX_CORNERS` dari 100 ke 50, 200
   - Ubah `QUALITY_LEVEL` dari 0.01 ke 0.05, 0.1
   - Ubah `MIN_DISTANCE` dari 10 ke 5, 20

#### PERCOBAAN 3: SIFT Feature Detection

**Langkah-langkah:**
1. Buka file `03_sift_detection.py`
2. Jalankan program:
   ```bash
   python praktikum/03_sift_detection.py
   ```
3. **Variasi Parameter:**
   - Ubah `N_FEATURES` dari 500 ke 100, 1000
   - Ubah `CONTRAST_THRESHOLD` dari 0.04 ke 0.02, 0.08
   - Amati keypoint dengan berbagai ukuran

#### PERCOBAAN 4: ORB Feature Detection

**Langkah-langkah:**
1. Buka file `04_orb_detection.py`
2. Jalankan program:
   ```bash
   python praktikum/04_orb_detection.py
   ```
3. **Variasi Parameter:**
   - Ubah `N_FEATURES` dari 500 ke 1000, 2000
   - Ubah `SCALE_FACTOR` dari 1.2 ke 1.1, 1.5
   - Ubah `N_LEVELS` dari 8 ke 4, 12

#### PERCOBAAN 5: Brute-Force Matching

**Langkah-langkah:**
1. Siapkan dua gambar yang mirip (sudut berbeda)
2. Buka file `05_bf_matching.py`
3. Jalankan program:
   ```bash
   python praktikum/05_bf_matching.py
   ```
4. **Variasi Parameter:**
   - Ubah `RATIO_THRESHOLD` dari 0.75 ke 0.5, 0.9
   - Bandingkan jumlah match yang dihasilkan

#### PERCOBAAN 6: FLANN Matching

**Langkah-langkah:**
1. Buka file `06_flann_matching.py`
2. Jalankan program:
   ```bash
   python praktikum/06_flann_matching.py
   ```
3. Bandingkan waktu eksekusi dengan Brute-Force

#### PERCOBAAN 7: Homography dengan RANSAC

**Langkah-langkah:**
1. Buka file `07_homography_ransac.py`
2. Jalankan program:
   ```bash
   python praktikum/07_homography_ransac.py
   ```
3. Amati:
   - Jumlah inlier vs outlier
   - Hasil transformasi perspektif
   - Akurasi alignment

#### PERCOBAAN 8: Aplikasi Nyata - Document Scanner

**Langkah-langkah:**
1. Buka file `08_real_world_example.py`
2. Jalankan program:
   ```bash
   python praktikum/08_real_world_example.py
   ```
3. Amati:
   - Deteksi sudut dokumen
   - Koreksi perspektif (warping)
   - Hasil "scan" dokumen

#### PERCOBAAN 9: AKAZE Feature Detection

**Langkah-langkah:**
1. Buka file `09_akaze_detection.py`
2. Jalankan program:
   ```bash
   python praktikum/09_akaze_detection.py
   ```
3. Amati:
   - Jumlah keypoint pada berbagai gambar
   - Perbandingan dengan ORB/SIFT

#### PERCOBAAN 10: FAST Feature Detection

**Langkah-langkah:**
1. Buka file `10_fast_detection.py`
2. Jalankan program:
   ```bash
   python praktikum/10_fast_detection.py
   ```
3. Amati:
   - Pengaruh threshold terhadap jumlah keypoint
   - Perbandingan speed dengan algoritma lain

---

## 4. DATA PENGAMATAN

### 4.1 Tabel Pengamatan Percobaan 1 (Harris Corner)

| Parameter | Nilai | Jumlah Corner | Waktu (ms) | Observasi |
|-----------|-------|---------------|------------|-----------|
| blockSize=2, k=0.04 | Default | ... | ... | ... |
| blockSize=5, k=0.04 | Variasi 1 | ... | ... | ... |
| blockSize=7, k=0.04 | Variasi 2 | ... | ... | ... |
| blockSize=2, k=0.06 | Variasi 3 | ... | ... | ... |
| blockSize=2, k=0.08 | Variasi 4 | ... | ... | ... |

### 4.2 Tabel Pengamatan Percobaan 2 (Shi-Tomasi)

| max_corners | quality_level | min_distance | Jumlah Terdeteksi | Distribusi |
|-------------|---------------|--------------|-------------------|------------|
| 100 | 0.01 | 10 | ... | ... |
| 50 | 0.01 | 10 | ... | ... |
| 200 | 0.01 | 10 | ... | ... |
| 100 | 0.05 | 10 | ... | ... |
| 100 | 0.01 | 20 | ... | ... |

### 4.3 Tabel Pengamatan Percobaan 3 (SIFT)

| n_features | contrast_threshold | Keypoints | Waktu (ms) | Ukuran Descriptor |
|------------|--------------------|-----------|-----------| ------------------|
| 500 | 0.04 | ... | ... | 128 dimensi |
| 100 | 0.04 | ... | ... | 128 dimensi |
| 1000 | 0.04 | ... | ... | 128 dimensi |
| 500 | 0.02 | ... | ... | 128 dimensi |
| 500 | 0.08 | ... | ... | 128 dimensi |

### 4.4 Tabel Pengamatan Percobaan 4 (ORB)

| n_features | scale_factor | n_levels | Keypoints | Waktu (ms) |
|------------|--------------|----------|-----------|------------|
| 500 | 1.2 | 8 | ... | ... |
| 1000 | 1.2 | 8 | ... | ... |
| 500 | 1.1 | 8 | ... | ... |
| 500 | 1.5 | 8 | ... | ... |
| 500 | 1.2 | 12 | ... | ... |

### 4.5 Tabel Perbandingan Feature Matching

| Metode | Ratio Threshold | Total Matches | Good Matches | Waktu (ms) |
|--------|-----------------|---------------|--------------|------------|
| BF + ORB | 0.75 | ... | ... | ... |
| BF + SIFT | 0.75 | ... | ... | ... |
| FLANN + SIFT | 0.75 | ... | ... | ... |
| FLANN + ORB | 0.75 | ... | ... | ... |

### 4.6 Tabel Pengamatan RANSAC

| Jumlah Matches | Threshold | Inliers | Outliers | Akurasi Homography |
|----------------|-----------|---------|----------|-------------------|
| ... | 5.0 | ... | ... | ... |
| ... | 3.0 | ... | ... | ... |
| ... | 10.0 | ... | ... | ... |

---

## 5. ANALISIS

### 5.1 Panduan Analisis Percobaan 1-2 (Corner Detection)

Jawab pertanyaan berikut:
1. **Pengaruh blockSize:** Apa yang terjadi pada jumlah corner ketika blockSize diperbesar?
2. **Pengaruh k (Harris):** Bagaimana nilai k mempengaruhi sensitivitas deteksi?
3. **Perbedaan Harris vs Shi-Tomasi:** Algoritma mana yang menghasilkan distribusi corner lebih merata?
4. **Trade-off:** Apa trade-off antara sensitivitas dan noise?

### 5.2 Panduan Analisis Percobaan 3-4 (Feature Detection)

Jawab pertanyaan berikut:
1. **SIFT vs ORB:** Bandingkan kecepatan dan jumlah fitur yang terdeteksi
2. **Scale Invariance:** Apakah fitur yang sama terdeteksi pada gambar yang di-zoom?
3. **Rotation Invariance:** Apakah fitur tetap terdeteksi pada gambar yang dirotasi?
4. **Distribusi Fitur:** Di bagian gambar mana fitur paling banyak terdeteksi? Mengapa?

### 5.3 Panduan Analisis Percobaan 5-6 (Matching)

Jawab pertanyaan berikut:
1. **Ratio Test:** Mengapa ratio test penting? Apa yang terjadi tanpanya?
2. **BF vs FLANN:** Kapan sebaiknya menggunakan masing-masing metode?
3. **False Matches:** Karakteristik seperti apa yang menyebabkan false match?
4. **Optimal Threshold:** Berapa ratio threshold optimal untuk dataset Anda?

### 5.4 Panduan Analisis Percobaan 7 (RANSAC)

Jawab pertanyaan berikut:
1. **Fungsi RANSAC:** Mengapa RANSAC diperlukan setelah matching?
2. **Inlier Ratio:** Berapa persentase inlier yang dianggap baik?
3. **Threshold Impact:** Bagaimana threshold mempengaruhi jumlah inlier?
4. **Homography Quality:** Bagaimana cara mengevaluasi kualitas homography?

---

## 6. KESIMPULAN

### 6.1 Format Kesimpulan

Buat kesimpulan dengan menjawab pertanyaan berikut:

1. **Pemahaman Konsep:**
   - Apa itu fitur dalam konteks computer vision?
   - Mengapa deteksi fitur penting untuk berbagai aplikasi?

2. **Perbandingan Algoritma:**
   - Algoritma mana yang paling cepat?
   - Algoritma mana yang paling akurat?
   - Kapan menggunakan algoritma tertentu?

3. **Parameter Optimal:**
   - Parameter apa yang paling berpengaruh?
   - Apa nilai optimal untuk masing-masing parameter?

4. **Aplikasi Praktis:**
   - Untuk real-time application, algoritma mana yang dipilih?
   - Untuk precision-critical task, algoritma mana yang dipilih?

5. **Pembelajaran:**
   - Apa kesulitan yang ditemui?
   - Apa insight baru yang didapat?

### 6.2 Template Kesimpulan

```
KESIMPULAN PRAKTIKUM BAB 7

1. Corner Detection:
   - Harris lebih sensitif dengan k kecil, sementara...
   - Shi-Tomasi menghasilkan corner yang...

2. Feature Detection:
   - SIFT menghasilkan [X] keypoint dengan waktu [Y] ms
   - ORB lebih cepat [Z]x dibanding SIFT

3. Feature Matching:
   - Ratio test optimal adalah...
   - FLANN lebih efisien untuk...

4. RANSAC:
   - Threshold optimal adalah...
   - Inlier ratio yang baik adalah...

5. Rekomendasi:
   - Untuk real-time: gunakan...
   - Untuk akurasi tinggi: gunakan...
```

---

## 📎 LAMPIRAN

### Checklist Praktikum
- [ ] Semua percobaan selesai dijalankan
- [ ] Output tersimpan di folder yang benar
- [ ] Tabel pengamatan terisi lengkap
- [ ] Analisis setiap percobaan selesai
- [ ] Kesimpulan ditulis
- [ ] Screenshot hasil dilampirkan

### Pengumpulan
1. Folder lengkap dengan output
2. Laporan dalam format PDF
3. Video penjelasan (sesuai tugas video)
