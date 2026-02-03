# BAB 10: COMPUTATIONAL PHOTOGRAPHY
## Materi Pembelajaran

---

## 1. PENDAHULUAN

### 1.1 Definisi Computational Photography

**Computational Photography** adalah bidang yang menggabungkan teknik computer vision, graphics, dan image processing untuk meningkatkan atau memperluas kemampuan fotografi digital. Berbeda dengan fotografi tradisional yang mengandalkan optik dan sensor, computational photography menggunakan komputasi software untuk menghasilkan gambar yang tidak mungkin atau sulit diambil dengan kamera konvensional.

### 1.2 Evolusi Fotografi

```
Traditional Photography    → Digital Photography    → Computational Photography
(Optical + Film)             (Optical + Sensor)       (Optical + Sensor + Computing)
```

Kemampuan yang Ditambahkan:
- **Extended Dynamic Range**: Capture detail di highlight dan shadow
- **Depth Manipulation**: Blur background (bokeh), fokus adjustment
- **Super Resolution**: Meningkatkan resolusi beyond sensor capability
- **Noise Reduction**: Mengurangi noise tanpa kehilangan detail
- **Multi-frame Processing**: Menggabungkan multiple shots

### 1.3 Aplikasi Modern

| Aplikasi | Teknologi | Platform |
|----------|-----------|----------|
| Night Mode | Multi-frame HDR + Denoising | iPhone, Pixel |
| Portrait Mode | Depth estimation + Bokeh | Smartphone |
| Super Zoom | Super Resolution | Pixel |
| Astrophotography | Long exposure + Alignment | Pixel |
| ProRAW | Computational RAW | iPhone |

---

## 2. HIGH DYNAMIC RANGE (HDR) IMAGING

### 2.1 Dynamic Range Problem

**Dynamic Range** adalah rasio antara nilai terbesar dan terkecil yang dapat direpresentasikan. Kamera digital memiliki dynamic range terbatas (~10-12 stops), sementara scene nyata bisa mencapai >20 stops.

**Contoh Scene High Dynamic Range**:
- Indoor dengan window view (1:100,000 ratio)
- Night photography dengan lampu (1:1,000,000 ratio)
- Direct sunlight dengan shadows

### 2.2 Multi-Exposure HDR Pipeline

```
Multiple Exposures → Alignment → Merging → Tone Mapping → LDR Output
```

#### Step 1: Capture Multiple Exposures
Ambil beberapa gambar dengan exposure berbeda:
- Under-exposed: Detail di highlights
- Normal: Midtones
- Over-exposed: Detail di shadows

#### Step 2: Alignment
Karena handheld capture dapat menghasilkan slight movement, alignment diperlukan menggunakan:
- Feature-based alignment
- Intensity-based alignment (MTB - Median Threshold Bitmap)

#### Step 3: Merging to HDR
Combine pixels dari berbagai exposures:

$$I_{HDR}(x,y) = \frac{\sum_{i} w(Z_i) \cdot g(Z_i) / t_i}{\sum_{i} w(Z_i)}$$

Di mana:
- $Z_i$ = pixel value pada exposure $i$
- $t_i$ = exposure time
- $g()$ = inverse camera response function
- $w()$ = weighting function

**Algoritma Debevec-Malik**:
1. Estimate camera response function dari multiple exposures
2. Compute irradiance values untuk setiap pixel
3. Construct HDR radiance map

### 2.3 Tone Mapping

HDR image memiliki dynamic range yang melebihi display capability. **Tone mapping** mengkonversi HDR ke LDR yang dapat ditampilkan.

#### Global Tone Mapping
Fungsi yang sama untuk seluruh gambar:

$$L_{display} = \frac{L_{world}}{1 + L_{world}}$$

**Reinhard Global**:
$$L_d = \frac{L_w (1 + L_w/L_{white}^2)}{1 + L_w}$$

#### Local Tone Mapping
Adaptif berdasarkan luminance lokal:

**Reinhard Local**:
- Compute local adaptation luminance
- Apply dodging-and-burning

**Durand-Dorsey (Bilateral Filtering)**:
- Decompose ke base layer dan detail layer
- Compress base, preserve detail
- Recombine

#### Tone Mapping Operators di OpenCV:
1. **Drago**: Logarithmic mapping, mirip adaptasi mata
2. **Reinhard**: Photographic reproduction
3. **Mantiuk**: Perceptually uniform

---

## 3. IMAGE DENOISING

### 3.1 Noise Model

