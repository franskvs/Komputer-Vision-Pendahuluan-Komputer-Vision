# Tugas Bab 11: Structure from Motion dan SLAM

## Informasi Umum
- **Mata Kuliah**: Praktikum Komputer Vision
- **Topik**: Structure from Motion dan Visual SLAM
- **Tujuan**: Mengimplementasikan komponen-komponen SfM dan SLAM pipeline

---

## Tugas 1: Fundamental Matrix Estimator (25 poin)

### Deskripsi
Implementasikan robust fundamental matrix estimation dengan berbagai metode.

### Spesifikasi

```python
class RobustFundamentalEstimator:
    """
    Robust fundamental matrix estimation.
    """
    
    def __init__(self, threshold: float = 3.0):
        """
        Args:
            threshold: RANSAC inlier threshold (pixels)
        """
        self.threshold = threshold
    
    def eight_point_algorithm(self, pts1: np.ndarray, pts2: np.ndarray,
                              normalize: bool = True) -> np.ndarray:
        """
        Normalized 8-point algorithm.
        
        Args:
            pts1, pts2: Nx2 corresponding points
            normalize: Whether to apply normalization
            
        Returns:
            3x3 fundamental matrix
            
        Steps:
        1. Normalisasi koordinat (zero mean, sqrt(2) avg distance)
        2. Build matrix A (n x 9)
        3. SVD solve Af = 0
        4. Enforce rank 2
        5. Denormalize
        """
        # TODO: Implement
        pass
    
    def seven_point_algorithm(self, pts1: np.ndarray, pts2: np.ndarray
                             ) -> List[np.ndarray]:
        """
        7-point algorithm (returns 1 or 3 solutions).
        
        Uses cubic equation to find valid F matrices.
        
        Returns:
            List of possible fundamental matrices
        """
        # TODO: Implement
        # det(αF1 + (1-α)F2) = 0 gives cubic in α
        pass
    
    def compute_sampson_error(self, F: np.ndarray, 
                               pts1: np.ndarray, pts2: np.ndarray) -> np.ndarray:
        """
        Compute Sampson error (first-order approximation to geometric error).
        
        e = (x'^T F x)^2 / ((Fx)_1^2 + (Fx)_2^2 + (F^Tx')_1^2 + (F^Tx')_2^2)
        
        Returns:
            Nx1 array of errors
        """
        # TODO: Implement
        pass
    
    def compute_epipolar_error(self, F: np.ndarray,
                                pts1: np.ndarray, pts2: np.ndarray) -> np.ndarray:
        """
        Compute symmetric epipolar distance.
        
        d = d(x', l') + d(x, l)
        
        Returns:
            Nx1 array of symmetric distances
        """
        # TODO: Implement
        pass
    
    def ransac_estimate(self, pts1: np.ndarray, pts2: np.ndarray,
                        method: str = '8point',
                        max_iterations: int = 1000,
                        confidence: float = 0.999) -> Tuple[np.ndarray, np.ndarray]:
        """
        RANSAC fundamental matrix estimation.
        
        Args:
            pts1, pts2: Corresponding points
            method: '8point' or '7point'
            max_iterations: Maximum iterations
            confidence: Desired confidence level
            
        Returns:
            Tuple of (F, inlier_mask)
        """
        # TODO: Implement dengan adaptive iteration count
        pass
    
    def refine_with_lm(self, F: np.ndarray, pts1: np.ndarray, pts2: np.ndarray,
                       inliers: np.ndarray) -> np.ndarray:
        """
        Refine F menggunakan Levenberg-Marquardt minimizing Sampson error.
        
        Returns:
            Refined fundamental matrix
        """
        # TODO: Implement
        pass
```

### Test Cases

