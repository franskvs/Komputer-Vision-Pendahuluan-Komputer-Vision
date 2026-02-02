# Tugas Bab 13: 3D Reconstruction

## Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 13 - 3D Reconstruction
- **Kompetensi**: Mampu mengimplementasikan dan menganalisis berbagai teknik rekonstruksi 3D

---

## Tugas 1: Point Cloud Processing Pipeline (Bobot: 20%)

### Deskripsi
Implementasikan pipeline lengkap untuk processing point cloud dari raw data sampai clean output.

### Requirements

1. **Point Cloud I/O** (5 poin)
   - Load dari format PLY, PCD, XYZ
   - Save ke format PLY dan PCD
   - Support untuk color dan normal data
   
   ```python
   class PointCloudIO:
       @staticmethod
       def load(filename: str) -> PointCloud:
           """Load point cloud dari berbagai format."""
           pass
       
       @staticmethod
       def save(pc: PointCloud, filename: str, format: str = 'ply'):
           """Save point cloud ke file."""
           pass
   ```

2. **Normal Estimation** (5 poin)
   Implementasikan normal estimation dengan berbagai metode:
   - PCA-based (k-nearest neighbors)
   - Radius-based
   - Consistent normal orientation
   
   ```python
   def estimate_normals_pca(points: np.ndarray, k: int = 20) -> np.ndarray:
       """PCA-based normal estimation."""
       pass
   
   def orient_normals_consistently(points: np.ndarray, normals: np.ndarray) -> np.ndarray:
       """Make normals consistent (all pointing outward)."""
       pass
   ```

3. **Filtering dan Cleaning** (5 poin)
   - Statistical outlier removal
   - Radius outlier removal
   - Voxel grid downsampling
   - Bilateral filtering untuk noise

4. **Registration** (5 poin)
   Implementasikan point cloud registration:
   - Coarse alignment (feature-based)
   - Fine alignment (ICP)
   
   ```python
   def icp(source: np.ndarray, target: np.ndarray, 
           max_iterations: int = 50) -> Tuple[np.ndarray, float]:
       """
       Iterative Closest Point algorithm.
       
       Returns:
           transformation: 4x4 transformation matrix
           error: Final RMS error
       """
       pass
   ```

### Dataset
- Stanford 3D Scanning Repository
- Atau scan object sendiri menggunakan smartphone app

### Deliverables
1. Complete point cloud processing library
2. Demo script dengan berbagai test cases
3. Visualisasi hasil di setiap stage
4. Dokumentasi API

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| I/O implementation | 20 |
| Normal estimation | 25 |
| Filtering methods | 25 |
| ICP registration | 20 |
| Documentation | 10 |

---

## Tugas 2: Surface Reconstruction (Bobot: 25%)

### Deskripsi
Implementasikan berbagai algoritma surface reconstruction dari point cloud.

### Requirements

1. **Marching Cubes (Full)** (10 poin)
   Implementasi lengkap dengan lookup tables:
   
   ```python
   class MarchingCubes:
       # Full edge table (256 entries)
       EDGE_TABLE = [...]
       
       # Full triangle table
       TRI_TABLE = [...]
       
       def extract_surface(self, volume: np.ndarray, 
                          isovalue: float = 0.0) -> TriangleMesh:
           """
           Full marching cubes implementation.
           """
           pass
       
       def _interpolate_vertex(self, v1: np.ndarray, v2: np.ndarray,
                               val1: float, val2: float, 
                               isovalue: float) -> np.ndarray:
           """Linear interpolation untuk vertex position."""
           pass
   ```

2. **Ball Pivoting Algorithm** (7 poin)
   ```python
   def ball_pivoting(points: np.ndarray, normals: np.ndarray,
                     radius: float) -> TriangleMesh:
       """
       Ball pivoting surface reconstruction.
       
       Args:
           points: Nx3 point positions
           normals: Nx3 point normals
           radius: Ball radius
           
       Returns:
           Triangle mesh
       """
       pass
   ```

