# Bab 13: 3D Reconstruction

## Pendahuluan

**3D Reconstruction** adalah proses membangun model tiga dimensi dari objek atau scene berdasarkan gambar 2D atau data sensor lainnya. Ini merupakan salah satu tujuan utama computer vision dengan aplikasi luas di bidang robotika, realitas virtual/augmented, manufaktur, arsitektur, dan hiburan.

Bab ini membahas berbagai teknik rekonstruksi 3D, mulai dari pendekatan berbasis geometri klasik hingga metode deep learning modern.

---

## 1. Representasi 3D

### 1.1 Point Clouds

**Point cloud** adalah kumpulan titik 3D (x, y, z) yang merepresentasikan permukaan objek.

**Karakteristik:**
- Unstructured: Tidak ada konektivitas
- Sparse atau dense
- Dapat memiliki atribut (warna, normal, intensity)

**Format umum:**
- PLY (Polygon File Format)
- PCD (Point Cloud Data - PCL format)
- XYZ, LAS (LiDAR)

```python
# Point cloud structure
points = np.array([
    [x1, y1, z1],
    [x2, y2, z2],
    ...
])  # Shape: (N, 3)

colors = np.array([
    [r1, g1, b1],
    ...
])  # Shape: (N, 3)
```

### 1.2 Mesh (Triangle Mesh)

**Mesh** adalah representasi permukaan menggunakan vertices dan faces (biasanya segitiga).

**Komponen:**
- **Vertices (V)**: Titik-titik 3D
- **Faces (F)**: Indeks vertices yang membentuk face
- **Normals**: Vektor normal untuk shading
- **Texture coordinates (UV)**: Mapping ke texture

```python
# Triangle mesh
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])  # Shape: (V, 3)

faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
])  # Shape: (F, 3), indices ke vertices
```

### 1.3 Volumetric Representations

#### Voxels
**Voxel** (volumetric pixel) adalah grid 3D dengan nilai occupancy atau signed distance.

```python
# Voxel grid
voxels = np.zeros((64, 64, 64))  # Binary occupancy
voxels[x, y, z] = 1  # Occupied
voxels[x, y, z] = 0  # Empty
```

#### TSDF (Truncated Signed Distance Function)
Menyimpan signed distance ke surface terdekat.

$$TSDF(x) = \begin{cases} 
d(x) & \text{if } d(x) < t \\
t & \text{otherwise}
\end{cases}$$

dimana $d(x)$ adalah signed distance dan $t$ adalah truncation threshold.

### 1.4 Implicit Representations

#### Occupancy Networks
$$f_\theta(x, z) = o \in [0, 1]$$

dimana $x$ adalah koordinat 3D, $z$ adalah latent code, dan $o$ adalah probability occupancy.

#### Signed Distance Functions (Neural)
$$f_\theta(x) = s \in \mathbb{R}$$

dimana $s$ adalah signed distance ke surface.

#### NeRF (Neural Radiance Fields)
$$f_\theta(x, d) = (c, \sigma)$$

dimana $x$ adalah posisi, $d$ adalah viewing direction, $c$ adalah color, dan $\sigma$ adalah density.

---

## 2. Surface Reconstruction dari Point Cloud

### 2.1 Ball Pivoting Algorithm (BPA)

**Konsep:** Ball dengan radius $\rho$ berputar di sekitar edge, menyentuh tiga titik sekaligus.

**Algoritma:**
1. Initialize dengan seed triangle
2. Pivot ball di sekitar edge
3. Jika ball menyentuh titik baru, buat triangle baru
4. Repeat sampai semua edges processed

**Karakteristik:**
- Membutuhkan normal estimation
- Sensitif terhadap pilihan radius
- Tidak mengisi holes dengan baik

### 2.2 Poisson Surface Reconstruction

**Prinsip:** Merekonstruksi surface sebagai isosurface dari indicator function.

**Formulasi:**
Diberikan oriented points $(p_i, n_i)$, cari indicator function $\chi$ dimana:
$$\nabla \chi = V$$

