# Jobsheet Praktikum - Bab 4: Model Fitting dan Feature Matching

## Informasi Umum
- **Mata Kuliah:** Praktikum Computer Vision
- **Bab:** 4 - Model Fitting dan Feature Matching
- **Referensi:** Computer Vision: Algorithms and Applications, 2nd Edition - Chapter 7 & 8
- **Durasi:** 3 × pertemuan (@ 100 menit)

---

## 1. Tujuan Praktikum

### Tujuan Umum
Mahasiswa mampu mengimplementasikan teknik model fitting dan feature matching untuk berbagai aplikasi computer vision.

### Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan Pembelajaran |
|----|-----------|---------------------|
| 1 | Feature Detection | Memahami berbagai algoritma deteksi fitur (Harris, ORB, SIFT, AKAZE) |
| 2 | Feature Matching | Menguasai teknik matching dengan Brute-Force dan FLANN |
| 3 | RANSAC | Mengimplementasikan algoritma RANSAC untuk robust estimation |
| 4 | Hough Line Transform | Mendeteksi garis menggunakan Hough Transform |
| 5 | Hough Circle Transform | Mendeteksi lingkaran dalam gambar |
| 6 | Homography | Menghitung dan menerapkan transformasi homography |
| 7 | Perspective Correction | Menerapkan homography untuk koreksi perspektif |
| 8 | Optical Flow | Mengimplementasikan optical flow untuk tracking |

---

## 2. Alat dan Bahan

### Software Requirements
```
Python >= 3.8
opencv-python >= 4.8.0
opencv-contrib-python >= 4.8.0  # Untuk SIFT/SURF
numpy >= 1.24.0
matplotlib >= 3.7.0
```

### Hardware Requirements
- Komputer dengan RAM minimal 4GB
- Webcam (untuk percobaan optical flow)
- Resolusi layar minimal 1366×768

### Bahan Percobaan
1. **Gambar untuk Feature Matching:**
   - Dua gambar dengan area overlap
   - Gambar dengan sudut pandang berbeda
   
2. **Gambar untuk Hough Transform:**
   - Gambar dengan garis-garis jelas (jalan, bangunan)
   - Gambar dengan lingkaran (koin, bola, mata)
   
3. **Gambar untuk Homography:**
   - Gambar dokumen/papan tulis dengan sudut
   - Gambar untuk panorama (2-3 gambar berurutan)

4. **Video untuk Optical Flow:**
   - Video dengan gerakan objek
   - Webcam stream

---

## 3. Langkah Kerja

### Percobaan 1: Feature Detection

#### Setup Awal
```bash
# Pastikan di direktori praktikum
cd Bab-04-Model-Fitting/praktikum

# Jalankan program
python 01_feature_detection.py
```

#### Langkah Percobaan
1. Buka file `01_feature_detection.py`
2. Perhatikan variabel konfigurasi di bagian atas
3. Jalankan program dengan gambar default
4. Ubah parameter dan amati perubahan:
   - `DETECTOR_TYPE`: 'harris', 'orb', 'sift', 'akaze'
   - `HARRIS_BLOCK_SIZE`: 2, 3, 5
   - `HARRIS_KSIZE`: 3, 5, 7
   - `ORB_NFEATURES`: 100, 500, 1000
5. Catat jumlah keypoints untuk setiap konfigurasi

#### Output yang Diharapkan
- Gambar dengan keypoints yang ditandai
- Informasi jumlah keypoints terdeteksi
- Waktu komputasi untuk setiap detector

---

### Percobaan 2: Feature Matching

#### Langkah Percobaan
1. Siapkan 2 gambar dengan area overlap
2. Buka file `02_feature_matching.py`
3. Konfigurasi path gambar di variabel `IMAGE_1` dan `IMAGE_2`
4. Jalankan dan amati:
   - Matches sebelum filtering
   - Matches setelah ratio test
   - Good matches yang tersisa
