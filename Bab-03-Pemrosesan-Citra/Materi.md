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
├── Global Operations
│   ├── Histogram equalization
│   ├── Fourier transform
│   └── Image pyramids
│
├── Compositing & Matting
│   ├── Alpha compositing
│   ├── Green screen matting
│   └── Image blending
│
└── Geometric Transformations
    ├── Affine transforms
    ├── Perspective transforms
    └── Image warping
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

### 6. Compositing & Matting

#### A. Alpha Compositing

Alpha compositing menggabungkan dua gambar menggunakan alpha channel (transparansi).

**Formula Over Operator:**
```
C = (1 - α)B + αF

Di mana:
- F = Foreground image
- B = Background image
- α = Alpha matte (0 = transparan, 1 = opak)
- C = Composited result
```

**Pre-multiplied Alpha:**
```
F' = αF (pre-multiply foreground)
C = B + F' - αB
C = B(1 - α) + F'

Keuntungan:
- Lebih efisien untuk multiple compositing
- Mencegah fringe artifacts
```

#### B. Matting Techniques

**Green Screen Matting:**
1. Isolasi warna hijau menggunakan HSV color space
2. Create alpha matte dari color distance
3. Refine matte edges dengan morphology
4. Composite foreground dengan background baru

**Applications:**
- Film VFX (Marvel, Star Wars)
- Virtual backgrounds (Zoom, Teams)
- Portrait mode (smartphone cameras)

#### C. Image Blending

**Linear Blending:**
```
Result = α × Image1 + (1-α) × Image2
```

**Multi-band Blending:**
- Menggunakan pyramid untuk seamless transitions
- Blend different frequencies di different scales

---

### 7. Fourier Transform

#### A. Discrete Fourier Transform (DFT)

Mengubah image dari spatial domain ke frequency domain.

**Formula 2D DFT:**
```
F(u,v) = ∑∑ f(x,y) e^(-2πi(ux/M + vy/N))
        x y

Di mana:
- f(x,y) = spatial domain image
- F(u,v) = frequency domain representation
- u,v = frequency coordinates
```

**Magnitude & Phase:**
```
Magnitude: |F(u,v)| = √(Re² + Im²)
Phase:     φ(u,v) = arctan(Im/Re)
```

#### B. Filtering di Frequency Domain

**Low-pass Filter:**
- Hapus high frequencies
- Hasil: smoothing/blurring
- Ideal: rectangle cutoff
- Gaussian: smooth cutoff

**High-pass Filter:**
- Hapus low frequencies
- Hasil: edge enhancement
- H_high(u,v) = 1 - H_low(u,v)

**Band-pass Filter:**
- Keep specific frequency range
- Hapus very low dan very high frequencies

**Konvolusi Theorem:**
```
f ⊗ g ↔ F · G

Spatial convolution = Frequency multiplication
```

#### C. Applications

- **Image compression** (JPEG = DCT, wavelet compression)
- **Periodic noise removal** (notch filtering)
- **Image analysis** (texture, patterns)

---

### 8. Image Pyramids & Multi-Resolution

#### A. Gaussian Pyramid

Hierarchical representation dengan progressive blur + downsampling.

**Construction:**
```
G₀ = Original image
G₁ = Downsample(GaussianBlur(G₀))
G₂ = Downsample(GaussianBlur(G₁))
...

Each level: ½ width, ½ height
Total size: ~1.33× original (overhead ~33%)
```

**Applications:**
- Fast template matching (coarse-to-fine)
- Multi-scale feature detection
- Image blending

#### B. Laplacian Pyramid

Band-pass representation dengan perfect reconstruction.

**Construction:**
```
L_i = G_i - Upsample(G_{i+1})

Di mana:
- G_i = Gaussian pyramid level i
- L_i = Laplacian (band-pass) level i
```

**Reconstruction:**
```
G_i = L_i + Upsample(G_{i+1})

Perfect reconstruction (no information loss)
```

