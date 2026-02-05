# JOBSHEET PRAKTIKUM
# BAB 9: MOTION ESTIMATION DAN OPTICAL FLOW

---

## 📋 INFORMASI PRAKTIKUM
| Item | Keterangan |
|------|------------|
| Mata Kuliah | Praktikum Computer Vision |
| Materi | Motion Estimation, Optical Flow, dan Video Analysis |
| Pertemuan | Minggu ke-9 |
| Waktu | 3 × 50 menit (150 menit) |
| Tingkat Kesulitan | Menengah - Lanjut |
| Prasyarat | Menguasai Bab 1-8, Feature Detection |

---

## 1. TUJUAN PRAKTIKUM

### 1.1 Tujuan Umum
Mahasiswa mampu memahami konsep motion estimation dan optical flow, serta mengimplementasikannya untuk berbagai aplikasi analisis video seperti tracking, stabilization, dan motion detection dalam konteks computer vision modern.

### 1.2 Kompetensi yang Diharapkan
Setelah menyelesaikan praktikum ini, mahasiswa diharapkan dapat:
1. Menjelaskan perbedaan antara sparse dan dense optical flow
2. Mengimplementasikan algoritma Lucas-Kanade dan Farneback
3. Menerapkan motion detection untuk surveillance applications
4. Melakukan object tracking dengan berbagai metode
5. Membuat video stabilization system
6. Memahami konsep translational alignment dan frame interpolation
7. Menganalisis performa berbagai metode motion estimation

### 1.3 Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan |
|----|-----------|--------|
| 1 | Lucas-Kanade Optical Flow | Tracking sparse features dengan LK method |
| 2 | Dense Optical Flow (Farneback) | Visualisasi flow field untuk seluruh frame |
| 3 | Motion Detection | Deteksi area yang bergerak dalam video |
| 4 | Object Tracking | Melacak objek spesifik dalam video |
| 5 | Motion History | Visualisasi history pergerakan |
| 6 | Video Stabilization | Menstabilkan video yang goyang |
| 7 | Translational Alignment | Estimasi pergeseran antar dua frame (SSD & phase correlation) |
| 8 | Frame Interpolation | Membuat frame tengah dengan optical flow |

---

## 2. ALAT DAN BAHAN

### 2.1 Perangkat Keras
| No | Alat | Spesifikasi |
|----|------|-------------|
| 1 | Komputer/Laptop | RAM 8GB, Processor i5+ |
| 2 | Webcam (opsional) | Untuk capture video langsung |

### 2.2 Perangkat Lunak
| No | Software | Versi |
|----|----------|-------|
| 1 | Python | 3.8+ |
| 2 | OpenCV | 4.5+ |
| 3 | NumPy | 1.19+ |
| 4 | Matplotlib | 3.3+ |

### 2.3 Bahan Praktikum
| No | Bahan | Keterangan |
|----|-------|------------|
| 1 | Video sample | Video dengan objek bergerak |
| 2 | Video stabilization test | Video yang goyang |

---

## 3. LANGKAH KERJA

### 3.1 Persiapan Environment

#### A. Instalasi Dependencies
```bash
# Install library yang diperlukan
pip install opencv-python opencv-contrib-python
pip install numpy matplotlib scipy
pip install imutils  # Optional, untuk helper functions
```

#### B. Verifikasi Instalasi
```bash
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
python -c "import numpy; print('NumPy version:', numpy.__version__)"
```

#### C. Download Sample Data
```bash
cd "Praktikum Komputer Vision/Modul-09-Motion-Estimation"
python praktikum/download_sample_data.py
```

#### D. Persiapan Webcam (Opsional)
Pastikan webcam terhubung dan dapat diakses:
```bash
python -c "import cv2; cap=cv2.VideoCapture(0); print('Webcam:', cap.isOpened()); cap.release()"
```

