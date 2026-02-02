# Bab 12: Depth Estimation

## Pendahuluan

**Depth Estimation** adalah proses memperkirakan jarak objek dari kamera. Informasi kedalaman sangat penting untuk pemahaman scene 3D, navigasi robot, augmented reality, dan berbagai aplikasi computer vision lainnya.

### Jenis Depth Estimation
1. **Stereo Matching** - Dari pasangan gambar stereo
2. **Multi-view Stereo** - Dari banyak gambar
3. **Time-of-Flight** - Sensor aktif
4. **Structured Light** - Proyeksi pola
5. **Monocular Depth** - Dari single image (learning-based)

---

## 1. Stereo Vision Fundamentals

### 1.1 Stereo Geometry

Dua kamera dengan baseline $b$ dan focal length $f$:

**Disparity:**
$$d = x_L - x_R = \frac{bf}{Z}$$

**Depth dari disparity:**
$$Z = \frac{bf}{d}$$

dimana:
- $Z$ = depth (jarak dari kamera)
- $b$ = baseline (jarak antar kamera)
- $f$ = focal length (dalam pixels)
- $d$ = disparity

### 1.2 Epipolar Constraint

Untuk stereo rectified images:
- Corresponding points berada pada baris yang sama
- Pencarian menjadi 1D problem
- Mengurangi kompleksitas dari $O(W \times H)$ ke $O(W)$

### 1.3 Stereo Rectification

**Tujuan:** Transform images sehingga epipolar lines horizontal dan aligned.

**Proses:**
1. Compute essential matrix E
2. Find rotation matrices $R_1, R_2$
3. Apply homographies ke kedua images
4. Resulting images: corresponding points pada same row

---

## 2. Stereo Matching Algorithms

### 2.1 Local Methods

#### Block Matching

Matching cost untuk pixel $(x, y)$ dengan disparity $d$:

$$C(x, y, d) = \sum_{(u,v) \in W} \rho(I_L(x+u, y+v), I_R(x+u-d, y+v))$$

**Cost Functions:**

1. **Sum of Absolute Differences (SAD):**
$$SAD = \sum |I_L - I_R|$$

2. **Sum of Squared Differences (SSD):**
$$SSD = \sum (I_L - I_R)^2$$

3. **Normalized Cross-Correlation (NCC):**
$$NCC = \frac{\sum(I_L - \bar{I_L})(I_R - \bar{I_R})}{\sqrt{\sum(I_L - \bar{I_L})^2 \sum(I_R - \bar{I_R})^2}}$$

4. **Census Transform:**
- Binary string dari comparisons dengan center pixel
- Robust terhadap illumination changes

#### Winner-Take-All (WTA)

$$d^*(x, y) = \arg\min_d C(x, y, d)$$

### 2.2 Semi-Global Matching (SGM)

**Idea:** Agregasi cost sepanjang multiple paths, bukan local window saja.

**Energy Function:**
$$E(D) = \sum_p(C(p, D_p) + \sum_{q \in N_p} P_1 \cdot T[|D_p - D_q| = 1] + \sum_{q \in N_p} P_2 \cdot T[|D_p - D_q| > 1])$$

dimana:
- $P_1$ = penalty untuk small disparity change
- $P_2$ = penalty untuk large disparity change

**Aggregation:**
$$L_r(p, d) = C(p, d) + \min \begin{cases}
L_r(p-r, d) \\
L_r(p-r, d-1) + P_1 \\
L_r(p-r, d+1) + P_1 \\
\min_i L_r(p-r, i) + P_2
\end{cases}$$

Agregasi dari 8 atau 16 directions, lalu sum:
$$S(p, d) = \sum_r L_r(p, d)$$

### 2.3 Global Methods

#### Graph Cuts

**Energy minimization:**
$$E(f) = E_{data}(f) + E_{smooth}(f)$$

$$E_{data} = \sum_p D_p(f_p)$$
$$E_{smooth} = \sum_{(p,q)} V_{pq}(f_p, f_q)$$

Solved dengan α-expansion atau α-β swap.

#### Belief Propagation

- Message passing pada MRF
- Iterative updates

---

## 3. Deep Learning untuk Stereo

### 3.1 Matching Cost Learning

**MC-CNN (Matching Cost CNN):**
- Learn feature descriptors untuk matching
- Siamese network architecture

### 3.2 End-to-End Networks

#### DispNet

```
Architecture:
Encoder (contracting) → Decoder (expanding)
                    ↓
              Disparity maps at multiple scales
```

#### PSMNet (Pyramid Stereo Matching)

1. **Spatial Pyramid Pooling** - Multi-scale features
2. **3D CNN Cost Volume** - Regularization
3. **Stacked Hourglass** - Refinement

