# Bab 11: Structure from Motion dan SLAM

## Pendahuluan

**Structure from Motion (SfM)** adalah teknik untuk merekonstruksi struktur 3D dari sekuens gambar 2D, sekaligus memulihkan posisi kamera. **SLAM (Simultaneous Localization and Mapping)** menggabungkan estimasi pose kamera dengan pembuatan peta lingkungan secara real-time.

### Aplikasi
- **Fotogrametri** - Pembuatan model 3D dari foto
- **Autonomous Vehicles** - Navigasi dan pemetaan
- **Augmented Reality** - Tracking dan scene understanding
- **Robotika** - Localization dan mapping
- **Surveying** - Pemetaan topografi

---

## 1. Geometri Dua View

### 1.1 Epipolar Geometry

Hubungan geometris antara dua view dari scene yang sama.

#### Fundamental Matrix (F)
Untuk uncalibrated cameras:

$$x'^T F x = 0$$

dimana:
- $x, x'$ = corresponding points di image 1 dan 2
- $F$ = 3×3 fundamental matrix (rank 2)

#### Essential Matrix (E)
Untuk calibrated cameras:

$$\hat{x}'^T E \hat{x} = 0$$

dimana $\hat{x} = K^{-1}x$ (normalized coordinates)

Hubungan:
$$E = K'^T F K$$

#### Dekomposisi Essential Matrix
Essential matrix dapat didekomposisi menjadi:

$$E = [t]_\times R$$

dimana:
- $R$ = rotation matrix
- $t$ = translation vector
- $[t]_\times$ = skew-symmetric matrix dari $t$

### 1.2 Epipolar Lines dan Epipoles

**Epipole** adalah proyeksi pusat kamera satu ke image lain:
- $e = F^T e' = 0$ (null space of $F^T$)
- $e' = F e = 0$ (null space of $F$)

**Epipolar line** untuk point $x$:
$$l' = Fx$$
Point $x'$ harus berada pada line $l'$.

### 1.3 Estimasi Fundamental Matrix

#### 8-Point Algorithm (Normalized)

1. **Normalisasi** koordinat untuk stabilitas numerik
2. **Set up** linear system $Af = 0$
3. **Solve** dengan SVD
4. **Enforce** rank-2 constraint
5. **Denormalize** hasil

```
Algorithm: Normalized 8-Point Algorithm
Input: Point correspondences {(x_i, x'_i)}
Output: Fundamental matrix F

1. Normalize points:
   T, T' = normalization transforms
   x̂_i = T x_i
   x̂'_i = T' x'_i

2. Build matrix A where each row:
   [x'x, x'y, x', y'x, y'y, y', x, y, 1]

3. Solve Af = 0 dengan SVD
   f = last column of V

4. Reshape f ke F̂ (3x3)

5. Enforce rank 2:
   F̂ = UDV^T
   D(3,3) = 0
   F̂ = UD'V^T

6. Denormalize:
   F = T'^T F̂ T
```

### 1.4 RANSAC untuk Robust Estimation

```
Algorithm: RANSAC Fundamental Matrix
Input: Point correspondences, threshold τ
Output: Best F, inliers

1. for iteration = 1 to max_iterations:
   a. Sample 8 random correspondences
   b. Compute F using 8-point algorithm
   c. For each correspondence (x, x'):
      - Compute epipolar line l' = Fx
      - Compute distance d = |x'^T l'| / ||l'||
      - If d < τ: mark as inlier
   d. If #inliers > best_inliers:
      - Update best F
      - Store inliers

2. Recompute F using all inliers
3. Return F, inliers
```

---

## 2. Triangulation

### 2.1 Linear Triangulation

Diberikan projection matrices $P, P'$ dan corresponding points $x, x'$, triangulasi mencari 3D point $X$.

$$x = PX \Rightarrow x \times PX = 0$$

Expand menjadi linear system:
$$\begin{bmatrix}
xp_3^T - p_1^T \\
yp_3^T - p_2^T \\
x'p'_3^T - p'_1^T \\
y'p'_3^T - p'_2^T
\end{bmatrix} X = 0$$

Solve dengan SVD (DLT method).

### 2.2 Optimal Triangulation

**Midpoint Method:**
- Temukan titik terdekat pada dua rays
- Rata-rata sebagai 3D point

**Geometric Error Minimization:**
- Minimize reprojection error
- Non-linear optimization

---

## 3. Structure from Motion Pipeline

### 3.1 Incremental SfM

Pipeline klasik untuk SfM:

```
Algorithm: Incremental SfM
Input: Image set {I_1, ..., I_n}
Output: 3D points, camera poses

1. Feature Detection & Matching
   - Detect features (SIFT, ORB) di semua images
   - Match features antar image pairs
   - Geometric verification dengan F-matrix

2. Initialize dengan Two-View Reconstruction
   - Select image pair dengan banyak matches
   - Estimate F → E → R, t
   - Triangulate initial points

3. Incremental Registration
   For each remaining image:
   a. Find 2D-3D correspondences (PnP)
   b. Estimate camera pose
   c. Triangulate new points
   d. Bundle adjustment (optional, setiap N images)

4. Final Bundle Adjustment
   - Optimize semua cameras dan points
   - Minimize total reprojection error
```

