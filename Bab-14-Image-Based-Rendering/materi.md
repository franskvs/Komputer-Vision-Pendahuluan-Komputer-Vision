# Bab 14: Image-Based Rendering

## Pendahuluan

**Image-Based Rendering (IBR)** adalah teknik untuk menyintesis pandangan baru (novel views) dari scene menggunakan sekumpulan gambar referensi. Berbeda dengan rendering tradisional yang membutuhkan model geometri eksplisit, IBR langsung memanfaatkan informasi yang tersimpan dalam gambar.

IBR menjembatani gap antara:
- **Computer Graphics**: Rendering dari model 3D
- **Computer Vision**: Analisis dan rekonstruksi dari gambar

---

## 1. Konsep Dasar IBR

### 1.1 Plenoptic Function

**Plenoptic function** mendeskripsikan semua kemungkinan pandangan dari scene:

$$P(V_x, V_y, V_z, \theta, \phi, \lambda, t)$$

dimana:
- $(V_x, V_y, V_z)$ = posisi viewer
- $(\theta, \phi)$ = viewing direction
- $\lambda$ = wavelength (color)
- $t$ = time

**Simplifikasi:**
- Static scene: hilangkan $t$
- Fixed lighting: hilangkan beberapa dependencies
- Monochrome: hilangkan $\lambda$

### 1.2 Taxonomy of IBR

Berdasarkan jumlah geometri yang digunakan:

| Kategori | Geometri | Contoh |
|----------|----------|--------|
| No geometry | None | Light fields, Lumigraph |
| Implicit geometry | Correspondence | View morphing |
| Approximate geometry | Proxy | View-dependent texture |
| Accurate geometry | Full 3D | Traditional rendering |

### 1.3 Trade-offs

```
More Images ←――――――――――――――→ More Geometry
Light Field                    3D Rendering
(dense sampling)               (sparse images)

Pros:                         Pros:
- No geometry needed          - Few images needed
- Simple interpolation        - Accurate extrapolation

Cons:                         Cons:
- Many images required        - Need accurate geometry
- Storage intensive           - Complex acquisition
```

---

## 2. Light Fields dan Lumigraph

### 2.1 Light Field Representation

**4D Light Field** menyederhanakan plenoptic function untuk rays di free space:

$$L(u, v, s, t)$$

dimana:
- $(u, v)$ = koordinat pada plane UV
- $(s, t)$ = koordinat pada plane ST

**Two-plane parameterization:**
```
ST Plane (camera positions)
    ↑
    |    Ray
    |  ↗
    | /
    |/
――――+――――→
UV Plane (image coordinates)
```

### 2.2 Light Field Acquisition

**Camera Array:**
- Grid of cameras
- Capture simultan
- Contoh: Stanford Light Field Camera Array

**Gantry/Robot:**
- Single camera
- Systematic movement
- Higher quality, slower

**Lenslet Array:**
- Microlens array di depan sensor
- Single exposure
- Contoh: Lytro camera

### 2.3 Light Field Rendering

**View Synthesis:**
1. Tentukan virtual camera position
2. Untuk setiap pixel di virtual view:
   - Compute ray direction
   - Intersect dengan UV dan ST planes
   - Lookup atau interpolate di light field
3. Handle occlusions dan gaps

```python
def render_lightfield(lf_data, camera_pose, intrinsics):
    """
    Render view dari light field data.
    
    Args:
        lf_data: 4D array (u, v, s, t)
        camera_pose: Virtual camera pose
        intrinsics: Camera intrinsics
        
    Returns:
        Rendered image
    """
    image = np.zeros((height, width, 3))
    
    for y in range(height):
        for x in range(width):
            # Ray dari virtual camera
            ray = compute_ray(x, y, camera_pose, intrinsics)
            
            # Intersect dengan two planes
            uv = intersect_uv_plane(ray)
            st = intersect_st_plane(ray)
            
            # Interpolate di light field
            color = interpolate_4d(lf_data, uv, st)
            image[y, x] = color
    
    return image
```

### 2.4 Light Field Compression

**Challenges:**
- 4D data sangat besar
- Banyak redundancy antar views

**Approaches:**
- Disparity-based compression
- Neural compression (NeRF-like)
- Standard video codecs pada sub-aperture images

---

## 3. View Morphing dan Interpolation

### 3.1 View Interpolation

**Prinsip:** Generate intermediate views antara dua reference views.

**Linear interpolation (naif):**
$$I_{int}(x) = (1-t) I_1(x) + t I_2(x)$$

Problem: Ghosting/doubling tanpa correspondence.

### 3.2 View Morphing

**Beizer-Seitz View Morphing Algorithm:**

1. **Prewarping:** Transform images ke parallel configuration
2. **Morphing:** Interpolate features dan pixels
3. **Postwarping:** Transform ke target viewpoint

**Langkah Detail:**
```
I₁ →[H₁]→ I₁' (parallel)
                        → Morph → I_int' →[H_int]→ I_int
I₂ →[H₂]→ I₂' (parallel)
```

**Morphing dengan correspondence:**
$$I_{int}(x_{int}) = (1-t) I_1'(x_1') + t I_2'(x_2')$$

dimana $x_{int} = (1-t) x_1' + t x_2'$

### 3.3 Feature-Based Morphing

**Steps:**
1. Detect dan match features
2. Compute warp field (e.g., mesh-based atau TPS)
3. Warp kedua images ke intermediate position
4. Blend

```python
def view_morph(img1, img2, pts1, pts2, t):
    """
    Morph between two views.
    
    Args:
        img1, img2: Source images
        pts1, pts2: Corresponding points
        t: Interpolation factor (0-1)
        
    Returns:
        Morphed image
    """
    # Interpolate point positions
    pts_int = (1 - t) * pts1 + t * pts2
    
    # Compute warp fields
    warp1 = compute_warp(pts1, pts_int)
    warp2 = compute_warp(pts2, pts_int)
    
    # Warp images
    warped1 = warp_image(img1, warp1)
    warped2 = warp_image(img2, warp2)
    
    # Blend
    result = (1 - t) * warped1 + t * warped2
    
    return result
```

---

## 4. View-Dependent Texture Mapping

### 4.1 Konsep

Gunakan approximate geometry sebagai proxy, dengan texture yang bervariasi berdasarkan viewing direction.

**Keuntungan:**
- Geometri tidak perlu sempurna
- Menangkap view-dependent effects (specular, etc.)
- Lebih sedikit gambar dari light field

### 4.2 Unstructured Lumigraph

**Algorithm:**
1. Untuk setiap pixel di target view:
   - Tentukan surface point pada proxy geometry
   - Cari reference images yang "melihat" point tersebut
   - Weight dan blend berdasarkan:
     - Angular similarity dengan target view
     - Resolution/distance
     - Visibility
2. Render dengan weighted texture

**Blending weights:**
$$w_i = w_{angular}(i) \cdot w_{resolution}(i) \cdot w_{field}(i)$$

### 4.3 View-Dependent Geometry

**Billboards:**
- Simple planar proxy
- Orient menghadap camera
- Untuk distant objects

**Depth Layers:**
- Multiple depth planes
- Layer-based rendering
- Trade-off detail vs. complexity

**Mesh Proxy:**
- Approximate 3D mesh
- Better untuk close views
- View-dependent texturing

---

## 5. Image-Based Rendering dengan Depth

### 5.1 3D Warping

**Forward warping:**
```
Source Image + Depth → 3D Points → Project ke Target View
```

**Backward warping:**
```
For each pixel di target:
  - Compute 3D point (dari depth)
  - Project ke source
  - Sample source image
```

**Equations:**
$$x_{target} = K_{target} [R | t] K_{source}^{-1} d \cdot x_{source}$$

### 5.2 DIBR (Depth Image-Based Rendering)

**Pipeline:**
1. Input: RGB + Depth image(s)
2. Warp ke novel viewpoint
3. Handle:
   - Disocclusions (holes)
   - Cracks (dari forward warp)
4. Inpaint missing regions

**Hole filling strategies:**
- Background layer extrapolation
- Inpainting algorithms
- Neural completion

### 5.3 Multi-View DIBR

**Input:** Multiple RGB-D images dari berbagai sudut

**Process:**
1. Warp semua views ke target
2. Fuse berdasarkan:
   - Confidence/weight
   - Distance to surface
   - Viewing angle
3. Fill remaining holes

---

## 6. Neural View Synthesis

### 6.1 Deep Image-Based Rendering

**CNN-based View Synthesis:**
```
Input Views → Feature Extraction → View Fusion → Novel View Generation
```

**Multi-Plane Images (MPI):**
- Represent scene sebagai stack of RGBA planes
- Learned dari images
- Alpha compositing untuk rendering

$$C = \sum_{d=1}^{D} T_d \cdot \alpha_d \cdot c_d$$

dimana $T_d = \prod_{d'<d}(1 - \alpha_{d'})$