3. **Poisson Reconstruction (Simplified)** (8 poin)
   ```python
   def poisson_reconstruction(points: np.ndarray, normals: np.ndarray,
                              depth: int = 8) -> TriangleMesh:
       """
       Simplified Poisson surface reconstruction.
       """
       pass
   ```

### Eksperimen
1. Compare hasil dari berbagai metode
2. Analisis pengaruh parameter (radius, depth, resolution)
3. Test dengan point clouds berbeda (clean vs noisy)

### Deliverables
1. Implementation semua algoritma
2. Comparison study dengan metrics (Chamfer, Hausdorff)
3. Visual comparison gallery
4. Analysis report

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Marching Cubes (full) | 30 |
| Ball Pivoting | 25 |
| Poisson (simplified) | 25 |
| Comparison analysis | 20 |

---

## Tugas 3: Multi-View 3D Reconstruction (Bobot: 25%)

### Deskripsi
Bangun pipeline rekonstruksi 3D dari multiple images.

### Requirements

1. **Camera Calibration** (5 poin)
   - Intrinsic calibration menggunakan checkerboard
   - Extrinsic estimation (PnP)
   
   ```python
   def calibrate_camera(images: List[np.ndarray], 
                        pattern_size: Tuple[int, int],
                        square_size: float) -> Tuple[np.ndarray, np.ndarray]:
       """
       Returns:
           K: 3x3 intrinsic matrix
           dist: Distortion coefficients
       """
       pass
   ```

2. **Dense Stereo** (8 poin)
   - Implement atau gunakan StereoSGBM
   - Depth map ke point cloud conversion
   - Multi-baseline stereo (3+ views)

3. **Depth Map Fusion** (7 poin)
   ```python
   class DepthFusion:
       def __init__(self, volume_size, resolution):
           pass
       
       def integrate(self, depth_map, rgb, pose, intrinsics):
           """Integrate satu depth map."""
           pass
       
       def extract_mesh(self) -> TriangleMesh:
           """Extract final mesh."""
           pass
   ```

4. **Texture Mapping** (5 poin)
   ```python
   def texture_mesh(mesh: TriangleMesh, images: List[np.ndarray],
                    cameras: List[Dict]) -> TriangleMesh:
       """
       Apply texture ke mesh dari multiple views.
       """
       pass
   ```

### Pipeline
```
Multi-View Images → Calibration → Depth Estimation → Fusion → Mesh → Texturing
```

### Dataset
- DTU Dataset (subset)
- Tanks and Temples (subset)
- Atau capture sendiri

### Deliverables
1. Complete MVS pipeline
2. Hasil rekonstruksi untuk minimal 2 scenes
3. Comparison dengan ground truth (jika ada)
4. Performance analysis

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Camera calibration | 15 |
| Dense stereo | 30 |
| Depth fusion | 30 |
| Texture mapping | 15 |
| Documentation | 10 |

---

## Tugas 4: Neural 3D Reconstruction (Bobot: 30%)

### Deskripsi
Implementasikan neural network-based 3D reconstruction.

### Requirements

1. **Simple Occupancy Network** (12 poin)
   ```python
   class OccupancyNetwork(nn.Module):
       def __init__(self, latent_dim=256):
           super().__init__()
           # Encoder (process input - e.g., point cloud)
           self.encoder = ...
           
           # Decoder (predict occupancy)
           self.decoder = nn.Sequential(
               nn.Linear(3 + latent_dim, 256),
               nn.ReLU(),
               nn.Linear(256, 256),
               nn.ReLU(),
               nn.Linear(256, 1),
               nn.Sigmoid()
           )
       
       def forward(self, query_points, shape_code):
           """
           Args:
               query_points: Bx3 query coordinates
               shape_code: Latent representation
               
           Returns:
               Occupancy probability (0-1)
           """
           pass
   ```

2. **Training Pipeline** (8 poin)
   - Data loading (ShapeNet subset)
   - Occupancy sampling (inside/outside points)
   - Training loop dengan loss
   - Evaluation metrics

3. **Inference dan Mesh Extraction** (5 poin)
   - Encode shape ke latent space
   - Query occupancy di regular grid
   - Marching cubes untuk mesh extraction