### 3.2 Global SfM

```
Algorithm: Global SfM
Input: Pairwise relative poses
Output: Global camera poses, 3D points

1. Rotation Averaging
   - Build rotation graph
   - Estimate global rotations

2. Translation Averaging
   - Scale consistency
   - Global translation estimation

3. Triangulation
   - Multiple view triangulation

4. Bundle Adjustment
```

### 3.3 Bundle Adjustment

**Objective Function:**

$$\min_{R_i, t_i, X_j} \sum_{i,j} \rho(||x_{ij} - \pi(R_i, t_i, X_j)||^2)$$

dimana:
- $\pi$ = projection function
- $\rho$ = robust loss function (Huber, Cauchy)
- $x_{ij}$ = observed 2D point
- $X_j$ = 3D point
- $R_i, t_i$ = camera $i$ pose

**Sparsity Pattern:**
- Jacobian memiliki block-sparse structure
- Schur complement untuk efficient solving

### 3.4 Perspective-n-Point (PnP)

Estimasi camera pose dari 3D-2D correspondences.

**Metode:**
1. **P3P** - Minimal 3 points (4 solutions)
2. **EPnP** - Efficient untuk n points
3. **DLT** - Direct Linear Transform
4. **RANSAC + PnP** - Robust estimation

---

## 4. Visual SLAM

### 4.1 SLAM Problem Formulation

SLAM menyelesaikan:
1. **Localization**: Dimana robot/kamera berada?
2. **Mapping**: Seperti apa lingkungan?

**State:**
$$x_t = \{T_1, ..., T_t, M\}$$
- $T_i$ = camera pose pada waktu $i$
- $M$ = map (3D points, landmarks, dll)

### 4.2 Filter-based SLAM

#### Extended Kalman Filter (EKF) SLAM

**State Vector:**
$$x = [r, m_1, ..., m_n]^T$$
- $r$ = robot pose (6-DOF)
- $m_i$ = landmark positions

**Prediction:**
$$x_t^- = f(x_{t-1}, u_t) + w_t$$

**Update:**
$$K = P^- H^T (H P^- H^T + R)^{-1}$$
$$x_t = x_t^- + K(z - h(x_t^-))$$
$$P_t = (I - KH)P^-$$

**Limitasi:**
- $O(n^2)$ complexity per update
- Gaussian assumption
- Linearization errors

### 4.3 Graph-based SLAM

**Pose Graph:**
- Nodes = camera poses
- Edges = relative pose constraints

**Factor Graph:**
- Variable nodes = poses, landmarks
- Factor nodes = measurements

**Optimization:**
$$\min_x \sum_k ||e_k(x)||^2_{\Sigma_k}$$

dimana $e_k$ adalah error function untuk setiap factor.

### 4.4 ORB-SLAM Pipeline

```
ORB-SLAM Architecture:
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐   │
│  │ Tracking │ → │ Local    │ → │ Loop Closing │   │
│  │          │   │ Mapping  │   │              │   │
│  └──────────┘   └──────────┘   └──────────────┘   │
│       ↑              ↑               ↓             │
│       │              │         ┌─────────┐         │
│       └──────────────┴─────────│   Map   │         │
│                                └─────────┘         │
└─────────────────────────────────────────────────────┘
```

**1. Tracking Thread:**
- ORB feature extraction
- Initial pose estimation
- Track local map
- New keyframe decision

**2. Local Mapping Thread:**
- Process new keyframes
- Local BA
- Map point culling
- New map point creation

**3. Loop Closing Thread:**
- Loop detection (Bag of Words)
- Loop correction
- Pose graph optimization

### 4.5 Direct vs Feature-based

| Aspect | Feature-based | Direct |
|--------|---------------|--------|
| Data Association | Explicit matches | Implicit (photometric) |
| Information | Sparse keypoints | All pixels |
| Computation | Faster | More intensive |
| Texture | Requires texture | Works on gradients |
| Examples | ORB-SLAM | LSD-SLAM, DSO |

---

## 5. Visual Odometry

### 5.1 Monocular Visual Odometry

```
Algorithm: Monocular VO
Input: Image sequence
Output: Camera trajectory

1. for each frame t:
   a. Detect features
   b. Match dengan frame t-1
   c. Estimate Essential Matrix E
   d. Decompose E → R, t (scale ambiguity!)
   e. Update pose: T_t = T_{t-1} · [R|t]
   f. Triangulate new 3D points
```

**Scale Ambiguity:**
- Monocular tidak bisa recover absolute scale
- Perlu external source (IMU, known object, motion constraints)

### 5.2 Stereo Visual Odometry

```
Algorithm: Stereo VO

1. Stereo matching → Disparity map → Depth
2. Track features
3. 3D-3D atau 3D-2D pose estimation
4. No scale ambiguity!
```

### 5.3 RGB-D Visual Odometry