5. Eksperimen dengan:
   - `MATCHER_TYPE`: 'bf', 'flann'
   - `RATIO_THRESHOLD`: 0.6, 0.7, 0.8, 0.9
   - `DETECTOR_TYPE`: 'orb', 'sift', 'akaze'

#### Output yang Diharapkan
- Visualisasi matches antara dua gambar
- Jumlah matches sebelum dan sesudah filtering
- Perbandingan performa matcher

---

### Percobaan 3: RANSAC

#### Langkah Percobaan
1. Buka file `03_ransac.py`
2. Program akan generate data sintetis dengan outliers
3. Amati perbedaan hasil:
   - Least Squares fitting (semua data)
   - RANSAC fitting (robust)
4. Eksperimen dengan:
   - `OUTLIER_RATIO`: 0.1, 0.3, 0.5
   - `RANSAC_THRESHOLD`: 1.0, 5.0, 10.0
   - `RANSAC_ITERATIONS`: 100, 500, 1000

#### Output yang Diharapkan
- Plot data dengan outliers
- Garis hasil Least Squares
- Garis hasil RANSAC
- Perbandingan error

---

### Percobaan 4: Hough Line Transform

#### Langkah Percobaan
1. Siapkan gambar dengan garis-garis jelas
2. Buka file `04_hough_lines.py`
3. Jalankan dengan gambar default (lane/road image)
4. Eksperimen parameter:
   - `HOUGH_THRESHOLD`: 50, 100, 150, 200
   - `MIN_LINE_LENGTH`: 30, 50, 100
   - `MAX_LINE_GAP`: 5, 10, 20
   - `CANNY_LOW`: 30, 50, 100
   - `CANNY_HIGH`: 100, 150, 200

#### Output yang Diharapkan
- Edge detection result (Canny)
- Hough space visualization
- Detected lines overlay on original

---

### Percobaan 5: Hough Circle Transform

#### Langkah Percobaan
1. Siapkan gambar dengan lingkaran (koin, mata, bola)
2. Buka file `05_hough_circles.py`
3. Jalankan dan amati deteksi lingkaran
4. Eksperimen parameter:
   - `DP`: 1.0, 1.5, 2.0
   - `MIN_DIST`: 20, 50, 100
   - `PARAM1`: 50, 100, 200
   - `PARAM2`: 20, 30, 50
   - `MIN_RADIUS`, `MAX_RADIUS`

#### Output yang Diharapkan
- Lingkaran terdeteksi ditandai pada gambar
- Center points dan radius
- Jumlah lingkaran terdeteksi

---

### Percobaan 6: Homography

#### Langkah Percobaan
1. Siapkan 2 gambar dengan area overlap
2. Buka file `06_homography.py`
3. Program akan:
   - Detect dan match features
   - Compute homography dengan RANSAC
   - Warp salah satu gambar
4. Amati hasil transformasi

#### Output yang Diharapkan
- Feature matches visualization
- Computed homography matrix (3×3)
- Warped image result

---

### Percobaan 7: Perspective Correction

#### Langkah Percobaan
1. Siapkan gambar dokumen/papan tulis yang miring
2. Buka file `07_perspective_correction.py`
3. Pilih 4 corner points secara manual atau otomatis
4. Program akan menghitung homography dan koreksi perspektif

#### Output yang Diharapkan
- Gambar original dengan sudut
- Gambar setelah perspective correction (frontal view)
- Homography matrix yang digunakan

---

### Percobaan 8: Optical Flow

#### Langkah Percobaan
1. Buka file `08_optical_flow.py`
2. Gunakan video file atau webcam
3. Amati tracking points bergerak
4. Eksperimen dengan:
   - `FLOW_TYPE`: 'lucas_kanade', 'farneback'
   - `LK_WIN_SIZE`: (15, 15), (21, 21), (31, 31)
   - `LK_MAX_LEVEL`: 2, 3, 4

#### Output yang Diharapkan
- Video dengan optical flow vectors
- Track lines mengikuti gerakan
- Visualisasi dense flow (untuk Farneback)

---

## 4. Data Pengamatan

### Tabel Pengamatan Percobaan 1: Feature Detection

