# Bab 4: Model Fitting dan Feature Matching

## 1. Definisi

**Model Fitting** adalah proses menemukan model matematika (seperti garis, lingkaran, atau transformasi geometri) yang paling sesuai dengan data observasi. Dalam computer vision, ini digunakan untuk mendeteksi bentuk, mencocokkan gambar, dan melacak gerakan.

**Feature Matching** adalah proses menemukan korespondensi antara fitur-fitur (titik-titik khusus) pada dua atau lebih gambar yang berbeda.

### Mengapa Model Fitting Penting?

```
┌─────────────────────────────────────────────────────────────┐
│                    APLIKASI MODEL FITTING                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🚗 Self-Driving Cars     📸 Panorama Stitching            │
│  ├── Lane detection       ├── Image alignment              │
│  └── Road sign detection  └── Homography estimation        │
│                                                             │
│  🏭 Industrial Vision     🎮 Augmented Reality              │
│  ├── Object measurement   ├── Marker detection             │
│  └── Defect detection     └── Pose estimation              │
│                                                             │
│  🔬 Medical Imaging       🎥 Video Stabilization            │
│  ├── Cell detection       ├── Motion estimation            │
│  └── Organ segmentation   └── Feature tracking             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Konsep Utama

### 2.1 Feature Detection & Description

Sebelum melakukan matching, kita perlu mendeteksi dan mendeskripsikan fitur pada gambar.

#### Jenis-jenis Feature Detector:

| Detector | Karakteristik | Kecepatan | Robustness |
|----------|---------------|-----------|------------|
| **Harris Corner** | Sudut/corner detection | Cepat | Rendah |
| **SIFT** | Scale-invariant, rotation-invariant | Lambat | Tinggi |
| **SURF** | Faster SIFT alternative | Sedang | Tinggi |
| **ORB** | Binary descriptor, sangat cepat | Sangat Cepat | Sedang |
| **AKAZE** | Non-linear scale space | Sedang | Tinggi |

```
Feature Detection Pipeline:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Gambar     │───▶│   Detect     │───▶│  Describe    │
│   Input      │    │  Keypoints   │    │  Features    │
└──────────────┘    └──────────────┘    └──────────────┘
                           │                    │
                           ▼                    ▼
                    [x1, y1, ...]         [128-d vector]
                    [x2, y2, ...]         [256-d vector]
                          ...                  ...
```

### 2.2 Feature Matching

Setelah fitur dideteksi, kita perlu mencocokkan fitur antar gambar.

#### Metode Matching:

1. **Brute-Force Matcher**
   - Membandingkan setiap descriptor dengan semua descriptor lain
   - Akurat tapi lambat untuk dataset besar

2. **FLANN (Fast Library for Approximate Nearest Neighbors)**
   - Menggunakan struktur data khusus untuk pencarian cepat
   - Lebih cepat, sedikit kurang akurat

3. **Ratio Test (Lowe's Ratio)**
   - Membandingkan jarak ke match terbaik dengan match kedua
   - Menghilangkan ambiguous matches
   - Threshold umum: 0.7 - 0.8

```python
# Ratio Test Example
if distance_to_best_match / distance_to_second_best < 0.75:
    accept_match()
else:
    reject_match()
```

### 2.3 RANSAC (Random Sample Consensus)

RANSAC adalah algoritma robust untuk estimasi model dengan data yang mengandung outliers.

```
┌─────────────────────────────────────────────────────────────┐
│                    ALGORITMA RANSAC                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SAMPLE: Pilih subset minimum titik secara random        │
│     ─────────────────────────────────────────────────       │
│     Untuk garis: 2 titik                                    │
│     Untuk homography: 4 titik                               │
│                                                             │
│  2. MODEL: Hitung model dari sample                         │
│     ─────────────────────────────────────────────────       │
│     Fit garis/plane/homography ke titik-titik sample        │
│                                                             │
│  3. CONSENSUS: Hitung berapa titik yang cocok (inliers)     │
│     ─────────────────────────────────────────────────       │
│     Titik dengan error < threshold adalah inlier            │
│                                                             │
│  4. REPEAT: Ulangi N kali, simpan model terbaik             │
│     ─────────────────────────────────────────────────       │
│     Model terbaik = model dengan inliers terbanyak          │
│                                                             │
│  5. REFINE: Re-estimate model menggunakan semua inliers     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Jumlah Iterasi RANSAC:

$$N = \frac{\log(1-p)}{\log(1-w^n)}$$

Dimana:
- $N$ = jumlah iterasi
- $p$ = probabilitas sukses yang diinginkan (biasanya 0.99)
- $w$ = rasio inliers dalam data
- $n$ = jumlah titik minimum untuk fit model

### 2.4 Hough Transform

Hough Transform digunakan untuk mendeteksi bentuk parametrik (garis, lingkaran) dalam gambar.

#### Hough Line Transform:

Setiap titik $(x, y)$ dalam gambar dapat berada pada banyak garis. Dalam parameter space $(\rho, \theta)$:

$$\rho = x \cos\theta + y \sin\theta$$

```
Image Space              Parameter Space (Hough Space)
     y                          θ
     │    •                     │
     │   /                      │    ╲
     │  /                       │     ╲
     │ /                        │      ●  (peak = line detected)
     │/                         │     /
     └────────── x              └────────── ρ

Satu titik → kurva sinusoidal di Hough space
Titik-titik segaris → kurva bertemu di satu titik
```

#### Hough Circle Transform:

Untuk lingkaran dengan parameter $(a, b, r)$:

$$(x-a)^2 + (y-b)^2 = r^2$$

### 2.5 Homography

Homography adalah transformasi proyektif yang memetakan titik-titik dari satu plane ke plane lain.

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

```
┌─────────────────────────────────────────────────────────────┐
│                    APLIKASI HOMOGRAPHY                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  • Panorama Stitching                                       │
│    ├── Align overlapping images                             │
│    └── Warp dan blend                                       │
│                                                             │
│  • Perspective Correction                                   │
│    ├── Document scanning (bird's eye view)                  │
│    └── Whiteboard rectification                             │
│                                                             │
│  • Augmented Reality                                        │
│    ├── Planar marker tracking                               │
│    └── Virtual object placement                             │
│                                                             │
│  • Sports Analytics                                         │
│    ├── Court/field homography                               │
│    └── Player position mapping                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.6 Optical Flow

Optical Flow mengestimasi gerakan piksel antar frame video.

#### Lucas-Kanade Method (Sparse Optical Flow):
- Melacak fitur tertentu antar frame
- Asumsi: gerakan konstan dalam neighborhood kecil

#### Farneback Method (Dense Optical Flow):
- Menghitung flow untuk setiap piksel
- Lebih lambat tapi memberikan informasi lengkap

```
Frame t              Frame t+1            Optical Flow
┌───────────┐        ┌───────────┐        ┌───────────┐
│     ●     │   ──▶  │        ●  │   =    │     ──▶   │
│           │        │           │        │           │
│  ●        │   ──▶  │     ●     │   =    │  ──▶      │
└───────────┘        └───────────┘        └───────────┘
```

---

## 3. Diagram dan Ilustrasi

### Pipeline Feature Matching dan Homography

```
┌──────────────────────────────────────────────────────────────────────┐
│                 FEATURE MATCHING PIPELINE                             │
└──────────────────────────────────────────────────────────────────────┘

Image 1                              Image 2
┌─────────────┐                      ┌─────────────┐
│             │                      │             │
│    ● ●      │                      │      ● ●    │
│  ●          │                      │          ●  │
│      ●      │                      │        ●    │
└─────────────┘                      └─────────────┘
       │                                    │
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│  Feature    │                      │  Feature    │
│  Detection  │                      │  Detection  │
│  (ORB/SIFT) │                      │  (ORB/SIFT) │
└─────────────┘                      └─────────────┘
       │                                    │
       ▼                                    ▼
┌─────────────┐                      ┌─────────────┐
│  Compute    │                      │  Compute    │
│ Descriptors │                      │ Descriptors │
└─────────────┘                      └─────────────┘
       │                                    │
       └──────────────┬─────────────────────┘
                      ▼
              ┌──────────────┐
              │   Feature    │
              │   Matching   │
              │ (BF/FLANN)   │
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  Ratio Test  │
              │   Filtering  │
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │   RANSAC     │
              │ (Homography) │
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │   Output:    │
              │ - Inliers    │
              │ - H matrix   │
              │ - Warped img │
              └──────────────┘
```

### Visualisasi RANSAC

```
Data dengan Outliers            Setelah RANSAC
        ●                              ●  (outlier)
    ● ● ● ●                        ● ● ● ●
  ● ● ● ● ● ●        ──▶       ══════════════ (fitted line)
    ● ● ● ●                        ● ● ● ●
        ●                              ●  (outlier)
      ●                              ●    (outlier)

  ● = data point                ═ = estimated model
                                ● = inliers
                                ● = outliers (ignored)
