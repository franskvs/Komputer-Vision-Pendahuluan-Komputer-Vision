# Bab 14: Image-Based Rendering

## 1. Pendahuluan

### 1.1 Definisi
**Image-Based Rendering (IBR)** adalah teknik untuk mensintesis tampilan baru (novel views) dari sebuah scene menggunakan kumpulan gambar referensi, tanpa memerlukan rekonstruksi geometri 3D eksplisit yang lengkap.

### 1.2 Motivasi
- **Photorealism**: Gambar nyata memberikan kualitas visual tertinggi
- **Efisiensi**: Tidak perlu memodelkan geometri kompleks secara detail
- **Scalability**: Menangani scene besar dengan kompleksitas visual tinggi
- **Real-time**: Rendering cepat dibanding ray tracing tradisional

### 1.3 Spektrum IBR
```
Pure Image-Based ←――――――――――――――――→ Pure Geometry-Based
    |                                      |
Light Fields                        3D Model + Textures
Panoramas                           Mesh Rendering
Image Morphing                      Ray Tracing
```

## 2. Light Fields

### 2.1 Konsep Dasar
**Light Field** merepresentasikan cahaya yang melewati setiap titik dalam ruang dari setiap arah.

**Plenoptic Function** (7D):
$$L = P(x, y, z, \theta, \phi, \lambda, t)$$

Dimana:
- $(x, y, z)$ = posisi dalam ruang
- $(\theta, \phi)$ = arah pandang
- $\lambda$ = panjang gelombang (warna)
- $t$ = waktu

**Simplifikasi 4D Light Field**:
$$L(u, v, s, t)$$

Menggunakan dua bidang paralel:
- $(u, v)$ = posisi pada camera plane
- $(s, t)$ = posisi pada focal plane

### 2.2 Light Field Capture

**Camera Array**:
```
[C] [C] [C] [C] [C]
[C] [C] [C] [C] [C]
[C] [C] [C] [C] [C]
[C] [C] [C] [C] [C]
```

**Lytro Camera** (Plenoptic Camera):
- Microlens array di depan sensor
- Capture angular information dalam single shot

### 2.3 Light Field Rendering
```
Input: Light field L(u,v,s,t)
Target view: Virtual camera position (u', v')

For each pixel (s, t) in output:
    1. Sample L at (u', v', s, t)
    2. Interpolate if needed
    3. Output pixel value
```

**Interpolasi**:
- Bilinear interpolation untuk posisi non-integer
- Depth-corrected interpolation untuk parallax

### 2.4 Depth from Light Field
Dengan mencari korespondensi sepanjang epipolar lines:
$$\text{depth}(s, t) = \text{argmax}_d \sum_{(u,v)} \text{sim}(L(u, v, s+du, t+dv))$$

## 3. Panoramic Imaging

### 3.1 Panorama Stitching

**Pipeline**:
```
Images → Feature Detection → Matching → 
Homography → Warping → Blending → Panorama
```

**Bundle Adjustment** untuk optimasi global:
$$\min_{\{H_i\}} \sum_{i,j} \sum_k ||H_j x_{ij}^k - H_i x_{ji}^k||^2$$

### 3.2 Cylindrical dan Spherical Projection

**Cylindrical**:
$$x' = f \cdot \tan^{-1}\left(\frac{x}{f}\right)$$
$$y' = f \cdot \frac{y}{\sqrt{x^2 + f^2}}$$

**Spherical**:
$$\theta = \tan^{-1}\left(\frac{x}{f}\right)$$
$$\phi = \tan^{-1}\left(\frac{y}{\sqrt{x^2 + f^2}}\right)$$

### 3.3 360° Video
- Equirectangular projection untuk storage
- Reprojection ke view direction saat playback

## 4. View Morphing

### 4.1 Image Morphing
Transisi antara dua gambar:
$$I(t) = (1-t) \cdot W(I_0, f_t) + t \cdot W(I_1, f_t)$$

Dimana:
- $W$ = warping function
- $f_t$ = intermediate feature positions