| Detector | Parameters | Jumlah Keypoints | Waktu (ms) | Catatan |
|----------|------------|------------------|------------|---------|
| Harris | block=2, k=0.04 | | | |
| Harris | block=3, k=0.04 | | | |
| ORB | nfeatures=500 | | | |
| ORB | nfeatures=1000 | | | |
| SIFT | default | | | |
| AKAZE | default | | | |

### Tabel Pengamatan Percobaan 2: Feature Matching

| Detector | Matcher | Ratio | Raw Matches | Good Matches | Akurasi (%) |
|----------|---------|-------|-------------|--------------|-------------|
| ORB | BF | 0.7 | | | |
| ORB | BF | 0.8 | | | |
| ORB | FLANN | 0.7 | | | |
| SIFT | BF | 0.7 | | | |
| SIFT | FLANN | 0.7 | | | |

### Tabel Pengamatan Percobaan 3: RANSAC

| Outlier Ratio | Threshold | Iterations | Inliers | LS Error | RANSAC Error |
|---------------|-----------|------------|---------|----------|--------------|
| 10% | 5.0 | 100 | | | |
| 30% | 5.0 | 100 | | | |
| 50% | 5.0 | 100 | | | |
| 30% | 1.0 | 100 | | | |
| 30% | 10.0 | 100 | | | |

### Tabel Pengamatan Percobaan 4: Hough Lines

| Canny Thresholds | Hough Threshold | Min Length | Max Gap | Lines Detected |
|------------------|-----------------|------------|---------|----------------|
| 50/150 | 100 | 50 | 10 | |
| 50/150 | 150 | 50 | 10 | |
| 50/150 | 100 | 100 | 10 | |
| 100/200 | 100 | 50 | 10 | |

### Tabel Pengamatan Percobaan 5: Hough Circles

| dp | minDist | param1 | param2 | minR | maxR | Circles Detected |
|----|---------|--------|--------|------|------|------------------|
| 1.0 | 50 | 100 | 30 | 10 | 100 | |
| 1.5 | 50 | 100 | 30 | 10 | 100 | |
| 1.0 | 30 | 100 | 30 | 10 | 100 | |
| 1.0 | 50 | 100 | 50 | 10 | 100 | |

### Tabel Pengamatan Percobaan 6-7: Homography

| Gambar | Jumlah Matches | Inliers | Reprojection Error | Visual Quality |
|--------|----------------|---------|-------------------|----------------|
| Set 1 | | | | |
| Set 2 | | | | |
| Set 3 | | | | |

### Tabel Pengamatan Percobaan 8: Optical Flow

| Method | Window Size | Max Level | FPS | Tracking Quality |
|--------|-------------|-----------|-----|------------------|
| LK | 15×15 | 2 | | |
| LK | 21×21 | 3 | | |
| LK | 31×31 | 4 | | |
| Farneback | - | - | | |

---

## 5. Analisis

### Panduan Analisis Percobaan 1: Feature Detection

**Pertanyaan untuk dijawab:**
1. Mengapa jumlah keypoints berbeda untuk setiap detector?
2. Bagaimana pengaruh block_size pada Harris detector?
3. Kapan sebaiknya menggunakan masing-masing detector?
4. Bagaimana trade-off antara jumlah keypoints dan waktu komputasi?

**Template Analisis:**
```
Dari hasil percobaan, detector [NAMA] mendeteksi [JUMLAH] keypoints
dalam waktu [WAKTU] ms. Hal ini disebabkan oleh [ALASAN].

Perbandingan dengan detector lain menunjukkan bahwa [OBSERVASI].

Untuk aplikasi [CONTOH], detector yang paling sesuai adalah [NAMA]
karena [ALASAN].
```

### Panduan Analisis Percobaan 2: Feature Matching

**Pertanyaan untuk dijawab:**
1. Mengapa ratio test dapat meningkatkan kualitas matching?
2. Bagaimana pengaruh threshold ratio terhadap jumlah dan kualitas matches?
3. Kapan BF matcher lebih baik dari FLANN dan sebaliknya?