```python
def test_fundamental_estimator():
    estimator = RobustFundamentalEstimator(threshold=2.0)
    
    # Create synthetic data
    K = np.array([[500, 0, 320], [0, 500, 240], [0, 0, 1]])
    R = rotation_matrix(10, 5, 3)  # degrees
    t = np.array([0.5, 0.1, 0])
    
    pts1, pts2 = generate_correspondences(K, R, t, n_points=100, noise=1.0)
    
    # Add outliers
    pts2_with_outliers = add_outliers(pts2, ratio=0.3)
    
    # Test 8-point
    F_8pt = estimator.eight_point_algorithm(pts1, pts2)
    error_8pt = estimator.compute_sampson_error(F_8pt, pts1, pts2)
    print(f"8-point mean Sampson error: {np.mean(error_8pt):.4f}")
    
    # Test RANSAC
    F_ransac, inliers = estimator.ransac_estimate(pts1, pts2_with_outliers)
    print(f"RANSAC inliers: {np.sum(inliers)}/{len(pts1)}")
    
    # Test refinement
    F_refined = estimator.refine_with_lm(F_ransac, pts1, pts2_with_outliers, inliers)
    error_refined = estimator.compute_sampson_error(F_refined, pts1[inliers], pts2_with_outliers[inliers])
    print(f"Refined mean error: {np.mean(error_refined):.4f}")
```

### Deliverables
1. Implementasi lengkap dengan 8-point dan 7-point algorithms
2. RANSAC dengan adaptive iteration count
3. Perbandingan error sebelum dan sesudah refinement
4. Analisis pengaruh noise dan outlier ratio

---

## Tugas 2: Incremental SfM Pipeline (25 poin)

### Deskripsi
Implementasikan incremental Structure from Motion pipeline.

### Spesifikasi

```python
class IncrementalSfM:
    """
    Incremental Structure from Motion pipeline.
    """
    
    def __init__(self, K: np.ndarray):
        """
        Args:
            K: Camera intrinsic matrix
        """
        self.K = K
        self.cameras = {}  # {image_id: (R, t)}
        self.points_3d = []  # List of 3D points
        self.observations = {}  # {point_id: [(img_id, (x, y)), ...]}
        
    def detect_features(self, images: Dict[int, np.ndarray]) -> Dict[int, Tuple]:
        """
        Detect features di semua images.
        
        Returns:
            {image_id: (keypoints, descriptors)}
        """
        # TODO: Implement
        pass
    
    def match_features(self, features: Dict[int, Tuple]
                      ) -> Dict[Tuple[int, int], List[cv2.DMatch]]:
        """
        Match features antar semua image pairs.
        
        Returns:
            {(img_i, img_j): matches}
        """
        # TODO: Implement with geometric verification
        pass
    
    def select_initial_pair(self, matches: Dict) -> Tuple[int, int]:
        """
        Select best image pair untuk inisialisasi.
        
        Criteria:
        - Banyak matches
        - Sufficient baseline (parallax)
        - Low homography ratio
        
        Returns:
            Tuple of (img_id_1, img_id_2)
        """
        # TODO: Implement
        pass
    
    def initialize(self, img1_id: int, img2_id: int,
                   pts1: np.ndarray, pts2: np.ndarray) -> bool:
        """
        Initialize reconstruction dengan two-view.
        
        Steps:
        1. Estimate essential matrix
        2. Decompose to R, t
        3. Triangulate initial points
        
        Returns:
            Success flag
        """
        # TODO: Implement
        pass
    
    def find_2d_3d_correspondences(self, img_id: int, 
                                    features: Tuple) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find correspondences antara 2D features di new image
        dan existing 3D points.
        
        Returns:
            Tuple of (points_3d, points_2d)
        """
        # TODO: Implement
        pass
    
    def register_image(self, img_id: int, pts_3d: np.ndarray,
                       pts_2d: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Register new image dengan PnP.
        
        Returns:
            Tuple of (R, t) atau None jika gagal
        """
        # TODO: Implement with RANSAC
        pass
    
    def triangulate_new_points(self, img1_id: int, img2_id: int,
                                pts1: np.ndarray, pts2: np.ndarray
                               ) -> np.ndarray:
        """
        Triangulate new 3D points dari two views.
        
        Returns:
            Nx3 array of new 3D points
        """
        # TODO: Implement
        pass
    
    def bundle_adjustment(self, 
                          fix_first_camera: bool = True,
                          max_iterations: int = 100) -> float:
        """
        Bundle adjustment - optimize cameras dan points.
        
        Returns:
            Final reprojection error
        """
        # TODO: Implement menggunakan scipy atau GTSAM
        pass
    
    def run(self, images: Dict[int, np.ndarray]) -> Tuple[Dict, np.ndarray]:
        """
        Run full SfM pipeline.
        
        Returns:
            Tuple of (cameras, points_3d)
        """
        # 1. Feature detection
        features = self.detect_features(images)
        
        # 2. Feature matching
        matches = self.match_features(features)
        
        # 3. Select initial pair
        id1, id2 = self.select_initial_pair(matches)
        
        # 4. Initialize
        self.initialize(id1, id2, ...)
        
        # 5. Incremental registration
        remaining = set(images.keys()) - {id1, id2}
        while remaining:
            for img_id in list(remaining):
                pts_3d, pts_2d = self.find_2d_3d_correspondences(img_id, features[img_id])
                if len(pts_3d) >= 6:
                    R, t = self.register_image(img_id, pts_3d, pts_2d)
                    if R is not None:
                        # Triangulate new points
                        # ...
                        remaining.remove(img_id)
                        break
            else:
                break  # No more images can be registered
        
        # 6. Final BA
        self.bundle_adjustment()
        
        return self.cameras, np.array(self.points_3d)
```

