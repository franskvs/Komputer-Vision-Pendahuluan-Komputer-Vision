# PROJECT BAB 12: AUTONOMOUS VEHICLE DEPTH PERCEPTION

## 🎯 Studi Kasus: Sistem Persepsi Kedalaman untuk Kendaraan Otonom

### Deskripsi Proyek

Sebuah startup teknologi otomotif di Indonesia, **"AutoVision Indonesia"**, sedang mengembangkan sistem Advanced Driver Assistance System (ADAS) untuk kendaraan listrik lokal. Anda diminta untuk mengembangkan **modul depth perception** yang akan digunakan untuk:

1. **Collision avoidance** - Mendeteksi obstacle di depan kendaraan
2. **Lane keeping** - Memahami geometri jalan
3. **Parking assistance** - Mengukur jarak ke obstacle saat parkir

### Spesifikasi Teknis

#### Hardware yang Disimulasikan
- **Stereo Camera Setup**: 2 kamera dengan baseline 12cm
- **Resolution**: 1280×720 @ 30fps
- **FOV**: 90° horizontal

#### Requirements Fungsional
1. Sistem harus mampu menghasilkan depth map real-time (>15fps)
2. Akurasi depth: ±5% untuk jarak 1-15 meter
3. Deteksi obstacle di ground plane
4. Estimasi free space untuk navigasi

---

## 📋 Tugas yang Harus Dikerjakan

### Task 1: Stereo Pipeline Implementation (35%)

**Subtasks:**
1. **Stereo Calibration Module** (10%)
   - Implementasi kalibrasi stereo camera
   - Simpan parameter dalam format yang portable (XML/YAML)
   - Error kalibrasi < 0.5 pixel

2. **Rectification Pipeline** (10%)
   - Implementasi stereo rectification
   - Validasi dengan epipolar constraint
   - Visualisasi hasil rectification

3. **Disparity Computation** (15%)
   - Implementasi minimal 2 metode (BM dan SGM)
   - Post-processing untuk mengurangi noise
   - Perbandingan kualitas dan kecepatan

### Task 2: Depth Estimation Module (25%)

**Subtasks:**
1. **Disparity to Depth Conversion** (10%)
   - Konversi disparity ke metric depth
   - Handle invalid disparity values
   - Output depth dalam meter

2. **Depth Map Post-Processing** (15%)
   - Hole filling untuk missing depth
   - Temporal filtering untuk stabilitas
   - Edge-preserving smoothing

### Task 3: Obstacle Detection (20%)

**Subtasks:**
1. **Ground Plane Estimation** (10%)
   - RANSAC untuk estimasi ground plane
   - Segmentasi ground vs non-ground

2. **Obstacle Clustering** (10%)
   - Deteksi dan clustering obstacle points
   - Bounding box estimation
   - Jarak minimum ke obstacle terdekat

### Task 4: Integration & Visualization (20%)

**Subtasks:**
1. **Real-time Pipeline** (10%)
   - Integrasi semua modul dalam satu pipeline
   - Target minimum 15fps
   - Memory management yang efisien

2. **Visualization Dashboard** (10%)
   - RGB view dengan overlay depth
   - Bird's eye view representation
   - Obstacle warning indicator

---

## 📁 Struktur Direktori Project

```
project_adas_depth/
├── config/
│   ├── camera_params.yaml      # Parameter kalibrasi
│   └── pipeline_config.yaml    # Konfigurasi pipeline
├── modules/
│   ├── __init__.py
│   ├── stereo_calibration.py   # Modul kalibrasi
│   ├── stereo_matching.py      # BM dan SGM
│   ├── depth_processing.py     # Post-processing depth
│   ├── obstacle_detection.py   # Deteksi obstacle
│   └── visualization.py        # Fungsi visualisasi
├── data/
│   ├── calibration/            # Gambar kalibrasi
│   ├── test_sequences/         # Video/gambar test
│   └── results/                # Output results
├── tests/
│   ├── test_calibration.py     # Unit test
│   └── test_matching.py
├── main.py                     # Entry point
├── demo.py                     # Demo visualization
└── requirements.txt            # Dependencies
```

---

## 🔧 Panduan Implementasi

### Step 1: Setup Project
```python
# main.py - Entry point
from modules.stereo_calibration import StereoCalibrator
from modules.stereo_matching import StereoMatcher
from modules.depth_processing import DepthProcessor
from modules.obstacle_detection import ObstacleDetector
from modules.visualization import Visualizer

class ADASDepthSystem:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.calibrator = StereoCalibrator(...)
        self.matcher = StereoMatcher(...)
        self.processor = DepthProcessor(...)
        self.detector = ObstacleDetector(...)
        self.visualizer = Visualizer(...)
    
    def process_frame(self, left_img, right_img):
        # Implement full pipeline
        pass
```