**Applications:**
- Seamless image blending (Burt & Adelson, 1983)
- Image compression
- Detail enhancement

#### C. Wavelets

Oriented multi-scale decomposition.

**2D Wavelet Decomposition:**
```
[cA | cH]
[cV | cD]

Di mana:
- cA = Approximation (low-pass)
- cH = Horizontal details (vertical edges)
- cV = Vertical details (horizontal edges)  
- cD = Diagonal details (corners)
```

**Wavelet Types:**
- **Haar**: simplest, blocky
- **Daubechies (db4)**: smooth, good for compression
- **Symlets**: symmetrical, image processing
- **Coiflets**: better reconstruction

**Applications:**
- JPEG 2000 compression
- Image denoising (threshold small coefficients)
- Texture analysis

---

### 9. Geometric Transformations

#### A. Transformation Hierarchy

```
Translation (2 DoF)
  ↓ add rotation
Euclidean/Rigid (3 DoF)
  ↓ add scale
Similarity (4 DoF)
  ↓ add shear
Affine (6 DoF)
  ↓ add perspective
Projective/Homography (8 DoF)
```

#### B. Parametric Transforms

**Translation:**
```
x' = x + t_x
y' = y + t_y
```

**Rotation:**
```
[x']   [cos(θ)  -sin(θ)] [x]
[y'] = [sin(θ)   cos(θ)] [y]
```

**Affine (matrix form):**
```
[x']   [a11  a12  t_x] [x]
[y'] = [a21  a22  t_y] [y]
[1 ]   [0    0    1  ] [1]

Properties:
- Preserves parallel lines
- Preserves ratios on lines
- Needs 3 point correspondences
```

**Perspective (Homography):**
```
    [h11  h12  h13] [x]
w · [y'] = [h21  h22  h23] [y]
    [1 ]   [h31  h32  h33] [1]

Then: x' = x'/w, y' = y'/w

Properties:
- Preserves straight lines
- Does NOT preserve parallel lines
- Needs 4 point correspondences
- 8 DoF (h33 = 1 by convention)
```

#### C. Interpolation Methods

**Inverse Warping:**
```
For each pixel (x', y') in output:
  1. Compute source location (x, y) using inverse transform
  2. Interpolate value at non-integer (x, y)
```

**Interpolation Types:**
- **Nearest neighbor**: Fast, blocky (INTER_NEAREST)
- **Bilinear**: Fast, smooth (INTER_LINEAR)
- **Bicubic**: Slower, smoother (INTER_CUBIC)
- **Lanczos**: Slowest, sharpest (INTER_LANCZOS4)

#### D. Mesh-Based Warping

Non-parametric warping menggunakan displacement field.

**Radial Distortion (lens correction):**
```
r' = r(1 + k₁r² + k₂r⁴ + k₃r⁶)

Di mana:
- r = radius dari center
- k₁, k₂, k₃ = distortion coefficients
- Barrel: k₁ > 0
- Pincushion: k₁ < 0
```

**Applications:**
- Document rectification (scanner apps)
- Lens distortion correction (camera calibration)
- Image morphing (visual effects)
- Augmented reality (planar tracking)

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

### 6. Film & VFX Industry
**Studios**: Industrial Light & Magic, Weta Digital, Framestore

**Penggunaan:**
- **Green screen compositing** → Alpha matting
- **Background replacement** → Over operator
- **Seamless blending** → Pyramid blending
- **Lens distortion correction** → Geometric warping

**Contoh Film:**
- Marvel movies (green screen VFX)
- Avatar (performance capture + compositing)

### 7. Document Scanner Apps
**Apps**: CamScanner, Adobe Scan, Microsoft Lens

**Pipeline:**
1. **Corner detection** → Edge detection
2. **Perspective correction** → Homography transform
3. **Enhancement** → Adaptive thresholding, sharpening
4. **OCR preparation** → Binarization

