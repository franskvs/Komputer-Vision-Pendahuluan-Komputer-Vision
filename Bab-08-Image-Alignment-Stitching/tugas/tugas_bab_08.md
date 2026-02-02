# Tugas Bab 8: Image Alignment dan Stitching

## 📋 Informasi Umum

| Item | Keterangan |
|------|------------|
| **Topik** | Image Alignment dan Stitching |
| **Tujuan** | Memahami dan mengimplementasikan teknik alignment dan panorama |
| **Prasyarat** | Bab 7 (Feature Detection), Linear Algebra |
| **Estimasi Waktu** | 4-5 jam |

---

## 📝 Tugas 1: Implementasi Direct Linear Transform (DLT)

### Deskripsi
Implementasikan algoritma DLT untuk estimasi homography dari scratch (tanpa `cv2.findHomography`).

### Spesifikasi

```python
class DLTHomography:
    """
    Direct Linear Transform untuk homography estimation.
    """
    
    def normalize_points(self, points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Normalisasi titik untuk numerical stability.
        
        Transformasi:
        1. Translate centroid ke origin
        2. Scale agar average distance dari origin = sqrt(2)
        
        Args:
            points: Nx2 array of points
            
        Returns:
            normalized_points: Titik ternormalisasi
            T: 3x3 normalization matrix
        """
        pass
    
    def build_matrix_A(self, src_pts: np.ndarray, dst_pts: np.ndarray) -> np.ndarray:
        """
        Bangun matrix A untuk DLT.
        
        Untuk setiap korespondensi:
        [-x, -y, -1, 0, 0, 0, x'x, x'y, x']
        [0, 0, 0, -x, -y, -1, y'x, y'y, y']
        
        Args:
            src_pts: Source points (Nx2)
            dst_pts: Destination points (Nx2)
            
        Returns:
            A: 2Nx9 coefficient matrix
        """
        pass
    
    def compute_homography(self, src_pts: np.ndarray, dst_pts: np.ndarray) -> np.ndarray:
        """
        Compute homography menggunakan normalized DLT.
        
        Steps:
        1. Normalize source dan destination points
        2. Build matrix A
        3. Solve menggunakan SVD
        4. Denormalize H
        
        Args:
            src_pts: Source points (Nx2), N >= 4
            dst_pts: Destination points (Nx2)
            
        Returns:
            H: 3x3 homography matrix
        """
        pass
```

### Deliverables
1. Implementasi lengkap `DLTHomography`
2. Comparison dengan `cv2.findHomography`:
   - Numerical error
   - Reprojection error
3. Test dengan berbagai konfigurasi titik

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Normalisasi benar | 25% |
| Matrix A benar | 25% |
| SVD solution benar | 25% |
| Testing dan analisis | 25% |

---

## 📝 Tugas 2: Lucas-Kanade Template Tracker

### Deskripsi
Implementasikan Lucas-Kanade tracker untuk template tracking dengan inverse compositional approach.

### Spesifikasi

```python
class InverseCompositionalTracker:
    """
    Lucas-Kanade tracker dengan inverse compositional algorithm.
    
    Lebih efisien karena Hessian dan steepest descent dihitung sekali.
    """
    
    def __init__(self, template: np.ndarray, warp_type: str = 'translation'):
        """
        Initialize tracker dengan template.
        
        Args:
            template: Template image (grayscale)
            warp_type: 'translation', 'euclidean', atau 'affine'
        """
        self.template = template.astype(np.float32)
        self.warp_type = warp_type
        
        # Pre-compute (hanya sekali!)
        self._precompute()
    
    def _precompute(self):
        """
        Pre-compute:
        1. Gradient template
        2. Jacobian warp
        3. Steepest descent images
        4. Hessian
        """
        pass
    
    def _compute_jacobian(self, x: int, y: int) -> np.ndarray:
        """
        Compute Jacobian of warp function.
        
        Translation: [[1, 0], [0, 1]]
        Euclidean: [[1, 0, -y], [0, 1, x]]
        Affine: [[x, y, 0, 0, 1, 0], [0, 0, x, y, 0, 1]]
        """
        pass
    
    def track(self, image: np.ndarray, initial_warp: np.ndarray,
              max_iterations: int = 100, epsilon: float = 1e-4
              ) -> Tuple[np.ndarray, float]:
        """
        Track template dalam image.
        
        Args:
            image: Current frame
            initial_warp: Initial warp parameters
            max_iterations: Maximum iterations
            epsilon: Convergence threshold
            
        Returns:
            warp: Final warp parameters
            error: Final SSD error
        """
        pass
    
    def warp_image(self, image: np.ndarray, params: np.ndarray) -> np.ndarray:
        """Apply warp ke image."""
        pass
```

