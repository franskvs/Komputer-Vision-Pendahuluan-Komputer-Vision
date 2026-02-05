# BAB 13: 3D RECONSTRUCTION - MODULE GUIDE

## 📋 Daftar Isi

1. [Gambaran Umum](#gambaran-umum)
2. [Struktur Module](#struktur-module)
3. [Persyaratan Sistem](#persyaratan-sistem)
4. [Panduan Instalasi](#panduan-instalasi)
5. [Panduan Praktikum](#panduan-praktikum)
6. [File Output](#file-output)
7. [Troubleshooting](#troubleshooting)

---

## Gambaran Umum

**BAB 13: 3D Reconstruction** adalah modul praktikum yang komprehensif untuk mempelajari teknik-teknik rekonstruksi 3D modern. Modul ini mencakup:

- ✅ **Fundamentals:** Point cloud basics, format file, dan visualisasi
- ✅ **Preprocessing:** Filtering, downsampling, normal estimation
- ✅ **Registration:** ICP (Iterative Closest Point) dan global registration
- ✅ **Reconstruction:** Poisson surface reconstruction dan Ball Pivoting Algorithm
- ✅ **Post-processing:** Mesh smoothing, simplification, dan repair

### Tujuan Pembelajaran

Setelah menyelesaikan modul ini, Anda diharapkan mampu:

1. Memahami konsep dasar 3D reconstruction
2. Mengolah point cloud dengan filtering dan normal estimation
3. Melakukan surface reconstruction menggunakan berbagai algoritma
4. Memproses mesh untuk meningkatkan kualitas
5. Menerapkan teknik-teknik ini untuk aplikasi real-world

---

## Struktur Module

```
Bab-13-3D-Reconstruction/
├── Materi.md                              # Teori komprehensif
├── Jobsheet.md                            # Panduan praktikum lengkap
├── Project.md                             # Spesifikasi project akhir
├── Referensi.md                           # Daftar referensi & resources
├── Rubrik_Penilaian_Project.md           # Kriteria penilaian project
├── Rubrik_Penilaian_Tugas_Video.md       # Kriteria video tutorial
│
└── praktikum/                             # Directory praktikum
    ├── 01_point_cloud_basics.py          # Load, save, visualize point cloud
    ├── 02_point_cloud_filtering.py       # Voxel grid, outlier removal
    ├── 03_normal_estimation.py           # KNN & radius-based normal estimation
    ├── 04_point_cloud_registration.py    # ICP, global registration
    ├── 05_poisson_reconstruction.py      # Poisson surface reconstruction
    ├── 06_ball_pivoting.py               # Ball pivoting algorithm
    ├── 07_mesh_processing.py             # Smoothing, simplification, repair
    ├── run_all_tests.py                  # Automated test runner
    ├── run_program.py                    # Individual program runner
    │
    ├── data/                             # Directory untuk sample data
    │   └── point_clouds/                 # PLY, PCD, XYZ files
    │
    └── output/                           # Directory output hasil praktikum
        ├── output1/                      # Output program 1
        ├── output2/                      # Output program 2
        ├── ...
        ├── output7/                      # Output program 7
        ├── test_report.json              # Hasil testing semua program
        └── README.txt                    # Informasi output files
```

---

## Persyaratan Sistem

### Hardware Minimum
- CPU: 4-core processor
- RAM: 8 GB (16 GB recommended untuk large point clouds)
- Storage: 10 GB free space untuk sample data dan outputs
- GPU: Optional (untuk processing lebih cepat)

### Software Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Programming language |
| Open3D | 0.17+ | 3D processing library |
| NumPy | 1.19+ | Numerical computing |
| Matplotlib | 3.3+ | Visualization |
| SciPy | 1.5+ | Scientific computing |

### Operating System
- Linux (Ubuntu 20.04+) ✅ **Recommended**
- macOS (10.14+) ✅
- Windows 10/11 ✅
- Wayland display server ✅ (auto-detects and uses Matplotlib)

---

## Panduan Instalasi

### 1. Instalasi Python & Dependencies

**Option A: Using pip (Recommended)**

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install --upgrade pip
pip install open3d numpy matplotlib scipy
```

**Option B: Using conda**

```bash
conda create -n cv-3d python=3.9
conda activate cv-3d
conda install -c conda-forge open3d numpy matplotlib scipy
```

### 2. Verifikasi Instalasi

```bash
cd Bab-13-3D-Reconstruction/praktikum

# Test Open3D
python3 -c "import open3d as o3d; print(f'Open3D {o3d.__version__} OK')"

# Test other packages
python3 -c "import numpy, matplotlib, scipy; print('All dependencies OK')"
```

---

## Panduan Praktikum

### Quick Start

```bash
# Navigate to praktikum directory
cd Bab-13-3D-Reconstruction/praktikum

# Run ALL programs with automatic testing
python3 run_all_tests.py

# Or run individual program
python3 01_point_cloud_basics.py
```

### Program-by-Program Guide

#### 1. Point Cloud Basics (01_point_cloud_basics.py)
**Waktu: ~5 menit** | **Output: 4 files**

Tujuan: Memahami struktur point cloud dan operasi dasar

**Apa yang dipelajari:**
- Load/save point cloud dari berbagai format (PLY, PCD, XYZ)
- Create synthetic point clouds (sphere, cube, random)
- Access point coordinates, colors, normals
- Basic transformations (translate, rotate, scale)
- Analyze point cloud properties

**Output Files:**
- `sphere.ply`, `sphere.pcd` - Sphere point cloud
- `cube.ply` - Cube point cloud
- `random.xyz` - Random point cloud

**Tugas Bonus:**
- Modify NUM_POINTS_* constants untuk test dengan berbagai ukuran
- Implement custom point cloud generation function
- Add color mapping berdasarkan coordinate values

---

#### 2. Point Cloud Filtering (02_point_cloud_filtering.py)
**Waktu: ~10 menit** | **Output: 8 files**

Tujuan: Membersihkan point cloud dari noise dan mengurangi ukuran

**Apa yang dipelajari:**
- Voxel grid downsampling untuk uniform sampling
- Statistical outlier removal menggunakan neighbor analysis
- Radius-based outlier removal
- Pass-through filtering untuk region of interest

**Output Files:**
- `downsampled_v*.ply` - Results dari berbagai voxel sizes
- `sor_filtered.ply` - Statistical outlier removal result
- `ror_filtered.ply` - Radius outlier removal result
- `passthrough_filtered.ply` - Pass-through filter result
- `combined_filtered.ply` - Combined filtering result

**Parameter Eksperimen:**
```python
VOXEL_SIZES = [0.01, 0.02, 0.05, 0.1]
SOR_NB_NEIGHBORS = 20
SOR_STD_RATIO = 2.0
ROR_NB_POINTS = 16
ROR_RADIUS = 0.05
```

---

#### 3. Normal Estimation (03_normal_estimation.py)
**Waktu: ~8 menit** | **Output: 1 file**

Tujuan: Estimate surface normals yang diperlukan untuk reconstruction

**Apa yang dipelajari:**
- KNN-based normal estimation (k-nearest neighbors)
- Radius-based normal estimation
- Consistent normal orientation
- Comparison of estimation methods

**Output Files:**
- `normals_estimated.ply` - Point cloud dengan normals

**Key Concepts:**
- Normal vectors penting untuk surface reconstruction
- KNN vs Radius: trade-off antara speed dan stability
- Consistent orientation mencegah flipped normals

---

#### 4. Point Cloud Registration (04_point_cloud_registration.py)
**Waktu: ~8 menit** | **Output: 1 file**

Tujuan: Align multiple point clouds ke sistem koordinat yang sama

**Apa yang dipelajari:**
- Iterative Closest Point (ICP) - Point to Point
- Point-to-Plane ICP (lebih robust)
- Global registration dengan RANSAC
- Multi-view fusion

**Output Files:**
- `registered_merged.ply` - Merged result dari multiple scans

**Skenario:**
- Small rotations/translations (< 30°)
- Large transformations (> 45°)
- Partial overlap
- With noise

---

#### 5. Poisson Surface Reconstruction (05_poisson_reconstruction.py)
**Waktu: ~120+ menit (computationally intensive)** | **Output: varies**

⚠️ **Note:** Program ini melakukan banyak rekonstruksi dengan parameter berbeda. Untuk testing cepat, dapat mengurangi jumlah points atau depth values.

Tujuan: Menghasilkan mesh watertight dari point cloud

**Apa yang dipelajari:**
- Poisson equation solving untuk surface reconstruction
- Octree-based algorithm
- Density-based mesh cropping
- Quality assessment

**Optimization Tips:**
- Reduce point count: `NUM_POINTS = 20000` (default 50000)
- Reduce depth levels: `POISSON_DEPTHS = [8, 9]` (default [6,8,9,10])
- Skip demo_reconstruction_quality untuk testing cepat

---

#### 6. Ball Pivoting Algorithm (06_ball_pivoting.py)
**Waktu: ~90+ menit (computationally intensive)** | **Output: 4+ files**

Tujuan: Alternative surface reconstruction yang preserves detail

**Apa yang dipelajari:**
- Ball pivoting concept
- Optimal radius selection
- Multi-scale BPA
- Comparison dengan Poisson

**Output Files:**
- `bpa_r*.ply` - Results dengan berbagai radii

---

#### 7. Mesh Processing (07_mesh_processing.py)
**Waktu: ~20 menit** | **Output: 14+ files**

Tujuan: Post-processing untuk meningkatkan kualitas mesh

**Apa yang dipelajari:**
- Laplacian dan Taubin smoothing
- Mesh decimation (simplification)
- Subdivision
- Hole filling
- Mesh repair

**Output Files:**
- `pipeline_*.ply` - Complete pipeline stages
- `smoothing_*.ply` - Smoothing results
- `simplify_*.ply` - Decimation results
- `repair_*.ply` - Repair results
- `color_*.ply` - Colored output

---

### Menjalankan Semua Tests

```bash
# Run dengan automatic testing
python3 run_all_tests.py

# Hasil akan tersimpan di:
# - output/test_report.json (detailed results)
# - output/output1-7/ (program outputs)
```

**Expected Results:**
- ✅ Program 1-4: ~5-10s each (✓ fast)
- ✅ Program 7: ~15-20s (✓ reasonable)
- ⚠️ Program 5-6: >180s (slow, computationally intensive)

---

## File Output

### Output Structure

```
praktikum/output/
├── output1/                    # Point Cloud Basics
│   ├── sphere.ply             (264 KB)
│   ├── sphere.pcd             (157 KB)
│   ├── cube.ply               (212 KB)
│   └── random.xyz             (198 KB)
│
├── output2/                    # Point Cloud Filtering
│   ├── downsampled_v0.01.ply  (1.3 MB)
│   ├── downsampled_v0.02.ply  (1.1 MB)
│   ├── sor_filtered.ply        (792 KB)
│   ├── ror_filtered.ply        (200 KB)
│   ├── passthrough_filtered.ply (197 KB)
│   └── combined_filtered.ply    (946 KB)
│
├── output3/                    # Normal Estimation
│   └── normals_estimated.ply   (1.4 MB)
│
├── output4/                    # Point Cloud Registration
│   └── registered_merged.ply   (2.0 MB)
│
├── output5/                    # Poisson Reconstruction
│   └── (varies, depends on completion)
│
├── output6/                    # Ball Pivoting
│   ├── bpa_r0.0349.ply        (2.1 MB)
│   ├── bpa_r0.0697.ply        (1.9 MB)
│   └── bpa_r0.1395.ply        (1.8 MB)
│
├── output7/                    # Mesh Processing
│   ├── pipeline_*.ply          (5-10 MB each)
│   ├── smoothing_*.ply         (various)
│   ├── simplify_*.ply          (various)
│   ├── repair_*.ply            (120 KB each)
│   └── color_*.ply             (114 KB each)
│
└── test_report.json            # Test results summary
```

### Membuka Output Files

```bash
# View dengan Open3D
python3 << 'EOF'
import open3d as o3d

pcd = o3d.io.read_point_cloud("output1/sphere.ply")
mesh = o3d.io.read_triangle_mesh("output7/pipeline_5_final.ply")

# Visualize
o3d.visualization.draw_geometries([pcd])  # For point clouds
o3d.visualization.draw_geometries([mesh])  # For meshes
EOF

# Or use external viewers
# - CloudCompare (cross-platform, free): https://www.cloudcompare.org/
# - Meshlab (free): https://www.meshlab.net/
# - Blender (free): https://www.blender.org/
```

---

## Troubleshooting

### Problem: "ImportError: No module named 'open3d'"

**Solution:**
```bash
pip install --upgrade open3d
# Or if using conda:
conda install -c conda-forge open3d
```

### Problem: "Segmentation fault" atau "Bus error"

**Cause:** Memory issue dengan large point clouds

**Solution:**
- Reduce point cloud size: `NUM_POINTS = 10000`
- Close other applications
- Upgrade RAM
- Use downsampling before reconstruction

### Problem: Visualization window tidak muncul

**For Wayland/X11 Display Issues:**
```bash
# Set matplotlib backend
export MPLBACKEND=Agg
python3 program.py
```

### Problem: Timeout pada Poisson/BPA programs

**Solution:**
```bash
# Run dengan extended timeout
timeout 300 python3 05_poisson_reconstruction.py

# Or modify run_all_tests.py timeout values
# Find: "timeout=180" → change to "timeout=300"
```

### Problem: Output files terlalu besar

**Solution:** Enable compression dalam Open3D
```python
import open3d as o3d

mesh = ...  # Your mesh
# Write compressed
o3d.io.write_triangle_mesh("output.ply", mesh, write_ascii=False, compressed=True)
```

---

## Advanced Topics

### Optimizing Large Point Cloud Processing

```python
import open3d as o3d

# 1. Downsample terlebih dahulu
pcd = o3d.io.read_point_cloud("large_cloud.ply")
pcd_down = pcd.voxel_down_sample(voxel_size=0.02)

# 2. Estimate normals dengan hybrid search
pcd_down.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30
    )
)

# 3. Perform reconstruction
mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd_down,
    depth=9
)

# 4. Optional: Simplify mesh
mesh_simp = mesh.simplify_quadric_mesh_decimation(
    target_count=50000
)
```

### Batch Processing Multiple Files

```python
from pathlib import Path
import open3d as o3d

# Process all PLY files in directory
for ply_file in Path("data").glob("*.ply"):
    pcd = o3d.io.read_point_cloud(str(ply_file))
    
    # Process...
    pcd.estimate_normals()
    
    # Save result
    output_file = Path("output") / f"{ply_file.stem}_processed.ply"
    o3d.io.write_point_cloud(str(output_file), pcd)
    
    print(f"✓ Processed {ply_file.name}")
```

---

## Reference Resources

### Online Documentation
- Open3D: http://www.open3d.org/docs/
- Point Cloud Library (PCL): https://pointclouds.org/documentation/
- Meshlab Tutorials: https://www.meshlab.net/

### Research Papers
- "Poisson Surface Reconstruction" (Kazhdan et al., 2006)
- "The Ball Pivoting Algorithm for Surface Reconstruction" (Bernardini et al., 1999)
- "A Method for Registration of 3-D Shapes" (Besl & McKay, 1992) - ICP

### Tools & Viewers
- CloudCompare: https://www.cloudcompare.org/
- Meshlab: https://www.meshlab.net/
- Blender: https://www.blender.org/

---

## Summary

Module ini menyediakan:
- ✅ **7 program praktikum** dengan kompleksitas bertingkat
- ✅ **Komprehensif materi teori** dengan ilustrasi visual
- ✅ **Real-world applications** (Industrial, Medical, Heritage)
- ✅ **Otomatis testing suite** untuk verifikasi
- ✅ **Detailed output files** untuk analisis

**Total Learning Time:** ~8-10 jam praktikum
**Hands-on Projects:** 3 individual projects + 1 final project

---

## Contact & Support

Jika mengalami masalah atau memiliki pertanyaan:
1. Check Troubleshooting section
2. Review relevant Materi.md sections
3. Consult Jobsheet.md untuk langkah-langkah detail
4. Examine program source code dengan inline comments

**Last Updated:** 2026-02-05
**Version:** 1.0
