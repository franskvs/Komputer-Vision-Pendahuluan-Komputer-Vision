# Tugas Bab 9: Motion Estimation

## 📋 Informasi Umum

| Item | Keterangan |
|------|------------|
| **Topik** | Motion Estimation dan Optical Flow |
| **Tujuan** | Memahami dan mengimplementasikan teknik motion estimation |
| **Prasyarat** | Bab 7-8 (Features, Alignment), Calculus |
| **Estimasi Waktu** | 4-5 jam |

---

## 📝 Tugas 1: Implementasi Coarse-to-Fine Lucas-Kanade

### Deskripsi
Implementasikan Lucas-Kanade optical flow dengan coarse-to-fine (pyramid) approach untuk menangani large displacement.

### Spesifikasi

```python
class PyramidalLucasKanade:
    """
    Coarse-to-fine Lucas-Kanade optical flow.
    """
    
    def __init__(self, window_size: int = 15, num_levels: int = 4,
                 num_iterations: int = 10):
        """
        Args:
            window_size: LK window size
            num_levels: Number of pyramid levels
            num_iterations: Iterations per level for refinement
        """
        self.window_size = window_size
        self.num_levels = num_levels
        self.num_iterations = num_iterations
    
    def build_pyramid(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Build Gaussian pyramid.
        
        Args:
            image: Input image
            
        Returns:
            List of images from finest to coarsest
        """
        pass
    
    def compute_flow_single_scale(self, img1: np.ndarray, img2: np.ndarray,
                                   initial_flow: np.ndarray = None
                                   ) -> np.ndarray:
        """
        Compute LK flow at single scale.
        
        Args:
            img1, img2: Input images
            initial_flow: Initial flow estimate (for warping)
            
        Returns:
            flow: Estimated flow field
        """
        pass
    
    def warp_image(self, image: np.ndarray, flow: np.ndarray) -> np.ndarray:
        """
        Warp image menggunakan flow field.
        
        Args:
            image: Image to warp
            flow: Flow field
            
        Returns:
            Warped image
        """
        pass
    
    def compute_flow(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Compute flow using coarse-to-fine approach.
        
        Algorithm:
        1. Build pyramids for both images
        2. At coarsest level: compute flow with LK
        3. For each finer level:
           a. Upsample flow from coarser level
           b. Warp img2 towards img1 using current flow
           c. Compute residual flow
           d. Add to upsampled flow
        
        Returns:
            Dense optical flow field
        """
        pass
```

### Deliverables
1. Implementasi lengkap pyramidal LK
2. Comparison dengan:
   - Single-scale LK
   - OpenCV `calcOpticalFlowPyrLK`
3. Test pada sequence dengan large motion

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Pyramid construction benar | 20% |
| Single-scale LK benar | 25% |
| Coarse-to-fine logic benar | 30% |
| Evaluation dan analisis | 25% |

---

## 📝 Tugas 2: Horn-Schunck dengan Robust Estimation

### Deskripsi
Implementasikan Horn-Schunck optical flow dengan robust penalty functions untuk handle outliers (occlusions, motion boundaries).

### Spesifikasi

```python
class RobustHornSchunck:
    """
    Horn-Schunck dengan robust estimation.
    
    Minimizes:
    E = sum[ rho_data(Ix*u + Iy*v + It) ] + 
        alpha * sum[ rho_smooth(|∇u|) + rho_smooth(|∇v|) ]
    """
    
    def __init__(self, alpha: float = 50.0, 
                 data_sigma: float = 5.0,
                 smooth_sigma: float = 2.0,
                 num_iterations: int = 200,
                 num_warps: int = 5):
        """
        Args:
            alpha: Smoothness weight
            data_sigma: Sigma for robust data term
            smooth_sigma: Sigma for robust smoothness term
            num_iterations: Inner iterations
            num_warps: Number of warping iterations
        """
        pass
    
    def robust_function(self, x: np.ndarray, sigma: float) -> np.ndarray:
        """
        Compute robust penalty function.
        
        Options:
        - Charbonnier: sqrt(x^2 + epsilon)
        - Lorentzian: log(1 + x^2/(2*sigma^2))
        - Geman-McClure: x^2 / (sigma^2 + x^2)
        """
        pass
    
    def robust_weight(self, x: np.ndarray, sigma: float) -> np.ndarray:
        """
        Compute weight dari robust function: w = rho'(x) / x
        """
        pass
    
    def compute_flow(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Compute robust Horn-Schunck flow.
        
        Algorithm (outer loop warping):
        1. Initialize flow to zero
        2. For each warp iteration:
           a. Warp img2 towards img1
           b. Compute gradients
           c. Solve weighted Horn-Schunck (inner iterations)
           d. Update flow
           
        Returns:
            Dense optical flow
        """
        pass
```