4. **Optional: Simple NeRF** (5 poin bonus)
   ```python
   class SimpleNeRF(nn.Module):
       def __init__(self):
           super().__init__()
           # MLP
           self.mlp = ...
       
       def forward(self, positions, directions):
           """
           Returns:
               rgb: Color (Nx3)
               sigma: Density (Nx1)
           """
           pass
   
   def render_ray(model, ray_origin, ray_direction, near, far, n_samples):
       """Volume rendering along a ray."""
       pass
   ```

### Dataset
- ShapeNet (subset - chairs, airplanes)
- Synthetic data untuk NeRF

### Deliverables
1. Trained occupancy network
2. Inference script
3. Reconstructed meshes
4. Training curves dan metrics
5. (Bonus) Simple NeRF dengan view synthesis

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Network architecture | 25 |
| Training pipeline | 25 |
| Mesh extraction | 20 |
| Results quality | 20 |
| Documentation | 10 |
| Bonus NeRF | +20 |

---

## Proyek Akhir: 3D Scanning System (Bonus: 20%)

### Deskripsi
Bangun sistem 3D scanning lengkap dari capture sampai textured mesh.

### Pilihan Proyek

#### Opsi 1: Turntable 3D Scanner
- Setup webcam + turntable
- Auto-capture pada interval rotasi
- Full reconstruction pipeline
- Interactive viewer

#### Opsi 2: Smartphone 3D Scanner
- Guide user untuk capture
- SLAM/odometry untuk camera poses
- Real-time preview
- Cloud processing

#### Opsi 3: Structured Light Scanner
- Projector + camera setup
- Gray code pattern projection
- Dense depth dari correspondence
- High-quality mesh output

#### Opsi 4: Multi-View Photogrammetry Tool
- Drag-and-drop image input
- Automatic SfM + MVS
- Progress visualization
- Export ke berbagai format

### Minimum Requirements
1. End-to-end pipeline dari input ke output
2. GUI untuk user interaction
3. Hasil mesh yang reasonable
4. Export ke OBJ/PLY
5. Documentation

### Deliverables
1. Complete application source code
2. User manual
3. Demo video
4. Sample outputs

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Functionality | 30 |
| Reconstruction quality | 30 |
| User interface | 20 |
| Documentation | 10 |
| Creativity | 10 |

---

## Panduan Pengerjaan

### Environment Setup
```bash
# Create environment
conda create -n reconstruction python=3.8
conda activate reconstruction

# Core dependencies
pip install numpy scipy matplotlib opencv-contrib-python

# 3D processing
pip install open3d trimesh pymeshlab

# Deep learning
pip install torch torchvision

# Optional
pip install pyvista  # visualization
pip install pyrender  # rendering
```

### Useful Libraries

| Library | Purpose |
|---------|---------|
| Open3D | Point cloud, mesh, RGBD |
| Trimesh | Mesh processing |
| PyMeshLab | Mesh algorithms |
| COLMAP (CLI) | SfM + MVS |
| PyTorch3D | Differentiable rendering |

### Tips
1. Start dengan synthetic data untuk validation
2. Visualize intermediate results
3. Use existing implementations untuk reference
4. Test dengan simple shapes first
5. Profile memory untuk large scenes

---

## Jadwal Pengumpulan

| Tugas | Deadline | Platform |
|-------|----------|----------|
| Tugas 1 | Minggu 13 | GitHub Classroom |
| Tugas 2 | Minggu 14 | GitHub Classroom |
| Tugas 3 | Minggu 15 | GitHub Classroom |
| Tugas 4 | Minggu 16 | GitHub Classroom + Demo |
| Proyek Bonus | Minggu 17 | Presentasi + Report |

---

## Referensi
1. Szeliski - "Computer Vision: Algorithms and Applications", Chapter 12-13
2. Kazhdan et al. - "Poisson Surface Reconstruction"
3. Mescheder et al. - "Occupancy Networks"
4. Mildenhall et al. - "NeRF"
5. Open3D Documentation