### 3.2 Struktur Folder
```
Modul-09-Motion-Estimation/
├── praktikum/
│   ├── 01_lucas_kanade.py              # Sparse optical flow
│   ├── 02_dense_optical_flow.py         # Dense flow visualization
│   ├── 03_motion_detection.py           # Background subtraction
│   ├── 04_object_tracking.py            # Single/multi object tracking
│   ├── 05_motion_history.py             # Motion history imaging
│   ├── 06_video_stabilization.py        # Video stabilizer
│   ├── 07_translational_alignment.py    # Image registration
│   ├── 08_frame_interpolation.py        # Frame rate up-conversion
│   ├── download_sample_data.py          # Data downloader
│   └── output/                          # Output hasil percobaan
├── data/
│   ├── videos/                          # Video samples
│   └── images/                          # Image sequences
├── Jobsheet.md
├── Materi.md
└── Project.md
```

---

### 3.3 Pelaksanaan Percobaan

#### PERCOBAAN 1: Lucas-Kanade Optical Flow

**Tujuan:** Memahami dan mengimplementasikan sparse optical flow untuk feature tracking menggunakan metode Lucas-Kanade

**Teori Singkat:**
Lucas-Kanade adalah algoritma sparse optical flow yang melacak fitur-fitur tertentu antar frame. Metode ini efisien karena hanya menghitung flow pada titik-titik menarik (keypoints), bukan seluruh pixel.

**Langkah-langkah:**
1. Buka file `01_lucas_kanade.py` dan pahami struktur kode

2. Pelajari parameter penting:
   ```python
   # Parameter untuk deteksi corner (Shi-Tomasi)
   feature_params = dict(
       maxCorners = 100,      # Jumlah max features yang ditrack
       qualityLevel = 0.3,    # Quality threshold (0-1)
       minDistance = 7,       # Jarak minimum antar features
       blockSize = 7          # Ukuran neighborhood
   )
   
   # Parameter untuk Lucas-Kanade optical flow
   lk_params = dict(
       winSize = (15, 15),    # Search window size
       maxLevel = 2,          # Pyramid levels
       criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
   )
   ```

3. Jalankan program:
   ```bash
   python praktikum/01_lucas_kanade.py
   ```

4. Amati output:
   - Track lines menunjukkan trajectory features
   - Warna berbeda untuk setiap track
   - Features yang hilang akan di-redeteksi

5. **Eksperimen dengan Parameter:**
   
   **Variasi 1 - Jumlah Features:**
   - Ubah `maxCorners` menjadi 50, 100, 200
   - Amati: Lebih banyak features = lebih detail tapi lebih lambat
   
   **Variasi 2 - Window Size:**
   - Ubah `winSize` menjadi (10,10), (15,15), (31,31)
   - Amati: Window kecil = sensitive, window besar = robust tapi blur
   
   **Variasi 3 - Pyramid Levels:**
   - Ubah `maxLevel` menjadi 1, 2, 3
   - Amati: Lebih banyak level = dapat handle gerakan lebih besar

6. **Pertanyaan Analisis:**
   - Pada kondisi apa tracking gagal?
   - Apa pengaruh pencahayaan terhadap tracking?
   - Kapan features perlu di-redeteksi?

**Expected Output:**
- Video dengan tracking trails berwarna
- Console output menunjukkan jumlah features tracked
- File output: `output/01_lucas_kanade_result.mp4`

#### PERCOBAAN 2: Dense Optical Flow (Farneback)

**Tujuan:** Memahami dan memvisualisasikan dense optical flow untuk analisis pergerakan seluruh frame

**Teori Singkat:**
Farneback method menghitung optical flow untuk setiap pixel dalam frame, memberikan visualisasi lengkap dari motion field. Berbeda dengan Lucas-Kanade yang sparse, metode ini menghasilkan dense flow field.

**Langkah-langkah:**
1. Buka file `02_dense_optical_flow.py`

