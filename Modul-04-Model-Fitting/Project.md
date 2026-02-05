# Project Bab 4: AutoStitch - Sistem Panorama Otomatis

## Latar Belakang Cerita

Sebuah startup properti **"VirtualTour.id"** sedang mengembangkan platform virtual tour untuk pemasaran properti. Mereka membutuhkan sistem yang dapat secara otomatis menggabungkan foto-foto yang diambil dari satu lokasi menjadi panorama 360° yang seamless.

Kamu dipekerjakan sebagai **Computer Vision Engineer** untuk membangun modul **AutoStitch** - sistem yang dapat:
1. Menerima input beberapa foto dengan overlap
2. Mendeteksi dan mencocokkan fitur antar foto
3. Menghitung transformasi (homography) untuk setiap pasangan
4. Menggabungkan foto menjadi panorama dengan blending yang halus

## Deskripsi Project

### Tujuan
Membangun sistem panorama stitching otomatis yang dapat menggabungkan 2-5 gambar menjadi panorama yang seamless.

### Fitur yang Harus Diimplementasikan

#### 1. Feature Detector Module
```
Input: Gambar
Output: Keypoints dan Descriptors

Fungsi:
- detect_features(image, method='orb')
- Mendukung minimal 2 metode: ORB dan SIFT
- Return: keypoints, descriptors
```

#### 2. Feature Matcher Module
```
Input: Descriptors dari 2 gambar
Output: Matched keypoints

Fungsi:
- match_features(desc1, desc2, method='bf')
- Implementasi ratio test
- Filtering outliers
- Return: good_matches
```

#### 3. Homography Estimator Module
```
Input: Matched keypoints dari 2 gambar
Output: Homography matrix

Fungsi:
- estimate_homography(pts1, pts2)
- Menggunakan RANSAC untuk robustness
- Return: H matrix (3×3), inlier_mask
```

#### 4. Image Warper Module
```
Input: Gambar dan Homography matrix
Output: Warped image

Fungsi:
- warp_image(image, H, output_size)
- Handle boundary dan padding
- Return: warped_image
```

#### 5. Image Blender Module
```
Input: Dua gambar yang sudah di-align
Output: Blended panorama

Fungsi:
- blend_images(img1, img2, method='linear')
- Minimal 2 metode: simple overlay dan linear blending
- Return: blended_image
```

#### 6. Panorama Pipeline
```
Input: List gambar (2-5 gambar)
Output: Panorama hasil

Fungsi:
- create_panorama(images)
- Menggabungkan semua modul di atas
- Handling untuk multiple images
- Return: panorama_image
```

## Spesifikasi Teknis

### Input
- Format: JPG, PNG
- Minimum overlap: 20%
- Jumlah gambar: 2-5 gambar
- Resolusi: minimal 640×480

### Output
- Panorama dalam format JPG/PNG
- Visualization dengan:
  - Feature matches untuk setiap pasangan
  - Homography transformation visualization
  - Step-by-step stitching process
- Metrics:
  - Jumlah features terdeteksi per gambar
  - Jumlah matches per pasangan
  - Jumlah inliers
  - Processing time

### Quality Requirements
- Seamless blending (tidak ada garis terlihat)
- Geometric accuracy (tidak ada distorsi signifikan)
- Processing time < 30 detik untuk 3 gambar HD

## Struktur Project

```
AutoStitch_NamaKelompok/
├── src/
│   ├── __init__.py
│   ├── feature_detector.py     # Modul 1
│   ├── feature_matcher.py      # Modul 2
│   ├── homography.py           # Modul 3
│   ├── warper.py               # Modul 4
│   ├── blender.py              # Modul 5
│   └── panorama.py             # Modul 6 (Pipeline)
├── tests/
│   ├── test_detector.py
│   ├── test_matcher.py
│   ├── test_homography.py
│   └── test_panorama.py
├── examples/
│   ├── input/
│   │   ├── set1/               # Contoh set gambar 1
│   │   ├── set2/               # Contoh set gambar 2
│   │   └── set3/               # Contoh set gambar 3
│   └── output/
│       ├── panorama1.jpg
│       ├── panorama2.jpg
│       └── panorama3.jpg
├── docs/
│   └── report.pdf
├── main.py
├── requirements.txt
└── README.md
```

## Tahapan Pengerjaan

### Minggu 1: Foundation
1. Setup project structure
2. Implementasi Feature Detector Module
3. Implementasi Feature Matcher Module
4. Unit tests untuk kedua modul

### Minggu 2: Core Algorithm
1. Implementasi Homography Estimator
2. Implementasi Image Warper
3. Implementasi Image Blender
4. Integration testing