```

---

## 4. Contoh Kasus Industri dan Dunia Nyata

### Kasus 1: Sistem Lane Detection pada Self-Driving Cars

**Perusahaan:** Tesla, Waymo, Mobileye

**Teknologi yang Digunakan:**
- Hough Line Transform untuk deteksi garis lane
- RANSAC untuk robust line fitting
- Perspective transform untuk bird's eye view

```
Camera View                Bird's Eye View
┌─────────────┐            ┌─────────────┐
│    /   \    │    ──▶     │  │       │  │
│   /     \   │  Inverse   │  │       │  │
│  /       \  │ Perspective│  │       │  │
│ /         \ │ Transform  │  │       │  │
└─────────────┘            └─────────────┘
```

### Kasus 2: Panorama Photography (Google Photo Sphere)

**Teknologi:**
- SIFT/ORB untuk feature detection
- Feature matching antar gambar overlap
- RANSAC + Homography untuk alignment
- Image blending untuk seamless result

### Kasus 3: Document Scanner (CamScanner, Adobe Scan)

**Proses:**
1. Edge detection untuk menemukan batas dokumen
2. Hough Line Transform untuk mendeteksi 4 sisi
3. Corner detection di intersection garis
4. Homography untuk perspective correction

### Kasus 4: Sports Analytics (FIFA, Hawk-Eye)

**Aplikasi:**
- Mapping posisi pemain ke field diagram
- Offside detection
- Ball tracking

**Teknologi:**
- Homography antara camera view dan field template
- Feature tracking dengan optical flow
- RANSAC untuk robust estimation

### Kasus 5: Augmented Reality Markers (Vuforia, ARToolkit)

**Proses:**
1. Detect marker pattern dalam gambar
2. Extract corner points
3. Compute homography ke canonical marker
4. Derive 3D pose dari homography
5. Render virtual object

---

## 5. Ringkasan

### Tabel Perbandingan Teknik

| Teknik | Input | Output | Use Case |
|--------|-------|--------|----------|
| **Harris Corner** | Grayscale image | Corner points | Basic feature detection |
| **ORB** | Image | Keypoints + Descriptors | Fast matching |
| **SIFT** | Image | Keypoints + Descriptors | Robust matching |
| **Brute-Force** | 2 sets descriptors | Matches | Small dataset matching |
| **FLANN** | 2 sets descriptors | Matches | Large dataset matching |
| **RANSAC** | Matches + Model type | Inliers + Model params | Robust estimation |
| **Hough Lines** | Edge image | Line parameters | Line detection |
| **Hough Circles** | Grayscale | Circle parameters | Circle detection |
| **Homography** | Point correspondences | 3×3 matrix | Planar transformation |
| **Lucas-Kanade** | 2 frames + points | Flow vectors | Sparse tracking |
| **Farneback** | 2 frames | Dense flow field | Motion analysis |

### Key Takeaways

1. **Feature Detection** adalah fondasi untuk banyak aplikasi CV
2. **RANSAC** essential untuk handling outliers di real-world data
3. **Hough Transform** powerful untuk shape detection
4. **Homography** kunci untuk planar transformations
5. **Optical Flow** fundamental untuk video analysis

---

## 6. Deskripsi Tugas Video

### Judul Video
**"Implementasi Model Fitting dan Feature Matching untuk Aplikasi Computer Vision"**

### Durasi
8-12 menit

### Struktur Video yang Harus Dibuat

#### Pembukaan (0:00 - 0:30)
- [ ] Perkenalan diri (nama, NIM)
- [ ] Judul materi yang akan dibahas
- [ ] Overview singkat tentang apa yang akan ditunjukkan

#### Bagian 1: Feature Detection & Matching (0:30 - 3:00)
- [ ] Jelaskan konsep feature detection
- [ ] Demo Harris Corner Detection
- [ ] Demo ORB feature detection
- [ ] Demo feature matching antara 2 gambar
- [ ] Jelaskan ratio test dan fungsinya

#### Bagian 2: RANSAC (3:00 - 5:00)
- [ ] Jelaskan algoritma RANSAC step-by-step
- [ ] Demo RANSAC untuk line fitting
- [ ] Tunjukkan perbedaan dengan/tanpa RANSAC
- [ ] Jelaskan konsep inliers vs outliers

#### Bagian 3: Hough Transform (5:00 - 7:00)
- [ ] Jelaskan konsep Hough space
- [ ] Demo Hough Line Transform
- [ ] Demo Hough Circle Transform
- [ ] Aplikasi: lane detection atau object detection

#### Bagian 4: Homography & Optical Flow (7:00 - 9:00)
- [ ] Jelaskan apa itu homography
- [ ] Demo perspective correction
- [ ] Demo panorama stitching sederhana
- [ ] Demo optical flow tracking

#### Bagian 5: Eksperimen (9:00 - 11:00)
- [ ] Variasi parameter (threshold, iterations)
- [ ] Perbandingan hasil dengan parameter berbeda
- [ ] Analisis trade-off

#### Penutup (11:00 - 12:00)
- [ ] Ringkasan materi yang sudah dibahas
- [ ] Aplikasi real-world yang sudah dicoba
- [ ] Kesimpulan dan pembelajaran
- [ ] Penutup

### Checklist Teknis Video
- [ ] Resolusi minimal 720p
- [ ] Audio jelas dan tidak ada background noise
- [ ] Screen recording mencakup code dan output
- [ ] Setiap demo dijelaskan sebelum dijalankan
- [ ] Parameter yang diubah di-highlight
- [ ] Hasil ditampilkan dengan jelas

---

*Materi ini merupakan bagian dari Praktikum Computer Vision berdasarkan buku "Computer Vision: Algorithms and Applications, 2nd Edition" oleh Richard Szeliski*