### Deliverables
1. Implementasi lengkap robust Horn-Schunck
2. Comparison berbagai robust functions
3. Visualisasi weight maps di motion boundaries
4. Comparison dengan standard Horn-Schunck

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Robust functions benar | 25% |
| Weighted iteration benar | 25% |
| Warping loop benar | 25% |
| Analisis dan comparison | 25% |

---

## 📝 Tugas 3: Motion-Based Video Segmentation

### Deskripsi
Implementasikan video segmentation berdasarkan motion, untuk memisahkan foreground dan background atau multiple moving objects.

### Spesifikasi

```python
class MotionBasedSegmentation:
    """
    Video segmentation berdasarkan motion analysis.
    """
    
    def __init__(self, flow_method: str = 'farneback'):
        self.flow_method = flow_method
    
    def compute_flow_sequence(self, frames: List[np.ndarray]
                             ) -> List[np.ndarray]:
        """
        Compute optical flow untuk seluruh sequence.
        """
        pass
    
    def estimate_dominant_motion(self, flow: np.ndarray, 
                                  method: str = 'ransac'
                                  ) -> np.ndarray:
        """
        Estimate dominant (background) motion.
        
        Methods:
        - 'mean': Simple mean of flow
        - 'median': Robust median
        - 'ransac': Fit affine/homography model
        
        Returns:
            Parameters of dominant motion model
        """
        pass
    
    def compute_motion_residual(self, flow: np.ndarray,
                                 dominant_motion: np.ndarray) -> np.ndarray:
        """
        Compute residual setelah kompensasi dominant motion.
        
        Returns:
            Residual flow field
        """
        pass
    
    def segment_moving_objects(self, frames: List[np.ndarray],
                               threshold: float = 2.0) -> List[np.ndarray]:
        """
        Segment moving objects dari video.
        
        Algorithm:
        1. Compute optical flow
        2. Estimate dominant motion (camera/background)
        3. Compute motion residual
        4. Threshold residual magnitude
        5. Apply morphological operations
        6. Optional: temporal consistency filtering
        
        Returns:
            List of segmentation masks
        """
        pass
    
    def track_segments(self, masks: List[np.ndarray]) -> Dict[int, List]:
        """
        Track segmented regions across frames.
        
        Returns:
            Dictionary of object_id -> list of (frame_idx, bounding_box)
        """
        pass


class TemporalConsistencyFilter:
    """
    Temporal filtering untuk consistent segmentation.
    """
    
    def __init__(self, history_length: int = 5):
        self.history_length = history_length
        self.history = []
    
    def update(self, mask: np.ndarray) -> np.ndarray:
        """
        Update dengan mask baru dan return filtered mask.
        """
        pass
    
    def get_consistent_mask(self) -> np.ndarray:
        """
        Combine history untuk temporally consistent mask.
        """
        pass
```

### Deliverables
1. Implementasi lengkap motion-based segmentation
2. Test pada:
   - Video dengan static camera
   - Video dengan moving camera
3. Quantitative evaluation jika ground truth tersedia
4. Demo video output

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Flow computation benar | 20% |
| Dominant motion estimation | 25% |
| Segmentation quality | 30% |
| Temporal consistency | 25% |

---

## 📝 Tugas 4 (Proyek): Video Frame Interpolation

### Deskripsi
Implementasikan sistem frame interpolation untuk membuat slow-motion video dari video normal menggunakan optical flow.

### Spesifikasi

```python
class VideoFrameInterpolator:
    """
    Video frame interpolation untuk slow-motion.
    
    Supports:
    - Bidirectional flow-based interpolation
    - Occlusion handling
    - Multiple interpolation methods
    """
    
    def __init__(self, flow_method: str = 'dis'):
        """
        Args:
            flow_method: 'farneback', 'dis', atau 'raft' (deep)
        """
        self.flow_method = flow_method
    
    def compute_bidirectional_flow(self, frame1: np.ndarray, 
                                    frame2: np.ndarray
                                    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute flow di kedua arah.
        
        Returns:
            flow_forward: frame1 -> frame2
            flow_backward: frame2 -> frame1
        """
        pass
    
    def detect_occlusions(self, flow_forward: np.ndarray,
                          flow_backward: np.ndarray) -> np.ndarray:
        """
        Detect occluded regions menggunakan forward-backward consistency.
        
        Occlusion mask: regions where flow tidak konsisten
        
        Returns:
            occlusion_mask: Binary mask (1 = occluded)
        """
        pass
    
    def interpolate_flow(self, flow_forward: np.ndarray,
                         flow_backward: np.ndarray,
                         t: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Interpolate flow untuk intermediate time t.
        
        Args:
            flow_forward, flow_backward: Bidirectional flows
            t: Interpolation time (0 = frame1, 1 = frame2)
            
        Returns:
            flow_t0: Flow from intermediate to frame1
            flow_t1: Flow from intermediate to frame2
        """
        pass
    
    def warp_frame(self, frame: np.ndarray, flow: np.ndarray) -> np.ndarray:
        """
        Backward warping frame menggunakan flow.
        """
        pass
    
    def blend_frames(self, warped1: np.ndarray, warped2: np.ndarray,
                     t: float, occlusion_mask: np.ndarray = None
                     ) -> np.ndarray:
        """
        Blend warped frames dengan handling occlusions.
        
        Args:
            warped1: Frame warped from frame1
            warped2: Frame warped from frame2
            t: Interpolation time
            occlusion_mask: Optional occlusion mask
            
        Returns:
            Interpolated frame
        """
        pass
    
    def interpolate_frame(self, frame1: np.ndarray, frame2: np.ndarray,
                          t: float) -> np.ndarray:
        """
        Generate intermediate frame at time t.
        
        Full pipeline:
        1. Compute bidirectional flow
        2. Detect occlusions
        3. Interpolate flow to time t
        4. Warp both frames
        5. Blend dengan occlusion-aware weighting
        
        Returns:
            Interpolated frame
        """
        pass
    
    def interpolate_video(self, video_path: str, 
                         output_path: str,
                         slowdown_factor: int = 2) -> None:
        """
        Create slow-motion video.
        
        Args:
            video_path: Input video
            output_path: Output video
            slowdown_factor: How many times slower (2 = half speed)
        """
        pass


class QualityMetrics:
    """
    Metrics untuk evaluasi frame interpolation.
    """
    
    @staticmethod
    def psnr(img1: np.ndarray, img2: np.ndarray) -> float:
        """Peak Signal-to-Noise Ratio."""
        pass
    
    @staticmethod
    def ssim(img1: np.ndarray, img2: np.ndarray) -> float:
        """Structural Similarity Index."""
        pass
    
    @staticmethod
    def interpolation_error(gt_frame: np.ndarray, 
                           interp_frame: np.ndarray) -> Dict[str, float]:
        """Compute all metrics."""
        pass
```

### Dataset yang Disarankan
- **Middlebury Interpolation**: http://vision.middlebury.edu/flow/data/
- **Vimeo-90K**: https://github.com/anchen1011/toflow
- Video sendiri (skip every other frame sebagai test)

### Requirements
1. **Real-time** untuk low resolution
2. Handle:
   - Large motion
   - Occlusions
   - Motion blur
3. Quality metrics:
   - PSNR > 30 dB pada standard sequences
   - SSIM > 0.9

### Deliverables
1. Implementasi lengkap frame interpolator
2. Demo videos:
   - 2x slow motion
   - 4x slow motion
3. Quantitative evaluation pada benchmark
4. Report yang mencakup:
   - Algorithm design
   - Occlusion handling strategy
   - Limitations dan future work

### Kriteria Penilaian
| Kriteria | Bobot |
|----------|-------|
| Bidirectional flow | 20% |
| Occlusion handling | 25% |
| Interpolation quality | 25% |
| System completeness | 15% |
| Documentation | 15% |

---

## 📚 Referensi Tugas

### Papers
1. Lucas & Kanade - "An Iterative Image Registration Technique" (1981)
2. Horn & Schunck - "Determining Optical Flow" (1981)
3. Black & Anandan - "The Robust Estimation of Multiple Motions" (1996)
4. Brox et al. - "High Accuracy Optical Flow" (2004)
5. Jiang et al. - "Super SloMo" (2018) - Deep frame interpolation

### Tutorials
1. Middlebury Flow Tutorial: http://vision.middlebury.edu/flow/
2. OpenCV Optical Flow: https://docs.opencv.org/master/d4/dee/tutorial_optical_flow.html

### Code References
1. OpenCV Optical Flow: https://github.com/opencv/opencv
2. FlowNet2: https://github.com/NVIDIA/flownet2-pytorch
3. RAFT: https://github.com/princeton-vl/RAFT

---

## 📅 Timeline Pengumpulan

| Tugas | Deadline | Bobot |
|-------|----------|-------|
| Tugas 1 (Pyramidal LK) | Minggu ke-1 | 20% |
| Tugas 2 (Robust HS) | Minggu ke-2 | 25% |
| Tugas 3 (Segmentation) | Minggu ke-3 | 25% |
| Tugas 4 (Proyek) | Minggu ke-4 | 30% |

---

## 💡 Tips

1. **Pyramidal LK**: Pastikan downsampling dan upsampling benar
2. **Robust HS**: Mulai dengan standard HS, lalu tambah robust term
3. **Segmentation**: Test dulu dengan static camera
4. **Interpolation**: Handle boundaries dengan hati-hati

---

*Selamat Mengerjakan!*