### Panduan Analisis Percobaan 3: RANSAC

**Pertanyaan untuk dijawab:**
1. Mengapa RANSAC lebih robust terhadap outliers dibanding Least Squares?
2. Bagaimana pengaruh outlier ratio terhadap jumlah iterasi yang dibutuhkan?
3. Bagaimana memilih threshold yang tepat?

### Panduan Analisis Percobaan 4-5: Hough Transform

**Pertanyaan untuk dijawab:**
1. Bagaimana threshold mempengaruhi deteksi (true positives vs false positives)?
2. Mengapa preprocessing (blur, edge detection) penting?
3. Bagaimana cara mengatasi deteksi ganda pada satu objek?

### Panduan Analisis Percobaan 6-7: Homography

**Pertanyaan untuk dijawab:**
1. Berapa minimum matches yang dibutuhkan untuk homography yang baik?
2. Mengapa RANSAC penting dalam estimasi homography?
3. Apa yang menyebabkan warping artifacts?

### Panduan Analisis Percobaan 8: Optical Flow

**Pertanyaan untuk dijawab:**
1. Bagaimana ukuran window mempengaruhi tracking?
2. Kapan tracking gagal dan bagaimana mengatasinya?
3. Trade-off antara Lucas-Kanade dan Farneback?

---

## 6. Kesimpulan

### Panduan Menyusun Kesimpulan

Kesimpulan harus mencakup:

1. **Ringkasan Temuan Utama**
   - Detector mana yang paling sesuai untuk skenario apa
   - Parameter optimal untuk setiap teknik
   - Kelebihan dan kekurangan setiap metode

2. **Validasi Tujuan Praktikum**
   - Apakah tujuan praktikum tercapai?
   - Teknik mana yang sudah dikuasai?
   - Kesulitan yang dihadapi

3. **Rekomendasi**
   - Best practices untuk aplikasi tertentu
   - Parameter yang disarankan
   - Kombinasi teknik yang efektif

4. **Refleksi**
   - Apa yang dipelajari dari praktikum ini?
   - Bagaimana teknik ini dapat diterapkan di proyek nyata?

### Template Kesimpulan

```
KESIMPULAN

1. Dari praktikum ini, saya mempelajari bahwa:
   - [TEMUAN 1]
   - [TEMUAN 2]
   - [TEMUAN 3]

2. Perbandingan berbagai metode menunjukkan:
   - Untuk [SKENARIO 1], metode terbaik adalah [METODE] karena [ALASAN]
   - Untuk [SKENARIO 2], metode terbaik adalah [METODE] karena [ALASAN]

3. Parameter optimal yang ditemukan:
   - [TEKNIK 1]: [PARAMETER]
   - [TEKNIK 2]: [PARAMETER]

4. Teknik-teknik ini dapat diterapkan untuk:
   - [APLIKASI 1]
   - [APLIKASI 2]

5. Tantangan utama dalam implementasi adalah [TANTANGAN],
   yang dapat diatasi dengan [SOLUSI].
```

---

## Lampiran

### Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| SIFT not found | opencv-contrib tidak terinstall | `pip install opencv-contrib-python` |
| No matches found | Gambar terlalu berbeda | Gunakan gambar dengan overlap |
| RANSAC gagal | Terlalu banyak outliers | Tingkatkan filtering atau iterasi |
| Homography distorted | Tidak cukup inliers | Tingkatkan jumlah features |
| Optical flow drift | Accumulated error | Re-detect features periodically |

### Referensi Cepat OpenCV

```python
# Feature Detection
orb = cv2.ORB_create(nfeatures=500)
sift = cv2.SIFT_create()
akaze = cv2.AKAZE_create()

# Feature Matching
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# RANSAC Homography
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Hough Transform
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, minLength, maxGap)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, minDist, param1, param2)

# Optical Flow
p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, gray, p0, None, **lk_params)
flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
```

---

*Jobsheet ini mendukung pembelajaran Bab 4: Model Fitting dan Feature Matching*