### 4.2 View Morphing dengan Geometry
```
1. Rectify images ke parallel views
2. Find correspondences
3. Interpolate disparity
4. Morph dengan consistency
5. Unrectify ke target view
```

**Keuntungan**: Preservasi struktur 3D

### 4.3 Feature-Based Morphing
- Beizer Curves untuk feature correspondences
- Delaunay triangulation untuk warping

## 5. Image-Based Modeling

### 5.1 View-Dependent Texture Mapping
Memilih tekstur berdasarkan viewing angle:
$$T(x, n, v) = \sum_i w_i(n, v) T_i(x)$$

Dimana:
- $w_i$ = weight berdasarkan angle
- $T_i$ = texture dari view $i$

### 5.2 Unstructured Lumigraph
Kombinasi geometry proxy + image blending:
```
1. Approximate geometry (visual hull/space carving)
2. Project images onto geometry
3. Blend dengan view-dependent weights
```

### 5.3 Surface Light Fields
Menyimpan radiance per surface point:
$$L(u, v, \theta, \phi)$$

Parameterisasi pada surface (u, v) + direction (θ, φ)

## 6. Layered Representations

### 6.1 Sprite dengan Depth
**Layered Depth Images (LDI)**:
- Multiple depth values per pixel
- Handle occlusions

```
Pixel (x, y):
  Layer 1: (color, depth, normal)
  Layer 2: (color, depth, normal)
  ...
```

### 6.2 Multi-Plane Images (MPI)
Representasi scene sebagai set of alpha-blended planes:
$$I(x, y) = \sum_d \alpha_d(x, y) \cdot C_d(x, y) \cdot \prod_{d' < d}(1 - \alpha_{d'}(x, y))$$

**Keuntungan**:
- Efficient novel view synthesis
- Handles semi-transparency
- GPU-friendly

### 6.3 3D Photo Inpainting
```
1. Estimate depth from single image
2. Create layered representation
3. Inpaint disoccluded regions
4. Render novel views
```

## 7. Neural Radiance Fields (NeRF)

### 7.1 Representasi
NeRF mempelajari fungsi kontinu:
$$F_\Theta: (x, y, z, \theta, \phi) \rightarrow (r, g, b, \sigma)$$

Dimana:
- $(x, y, z)$ = posisi 3D
- $(\theta, \phi)$ = viewing direction
- $(r, g, b)$ = color
- $\sigma$ = density

### 7.2 Volume Rendering
$$C(r) = \int_{t_n}^{t_f} T(t) \cdot \sigma(r(t)) \cdot c(r(t), d) \, dt$$

Dimana:
$$T(t) = \exp\left(-\int_{t_n}^{t} \sigma(r(s)) \, ds\right)$$

**Diskretisasi**:
$$\hat{C}(r) = \sum_{i=1}^{N} T_i \cdot (1 - \exp(-\sigma_i \delta_i)) \cdot c_i$$

### 7.3 Positional Encoding
Untuk menangkap high-frequency details:
$$\gamma(p) = (\sin(2^0 \pi p), \cos(2^0 \pi p), ..., \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p))$$

### 7.4 Training
```
Loss = ||C_rendered - C_ground_truth||^2

Untuk setiap training iteration:
1. Sample batch of rays dari training images
2. Sample points along each ray
3. Query MLP untuk color dan density
4. Volume render
5. Compute loss dan backpropagate
```

### 7.5 NeRF Variants
| Variant | Improvement |
|---------|-------------|
| Instant-NGP | Hash encoding, real-time |
| Mip-NeRF | Anti-aliasing, scale-aware |
| NeRF-W | Handle transient objects |
| NeRF-- | Without known camera poses |
| Plenoxels | Voxel-based, faster training |

## 8. 3D Gaussian Splatting

### 8.1 Representasi
Scene direpresentasikan sebagai set of 3D Gaussians:
$$G_i = \{\mu_i, \Sigma_i, c_i, \alpha_i\}$$

Dimana:
- $\mu$ = center position
- $\Sigma$ = 3D covariance (shape)
- $c$ = color (spherical harmonics)
- $\alpha$ = opacity

### 8.2 Splatting
Project 3D Gaussian ke 2D:
$$\Sigma_{2D} = J W \Sigma W^T J^T$$