**Noise Sources**:
1. **Photon Noise (Shot Noise)**: Poisson distribution, inherent in light
2. **Read Noise**: Electronic, Gaussian distribution
3. **Dark Current**: Temperature-dependent
4. **Quantization Noise**: A/D conversion

**Combined Model**:
$$I_{observed} = I_{true} + n_{shot} + n_{read}$$

Di mana $n_{shot} \sim Poisson(I_{true})$ dan $n_{read} \sim \mathcal{N}(0, \sigma^2)$

### 3.2 Denoising Methods

#### Spatial Domain Methods

**Gaussian Blur**:
- Simple averaging
- Reduces noise but blurs edges
- $I_{out} = I_{in} * G_\sigma$

**Bilateral Filter**:
- Edge-preserving smoothing
- Weights berdasarkan spatial dan intensity proximity:

$$I_{out}(p) = \frac{1}{W_p} \sum_{q \in \Omega} G_{\sigma_s}(||p-q||) \cdot G_{\sigma_r}(|I(p)-I(q)|) \cdot I(q)$$

**Non-Local Means (NLM)**:
- Compare patches, not just pixels
- Lebih efektif untuk structured textures:

$$I_{out}(p) = \frac{1}{W_p} \sum_{q \in V(p)} w(p,q) \cdot I(q)$$

Di mana $w(p,q) = exp(-\frac{||P(p) - P(q)||^2}{h^2})$

#### Transform Domain Methods

**BM3D (Block-Matching and 3D Filtering)**:
1. Find similar patches (block matching)
2. Stack into 3D arrays
3. Apply 3D transform (DCT/wavelet)
4. Collaborative filtering
5. Aggregate patches

### 3.3 Multi-Frame Denoising

**Temporal Averaging**:
Jika noise independent antar frames:
$$\sigma_{combined} = \frac{\sigma}{\sqrt{N}}$$

Dengan $N$ frames, SNR meningkat $\sqrt{N}$ kali.

**Alignment + Averaging**:
1. Register frames (handle camera motion)
2. Detect motion regions (untuk ghost prevention)
3. Weighted averaging

---

## 4. FOCUS MANIPULATION

### 4.1 Depth of Field

**Depth of Field (DoF)** adalah range di mana objek terlihat sharp.

Faktor yang Mempengaruhi:
- **Aperture**: Larger aperture (f/1.4) → Shallow DoF
- **Focal Length**: Longer focal length → Shallower DoF
- **Distance**: Closer subject → Shallower DoF

### 4.2 Synthetic Bokeh (Portrait Mode)

**Pipeline**:
```
Input Image → Depth Estimation → Blur Kernel → Selective Blur → Output
```

#### Depth Estimation Methods:
1. **Dual-Camera Stereo**: Disparitas dari dua kamera
2. **Phase-Detection Autofocus**: Depth dari PDAF data
3. **Neural Network**: Monocular depth estimation

#### Blur Application:
**Circle of Confusion (CoC)**:
$$CoC = \frac{A \cdot f \cdot |D - D_f|}{D \cdot (D_f - f)}$$

Di mana:
- $A$ = aperture diameter
- $f$ = focal length
- $D$ = object distance
- $D_f$ = focus distance

**Implementation**:
```python
blur_amount = f(depth)  # Depth-dependent blur
for each pixel:
    if depth != focus_depth:
        apply_blur(pixel, blur_amount[depth])
```

### 4.3 Focus Stacking

Menggabungkan multiple images dengan focus berbeda untuk extended DoF:

**Algorithm**:
1. Capture images dengan berbagai focus distances
2. Align images (handle slight camera movement)
3. Compute sharpness measure per pixel (e.g., Laplacian)
4. Select sharpest pixel dari semua images
5. Blend seamlessly

**Sharpness Measures**:
- Laplacian magnitude
- Gradient magnitude
- Local variance

---

## 5. SUPER RESOLUTION

### 5.1 Single Image Super Resolution (SISR)

Meningkatkan resolusi dari satu gambar.

**Classical Methods**:
- Bicubic interpolation
- Lanczos resampling
- Edge-directed interpolation

**Learning-Based Methods**:
- SRCNN: First CNN-based approach
- EDSR: Enhanced Deep SR
- ESRGAN: Perceptual quality focus
- Real-ESRGAN: Real-world degradation

### 5.2 Multi-Frame Super Resolution

Menggabungkan informasi dari multiple frames dengan sub-pixel shifts.

**Requirements**:
1. Sub-pixel displacement antar frames
2. Accurate registration
3. Non-redundant information

**Algorithm**:
1. Capture burst of images
2. Estimate sub-pixel motion
3. Combine observations dalam high-res grid
4. Regularization untuk handle ill-posed problem

