# Materi Praktikum
## Bab 3: Pemrosesan Citra (Image Processing)

---

## 🎯 Tujuan Pembelajaran

Setelah menyelesaikan bab ini, mahasiswa diharapkan mampu:
1. Memahami dan mengimplementasikan operasi titik (point operations)
2. Menerapkan histogram equalization dan color manipulation
3. Memahami dan menggunakan berbagai jenis filter (smoothing, sharpening)
4. Mengimplementasikan edge detection dan morphological operations
5. Menerapkan teknik-teknik pemrosesan citra untuk aplikasi nyata

---

## 📖 Definisi dan Konsep Dasar

### Apa itu Image Processing?

**Pemrosesan Citra (Image Processing)** adalah manipulasi matematis pada gambar digital untuk menghasilkan gambar yang lebih baik atau mengekstrak informasi yang berguna. Berbeda dengan Computer Vision yang berfokus pada "memahami" gambar, image processing lebih fokus pada "memodifikasi" atau "meningkatkan kualitas" gambar.

### Klasifikasi Operasi Image Processing

```
Image Processing Operations
├── Point Operations (Per-Pixel)
│   ├── Brightness adjustment
│   ├── Contrast adjustment
│   ├── Gamma correction
│   ├── Thresholding
│   └── Color space conversion
│
├── Neighborhood Operations (Filtering)
│   ├── Smoothing/Blurring
│   │   ├── Mean filter
│   │   ├── Gaussian filter
│   │   ├── Median filter
│   │   └── Bilateral filter
│   │
│   ├── Sharpening
│   │   ├── Unsharp masking
│   │   └── Laplacian
│   │
│   └── Edge Detection
│       ├── Sobel
│       ├── Canny
│       └── Laplacian of Gaussian
│
├── Morphological Operations
│   ├── Erosion
│   ├── Dilation
│   ├── Opening
│   ├── Closing
│   └── Gradient
│
└── Global Operations
    ├── Histogram equalization
    ├── Fourier transform
    └── Image pyramids
```

---

## 📊 Konsep Utama

### 1. Point Operations (Operasi Titik)

Point operations memodifikasi setiap piksel secara independen, tanpa mempertimbangkan piksel tetangga.

#### A. Brightness Adjustment (Kecerahan)
```python
g(x,y) = f(x,y) + β

# Di mana:
# f(x,y) = nilai piksel original
# g(x,y) = nilai piksel hasil
# β = nilai brightness (positif = lebih terang, negatif = lebih gelap)
```

#### B. Contrast Adjustment (Kontras)
```python
g(x,y) = α × f(x,y)

# Di mana:
# α > 1 = kontras meningkat
# α < 1 = kontras menurun
```

#### C. Gamma Correction
```python
g(x,y) = c × f(x,y)^γ

# Di mana:
# γ < 1 = gambar lebih terang (highlight shadows)
# γ > 1 = gambar lebih gelap (enhance highlights)
```

Gamma correction penting untuk:
- Menyesuaikan tampilan pada monitor berbeda
- Menormalkan gambar dengan pencahayaan berbeda
- Preprocessing untuk algoritma machine learning

#### D. Thresholding
```python
Binary:     g(x,y) = 255 if f(x,y) > T else 0
Truncate:   g(x,y) = T if f(x,y) > T else f(x,y)
To Zero:    g(x,y) = f(x,y) if f(x,y) > T else 0
```

### 2. Histogram Operations

#### A. Histogram
Histogram menunjukkan distribusi intensitas piksel dalam gambar.

```
Histogram Gambar Gelap:     Histogram Gambar Terang:    Histogram Low Contrast:
    │                           │                           │
    │▓▓▓                       │          ▓▓▓              │
    │▓▓▓▓▓                     │         ▓▓▓▓▓             │       ▓▓▓▓
    │▓▓▓▓▓▓                    │        ▓▓▓▓▓▓             │      ▓▓▓▓▓▓
    └────────────              └────────────               └────────────
    0         255               0         255               0         255
```

#### B. Histogram Equalization
Teknik untuk meningkatkan kontras dengan menyebarkan distribusi intensitas secara merata.

**Langkah-langkah:**
1. Hitung histogram asli
2. Hitung Cumulative Distribution Function (CDF)
3. Normalisasi CDF
4. Map nilai piksel ke nilai baru menggunakan CDF

```python
# Formula
s_k = (L-1) × CDF(r_k)

# Di mana:
# s_k = nilai output untuk intensitas k
# L = jumlah level (256 untuk 8-bit)
# CDF(r_k) = cumulative distribution function pada intensitas k
```

#### C. CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Histogram equalization pada region lokal (tiles)
- Clip limit untuk menghindari over-amplification noise
- Lebih baik untuk gambar dengan variasi pencahayaan

### 3. Spatial Filtering (Konvolusi)

#### A. Konsep Konvolusi

Konvolusi menghitung nilai piksel baru berdasarkan piksel tetangga dengan kernel/filter.

```
                    Kernel (3×3)
     Image         ┌───┬───┬───┐
┌───┬───┬───┐      │ k₁│ k₂│ k₃│
│ a │ b │ c │      ├───┼───┼───┤
├───┼───┼───┤  ⊗   │ k₄│ k₅│ k₆│   =   Result
│ d │ e │ f │      ├───┼───┼───┤
├───┼───┼───┤      │ k₇│ k₈│ k₉│
│ g │ h │ i │      └───┴───┴───┘
└───┴───┴───┘

Result = a×k₁ + b×k₂ + c×k₃ + d×k₄ + e×k₅ + f×k₆ + g×k₇ + h×k₈ + i×k₉
```

#### B. Smoothing Filters

**Mean Filter (Box Filter):**
```
┌───┬───┬───┐
│1/9│1/9│1/9│    Efek: Blur sederhana
├───┼───┼───┤    Kelebihan: Cepat
│1/9│1/9│1/9│    Kekurangan: Blur edges
├───┼───┼───┤
│1/9│1/9│1/9│
└───┴───┴───┘
```

**Gaussian Filter:**
```
┌───────┬───────┬───────┐
│ 1/16  │ 2/16  │ 1/16  │    Efek: Blur natural
├───────┼───────┼───────┤    Kelebihan: Smooth, preserves edges better
│ 2/16  │ 4/16  │ 2/16  │    Parameter: σ (sigma) mengontrol blur amount
├───────┼───────┼───────┤
│ 1/16  │ 2/16  │ 1/16  │
└───────┴───────┴───────┘
```

**Median Filter:**
- Non-linear filter
- Ganti piksel dengan median dari neighborhood
- Sangat efektif untuk salt-and-pepper noise

**Bilateral Filter:**
- Edge-preserving smoothing
- Mempertimbangkan spatial distance DAN intensity difference
- Digunakan untuk: skin smoothing, denoising

#### C. Sharpening Filters

**Laplacian:**
```
┌────┬────┬────┐
│  0 │ -1 │  0 │
├────┼────┼────┤
│ -1 │  4 │ -1 │    Mendeteksi perubahan cepat (edges)
├────┼────┼────┤
│  0 │ -1 │  0 │
└────┴────┴────┘
```

**Unsharp Masking:**
```
sharpened = original + α × (original - blurred)

Di mana:
- blurred = Gaussian blur dari original
- α = strength (biasanya 0.5 - 2.0)
```

### 4. Edge Detection

#### A. Gradient-based Methods

**Sobel Operator:**
```
Gx (Horizontal):       Gy (Vertical):
┌────┬────┬────┐       ┌────┬────┬────┐
│ -1 │  0 │ +1 │       │ -1 │ -2 │ -1 │
├────┼────┼────┤       ├────┼────┼────┤
│ -2 │  0 │ +2 │       │  0 │  0 │  0 │
├────┼────┼────┤       ├────┼────┼────┤
│ -1 │  0 │ +1 │       │ +1 │ +2 │ +1 │
└────┴────┴────┘       └────┴────┴────┘

Magnitude: G = √(Gx² + Gy²)
Direction: θ = arctan(Gy/Gx)
```

#### B. Canny Edge Detection

Algoritma edge detection paling populer dengan langkah:
1. **Gaussian smoothing** - Mengurangi noise
2. **Gradient calculation** - Sobel untuk Gx, Gy
3. **Non-maximum suppression** - Menipiskan edge
4. **Double thresholding** - High dan low threshold
5. **Edge tracking by hysteresis** - Connect weak edges to strong edges

