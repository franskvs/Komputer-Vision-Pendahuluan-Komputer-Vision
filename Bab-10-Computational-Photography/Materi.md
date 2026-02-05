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

Computational photography telah menjadi fitur utama di smartphone dan kamera modern:

| Aplikasi | Teknologi | Platform | Contoh Penerapan |
|----------|-----------|----------|------------------|
| Night Mode | Multi-frame HDR + Denoising | iPhone, Pixel, Samsung | Foto malam tanpa flash, detail di area gelap |
| Portrait Mode | Depth estimation + Bokeh | Semua smartphone | Blur background seperti DSLR f/1.8 |
| Super Zoom | Super Resolution | Pixel, Xiaomi | Zoom 100x dengan AI enhancement |
| Astrophotography | Long exposure + Alignment | Pixel, iPhone 14+ | Foto bintang dengan handheld |
| ProRAW | Computational RAW | iPhone 12+ | RAW dengan HDR & Night Mode |
| HDR+ | Burst alignment + merging | Google Camera | Detail sempurna di highlight & shadow |
| Smart HDR | Auto-bracket + fusion | iPhone | Scene optimization otomatis |

**Contoh Kasus Nyata:**

1. **Google Night Sight**: Menggabungkan 15+ frame dengan exposure pendek, melakukan alignment, denoising, dan enhancement untuk menghasilkan foto low-light tanpa noise yang biasanya muncul di ISO tinggi.

2. **iPhone Deep Fusion**: Mengambil 9 gambar sebelum shutter ditekan, melakukan pixel-by-pixel analysis menggunakan Neural Engine untuk texture dan detail optimization.

3. **Samsung's Scene Optimizer**: Menggunakan AI untuk mendeteksi 30+ scene types (food, landscape, sunset, dll) dan otomatis menyesuaikan processing pipeline.

---

## 2. HIGH DYNAMIC RANGE (HDR) IMAGING

### 2.1 Dynamic Range Problem

**Dynamic Range** adalah rasio antara nilai terbesar dan terkecil yang dapat direpresentasikan. Kamera digital memiliki dynamic range terbatas (~10-12 stops), sementara scene nyata bisa mencapai >20 stops.

**Visual Analogi Dynamic Range:**
```
Human Eye: ~20 stops (1:1,000,000 ratio)
Camera Sensor: ~12 stops (1:4,096 ratio)  
Display Monitor: ~8-10 stops (1:1,000 ratio)

1 stop = 2x lebih terang/gelap
```

**Contoh Scene High Dynamic Range:**

1. **Interior dengan Jendela (Wedding Photography)**
   - Window view: 10,000 lux (sangat terang)
   - Indoor room: 100 lux (redup)
   - Ratio: 1:100,000
   - Solusi: HDR bracketing 5 exposures (-2, -1, 0, +1, +2 EV)

2. **Night Photography dengan Lampu Neon**
   - Neon sign: 50,000 cd/m²
   - Dark sky: 0.05 cd/m²
   - Ratio: 1:1,000,000
   - Solusi: Exposure fusion atau HDR dengan local tone mapping

3. **Landscape Sunset**
   - Direct sun: 100,000 lux
   - Shadowed foreground: 10 lux
   - Ratio: 1:10,000
   - Solusi: 3-exposure bracket atau graduated ND filter + single exposure

**Real-World Example:**
Fotografer real estate menggunakan HDR untuk menampilkan detail interior room sekaligus pemandangan luar jendela. Tanpa HDR, harus memilih: jendela putih blown-out atau ruangan terlalu gelap.

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

**Noise Sources** dalam Digital Photography:

1. **Photon Noise (Shot Noise)**: 
   - Poisson distribution, inherent dalam light
   - $\sigma_{shot}^2 = I$ (variance = signal intensity)
   - Dominant di well-lit scenes
   - **Contoh**: Foto siang hari ISO 100 masih ada subtle noise di sky

2. **Read Noise**: 
   - Electronic, Gaussian distribution
   - Dari sensor readout circuitry
   - Dominant di low-light (low signal)
   - **Contoh**: Banding/noise di shadow area pada ISO 6400

