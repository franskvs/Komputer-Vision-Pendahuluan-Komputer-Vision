# Bab 9: Motion Estimation

## 📋 Daftar Isi
1. [Pendahuluan](#1-pendahuluan)
2. [Translational Motion](#2-translational-motion)
3. [Optical Flow](#3-optical-flow)
4. [Parametric Motion Models](#4-parametric-motion-models)
5. [Spline-Based Motion](#5-spline-based-motion)
6. [Layered Motion](#6-layered-motion)
7. [Deep Learning untuk Motion](#7-deep-learning-untuk-motion)

---

## 1. Pendahuluan

### 1.1 Apa itu Motion Estimation?

**Motion Estimation** adalah proses mengestimasi gerakan/perpindahan piksel atau objek antara frame video berturutan. Ini adalah fundamental untuk banyak aplikasi computer vision.

### 1.2 Aplikasi

1. **Video Compression**: MPEG, H.264, H.265 menggunakan motion compensation
2. **Video Stabilization**: Menghilangkan goyangan kamera
3. **Object Tracking**: Pelacakan objek bergerak
4. **Action Recognition**: Mengenali aktivitas dari gerakan
5. **Autonomous Driving**: Estimasi ego-motion dan obstacle motion
6. **Frame Interpolation**: Membuat slow-motion
7. **Video Editing**: Rotoscoping, compositing

### 1.3 Jenis Motion

| Jenis | Karakteristik | Contoh |
|-------|--------------|--------|
| **Camera Motion** | Global, affects all pixels | Panning, tilting, zooming |
| **Object Motion** | Local, independent motion | Walking person, moving car |
| **Articulated Motion** | Connected rigid parts | Human body, robot arm |
| **Deformable Motion** | Non-rigid | Cloth, water, face |

### 1.4 Representasi Motion

1. **Motion Vectors**: Per-pixel atau per-block displacement
2. **Optical Flow**: Dense motion field
3. **Parametric Models**: Global transformation (affine, homography)
4. **Layered Models**: Multiple motion layers
5. **Scene Flow**: 3D motion field

---

## 2. Translational Motion

### 2.1 Block Matching

Metode paling sederhana untuk motion estimation, digunakan di video compression.

**Prinsip**: Untuk setiap block di frame current, cari block paling mirip di frame reference.

**Sum of Absolute Differences (SAD)**:
$$\text{SAD}(dx, dy) = \sum_{(i,j) \in \text{block}} |I_1(i,j) - I_0(i+dx, j+dy)|$$

**Sum of Squared Differences (SSD)**:
$$\text{SSD}(dx, dy) = \sum_{(i,j) \in \text{block}} (I_1(i,j) - I_0(i+dx, j+dy))^2$$

### 2.2 Search Strategies

**Full Search (Exhaustive)**:
- Cari semua posisi dalam search window
- Optimal tapi lambat
- Complexity: $O(W^2 \times B^2)$ untuk window W dan block B

**Three-Step Search**:
```
1. Cari di 9 posisi dengan step size = search_range/2
2. Pilih posisi terbaik, kurangi step size setengah
3. Ulangi sampai step size = 1
```

**Diamond Search**:
```
1. Large Diamond Pattern (9 points)
2. Jika center terbaik → Small Diamond Pattern
3. Jika bukan center → Pindah ke titik terbaik, ulangi
```

**Hexagonal Search**:
- Hexagon pattern untuk search
- Lebih efisien dari diamond

### 2.3 Hierarchical/Coarse-to-Fine

```
1. Bangun image pyramid (Gaussian)
2. Mulai dari level paling kasar
3. Estimasi motion dengan search range kecil
4. Propagasi ke level lebih halus
5. Refine dengan search range kecil
```

**Keuntungan**:
- Menangani large motion
- Lebih cepat
- Lebih akurat

### 2.4 Sub-pixel Accuracy

Untuk akurasi sub-pixel:

1. **Parabolic Fitting**: Fit parabola ke 3 titik terbaik
2. **Bilinear Interpolation**: Interpolasi cost function
3. **Phase Correlation**: FFT-based, natural sub-pixel

**Phase Correlation**:
$$R = \mathcal{F}^{-1}\left(\frac{F_1 \cdot F_0^*}{|F_1 \cdot F_0^*|}\right)$$

Peak location memberikan translasi.

---

## 3. Optical Flow

### 3.1 Definisi

**Optical Flow** adalah apparent motion dari brightness patterns dalam image sequence. Representasi dense: motion vector untuk setiap pixel.

$$\mathbf{u}(x, y) = (u(x,y), v(x,y))$$

Di mana $u, v$ adalah horizontal dan vertical velocity.

### 3.2 Brightness Constancy Assumption

Asumsi fundamental:
$$I(x, y, t) = I(x + u, y + v, t + 1)$$

**Taylor expansion**:
$$I(x + u, y + v, t + 1) \approx I(x, y, t) + I_x u + I_y v + I_t$$

**Optical Flow Constraint**:
$$I_x u + I_y v + I_t = 0$$

atau
$$\nabla I \cdot \mathbf{u} + I_t = 0$$

### 3.3 Aperture Problem

Dari satu persamaan, kita tidak bisa menentukan 2 unknowns $(u, v)$.

**Aperture Problem**: Hanya bisa menentukan komponen flow **normal** ke edge.

**Solusi**: Tambahkan constraints:
- Spatial smoothness (Horn-Schunck)
- Local constancy (Lucas-Kanade)

### 3.4 Lucas-Kanade Method

**Asumsi**: Flow konstan dalam small window.

Untuk setiap pixel $(x, y)$, minimize dalam window $W$:
$$E = \sum_{(x_i, y_i) \in W} (I_x(x_i, y_i) u + I_y(x_i, y_i) v + I_t(x_i, y_i))^2$$

**Solusi (least squares)**:
$$\begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} \sum I_x^2 & \sum I_x I_y \\ \sum I_x I_y & \sum I_y^2 \end{bmatrix}^{-1} \begin{bmatrix} -\sum I_x I_t \\ -\sum I_y I_t \end{bmatrix}$$

atau $A^T A \mathbf{u} = -A^T \mathbf{b}$

**Kondisi untuk solusi yang baik**:
- $A^T A$ harus invertible
- Eigenvalues harus cukup besar
- Ini sama dengan Harris corner criterion!

### 3.5 Horn-Schunck Method

**Asumsi**: Flow bervariasi smooth secara spasial.

**Energy function**:
$$E = \int \int \left[ (I_x u + I_y v + I_t)^2 + \alpha^2 (|\nabla u|^2 + |\nabla v|^2) \right] dx dy$$

- Term pertama: brightness constancy
- Term kedua: smoothness regularization
- $\alpha$: smoothness weight

**Euler-Lagrange equations**:
$$I_x(I_x u + I_y v + I_t) - \alpha^2 \nabla^2 u = 0$$
$$I_y(I_x u + I_y v + I_t) - \alpha^2 \nabla^2 v = 0$$

**Iterative solution** (Gauss-Seidel):
$$u^{n+1} = \bar{u}^n - \frac{I_x(I_x \bar{u}^n + I_y \bar{v}^n + I_t)}{\alpha^2 + I_x^2 + I_y^2}$$
$$v^{n+1} = \bar{v}^n - \frac{I_y(I_x \bar{u}^n + I_y \bar{v}^n + I_t)}{\alpha^2 + I_x^2 + I_y^2}$$

Di mana $\bar{u}, \bar{v}$ adalah average dari neighbors.

### 3.6 Coarse-to-Fine Optical Flow

Untuk large displacement:

```
1. Build image pyramid
2. At coarsest level: compute flow (small search)
3. Upsample flow to next level
4. Warp frame 2 using current flow
5. Compute residual flow
6. Add to upsampled flow
7. Repeat until finest level
```

### 3.7 Modern Variational Methods

**TV-L1 Optical Flow**:
$$E = \int \int \left[ |I_x u + I_y v + I_t| + \lambda |\nabla u| + \lambda |\nabla v| \right] dx dy$$

Menggunakan:
- L1 data term (robust to outliers)
- Total Variation regularization (preserves edges)

**Implementation**: OpenCV `cv2.optflow.DualTVL1OpticalFlow_create()`

---

## 4. Parametric Motion Models

### 4.1 Motivasi

Untuk gerakan yang mengikuti model global (camera motion):
- Lebih efisien (fewer parameters)
- Lebih robust (outlier rejection)
- Interpolasi natural

### 4.2 Motion Models

**Translation (2 DOF)**:
$$\begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$

**Affine (6 DOF)**:
$$\begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} a_1 & a_2 \\ a_4 & a_5 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} a_3 \\ a_6 \end{bmatrix}$$

**Quadratic (12 DOF)**:
$$u = a_1 + a_2 x + a_3 y + a_4 x^2 + a_5 xy + a_6 y^2$$
$$v = a_7 + a_8 x + a_9 y + a_{10} x^2 + a_{11} xy + a_{12} y^2$$

**Projective/Homography (8 DOF)**:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} \sim H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

### 4.3 Direct Methods untuk Parametric Motion

**Lucas-Kanade untuk parametric motion**:

Minimize:
$$E(\mathbf{p}) = \sum_{\mathbf{x}} [I_1(\mathbf{W}(\mathbf{x}; \mathbf{p})) - I_0(\mathbf{x})]^2$$

Update:
$$\Delta \mathbf{p} = H^{-1} J^T \mathbf{e}$$

Di mana:
- $H = J^T J$ (Gauss-Newton Hessian)
- $J = \nabla I_1 \frac{\partial \mathbf{W}}{\partial \mathbf{p}}$
- $\mathbf{e} = I_0 - I_1(\mathbf{W})$

### 4.4 Robust Estimation

Untuk handle outliers (occlusion, independent motion):

**M-estimators**:
$$E = \sum_{\mathbf{x}} \rho(I_1(\mathbf{W}(\mathbf{x})) - I_0(\mathbf{x}))$$

**Common robust functions**:
- Huber: $\rho(x) = \begin{cases} x^2/2 & |x| \leq k \\ k|x| - k^2/2 & |x| > k \end{cases}$
- Tukey: $\rho(x) = \begin{cases} c^2/6(1-(1-x^2/c^2)^3) & |x| \leq c \\ c^2/6 & |x| > c \end{cases}$

**IRLS (Iteratively Reweighted Least Squares)**:
```
1. Compute flow dengan standard LS
2. Compute residuals
3. Compute weights: w_i = ρ'(e_i)/e_i
4. Solve weighted LS
5. Iterate sampai konvergen
```

---

## 5. Spline-Based Motion

### 5.1 Motivasi

Untuk motion yang tidak bisa dimodelkan dengan parametric sederhana tapi butuh smoothness.

### 5.2 B-Spline Motion Fields

Motion field direpresentasikan sebagai B-spline:
$$u(x, y) = \sum_{i,j} c_{ij}^u B_i(x) B_j(y)$$
$$v(x, y) = \sum_{i,j} c_{ij}^v B_i(x) B_j(y)$$

Di mana $B_i$ adalah B-spline basis functions.

**Keuntungan**:
- Smooth by construction
- Local control
- Efficient computation
- Natural regularization

### 5.3 Mesh-Based Motion

Divide image ke dalam mesh, setiap vertex punya motion vector.

**Interior points**: Bilinear interpolation dari vertices.

**Regularization**: Minimize mesh distortion.

---

## 6. Layered Motion

### 6.1 Konsep

Scene terdiri dari multiple layers, masing-masing dengan motion sendiri.

**Model**:
- Set of layers: $\{L_1, L_2, ..., L_K\}$
- Each layer has:
  - Motion model $M_k$
  - Alpha mask $\alpha_k$
  - Appearance $A_k$

### 6.2 Layer Extraction

**Problem**: Given video, extract:
1. Number of layers
2. Motion per layer
3. Layer assignment per pixel

**EM Algorithm approach**:
```
E-step: Assign pixels to layers based on motion consistency
M-step: Estimate motion per layer, update appearances
```

### 6.3 Alpha Matting

Untuk smooth boundaries:
$$I(x) = \sum_k \alpha_k(x) L_k(x)$$

dengan constraint: $\sum_k \alpha_k(x) = 1$

### 6.4 Applications

1. **Video Segmentation**: Separate foreground/background
2. **Video Editing**: Composite new elements
3. **Video Compression**: Efficient coding per layer
4. **Motion Analysis**: Understand scene structure

---

## 7. Deep Learning untuk Motion

### 7.1 FlowNet

**FlowNet (2015)**: CNN end-to-end untuk optical flow.

**Architecture**:
- Input: Stacked images (6 channels)
- Encoder: Convolutional
- Decoder: Deconvolutional dengan skip connections
- Output: Flow field (2 channels)

**Variants**:
- FlowNetS: Simple stacking
- FlowNetC: Correlation layer

### 7.2 FlowNet 2.0

Improvements:
- Stacking multiple FlowNets
- Specialized networks untuk small displacement
- Schedule-based training

### 7.3 PWC-Net

**Pyramid, Warping, Cost-volume**:

```
For each pyramid level:
1. Warp features dari frame 2 ke frame 1
2. Build cost volume
3. Estimate flow dari cost volume + context
4. Upsample dan refine
```

**Keuntungan**:
- Compact (8.75M params vs 162M FlowNet2)
- Accurate
- Fast

### 7.4 RAFT (Recurrent All-Pairs Field Transform)

**State-of-the-art** (2020):

1. **Feature Extraction**: Extract features dari kedua frames
2. **Correlation Volume**: All-pairs correlation
3. **Iterative Updates**: GRU-based refinement

**Key innovations**:
- Build full correlation volume
- Iterative refinement dengan GRU
- Multi-scale correlation lookup

### 7.5 Scene Flow

**3D motion field** in real world:
$$\mathbf{s}(X, Y, Z) = (S_X, S_Y, S_Z)$$

**Relation to optical flow**:
Optical flow adalah projection dari scene flow.

**Deep Scene Flow**:
- PointPWC-Net
- FlowNet3D
- HPLFlowNet

---

## 📊 Perbandingan Metode

| Metode | Speed | Accuracy | Large Motion | Robust |
|--------|-------|----------|--------------|--------|
| Block Matching | Fast | Low | Limited | No |
| Lucas-Kanade | Fast | Medium | Limited* | No |
| Horn-Schunck | Slow | Medium | Limited | No |
| TV-L1 | Medium | High | Good | Yes |
| FlowNet | Fast | Medium | Good | Medium |
| PWC-Net | Fast | High | Good | Good |
| RAFT | Medium | Highest | Excellent | Good |

*Dengan coarse-to-fine pyramid

---

## 🔧 Evaluasi Optical Flow

### Metrics

**End-Point Error (EPE)**:
$$\text{EPE} = \frac{1}{N} \sum_i \|(u_i, v_i) - (u_i^{gt}, v_i^{gt})\|_2$$

**Angular Error (AE)**:
$$\text{AE} = \arccos\left(\frac{1 + u \cdot u^{gt} + v \cdot v^{gt}}{\sqrt{1 + u^2 + v^2} \sqrt{1 + (u^{gt})^2 + (v^{gt})^2}}\right)$$

### Benchmarks

1. **Middlebury Flow**: http://vision.middlebury.edu/flow/
2. **KITTI Flow**: http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php
3. **Sintel**: http://sintel.is.tue.mpg.de/

---

## 📚 Ringkasan

| Topik | Metode Utama | Aplikasi |
|-------|--------------|----------|
| Block Matching | SAD, SSD, Diamond Search | Video compression |
| Sparse Flow | Lucas-Kanade | Feature tracking |
| Dense Flow | Horn-Schunck, TV-L1 | Video analysis |
| Parametric | Direct methods | Video stabilization |
| Layered | EM, MRF | Video segmentation |
| Deep Learning | RAFT, PWC-Net | General purpose |

---

## 📚 Referensi

1. Szeliski, R. - Computer Vision: Algorithms and Applications, Chapter 9
2. Horn, B. & Schunck, B. - "Determining Optical Flow" (1981)
3. Lucas, B. & Kanade, T. - "An Iterative Image Registration Technique" (1981)
4. Teed, Z. & Deng, J. - "RAFT: Recurrent All-Pairs Field Transforms" (2020)

---

*Materi ini adalah bagian dari Praktikum Computer Vision*
