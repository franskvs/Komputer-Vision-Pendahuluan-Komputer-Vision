# JOBSHEET PRAKTIKUM
# BAB 9: MOTION ESTIMATION

---

## 📋 INFORMASI PRAKTIKUM
| Item | Keterangan |
|------|------------|
| Mata Kuliah | Praktikum Computer Vision |
| Materi | Motion Estimation dan Optical Flow |
| Pertemuan | Bab 9 |
| Waktu | 150 menit |

---

## 1. TUJUAN PRAKTIKUM

### 1.1 Tujuan Umum
Mahasiswa mampu memahami dan mengimplementasikan teknik motion estimation untuk menganalisis pergerakan dalam video.

### 1.2 Tujuan Khusus per Percobaan

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

```bash
cd "Praktikum Komputer Vision/Bab-09-Motion-Estimation"
python praktikum/download_sample_data.py
```

### 3.2 Struktur Folder
```
Bab-09-Motion-Estimation/
├── praktikum/
│   ├── 01_lucas_kanade.py
│   ├── 02_dense_optical_flow.py
│   ├── 03_motion_detection.py
│   ├── 04_object_tracking.py
│   ├── 05_motion_history.py
│   ├── 06_video_stabilization.py
│   ├── 07_translational_alignment.py
│   ├── 08_frame_interpolation.py
│   ├── download_sample_data.py
│   └── output/
└── data/
   ├── videos/
   └── images/
```

---

### 3.3 Pelaksanaan Percobaan

#### PERCOBAAN 1: Lucas-Kanade Optical Flow

**Tujuan:** Tracking sparse features dengan Lucas-Kanade method

**Langkah-langkah:**
1. Buka file `01_lucas_kanade.py`
2. Pelajari parameter `cv2.calcOpticalFlowPyrLK()`
3. Jalankan program:
   ```bash
   python praktikum/01_lucas_kanade.py
   ```
4. Amati tracking points dan trails
5. **Variasi:**
   - Ubah `maxCorners` (jumlah features)
   - Ubah `winSize` (window size)
   - Coba dengan video lain

#### PERCOBAAN 2: Dense Optical Flow (Farneback)

**Tujuan:** Visualisasi dense flow field

**Langkah-langkah:**
1. Buka file `02_dense_optical_flow.py`
2. Jalankan:
   ```bash
   python praktikum/02_dense_optical_flow.py
   ```
3. Perhatikan:
   - Hue = direction of motion
   - Saturation = magnitude of motion
4. **Variasi:**
   - Ubah `pyr_scale` (pyramid scale)
   - Ubah `levels` (pyramid levels)

#### PERCOBAAN 3: Motion Detection

**Tujuan:** Deteksi area yang bergerak

**Langkah-langkah:**
1. Buka file `03_motion_detection.py`
2. Jalankan:
   ```bash
   python praktikum/03_motion_detection.py
   ```
3. Amati:
   - Background subtraction
   - Motion mask
   - Bounding boxes
4. **Variasi:**
   - Ubah threshold sensitivity
   - Coba berbagai background subtractor

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