**Observation Model**:
$$y_k = D \cdot B \cdot M_k \cdot x + n_k$$

Di mana:
- $x$ = high-res image
- $M_k$ = motion model untuk frame $k$
- $B$ = blur kernel
- $D$ = downsampling operator
- $n_k$ = noise

---

## 6. EXPOSURE FUSION

### 6.1 Konsep

Exposure Fusion adalah alternatif HDR yang langsung menggabungkan multiple exposures tanpa membuat HDR intermediate.

**Keuntungan vs HDR + Tone Mapping**:
- Tidak perlu camera response calibration
- Tidak perlu tone mapping
- Hasil lebih natural

### 6.2 Mertens-Kautz-Van Reeth Fusion

**Quality Measures** per pixel per exposure:
1. **Contrast**: Laplacian filter, measures local contrast
2. **Saturation**: Standard deviation di R,G,B channels
3. **Well-exposedness**: Gaussian di tengah (0.5)

**Weight Calculation**:
$$W_{ijk} = C_{ijk}^{w_C} \cdot S_{ijk}^{w_S} \cdot E_{ijk}^{w_E}$$

**Fusion Process**:
1. Compute weights untuk setiap pixel di setiap exposure
2. Normalize weights
3. Laplacian pyramid blending untuk seamless result

### 6.3 Multi-Scale Fusion

**Laplacian Pyramid Blending**:
1. Build Laplacian pyramid untuk setiap exposure
2. Build Gaussian pyramid untuk weight maps
3. Blend each level: $L_{blend}^l = \sum_k G_k^l \cdot L_k^l$
4. Reconstruct dari blended pyramid

---

## 7. PANORAMA DAN IMAGE MOSAICING

### 7.1 Basic Pipeline

```
Images → Feature Extraction → Matching → Homography → Warping → Blending
```

### 7.2 Homography Estimation

Untuk planar scenes atau pure rotation:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

**RANSAC for Robust Estimation**:
1. Sample minimal set (4 correspondences)
2. Compute homography
3. Count inliers
4. Repeat dan pilih best

### 7.3 Cylindrical/Spherical Projection

Untuk wide FOV panoramas, projected ke cylindrical atau spherical surface untuk menghindari distorsi berlebihan.

**Cylindrical Projection**:
$$x' = f \cdot \arctan(\frac{x}{f}), \quad y' = f \cdot \frac{y}{\sqrt{x^2 + f^2}}$$

---

## 8. IMPLEMENTASI DI OPENCV

### 8.1 HDR dengan OpenCV

```python
# Load exposures
exposures = [cv2.imread(f) for f in files]
times = np.array([1/30, 1/15, 1/8, 1/4], dtype=np.float32)

# Merge to HDR
merge = cv2.createMergeDebevec()
hdr = merge.process(exposures, times)

# Tone mapping
tonemap = cv2.createTonemap(gamma=2.2)
ldr = tonemap.process(hdr)
```

### 8.2 Denoising

```python
# Non-local means
dst = cv2.fastNlMeansDenoisingColored(src, None, 10, 10, 7, 21)

# Bilateral filter
dst = cv2.bilateralFilter(src, 9, 75, 75)
```

### 8.3 Exposure Fusion

```python
merge_mertens = cv2.createMergeMertens()
fusion = merge_mertens.process(exposures)
```

---

## 9. RINGKASAN

Computational Photography telah mengubah paradigma fotografi digital:

| Teknik | Input | Output | Kegunaan |
|--------|-------|--------|----------|
| HDR | Multi-exposure | Extended DR | Scenes dengan contrast tinggi |
| Denoising | Noisy image | Clean image | Low-light photography |
| Focus Manipulation | Image + Depth | Synthetic bokeh | Portrait mode |
| Super Resolution | Low-res | High-res | Detail enhancement |
| Exposure Fusion | Multi-exposure | LDR | Simpler HDR alternative |

### Key Takeaways:
1. Computational photography extends camera capabilities through software
2. Multi-frame techniques leverage temporal information
3. AI/ML increasingly important untuk complex tasks
4. Trade-offs antara quality, computation, dan real-time requirements

---

## 10. REFERENSI PEMBELAJARAN

### Textbooks:
1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Edition. Chapter 10.
2. Reinhard et al. (2010). High Dynamic Range Imaging. Morgan Kaufmann.
3. Raskar, R. & Tumblin, J. (2009). Computational Photography.

### Online Resources:
- Google Research Blog - Computational Photography
- Stanford CS 448A: Computational Photography
- MIT Media Lab - Camera Culture Group
