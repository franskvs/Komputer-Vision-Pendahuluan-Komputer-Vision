# Tugas Bab 14: Image-Based Rendering

## Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 14 - Image-Based Rendering
- **Kompetensi**: Mampu mengimplementasikan dan menganalisis teknik image-based rendering

---

## Tugas 1: View Interpolation dan Morphing (Bobot: 20%)

### Deskripsi
Implementasikan sistem view interpolation untuk membuat transisi smooth antara dua viewpoints.

### Requirements

1. **Feature Correspondence** (5 poin)
   - Automatic feature detection dan matching
   - Manual correspondence refinement
   - Outlier rejection
   
   ```python
   class ViewInterpolation:
       def find_correspondences(self, img1, img2, method='sift'):
           """Find matching points between views."""
           pass
       
       def refine_matches(self, pts1, pts2, img1, img2):
           """Refine matches using geometric constraints."""
           pass
   ```

2. **Triangle Mesh Warping** (7 poin)
   ```python
   def create_mesh(self, points, image_shape):
       """Create triangulation dari correspondence points."""
       pass
   
   def warp_mesh(self, image, src_pts, dst_pts, triangles):
       """Warp image berdasarkan mesh transformation."""
       pass
   ```

3. **Morphing dengan Blending** (5 poin)
   - Cross-dissolve blending
   - Feature-line based blending
   - Multi-scale blending

4. **Video Generation** (3 poin)
   - Generate smooth video sequence
   - Frame interpolation
   - Export ke video file

### Eksperimen
1. Test dengan face morphing
2. Test dengan scene views
3. Compare blending methods
4. Analyze correspondence quality impact

### Deliverables
1. Complete morphing implementation
2. Sample video outputs
3. Analysis report
4. Comparison dengan simple blending

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Feature matching | 25 |
| Mesh warping | 30 |
| Blending quality | 25 |
| Video generation | 10 |
| Documentation | 10 |

---

## Tugas 2: Light Field Capture dan Rendering (Bobot: 25%)

### Deskripsi
Implementasikan sistem light field capture dan rendering untuk novel view synthesis.

### Requirements

1. **Light Field Acquisition** (8 poin)
   ```python
   class LightFieldCapture:
       def __init__(self, grid_size=(5, 5)):
           """Initialize light field dengan grid configuration."""
           pass
       
       def capture_from_video(self, video_path, method='grid'):
           """Extract light field dari video."""
           pass
       
       def capture_from_images(self, image_folder, positions=None):
           """Load light field dari image collection."""
           pass
   ```

2. **Light Field Representation** (5 poin)
   - Two-plane parameterization
   - Sub-aperture images
   - Efficient storage format

3. **Novel View Synthesis** (8 poin)
   ```python
   class LightFieldRenderer:
       def render_view(self, u, v, s, t, method='bilinear'):
           """Render view at specified coordinates."""
           pass
       
       def render_focal_stack(self, focus_distance):
           """Render images focused at different depths."""
           pass
       
       def refocus(self, target_depth):
           """Digital refocusing."""
           pass
   ```

4. **Depth Estimation dari Light Field** (4 poin)
   - Disparity estimation
   - Depth map generation
   - Confidence map

### Dataset
- Stanford Light Field Archive
- Atau capture sendiri (turntable + camera)

### Deliverables
1. Light field capture/loading system
2. Interactive viewer untuk novel views
3. Refocusing demo
4. Depth estimation results

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Capture system | 25 |
| Storage/representation | 15 |
| Novel view rendering | 35 |
| Depth estimation | 15 |
| Documentation | 10 |

---

## Tugas 3: DIBR (Depth Image-Based Rendering) (Bobot: 25%)

### Deskripsi
Implementasikan DIBR pipeline untuk novel view synthesis dari RGB-D images.

### Requirements

1. **Forward Warping** (8 poin)
   ```python
   class DIBR:
       def forward_warp(self, rgb, depth, K, R, t):
           """
           Forward warp RGB-D ke novel viewpoint.
           Handle z-buffer dan splatting.
           """
           pass
       
       def backward_warp(self, target_depth, rgb, depth, K, R, t):
           """
           Backward warp menggunakan target depth.
           """
           pass
   ```

2. **Hole Filling** (7 poin)
   - Background extrapolation
   - Inpainting
   - Multi-layer approach
   
   ```python
   def fill_holes(self, warped_image, warped_depth, method='inpaint'):
       """Fill disocclusion holes."""
       pass
   
   def depth_based_inpaint(self, image, depth, mask):
       """Depth-aware inpainting."""
       pass
   ```

3. **Multi-View Fusion** (6 poin)
   ```python
   def fuse_views(self, views_data, target_pose):
       """
       Fuse multiple warped views.
       
       Args:
           views_data: List of (rgb, depth, pose) tuples
           target_pose: Target camera pose
           
       Returns:
           Fused novel view
       """
       pass
   ```

4. **Quality Enhancement** (4 poin)
   - Edge-aware filtering
   - Temporal consistency
   - Anti-aliasing

### Dataset
- NYU Depth V2 (RGB-D)
- TUM RGB-D Dataset
- Atau synthetic data

### Deliverables
1. Complete DIBR pipeline
2. Comparison of hole-filling methods
3. Multi-view fusion results
4. Quality analysis

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Forward warping | 25 |
| Hole filling | 30 |
| Multi-view fusion | 25 |
| Quality enhancement | 10 |
| Documentation | 10 |

---

## Tugas 4: Panorama dan 360° Rendering (Bobot: 30%)

