# MATERI BAB 13: 3D RECONSTRUCTION

## 🎯 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami konsep dasar rekonstruksi 3D dari gambar 2D
2. Mengimplementasikan point cloud processing
3. Melakukan surface reconstruction dari point cloud
4. Memahami berbagai algoritma mesh generation
5. Menerapkan teknik rekonstruksi 3D untuk aplikasi nyata

---

## 📚 1. Definisi dan Konsep Dasar

### 1.1 Apa itu 3D Reconstruction?

**3D Reconstruction** adalah proses membangun representasi tiga dimensi dari sebuah objek atau scene berdasarkan input data seperti gambar 2D, depth maps, atau sensor 3D. Tujuannya adalah merekonstruksi bentuk (geometry), permukaan (surface), dan seringkali tampilan (appearance) dari objek.

### 1.2 Tingkatan Representasi 3D

```
┌─────────────────────────────────────────────────────────────────┐
│                    REPRESENTASI 3D                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Point Cloud   │      Mesh       │     Volumetric              │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • Kumpulan      │ • Vertices +    │ • Voxel grid                │
│   titik 3D      │   Faces         │ • Signed Distance           │
│ • (x, y, z)     │ • Triangles/    │   Function (SDF)           │
│ • + color/      │   Quads         │ • Implicit surface          │
│   normal        │ • Textured/     │ • Octree                    │
│                 │   Untextured    │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### 1.3 Pipeline Rekonstruksi 3D

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│  Images  │───▶│ Depth/Point  │───▶│   Surface    │───▶│  Final   │
│  /Depth  │    │    Cloud     │    │Reconstruction│    │  Mesh    │
└──────────┘    └──────────────┘    └──────────────┘    └──────────┘
                      │                    │
                      ▼                    ▼
              ┌──────────────┐    ┌──────────────┐
              │   Filtering  │    │   Smoothing  │
              │   Denoising  │    │   Texturing  │
              └──────────────┘    └──────────────┘
```

---

## 📖 2. Konsep Utama

### 2.1 Point Cloud Processing

#### 2.1.1 Apa itu Point Cloud?

Point cloud adalah representasi 3D paling dasar, berupa kumpulan titik-titik dalam ruang 3D. Setiap titik memiliki:
- Koordinat (x, y, z)
- Opsional: warna (RGB), normal, intensity

#### 2.1.2 Operasi pada Point Cloud

| Operasi | Deskripsi | Kegunaan |
|---------|-----------|----------|
| **Filtering** | Menghapus outlier/noise | Cleaning data |
| **Downsampling** | Mengurangi densitas | Efisiensi komputasi |
| **Normal Estimation** | Menghitung normal setiap titik | Persiapan reconstruction |
| **Registration** | Menggabungkan multiple scans | Multi-view 3D |
| **Segmentation** | Memisahkan objek berbeda | Object detection |

#### 2.1.3 Voxel Grid Filter

```
Input Point Cloud          Voxel Grid              Output Point Cloud
(Dense, Noisy)            (Discretization)         (Uniform, Clean)

    ● ●  ●                 ┌───┬───┬───┐
   ●  ● ●  ●               │ ● │   │ ● │           ●     ●
  ● ●● ●●● ●               ├───┼───┼───┤
   ●●  ●● ●         ───▶   │ ● │ ● │ ● │   ───▶    ●  ●  ●
  ●● ●●● ●●                ├───┼───┼───┤
   ● ●●  ●                 │ ● │ ● │   │           ●  ●
    ●                      └───┴───┴───┘
```

### 2.2 Surface Reconstruction

#### 2.2.1 Poisson Surface Reconstruction

**Konsep:**
- Menganggap surface sebagai iso-surface dari fungsi indicator
- Menggunakan gradient field dari estimated normals
- Menyelesaikan Poisson equation: ∇²χ = ∇·V

**Langkah-langkah:**
1. Estimate normal di setiap point
2. Construct vector field V dari normals
3. Solve Poisson equation untuk indicator function χ
4. Extract iso-surface (biasanya χ = 0)

```
Point Cloud        Normal Field       Poisson Solution     Mesh
with Normals       (Vector Field V)   (Indicator χ)        (Iso-surface)

  ● ↗ ● ↗         ┌─────────────┐     ┌─────────────┐     ╱──────╲
  ↗   ↗           │ → → → ↗ ↗   │     │ ░░░░░░░░░░░ │    │        │
● ↗ ● ↗ ●    ───▶ │ → → → → ↗   │ ───▶│ ░░░░░░░░   │ ───▶│        │
  ↗   ↗           │ → → → → →   │     │ ░░░░░░░    │    │        │
  ● ↗ ● ↗         └─────────────┘     └─────────────┘     ╲──────╱
```

#### 2.2.2 Ball Pivoting Algorithm (BPA)

**Konsep:**
- Menggunakan bola virtual yang "berputar" di antara points
- Tiga titik yang disentuh bola membentuk segitiga
- Iterasi sampai semua segitiga terbentuk

**Ilustrasi:**

```
                    Ball radius = r
                         ╭──╮
                        ╱    ╲
        ●──────●      ╱  ◯   ╲      ●──────●
       ╱              ╲      ╱     ╱╲
      ╱                ╲    ╱     ╱  ╲
     ●                  ╲──╱     ●────●
     
  Initial          Ball pivoting    Triangle formed
```

### 2.3 Mesh Representation

#### 2.3.1 Triangle Mesh

```
Vertices: [V₀, V₁, V₂, V₃, V₄, ...]
Faces: [(0,1,2), (1,2,3), (2,3,4), ...]

        V₀
       ╱  ╲
      ╱    ╲
    V₁──────V₂
     │╲    ╱│
     │  ╲╱  │
    V₃──────V₄
```

#### 2.3.2 Mesh Quality Metrics

| Metric | Deskripsi | Formula |
|--------|-----------|---------|
| **Face count** | Jumlah segitiga | \|F\| |
| **Vertex count** | Jumlah vertex | \|V\| |
| **Edge length** | Panjang sisi | √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²) |
| **Face area** | Luas segitiga | ½ \|AB × AC\| |
| **Aspect ratio** | Rasio sisi | longest_edge / shortest_edge |
| **Watertight** | Mesh tertutup | No holes, manifold |

### 2.4 Volumetric Reconstruction

#### 2.4.1 Voxel Grid

```
        ┌───┬───┬───┬───┐
       ╱   ╱   ╱   ╱   ╱│
      ┌───┬───┬───┬───┐ │
     ╱   ╱░░░╱░░░╱   ╱│ │
    ┌───┬───┬───┬───┐ │ │
   ╱   ╱░░░╱░░░╱   ╱│ │╱
  ┌───┬───┬───┬───┐ │╱ 
  │   │░░░│░░░│   │╱   
  └───┴───┴───┴───┘    
  
  ░ = occupied voxel
```

#### 2.4.2 Signed Distance Function (SDF)

SDF menyimpan jarak dari setiap voxel ke surface terdekat:
- Positif: di luar object
- Negatif: di dalam object
- Zero crossing: surface

```
  +2  +1   0  -1  -2
  ┌───┬───┬───┬───┬───┐
  │+2 │+1 │ 0 │-1 │-2 │  ← Cross section
  ├───┼───┼───┼───┼───┤
  │+1 │ 0 │-1 │-2 │-1 │     of SDF volume
  ├───┼───┼───┼───┼───┤
  │ 0 │-1 │-2 │-1 │ 0 │
  ├───┼───┼───┼───┼───┤
  │+1 │ 0 │-1 │ 0 │+1 │
  └───┴───┴───┴───┴───┘
         ↑
    Zero-crossing = surface
```

### 2.5 Marching Cubes Algorithm

**Tujuan:** Extract iso-surface dari volumetric data (SDF atau voxel grid)

**Konsep:**
1. Iterasi melalui setiap cell (8 voxel corners)
2. Tentukan konfigurasi berdasarkan inside/outside
3. 256 kemungkinan konfigurasi → 15 unique cases
4. Generate triangles berdasarkan lookup table

```
Case 0:         Case 1:         Case 3:         Case 14:
All outside     One corner in    Two corners     Seven corners
                
  ○───○         ●───○           ●───●           ●───●
  │   │         │╲  │           │   │           │   │
  │   │   vs    │ ╲ │    vs     ├───┤    vs     │╲╲╲│
  │   │         │  ╲│           │   │           │ ╲╲│
  ○───○         ○───○           ○───○           ●───○
  
(no triangle)  (1 triangle)   (2 triangles)  (3 triangles)
```

---

## 📊 3. Diagram dan Ilustrasi

### 3.1 Multi-View 3D Reconstruction Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MULTI-VIEW 3D RECONSTRUCTION                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    ▼                         ▼                         ▼
┌───────┐                ┌───────┐                 ┌───────┐
│Image 1│                │Image 2│                 │Image N│
└───┬───┘                └───┬───┘                 └───┬───┘
    │                        │                         │
    └────────────┬───────────┴─────────────────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   Feature Detection    │  ◀── SIFT, SURF, ORB
    │    & Matching          │
    └───────────┬────────────┘
                │
                ▼
    ┌────────────────────────┐
    │ Structure from Motion  │  ◀── Camera poses + Sparse 3D
    │        (SfM)           │
    └───────────┬────────────┘
                │
                ▼
    ┌────────────────────────┐
    │    Multi-View Stereo   │  ◀── Dense depth maps
    │        (MVS)           │
    └───────────┬────────────┘
                │
                ▼
    ┌────────────────────────┐
    │    Point Cloud Fusion  │  ◀── Merge + Filter
    │                        │
    └───────────┬────────────┘
                │
                ▼
    ┌────────────────────────┐
    │ Surface Reconstruction │  ◀── Poisson, BPA, etc.
    │                        │
    └───────────┬────────────┘
                │
                ▼
    ┌────────────────────────┐
    │    Texture Mapping     │  ◀── Project images to mesh
    │                        │
    └────────────────────────┘
```

### 3.2 Point Cloud Registration (ICP)

```
Source Cloud         Target Cloud         After ICP
    
    ●●●                    ○○○            ●●●  (aligned)
   ●●●●●                  ○○○○○          ●●●●●
    ●●●                    ○○○            ●●●
    
Initial Transform:            Iterative Refinement:
┌         ┐                  1. Find correspondences
│ R  | t  │                  2. Compute transform
│────┼────│         ───▶     3. Apply transform
│ 0  | 1  │                  4. Repeat until converge
└         ┘
```

---

## 🏭 4. Contoh Kasus Industri

### 4.1 Digital Heritage Preservation

**Skenario:** Museum Nasional Indonesia ingin membuat arsip digital dari artefak-artefak bersejarah.

**Solusi:**
- Multi-view photogrammetry untuk rekonstruksi 3D
- High-resolution texture mapping
- Level of Detail (LOD) untuk web viewing

**Workflow:**
1. Capture 100+ foto dari berbagai sudut
2. SfM untuk camera poses
3. MVS untuk dense reconstruction
4. Poisson surface reconstruction
5. Texture projection dari foto original

### 4.2 Quality Inspection di Manufaktur

**Skenario:** Pabrik otomotif perlu mengukur presisi komponen dengan toleransi < 0.1mm.

**Solusi:**
- 3D scanning dengan structured light
- Point cloud alignment dengan CAD model
- Automatic defect detection

**Metrics yang diukur:**
- Deviasi dari CAD reference
- Surface roughness
- Hole diameter accuracy
- Edge quality

### 4.3 Medical Imaging

**Skenario:** Rekonstruksi 3D organ dari CT/MRI scan untuk surgical planning.

**Pipeline:**
1. DICOM image stack loading
2. Segmentation (organ isolation)
3. Marching cubes for surface extraction
4. Smoothing dan hole filling
5. 3D printing untuk surgical guide

---

## 📝 5. Ringkasan

### Konsep Kunci:

| Konsep | Definisi | Aplikasi |
|--------|----------|----------|
| Point Cloud | Kumpulan titik 3D dengan atribut | Raw 3D data |
| Mesh | Vertices + faces (triangles) | Rendering, CAD |
| SDF | Signed distance to surface | Implicit modeling |
| Poisson Recon | Surface dari gradient field | Smooth surfaces |
| Marching Cubes | Iso-surface dari volume | Medical imaging |
| ICP | Alignment via closest point | Multi-view fusion |

### Algoritma Utama:

1. **Preprocessing:**
   - Voxel grid downsampling
   - Statistical outlier removal
   - Normal estimation

2. **Surface Reconstruction:**
   - Poisson: smooth, watertight
   - Ball pivoting: preserves detail
   - Alpha shapes: handles thin structures

3. **Post-processing:**
   - Mesh smoothing (Laplacian)
   - Decimation (simplification)
   - Hole filling
   - Texture mapping

---

## 🎥 6. Deskripsi Tugas Video

### Judul: "Rekonstruksi 3D: Dari Point Cloud ke Mesh"

### Durasi: 7-10 menit

### Outline Video:

1. **Pendahuluan (1-2 menit)**
   - Perkenalan
   - Apa itu 3D reconstruction?
   - Aplikasi dalam kehidupan nyata

2. **Konsep Point Cloud (2-3 menit)**
   - Definisi point cloud
   - Sumber data: stereo, LiDAR, depth camera
   - Operasi dasar: filtering, downsampling

3. **Surface Reconstruction (2-3 menit)**
   - Penjelasan Poisson reconstruction
   - Demo dengan Open3D
   - Parameter tuning

4. **Demonstrasi Kode (2-3 menit)**
   - Load point cloud
   - Preprocessing
   - Reconstruction
   - Save mesh

5. **Penutup (1 menit)**
   - Ringkasan
   - Tantangan dan future work

### Kriteria Penilaian:
- Akurasi penjelasan teori (30%)
- Kualitas demo praktis (30%)
- Kejelasan penyampaian (20%)
- Kualitas produksi video (20%)