3. **Dark Current**: 
   - Temperature-dependent
   - Electrons generated tanpa photons
   - Worse di long exposures & high temperature
   - **Contoh**: Hot pixels pada astrophotography 30s exposure

4. **Quantization Noise**: 
   - A/D conversion rounding errors
   - Minimal di modern 14-bit+ sensors
   - Visible di heavy post-processing

**Combined Model**:
$$I_{observed} = I_{true} + n_{shot} + n_{read}$$

Di mana $n_{shot} \sim Poisson(I_{true})$ dan $n_{read} \sim \mathcal{N}(0, \sigma^2)$

**Praktis:**
- ISO 100: Read noise ≈ 2-3 e⁻, Shot noise dominan di bright areas
- ISO 6400: Read noise ≈ 10-20 e⁻, terlihat di semua area
- Long exposure (>10s): Dark current mulai berkontribusi

**Real-World Scenario:**
Wedding photographer di indoor reception (ISO 3200-6400) akan mengalami:
- Shadow areas: Read noise dominan → perlu aggressive NLM denoising
- Highlight areas: Shot noise minimal → bilateral filter cukup
- Skin tones: Perlu careful denoising untuk preserve texture

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

**Pipeline** yang digunakan di smartphone modern:

```
Input Image → Depth Estimation → Segmentation → Blur Kernel → Selective Blur → Edge Refinement → Output
```

#### Depth Estimation Methods:

1. **Dual-Camera Stereo** (iPhone 7+, Pixel 2+)
   - Menggunakan disparitas dari dua kamera dengan baseline berbeda
   - Parallax calculation: $depth = \frac{f \cdot baseline}{disparity}$
   - **Advantage**: Accurate depth, works di berbagai kondisi
   - **Limitation**: Minimum focus distance ~30cm
   - **Contoh**: iPhone 13 Pro dengan 3x tele + wide camera

2. **Phase-Detection Autofocus (PDAF)** (Samsung, Pixel)
   - Dual-pixel sensor memberikan phase information
   - Setiap pixel terpisah jadi 2 sub-pixels
   - **Advantage**: Dense depth map, single camera
   - **Limitation**: Lower accuracy dibanding stereo
   - **Contoh**: Samsung Galaxy S23 Dual Pixel sensor

3. **Neural Network Monocular Estimation** (All modern phones)
   - Deep learning untuk predict depth dari single image
   - Trained pada millions of image-depth pairs
   - **Advantage**: Works dengan single camera, fallback method
   - **Limitation**: Dapat salah pada unusual scenes
   - **Contoh**: Google Portrait Light menggunakan ML depth

4. **LiDAR Sensor** (iPhone 12 Pro+, iPad Pro)
   - Direct time-of-flight measurement
   - Accuracy sampai millimeter
   - **Advantage**: Extreme accuracy, works di dark
   - **Limitation**: Expensive, limited range
   - **Contoh**: iPhone 15 Pro untuk AR dan Night Mode Portrait

#### Blur Application - Circle of Confusion:

**Circle of Confusion (CoC)** Formula:
$$CoC = \frac{A \cdot f \cdot |D - D_f|}{D \cdot (D_f - f)}$$

Di mana:
- $A$ = aperture diameter (mm)
- $f$ = focal length (mm)
- $D$ = object distance (mm)
- $D_f$ = focus distance (mm)

**Practical Example - iPhone Portrait Mode Simulation:**
```
Simulating f/1.4 lens:
- Subject at 1m (focus point)
- Background at 3m
- Equivalent focal length: 26mm (wide), 52mm (tele)

CoC_background = 26mm × 18mm × |3000-1000| / (3000 × 979) ≈ 0.3mm
→ Translate ke blur radius: ~12 pixels di 4032×3024 image
```

**Real-World Application:**
- **Instagram/TikTok Portrait**: Lebih aggressive blur (bokeh radius 15-20px) untuk dramatic effect
- **Professional headshot**: Subtle blur (radius 5-10px) untuk natural look
- **Product photography**: Focus stacking untuk extended DoF, semua sharp

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

Meningkatkan resolusi dari satu gambar - fundamental problem dalam computer vision.

**Classical Methods**:
- **Bicubic interpolation**: Smooth tapi blurry, default di Photoshop
- **Lanczos resampling**: Sharper edges, ringing artifacts possible
- **Edge-directed interpolation**: Preserve edges tapi lambat

**Learning-Based Methods**:

1. **SRCNN (2014)** - Super-Resolution Convolutional Neural Network
   - First CNN-based approach
   - 3-layer network: patch extraction, mapping, reconstruction
   - **Usage**: Research baseline

2. **EDSR (2017)** - Enhanced Deep SR
   - Remove batch normalization untuk better performance
   - Residual learning dengan deep network (32+ layers)
   - **Usage**: Waifu2x anime upscaling

3. **ESRGAN (2018)** - Enhanced SRGAN
   - GAN-based perceptual quality focus
   - Realistic textures, bukan hanya PSNR
   - **Usage**: Topaz Gigapixel AI, DVDFab Enlarger AI
   
4. **Real-ESRGAN (2021)** - Real-world degradation
   - Trained on practical degradations (compression, blur, noise)
   - Works pada low-quality images dari internet
   - **Usage**: Video upscaling (Topaz Video AI)

**Real-World Applications:**

1. **Google Pixel Super Res Zoom**:
   - Burst capture saat zooming (>3x)
   - Multi-frame alignment untuk sub-pixel detail
   - ML enhancement untuk texture
   - Result: 8x zoom terlihat seperti optical 3x

2. **Samsung Galaxy Space Zoom (100x)**:
   - Optical 10x dari periscope lens
   - Digital 10x dengan AI SR
   - Noise reduction dan stabilization
   - Result: Readable text dari 100m+ distance

3. **Adobe Super Resolution**:
   - Enhanced Details di Camera Raw/Lightroom
   - 2x upscale dengan AI texture preservation
   - **Use case**: Crop aggressively dari RAW file

4. **Netflix/YouTube AI Upscaling**:
   - Upscale 1080p content ke 4K untuk modern TVs
   - Real-time on-device processing
   - Preserve film grain dan avoid over-smoothing

### 5.2 Multi-Frame Super Resolution

Menggabungkan informasi dari multiple frames dengan sub-pixel shifts - teknik yang sangat powerful!

**Key Concept**: 
Jika kamera bergerak sedikit antar frames, setiap frame capture scene dari slightly different sub-pixel position. Combine = higher resolution!

**Requirements**:
1. Sub-pixel displacement antar frames (0.3-0.7 pixel ideal)
2. Accurate registration (alignment error < 0.1 pixel)
3. Non-redundant information (frames harus berbeda)

**Algorithm**:
1. Capture burst of images (8-15 frames)
2. Estimate sub-pixel motion dengan optical flow
3. Combine observations dalam high-res grid
4. Regularization untuk handle ill-posed problem
5. Denoising dan sharpening

**Practical Example - Google Pixel Night Sight:**
```
Input: 15 frames @ 12MP, handheld motion
Process:
  - Frame alignment dengan optical flow
  - Reject blurry/shaky frames (keep 8-12)
  - Multi-frame SR: effective 18-20MP detail
  - Merge untuk noise reduction
  - Local tone mapping
Output: Sharp, low-noise 12MP image
```

**Mathematical Model**:
$$y_k = D \cdot B \cdot M_k \cdot x + n_k$$

Di mana:
- $x$ = high-res image (target, unknown)
- $M_k$ = motion/warp model untuk frame $k$
- $B$ = blur kernel (optical PSF)
- $D$ = downsampling operator
- $n_k$ = noise (sensor + quantization)

**Commercial Implementations:**

1. **Hasselblad Multi-Shot** (High-end medium format):
   - 4-shot atau 6-shot mode
   - Sensor shift dengan piezo actuator
   - 400MP output dari 100MP sensor
   - **Use**: Product photography, art reproduction

2. **Sony Pixel Shift Multi Shooting**:
   - 16 frames dengan 1-pixel sensor shifts
   - Combine ke 4× pixel count
   - Perfect color accuracy (no Bayer interpolation)
   - **Use**: Landscape, architecture, studio