**Cost Volume:**
$$C(d, x, y) = \frac{1}{N_c} \sum_c f_L^c(x, y) \cdot f_R^c(x-d, y)$$

#### AANet (Adaptive Aggregation)

- Intra-scale aggregation
- Cross-scale aggregation
- Efficient tanpa 3D convolutions

#### RAFT-Stereo

- Correlation volumes
- Iterative updates (GRU-based)
- State-of-the-art accuracy

### 3.3 Loss Functions

**Supervised:**
$$L = \frac{1}{N} \sum_{i} |d_i - d_i^{gt}|$$

atau smooth L1:
$$L = \frac{1}{N} \sum_i smooth_{L1}(d_i - d_i^{gt})$$

**Self-supervised:**
$$L_{photo} = \frac{1}{N} \sum \rho(I_L, \hat{I}_L)$$

dimana $\hat{I}_L$ adalah warped image dari right ke left.

---

## 4. Monocular Depth Estimation

### 4.1 Depth from Single Image

**Challenge:** Ill-posed problem - infinite 3D scenes dapat menghasilkan same 2D image.

**Solution:** Learn depth priors dari data.

### 4.2 Supervised Monocular Depth

#### Eigen et al. (2014)

Multi-scale network:
1. **Coarse Network** - Global depth
2. **Fine Network** - Local refinement

#### DenseDepth

- Encoder: DenseNet pretrained pada ImageNet
- Decoder: Upsampling dengan skip connections
- Loss: Combination of L1, SSIM, gradient

**Loss Function:**
$$L = \lambda L_{depth} + L_{grad} + L_{SSIM}$$

$$L_{depth} = \frac{1}{n} \sum_i |d_i - d_i^*|$$

$$L_{grad} = \frac{1}{n} \sum_i(|\nabla_x(d_i - d_i^*)| + |\nabla_y(d_i - d_i^*)|)$$

#### MiDaS

- Robust across datasets
- Affine-invariant loss
- Mixed dataset training

**Affine-invariant loss:**
$$L = \frac{1}{n}\sum_i \rho(s \cdot d_i + t - d_i^*)$$

dimana $s, t$ adalah scale dan shift untuk alignment.

### 4.3 Self-Supervised Monocular Depth

#### Monodepth (Godard et al., 2017)

Training tanpa ground truth depth:
- Use stereo pairs during training
- Photometric consistency loss
- Disparity smoothness loss
- Left-right consistency

**Photometric Loss:**
$$L_p = \alpha \frac{1 - SSIM(I, \hat{I})}{2} + (1-\alpha)||I - \hat{I}||_1$$

**Smoothness Loss:**
$$L_s = |\partial_x d^*| e^{-|\partial_x I|} + |\partial_y d^*| e^{-|\partial_y I|}$$

#### Monodepth2 (Godard et al., 2019)

Improvements:
- Minimum reprojection loss (handles occlusion)
- Auto-masking stationary pixels
- Multi-scale appearance matching

**Minimum Reprojection:**
$$L_p = \min_{t'} pe(I_t, \hat{I}_{t' \rightarrow t})$$

### 4.4 Depth Anything / DPT

**Vision Transformer based:**
- ViT encoder
- Dense prediction decoder
- Excellent generalization

---

## 5. Multi-View Stereo (MVS)

### 5.1 Plane-Sweep Stereo

Untuk reference view dan multiple source views:

1. Define depth planes $Z_1, Z_2, ..., Z_D$
2. For each plane:
   - Warp source images ke reference
   - Compute matching cost
3. Select best depth per pixel

### 5.2 Patch-based MVS (PMVS)

1. **Feature Matching** - Sparse correspondences
2. **Patch Optimization** - Refine depth dan normal
3. **Patch Expansion** - Grow dari seeds
4. **Filtering** - Remove inconsistent patches

### 5.3 Learning-based MVS

#### MVSNet

**Architecture:**
1. Feature extraction (2D CNN)
2. Differentiable homography warping
3. Cost volume construction
4. 3D CNN regularization
5. Soft argmin depth regression

**Cost Volume:**
$$C_i(d) = f_{ref} \odot f_i(H_i(d))$$

dimana $H_i(d)$ adalah homography dari source $i$ ke reference pada depth $d$.

#### Cascade MVSNet

- Coarse-to-fine dengan narrowing depth range
- Reduces memory
- Improves accuracy

#### PatchmatchNet

- Differentiable PatchMatch
- Adaptive propagation
- Multi-scale processing

---

## 6. Depth Sensors

### 6.1 Time-of-Flight (ToF)

**Principle:**
$$Z = \frac{c \cdot \Delta t}{2}$$

dimana:
- $c$ = speed of light
- $\Delta t$ = round-trip time