### 5. Morphological Operations

Operasi berbasis bentuk untuk binary/grayscale images.

#### A. Structuring Element
```
Rectangle:    Cross:        Ellipse:
┌───┬───┬───┐ ┌───┬───┬───┐ ┌───┬───┬───┐
│ 1 │ 1 │ 1 │ │ 0 │ 1 │ 0 │ │ 0 │ 1 │ 0 │
├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
│ 1 │ 1 │ 1 │ │ 1 │ 1 │ 1 │ │ 1 │ 1 │ 1 │
├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
│ 1 │ 1 │ 1 │ │ 0 │ 1 │ 0 │ │ 0 │ 1 │ 0 │
└───┴───┴───┘ └───┴───┴───┘ └───┴───┴───┘
```

#### B. Basic Operations

| Operasi | Efek | Rumus |
|---------|------|-------|
| **Erosion** | Mengecilkan objek, hapus noise kecil | A ⊖ B |
| **Dilation** | Memperbesar objek, fill holes kecil | A ⊕ B |
| **Opening** | Erosion → Dilation, hapus noise | (A ⊖ B) ⊕ B |
| **Closing** | Dilation → Erosion, fill holes | (A ⊕ B) ⊖ B |
| **Gradient** | Outline/edge objek | (A ⊕ B) - (A ⊖ B) |

---

## 🏢 Contoh Aplikasi di Industri

### 1. Instagram Filters (Social Media)
**Perusahaan**: Meta (Instagram), Snapchat, TikTok

**Penggunaan:**
- Point operations untuk brightness/contrast adjustment
- Color manipulation untuk mood/tone
- Gaussian blur untuk portrait mode
- Sharpening untuk detail enhancement

**Teknologi:**
- Real-time processing pada mobile GPU
- Preset LUT (Look-Up Table) untuk filter cepat

### 2. Medical Imaging Enhancement
**Institusi**: Hospital radiology departments, Siemens Healthineers, GE Healthcare

**Penggunaan:**
- CLAHE untuk CT/MRI scan enhancement
- Edge detection untuk tumor boundary detection
- Morphological operations untuk segmentation
- Noise reduction untuk low-dose imaging

**Contoh:**
```
X-Ray Original → Histogram Equalization → Edge Enhancement → Diagnosis
```

### 3. Automated Optical Inspection (AOI)
**Perusahaan**: Keyence, Cognex, Omron

**Penggunaan:**
- Thresholding untuk defect detection
- Morphological operations untuk cleaning masks
- Edge detection untuk dimension measurement
- Filtering untuk noise removal

**Aplikasi:**
- PCB inspection
- Semiconductor wafer inspection
- Packaging quality control

### 4. Satellite Image Processing
**Organisasi**: NASA, ESA, Planet Labs, Maxar

**Penggunaan:**
- Histogram matching untuk mosaic stitching
- Atmospheric correction (point operations)
- Edge detection untuk feature extraction
- Morphological operations untuk land classification

### 5. Adobe Photoshop / Lightroom
**Perusahaan**: Adobe

**Tools yang Menggunakan Konsep Ini:**
- Levels & Curves → Histogram operations
- Sharpen/Blur → Spatial filtering
- Shadow/Highlight → Adaptive processing
- Noise Reduction → Bilateral/Non-local means filter

---

## 📐 Diagram dan Ilustrasi

### Convolution Process
```
Input Image          Kernel (3×3)         Output
┌───┬───┬───┬───┐    ┌───┬───┬───┐
│10 │20 │30 │40 │    │ 0 │-1 │ 0 │
├───┼───┼───┼───┤    ├───┼───┼───┤
│50 │60 │70 │80 │ ⊗  │-1 │ 4 │-1 │  =   Result[1,1] = ?
├───┼───┼───┼───┤    ├───┼───┼───┤
│90 │100│110│120│    │ 0 │-1 │ 0 │
├───┼───┼───┼───┤    └───┴───┴───┘
│130│140│150│160│

Calculation for position (1,1):
= 10×0 + 20×(-1) + 30×0 +
  50×(-1) + 60×4 + 70×(-1) +
  90×0 + 100×(-1) + 110×0
= 0 - 20 + 0 - 50 + 240 - 70 + 0 - 100 + 0
= 0
```