### Test Cases

```python
def test_sfm_pipeline():
    # Generate synthetic scene
    K = np.array([[500, 0, 320], [0, 500, 240], [0, 0, 1]])
    
    # Create 3D points
    points_3d = create_synthetic_scene()
    
    # Create camera poses
    cameras_gt = create_camera_poses(n_cameras=5)
    
    # Render images
    images = render_synthetic_images(K, cameras_gt, points_3d)
    
    # Run SfM
    sfm = IncrementalSfM(K)
    cameras_est, points_est = sfm.run(images)
    
    # Evaluate
    align_and_evaluate(cameras_gt, cameras_est, points_3d, points_est)
```

### Deliverables
1. Complete SfM pipeline implementation
2. Visualization 3D point cloud
3. Camera trajectory comparison dengan ground truth
4. Analisis:
   - Reprojection error statistics
   - Number of 3D points vs cameras
   - Effect of BA iterations

---

## Tugas 3: Visual Odometry System (25 poin)

### Deskripsi
Implementasikan monocular visual odometry system yang robust.

### Spesifikasi

```python
class MonocularVO:
    """
    Monocular Visual Odometry with various enhancements.
    """
    
    def __init__(self, K: np.ndarray, config: dict = None):
        """
        Args:
            K: Camera intrinsic matrix
            config: Configuration dictionary
        """
        self.K = K
        self.config = config or self._default_config()
        
        # Feature detector/tracker
        self.detector = None
        self.tracker = None
        
        # State
        self.pose = np.eye(4)  # Current pose
        self.trajectory = []
        self.keyframes = []
        self.map_points = []
        
    def _default_config(self) -> dict:
        return {
            'feature_detector': 'orb',  # 'orb', 'sift', 'fast'
            'n_features': 2000,
            'tracking': 'optical_flow',  # 'optical_flow', 'descriptor'
            'min_features': 100,
            'keyframe_threshold': 50,  # pixel motion
            'use_local_ba': True,
            'ba_window': 5,
        }
    
    def detect_features(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect features di frame.
        
        Returns:
            Tuple of (keypoints, descriptors)
        """
        # TODO: Implement with configurable detector
        pass
    
    def track_features(self, prev_frame: np.ndarray, curr_frame: np.ndarray,
                       prev_pts: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Track features dari previous ke current frame.
        
        Returns:
            Tuple of (tracked_prev_pts, tracked_curr_pts, status)
        """
        # TODO: Implement KLT optical flow tracking
        pass
    
    def estimate_pose(self, pts1: np.ndarray, pts2: np.ndarray
                     ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Estimate relative pose dari point correspondences.
        
        Returns:
            Tuple of (R, t, inliers)
        """
        # TODO: Implement
        pass
    
    def check_keyframe(self, curr_pts: np.ndarray, 
                       keyframe_pts: np.ndarray) -> bool:
        """
        Check apakah perlu membuat keyframe baru.
        
        Criteria:
        - Sufficient feature motion
        - Minimum feature overlap
        
        Returns:
            True if should create keyframe
        """
        # TODO: Implement
        pass
    
    def local_bundle_adjustment(self) -> None:
        """
        Perform local BA pada recent keyframes.
        """
        # TODO: Implement
        pass
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process single frame.
        
        Returns:
            4x4 current pose matrix
        """
        # TODO: Implement full processing pipeline
        pass
    
    def run(self, video_path: str) -> np.ndarray:
        """
        Run VO pada video.
        
        Returns:
            Nx4x4 array of poses
        """
        cap = cv2.VideoCapture(video_path)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            pose = self.process_frame(frame)
            self.trajectory.append(pose.copy())
        
        cap.release()
        return np.array(self.trajectory)
    
    def get_trajectory(self) -> np.ndarray:
        """Get trajectory as Nx3 positions."""
        return np.array([pose[:3, 3] for pose in self.trajectory])


class StereoVO(MonocularVO):
    """
    Stereo Visual Odometry.
    """
    
    def __init__(self, K: np.ndarray, baseline: float, config: dict = None):
        super().__init__(K, config)
        self.baseline = baseline
        
    def compute_disparity(self, left: np.ndarray, right: np.ndarray
                         ) -> np.ndarray:
        """Compute disparity map."""
        # TODO: Implement
        pass
    
    def triangulate_stereo(self, left_pts: np.ndarray, 
                           disparity: np.ndarray) -> np.ndarray:
        """
        Triangulate 3D points dari stereo.
        depth = f * baseline / disparity
        
        Returns:
            Nx3 3D points
        """
        # TODO: Implement
        pass
    
    def process_stereo_frame(self, left: np.ndarray, right: np.ndarray
                            ) -> np.ndarray:
        """Process stereo frame pair."""
        # TODO: Implement
        pass
```

