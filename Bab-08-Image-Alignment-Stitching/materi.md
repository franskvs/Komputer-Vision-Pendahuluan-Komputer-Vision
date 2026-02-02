# Bab 8: Image Alignment dan Stitching

## 📋 Daftar Isi
1. [Pendahuluan](#1-pendahuluan)
2. [2D dan 3D Transformations](#2-2d-dan-3d-transformations)
3. [Direct Alignment Methods](#3-direct-alignment-methods)
4. [Feature-Based Alignment](#4-feature-based-alignment)
5. [Image Stitching Pipeline](#5-image-stitching-pipeline)
6. [Blending dan Seam Finding](#6-blending-dan-seam-finding)
7. [Panorama Creation](#7-panorama-creation)

---

## 1. Pendahuluan

### 1.1 Apa itu Image Alignment?

**Image Alignment** (registrasi citra) adalah proses menyelaraskan dua atau lebih gambar ke dalam sistem koordinat yang sama. Ini adalah langkah fundamental dalam banyak aplikasi computer vision.

### 1.2 Aplikasi

1. **Panorama Stitching**: Menggabungkan foto-foto menjadi panorama
2. **Video Stabilization**: Menghilangkan goyangan kamera
3. **Medical Imaging**: Registrasi CT/MRI scans
4. **Remote Sensing**: Alignment citra satelit
5. **Document Scanning**: Alignment halaman dokumen
6. **Face Morphing**: Menyelaraskan wajah untuk efek
7. **HDR Imaging**: Menggabungkan exposure berbeda
8. **Super Resolution**: Menggabungkan frame low-res

### 1.3 Jenis-jenis Alignment

| Jenis | Karakteristik | DOF |
|-------|--------------|-----|
| **Translation** | Geser saja | 2 |
| **Rigid (Euclidean)** | Translation + Rotation | 3 |
| **Similarity** | Rigid + Uniform Scale | 4 |
| **Affine** | Similarity + Shear | 6 |
| **Projective (Homography)** | Full perspective | 8 |

---

## 2. 2D dan 3D Transformations

### 2.1 Translation

Pergeseran sederhana dalam x dan y:

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

**Parameter**: $t_x, t_y$ (2 DOF)

**Invarian**:
- Jarak antar titik
- Sudut
- Garis lurus tetap lurus

### 2.2 Euclidean (Rigid) Transform

Translation + Rotation:

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta & t_x \\ \sin\theta & \cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

**Parameter**: $\theta, t_x, t_y$ (3 DOF)

**Invarian**:
- Jarak (isometric)
- Sudut
- Bentuk objek

### 2.3 Similarity Transform

Euclidean + Uniform Scaling:

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} s\cos\theta & -s\sin\theta & t_x \\ s\sin\theta & s\cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

**Parameter**: $s, \theta, t_x, t_y$ (4 DOF)

**Invarian**:
- Rasio jarak
- Sudut (conformal)
- Bentuk relatif

### 2.4 Affine Transform

Transformasi linear + translation:

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

**Parameter**: $a_{11}, a_{12}, a_{21}, a_{22}, t_x, t_y$ (6 DOF)

**Invarian**:
- Garis paralel tetap paralel
- Rasio pembagian garis
- Garis lurus tetap lurus

**Estimasi**:
- Membutuhkan minimal **3 titik korespondensi**

### 2.5 Projective Transform (Homography)

Transformasi perspektif penuh:

$$\begin{bmatrix} x' \\ y' \\ w' \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

Koordinat gambar: $(x'/w', y'/w')$

**Parameter**: 8 DOF (9 elemen - 1 untuk skala)

**Invarian**:
- Cross-ratio
- Garis lurus tetap lurus

**Kapan berlaku?**
- Kamera berputar di sekitar center of projection
- Scene planar (bidang datar)

**Estimasi**:
- Membutuhkan minimal **4 titik korespondensi**

### 2.6 Hirarki Transformasi

```
Projective (8 DOF)
    ↓ h31 = h32 = 0
Affine (6 DOF)
    ↓ constraints
Similarity (4 DOF)
    ↓ s = 1
Euclidean (3 DOF)
    ↓ θ = 0
Translation (2 DOF)
```

---

## 3. Direct Alignment Methods

### 3.1 Konsep Lucas-Kanade

Direct methods mengestimasi transformasi dengan **meminimalkan error intensitas** langsung antara gambar, tanpa explicit feature matching.

**Prinsip dasar**:
$$E(\mathbf{p}) = \sum_{\mathbf{x}} [I(\mathbf{W}(\mathbf{x}; \mathbf{p})) - T(\mathbf{x})]^2$$

Di mana:
- $I$: gambar target
- $T$: template/reference
- $\mathbf{W}$: warp function dengan parameter $\mathbf{p}$

### 3.2 Lucas-Kanade Algorithm

**Asumsi**: Small displacement (pergerakan kecil)

**Linearisasi** dengan Taylor expansion:

$$I(\mathbf{W}(\mathbf{x}; \mathbf{p} + \Delta\mathbf{p})) \approx I(\mathbf{W}(\mathbf{x}; \mathbf{p})) + \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \Delta\mathbf{p}$$

**Minimisasi**:

$$\sum_{\mathbf{x}} \left[ I(\mathbf{W}(\mathbf{x}; \mathbf{p})) + \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \Delta\mathbf{p} - T(\mathbf{x}) \right]^2$$

**Solusi (least squares)**:

$$\Delta\mathbf{p} = H^{-1} \sum_{\mathbf{x}} \left[ \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \right]^T [T(\mathbf{x}) - I(\mathbf{W}(\mathbf{x}; \mathbf{p}))]$$

Di mana Hessian:
$$H = \sum_{\mathbf{x}} \left[ \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \right]^T \left[ \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \right]$$

### 3.3 Jacobian untuk Berbagai Warp

**Translation**:
$$\frac{\partial \mathbf{W}}{\partial \mathbf{p}} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$

**Affine**:
$$\frac{\partial \mathbf{W}}{\partial \mathbf{p}} = \begin{bmatrix} x & y & 0 & 0 & 1 & 0 \\ 0 & 0 & x & y & 0 & 1 \end{bmatrix}$$

### 3.4 Coarse-to-Fine (Image Pyramid)

Untuk mengatasi masalah **small displacement assumption**:

```
1. Bangun image pyramid (Gaussian pyramid)
2. Mulai dari level paling kasar
3. Estimasi transformasi di level tersebut
4. Propagasi ke level lebih halus sebagai initial guess
5. Refine di level lebih halus
6. Ulangi sampai level paling detail
```

**Keuntungan**:
- Dapat menangani pergerakan besar
- Lebih robust terhadap noise
- Konvergensi lebih baik

### 3.5 Inverse Compositional Algorithm

**Masalah**: Lucas-Kanade standar perlu menghitung Jacobian setiap iterasi

**Solusi**: Baker-Matthews inverse compositional
- Hitung Jacobian sekali di awal (menggunakan template T)
- Update dengan komposisi inverse warp

$$\mathbf{W}(\mathbf{x}; \mathbf{p}) \leftarrow \mathbf{W}(\mathbf{x}; \mathbf{p}) \circ \mathbf{W}(\mathbf{x}; \Delta\mathbf{p})^{-1}$$

**Keuntungan**: Jauh lebih cepat

### 3.6 Enhanced Correlation Coefficient (ECC)

ECC lebih robust terhadap perubahan brightness:

$$\text{ECC}(\mathbf{p}) = \frac{\sum_{\mathbf{x}} \hat{I}(\mathbf{W}(\mathbf{x}; \mathbf{p})) \cdot \hat{T}(\mathbf{x})}{\|\hat{I}\| \|\hat{T}\|}$$

Di mana $\hat{I}, \hat{T}$ adalah versi normalized (zero-mean).

**OpenCV**: `cv2.findTransformECC()`

---

## 4. Feature-Based Alignment

### 4.1 Pipeline Umum

```
1. Detect features di kedua gambar
2. Compute descriptors
3. Match features
4. Estimate transformation dengan RANSAC
5. Refine transformation
```

### 4.2 Homography Estimation

**Direct Linear Transform (DLT)**

Untuk setiap korespondensi $(x_i, y_i) \leftrightarrow (x'_i, y'_i)$:

$$\begin{bmatrix} -x_i & -y_i & -1 & 0 & 0 & 0 & x'_i x_i & x'_i y_i & x'_i \\ 0 & 0 & 0 & -x_i & -y_i & -1 & y'_i x_i & y'_i y_i & y'_i \end{bmatrix} \mathbf{h} = \mathbf{0}$$

Di mana $\mathbf{h} = [h_{11}, h_{12}, ..., h_{33}]^T$

**Solusi**: SVD dari matrix koefisien, ambil singular vector terakhir

### 4.3 Normalized DLT

Untuk numerical stability yang lebih baik:

1. **Normalisasi titik sumber**:
   - Translate centroid ke origin
   - Scale agar RMS distance = $\sqrt{2}$

2. **Normalisasi titik target** dengan cara sama

3. **Hitung homography** dari titik ternormalisasi

4. **Denormalize**: $H = T'^{-1} \hat{H} T$

### 4.4 RANSAC untuk Homography

```python
def ransac_homography(matches, threshold, iterations):
    best_H = None
    best_inliers = 0
    
    for _ in range(iterations):
        # Sample 4 random matches
        sample = random_sample(matches, 4)
        
        # Compute homography from sample
        H = compute_homography(sample)
        
        # Count inliers
        inliers = count_inliers(H, matches, threshold)
        
        if inliers > best_inliers:
            best_inliers = inliers
            best_H = H
    
    # Refine dengan semua inliers
    inlier_matches = get_inliers(best_H, matches, threshold)
    best_H = compute_homography(inlier_matches)
    
    return best_H
```

### 4.5 Levenberg-Marquardt Refinement

Setelah RANSAC, refine homography dengan **non-linear least squares**:

$$\min_H \sum_i d(\mathbf{x}'_i, H\mathbf{x}_i)^2$$

Menggunakan Levenberg-Marquardt untuk optimisasi.

---

## 5. Image Stitching Pipeline

### 5.1 Overview

```
Input Images
     ↓
Feature Detection (SIFT/ORB)
     ↓
Feature Matching
     ↓
Pairwise Homography Estimation
     ↓
Bundle Adjustment
     ↓
Warp to Common Canvas
     ↓
Blending
     ↓
Output Panorama
```

### 5.2 Determining Image Connectivity

Untuk multiple images:

1. **Match semua pasangan** gambar
2. **Build connectivity graph**:
   - Node = gambar
   - Edge = pasangan dengan cukup matches
3. **Find connected components**
4. **Select reference image** (center image)

### 5.3 Global Registration / Bundle Adjustment

**Masalah**: Pairwise homography bisa akumulasi error

**Solusi**: Bundle Adjustment - optimisasi global simultan

$$\min_{\{H_i\}} \sum_{\text{pairs }(i,j)} \sum_{\text{matches }k} \|H_i \mathbf{x}_k^i - H_j \mathbf{x}_k^j\|^2$$

**Parameterisasi**:
- Focal length $f$
- Rotation $R$ (3 DOF)
- Radial distortion $k_1, k_2$

### 5.4 Recognizing Panoramas

**APAP (As-Projective-As-Possible)**:
- Tidak semua gambar selalu overlap
- Automatic panorama recognition
- Probabilistic model untuk verify matches

---

## 6. Blending dan Seam Finding

### 6.1 Masalah Blending

Ketika menggabungkan gambar, muncul artifacts:
- **Seam visibility**: Batas antar gambar terlihat
- **Ghosting**: Objek bergerak muncul double
- **Exposure differences**: Perbedaan brightness

### 6.2 Simple Blending Methods

**Feather Blending (Alpha Blending)**:

$$I_{out} = \alpha \cdot I_1 + (1-\alpha) \cdot I_2$$

Di mana $\alpha$ berubah gradual dari 0 ke 1 pada overlap region.

**Masalah**: Low-frequency artifacts masih terlihat

### 6.3 Multi-Band Blending

**Burt & Adelson (1983)** - Laplacian Pyramid Blending:

```
1. Bangun Laplacian pyramid untuk setiap gambar
2. Bangun Gaussian pyramid untuk mask
3. Blend setiap level pyramid secara independen:
   L_blend[i] = G_mask[i] * L1[i] + (1 - G_mask[i]) * L2[i]
4. Reconstruct dari blended pyramid
```

**Mengapa efektif?**
- High frequency: blend dengan seam tajam
- Low frequency: blend dengan transisi smooth

### 6.4 Optimal Seam Finding

**Tujuan**: Temukan seam yang meminimalkan artifacts

**Graph Cut**:
1. Model overlap sebagai graph
2. Node = pixel
3. Edge weight = dissimilarity measure
4. Min-cut = optimal seam

**Cost function**:
$$C(p) = |I_1(p) - I_2(p)| + |\nabla I_1(p) - \nabla I_2(p)|$$

### 6.5 Exposure Compensation

Untuk mengatasi perbedaan exposure:

1. **Gain compensation**: Estimate gain per image
   $$I'_n = g_n \cdot I_n$$

2. **Minimisasi**:
   $$\min_{\{g_n\}} \sum_{(i,j)} \sum_{\text{overlap}} (g_i I_i - g_j I_j)^2$$

---

## 7. Panorama Creation

### 7.1 Projection Surfaces

**Planar**:
- Cocok untuk narrow FOV
- Distorsi di edges untuk wide FOV

**Cylindrical**:
$$x_{cyl} = f \cdot \arctan(x/f)$$
$$y_{cyl} = f \cdot y / \sqrt{x^2 + f^2}$$

- Cocok untuk horizontal panorama
- 360° possible

**Spherical (Equirectangular)**:
$$\phi = \arctan(x/f)$$
$$\theta = \arctan(y / \sqrt{x^2 + f^2})$$

- Full spherical panorama
- 360° × 180°

### 7.2 Deghosting

Untuk menangani objek bergerak:

1. **Reference frame selection**
2. **Detect moving objects**
3. **Select best pixels** dari reference atau closest frame

### 7.3 360° Panorama

**Requirements**:
- Overlapping images covering full 360°
- Consistent exposure
- Kamera berputar di satu titik

**Process**:
1. Warp ke cylindrical/spherical
2. Estimate rotations
3. Bundle adjustment
4. Blend dengan wrapping

### 7.4 Video Stabilization

**Aplikasi** image alignment untuk video:

1. **Track features** antar frame
2. **Estimate motion** (translation/homography)
3. **Smooth motion path**
4. **Warp frames** ke smoothed trajectory

**Motion models**:
- 2D translation (simple)
- Affine
- Homography (full)

### 7.5 OpenCV Stitcher Class

```python
import cv2

# Load images
imgs = [cv2.imread(f'img{i}.jpg') for i in range(5)]

# Create stitcher
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)

# Stitch
status, panorama = stitcher.stitch(imgs)

if status == cv2.Stitcher_OK:
    cv2.imwrite('panorama.jpg', panorama)
```

**Modes**:
- `PANORAMA`: Untuk panorama, asumsi rotation only
- `SCANS`: Untuk document scans, arbitrary motion

---

## 📊 Ringkasan Transformasi

| Transform | DOF | Min Points | Invarian | Aplikasi |
|-----------|-----|------------|----------|----------|
| Translation | 2 | 1 | Jarak, sudut | Template tracking |
| Euclidean | 3 | 2 | Jarak, sudut | Rigid registration |
| Similarity | 4 | 2 | Rasio, sudut | Face alignment |
| Affine | 6 | 3 | Parallelism | Texture mapping |
| Homography | 8 | 4 | Cross-ratio | Panorama, AR |

---

## 🔧 Best Practices

### Untuk Direct Methods
1. Gunakan image pyramid untuk large motion
2. Robust loss function untuk outliers
3. ECC untuk photometric variations

### Untuk Feature-Based
1. RANSAC dengan threshold yang tepat
2. Normalized DLT untuk numerical stability
3. Bundle adjustment untuk multiple images

### Untuk Stitching
1. Multi-band blending untuk seamless results
2. Exposure compensation
3. Seam finding untuk optimal boundaries

---

## 📚 Referensi

1. Szeliski, R. - Computer Vision: Algorithms and Applications, Chapter 8
2. Brown, M. & Lowe, D. - "Automatic Panoramic Image Stitching" (2007)
3. Baker, S. & Matthews, I. - "Lucas-Kanade 20 Years On" (2004)
4. Burt, P. & Adelson, E. - "A Multiresolution Spline" (1983)

---

*Materi ini adalah bagian dari Praktikum Computer Vision*