### Morphological Operations Visualization
```
Original Binary:    After Erosion:      After Dilation:
  ████████            ██████              ██████████
  ████████            ██████              ██████████
  ████████     →      ██████      →       ██████████
  ████████            ██████              ██████████
  ████████            ██████              ██████████

Opening (remove small objects):    Closing (fill small holes):
  ████  ██                           ████████
  ████     →   ████                  ████████   →   ████████
  ████  ██     ████                  ██  ████       ████████
```

### Edge Detection Pipeline
```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Original │ →   │ Gaussian │ →   │  Sobel   │ →   │   NMS    │
│  Image   │     │   Blur   │     │ Gradient │     │(thinning)│
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                        │
                                                        ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Final   │ ←   │Hysteresis│ ←   │ Double   │ ←   │  Thin    │
│  Edges   │     │ Tracking │     │Threshold │     │  Edges   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

---

## 📝 Ringkasan

| Kategori | Operasi | OpenCV Function | Use Case |
|----------|---------|-----------------|----------|
| Point | Brightness/Contrast | cv2.convertScaleAbs() | Image enhancement |
| Point | Gamma | Manual: img**(1/gamma) | Display correction |
| Point | Threshold | cv2.threshold() | Segmentation |
| Histogram | Equalization | cv2.equalizeHist() | Contrast enhancement |
| Histogram | CLAHE | cv2.createCLAHE() | Local enhancement |
| Filter | Blur | cv2.GaussianBlur() | Noise reduction |
| Filter | Median | cv2.medianBlur() | Salt-pepper noise |
| Filter | Bilateral | cv2.bilateralFilter() | Edge-preserving smooth |
| Filter | Sharpen | cv2.filter2D() | Detail enhancement |
| Edge | Sobel | cv2.Sobel() | Gradient detection |
| Edge | Canny | cv2.Canny() | Edge detection |
| Morph | Erosion | cv2.erode() | Shrink objects |
| Morph | Dilation | cv2.dilate() | Expand objects |
| Morph | Opening | cv2.morphologyEx() | Remove noise |
| Morph | Closing | cv2.morphologyEx() | Fill holes |

---

## 🎬 Tugas Video

### Deskripsi Tugas
Buat video tutorial dengan durasi **10-15 menit** yang mendemonstrasikan teknik-teknik pemrosesan citra.

### Konten yang Harus Ada
1. **Pembukaan** (1-2 menit)
   - Perkenalan topik Image Processing
   - Preview hasil yang akan dicapai

2. **Point Operations Demo** (3-4 menit)
   - Demo brightness dan contrast adjustment
   - Demo gamma correction dengan berbagai nilai
   - Demo thresholding (binary, adaptive)

3. **Filtering Demo** (3-4 menit)
   - Perbandingan berbagai smoothing filters
   - Demo pada gambar dengan noise
   - Demo sharpening

4. **Edge Detection & Morphology** (3-4 menit)
   - Demo Canny edge detection dengan parameter tuning
   - Demo morphological operations
   - Aplikasi: pembersihan hasil segmentasi

5. **Penutup** (1-2 menit)
   - Mini project: kombinasikan teknik-teknik tersebut
   - Tips praktis dan best practices

### Checklist Penilaian
- [ ] Penjelasan konsep dengan visualisasi
- [ ] Demonstrasi kode yang berfungsi
- [ ] Perbandingan efek berbagai parameter
- [ ] Kualitas audio dan video baik
- [ ] Durasi sesuai (10-15 menit)

---

## 📚 Referensi

1. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications, 2nd Edition*. Chapter 3: Image Processing.
2. Gonzalez, R.C. & Woods, R.E. (2018). *Digital Image Processing, 4th Edition*.
3. OpenCV Documentation: [Image Processing](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html)
4. [Image Filtering - First Principles of Computer Vision (YouTube)](https://www.youtube.com/watch?v=example)

---

*Materi ini adalah bagian dari Praktikum Computer Vision*