**Teknologi:**
```
Tilted photo → Detect corners → Perspective warp → Enhancement → OCR-ready
```

### 8. Smartphone Computational Photography
**Perusahaan**: Apple, Google (Pixel), Samsung

**Features:**
- **Portrait mode** → Depth estimation + bilateral filter
- **Night mode** → Multi-frame alignment + pyramid blending
- **HDR+** → Exposure fusion dengan Laplacian pyramid
- **Panorama** → Perspective warping + multi-band blending

### 9. Compression Standards
**Standards**: JPEG, JPEG 2000, WebP

**Teknologi:**
- **JPEG** → DCT (Discrete Cosine Transform)
- **JPEG 2000** → Wavelet compression (better quality)
- **Thumbnail generation** → Gaussian pyramid

### 10. Augmented Reality (AR)
**Apps**: Snapchat, Instagram AR, Pokémon GO

**Penggunaan:**
- **Planar tracking** → Homography estimation
- **Real-time warping** → Affine/perspective transforms
- **Face filters** → Mesh-based warping
- **Background blur** → Matting + bilateral filter

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
| Compositing | Alpha blend | cv2.addWeighted() | Image compositing |
| Compositing | Green screen | HSV masking | Chroma keying |
| Frequency | FFT | cv2.dft() | Frequency analysis |
| Frequency | DCT | cv2.dct() | JPEG compression |
| Frequency | Filtering | Frequency masks | Noise removal |
| Pyramid | Gaussian | cv2.pyrDown() | Multi-scale |
| Pyramid | Laplacian | Manual construction | Blending |
| Wavelet | Decomposition | pywt.wavedec2() | Compression, denoising |
| Transform | Rotation | cv2.getRotationMatrix2D() | Image rotation |
| Transform | Affine | cv2.getAffineTransform() | 6-DoF warp |
| Transform | Perspective | cv2.getPerspectiveTransform() | 8-DoF warp |
| Transform | Remap | cv2.remap() | Custom warping |

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

### 10. Steerable Filters dan Band-Pass Filtering

#### A. Konsep Steerable Filters

Steerable filters adalah keluarga filter yang dapat dirotasi ke orientasi apapun melalui kombinasi linear dari basis filters.

**Freeman & Adelson Steerable Filters:**
```
G(θ) = cos(θ)·G₀(x,y) + sin(θ)·G₉₀(x,y)

Di mana:
- G₀ = first-order directional derivative pada 0°
- G₉₀ = first-order directional derivative pada 90°
- θ = desired orientation

Keuntungan:
- Efficient: compute 2 basis filters, interpolate untuk any angle
- Smooth orientation detection
- Edge detection di arbitrary directions
```

**Second-Order Steerable Filters:**
```
G(θ) = cos²(θ)·G₀ + 2cos(θ)sin(θ)·G₄₅ + sin²(θ)·G₉₀

Untuk corner/junction detection dengan oriented response.
```

#### B. Laplacian of Gaussian (LoG)

Scale-space blob detector yang mendeteksi circular features di berbagai skala.

**Formula:**
```
LoG(x,y,σ) = ∇²(G(x,y,σ))
            = σ²·(∂²G/∂x² + ∂²G/∂y²)

Respons maksimal pada σ ≈ r/√2 (blob radius r)
```

**Aplikasi:**
- SIFT scale-space detection
- Blob detection untuk feature points
- Multi-scale edge detection

#### C. Band-Pass Filtering

Filtering yang keep specific frequency range, hapus very low dan very high.

**Band-Pass Filter Design:**
```
H(u,v) = H_high(u,v) × H_low(u,v)

Di mana:
- H_high = 1 - Low-pass (removes DC)
- H_low = Low-pass (removes high frequencies)

Result: Only middle frequencies pass
```

**Steerable Band-Pass:**
- Combine orientation selectivity dengan frequency selectivity
- Detect textures dengan specific orientation AND frequency

**Aplikasi:**
- Texture analysis
- Oriented edge detection
- Medical imaging enhancement

