# Bab 7: Feature Detection dan Matching

## Daftar Isi
1. [Pendahuluan](#1-pendahuluan)
2. [Point Feature Detection](#2-point-feature-detection)
3. [Feature Descriptors](#3-feature-descriptors)
4. [Feature Matching](#4-feature-matching)
5. [Line dan Edge Detection](#5-line-dan-edge-detection)
6. [Deep Learning Features](#6-deep-learning-features)

---

## 1. Pendahuluan

### 1.1 Apa itu Feature?

**Feature** adalah pola atau struktur yang menonjol dalam gambar yang dapat digunakan untuk:
- Mencocokkan bagian gambar yang sama dari viewpoint berbeda
- Mengenali objek
- Merekonstruksi scene 3D
- Tracking objek dalam video

### 1.2 Karakteristik Feature yang Baik

```
┌─────────────────────────────────────────────────────────────────┐
│              KRITERIA FEATURE YANG BAIK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. REPEATABILITY                                               │
│     Dapat dideteksi kembali pada gambar berbeda                 │
│     dari scene yang sama                                        │
│                                                                  │
│  2. DISTINCTIVENESS                                             │
│     Unik dan dapat dibedakan dari feature lain                  │
│                                                                  │
│  3. LOCALITY                                                    │
│     Dipengaruhi area kecil (robust terhadap occlusion)          │
│                                                                  │
│  4. QUANTITY                                                    │
│     Cukup banyak untuk coverage yang baik                       │
│                                                                  │
│  5. ACCURACY                                                    │
│     Lokasi yang presisi                                         │
│                                                                  │
│  6. EFFICIENCY                                                  │
│     Dapat dihitung dengan cepat                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Pipeline Feature Matching

```
Image 1          Image 2
   │                │
   ▼                ▼
┌──────────┐   ┌──────────┐
│ Detection│   │ Detection│
└────┬─────┘   └────┬─────┘
     │              │
     ▼              ▼
┌──────────┐   ┌──────────┐
│Descriptor│   │Descriptor│
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │   Matching   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Verification │
     │   (RANSAC)   │
     └──────────────┘
```

---

## 2. Point Feature Detection

### 2.1 Harris Corner Detector

**Harris Corner** adalah detektor sudut yang paling fundamental.

**Prinsip**: Sudut adalah titik di mana perubahan intensitas signifikan di semua arah.

#### Auto-correlation Matrix

Untuk setiap pixel, hitung matriks struktur:

$$M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$$

Di mana:
- $I_x, I_y$: Gradient pada arah x dan y
- $w(x,y)$: Window function (Gaussian)

#### Eigenvalue Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│              INTERPRETASI EIGENVALUES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  λ₁ ≈ λ₂ ≈ 0:  Flat region (tidak ada fitur)                   │
│                                                                  │
│  λ₁ >> λ₂ ≈ 0: Edge (perubahan satu arah)                      │
│                                                                  │
│  λ₁ ≈ λ₂ >> 0: Corner (perubahan semua arah) ✓                 │
│                                                                  │
│                    λ₂                                            │
│                    ▲                                             │
│         Edge       │        Corner                               │
│    ┌───────────────┼───────────────┐                            │
│    │               │               │                             │
│    │               │               │                             │
│    ├───────────────┼───────────────┤──▶ λ₁                     │
│    │    Flat       │     Edge      │                             │
│    │               │               │                             │
│    └───────────────┴───────────────┘                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Harris Response Function

Menghitung eigenvalues mahal, jadi gunakan:

$$R = \det(M) - k \cdot \text{trace}(M)^2 = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2$$

Di mana $k$ biasanya 0.04-0.06.

**Corner jika** $R > threshold$

### 2.2 Shi-Tomasi (Good Features to Track)

Modifikasi Harris dengan response:

$$R = \min(\lambda_1, \lambda_2)$$

**Keuntungan**: Threshold lebih intuitif dan stabil.

### 2.3 FAST (Features from Accelerated Segment Test)

FAST sangat cepat untuk deteksi corner.

**Algoritma**:
1. Pilih pixel $p$ dengan intensitas $I_p$
2. Pilih threshold $t$
3. Periksa 16 pixel pada lingkaran radius 3
4. $p$ adalah corner jika ada $n$ pixels berturut-turut yang semuanya:
   - Lebih terang dari $I_p + t$, ATAU
   - Lebih gelap dari $I_p - t$

```
        16  1  2
      15        3
    14            4
    13      p     5
    12            6
      11        7
        10  9  8
```

**Biasanya $n = 12$** (FAST-12)

### 2.4 Scale-Invariant Detection

#### Scale Space

Untuk mendeteksi fitur pada berbagai scale, gunakan **Gaussian scale space**:

$$L(x, y, \sigma) = G(x, y, \sigma) * I(x, y)$$

#### Laplacian of Gaussian (LoG)

Mencari blob (titik yang menonjol) menggunakan:

$$\nabla^2 L = L_{xx} + L_{yy}$$

**Scale-normalized LoG:**

$$\nabla^2_{norm} L = \sigma^2 (L_{xx} + L_{yy})$$

#### Difference of Gaussian (DoG) - SIFT

Aproksimasi efisien dari LoG:

$$DoG = L(x, y, k\sigma) - L(x, y, \sigma) \approx (k-1)\sigma^2 \nabla^2 L$$

```
┌─────────────────────────────────────────────────────────────────┐
│                   SIFT SCALE SPACE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Octave 0:                                                      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                           │
│  │σ₀  │ │kσ₀ │ │k²σ₀│ │k³σ₀│ │k⁴σ₀│  Gaussian images          │
│  └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘ └────┘                           │
│     │      │      │      │                                      │
│     └──┬───┘  └───┬──┘  └──┬─┘                                 │
│        ▼         ▼         ▼                                    │
│     ┌────┐   ┌────┐   ┌────┐                                   │
│     │DoG │   │DoG │   │DoG │  DoG images                       │
│     └────┘   └────┘   └────┘                                   │
│                                                                  │
│  Octave 1: (image downsampled 2x)                               │
│  ...                                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Keypoint Selection**:
- Extrema detection: Bandingkan pixel dengan 26 neighbors (8 + 9 + 9)
- Subpixel localization: Taylor expansion
- Eliminate low contrast points
- Eliminate edges (ratio of principal curvatures)

### 2.5 SURF (Speeded-Up Robust Features)

SURF adalah versi lebih cepat dari SIFT menggunakan:
- **Integral images** untuk komputasi cepat
- **Box filters** untuk aproksimasi DoG
- **Haar wavelets** untuk descriptor

---

## 3. Feature Descriptors

### 3.1 SIFT Descriptor

**SIFT Descriptor** adalah representasi local appearance yang robust.

#### Langkah-langkah:

1. **Assign Orientation**: Dominant gradient direction
2. **Rotate to Orientation**: Achieve rotation invariance
3. **Compute Descriptor**:
   - Ambil 16×16 window di sekitar keypoint
   - Bagi menjadi 4×4 cells
   - Di setiap cell, hitung 8-bin histogram of gradients
   - Total: 4×4×8 = **128 dimensions**

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIFT DESCRIPTOR                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  16×16 window                      4×4 cells                     │
│  ┌────┬────┬────┬────┐          ┌────────────────┐             │
│  │    │    │    │    │          │  ┌──┬──┬──┬──┐ │             │
│  ├────┼────┼────┼────┤          │  │  │  │  │  │ │             │
│  │    │    │    │    │    →     │  ├──┼──┼──┼──┤ │             │
│  ├────┼────┼────┼────┤          │  │  │  │  │  │ │             │
│  │    │    │    │    │          │  ├──┼──┼──┼──┤ │             │
│  ├────┼────┼────┼────┤          │  │  │  │  │  │ │             │
│  │    │    │    │    │          │  └──┴──┴──┴──┘ │             │
│  └────┴────┴────┴────┘          └────────────────┘             │
│                                                                  │
│  Each cell → 8-bin gradient histogram                           │
│  Total: 4×4×8 = 128 dimensions                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 SURF Descriptor

SURF menggunakan **Haar wavelet responses**:
- 4×4 subregions
- Setiap region: $\sum d_x, \sum d_y, \sum |d_x|, \sum |d_y|$
- Total: **64 dimensions**

### 3.3 ORB (Oriented FAST and Rotated BRIEF)

**ORB** adalah alternative gratis dan cepat untuk SIFT/SURF.

**Detection**: FAST + Harris corner measure
**Orientation**: Intensity centroid method
**Descriptor**: Rotated BRIEF (rBRIEF)

#### BRIEF Descriptor

BRIEF adalah binary descriptor:
- Pilih $n$ pairs of pixels dalam patch
- Untuk setiap pair $(p_i, q_i)$: bit = 1 jika $I(p_i) < I(q_i)$
- Total: n bits (biasanya 256)

**Keuntungan**:
- Sangat cepat (binary comparison)
- Compact (256 bits = 32 bytes)
- Matching dengan Hamming distance

### 3.4 Perbandingan Descriptors

| Descriptor | Dimensions | Type | Speed | Robustness |
|------------|------------|------|-------|------------|
| SIFT | 128 | Float | Slow | Very High |
| SURF | 64 | Float | Medium | High |
| ORB | 256 | Binary | Fast | Medium |
| BRIEF | 256 | Binary | Very Fast | Low |
| BRISK | 512 | Binary | Fast | Medium |

---

## 4. Feature Matching

### 4.1 Nearest Neighbor Matching

Untuk setiap descriptor di image 1, cari descriptor terdekat di image 2.

**Distance Metrics:**

**Euclidean Distance** (untuk float descriptors):
$$d = \sqrt{\sum_i (a_i - b_i)^2}$$

**Hamming Distance** (untuk binary descriptors):
$$d = \text{popcount}(a \oplus b)$$

### 4.2 Ratio Test (Lowe's)

Untuk meningkatkan kualitas matches:

1. Untuk setiap feature, cari 2 nearest neighbors
2. Accept match jika:

$$\frac{d_1}{d_2} < threshold$$

Di mana $d_1$ = jarak ke match terdekat, $d_2$ = jarak ke match kedua.

**Typical threshold**: 0.7-0.8

### 4.3 Cross-Check (Mutual Nearest Neighbor)

Match valid jika:
- $A$ adalah nearest neighbor dari $B$ di image 2
- $B$ adalah nearest neighbor dari $A$ di image 1

### 4.4 FLANN (Fast Library for Approximate Nearest Neighbors)

Untuk matching cepat pada dataset besar:
- **KD-Tree** untuk low-dimensional data
- **Hierarchical K-Means** untuk high-dimensional data

### 4.5 Geometric Verification dengan RANSAC

Setelah matching, verifikasi dengan model geometri:

```python
# RANSAC untuk homography
def ransac_homography(matches, src_pts, dst_pts, threshold=4.0, max_iters=1000):
    best_inliers = []
    best_H = None
    
    for _ in range(max_iters):
        # Random sample 4 matches
        sample = random.sample(range(len(matches)), 4)
        
        # Compute homography
        H = compute_homography(src_pts[sample], dst_pts[sample])
        
        # Count inliers
        projected = apply_homography(H, src_pts)
        distances = np.linalg.norm(projected - dst_pts, axis=1)
        inliers = np.where(distances < threshold)[0]
        
        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_H = H
    
    return best_H, best_inliers
```

---

## 5. Line dan Edge Detection

### 5.1 Hough Transform untuk Lines

Transformasi titik-titik edge ke parameter space:

**Polar form**: $\rho = x \cos\theta + y \sin\theta$

```
Image Space              Hough Space (ρ, θ)
    y                         ρ
    ▲                         ▲
    │  • • •                  │     *
    │    • •          →       │   *
    │      •                  │ *
    └──────▶ x                └──────▶ θ
    
Titik collinear → Curves yang berpotongan di satu titik
```

### 5.2 LSD (Line Segment Detector)

LSD adalah detektor line modern yang lebih robust:
1. Compute gradient image
2. Partition ke line-support regions
3. Validate dengan NFA (Number of False Alarms)

### 5.3 Canny Edge Detection Review

```
Image → Gaussian Smooth → Gradient (Sobel) → NMS → Hysteresis → Edges
```

---

## 6. Deep Learning Features

### 6.1 Learned Feature Detectors

**SuperPoint** (Magic Leap, 2018):
- Self-supervised training
- Joint detection + description
- Homographic adaptation untuk training

**Architecture**:
```
Image → Shared Encoder (VGG-style) → Detection Head → Keypoints
                                  ↘ Description Head → Descriptors
```

### 6.2 Learned Matchers

**SuperGlue** (Magic Leap, 2019):
- Graph Neural Network untuk matching
- Attention mechanism
- Learns context untuk better matching

**LightGlue** (2023):
- Efficient version of SuperGlue
- Adaptive computation

### 6.3 End-to-End Feature Matching

**LoFTR** (CVPR 2021):
- Transformer-based
- Detector-free matching
- Dense matches, kemudian coarse-to-fine

```
┌─────────────────────────────────────────────────────────────────┐
│                        LoFTR PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Image A          Image B                                        │
│     │                │                                           │
│     ▼                ▼                                           │
│  ┌─────────────────────────────┐                                │
│  │       CNN Backbone          │                                │
│  │    (ResNet + FPN)           │                                │
│  └─────────────┬───────────────┘                                │
│                │                                                 │
│     ┌──────────┴──────────┐                                     │
│     │                     │                                      │
│     ▼                     ▼                                      │
│  Coarse Features     Coarse Features                            │
│     │                     │                                      │
│     └──────────┬──────────┘                                     │
│                │                                                 │
│                ▼                                                 │
│  ┌─────────────────────────────┐                                │
│  │  Self + Cross Attention     │  (Transformer)                 │
│  │       (Linear)              │                                │
│  └─────────────┬───────────────┘                                │
│                │                                                 │
│                ▼                                                 │
│         Coarse Matches                                           │
│                │                                                 │
│                ▼                                                 │
│  ┌─────────────────────────────┐                                │
│  │    Fine-level Refinement    │                                │
│  └─────────────┬───────────────┘                                │
│                │                                                 │
│                ▼                                                 │
│          Fine Matches                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ringkasan

### Detector Comparison

| Detector | Invariance | Speed | Quality |
|----------|------------|-------|---------|
| Harris | Rotation | Fast | Good |
| FAST | None | Very Fast | Medium |
| SIFT | Scale + Rotation | Slow | Excellent |
| SURF | Scale + Rotation | Medium | Good |
| ORB | Rotation | Fast | Good |
| SuperPoint | Learned | Medium | Excellent |

### Descriptor Comparison

| Descriptor | Size | Type | Matching |
|------------|------|------|----------|
| SIFT | 128 | Float | L2 |
| SURF | 64 | Float | L2 |
| ORB | 256 bits | Binary | Hamming |
| SuperPoint | 256 | Float | L2 |

---

## Latihan Mandiri

1. Implementasi Harris corner detector dari scratch
2. Bandingkan performa SIFT vs ORB pada berbagai transformasi
3. Implementasi ratio test dan cross-check matching
4. Gunakan RANSAC untuk estimate homography dari matches
5. Eksperimen dengan SuperPoint + SuperGlue

---

*Referensi: Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Edition. Chapter 7.*
