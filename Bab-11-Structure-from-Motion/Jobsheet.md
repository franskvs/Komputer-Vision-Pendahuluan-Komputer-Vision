# JOBSHEET PRAKTIKUM BAB 11
# STRUCTURE FROM MOTION DAN SLAM

---

## 🎯 1. Tujuan Praktikum

### Tujuan Umum
Mahasiswa mampu memahami dan mengimplementasikan teknik Structure from Motion (SfM) dan Visual SLAM untuk rekonstruksi 3D dan estimasi gerakan kamera.

### Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan |
|----|-----------|--------|
| 1 | Feature Matching Multi-View | Memahami cara mencocokkan fitur antar gambar dari sudut pandang berbeda |
| 2 | Fundamental Matrix | Mengestimasi hubungan geometris antar dua gambar tanpa kalibrasi |
| 3 | Essential Matrix | Mengestimasi pose relatif kamera dengan kalibrasi |
| 4 | Triangulasi 3D | Menghitung posisi 3D titik dari proyeksi 2D |
| 5 | Visual Odometry | Melacak gerakan kamera secara sekuensial |
| 6 | Bundle Adjustment | Mengoptimasi rekonstruksi 3D secara global |
| 7 | Simple SLAM | Membangun peta sekaligus melokalisasi kamera |

---

## 🔧 2. Alat dan Bahan

### 2.1 Perangkat Keras
| Alat | Spesifikasi Minimum | Keterangan |
|------|-------------------|------------|
| Komputer/Laptop | RAM 8GB, CPU Intel i5 atau setara | Untuk running program |
| Webcam/Kamera | Resolusi 720p | Untuk capture video |
| Objek 3D | Buku, kotak, atau objek bertekstur | Untuk percobaan |

### 2.2 Perangkat Lunak
| Software | Versi | Fungsi |
|----------|-------|--------|
| Python | 3.8+ | Bahasa pemrograman utama |
| OpenCV | 4.8+ | Library computer vision |
| NumPy | 1.24+ | Operasi numerik |
| Open3D | 0.17+ | Visualisasi 3D |
| SciPy | 1.11+ | Optimisasi (Bundle Adjustment) |

### 2.3 Data yang Dibutuhkan
- Sekuens gambar objek dari berbagai sudut (minimal 5 gambar)
- Video pendek (10-30 detik) untuk visual odometry
- Gambar stereo (left-right pair)
- Parameter kalibrasi kamera (jika tersedia)

### 2.4 Instalasi Library
```bash
pip install opencv-python opencv-contrib-python numpy scipy open3d matplotlib
```

---

## 📋 3. Langkah Kerja

### Persiapan Awal

1. **Clone/Download Repository**
   ```bash
   cd ~/Documents/Praktikum\ Komputer\ Vision/Bab-11-Structure-from-Motion
   ```

2. **Download Sample Data**
   ```bash
   python download_sample_data.py
   ```

3. **Verifikasi Instalasi**
   ```bash
   python -c "import cv2; import numpy; import open3d; print('Semua library siap!')"
   ```

### Percobaan 1: Feature Matching Multi-View

**Langkah:**
1. Buka file `01_feature_matching_multiview.py`
2. Perhatikan variabel konfigurasi di bagian atas:
   ```python
   DETECTOR_TYPE = 'SIFT'  # Coba: 'SIFT', 'ORB', 'AKAZE'
   RATIO_THRESHOLD = 0.75   # Lowe's ratio test
   ```
3. Jalankan program:
   ```bash
   python praktikum/01_feature_matching_multiview.py
   ```
4. Amati hasil matching pada gambar output
5. Ulangi dengan parameter berbeda

### Percobaan 2: Estimasi Fundamental Matrix

**Langkah:**
1. Buka file `02_fundamental_matrix.py`
2. Pelajari variabel konfigurasi:
   ```python
   RANSAC_THRESHOLD = 3.0    # Threshold reprojection error
   CONFIDENCE = 0.99          # Confidence level RANSAC
   ```
3. Jalankan dan amati epipolar lines
4. Verifikasi constraint: `x'ᵀ F x ≈ 0`

### Percobaan 3: Estimasi Essential Matrix

**Langkah:**
1. Buka file `03_essential_matrix.py`
2. Masukkan parameter kamera (atau gunakan default):
   ```python
   FOCAL_LENGTH = 1000  # dalam pixel
   PRINCIPAL_POINT = (320, 240)  # center gambar
   ```
3. Jalankan dan amati dekomposisi R, t
4. Catat pose kamera yang diestimasi

### Percobaan 4: Triangulasi 3D

**Langkah:**
1. Buka file `04_triangulasi_3d.py`
2. Gunakan hasil Essential Matrix dari percobaan sebelumnya
3. Jalankan dan visualisasi point cloud hasil
4. Evaluasi error reprojeksi

### Percobaan 5: Visual Odometry

**Langkah:**
1. Buka file `05_visual_odometry.py`
2. Siapkan video atau sekuens gambar
3. Jalankan dan amati trajectory kamera
4. Catat akurasi estimasi gerakan

### Percobaan 6: Bundle Adjustment

**Langkah:**
1. Buka file `06_bundle_adjustment.py`
2. Load hasil rekonstruksi sebelumnya
3. Jalankan optimasi dan bandingkan sebelum/sesudah
4. Ukur penurunan reprojection error

### Percobaan 7: Simple SLAM

**Langkah:**
1. Buka file `07_simple_slam.py`
2. Gunakan webcam atau video untuk input
3. Jalankan dan amati pembangunan peta real-time
4. Evaluasi drift dan akurasi

---

## 📊 4. Data Pengamatan

### Tabel 1: Hasil Feature Matching
| Detector | Jumlah Keypoints | Jumlah Match | Good Match | Waktu (ms) |
|----------|-----------------|--------------|------------|------------|
| SIFT | | | | |
| ORB | | | | |
| AKAZE | | | | |

### Tabel 2: Evaluasi Fundamental Matrix
| Pasangan Gambar | Jumlah Inlier | Epipolar Error Mean | Epipolar Error Std |
|-----------------|---------------|---------------------|-------------------|
| Img1-Img2 | | | |
| Img2-Img3 | | | |
| Img3-Img4 | | | |

### Tabel 3: Hasil Triangulasi
| Metode | Jumlah 3D Points | Reprojection Error (px) | Waktu (ms) |
|--------|-----------------|------------------------|------------|
| DLT | | | |
| Midpoint | | | |

### Tabel 4: Evaluasi Visual Odometry
| Frame Range | Translation Error | Rotation Error | Drift (%) |
|-------------|------------------|----------------|-----------|
| 0-50 | | | |
| 50-100 | | | |
| 100-150 | | | |

### Tabel 5: Bundle Adjustment Comparison
| Metrik | Sebelum BA | Sesudah BA | Improvement |
|--------|------------|------------|-------------|
| Mean Reproj Error | | | |
| Max Reproj Error | | | |
| Jumlah Outlier | | | |

### Tabel 6: SLAM Performance
| Skenario | Loop Closure | Map Points | Trajectory Length | Processing FPS |
|----------|--------------|------------|-------------------|----------------|
| Indoor | | | | |
| Outdoor | | | | |

---

## 🔍 5. Analisis

### 5.1 Panduan Analisis Feature Matching

**Pertanyaan Analisis:**
1. Mengapa SIFT menghasilkan lebih sedikit keypoints tapi match lebih akurat dibanding ORB?
2. Bagaimana pengaruh Lowe's ratio threshold terhadap jumlah good matches?
3. Pada kondisi apa detector tertentu lebih unggul?

**Cara Menganalisis:**
- Bandingkan repeatability (fitur yang terdeteksi di kedua gambar)
- Hitung precision: `good_matches / total_matches`
- Evaluasi trade-off antara akurasi dan kecepatan

### 5.2 Panduan Analisis Epipolar Geometry

**Pertanyaan Analisis:**
1. Apakah epipolar lines benar-benar melewati titik korespondensi?
2. Berapa error rata-rata dari constraint epipolar?
3. Apa yang menyebabkan outlier dalam estimasi Fundamental Matrix?

**Cara Menganalisis:**
- Hitung jarak titik ke epipolar line: `d = |x'ᵀFx| / ||Fx||`
- Visualisasi distribusi error
- Identifikasi pola outlier (biasanya di daerah homogen)

### 5.3 Panduan Analisis Rekonstruksi 3D

**Pertanyaan Analisis:**
1. Apakah struktur 3D yang dihasilkan sesuai dengan objek asli?
2. Bagaimana baseline kamera mempengaruhi akurasi depth?
3. Apa yang menyebabkan noise pada point cloud?

**Cara Menganalisis:**
- Bandingkan dengan ground truth jika tersedia
- Ukur scale dan proporsi objek
- Identifikasi area dengan rekonstruksi buruk

### 5.4 Panduan Analisis SLAM

**Pertanyaan Analisis:**
1. Kapan dan mengapa terjadi drift?
2. Bagaimana loop closure memperbaiki trajectory?
3. Apa faktor yang mempengaruhi real-time performance?

**Cara Menganalisis:**
- Plot trajectory dan identifikasi divergence
- Bandingkan trajectory sebelum dan sesudah loop closure
- Profiling waktu komputasi tiap modul

---

## 📝 6. Kesimpulan

### Panduan Membuat Kesimpulan

Kesimpulan harus mencakup poin-poin berikut:

1. **Pemahaman Konsep**
   - Apa hubungan antara feature matching dengan keberhasilan SfM?
   - Mengapa kalibrasi kamera penting untuk rekonstruksi akurat?

2. **Hasil Eksperimen**
   - Rangkum perbandingan performa berbagai metode
   - Identifikasi metode terbaik untuk kasus tertentu

3. **Tantangan dan Solusi**
   - Sebutkan tantangan yang ditemui selama praktikum
   - Jelaskan solusi atau workaround yang dilakukan

4. **Aplikasi Praktis**
   - Bagaimana teknik ini dapat diterapkan di dunia nyata?
   - Apa limitasi yang perlu dipertimbangkan?

5. **Pengembangan Lebih Lanjut**
   - Saran untuk meningkatkan hasil
   - Ide untuk eksperimen tambahan

### Template Kesimpulan

```
Berdasarkan praktikum yang telah dilakukan, dapat disimpulkan bahwa:

1. [Kesimpulan tentang feature matching]
2. [Kesimpulan tentang estimasi pose kamera]
3. [Kesimpulan tentang rekonstruksi 3D]
4. [Kesimpulan tentang Visual SLAM]
5. [Rekomendasi untuk aplikasi praktis]
```

---

## 📎 Lampiran

### Format Laporan
- **Halaman Judul**: Identitas, judul praktikum, tanggal
- **Tujuan**: Copy dari jobsheet + tujuan personal
- **Dasar Teori**: Ringkasan materi yang relevan
- **Metodologi**: Langkah kerja yang dilakukan
- **Hasil**: Screenshot, tabel data, grafik
- **Analisis**: Pembahasan hasil
- **Kesimpulan**: Ringkasan temuan
- **Daftar Pustaka**: Referensi yang digunakan

### Kriteria Penilaian Laporan
| Komponen | Bobot |
|----------|-------|
| Kelengkapan data | 20% |
| Kedalaman analisis | 30% |
| Kebenaran kesimpulan | 25% |
| Format dan presentasi | 15% |
| Ketepatan waktu | 10% |