### Deliverables
1. Implementasi lengkap inverse compositional tracker
2. Demo tracking pada:
   - Synthetic sequence dengan known motion
   - Video/image sequence dengan object movement
3. Comparison dengan forward additive approach

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Pre-computation benar | 20% |
| Iteration loop benar | 30% |
| Convergence proper | 20% |
| Demo dan analisis | 30% |

---

## 📝 Tugas 3: Advanced Panorama Stitcher

### Deskripsi
Implementasikan panorama stitcher lengkap dengan bundle adjustment dan multi-band blending.

### Spesifikasi

```python
class AdvancedPanoramaStitcher:
    """
    Advanced panorama stitcher dengan:
    - Bundle adjustment
    - Exposure compensation
    - Multi-band blending
    - Automatic panorama recognition
    """
    
    def __init__(self, detector: str = 'SIFT'):
        self.detector = detector
    
    def find_matches(self, images: List[np.ndarray]
                    ) -> Dict[Tuple[int, int], List]:
        """
        Find pairwise matches antara semua gambar.
        
        Returns:
            Dictionary of (i, j) -> matches
        """
        pass
    
    def build_connectivity_graph(self, images: List[np.ndarray],
                                  min_matches: int = 30
                                  ) -> List[List[int]]:
        """
        Build graph konektivitas.
        
        Returns:
            Adjacency list
        """
        pass
    
    def estimate_focal_length(self, images: List[np.ndarray],
                              homographies: Dict) -> List[float]:
        """
        Estimate focal length untuk setiap gambar.
        
        Dari homography H antara dua gambar dengan rotation only:
        f² = (h₁₁ * h₁₂ + h₂₁ * h₂₂) / -(h₃₁² + h₃₂² - h₁₁² - h₂₁²)
        """
        pass
    
    def bundle_adjustment(self, images: List[np.ndarray],
                          initial_params: np.ndarray
                          ) -> np.ndarray:
        """
        Global bundle adjustment untuk refine cameras.
        
        Minimize total reprojection error across all images.
        """
        pass
    
    def exposure_compensation(self, images: List[np.ndarray],
                             masks: List[np.ndarray]
                             ) -> List[np.ndarray]:
        """
        Compensate exposure differences.
        
        Solve for gains g_i that minimize:
        sum_ij sum_overlap (g_i * I_i - g_j * I_j)²
        """
        pass
    
    def multiband_blend(self, warped_images: List[np.ndarray],
                        masks: List[np.ndarray],
                        num_bands: int = 5
                        ) -> np.ndarray:
        """
        Multi-band blending untuk seamless compositing.
        """
        pass
    
    def stitch(self, images: List[np.ndarray],
               projection: str = 'cylindrical'
               ) -> np.ndarray:
        """
        Full stitching pipeline.
        
        Args:
            images: Input images
            projection: 'planar', 'cylindrical', atau 'spherical'
            
        Returns:
            panorama: Final panorama
        """
        pass
```

### Dataset yang Disarankan
- Capture 5-10 overlapping images dari scene
- PASSTA dataset: http://www.wisdom.weizmann.ac.il/~bagon/matlab.html
- Test dengan handheld photos

### Deliverables
1. Implementasi lengkap panorama stitcher
2. Test dengan:
   - Minimal 5 gambar overlapping
   - Berbagai projection types
3. Comparison dengan OpenCV Stitcher
4. Analisis kegagalan dan solusi

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Feature matching dan graph | 20% |
| Bundle adjustment | 25% |
| Blending quality | 25% |
| End-to-end results | 30% |

---

## 📝 Tugas 4 (Proyek): Real-Time Video Mosaic

### Deskripsi
Implementasikan sistem real-time video mosaic yang membangun panorama secara incremental dari video feed.

### Spesifikasi

```python
class RealtimeVideoMosaic:
    """
    Real-time video mosaic builder.
    
    Features:
    - Incremental panorama building
    - Drift compensation
    - Memory-efficient implementation
    - Keyframe management
    """
    
    def __init__(self, canvas_size: Tuple[int, int] = (2000, 1000)):
        """
        Initialize mosaic builder.
        
        Args:
            canvas_size: Maximum canvas size (width, height)
        """
        self.canvas = None
        self.keyframes = []
        self.cumulative_homography = np.eye(3)
    
    def initialize(self, first_frame: np.ndarray):
        """Initialize mosaic dengan frame pertama."""
        pass
    
    def should_add_keyframe(self, frame: np.ndarray) -> bool:
        """
        Determine apakah perlu add keyframe baru.
        
        Criteria:
        - Sufficient visual overlap dengan last keyframe
        - Significant motion since last keyframe
        """
        pass
    
    def add_keyframe(self, frame: np.ndarray, H: np.ndarray):
        """Add new keyframe untuk drift correction."""
        pass
    
    def loop_closure_detection(self) -> Optional[Tuple[int, np.ndarray]]:
        """
        Detect jika current frame overlap dengan keyframe lama.
        
        Returns:
            (keyframe_idx, H) if loop closure detected
        """
        pass
    
    def correct_drift(self, loop_closure: Tuple[int, np.ndarray]):
        """Correct accumulated drift dengan loop closure."""
        pass
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process single frame dan update mosaic.
        
        Args:
            frame: New video frame
            
        Returns:
            Updated mosaic visualization
        """
        pass
    
    def get_mosaic(self) -> np.ndarray:
        """Get current mosaic."""
        return self.canvas


class MosaicVisualizer:
    """
    Visualizer untuk real-time mosaic.
    """
    
    def __init__(self, mosaic_builder: RealtimeVideoMosaic):
        self.builder = mosaic_builder
    
    def draw_trajectory(self, canvas: np.ndarray) -> np.ndarray:
        """Draw camera trajectory pada mosaic."""
        pass
    
    def draw_keyframes(self, canvas: np.ndarray) -> np.ndarray:
        """Highlight keyframe positions."""
        pass
    
    def create_debug_view(self, frame: np.ndarray, 
                         mosaic: np.ndarray) -> np.ndarray:
        """Create debug view dengan frame dan mosaic."""
        pass
```

### Requirements
1. **Real-time performance**: >10 FPS pada video standar
2. **Robustness**: Handle:
   - Fast motion
   - Lighting changes
   - Temporary occlusions
3. **Drift compensation**: Loop closure jika kembali ke area sebelumnya
4. **Memory efficiency**: Batas memory usage

### Testing Scenarios
1. **Simple pan**: Gerak horizontal saja
2. **Complex motion**: Pan + tilt
3. **Loop closure**: Kembali ke starting point
4. **Challenging**: Fast motion, blur

### Deliverables
1. Implementasi lengkap real-time mosaic
2. Video demo dari berbagai scenarios
3. Performance metrics:
   - FPS
   - Drift error
   - Memory usage
4. Report yang mencakup:
   - Design decisions
   - Challenges dan solutions
   - Future improvements

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Real-time performance | 20% |
| Mosaic quality | 25% |
| Drift compensation | 20% |
| Robustness | 15% |
| Documentation | 20% |

---

## 📚 Referensi Tugas

### Papers
1. Brown & Lowe - "Automatic Panoramic Image Stitching using Invariant Features" (2007)
2. Baker & Matthews - "Lucas-Kanade 20 Years On: A Unifying Framework" (2004)
3. Burt & Adelson - "A Multiresolution Spline" (1983)
4. Zaragoza et al. - "As-Projective-As-Possible Image Stitching" (2013)

### Tutorials
1. OpenCV Stitching Pipeline: https://docs.opencv.org/master/d8/d19/tutorial_stitcher.html
2. CMU Image Stitching: http://graphics.cs.cmu.edu/courses/15-463/2011_fall/hw/proj5/
3. Brown Panorama: https://www.cs.ubc.ca/~lowe/papers/brown07.html

### Datasets
1. Adobe Panorama Dataset
2. HPatches (untuk feature matching)
3. Self-captured sequences

---

## 📅 Timeline Pengumpulan

| Tugas | Deadline | Bobot |
|-------|----------|-------|
| Tugas 1 (DLT) | Minggu ke-1 | 20% |
| Tugas 2 (LK Tracker) | Minggu ke-2 | 25% |
| Tugas 3 (Panorama) | Minggu ke-3 | 25% |
| Tugas 4 (Proyek) | Minggu ke-4 | 30% |

---

## 💡 Tips

1. **DLT**: Pastikan normalisasi benar, ini kunci numerical stability
2. **Lucas-Kanade**: Mulai dengan translation, baru ke affine
3. **Panorama**: Test dengan overlap yang cukup (30-50%)
4. **Video Mosaic**: Mulai dengan video slow motion

---

*Selamat Mengerjakan!*