**Types:**
- Pulsed ToF
- Continuous wave ToF (phase shift)

**Pros:** Dense depth, works in dark
**Cons:** Limited range, multi-path interference

### 6.2 Structured Light

**Principle:**
- Project known pattern
- Triangulate dari pattern deformation

**Examples:**
- Kinect v1 (IR pattern)
- Intel RealSense (IR stereo + pattern)

**Pros:** High accuracy indoor
**Cons:** Doesn't work outdoors (sunlight)

### 6.3 LiDAR

**Principle:** Laser-based ToF

**Types:**
- Mechanical (spinning)
- Solid-state
- Flash LiDAR

**Pros:** Long range, accurate
**Cons:** Sparse, expensive

### 6.4 Sensor Fusion

Combining:
- RGB + Depth (RGB-D)
- Stereo + LiDAR
- Camera + IMU + LiDAR

---

## 7. Depth Map Processing

### 7.1 Hole Filling

**Methods:**
1. Nearest neighbor interpolation
2. Inpainting (bilateral, guided filter)
3. Learning-based completion

### 7.2 Depth Upsampling

Dari low-res depth + high-res RGB:

**Guided Filter:**
$$D^{HR} = GF(D^{LR}, I^{HR})$$

**Deep Learning:**
- MSG-Net
- DKN (Deformable Kernel Network)

### 7.3 Depth Refinement

**Edge-aware smoothing:**
- Bilateral filter
- Domain transform
- Guided filter

**Joint bilateral:**
$$D'(p) = \frac{1}{W} \sum_q G_{\sigma_s}(||p-q||) G_{\sigma_r}(|I(p)-I(q)|) D(q)$$

---

## 8. Evaluation Metrics

### 8.1 Error Metrics

**Absolute Relative Error:**
$$AbsRel = \frac{1}{n}\sum_i \frac{|d_i - d_i^*|}{d_i^*}$$

**Squared Relative Error:**
$$SqRel = \frac{1}{n}\sum_i \frac{(d_i - d_i^*)^2}{d_i^*}$$

**RMSE:**
$$RMSE = \sqrt{\frac{1}{n}\sum_i(d_i - d_i^*)^2}$$

**RMSE (log):**
$$RMSE_{log} = \sqrt{\frac{1}{n}\sum_i(\log d_i - \log d_i^*)^2}$$

### 8.2 Accuracy Metrics

**Threshold Accuracy:**
$$\delta_t = \%\ of\ d_i\ s.t.\ \max(\frac{d_i}{d_i^*}, \frac{d_i^*}{d_i}) < t$$

Common thresholds: $t = 1.25, 1.25^2, 1.25^3$

### 8.3 Disparity Error

**End-Point Error (EPE):**
$$EPE = \frac{1}{n}\sum_i |d_i - d_i^*|$$

**Bad Pixel Percentage:**
$$\%\ pixels\ where\ |d - d^*| > \tau\ and\ |d - d^*|/d^* > \delta$$

Typical: $\tau = 3, \delta = 0.05$

---

## 9. Aplikasi

### 9.1 3D Reconstruction

Depth maps → Point clouds → Mesh:
$$\mathbf{X} = K^{-1} \cdot Z \cdot \mathbf{x}$$

### 9.2 Autonomous Vehicles

- Obstacle detection
- Free space estimation
- 3D object detection

### 9.3 Augmented Reality

- Occlusion handling
- Object placement
- Physics simulation

### 9.4 Robot Navigation

- Path planning
- Obstacle avoidance
- Manipulation

### 9.5 Computational Photography

- Bokeh effect
- Refocusing
- View synthesis

---

## 10. Ringkasan

| Method | Input | Pros | Cons |
|--------|-------|------|------|
| Stereo | 2 images | No scale ambiguity | Calibration required |
| Monocular (supervised) | 1 image | Simple setup | Needs GT depth |
| Monocular (self-supervised) | Video | No GT needed | Scale ambiguity |
| MVS | N images | High detail | Slow |
| ToF | Active sensor | Works in dark | Limited range |
| Structured Light | Active sensor | High accuracy | Indoor only |
| LiDAR | Active sensor | Long range | Sparse, expensive |

---

## Referensi

1. Scharstein, D., & Szeliski, R. (2002). A Taxonomy and Evaluation of Dense Two-Frame Stereo Correspondence Algorithms
2. Hirschmuller, H. (2008). Stereo Processing by Semi-Global Matching and Mutual Information
3. Godard, C., et al. (2017). Unsupervised Monocular Depth Estimation with Left-Right Consistency
4. Chang, J. R., & Chen, Y. S. (2018). Pyramid Stereo Matching Network
5. Ranftl, R., et al. (2020). Towards Robust Monocular Depth Estimation