### Deskripsi
Bangun sistem untuk create dan render 360° panoramic content.

### Requirements

1. **Panorama Stitching** (10 poin)
   ```python
   class PanoramaCreator:
       def stitch_images(self, images, mode='cylindrical'):
           """
           Stitch images ke panorama.
           
           Args:
               images: List of overlapping images
               mode: 'cylindrical', 'spherical', 'perspective'
               
           Returns:
               Stitched panorama
           """
           pass
       
       def bundle_adjust(self, images, homographies):
           """Global optimization untuk alignment."""
           pass
   ```

2. **Spherical Projection** (8 poin)
   ```python
   class SphericalProjection:
       def equirectangular_to_cubemap(self, equirect):
           """Convert equirectangular ke cube map."""
           pass
       
       def cubemap_to_equirectangular(self, cubemap):
           """Convert cube map ke equirectangular."""
           pass
       
       def render_perspective(self, equirect, fov, yaw, pitch):
           """Render perspective view dari panorama."""
           pass
   ```

3. **Interactive Viewer** (7 poin)
   - Mouse/keyboard navigation
   - Zoom in/out
   - VR-ready output (optional)
   
   ```python
   class PanoramaViewer:
       def __init__(self, panorama):
           pass
       
       def look_at(self, yaw, pitch, fov):
           """Render view looking at direction."""
           pass
       
       def run_interactive(self):
           """Run interactive viewing session."""
           pass
   ```

4. **Virtual Tour** (5 poin)
   - Multiple panorama nodes
   - Navigation hotspots
   - Smooth transitions

### Eksperimen
1. Create panorama dari image sequence
2. Test berbagai projection modes
3. Build simple virtual tour
4. Measure stitching quality

### Deliverables
1. Panorama creation tool
2. Interactive viewer
3. Sample virtual tour
4. Quality analysis report

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Stitching quality | 30 |
| Projection conversions | 25 |
| Interactive viewer | 25 |
| Virtual tour | 10 |
| Documentation | 10 |

---

## Proyek Akhir: Neural View Synthesis Application (Bonus: 25%)

### Deskripsi
Implementasikan neural view synthesis menggunakan modern techniques.

### Pilihan Proyek

#### Opsi 1: Multi-Plane Image (MPI) Renderer
- Learn MPI dari stereo pairs
- Render novel views dengan alpha compositing
- Real-time rendering

#### Opsi 2: Simple NeRF Implementation
- Basic NeRF architecture
- Volume rendering
- Novel view synthesis

#### Opsi 3: Image-Based Relighting
- Capture dengan varying lighting
- Relight dari novel directions
- Material estimation

#### Opsi 4: Free-Viewpoint Video
- Multi-camera capture
- Temporal consistency
- Interactive playback

### Technical Requirements

**Untuk MPI:**
```python
class MPIRenderer:
    def __init__(self, n_planes=32):
        pass
    
    def predict_mpi(self, reference_view):
        """Predict MPI dari single view."""
        pass
    
    def render_novel_view(self, mpi, target_pose):
        """Render view dari MPI."""
        pass
```

**Untuk NeRF:**
```python
class SimpleNeRF(nn.Module):
    def __init__(self):
        # Positional encoding
        # MLP layers
        pass
    
    def forward(self, positions, directions):
        """Returns (rgb, density)."""
        pass

def render_rays(model, rays_o, rays_d, near, far, n_samples):
    """Volume rendering."""
    pass
```

### Minimum Requirements
1. Novel view synthesis capability
2. Reasonable quality output
3. Documentation
4. Demo video

### Deliverables
1. Trained model atau implementation
2. Inference code
3. Sample outputs
4. Technical report
5. Demo video

### Kriteria Penilaian
| Aspek | Poin |
|-------|------|
| Technical implementation | 35 |
| Quality of results | 30 |
| Innovation/creativity | 15 |
| Documentation | 10 |
| Demo presentation | 10 |

---

## Panduan Pengerjaan

### Environment Setup
```bash
# Create environment
conda create -n ibr python=3.8
conda activate ibr

# Core dependencies
pip install numpy scipy matplotlib opencv-contrib-python

# Deep learning (untuk bonus)
pip install torch torchvision

# Visualization
pip install pygame  # untuk interactive viewer
pip install pyopengl  # untuk 3D rendering
```

### Useful Resources

| Library | Purpose |
|---------|---------|
| OpenCV | Stitching, warping |
| PyGame | Interactive viewer |
| PyOpenGL | 3D rendering |
| PyTorch | Neural methods |
| Open3D | Point cloud rendering |

### Tips
1. Start dengan synthetic data untuk testing
2. Validate warping mathematics carefully
3. Handle edge cases (holes, boundaries)
4. Profile performance untuk real-time
5. Use existing implementations as reference

---

## Jadwal Pengumpulan

| Tugas | Deadline | Platform |
|-------|----------|----------|
| Tugas 1 | Minggu 14 | GitHub Classroom |
| Tugas 2 | Minggu 15 | GitHub Classroom |
| Tugas 3 | Minggu 16 | GitHub Classroom |
| Tugas 4 | Minggu 17 | GitHub Classroom |
| Proyek Bonus | Minggu 18 | Presentasi + Demo |

---

## Referensi
1. Szeliski - "Computer Vision: Algorithms and Applications", Chapter 13-14
2. Levoy & Hanrahan - "Light Field Rendering"
3. Seitz & Dyer - "View Morphing"
4. Shum & Kang - "A Review of IBR Techniques"
5. Mildenhall et al. - "NeRF"