```
Algorithm: RGB-D VO

1. Get depth dari sensor (Kinect, RealSense)
2. Project ke 3D (back-projection)
3. ICP atau feature-based alignment
4. Dense atau semi-dense approach
```

---

## 6. Loop Closure

### 6.1 Place Recognition

**Bag of Visual Words (BoVW):**
1. Offline: Build vocabulary dari training features
2. Online: Convert image ke BoW vector
3. Compare dengan database images

**Deep Learning Approaches:**
- NetVLAD
- Global descriptors (GeM, etc.)

### 6.2 Loop Verification

1. **Geometric Verification**
   - Estimate fundamental matrix
   - Check inlier ratio

2. **Temporal Consistency**
   - Multiple consecutive detections

### 6.3 Loop Correction

**Pose Graph Optimization:**

$$\min_{T_1,...,T_n} \sum_{(i,j)} ||T_i^{-1}T_j - \tilde{T}_{ij}||^2$$

Setelah loop detected, jalankan optimization untuk distribute error.

---

## 7. Multi-Sensor Fusion

### 7.1 Visual-Inertial Odometry (VIO)

Gabungkan visual dengan IMU:

**IMU Provides:**
- High-rate motion estimation
- Scale information
- Gravity direction

**Fusion Methods:**
1. **Loosely Coupled** - Independent estimates, late fusion
2. **Tightly Coupled** - Joint optimization
3. **Filter-based** (MSCKF) atau **Optimization-based** (VINS-Mono)

### 7.2 State Estimation

**IMU Preintegration:**
$$\Delta R_{ij} = \prod_{k=i}^{j-1} Exp((\omega_k - b_g) \Delta t)$$
$$\Delta v_{ij} = \sum_{k=i}^{j-1} \Delta R_{ik}(a_k - b_a) \Delta t$$
$$\Delta p_{ij} = \sum_{k=i}^{j-1} [\Delta v_{ik}\Delta t + \frac{1}{2}\Delta R_{ik}(a_k - b_a)\Delta t^2]$$

---

## 8. Deep Learning untuk SfM/SLAM

### 8.1 Learning-based Components

| Component | Deep Learning Approach |
|-----------|----------------------|
| Feature Detection | SuperPoint, D2-Net |
| Feature Matching | SuperGlue, LoFTR |
| Depth Estimation | Monodepth, MiDaS |
| Pose Estimation | PoseNet, VLocNet |
| Loop Closure | NetVLAD |

### 8.2 End-to-End Methods

**DROID-SLAM:**
- Dense BA dengan learned features
- Differentiable optimization

**DeepVO:**
- CNN-RNN untuk visual odometry
- End-to-end training

### 8.3 Self-supervised Depth & Ego-motion

**Monodepth2:**
- Train dengan photometric consistency
- No ground truth needed

Loss function:
$$L = \lambda_1 L_{photo} + \lambda_2 L_{smooth}$$

---

## 9. Implementasi Praktis

### 9.1 Libraries dan Frameworks

| Library | Type | Language |
|---------|------|----------|
| OpenCV | SfM, VO | C++, Python |
| COLMAP | Full SfM | C++ |
| ORB-SLAM3 | Real-time SLAM | C++ |
| OpenVSLAM | Modular SLAM | C++ |
| GTSAM | Factor graphs | C++ |
| g2o | Graph optimization | C++ |
| Open3D | 3D processing | C++, Python |

### 9.2 Evaluation Metrics

**Absolute Trajectory Error (ATE):**
$$ATE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}||trans(Q_i^{-1}S P_i)||^2}$$

**Relative Pose Error (RPE):**
$$RPE_i = (Q_i^{-1}Q_{i+\Delta})^{-1}(P_i^{-1}P_{i+\Delta})$$

### 9.3 Common Issues

1. **Scale Drift** - Akumulasi error pada monocular
2. **Loop Closure False Positives** - Perlu verification
3. **Feature Tracking Loss** - Motion blur, occlusion
4. **Computational Cost** - Real-time constraints
5. **Initialization** - Need good initial reconstruction

---

## 10. Ringkasan

| Konsep | Deskripsi |
|--------|-----------|
| Epipolar Geometry | Hubungan geometris dua views |
| Fundamental Matrix | Encodes epipolar geometry (uncalibrated) |
| Essential Matrix | Encodes epipolar geometry (calibrated) |
| Triangulation | Reconstruct 3D dari 2D correspondences |
| SfM | Offline 3D reconstruction |
| SLAM | Online localization + mapping |
| Bundle Adjustment | Joint optimization cameras + points |
| Loop Closure | Detect revisited places, correct drift |
| VIO | Visual + IMU fusion |

---

## Referensi

1. Hartley, R., & Zisserman, A. (2003). Multiple View Geometry in Computer Vision
2. Ma, Y., et al. (2003). An Invitation to 3-D Vision
3. Mur-Artal, R., et al. (2015). ORB-SLAM: A Versatile and Accurate Monocular SLAM System
4. Engel, J., et al. (2014). LSD-SLAM: Large-Scale Direct Monocular SLAM
5. Qin, T., et al. (2018). VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator
