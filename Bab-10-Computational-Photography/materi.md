# Bab 10: Computational Photography

## 📋 Daftar Isi
1. [Pendahuluan](#1-pendahuluan)
2. [High Dynamic Range (HDR) Imaging](#2-high-dynamic-range-hdr-imaging)
3. [Image Denoising](#3-image-denoising)
4. [Image Deblurring](#4-image-deblurring)
5. [Super Resolution](#5-super-resolution)
6. [Image Inpainting](#6-image-inpainting)
7. [Computational Lighting](#7-computational-lighting)

---

## 1. Pendahuluan

### 1.1 Apa itu Computational Photography?

**Computational Photography** adalah bidang yang menggunakan teknik komputasi untuk meningkatkan atau memperluas kemampuan fotografi digital, melampaui batasan optik dan sensor tradisional.

### 1.2 Motivasi

Kamera tradisional memiliki keterbatasan:
- **Dynamic range** terbatas
- **Noise** pada low light
- **Blur** dari motion atau defocus
- **Resolusi** terbatas oleh sensor
- **Field of view** terbatas

### 1.3 Aplikasi

| Aplikasi | Deskripsi |
|----------|-----------|
| **HDR Imaging** | Capture scene dengan dynamic range tinggi |
| **Night Mode** | Foto low-light tanpa noise |
| **Portrait Mode** | Blur background (bokeh) |
| **Panorama** | Wide field of view |
| **Super Resolution** | Meningkatkan resolusi |
| **Burst Photography** | Combine multiple shots |
| **Computational Flash** | Enhance lighting |

---

## 2. High Dynamic Range (HDR) Imaging

### 2.1 Dynamic Range

**Dynamic Range** adalah rasio antara nilai maximum dan minimum yang dapat direpresentasikan.

- **Real-world scenes**: Dapat melebihi $10^6:1$
- **Standard camera**: Sekitar $1000:1$ (10 stops)
- **Display**: Sekitar $100:1$ hingga $1000:1$

### 2.2 Capturing HDR

**Multiple Exposure Fusion**:

1. Capture multiple images dengan exposure berbeda
2. Merge menjadi HDR image

**Exposure bracketing**:
- Under-exposed: Capture highlights
- Normal: Mid-tones
- Over-exposed: Capture shadows

### 2.3 Camera Response Function

Hubungan antara irradiance $E$ dan pixel value $Z$:

$$Z = f(E \cdot t)$$

Di mana:
- $f$: Camera response function (CRF)
- $E$: Irradiance
- $t$: Exposure time

**Recovering CRF (Debevec & Malik)**:

$$g(Z_{ij}) = \ln E_i + \ln t_j$$

Di mana $g = \ln f^{-1}$

**Objective function**:
$$\min_g \sum_{i,j} w(Z_{ij})[g(Z_{ij}) - \ln E_i - \ln t_j]^2 + \lambda \sum_z [g''(z)]^2$$

### 2.4 HDR Merging

Setelah recover $E$ untuk setiap pixel:

$$\ln E_i = \frac{\sum_j w(Z_{ij})(g(Z_{ij}) - \ln t_j)}{\sum_j w(Z_{ij})}$$

**Weighting function** $w(z)$:
- Avoid saturated pixels: $w(0) = w(255) = 0$
- Prefer mid-range: $w(z) = z - z_{min}$ untuk $z < 128$, dst.

### 2.5 Tone Mapping

HDR image harus di-**tone map** untuk display.

**Global operators**:

$$L_d = \frac{L(x,y)}{1 + L(x,y)}$$

**Reinhard operator**:
$$L_d = \frac{L}{1 + L} \cdot \frac{1 + L/L_{white}^2}{1}$$

**Local operators**:
- Bilateral filtering
- Gradient domain methods

**Exposure Fusion (Mertens)**:
Langsung merge LDR images tanpa create HDR:
$$R = \sum_k W_k \cdot I_k$$

Weight berdasarkan:
- Contrast
- Saturation
- Well-exposedness

---

## 3. Image Denoising

### 3.1 Noise Models

**Additive Gaussian Noise**:
$$I_{noisy} = I_{clean} + n, \quad n \sim \mathcal{N}(0, \sigma^2)$$

**Poisson Noise** (photon noise):
$$I_{noisy} \sim \text{Poisson}(I_{clean})$$

**Salt and Pepper Noise**:
Random pixels menjadi 0 atau 255.

### 3.2 Classical Methods

**Gaussian Filtering**:
$$I_{denoised} = G_\sigma * I_{noisy}$$

- Simple tapi blur edges

**Median Filtering**:
$$I_{denoised}(x) = \text{median}(\{I(y) : y \in N(x)\})$$

- Good untuk salt-and-pepper
- Preserves edges better

**Bilateral Filtering**:
$$I_{denoised}(x) = \frac{1}{W} \sum_{y \in N(x)} G_s(\|x-y\|) \cdot G_r(|I(x)-I(y)|) \cdot I(y)$$

- Combines spatial dan range filtering
- Edge-preserving

### 3.3 Non-Local Means (NLM)

**Key idea**: Pixels dengan similar neighborhood harus memiliki nilai similar.

$$I_{denoised}(x) = \sum_y w(x,y) \cdot I(y)$$

Weight:
$$w(x,y) = \frac{1}{Z(x)} \exp\left(-\frac{\|P(x) - P(y)\|^2}{h^2}\right)$$

Di mana $P(x)$ adalah patch di sekitar $x$.

**Keuntungan**:
- Non-local similarity
- Better texture preservation

### 3.4 BM3D (Block Matching 3D)

**State-of-the-art** traditional denoising:

1. **Block matching**: Find similar patches
2. **3D transform**: Stack patches, apply 3D transform
3. **Collaborative filtering**: Shrink coefficients
4. **Aggregation**: Return patches, aggregate

### 3.5 Deep Learning Denoising

**DnCNN**:
- Residual learning: Learn noise, bukan clean image
- Batch normalization

**FFDNet**:
- Fast dan flexible
- Non-blind denoising dengan sigma input

**Noise2Noise**:
- Train tanpa clean images!
- Learn from pairs of noisy images

---

## 4. Image Deblurring

### 4.1 Blur Models

**Motion Blur**:
$$I_{blur} = k * I_{sharp}$$

Di mana $k$ adalah blur kernel (PSF).

**Defocus Blur**:
Circular atau disk-shaped kernel.

### 4.2 Non-Blind Deconvolution

Jika kernel $k$ diketahui:

**Inverse filtering**:
$$\hat{I} = \mathcal{F}^{-1}\left(\frac{\mathcal{F}(I_{blur})}{\mathcal{F}(k)}\right)$$

Masalah: Amplify noise di frequencies di mana $\mathcal{F}(k)$ kecil.

**Wiener Filter**:
$$\hat{I} = \mathcal{F}^{-1}\left(\frac{\mathcal{F}(k)^* \cdot \mathcal{F}(I_{blur})}{|\mathcal{F}(k)|^2 + \text{NSR}}\right)$$

**Richardson-Lucy**:
Iterative algorithm untuk Poisson noise:
$$\hat{I}^{n+1} = \hat{I}^n \cdot \left(k^T * \frac{I_{blur}}{k * \hat{I}^n}\right)$$

### 4.3 Blind Deconvolution

Kernel $k$ tidak diketahui - estimate both $I$ dan $k$.

**MAP formulation**:
$$\min_{I,k} \|k * I - I_{blur}\|^2 + \lambda_I R(I) + \lambda_k R(k)$$

**Regularizers**:
- Total Variation: $R(I) = \|\nabla I\|_1$
- Sparse gradient prior
- L0 gradient sparsity

**Alternating optimization**:
```
1. Fix k, solve for I
2. Fix I, solve for k
3. Repeat
```

### 4.4 Deep Learning Deblurring

**DeblurGAN**:
- GAN-based deblurring
- Perceptual loss

**SRN-DeblurNet**:
- Scale-recurrent network
- Coarse-to-fine

**MIMO-UNet**:
- Multi-input multi-output
- State-of-the-art

---

## 5. Super Resolution

### 5.1 Problem Definition

Given low-resolution (LR) image, reconstruct high-resolution (HR) image.

**Degradation model**:
$$I_{LR} = (I_{HR} * k) \downarrow_s + n$$

Di mana:
- $k$: Blur kernel
- $\downarrow_s$: Downsampling factor $s$
- $n$: Noise

### 5.2 Classical Methods

**Interpolation**:
- Nearest neighbor
- Bilinear
- Bicubic
- Lanczos

**Example-based SR**:
- Learn mapping dari LR ke HR patches
- Sparse coding

### 5.3 Deep Learning SR

**SRCNN (2014)**:
- First CNN for SR
- 3 layers: extraction, mapping, reconstruction

**VDSR**:
- Very deep (20 layers)
- Residual learning
- Multiple scales

**EDSR**:
- Enhanced deep SR
- Remove batch norm
- Larger model

**RCAN**:
- Residual channel attention
- State-of-the-art for a while

**SwinIR**:
- Transformer-based
- Current state-of-the-art

### 5.4 GAN-Based SR

**SRGAN**:
$$L = L_{content} + \lambda L_{adversarial}$$

**Content loss**:
- Perceptual loss (VGG features)
- Pixel loss

**ESRGAN**:
- Enhanced SRGAN
- RRDB blocks
- Relativistic discriminator

**Real-ESRGAN**:
- Handle real-world degradations
- Practical super resolution

### 5.5 Multiple Image SR

Combine multiple LR images:

1. **Align** images dengan sub-pixel accuracy
2. **Fuse** information dari multiple frames
3. **Reconstruct** HR image

---

## 6. Image Inpainting

### 6.1 Problem Definition

Fill missing regions dalam image secara natural.

**Applications**:
- Object removal
- Photo restoration
- Image completion

### 6.2 Classical Methods

**Diffusion-based**:
Propagate information dari boundary ke dalam:
$$\frac{\partial I}{\partial t} = \nabla \cdot (c \nabla I)$$

**Patch-based (PatchMatch)**:
1. Find similar patches di known region
2. Copy ke unknown region
3. Iterate

**Criminisi Algorithm**:
Priority-based patch filling:
$$P(p) = C(p) \cdot D(p)$$

Di mana:
- $C(p)$: Confidence term
- $D(p)$: Data term (edge strength)

### 6.3 Deep Learning Inpainting

**Context Encoders**:
- Encoder-decoder dengan adversarial training
- Learn semantic understanding

**Partial Convolutions**:
- Konvolusi hanya pada valid pixels
- Progressively update mask

**Gated Convolutions**:
- Learn soft gating mechanism
- Better edge handling

**LaMa (Large Mask Inpainting)**:
- Fast Fourier Convolutions
- Handle large masks

### 6.4 Diffusion Models

**Stable Diffusion Inpainting**:
- State-of-the-art quality
- Semantic understanding
- Text-guided inpainting

---

## 7. Computational Lighting

### 7.1 Flash/No-Flash Photography

Combine:
- **Flash image**: Low noise, harsh lighting
- **No-flash image**: Natural lighting, noisy

**Joint bilateral filtering**:
Use flash image untuk guide denoising no-flash image.

### 7.2 Relighting

Change lighting setelah capture.

**Image-based relighting**:
Capture dengan berbagai lighting conditions, interpolate.

**Single image relighting**:
- Estimate lighting
- Re-render dengan new lighting

### 7.3 Intrinsic Images

Decompose image menjadi:
$$I = R \cdot S$$

Di mana:
- $R$: Reflectance (albedo)
- $S$: Shading

**Applications**:
- Relighting
- Material editing
- Shadow removal

### 7.4 Depth-Based Effects

**Synthetic Depth of Field**:
1. Estimate depth
2. Apply depth-dependent blur

**Portrait Mode**:
- Segment person
- Blur background
- Blend seamlessly

---

## 📊 Comparison of Methods

### Denoising

| Method | Type | Quality | Speed |
|--------|------|---------|-------|
| Gaussian | Filter | Low | Fast |
| Bilateral | Filter | Medium | Medium |
| NLM | Patch | High | Slow |
| BM3D | Patch | Very High | Slow |
| DnCNN | Deep | High | Fast |
| Restormer | Deep | Very High | Medium |

### Super Resolution

| Method | Scale | PSNR | Visual |
|--------|-------|------|--------|
| Bicubic | Any | Baseline | Blurry |
| SRCNN | 2-4x | +1 dB | Better |
| EDSR | 2-4x | +2 dB | Good |
| ESRGAN | 4x | Lower | Best |

---

## 🔧 Best Practices

### HDR
1. Gunakan tripod untuk avoid ghosting
2. Bracket dengan 2-stop intervals
3. Deghost untuk moving objects

### Denoising
1. Match noise level ke algorithm
2. Preserve texture
3. Avoid over-smoothing

### Super Resolution
1. GAN untuk visual quality
2. PSNR methods untuk fidelity
3. Consider real-world degradations

---

## 📚 Referensi

1. Szeliski, R. - Computer Vision: Algorithms and Applications, Chapter 10
2. Debevec, P. & Malik, J. - "Recovering High Dynamic Range Radiance Maps" (1997)
3. Buades et al. - "A Non-Local Algorithm for Image Denoising" (2005)
4. Dong et al. - "Image Super-Resolution Using Deep CNNs" (2014)
5. Wang et al. - "ESRGAN: Enhanced Super-Resolution GANs" (2018)

---

*Materi ini adalah bagian dari Praktikum Computer Vision*
