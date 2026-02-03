# PROJECT BAB 9: MOTION ESTIMATION

## 🎯 SISTEM ANALISIS PERGERAKAN UNTUK KEAMANAN RUMAH

---

## 📖 LATAR BELAKANG

Sebuah startup **"SmartGuard Security"** mengembangkan sistem keamanan rumah berbasis kamera yang cerdas. Berbeda dengan sistem CCTV tradisional yang hanya merekam, sistem ini harus bisa:

1. Mendeteksi pergerakan mencurigakan
2. Mengabaikan pergerakan normal (pohon, bayangan)
3. Tracking intruder secara real-time
4. Alert dengan video clip yang relevan

**Masalah yang dihadapi:**
- False alarms dari gerakan non-threatening (kucing, pohon)
- Missed detections saat gerakan lambat
- Storage penuh karena merekam terus-menerus
- Tidak ada tracking capability

---

## 🎯 TUJUAN PROJECT

### Tujuan Utama:
Mengembangkan sistem motion detection dan tracking yang intelligent untuk keamanan rumah.

### Tujuan Khusus:
1. Deteksi motion dengan minimal false positives
2. Track objek bergerak secara konsisten
3. Klasifikasi jenis pergerakan (manusia vs bukan)
4. Generate alert dengan video clip

---

## 📋 DESKRIPSI TUGAS

### Skenario:
Anda adalah engineer di SmartGuard Security. Tugasnya adalah membuat prototype "MotionGuard" dengan fitur:

1. **Smart Motion Detection:**
   - Deteksi area bergerak
   - Filter out noise dan small movements
   - Sensitivity adjustable

2. **Object Tracking:**
   - Track detected objects
   - Maintain ID across frames
   - Handle occlusion

3. **Motion Analysis:**
   - Calculate speed dan direction
   - Classify motion pattern
   - Detect suspicious behavior

4. **Alert System:**
   - Trigger recording saat ada motion
   - Save video clip with buffer
   - Generate summary

---

## 📝 SPESIFIKASI TEKNIS

### Input:
- Video dari file atau webcam
- Resolution: 640x480 minimum
- Frame rate: 15-30 FPS

### Output:
1. **Live Display:**
   - Bounding boxes pada moving objects
   - Tracking trails
   - Speed/direction indicators

2. **Recordings:**
   - Video clips saat ada motion
   - Motion history image
   - Event log

3. **Analysis Report:**
   - Total motion events
   - Duration per event
   - Motion heatmap

---

## 🔧 FITUR YANG HARUS DIIMPLEMENTASIKAN

### Fitur Wajib (80 poin):

1. **Motion Detection** (20 poin)
   - Background subtraction
   - Noise filtering
   - Region of Interest (ROI) support

2. **Object Tracking** (25 poin)
   - Multi-object tracking
   - Track ID maintenance
   - Trajectory visualization

3. **Motion Analysis** (20 poin)
   - Speed calculation
   - Direction estimation
   - Activity zones

4. **Recording System** (15 poin)
   - Pre-buffer recording
   - Event-triggered save
   - Timestamp overlay

### Fitur Bonus (20 poin):

1. **Person Detection** (+5 poin)
   - Integrate HOG atau deep learning
   - Filter non-human motion

2. **Zone Alerts** (+5 poin)
   - User-defined alert zones
   - Different sensitivity per zone

3. **Remote View** (+5 poin)
   - Simple web interface
   - Live streaming

4. **Statistics Dashboard** (+5 poin)
   - Motion timeline
   - Heatmap per jam

---

## 📁 STRUKTUR PROJECT

```
project_motionguard/
├── main.py                 # Entry point
├── detector.py            # Motion detection module
├── tracker.py             # Object tracking module
├── analyzer.py            # Motion analysis module
├── recorder.py            # Recording system
├── visualizer.py          # Display utilities
├── config.py              # Configuration
├── input/
│   └── test_videos/       # Test videos
├── output/
│   ├── recordings/        # Saved clips
│   ├── logs/              # Event logs
│   └── analysis/          # Reports
└── README.md
```

---

## 📝 LANGKAH PENGERJAAN

### Tahap 1: Motion Detection (Hari 1-2)
1. Implement background subtraction
2. Add noise filtering
3. Test dengan berbagai video
4. Tune sensitivity

### Tahap 2: Object Tracking (Hari 3-4)
1. Detect moving objects
2. Implement tracking algorithm
3. Handle multiple objects
4. Add trajectory visualization

### Tahap 3: Analysis & Recording (Hari 5)
1. Calculate motion metrics
2. Implement recording system
3. Add timestamps dan overlays
4. Generate event log

### Tahap 4: Integration & Testing (Hari 6-7)
1. Integrate semua module
2. Add UI/controls
3. Test berbagai skenario
4. Documentation

---

## 🎥 DEMO REQUIREMENTS

Video demo (3-5 menit) harus menunjukkan:

1. **Motion Detection**
   - Deteksi orang masuk frame
   - Filter out noise (bayangan, etc)

2. **Tracking**
   - Track objek across frame
   - Tampilkan trajectory

3. **Recording**
   - Tunjukkan auto-record saat motion
   - Preview saved clip

4. **Edge Cases**
   - Handling multiple objects
   - Handling occlusion

---

## 📊 RUBRIK PENILAIAN

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| **Detection Accuracy** | 25% | Low false positives, high true positives |
| **Tracking Robustness** | 25% | Consistent tracking, handle occlusion |
| **Code Quality** | 20% | Clean, modular, documented |
| **Performance** | 15% | Real-time capable (>15 FPS) |
| **Demo & Docs** | 15% | Clear demo, good documentation |

---

## 💡 HINTS

### Hint 1: Background Subtraction
```python
# MOG2 dengan tuning
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=16,
    detectShadows=True
)
fgbg.setShadowValue(0)  # Ignore shadows
```

### Hint 2: Noise Filtering
```python
# Morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

### Hint 3: Multi-Object Tracking
```python
# Simple centroid tracking
from scipy.spatial.distance import cdist

def match_objects(prev_centroids, curr_centroids, max_distance=50):
    if len(prev_centroids) == 0:
        return list(range(len(curr_centroids)))
    
    distances = cdist(prev_centroids, curr_centroids)
    # Hungarian algorithm atau simple matching
```

---

## 📚 REFERENSI

1. OpenCV Motion Detection Tutorial
2. "Multiple Object Tracking" - Papers with Code
3. Materi Praktikum Bab 9
4. OpenCV Background Subtraction docs

---

**Selamat mengerjakan! 🏠🎥**

*"Protecting homes with intelligent vision."*