3. **Olympus High-Res Shot**:
   - 8 frames dengan 0.5-pixel shifts
   - Handheld mode dengan stabilization
   - 80MP dari 20MP sensor
   - **Use**: Handheld landscape photography

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

Computational Photography telah mengubah paradigma fotografi digital dengan membawa capabilities yang sebelumnya hanya mungkin dengan equipment profesional ke smartphone dan consumer cameras.

### 9.1 Tabel Ringkasan Teknik

| Teknik | Input | Output | Kegunaan | Contoh Real-World |
|--------|-------|--------|----------|-------------------|
| HDR | Multi-exposure (3-7 images) | Extended DR | Scenes dengan contrast tinggi | Real estate interior, landscape sunset |
| Denoising | Noisy image | Clean image | Low-light photography | Concert photography, night street |
| Focus Manipulation | Image + Depth | Synthetic bokeh | Portrait mode | Instagram portraits, product photos |
| Super Resolution | Low-res | High-res (2-4x) | Detail enhancement | Zoom enhancement, old photo restoration |
| Exposure Fusion | Multi-exposure | LDR | Simpler HDR alternative | Architecture photography |
| Multi-frame | Burst (8-15 frames) | Enhanced single | Night mode, denoise | Google Night Sight, iPhone Night Mode |

### 9.2 Computational Photography Workflows

**Workflow 1: Professional Real Estate Photography**
```
Capture:
  → 5-bracket HDR (-2, -1, 0, +1, +2 EV)
  → Tripod mounted untuk alignment
  
Processing:
  → Merge dengan Debevec/Robertson
  → Tone map dengan Reinhard Local (preserve detail)
  → CLAHE untuk shadow enhancement
  → Lens correction & perspective adjustment
  → Selective color enhancement
  
Output: Interior dengan window view perfectly exposed
```

**Workflow 2: Smartphone Night Photography**
```
Capture (otomatis oleh phone):
  → Burst 8-15 frames, short exposure (1/15s - 1/4s)
  → OIS/EIS untuk stabilization
  
Processing Pipeline:
  1. Frame alignment (optical flow)
  2. Frame selection (reject blur/shake)
  3. Multi-frame SR (combine sub-pixel shifts)
  4. Multi-frame averaging (noise reduction)
  5. ML-based denoising (preserve details)
  6. Shadow/highlight optimization
  7. Color grading (warm tone untuk night)
  
Output: Low-noise, sharp night photo
Time: 2-3 seconds total
```

**Workflow 3: Portrait Photography Enhancement**
```
Capture:
  → Single frame atau 3-frame burst
  → Depth data (stereo/LiDAR/ML)
  
Processing:
  1. Face detection & skin segmentation
  2. Depth estimation & refinement
  3. Subject isolation (alpha matting)
  4. Background blur (depth-dependent)
  5. Skin smoothing (preserve texture)
  6. Eye enhancement (catchlight, color)
  7. Edge refinement (hair, face boundary)
  
Output: Professional portrait dengan bokeh
```

### 9.3 Key Takeaways:

1. **Computational photography extends camera capabilities through software**
   - Dynamic range expansion beyond sensor limits
   - Resolution enhancement beyond pixel count
   - Depth of field control in post-processing

2. **Multi-frame techniques leverage temporal information**
   - Noise reduction: SNR improves by √N with N frames
   - Super resolution: Sub-pixel shifts add real detail
   - HDR: Different exposures capture full tonal range

3. **AI/ML increasingly important untuk complex tasks**
   - Depth estimation dari single camera
   - Semantic segmentation (sky, people, etc)
   - Scene detection & auto-optimization
   - Realistic texture generation (super resolution)

4. **Trade-offs antara quality, computation, dan real-time**
   - Mobile: Must process dalam 2-3 detik
   - Desktop: Can use heavy algorithms (minutes)
   - Cloud: Unlimited processing tapi latency issue

5. **Future Directions**
   - Real-time video computational photography
   - Light field cameras for post-capture refocus
   - Computational zoom (>100x usable)
   - AI-generated fill untuk extreme crops
   - HDR video with real-time tone mapping

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