Dimana $J$ = Jacobian dari projective transformation

### 8.3 Rendering
Alpha-blending dari depan ke belakang:
$$C = \sum_{i \in N} c_i \alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

**Keuntungan**:
- Real-time (>100 FPS)
- Explicit representation
- Easy to edit

## 9. View Interpolation

### 9.1 Dense Correspondence
Untuk interpolasi akurat diperlukan:
- Optical flow
- Disparity maps
- Scene flow

### 9.2 Forward vs Backward Warping

**Forward Warping**:
$$I_{target}(W(x)) = I_{source}(x)$$
- Problem: holes dan multiple mappings

**Backward Warping**:
$$I_{target}(x) = I_{source}(W^{-1}(x))$$
- Problem: memerlukan inverse warp

### 9.3 Splatting dan Pulling
```
Splatting:
  Distribute source pixels ke target (with kernel)
  
Pulling:
  Accumulate contributions
  Normalize by total weight
```

### 9.4 Depth-Image-Based Rendering (DIBR)
```
1. Warp depth image ke virtual view
2. Handle occlusions/disocclusions
3. Inpaint holes
4. Warp texture image
```

## 10. Real-Time IBR

### 10.1 GPU-Based Rendering
- Texture atlases untuk efficient access
- Projective texturing
- View-dependent shading dalam shader

### 10.2 Level-of-Detail
```
if (distance < near)
    render high-resolution proxy + IBR
else if (distance < far)
    render simplified + blended images
else
    render impostors / billboards
```

### 10.3 Streaming
- Progressive transmission
- View-dependent streaming
- Cache management

## 11. Aplikasi

### 11.1 Virtual Tourism
- Google Street View
- Museum virtual tours
- Real estate visualization

### 11.2 Telepresence
- Volumetric video
- Free-viewpoint video
- Holographic displays

### 11.3 Visual Effects
- Virtual production (The Mandalorian)
- Background replacement
- Digital doubles

### 11.4 AR/VR
- Environment mapping
- Passthrough rendering
- Mixed reality

## 12. Evaluasi

### 12.1 Metrik Kualitas
| Metrik | Deskripsi |
|--------|-----------|
| PSNR | Peak Signal-to-Noise Ratio |
| SSIM | Structural Similarity |
| LPIPS | Learned Perceptual Image Patch Similarity |
| FID | Fréchet Inception Distance |

### 12.2 Perceptual Studies
- User preference tests
- A/B comparisons
- Mean Opinion Score (MOS)

## 13. Ringkasan

### Metode IBR dan Trade-offs:

| Metode | Geometry | Novel Views | Quality | Speed |
|--------|----------|-------------|---------|-------|
| Light Field | None | Limited | High | Fast |
| Panorama | None | Rotation only | High | Fast |
| View Morphing | Implicit | Along baseline | Medium | Medium |
| LDI/MPI | Implicit | Limited range | High | Fast |
| NeRF | Implicit (MLP) | 360° | Very High | Slow |
| 3D Gaussians | Explicit | 360° | Very High | Real-time |

### Key Insights:
1. **Geometry-Image tradeoff**: Lebih banyak geometry = lebih flexible views
2. **Quality vs Speed**: Neural methods high quality tapi lambat
3. **Capture complexity**: Light fields butuh banyak images
4. **Application specific**: Pilih metode sesuai use case

## 14. Tugas Video (7-10 Menit)

### Topik yang Harus Dibahas:
1. **Konsep IBR** - Motivasi dan spektrum metode (1 menit)
2. **Light Fields** - Plenoptic function dan rendering (1.5 menit)
3. **Panorama** - Stitching dan projection (1 menit)
4. **Neural Methods** - NeRF dan 3D Gaussian Splatting (2 menit)
5. **View Interpolation** - Forward/backward warping (1 menit)
6. **Demo Praktis** - Panorama stitching atau view synthesis (1.5 menit)

### Kriteria Penilaian:
- Kedalaman penjelasan konsep
- Visualisasi dan diagram
- Demonstrasi praktis
- Kualitas presentasi