dengan $V$ adalah vector field dari normals.

**Langkah:**
1. Estimate normals untuk point cloud
2. Build octree untuk adaptive sampling
3. Solve Poisson equation: $\Delta \chi = \nabla \cdot V$
4. Extract isosurface ($\chi = threshold$)

**Keuntungan:**
- Menghasilkan watertight mesh
- Robust terhadap noise
- Mengisi holes

### 2.3 Marching Cubes

**Tujuan:** Extract isosurface dari volumetric data.

**Algoritma:**
1. Divide space menjadi voxel grid
2. Untuk setiap voxel cube:
   - Tentukan vertex status (inside/outside surface)
   - Lookup table untuk triangles (256 cases, 15 unique)
   - Interpolate edge positions
3. Generate triangles

```python
# Marching cubes pseudocode
for each cube in grid:
    index = 0
    for i, vertex in enumerate(cube.vertices):
        if value[vertex] < isovalue:
            index |= (1 << i)
    
    triangles = lookup_table[index]
    for triangle in triangles:
        # Interpolate positions
        # Add to mesh
```

### 2.4 Delaunay Triangulation

**2D Delaunay:** Triangulasi dimana tidak ada titik di dalam circumcircle triangle manapun.

**3D Delaunay:** Menghasilkan tetrahedra, kemudian extract surface.

**Alpha Shapes:**
Subset dari Delaunay triangulation berdasarkan parameter alpha:
- Small alpha → Hollow/holes
- Large alpha → Convex hull

---

## 3. Multi-View Stereo (MVS) Reconstruction

### 3.1 Pipeline MVS

```
Multiple Images → SfM → Sparse Points + Cameras → MVS → Dense Points → Mesh
```

**Input:**
- Calibrated images dengan camera poses
- Sparse point cloud dari SfM

**Output:**
- Dense point cloud atau depth maps
- Triangle mesh

### 3.2 Depth Map Fusion Methods

#### Per-View Depth Estimation
Untuk setiap reference view:
1. Select neighboring views
2. Compute depth map via stereo matching
3. Filter dan refine

#### TSDF Fusion

**Langkah:**
1. Initialize TSDF volume
2. Untuk setiap depth map:
   - Project ke volume
   - Update TSDF values
   - Update weights

```python
def update_tsdf(volume, depth_map, camera_pose, intrinsics, truncation):
    for each voxel in volume:
        # Project to image
        point_cam = transform(voxel, camera_pose)
        pixel = project(point_cam, intrinsics)
        
        if pixel in image_bounds:
            measured_depth = depth_map[pixel]
            sdf = measured_depth - point_cam.z
            
            if abs(sdf) < truncation:
                # Running weighted average
                weight = compute_weight(sdf)
                volume.tsdf[voxel] = (
                    volume.tsdf[voxel] * volume.weight[voxel] + sdf * weight
                ) / (volume.weight[voxel] + weight)
                volume.weight[voxel] += weight
```

### 3.3 Patch-based MVS (PMVS)

**PMVS Algorithm:**
1. **Matching:** Detect dan match features
2. **Expansion:** Expand patches ke neighboring pixels
3. **Filtering:** Remove inconsistent patches

**Patch representation:**
- Center point $c$
- Normal vector $n$
- Reference image

**Photo-consistency check:**
$$NCC(P_1, P_2) > threshold$$

### 3.4 Deep Learning MVS

#### MVSNet Architecture
```
Reference Image + Source Images → Feature Extraction → Cost Volume → 3D CNN → Depth Map
```

**Cost Volume Construction:**
1. Extract features dari semua views
2. Warp source features ke reference view di berbagai depths
3. Compute variance across views
4. 3D CNN untuk regularization

#### CasMVSNet (Cascade MVS)
Coarse-to-fine approach:
1. Coarse depth dengan small resolution
2. Refine dengan narrower depth range
3. Multiple stages untuk high resolution

---

## 4. Shape from X Methods