2. Pahami visualisasi HSV color coding:
   ```python
   # Hue (0-179) = Direction of motion (angle)
   # Saturation (0-255) = Magnitude of motion (speed)
   # Value = Fixed at 255 (brightness)
   ```
   - Warna merah: Gerakan ke kanan
   - Warna cyan: Gerakan ke kiri  
   - Warna kuning: Gerakan ke bawah
   - Warna biru: Gerakan ke atas
   - Intensitas warna: Kecepatan gerakan

3. Jalankan program:
   ```bash
   python praktikum/02_dense_optical_flow.py
   ```

4. Perhatikan output window:
   - Original frame (kiri)
   - Flow visualization dengan HSV (kanan)
   - Magnitude overlay (opsional)

5. **Eksperimen dengan Parameter Farneback:**
   ```python
   flow = cv2.calcOpticalFlowFarneback(
       prev_gray, curr_gray,
       pyr_scale=0.5,     # Pyramid scale [0.3-0.8]
       levels=3,          # Pyramid levels [1-5]
       winsize=15,        # Window size [5-25]
       iterations=3,      # Iterations per level
       poly_n=5,          # Polynomial neighborhood [5-7]
       poly_sigma=1.2,    # Gaussian sigma [1.1-1.5]
       flags=0
   )
   ```
   
   **Variasi 1 - Pyramid Scale:**
   - `pyr_scale=0.3`: Lebih detail, untuk gerakan lambat
   - `pyr_scale=0.5`: Balanced (default)
   - `pyr_scale=0.7`: Lebih coarse, untuk gerakan cepat
   
   **Variasi 2 - Pyramid Levels:**
   - `levels=1`: Cepat tapi tidak bisa handle gerakan besar
   - `levels=3`: Balanced
   - `levels=5`: Lambat tapi robust untuk gerakan besar
   
   **Variasi 3 - Window Size:**
   - `winsize=5`: Sensitif, detail tinggi
   - `winsize=15`: Balanced  
   - `winsize=25`: Smooth, robust terhadap noise

6. **Analisis:**
   - Bandingkan FPS antara berbagai konfigurasi
   - Identifikasi area dengan gerakan paling cepat
   - Perhatikan noise pada area statis

**Expected Output:**
- Video dengan flow visualization berwarna
- Console: FPS dan processing time
- File: `output/02_dense_flow_result.mp4`

#### PERCOBAAN 3: Motion Detection

**Tujuan:** Implementasi sistem deteksi gerakan untuk aplikasi surveillance

**Teori Singkat:**
Motion detection menggunakan background subtraction untuk memisahkan foreground (objek bergerak) dari background (area statis). Teknik ini fundamental untuk aplikasi security camera dan monitoring.

**Langkah-langkah:**
1. Buka file `03_motion_detection.py`

2. Pahami metode background subtraction:
   ```python
   # MOG2 (Mixture of Gaussians 2)
   bg_subtractor = cv2.createBackgroundSubtractorMOG2(
       history=500,          # Frames untuk learning
       varThreshold=16,      # Threshold untuk detection
       detectShadows=True    # Deteksi bayangan
   )
   ```

3. Jalankan program:
   ```bash
   python praktikum/03_motion_detection.py
   ```

4. Amati output multi-window:
   - **Original**: Frame asli
   - **Motion Mask**: Binary mask (putih=motion, hitam=statis)
   - **Foreground**: Objek bergerak yang terdeteksi
   - **Bounding Boxes**: Kotak pembatas objek

5. **Eksperimen dengan Methods:**
   
   **Method 1 - MOG2 (Recommended):**
   ```python
   bg_subtractor = cv2.createBackgroundSubtractorMOG2(
       history=500, varThreshold=16, detectShadows=True
   )
   ```
   - Pro: Adaptif, handle illumination changes
   - Con: Sedikit lebih lambat
   
   **Method 2 - KNN:**
   ```python
   bg_subtractor = cv2.createBackgroundSubtractorKNN(
       history=500, dist2Threshold=400, detectShadows=True
   )
   ```
   - Pro: Lebih akurat untuk beberapa scene
   - Con: Lebih lambat dari MOG2
   
   **Method 3 - Frame Differencing:**
   ```python
   # Simple frame difference
   diff = cv2.absdiff(prev_frame, curr_frame)
   ```
   - Pro: Sangat cepat
   - Con: Sensitif terhadap noise