### Test Cases

```python
def test_visual_odometry():
    K = np.array([[718.856, 0, 607.1928],
                  [0, 718.856, 185.2157],
                  [0, 0, 1]])  # KITTI calibration
    
    vo = MonocularVO(K)
    
    # Run pada KITTI sequence atau synthetic video
    trajectory = vo.run('sequence_00.mp4')
    
    # Load ground truth
    gt_trajectory = load_kitti_poses('00.txt')
    
    # Compute ATE dan RPE
    ate = compute_ate(gt_trajectory, trajectory)
    rpe = compute_rpe(gt_trajectory, trajectory)
    
    print(f"ATE: {ate:.4f} m")
    print(f"RPE: {rpe:.4f}")
    
    # Plot
    plot_trajectory(gt_trajectory, trajectory)
```

### Deliverables
1. Working monocular VO implementation
2. Trajectory visualization dan comparison
3. Error metrics (ATE, RPE)
4. Analisis:
   - Effect of feature detector choice
   - Impact of local BA
   - Failure cases

---

## Tugas 4: Proyek Akhir - Simple SLAM System (25 poin)

### Deskripsi
Bangun simple SLAM system dengan loop closure.

### Spesifikasi

```python
class SimpleSLAM:
    """
    Simple monocular SLAM with loop closure.
    """
    
    def __init__(self, K: np.ndarray, vocabulary_path: str = None):
        """
        Args:
            K: Camera intrinsics
            vocabulary_path: Path to BoW vocabulary (optional)
        """
        self.K = K
        self.vo = MonocularVO(K)
        
        # Map
        self.keyframes = []  # List of Keyframe objects
        self.map_points = []  # List of MapPoint objects
        
        # Loop closure
        self.vocabulary = self._load_vocabulary(vocabulary_path)
        self.keyframe_database = []
        
        # Pose graph
        self.pose_graph = PoseGraph()
        
    def _load_vocabulary(self, path: str):
        """Load or create BoW vocabulary."""
        # TODO: Implement
        pass
    
    def create_keyframe(self, frame: np.ndarray, pose: np.ndarray
                       ) -> 'Keyframe':
        """Create new keyframe."""
        # TODO: Implement
        pass
    
    def compute_bow_vector(self, descriptors: np.ndarray) -> np.ndarray:
        """Compute Bag of Words vector."""
        # TODO: Implement
        pass
    
    def detect_loop_closure(self, current_kf: 'Keyframe'
                           ) -> Optional['Keyframe']:
        """
        Detect loop closure dengan BoW similarity.
        
        Returns:
            Matching keyframe atau None
        """
        # TODO: Implement
        # 1. Compute BoW vector
        # 2. Query database
        # 3. Geometric verification
        pass
    
    def compute_sim3(self, kf1: 'Keyframe', kf2: 'Keyframe'
                    ) -> Optional[np.ndarray]:
        """
        Compute Sim(3) transformation untuk loop closure.
        
        Returns:
            4x4 similarity transform atau None
        """
        # TODO: Implement
        pass
    
    def correct_loop(self, loop_kf: 'Keyframe', current_kf: 'Keyframe',
                     sim3: np.ndarray) -> None:
        """
        Correct trajectory setelah loop closure.
        
        Steps:
        1. Fuse duplicate map points
        2. Pose graph optimization
        3. Full BA (optional)
        """
        # TODO: Implement
        pass
    
    def run(self, video_source) -> Tuple[np.ndarray, List]:
        """
        Run SLAM.
        
        Returns:
            Tuple of (trajectory, map_points)
        """
        # Main loop
        # 1. Track current frame
        # 2. Check for keyframe
        # 3. If keyframe:
        #    - Create keyframe
        #    - Check loop closure
        #    - If loop: correct
        # 4. Optional: local mapping thread
        pass
    
    def save_map(self, path: str) -> None:
        """Save map untuk later use."""
        # TODO: Implement
        pass
    
    def load_map(self, path: str) -> None:
        """Load saved map."""
        # TODO: Implement
        pass


class Keyframe:
    """Keyframe representation."""
    
    def __init__(self, id: int, frame: np.ndarray, pose: np.ndarray):
        self.id = id
        self.frame = frame
        self.pose = pose
        self.keypoints = None
        self.descriptors = None
        self.bow_vector = None
        self.map_point_indices = []


class MapPoint:
    """3D map point."""
    
    def __init__(self, id: int, position: np.ndarray):
        self.id = id
        self.position = position
        self.descriptor = None
        self.observations = {}  # {keyframe_id: keypoint_idx}
        self.num_visible = 0
        self.num_found = 0


class PoseGraph:
    """Pose graph untuk optimization."""
    
    def __init__(self):
        self.nodes = []  # poses
        self.edges = []  # constraints
    
    def add_node(self, pose: np.ndarray) -> int:
        """Add pose node."""
        pass
    
    def add_edge(self, i: int, j: int, relative_pose: np.ndarray,
                 information: np.ndarray = None) -> None:
        """Add edge constraint."""
        pass
    
    def optimize(self) -> None:
        """Optimize pose graph."""
        # TODO: Implement using scipy or g2o
        pass
```