### Step 2: Stereo Matching Module
```python
# modules/stereo_matching.py
class StereoMatcher:
    def __init__(self, method='sgm', config=None):
        self.method = method
        if method == 'bm':
            self.matcher = cv2.StereoBM_create(...)
        else:
            self.matcher = cv2.StereoSGBM_create(...)
    
    def compute(self, left_rect, right_rect):
        """Compute disparity with post-processing"""
        disparity = self.matcher.compute(left_rect, right_rect)
        disparity = self.post_process(disparity)
        return disparity
```

### Step 3: Obstacle Detection
```python
# modules/obstacle_detection.py
class ObstacleDetector:
    def __init__(self, config):
        self.ground_threshold = config['ground_threshold']
        self.min_obstacle_height = config['min_obstacle_height']
    
    def estimate_ground_plane(self, depth_map, K):
        """RANSAC ground plane estimation"""
        # Convert depth to 3D points
        # Fit plane using RANSAC
        # Return plane parameters (n, d)
        pass
    
    def detect_obstacles(self, depth_map, ground_plane):
        """Detect obstacles above ground plane"""
        # Segment non-ground points
        # Cluster into obstacles
        # Return bounding boxes and distances
        pass
```

---

## 📊 Kriteria Evaluasi

### Rubrik Penilaian

| Kriteria | Excellent (90-100) | Good (75-89) | Fair (60-74) | Poor (<60) |
|----------|-------------------|--------------|--------------|------------|
| **Stereo Pipeline (35%)** | Pipeline lengkap, error kalibrasi <0.3px, hasil excellent | Pipeline lengkap, error <0.5px, hasil baik | Pipeline partial, error <1px | Pipeline tidak berfungsi |
| **Depth Module (25%)** | Depth akurat, post-processing excellent | Depth reasonable, post-processing baik | Depth dengan noise tinggi | Depth tidak valid |
| **Obstacle Detection (20%)** | Deteksi akurat, false positive <5% | Deteksi cukup baik, FP <15% | Deteksi dengan banyak error | Tidak berfungsi |
| **Integration (20%)** | Real-time >20fps, UI excellent | >15fps, UI baik | >10fps, UI basic | Tidak real-time |

### Deliverables

1. **Source Code** (40%)
   - Clean, well-documented code
   - Modular architecture
   - Error handling

2. **Demo Video** (20%)
   - Durasi: 5-7 menit
   - Menunjukkan semua fitur
   - Narasi dalam Bahasa Indonesia

3. **Technical Report** (25%)
   - Maksimal 10 halaman
   - Include methodology, results, analysis
   - Format IEEE

4. **Presentation** (15%)
   - 10-15 menit
   - Live demo
   - Q&A session

---

## 📅 Timeline

| Minggu | Deliverable | Checkpoint |
|--------|-------------|------------|
| 1 | Project setup, stereo calibration | Calibration module working |
| 2 | Stereo matching implementation | Disparity map generated |
| 3 | Depth processing, obstacle detection | Basic detection working |
| 4 | Integration, visualization, testing | Full pipeline working |
| 5 | Documentation, video, presentation | Final submission |

---

## 📚 Referensi Tambahan

### Academic Papers
1. Hirschmuller, H. "Stereo Processing by Semiglobal Matching" (SGM paper)
2. Geiger, A. "Are we ready for autonomous driving? The KITTI benchmark"

### Datasets
- **Middlebury Stereo**: https://vision.middlebury.edu/stereo/
- **KITTI**: https://www.cvlibs.net/datasets/kitti/
- **Driving Stereo**: https://drivingstereo-dataset.github.io/

### Code References
- OpenCV Stereo Tutorial: https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html
- MiDaS: https://github.com/isl-org/MiDaS

---

## 💡 Tips dan Best Practices

1. **Kalibrasi yang Baik adalah Kunci**
   - Gunakan minimal 20 gambar checkerboard
   - Pastikan checkerboard terlihat di berbagai posisi dan orientasi
   - RMS error target < 0.5 pixel

2. **Parameter Tuning**
   - Mulai dengan parameter default
   - Tune satu parameter pada satu waktu
   - Dokumentasikan setiap perubahan

3. **Real-time Optimization**
   - Gunakan image pyramids untuk speed
   - Consider GPU acceleration (cv2.cuda)
   - Profile kode untuk bottleneck

4. **Testing**
   - Test pada berbagai kondisi pencahayaan
   - Test pada berbagai jarak
   - Validasi dengan ground truth jika tersedia

---

## ⚠️ Catatan Penting

1. **Keamanan**: Sistem ini untuk pembelajaran, BUKAN untuk deployment di kendaraan nyata
2. **Dataset**: Gunakan dataset publik, jangan merekam di jalan raya
3. **Dokumentasi**: Semua kode harus didokumentasi dengan baik
4. **Plagiarisme**: Kode harus original, cite sumber jika menggunakan referensi
