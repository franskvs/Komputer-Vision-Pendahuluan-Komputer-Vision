# Tugas Bab 12: Depth Estimation

## Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 12 - Depth Estimation
- **Kompetensi**: Mampu mengimplementasikan dan menganalisis berbagai teknik estimasi kedalaman

---

## Tugas 1: Implementasi Block Matching Stereo (Bobot: 20%)

### Deskripsi
Implementasikan algoritma stereo matching menggunakan berbagai cost functions dan bandingkan hasilnya.

### Requirements

1. **Cost Functions** (10 poin)
   Implementasikan cost function berikut:
   - Sum of Absolute Differences (SAD)
   - Sum of Squared Differences (SSD)
   - Normalized Cross-Correlation (NCC)
   - Census Transform
   
   ```python
   class StereoMatcher:
       def __init__(self, block_size, num_disparities):
           pass
       
       def sad_cost(self, left, right, x, y, d):
           """Compute SAD cost at pixel (x,y) for disparity d."""
           pass
       
       def ssd_cost(self, left, right, x, y, d):
           """Compute SSD cost."""
           pass
       
       def ncc_cost(self, left, right, x, y, d):
           """Compute NCC cost."""
           pass
       
       def census_cost(self, left, right, x, y, d):
           """Compute Census/Hamming cost."""
           pass
   ```

2. **Subpixel Refinement** (5 poin)
   Implementasikan subpixel accuracy:
   - Quadratic interpolation pada disparity
   - Equiangular atau symmetric interpolation
   
3. **Left-Right Consistency Check** (5 poin)
   - Compute disparity dari left→right dan right→left
   - Mark inconsistent pixels sebagai occlusion

### Dataset
Gunakan salah satu dari:
- Middlebury Stereo Dataset (2014)
- KITTI Stereo Benchmark
- Atau buat synthetic stereo pair

### Deliverables
1. Source code dengan dokumentasi
2. Visualisasi disparity map untuk setiap cost function
3. Analisis perbandingan (tabel metrik: error rate, runtime)
4. Occlusion mask hasil LR check

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Correctness of cost functions | 40 |
| Subpixel refinement | 20 |
| LR consistency check | 20 |
| Visualisasi dan analisis | 20 |

---

## Tugas 2: Semi-Global Matching (Bobot: 25%)

### Deskripsi
Implementasikan algoritma SGM (Semi-Global Matching) untuk stereo correspondence.

### Requirements

1. **Cost Volume Computation** (5 poin)
   ```python
   def compute_cost_volume(left, right, max_disp, method='census'):
       """
       Compute 3D cost volume C(x, y, d).
       
       Returns:
           np.ndarray: Shape (H, W, D)
       """
       pass
   ```

2. **Path Aggregation** (10 poin)
   Implementasikan cost aggregation untuk:
   - Minimum 4 paths (horizontal & vertical)
   - Idealnya 8 paths (termasuk diagonal)
   - 16 paths untuk hasil terbaik (optional)
   
   ```python
   def aggregate_path(cost_volume, direction, P1, P2):
       """
       Aggregate cost sepanjang satu path.
       
       Args:
           cost_volume: Initial cost (H, W, D)
           direction: (dy, dx)
           P1: Small disparity penalty
           P2: Large disparity penalty
           
       Returns:
           Aggregated cost volume
       """
       pass
   
   def sgm_aggregate(cost_volume, num_paths=8, P1=10, P2=120):
       """
       Full SGM aggregation.
       
       Returns:
           Sum of aggregated costs dari semua paths
       """
       pass
   ```

3. **Disparity Computation** (5 poin)
   - Winner-take-all selection
   - Uniqueness check
   - Speckle filtering

4. **Parameter Tuning** (5 poin)
   - Eksperimen dengan P1 dan P2
   - Analisis pengaruh parameter terhadap hasil

### Eksperimen
1. Bandingkan SGM 4-path vs 8-path vs 16-path
2. Analisis runtime vs quality trade-off
3. Compare dengan OpenCV StereoSGBM

### Deliverables
1. Implementasi SGM lengkap
2. Perbandingan dengan berbagai konfigurasi path
3. Grafik error rate vs runtime
4. Analisis parameter sensitivity

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Cost volume computation | 15 |
| Path aggregation (correctness) | 30 |
| Multi-path implementation | 25 |
| Parameter analysis | 15 |
| Dokumentasi dan visualisasi | 15 |

---

## Tugas 3: Depth Fusion dan Processing (Bobot: 25%)

### Deskripsi
Implementasikan pipeline untuk processing dan fusion depth maps dari multiple sources.

### Requirements

1. **Depth Map Refinement** (10 poin)
   ```python
   class DepthRefinement:
       def fill_holes(self, depth, method='interpolate'):
           """Fill invalid/missing depth values."""
           pass
       
       def bilateral_filter(self, depth, guide=None, sigma_s=5, sigma_r=0.1):
           """Edge-preserving bilateral filtering."""
           pass
       
       def guided_filter(self, depth, guide, r=4, eps=0.01):
           """Guided filter for depth refinement."""
           pass
       
       def temporal_filter(self, depth_buffer, weights=None):
           """Temporal filtering untuk video depth."""
           pass
   ```

2. **Multi-View Depth Fusion** (8 poin)
   ```python
   def fuse_depth_maps(depth_maps, poses, intrinsics, method='tsdf'):
       """
       Fuse multiple depth maps ke 3D representation.
       
       Args:
           depth_maps: List of depth images
           poses: Camera poses untuk setiap view
           intrinsics: Camera intrinsic matrix
           method: 'tsdf' atau 'point_fusion'
           
       Returns:
           Fused 3D representation
       """
       pass
   ```

3. **Depth-to-PointCloud Conversion** (4 poin)
   - Back-projection ke 3D coordinates
   - Support colored point clouds
   - Export ke PLY format

4. **Surface Normal Computation** (3 poin)
   - Compute normals dari depth gradients
   - Handle depth discontinuities

### Eksperimen
1. Test pada depth map dengan berbagai noise level
2. Compare different filtering methods
3. Fuse depth maps dari multi-view untuk simple scene

### Deliverables
1. Complete depth processing pipeline
2. Point cloud output (PLY files)
3. Comparison of filtering methods
4. Fused 3D reconstruction demo

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Hole filling methods | 20 |
| Filtering implementations | 25 |
| Depth fusion | 25 |
| Point cloud generation | 15 |
| Documentation | 15 |

---

## Tugas 4: Monocular Depth Estimation System (Bobot: 30%)

### Deskripsi
Bangun sistem monocular depth estimation menggunakan deep learning.

### Requirements

1. **Dataset Preparation** (5 poin)
   - Download dan preprocess NYU Depth V2 atau KITTI subset
   - Data augmentation pipeline
   - Train/val/test split

2. **Model Implementation** (15 poin)
   
   Pilih salah satu:
   
   **Opsi A: Encoder-Decoder dari Scratch**
   ```python
   class MonoDepthNet(nn.Module):
       def __init__(self):
           super().__init__()
           # Encoder (ResNet-like atau EfficientNet)
           self.encoder = ...
           
           # Decoder dengan skip connections
           self.decoder = ...
           
       def forward(self, x):
           # Multi-scale features
           features = self.encoder(x)
           
           # Decode ke depth
           depth = self.decoder(features)
           
           return depth
   ```
   
   **Opsi B: Fine-tune Pretrained Model**
   - Gunakan MiDaS atau DPT dari torch.hub
   - Fine-tune pada custom dataset
   
   **Opsi C: Self-Supervised Training**
   - Implement photometric loss
   - Smoothness loss
   - Training dengan video sequences

3. **Loss Functions** (5 poin)
   ```python
   def depth_loss(pred, target, mask=None):
       """
       Compute depth estimation loss.
       
       Components:
       - L1/L2 loss
       - Scale-invariant loss
       - Gradient matching loss
       - SSIM loss
       """
       pass
   
   def photometric_loss(source, target, depth, pose, intrinsics):
       """Self-supervised photometric loss."""
       pass
   ```

4. **Evaluation Metrics** (5 poin)
   Implement dan report:
   - Absolute Relative Error (AbsRel)
   - Squared Relative Error (SqRel)
   - RMSE dan RMSE log
   - δ < 1.25, δ < 1.25², δ < 1.25³

### Pipeline
```
Input Image → Preprocessing → Neural Network → Post-processing → Depth Map
                                   ↓
                           Multi-scale Output
                                   ↓
                            Refinement
```

### Deliverables
1. Training script dan config
2. Trained model checkpoint
3. Inference script untuk single image
4. Evaluation results pada test set
5. Demo video (optional)

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Dataset preparation | 10 |
| Model architecture | 30 |
| Loss functions | 15 |
| Training pipeline | 15 |
| Evaluation dan analysis | 20 |
| Code quality | 10 |

---

## Proyek Akhir: Real-Time Depth Sensing Application (Bonus: 20%)

### Deskripsi
Bangun aplikasi real-time yang memanfaatkan depth estimation.

### Pilihan Proyek

#### Opsi 1: AR Distance Measurement
- Real-time depth estimation dari webcam
- Point-and-measure distance
- Display overlay dengan measurements

#### Opsi 2: Depth-Based Video Effects
- Portrait mode (background blur)
- Depth-based color grading
- 3D photo effect

#### Opsi 3: Simple 3D Scanner
- Capture depth dari multiple angles
- Fuse ke point cloud
- Basic surface reconstruction

#### Opsi 4: Obstacle Detection untuk Robot
- Real-time depth processing
- Obstacle detection dan distance
- Navigation suggestions

### Minimum Requirements
1. Real-time processing (minimal 10 FPS)
2. GUI untuk interaksi
3. Save/export hasil
4. Dokumentasi penggunaan

### Deliverables
1. Working application dengan source code
2. Demo video (2-3 menit)
3. User guide
4. Technical documentation

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Functionality | 30 |
| Real-time performance | 25 |
| User interface | 20 |
| Documentation | 15 |
| Creativity | 10 |

---

## Panduan Pengerjaan

### Environment Setup
```bash
# Create environment
conda create -n depth_estimation python=3.8
conda activate depth_estimation

# Install dependencies
pip install opencv-contrib-python numpy matplotlib scipy
pip install torch torchvision  # untuk deep learning
pip install open3d  # untuk point cloud visualization
pip install timm  # untuk pretrained models
```

### Dataset Resources
1. **Middlebury Stereo**: https://vision.middlebury.edu/stereo/data/
2. **KITTI Depth**: https://www.cvlibs.net/datasets/kitti/eval_depth.php
3. **NYU Depth V2**: https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
4. **ETH3D**: https://www.eth3d.net/datasets

### Pretrained Models
1. **MiDaS**: https://github.com/isl-org/MiDaS
2. **DPT**: https://github.com/isl-org/DPT
3. **Monodepth2**: https://github.com/nianticlabs/monodepth2

### Tips
1. Mulai dengan synthetic data untuk debugging
2. Gunakan pretrained models untuk hasil cepat
3. Perhatikan scaling depth (absolute vs relative)
4. Profile runtime untuk optimisasi

---

## Jadwal Pengumpulan

| Tugas | Deadline | Platform |
|-------|----------|----------|
| Tugas 1 | Minggu 12 | GitHub Classroom |
| Tugas 2 | Minggu 13 | GitHub Classroom |
| Tugas 3 | Minggu 14 | GitHub Classroom |
| Tugas 4 | Minggu 15 | GitHub Classroom + Demo |
| Proyek Bonus | Minggu 16 | Presentasi + Report |

---

## Referensi
1. Scharstein & Szeliski - "A Taxonomy of Stereo Matching"
2. Hirschmuller - "SGM Paper"
3. Eigen et al. - "Depth Prediction from Single Image"
4. Godard et al. - "Monodepth"
5. Ranftl et al. - "MiDaS"