### Fitur Wajib
1. **Visual Odometry** - Basic tracking
2. **Keyframe Management** - Selection dan storage
3. **Loop Closure Detection** - BoW-based atau simple feature matching
4. **Pose Graph Optimization** - Correct drift

### Fitur Bonus
- Multi-threaded (tracking, mapping, loop closing)
- Map saving/loading
- Relocalization
- Dense mapping

### Evaluation

```python
def evaluate_slam(slam_trajectory: np.ndarray, 
                  gt_trajectory: np.ndarray) -> dict:
    """
    Evaluate SLAM performance.
    
    Returns:
        Dict with ATE, RPE, loop closure stats
    """
    # Align trajectories
    aligned = align_trajectories(slam_trajectory, gt_trajectory)
    
    # Compute metrics
    ate = compute_ate(gt_trajectory, aligned)
    rpe_trans, rpe_rot = compute_rpe(gt_trajectory, aligned)
    
    return {
        'ate': ate,
        'rpe_translation': rpe_trans,
        'rpe_rotation': rpe_rot,
    }
```

### Deliverables
1. **Source Code**:
   - Complete SLAM system
   - All component classes
   - Demo script

2. **Results**:
   - Trajectory plot dengan loop closures marked
   - 3D map visualization
   - Before/after loop closure comparison