6. **Post-Processing untuk Noise Reduction:**
   ```python
   # Morphological operations
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
   mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Remove noise
   mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill gaps
   ```

7. **Parameter Tuning:**
   - **varThreshold** (16-50): Lower=lebih sensitif
   - **history** (100-1000): Durasi learning background
   - **Minimum contour area**: Filter small noise

8. **Analisis:**
   - Hitung true positives vs false positives
   - Test dengan kondisi: orang jalan, pohon goyang, bayangan
   - Identifikasi situasi dimana detection gagal

**Expected Output:**
- Multi-window dengan visualisasi berbeda
- Bounding boxes pada objek bergerak
- Console: Detection statistics
- File: `output/03_motion_detection_result.mp4`

#### PERCOBAAN 4: Object Tracking

**Tujuan:** Track objek spesifik dalam video

**Langkah-langkah:**
1. Buka file `04_object_tracking.py`
2. Jalankan:
   ```bash
   python praktikum/04_object_tracking.py
   ```
3. Pilih objek untuk di-track
4. Amati tracking performance
5. **Variasi:**
   - Coba tracker berbeda (CSRT, KCF, MOSSE)

#### PERCOBAAN 5: Motion History Image

**Tujuan:** Visualisasi history pergerakan

**Langkah-langkah:**
1. Buka file `05_motion_history.py`
2. Jalankan:
   ```bash
   python praktikum/05_motion_history.py
   ```
3. Amati gradasi warna yang menunjukkan motion recency
4. **Variasi:**
   - Ubah duration parameter
   - Ubah threshold

#### PERCOBAAN 6: Video Stabilization

**Tujuan:** Menstabilkan video yang goyang

**Langkah-langkah:**
1. Buka file `06_video_stabilization.py`
2. Jalankan:
   ```bash
   python praktikum/06_video_stabilization.py
   ```
3. Bandingkan video original vs stabilized
4. **Variasi:**
   - Ubah smoothing radius
   - Coba dengan video yang lebih goyang

#### PERCOBAAN 7: Translational Alignment (SSD & Phase Correlation)

**Tujuan:** Estimasi pergeseran translasi antar dua frame

**Langkah-langkah:**
1. Buka file `07_translational_alignment.py`
2. Jalankan:
   ```bash
   python praktikum/07_translational_alignment.py
   ```
3. Perhatikan estimasi `dx, dy` dari SSD dan phase correlation
4. **Variasi:**
   - Ubah `SEARCH_RANGE`
   - Coba pasangan gambar berbeda

#### PERCOBAAN 8: Frame Interpolation

**Tujuan:** Membuat frame tengah (t=0.5) dengan optical flow

**Langkah-langkah:**
1. Buka file `08_frame_interpolation.py`
2. Jalankan:
   ```bash
   python praktikum/08_frame_interpolation.py
   ```
3. Amati hasil interpolasi di antara Frame 1 dan Frame 2
4. **Variasi:**
   - Ubah parameter Farneback
   - Coba video/dua frame yang lebih kompleks

---

## 4. DATA PENGAMATAN

### 4.1 Tabel Percobaan 1 (Lucas-Kanade)

| Parameter | Nilai | Tracked Points | FPS | Tracking Quality |
|-----------|-------|----------------|-----|------------------|
| maxCorners=100, winSize=15 | Default | ... | ... | ... |
| maxCorners=50, winSize=15 | Variasi 1 | ... | ... | ... |
| maxCorners=100, winSize=31 | Variasi 2 | ... | ... | ... |