### 6.2 Neural Radiance Fields (NeRF) untuk IBR

**NeRF** dapat dilihat sebagai neural IBR method.

**Proses:**
1. Train MLP dari multi-view images:
$$F_\theta(x, y, z, \theta, \phi) \rightarrow (r, g, b, \sigma)$$

2. Render novel view via volume rendering:
$$C(r) = \int_{t_n}^{t_f} T(t) \sigma(t) c(t) dt$$

**Advantages:**
- View-dependent effects (specularity)
- No explicit geometry needed
- High-quality results

### 6.3 Generative View Synthesis

**GAN-based:**
- Generate plausible novel views
- Handle large viewpoint changes
- May hallucinate content

**Diffusion-based:**
- Recent advances (2023-2024)
- Zero-shot novel view synthesis
- Conditioning pada reference images

---

## 7. Panoramic dan Omnidirectional Rendering

### 7.1 Cylindrical Panorama

**Stitching:**
1. Capture images dengan rotasi
2. Project ke cylindrical surface
3. Align dan blend

**Parameterization:**
$$x_{cyl} = f \cdot \theta$$
$$y_{cyl} = f \cdot \tan(\phi)$$

### 7.2 Spherical Panorama (360°)

**Equirectangular projection:**
- Map sphere ke rectangle
- Longitude → x, Latitude → y

**Cube map:**
- 6 faces of cube
- Commonly used dalam graphics

### 7.3 Virtual Tours

**Implementation:**
1. Capture 360° panoramas at multiple locations
2. Create navigation graph
3. Render current panorama
4. Transition antar nodes

---

## 8. Real-Time IBR Applications

### 8.1 Virtual Reality

**Requirements:**
- Low latency (< 20ms)
- High frame rate (90+ fps)
- Stereo rendering

**IBR untuk VR:**
- Pre-rendered light fields
- Foveated rendering
- Reprojection dari sparse views

### 8.2 Augmented Reality

**Challenges:**
- Real-time camera tracking
- Consistent lighting
- Occlusion handling

**IBR helps with:**
- Environment maps dari real world
- View-dependent reflections
- Background reconstruction

### 8.3 Telepresence

**Free-Viewpoint Video:**
- Capture dengan camera array
- Real-time novel view synthesis
- Enable virtual camera control

---

## 9. Evaluasi IBR

### 9.1 Image Quality Metrics

**PSNR (Peak Signal-to-Noise Ratio):**
$$PSNR = 10 \log_{10}\left(\frac{MAX^2}{MSE}\right)$$

**SSIM (Structural Similarity):**
$$SSIM(x, y) = \frac{(2\mu_x\mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 + c_2)}$$

**LPIPS (Learned Perceptual Image Patch Similarity):**
- Deep feature-based metric
- Better correlates dengan human perception

### 9.2 Temporal Consistency

Untuk video view synthesis:
- Flickering detection
- Temporal coherence
- Motion smoothness

### 9.3 Perceptual Studies

- User studies
- A/B testing
- Quality ratings

---

## 10. Aplikasi dan Kasus Penggunaan

### 10.1 Virtual Tourism

- Google Street View
- Virtual museum tours
- Real estate visualization

### 10.2 Sports Broadcasting

- Free viewpoint replay
- Bullet time effects
- Multiple angle viewing

### 10.3 E-Commerce

- 360° product views
- Virtual try-on
- Room visualization

### 10.4 Film dan Entertainment

- Visual effects
- Virtual production
- Game environments

### 10.5 Medical Visualization

- Surgical planning
- Training simulations
- Anatomy education

---

## Rangkuman

| Metode | Input | Geometri | Kelebihan | Kekurangan |
|--------|-------|----------|-----------|------------|
| Light Field | Dense images | None | Simple rendering | Banyak data |
| View Morphing | 2+ images | Implicit | Smooth transitions | Limited range |
| View-Dependent Texture | Sparse images | Proxy | Flexible | Need geometry |
| DIBR | RGB-D | Depth | Efficient | Holes/artifacts |
| NeRF | Multi-view | Implicit neural | High quality | Slow training |
| Panoramic | 360° images | None/simple | Immersive | Static position |

**Trend saat ini:**
1. Neural IBR (NeRF, 3D Gaussian Splatting) mendominasi research
2. Real-time rendering menjadi fokus
3. Generative models untuk novel view synthesis
4. Integration dengan AR/VR platforms

**Masa depan:**
- Instant novel view synthesis dari single image
- Real-time neural rendering pada mobile devices
- Seamless integration antara real dan virtual content