### Minggu 3: Pipeline & Polish
1. Implementasi Panorama Pipeline
2. Testing dengan berbagai dataset
3. Optimization dan debugging
4. Documentation dan report

## Contoh Penggunaan

### Basic Usage
```python
from src.panorama import PanoramaStitcher

# Inisialisasi
stitcher = PanoramaStitcher(detector='orb', matcher='bf')

# Load images
images = ['img1.jpg', 'img2.jpg', 'img3.jpg']

# Create panorama
panorama = stitcher.stitch(images)

# Save result
cv2.imwrite('panorama.jpg', panorama)
```

### Dengan Visualization
```python
# Create panorama dengan visualization
panorama, viz = stitcher.stitch(images, visualize=True)

# viz berisi:
# - viz['matches']: visualisasi matches per pasangan
# - viz['warped']: gambar setelah warping
# - viz['steps']: step-by-step stitching
```

### CLI Interface (Bonus)
```bash
python main.py --input img1.jpg img2.jpg img3.jpg --output panorama.jpg
python main.py --input ./my_photos/ --output result.jpg --visualize
```

## Kriteria Penilaian

### Fungsionalitas (40%)
- [ ] Semua modul berfungsi dengan benar
- [ ] Pipeline menghasilkan panorama yang valid
- [ ] Mendukung minimal 2 metode feature detection
- [ ] Mendukung minimal 2 metode blending
- [ ] Error handling yang proper

### Kualitas Output (25%)
- [ ] Panorama seamless (tidak ada visible seams)
- [ ] Geometri akurat (minimal distortion)
- [ ] Color consistency antar gambar
- [ ] Handling edge cases (low overlap, few features)

### Code Quality (20%)
- [ ] Modular dan well-organized
- [ ] Documented dengan docstrings
- [ ] Clean code dan PEP8 compliant
- [ ] Unit tests dengan coverage memadai

### Documentation (15%)
- [ ] README lengkap dengan instruksi
- [ ] Report dengan penjelasan algoritma
- [ ] Visualization hasil yang informatif
- [ ] Analisis kelebihan dan kekurangan

## Bonus Points (+15 max)

| Bonus | Points |
|-------|--------|
| GUI interface (Tkinter/PyQt) | +5 |
| Video panorama (dari video input) | +4 |
| 360° cylindrical/spherical projection | +3 |
| Exposure compensation | +3 |
| Multi-band blending | +2 |
| Real-time stitching (webcam) | +3 |
| Mobile app wrapper | +3 |

## Dataset untuk Testing

### Set 1: Indoor Scene
- 3 gambar kamar/ruangan
- Overlap: ~30%
- Challenge: textured walls, furniture

### Set 2: Outdoor Landscape
- 4 gambar pemandangan
- Overlap: ~25%
- Challenge: sky blending, moving objects

### Set 3: Document/Whiteboard
- 2 gambar dokumen besar
- Overlap: ~40%
- Challenge: perspective correction

### Set 4: Night Scene (Advanced)
- 3 gambar malam hari
- Overlap: ~30%
- Challenge: low light, noise

## Submission Requirements

### Yang Harus Dikumpulkan
1. Source code (ZIP)
2. Report (PDF, max 10 halaman)
3. Demo video (5-10 menit)
4. Sample outputs (minimal 3 panorama)

### Deadline
- Week 3 setelah assignment

### Format Nama File
```
AutoStitch_[NIM1]_[NIM2]_[NIM3].zip
```

## Referensi

1. Brown, M., & Lowe, D. G. (2007). "Automatic Panoramic Image Stitching using Invariant Features"
2. Szeliski, R. (2022). "Computer Vision: Algorithms and Applications" - Chapter 8
3. OpenCV Documentation: Feature Detection and Description
4. OpenCV Documentation: Feature Matching

## FAQ

**Q: Bolehkah menggunakan cv2.Stitcher?**
A: Tidak. Tujuan project adalah memahami algoritma, bukan menggunakan high-level API.

**Q: Bagaimana jika gambar tidak punya cukup overlap?**
A: Implementasikan error handling yang mengembalikan pesan yang informatif.

**Q: Apakah harus real-time?**
A: Tidak harus, tapi akan ada bonus untuk real-time implementation.

**Q: Bolehkah menggunakan deep learning untuk feature detection?**
A: Boleh sebagai bonus/tambahan, tapi harus ada implementasi traditional (ORB/SIFT) juga.

---

*Project ini merupakan bagian dari Praktikum Computer Vision Bab 4: Model Fitting*
