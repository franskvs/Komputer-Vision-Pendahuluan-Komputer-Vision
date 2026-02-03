# JOBSHEET PRAKTIKUM BAB 12
# DEPTH ESTIMATION (STEREO MATCHING)

---

## 🎯 1. Tujuan Praktikum

### Tujuan Umum
Mahasiswa mampu memahami dan mengimplementasikan teknik estimasi kedalaman menggunakan stereo vision dan deep learning.

### Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan |
|----|-----------|--------|
| 1 | Stereo Camera Calibration | Memahami cara mengkalibrasi stereo camera |
| 2 | Stereo Rectification | Memahami proses rectification untuk stereo matching |
| 3 | Block Matching | Mengimplementasikan algoritma stereo matching dasar |
| 4 | Semi-Global Matching (SGM) | Menggunakan SGM untuk hasil lebih baik |
| 5 | Disparity to Depth Conversion | Mengkonversi disparity map ke depth map |
| 6 | Monocular Depth Estimation | Menggunakan deep learning untuk depth estimation |
| 7 | Depth Map Applications | Menerapkan depth map untuk segmentasi dan 3D |

---

## 🔧 2. Alat dan Bahan

### 2.1 Perangkat Keras
| Alat | Spesifikasi Minimum | Keterangan |
|------|-------------------|------------|
| Komputer/Laptop | RAM 8GB, GPU recommended | Untuk running program |
| Stereo Camera (opsional) | ZED, RealSense, atau DIY | Untuk capture stereo |
| Webcam | 2 unit identik | Untuk DIY stereo |

### 2.2 Perangkat Lunak
| Software | Versi | Fungsi |
|----------|-------|--------|
| Python | 3.8+ | Bahasa pemrograman |
| OpenCV | 4.8+ | Stereo matching algorithms |
| NumPy | 1.24+ | Operasi numerik |
| PyTorch | 2.0+ | Deep learning (MiDaS) |
| Open3D | 0.17+ | Visualisasi point cloud |

### 2.3 Data yang Dibutuhkan
- Gambar stereo (left-right pair)
- Checkerboard untuk kalibrasi (9×6 atau 7×5)
- Dataset stereo (Middlebury, KITTI)

### 2.4 Instalasi Library
```bash
pip install opencv-python opencv-contrib-python numpy torch torchvision timm open3d matplotlib
```

---

## 📋 3. Langkah Kerja

### Persiapan Awal

1. **Clone/Download Repository**
   ```bash
   cd ~/Documents/Praktikum\ Komputer\ Vision/Bab-12-Depth-Estimation
   ```

2. **Download Sample Data**
   ```bash
   python download_sample_data.py
   ```

3. **Verifikasi Instalasi**
   ```bash
   python -c "import cv2; import torch; print('Libraries ready!')"
   ```

### Percobaan 1: Stereo Camera Calibration

**Langkah:**
1. Buka file `01_stereo_calibration.py`
2. Siapkan gambar checkerboard dari stereo camera
3. Perhatikan variabel konfigurasi:
   ```python
   CHECKERBOARD_SIZE = (9, 6)  # Inner corners
   SQUARE_SIZE = 25.0  # mm
   ```
4. Jalankan dan simpan hasil kalibrasi
5. Analisis parameter intrinsik dan extrinsik

### Percobaan 2: Stereo Rectification

**Langkah:**
1. Buka file `02_stereo_rectification.py`
2. Load hasil kalibrasi dari percobaan 1
3. Jalankan rectification dan bandingkan:
   - Sebelum rectification
   - Sesudah rectification
4. Verifikasi epipolar lines horizontal

### Percobaan 3: Block Matching

**Langkah:**
1. Buka file `03_block_matching.py`
2. Konfigurasi parameter:
   ```python
   NUM_DISPARITIES = 64   # Max disparity
   BLOCK_SIZE = 15        # Matching window
   ```
3. Jalankan dan amati disparity map
4. Eksperimen dengan parameter berbeda

### Percobaan 4: Semi-Global Matching (SGM)

**Langkah:**
1. Buka file `04_sgm_matching.py`
2. Bandingkan dengan Block Matching:
   ```python
   # SGM memiliki parameter tambahan
   P1 = 8 * 3 * BLOCK_SIZE**2
   P2 = 32 * 3 * BLOCK_SIZE**2
   ```
3. Analisis perbedaan kualitas dan waktu komputasi

### Percobaan 5: Disparity to Depth

**Langkah:**
1. Buka file `05_disparity_to_depth.py`
2. Input parameter kamera:
   ```python
   BASELINE = 120.0  # mm (jarak antar kamera)
   FOCAL_LENGTH = 700.0  # pixel
   ```
3. Hitung depth map dari disparity
4. Visualisasi depth dengan colormap

### Percobaan 6: Monocular Depth (MiDaS)

**Langkah:**
1. Buka file `06_monocular_depth.py`
2. Download model MiDaS (otomatis)
3. Jalankan pada gambar single view
4. Bandingkan hasil dengan stereo depth

### Percobaan 7: Depth Map Applications

**Langkah:**
1. Buka file `07_depth_applications.py`
2. Implementasi aplikasi:
   - Segmentasi berdasarkan depth
   - Konversi ke point cloud 3D
   - Bokeh effect simulation
3. Analisis hasil masing-masing aplikasi

---

## 📊 4. Data Pengamatan

### Tabel 1: Hasil Kalibrasi Stereo
| Parameter | Kamera Kiri | Kamera Kanan |
|-----------|-------------|--------------|
| Focal Length fx | | |
| Focal Length fy | | |
| Principal Point cx | | |
| Principal Point cy | | |
| RMS Error | | |

### Tabel 2: Perbandingan Stereo Matching
| Algoritma | numDisparities | blockSize | Waktu (ms) | Kualitas |
|-----------|----------------|-----------|------------|----------|
| Block Matching | 64 | 15 | | |
| Block Matching | 128 | 15 | | |
| SGM | 64 | 5 | | |
| SGM | 128 | 5 | | |

### Tabel 3: Analisis Parameter Block Matching
| blockSize | Smoothness | Edge Preservation | Noise |
|-----------|------------|-------------------|-------|
| 5 | | | |
| 11 | | | |
| 15 | | | |
| 21 | | | |

### Tabel 4: Depth Accuracy (jika ground truth tersedia)
| Metode | MAE (m) | RMSE (m) | δ < 1.25 |
|--------|---------|----------|----------|
| Block Matching | | | |
| SGM | | | |
| MiDaS (mono) | | | |

### Tabel 5: Evaluasi Monocular Depth
| Model | Input Size | Waktu (ms) | Memory (MB) | Kualitas Visual |
|-------|------------|------------|-------------|-----------------|
| MiDaS Small | | | | |
| MiDaS Large | | | | |
| DPT Hybrid | | | | |

---

## 🔍 5. Analisis

### 5.1 Panduan Analisis Stereo Matching

**Pertanyaan Analisis:**
1. Mengapa ada "hole" (area tanpa depth) di disparity map?
2. Bagaimana blockSize mempengaruhi trade-off smoothness vs detail?
3. Mengapa SGM menghasilkan hasil lebih smooth dari Block Matching?
4. Pada area apa stereo matching sering gagal?

**Cara Menganalisis:**
- Identifikasi area textureless (dinding polos, langit)
- Identifikasi occlusion (area terhalang)
- Bandingkan edge preservation antar metode
- Ukur error di area berbeda (foreground vs background)

### 5.2 Panduan Analisis Depth Accuracy

**Pertanyaan Analisis:**
1. Bagaimana depth error bervariasi dengan jarak?
2. Apakah ada systematic bias (selalu overestimate/underestimate)?
3. Bagaimana performa di kondisi pencahayaan berbeda?

**Cara Menganalisis:**
- Plot error vs ground truth distance
- Hitung error statistics per range (0-5m, 5-10m, dst)
- Visualisasi error map

### 5.3 Panduan Analisis Monocular vs Stereo

**Pertanyaan Analisis:**
1. Apa kelebihan dan kekurangan masing-masing metode?
2. Kapan menggunakan monocular vs stereo?
3. Bagaimana handling scale ambiguity di monocular depth?

**Cara Menganalisis:**
- Bandingkan kualitas visual
- Ukur waktu komputasi
- Evaluasi kebutuhan hardware

---

## 📝 6. Kesimpulan

### Panduan Membuat Kesimpulan

Kesimpulan harus mencakup poin-poin berikut:

1. **Pemahaman Konsep**
   - Jelaskan hubungan disparity dengan depth
   - Jelaskan mengapa stereo vision memerlukan kalibrasi

2. **Perbandingan Metode**
   - Block Matching vs SGM: mana yang lebih baik untuk kasus apa?
   - Stereo vs Monocular: kapan menggunakan masing-masing?

3. **Limitasi dan Solusi**
   - Apa tantangan utama dalam stereo matching?
   - Bagaimana deep learning membantu mengatasi limitasi?

4. **Aplikasi Praktis**
   - Rekomendasi metode untuk aplikasi tertentu
   - Pertimbangan real-time vs accuracy

### Template Kesimpulan

```
Berdasarkan praktikum yang telah dilakukan, dapat disimpulkan bahwa:

1. [Kesimpulan tentang stereo matching]
2. [Kesimpulan tentang pengaruh parameter]
3. [Kesimpulan tentang monocular depth]
4. [Kesimpulan tentang aplikasi depth map]
5. [Rekomendasi untuk penggunaan praktis]
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