3. **Documentation**:
   - System architecture diagram
   - Algorithm descriptions
   - Performance analysis

4. **Video Demo**:
   - Real-time tracking visualization
   - Loop closure events

---

## Kriteria Penilaian

### Tugas 1: Fundamental Matrix (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| 8-point Algorithm | 8 | Correct normalization, rank enforcement |
| RANSAC | 8 | Adaptive, correct error metric |
| Refinement | 5 | LM optimization working |
| Analysis | 4 | Thorough comparison |

### Tugas 2: Incremental SfM (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| Pipeline | 10 | All components working |
| Bundle Adjustment | 8 | Proper optimization |
| Visualization | 4 | Clear 3D reconstruction |
| Analysis | 3 | Error metrics |

### Tugas 3: Visual Odometry (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| Tracking | 10 | Robust feature tracking |
| Pose Estimation | 8 | Accurate relative pose |
| Evaluation | 4 | ATE, RPE computed |
| Analysis | 3 | Failure case analysis |

### Tugas 4: Simple SLAM (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| VO Integration | 8 | Smooth tracking |
| Loop Closure | 10 | Detection + correction |
| Optimization | 4 | Pose graph working |
| Documentation | 3 | Clear explanation |

---

## Dataset dan Resources

### Datasets

1. **KITTI Odometry**
   - https://www.cvlibs.net/datasets/kitti/eval_odometry.php
   - Stereo sequences dengan ground truth

2. **TUM RGB-D**
   - https://vision.in.tum.de/data/datasets/rgbd-dataset
   - RGB-D sequences

3. **EuRoC MAV**
   - https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets
   - Visual-inertial data

### Libraries

```bash
# Core
pip install opencv-contrib-python numpy scipy matplotlib

# Optimization
pip install g2o  # atau pip install pygtsam
pip install scipy

# Visualization
pip install open3d plotly

# Evaluation
pip install evo  # trajectory evaluation
```

---

## Tips dan Panduan

### Untuk Fundamental Matrix
1. Normalisasi sangat penting untuk stabilitas numerik
2. Test pada synthetic data dulu (ground truth tersedia)
3. Sampson error lebih baik dari algebraic error

### Untuk SfM
1. Mulai dengan two-view, lalu incremental
2. Initial pair selection sangat krusial
3. BA bisa gunakan scipy.optimize.least_squares

### Untuk Visual Odometry
1. Feature tracking dengan KLT lebih cepat dari descriptor matching
2. Handle scale drift dengan external info atau stereo
3. Keyframe selection affects accuracy dan efficiency

### Untuk SLAM
1. Start simple - VO + pose graph
2. Loop closure detection bisa mulai dengan global feature matching
3. Test pada sequence dengan known loops

---

## Referensi

1. Hartley & Zisserman - Multiple View Geometry in Computer Vision
2. ORB-SLAM papers (Mur-Artal et al.)
3. PTAM paper (Klein & Murray)
4. Szeliski - Computer Vision: Algorithms and Applications, Ch. 11

---

**Selamat mengerjakan!**
