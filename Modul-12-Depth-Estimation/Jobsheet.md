# JOBSHEET PRAKTIKUM BAB 12
# DEPTH ESTIMATION (STEREO MATCHING)

---

## 🎯 1. Tujuan Praktikum

### Tujuan Umum
Mahasiswa mampu memahami, mengimplementasikan, dan menganalisis berbagai teknik estimasi kedalaman (depth estimation) menggunakan stereo vision dan deep learning, serta menerapkannya dalam aplikasi computer vision seperti autonomous driving, robotics, dan augmented reality.

### Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan Pembelajaran | Kompetensi yang Dikembangkan | Penerapan Industri |
|----|-----------|---------------------|------------------------------|-------------------|
| 1 | Stereo Camera Calibration | Memahami dan melakukan kalibrasi stereo camera dengan akurasi tinggi (RMS error < 0.5 pixel) | Menguasai konsep parameter intrinsik, extrinsik, dan rectification mapping | Robot vision systems, 3D scanning, industrial inspection |
| 2 | Stereo Rectification | Memahami proses rectification dan transformasi epipolar untuk optimasi pencarian korespondensi | Implementasi image warping dan validasi epipolar constraints | ADAS (Advanced Driver Assistance Systems), drone navigation |
| 3 | Block Matching (BM) | Mengimplementasikan algoritma stereo matching berbasis window-based correlation | Analisis trade-off antara speed dan accuracy, parameter tuning | Real-time robotics, warehouse automation, AGV |
| 4 | Semi-Global Matching (SGM) | Menerapkan SGM untuk hasil depth yang lebih smooth dengan global optimization | Memahami path aggregation, smoothness constraints, dan post-processing | Autonomous vehicles (Tesla, Waymo), mapping & SLAM |
| 5 | Disparity to Depth Conversion | Mengkonversi disparity map ke metric depth menggunakan triangulation principles | Kalibrasi baseline dan focal length, handling invalid disparities | Distance measurement, collision avoidance, parking assistance |
| 6 | Monocular Depth Estimation | Menggunakan deep learning (MiDaS, DPT) untuk estimasi depth dari single image | Transfer learning, model inference, relative vs absolute depth | AR filters (Instagram, Snapchat), smartphone photography |
| 7 | Depth Map Post-Processing | Menerapkan filtering, hole filling, dan temporal smoothing | Bilateral filtering, WLS filtering, median filtering | Production-ready systems, noise reduction |
| 8 | Depth-based Applications | Implementasi obstacle detection, 3D reconstruction, dan depth segmentation | Point cloud generation, plane fitting, clustering | Safety systems, scene understanding, virtual reality |

---

## 🔧 2. Alat dan Bahan

### 2.1 Perangkat Keras
| Alat | Spesifikasi Minimum | Spesifikasi Rekomendasi | Keterangan |
|------|-------------------|------------------------|------------|
| Komputer/Laptop | RAM 8GB, CPU multi-core | RAM 16GB+, GPU NVIDIA (4GB+ VRAM) | GPU untuk deep learning models (MiDaS, DPT) |
| Stereo Camera (opsional) | ZED, RealSense D435, OAK-D | RealSense D455, ZED 2i | Untuk capture stereo real-time |
| Webcam | 2 unit identik (minimal 720p) | 2 unit 1080p dengan mounting rig | Untuk DIY stereo setup |
| Printer Checkerboard | - | - | Untuk mencetak pattern kalibrasi |

### 2.2 Perangkat Lunak
| Software | Versi | Fungsi | Instalasi |
|----------|-------|--------|-----------|
| Python | 3.8 - 3.11 | Bahasa pemrograman utama | `python --version` |
| OpenCV | 4.8+ | Stereo algorithms (BM, SGM, WLS filter) | `pip install opencv-contrib-python` |
| NumPy | 1.24+ | Array operations dan matrix math | `pip install numpy` |
| PyTorch | 2.0+ | Deep learning framework (MiDaS) | `pip install torch torchvision` |
| Timm | 0.9+ | Vision models backbone | `pip install timm` |
| Open3D | 0.17+ | 3D visualization dan point clouds | `pip install open3d` |
| Matplotlib | 3.7+ | Plotting dan visualization | `pip install matplotlib` |
| SciPy | 1.10+ | Scientific computing | `pip install scipy` |
| PIL/Pillow | 10.0+ | Image I/O operations | `pip install Pillow` |

### 2.3 Data dan Resource yang Dibutuhkan
| Resource | Sumber | Keterangan |
|----------|--------|------------|
| **Gambar Stereo Pairs** | - Middlebury Dataset<br>- KITTI Dataset<br>- Driving Stereo Dataset | Download dari official websites |
| **Checkerboard Pattern** | - 9×6 inner corners (recommended)<br>- 7×5 alternative<br>- Square size: 25mm | Print dengan akurasi tinggi |
| **Pre-trained Models** | - MiDaS v3.1 (DPT-Large)<br>- MiDaS v2.1 (Small)<br>- Depth-Anything | Auto-download via PyTorch Hub |
| **Sample Videos** | - Driving scenes<br>- Indoor navigation<br>- Outdoor scenes | Untuk testing real-world scenarios |

### 2.4 Instalasi Lengkap Library

#### A. Instalasi via pip (Recommended)
```bash
# Core libraries
pip install opencv-contrib-python==4.8.1.78
pip install numpy==1.24.3
pip install matplotlib==3.7.2
pip install scipy==1.10.1
pip install Pillow==10.0.0

# Deep learning
pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cu118
pip install timm==0.9.5

# 3D visualization
pip install open3d==0.17.0

# Optional: untuk visualisasi interaktif
pip install plotly==5.15.0
pip install dash==2.11.1
```

#### B. Instalasi via Conda (Alternative)
```bash
conda create -n depth_estimation python=3.10
conda activate depth_estimation
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
conda install -c conda-forge opencv matplotlib numpy scipy pillow open3d
pip install timm
```

#### C. Verifikasi Instalasi
```bash
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import torch; print('PyTorch:', torch.__version__, 'CUDA:', torch.cuda.is_available())"
python -c "import open3d; print('Open3D:', open3d.__version__)"
python -c "import timm; print('Timm:', timm.__version__)"
```

### 2.5 Download Sample Data
Gunakan script berikut untuk download dataset:

```python
# download_sample_data.py
import urllib.request
import zipfile
import os

DATASETS = {
    'middlebury_2014': 'https://vision.middlebury.edu/stereo/data/scenes2014/zip/Adirondack-perfect.zip',
    'sample_stereo': 'https://github.com/opencv/opencv_extra/raw/master/testdata/cv/stereo/',
}

def download_dataset(name, url, extract_to='./data'):
    os.makedirs(extract_to, exist_ok=True)
    filename = os.path.join(extract_to, name + '.zip')
    
    if not os.path.exists(filename):
        print(f'Downloading {name}...')
        urllib.request.urlretrieve(url, filename)
        print(f'Extracting {name}...')
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f'{name} ready!')
    else:
        print(f'{name} already exists.')

# Download all datasets
for name, url in DATASETS.items():
    download_dataset(name, url)
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

> **Catatan Otomasi Tampilan:**
> Semua program praktikum akan menutup window visualisasi secara otomatis setelah ~2 detik.
> Jika ingin menutup lebih cepat, tekan tombol **q**.

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