### 4.2 Tabel Percobaan 2 (Dense Flow)

| Parameter | FPS | Motion Visible | Notes |
|-----------|-----|----------------|-------|
| pyr_scale=0.5, levels=3 | ... | ... | ... |
| pyr_scale=0.5, levels=5 | ... | ... | ... |
| pyr_scale=0.3, levels=3 | ... | ... | ... |

### 4.3 Tabel Percobaan 3 (Motion Detection)

| Method | Sensitivity | False Positives | True Detections |
|--------|-------------|-----------------|-----------------|
| MOG2 | ... | ... | ... |
| KNN | ... | ... | ... |
| Frame Diff | ... | ... | ... |

### 4.4 Tabel Percobaan 4 (Tracking)

| Tracker | Init Success | Track Duration | Lost Count |
|---------|--------------|----------------|------------|
| CSRT | ... | ... | ... |
| KCF | ... | ... | ... |
| MOSSE | ... | ... | ... |

### 4.5 Tabel Percobaan 6 (Stabilization)

| Smoothing | Jitter Reduction | Border Crop | Quality |
|-----------|------------------|-------------|---------|
| 5 frames | ... | ... | ... |
| 15 frames | ... | ... | ... |
| 30 frames | ... | ... | ... |

### 4.6 Tabel Percobaan 7 (Translational Alignment)

| Metode | dx, dy | Error/Response | Notes |
|--------|--------|----------------|-------|
| SSD | ... | ... | ... |
| Phase Correlation | ... | ... | ... |

### 4.7 Tabel Percobaan 8 (Frame Interpolation)

| Parameter | Visual Quality | Artifacts | Notes |
|-----------|----------------|----------|-------|
| Default Farneback | ... | ... | ... |
| Variasi 1 | ... | ... | ... |

---

## 5. ANALISIS

### 5.1 Panduan Analisis Percobaan 1-2

1. **Sparse vs Dense:** Kapan menggunakan Lucas-Kanade vs Farneback?
2. **Performance:** Bagaimana hubungan parameter dengan FPS?
3. **Accuracy:** Pada kondisi apa tracking akurat/gagal?
4. **Window size:** Bagaimana pengaruh window size pada accuracy?

### 5.2 Panduan Analisis Percobaan 3-4

1. **Motion Detection:** Apa penyebab false positives?
2. **Tracker Comparison:** Tracker mana paling robust?
3. **Occlusion:** Bagaimana tracker handle occlusion?
4. **Speed vs Accuracy:** Trade-off apa yang terlihat?

### 5.3 Panduan Analisis Percobaan 5-6

1. **Motion History:** Kegunaan visualisasi ini?
2. **Stabilization:** Seberapa efektif stabilization?
3. **Side Effects:** Apa dampak negatif dari stabilization?

---

## 6. KESIMPULAN

### Format Kesimpulan:

```
KESIMPULAN PRAKTIKUM BAB 9

1. Optical Flow:
   - Lucas-Kanade cocok untuk: ...
   - Farneback cocok untuk: ...

2. Motion Detection:
   - Metode terbaik: ...
   - Limitasi: ...

3. Tracking:
   - Tracker terobust: ...
   - Kondisi gagal: ...

4. Stabilization:
   - Efektivitas: ...
   - Trade-off: ...

5. Pembelajaran:
   - Insight utama: ...
   - Aplikasi praktis: ...
```

---

## 📎 LAMPIRAN

### Checklist Praktikum
- [ ] Semua percobaan dijalankan
- [ ] Output tersimpan
- [ ] Tabel pengamatan terisi
- [ ] Analisis selesai
- [ ] Kesimpulan ditulis
- [ ] Video sendiri dicoba (bonus)

### Pengumpulan
1. Folder lengkap dengan output
2. Video demo hasil tracking/stabilization
3. Laporan PDF
4. Video penjelasan