---

### 11. Advanced Interpolation, Decimation, dan Multi-Resolution Pyramids

#### A. Interpolation Methods (Review & Advanced)

**Bilinear Interpolation:**
```
f(x,y) = f(0,0)(1-u)(1-v) + f(1,0)u(1-v) +
         f(0,1)(1-u)v + f(1,1)uv

Di mana: u = frac(x), v = frac(y)
Smoothness: C⁰ (continuous but not smooth at integer points)
```

**Bicubic Interpolation:**
```
f(x,y) = ∑∑ a[i][j]·x^i·y^j   (i,j = 0 to 3)

Cubic kernel: k(t) = {
  1 - 2|t|² + |t|³     jika |t| < 1
  4 - 8|t| + 5|t|² - |t|³  jika 1 ≤ |t| < 2
  0                    otherwise
}

Smoothness: C¹ (smooth transitions)
Parameter a mengontrol sharpness:
- a = -1: sharp (Catmull-Rom)
- a = -0.5: balanced
- a = -0.75: intermediate
```

**Windowed Sinc Interpolation:**
```
f(x) = ∑ f[n]·sinc(x-n)·w(x-n)

Di mana:
- sinc(x) = sin(πx)/(πx)
- w(x) = window function (Hann, Lanczos)

Kualitas: Tertinggi, untuk professional applications
```

**Lanczos Interpolation:**
```
Lanczos kernel: L(t) = {
  sinc(t)·sinc(t/a)     jika |t| < a
  0                     otherwise
}

Parameter a = 3 biasanya (balance quality vs speed)
Used by: ImageMagick, GIMP, FFmpeg
```

#### B. Anti-Aliasing Prefiltering

Sebelum downsampling, apply low-pass filter untuk avoid aliasing.

**Binomial Filter (Burt & Adelson):**
```
[1 4 6 4 1]/16 kernel  (1D)
atau 2D: outer product

Properties:
- Smooth, natural-looking
- Commonly used dalam pyramid construction
```

**Gaussian Prefilter:**
```
σ = 1/(2π·f_c)  untuk cutoff frequency f_c
```

#### C. MIP-Mapping (Multum In Parvo)

Multi-level Pyramid Image untuk efficient texture mapping.

**Construction:**
```
Level 0: Original resolution (w × h)
Level 1: Downsample (w/2 × h/2)
Level 2: Downsample (w/4 × h/4)
...
Level k: (w/2^k × h/2^k)

Total storage: ~1.33× original
```

**Trilinear Mipmap Sampling:**
```
For texture coordinate (x, y, lod):
1. Find 2 closest MIP levels: L_lo, L_hi
2. Bilinear interpolation pada both levels
3. Linear interpolation antara levels

Result: Smooth transitions across detail levels
```

**Aplikasi:**
- Real-time 3D graphics (GPU texture mapping)
- Image zooming dengan lossless quality
- Memory cache efficiency

---

### 12. Advanced Image Blending dan Feature-Based Morphing

#### A. Poisson Image Editing

Gradient-domain compositing untuk seamless blending.

**Konsep:**
```
Minimize: ∫∫ |∇I|² subject to: I|boundary = boundary_condition

Ini menyelesaikan Laplace equation:
∇²I = 0

Seamless karena gradient transitions smooth.
```

**Applications:**
- Seamless cloning (copy-paste)
- Object removal (inpainting)
- Exposure blending

#### B. Multi-Band Blending (Burt & Adelson)

Blend different frequency bands independently, then reconstruct.

**Algorithm:**
```
1. Decompose: img1 & img2 ke Laplacian pyramid
2. Blend each band dengan mask
3. Reconstruct: sum blended bands

L_blended[level] = (1-α)·L1[level] + α·L2[level]
Result = sum(L_blended[level] + G[last_level])
```

**Keuntungan:**
- Seamless transitions di multiple scales
- Detail preservation
- Better untuk complex boundaries

#### C. Thin-Plate Spline (TPS) Warping

Non-parametric smooth interpolator untuk image warping.

**Properties:**
```
- Passes through control points exactly
- Minimizes bending energy (∫∫ (∂²z/∂x² + ∂²z/∂y²)² dxdy)
- Smooth everywhere, especially far dari points

RBF Kernel: φ(r) = r² log(r)
```

**Interpolation:**
```
z(x,y) = a₀ + a₁x + a₂y + ∑ wᵢ·φ(||p - pᵢ||)

Solve linear system untuk weights wᵢ dan coefficients aⱼ
```

**Aplikasi:**
- Face morphing (smooth facial transitions)
- Shape transformation
- Free-form image deformation

#### D. Line-Based Warping (Beier-Neely Algorithm)

Warp image by specifying corresponding line segments.

**Displacement dari line j pada titik p:**
```
d_j(p) = (displacements dari line correspondences)

Distance weighting:
w_j = (||line_j|| / (a + distance(p, line_j)))^b

Final displacement: d(p) = ∑(w_j · d_j(p)) / ∑w_j
```

**Keuntungan:**
- More intuitive: user specify lines not points
- Preserve line structures
- Better untuk structural warping

#### E. Feature-Based Morphing

Combine warping + blending untuk smooth transition antara images.

**Morphing Pipeline:**
```
Image 1 ──Warp→ Intermediate──Warp← Image 2
    ∧                ∨               ∧
    |─────────Blend────────────────|

Frame t:
1. Interpolate control points: P(t) = (1-t)·P₁ + t·P₂
2. Warp img1 → intermediate: W₁
3. Warp img2 → intermediate: W₂
4. Cross-dissolve: Result = (1-t)·W₁ + t·W₂
```

**Quality Parameters:**
```
- Control point density: lebih dense = lebih detail tapi lebih slow
- Interpolation method: TPS (smooth) vs linear (fast)
- Blend frames: lebih banyak = smoother animation
- Morphing curves: linear vs easing functions
```

**Aplikasi:**
- Movie title sequences
- Face morphing videos
- Shape transformation animations
- Character blending dalam visual effects

#### F. Mesh-Based Deformation

Deform image menggunakan control mesh untuk local shape control.

**Methods:**
- **Affine-per-triangle**: Compute affine untuk each triangle
- **Barycentric interpolation**: Smooth deformation across triangles
- **RBF-based**: Global smooth deformation field

**Deformation Effects:**
```
Bulge:  Push points away dari center
Pinch:  Pull points toward center
Twist:  Rotate points around center
Bend:   Arc deformation
```

---

## 📚 Referensi

1. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications, 2nd Edition*. Chapter 3: Image Processing.
2. Gonzalez, R.C. & Woods, R.E. (2018). *Digital Image Processing, 4th Edition*.
3. Freeman, W.T. & Adelson, E.H. (1991). "The design and use of steerable filters". IEEE Transactions on Pattern Analysis and Machine Intelligence.
4. Beier, T. & Neely, S. (1992). "Feature-Based Image Metamorphosis". SIGGRAPH Proceedings.
5. Burt, P.J. & Adelson, E.H. (1983). "A multiresolution spline with application to image mosaics". ACM Transactions on Graphics.
6. Bookstein, F.L. (1989). "Principal Warps: Thin-Plate Splines and the Decomposition of Deformations". IEEE TPAMI.
7. Pérez, P., Gangnet, M. & Blake, A. (2003). "Poisson image editing". ACM SIGGRAPH.
8. OpenCV Documentation: [Image Processing](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html)
9. SciPy Documentation: [Interpolation](https://docs.scipy.org/doc/scipy/reference/interpolate.html)
10. [Digital Image Warping - George Wolberg](https://www.routledge.com/Digital-Image-Warping/Wolberg/p/book/9780849371639)

---

*Materi ini adalah bagian dari Praktikum Computer Vision*