### 4.1 Shape from Silhouette

**Visual Hull:** Intersection dari semua silhouette cones.

```python
def visual_hull(silhouettes, cameras):
    volume = np.ones((N, N, N))  # Initialize all occupied
    
    for silhouette, camera in zip(silhouettes, cameras):
        for voxel in volume:
            pixel = project(voxel, camera)
            if not silhouette[pixel]:
                volume[voxel] = 0  # Carve out
    
    return volume
```

**Limitasi:**
- Hanya convex approximation
- Tidak bisa reconstruct concavities

### 4.2 Shape from Shading

**Prinsip:** Infer surface orientation dari image intensity.

**Image formation model:**
$$I(x, y) = \rho(x, y) \cdot R(n(x, y))$$

dimana:
- $\rho$ = surface albedo
- $R$ = reflectance function
- $n$ = surface normal

**Untuk Lambertian surface:**
$$I = \rho \cdot (n \cdot l)$$

dengan $l$ adalah light direction.

**Challenges:**
- Perlu known lighting
- Ambiguity (concave vs convex)
- Assumes known reflectance

### 4.3 Photometric Stereo

**Setup:** Multiple images dengan different lighting, fixed camera.

**Untuk Lambertian surface:**
$$I_i = \rho \cdot (n \cdot l_i)$$

Dengan $k$ lights:
$$\begin{bmatrix} I_1 \\ I_2 \\ \vdots \\ I_k \end{bmatrix} = \rho \begin{bmatrix} l_1^T \\ l_2^T \\ \vdots \\ l_k^T \end{bmatrix} n$$

**Solve untuk normal:**
$$n = \frac{1}{\rho} L^+ \cdot I$$

dimana $L^+$ adalah pseudoinverse dari lighting matrix.

### 4.4 Shape from Focus/Defocus

**Shape from Focus:**
1. Capture focus stack (varying focus distance)
2. Compute sharpness measure per pixel
3. Depth = focus distance dengan maximum sharpness

**Shape from Defocus:**
Estimate depth dari blur amount:
$$\sigma \propto |d - d_{focus}|$$

---

## 5. Neural 3D Reconstruction

### 5.1 Occupancy Networks

**Network:**
$$f_\theta : \mathbb{R}^3 \times \mathbb{R}^L \rightarrow [0, 1]$$

**Training:**
- Input: 3D coordinate $x$, shape code $z$
- Output: Occupancy probability
- Loss: Binary cross-entropy

**Inference:**
1. Encode input ke latent code $z$
2. Query occupancy di regular grid
3. Extract surface via Marching Cubes

### 5.2 DeepSDF

**Signed Distance Function:**
$$f_\theta : \mathbb{R}^3 \times \mathbb{R}^L \rightarrow \mathbb{R}$$

**Loss:**
$$L = \sum_i |clamp(f_\theta(x_i, z), -\delta, \delta) - clamp(s_i, -\delta, \delta)|$$

**Auto-decoder training:**
- Jointly optimize $\theta$ dan latent codes $\{z_i\}$
- No encoder needed

### 5.3 NeRF (Neural Radiance Fields)

**Representation:**
$$F_\theta : (x, y, z, \theta, \phi) \rightarrow (r, g, b, \sigma)$$

**Volume Rendering:**
$$C(r) = \int_{t_n}^{t_f} T(t) \sigma(r(t)) c(r(t), d) dt$$

dimana $T(t) = exp(-\int_{t_n}^{t} \sigma(r(s)) ds)$

**Training:**
- Minimize rendering loss:
$$L = \sum_r ||C(r) - C_{gt}(r)||^2$$

**Positional Encoding:**
$$\gamma(p) = (\sin(2^0\pi p), \cos(2^0\pi p), ..., \sin(2^{L-1}\pi p), \cos(2^{L-1}\pi p))$$

### 5.4 Instant NGP (Neural Graphics Primitives)

**Hash encoding** untuk faster training:
- Multi-resolution hash grid
- Interpolate features dari grid
- Much faster training (seconds vs hours)

---

## 6. 3D Reconstruction Pipeline

### 6.1 Complete Pipeline

```
Images → Feature Detection → Feature Matching → SfM → Camera Poses
                                                    ↓
                                            Sparse Point Cloud
                                                    ↓
                            Dense Reconstruction (MVS / Depth Fusion)
                                                    ↓
                                            Dense Point Cloud
                                                    ↓
                                    Surface Reconstruction (Poisson/TSDF)
                                                    ↓
                                            Triangle Mesh
                                                    ↓
                                    Texture Mapping (optional)
                                                    ↓
                                            Textured Model
```

### 6.2 Tools dan Software

| Tool | Deskripsi | License |
|------|-----------|---------|
| COLMAP | SfM + MVS | BSD |
| OpenMVS | Dense reconstruction | AGPL |
| Meshlab | Mesh processing | GPL |
| Open3D | Point cloud processing | MIT |
| Metashape | Commercial photogrammetry | Commercial |

### 6.3 Best Practices

**Image Capture:**
- Overlap 60-80% antar images
- Consistent lighting
- Avoid reflective/transparent surfaces
- Multiple angles coverage

**Processing:**
- Start dengan incremental SfM
- Use global bundle adjustment
- Filter outliers di setiap stage
- Adaptive resolution untuk efficiency

---

## 7. Evaluasi dan Metrics

### 7.1 Geometric Accuracy

**Chamfer Distance:**
$$CD(P_1, P_2) = \frac{1}{|P_1|}\sum_{p \in P_1} \min_{q \in P_2} ||p - q||^2 + \frac{1}{|P_2|}\sum_{q \in P_2} \min_{p \in P_1} ||q - p||^2$$

**Hausdorff Distance:**
$$HD(P_1, P_2) = \max\{\max_{p \in P_1} \min_{q \in P_2} ||p - q||, \max_{q \in P_2} \min_{p \in P_1} ||q - p||\}$$

**F-Score:**
$$F = \frac{2 \cdot Precision \cdot Recall}{Precision + Recall}$$

dengan:
- Precision = % predicted points dekat GT
- Recall = % GT points dekat prediction

### 7.2 Surface Quality

- **Normal consistency**: Angle antara predicted dan GT normals
- **Surface smoothness**: Variance of normals
- **Completeness**: Coverage of target surface

### 7.3 Visual Quality

- **PSNR/SSIM** untuk rendered views
- **LPIPS** untuk perceptual similarity

---

## 8. Aplikasi

### 8.1 Cultural Heritage
- Digitalisasi artefak dan bangunan bersejarah
- Virtual museum
- Preservation dan restoration

### 8.2 Manufacturing dan Inspection
- Quality control
- Reverse engineering
- CAD/CAM integration

### 8.3 Medical Imaging
- 3D reconstruction dari CT/MRI
- Surgical planning
- Prosthetics design

### 8.4 Entertainment
- VFX dan film production
- Video game assets
- Virtual/Augmented reality

### 8.5 Autonomous Systems
- 3D mapping untuk robot navigation
- Obstacle detection
- Environment understanding

---

## Rangkuman

| Metode | Input | Output | Kelebihan | Kekurangan |
|--------|-------|--------|-----------|------------|
| Point Cloud | Sensor/MVS | Points | Simple, direct | No surface info |
| Poisson | Oriented points | Watertight mesh | Robust, fills holes | May hallucinate |
| TSDF Fusion | Depth maps | Volumetric | Real-time capable | Resolution limited |
| MVS | Multi-view images | Dense depth | Detailed | Compute intensive |
| Shape from Silhouette | Silhouettes | Visual hull | Simple | Only convex |
| NeRF | Multi-view images | Implicit | View synthesis | Slow training |

Pilihan metode tergantung pada:
- Tipe input data yang tersedia
- Akurasi yang dibutuhkan
- Computational budget
- Real-time requirements
- Tipe objek (convex, thin structures, texture)
