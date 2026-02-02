# Tugas Bab 7: Feature Detection dan Matching

## Informasi Tugas
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 7 - Feature Detection dan Matching
- **Topik**: Keypoint Detectors, Descriptors, Matching, RANSAC
- **Waktu Pengerjaan**: 2 minggu

---

## Bagian A: Pertanyaan Teori (30 poin)

### A1. Corner Detection (10 poin)

1. **Dalam Harris Corner Detector, jelaskan:**
   - Apa yang direpresentasikan oleh matriks struktur M?
   - Bagaimana eigenvalues diinterpretasikan (flat, edge, corner)?
   - Apa keuntungan menggunakan Harris response function dibanding menghitung eigenvalues langsung?

2. **Bandingkan Harris dan Shi-Tomasi detector:**
   - Perbedaan response function
   - Kelebihan dan kekurangan masing-masing

3. **Jelaskan bagaimana FAST detector bekerja:**
   - Segment test
   - Mengapa FAST sangat cepat?
   - Apa kelemahannya?

### A2. Scale-Invariant Features (10 poin)

4. **Jelaskan konsep scale space dalam SIFT:**
   - Gaussian pyramid
   - Difference of Gaussian (DoG)
   - Bagaimana extrema detection dilakukan?

5. **Dalam SIFT descriptor, jelaskan:**
   - Mengapa menggunakan histogram of gradients?
   - Bagaimana rotation invariance dicapai?
   - Struktur descriptor 128 dimensi

6. **Bandingkan SIFT, SURF, dan ORB:**
   | Aspect | SIFT | SURF | ORB |
   |--------|------|------|-----|
   | Detection | ? | ? | ? |
   | Descriptor | ? | ? | ? |
   | Speed | ? | ? | ? |
   | Robustness | ? | ? | ? |
   | License | ? | ? | ? |

### A3. Feature Matching (10 poin)

7. **Jelaskan Lowe's ratio test:**
   - Mengapa ratio test efektif?
   - Bagaimana memilih threshold yang baik?

8. **Apa perbedaan antara:**
   - Brute-force matching vs FLANN
   - Euclidean distance vs Hamming distance

9. **Dalam RANSAC untuk homography estimation:**
   - Mengapa minimal 4 points untuk homography?
   - Bagaimana cara memilih threshold inlier?
   - Apa yang dimaksud dengan model refitting?

---

## Bagian B: Implementasi Coding (40 poin)

### B1. Harris Corner Detector dari Scratch (15 poin)

Implementasikan Harris Corner Detector lengkap:

```python
import numpy as np
import cv2

class HarrisCornerDetector:
    """
    Implementasi Harris Corner Detector dari scratch
    """
    
    def __init__(self, k: float = 0.04, threshold: float = 0.01,
                 block_size: int = 3, aperture_size: int = 3):
        """
        Args:
            k: Harris parameter (0.04-0.06)
            threshold: Response threshold (relative)
            block_size: Window size untuk summing
            aperture_size: Sobel kernel size
        """
        self.k = k
        self.threshold = threshold
        self.block_size = block_size
        self.aperture_size = aperture_size
    
    def compute_gradients(self, image: np.ndarray) -> tuple:
        """
        Compute image gradients Ix dan Iy
        
        Gunakan Sobel operator
        """
        # TODO: Implementasi
        pass
    
    def compute_structure_tensor(self, Ix: np.ndarray, Iy: np.ndarray) -> tuple:
        """
        Compute struktur tensor components: Sxx, Syy, Sxy
        
        Hint: Gunakan Gaussian smoothing pada Ix², Iy², Ix*Iy
        """
        # TODO: Implementasi
        pass
    
    def compute_response(self, Sxx: np.ndarray, Syy: np.ndarray, 
                        Sxy: np.ndarray) -> np.ndarray:
        """
        Compute Harris response:
        R = det(M) - k * trace(M)²
          = Sxx*Syy - Sxy² - k*(Sxx + Syy)²
        """
        # TODO: Implementasi
        pass
    
    def non_max_suppression(self, response: np.ndarray, 
                           window_size: int = 3) -> np.ndarray:
        """
        Non-maximum suppression untuk mendapatkan corner yang distinct
        
        Corner valid jika response adalah maksimum dalam neighborhood
        """
        # TODO: Implementasi
        pass
    
    def detect(self, image: np.ndarray) -> tuple:
        """
        Full detection pipeline
        
        Returns:
            corners: Array of (x, y) corner coordinates
            response: Harris response image
        """
        # TODO: Implementasi
        # 1. Convert to grayscale if needed
        # 2. Compute gradients
        # 3. Compute structure tensor
        # 4. Compute Harris response
        # 5. Threshold
        # 6. Non-max suppression
        # 7. Extract corner coordinates
        pass
    
    def draw_corners(self, image: np.ndarray, corners: np.ndarray,
                    color: tuple = (0, 255, 0), radius: int = 3) -> np.ndarray:
        """Draw corners on image"""
        # TODO: Implementasi
        pass


# Testing
def test_harris():
    # Create test image dengan checkerboard
    img = np.zeros((200, 200), dtype=np.uint8)
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                img[i*50:(i+1)*50, j*50:(j+1)*50] = 255
    
    detector = HarrisCornerDetector()
    corners, response = detector.detect(img)
    
    # Visualize
    # TODO: Plot response dan detected corners
    
    # Compare dengan OpenCV
    opencv_corners = cv2.cornerHarris(img.astype(np.float32), 2, 3, 0.04)
    
    print(f"Detected {len(corners)} corners")
```

**Kriteria Penilaian:**
- Gradient computation benar (3 poin)
- Structure tensor benar (3 poin)
- Harris response benar (4 poin)
- NMS benar (3 poin)
- Testing dan comparison (2 poin)

### B2. Feature Matcher dengan RANSAC (15 poin)

Implementasikan feature matcher lengkap dengan geometric verification:

```python
class RobustFeatureMatcher:
    """
    Feature matcher dengan berbagai strategi dan RANSAC verification
    """
    
    def __init__(self, detector: str = 'sift', matcher: str = 'bf'):
        """
        Args:
            detector: 'sift', 'orb', atau 'akaze'
            matcher: 'bf' atau 'flann'
        """
        # TODO: Initialize detector dan matcher
        pass
    
    def detect_and_describe(self, image: np.ndarray) -> tuple:
        """
        Detect keypoints dan compute descriptors
        
        Returns:
            keypoints: List of cv2.KeyPoint
            descriptors: Descriptor array
        """
        # TODO: Implementasi
        pass
    
    def match_bruteforce(self, desc1: np.ndarray, desc2: np.ndarray) -> list:
        """Simple brute-force matching"""
        # TODO: Implementasi
        pass
    
    def match_with_ratio_test(self, desc1: np.ndarray, desc2: np.ndarray,
                             ratio: float = 0.75) -> list:
        """Matching dengan Lowe's ratio test"""
        # TODO: Implementasi
        pass
    
    def match_mutual(self, desc1: np.ndarray, desc2: np.ndarray) -> list:
        """Cross-check / mutual nearest neighbor matching"""
        # TODO: Implementasi
        pass
    
    def ransac_fundamental(self, pts1: np.ndarray, pts2: np.ndarray,
                          threshold: float = 3.0, 
                          max_iters: int = 1000) -> tuple:
        """
        RANSAC untuk fundamental matrix estimation
        
        Args:
            pts1, pts2: Matched point pairs (N, 2)
            threshold: Epipolar distance threshold
            max_iters: Max RANSAC iterations
            
        Returns:
            F: 3x3 fundamental matrix
            inliers: Boolean mask
        """
        # TODO: Implementasi
        # 1. Random sample 8 points
        # 2. Compute F dengan 8-point algorithm
        # 3. Compute epipolar distances
        # 4. Count inliers
        # 5. Repeat dan keep best
        pass
    
    def ransac_homography(self, pts1: np.ndarray, pts2: np.ndarray,
                         threshold: float = 4.0,
                         max_iters: int = 1000) -> tuple:
        """
        RANSAC untuk homography estimation
        
        Returns:
            H: 3x3 homography matrix
            inliers: Boolean mask
        """
        # TODO: Implementasi
        pass
    
    def match_images(self, img1: np.ndarray, img2: np.ndarray,
                    method: str = 'ratio',
                    geometric_verify: str = 'homography') -> dict:
        """
        Complete matching pipeline
        
        Args:
            method: 'simple', 'ratio', atau 'mutual'
            geometric_verify: 'none', 'homography', atau 'fundamental'
            
        Returns:
            {
                'keypoints1': [...],
                'keypoints2': [...],
                'matches': [...],
                'inliers': [...],
                'transform': H or F
            }
        """
        # TODO: Implementasi
        pass
    
    def visualize_matches(self, img1: np.ndarray, img2: np.ndarray,
                         result: dict, show_inliers_only: bool = True) -> np.ndarray:
        """Visualize matching result"""
        # TODO: Implementasi
        pass


# Testing dengan berbagai transformasi
def test_robust_matching():
    # Create test image
    img1 = create_test_image()  # TODO: Implement
    
    # Create transformed versions
    # 1. Rotation
    img2_rot = rotate_image(img1, 30)
    
    # 2. Scale
    img2_scale = cv2.resize(img1, None, fx=0.7, fy=0.7)
    
    # 3. Perspective
    img2_persp = apply_perspective(img1)
    
    # 4. Illumination change
    img2_illum = cv2.convertScaleAbs(img1, alpha=1.3, beta=30)
    
    # Test matching pada setiap transformasi
    matcher = RobustFeatureMatcher('sift', 'bf')
    
    for name, img2 in [('rotation', img2_rot), ('scale', img2_scale),
                       ('perspective', img2_persp), ('illumination', img2_illum)]:
        result = matcher.match_images(img1, img2)
        print(f"{name}: {len(result['inliers'])} inliers")
        
        # Visualize
        vis = matcher.visualize_matches(img1, img2, result)
        cv2.imwrite(f'matches_{name}.png', vis)
```

**Kriteria Penilaian:**
- Ratio test benar (3 poin)
- Mutual matching benar (3 poin)
- RANSAC homography benar (5 poin)
- Complete pipeline (2 poin)
- Testing dan visualization (2 poin)

### B3. Panorama Stitcher (10 poin)

Implementasikan panorama stitcher sederhana:

```python
class PanoramaStitcher:
    """
    Panorama stitcher untuk 2 atau lebih gambar
    """
    
    def __init__(self, feature_method: str = 'sift'):
        self.matcher = RobustFeatureMatcher(feature_method)
    
    def find_homography(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Find homography dari img2 ke img1
        
        Returns:
            H: 3x3 homography matrix
        """
        # TODO: Implementasi menggunakan matcher
        pass
    
    def compute_output_size(self, img1: np.ndarray, img2: np.ndarray,
                           H: np.ndarray) -> tuple:
        """
        Compute output canvas size dan offset
        
        Returns:
            (width, height), (offset_x, offset_y)
        """
        # TODO: Implementasi
        pass
    
    def warp_images(self, img1: np.ndarray, img2: np.ndarray,
                   H: np.ndarray, output_size: tuple, 
                   offset: tuple) -> tuple:
        """
        Warp both images onto common canvas
        
        Returns:
            warped_img1, warped_img2, mask1, mask2
        """
        # TODO: Implementasi
        pass
    
    def blend_images(self, img1: np.ndarray, img2: np.ndarray,
                    mask1: np.ndarray, mask2: np.ndarray,
                    method: str = 'average') -> np.ndarray:
        """
        Blend images in overlap region
        
        Methods:
        - 'simple': img1 takes priority
        - 'average': Simple averaging
        - 'feather': Distance-weighted blending
        - 'multiband': Laplacian pyramid blending
        """
        # TODO: Implementasi berbagai blending methods
        pass
    
    def stitch(self, images: list, blend_method: str = 'feather') -> np.ndarray:
        """
        Stitch multiple images into panorama
        
        Args:
            images: List of images (left to right order)
            blend_method: Blending method
            
        Returns:
            panorama: Stitched image
        """
        # TODO: Implementasi
        # Untuk 2 gambar: langsung stitch
        # Untuk >2 gambar: stitch secara berurutan
        pass


# Testing
def test_panorama():
    # Load atau create overlapping images
    # TODO: Load test images
    
    stitcher = PanoramaStitcher('sift')
    
    # Test different blending methods
    for method in ['simple', 'average', 'feather']:
        panorama = stitcher.stitch(images, blend_method=method)
        cv2.imwrite(f'panorama_{method}.png', panorama)
```

**Kriteria Penilaian:**
- Homography estimation benar (3 poin)
- Canvas size computation (2 poin)
- Image warping benar (2 poin)
- Blending (3 poin)

---

## Bagian C: Proyek Mini - Visual Odometry Sederhana (30 poin)

### Deskripsi Proyek

Implementasikan visual odometry sederhana menggunakan feature tracking:

```python
class SimpleVisualOdometry:
    """
    Simple visual odometry untuk estimasi gerakan kamera
    dari sequence gambar
    """
    
    def __init__(self, K: np.ndarray, feature_method: str = 'sift'):
        """
        Args:
            K: Camera intrinsic matrix (3x3)
            feature_method: Feature detector/descriptor
        """
        self.K = K
        self.matcher = RobustFeatureMatcher(feature_method)
        
        # Trajectory
        self.poses = [np.eye(4)]  # Start at origin
        self.trajectory = [(0, 0, 0)]  # (x, y, z) positions
    
    def estimate_motion(self, pts1: np.ndarray, pts2: np.ndarray) -> tuple:
        """
        Estimate camera motion dari matched points
        
        Args:
            pts1, pts2: Matched 2D points (N, 2)
            
        Returns:
            R: Rotation matrix (3x3)
            t: Translation vector (3,)
        """
        # TODO: Implementasi
        # 1. Compute essential matrix: E = K.T @ F @ K
        # 2. Decompose E ke R dan t
        # 3. Select correct solution (positive depth)
        pass
    
    def process_frame(self, img: np.ndarray) -> dict:
        """
        Process new frame dan update trajectory
        
        Returns:
            {
                'matches': number of matches,
                'inliers': number of inliers,
                'R': rotation,
                't': translation,
                'position': (x, y, z)
            }
        """
        # TODO: Implementasi
        pass
    
    def process_sequence(self, images: list) -> dict:
        """
        Process entire image sequence
        
        Returns:
            {
                'trajectory': [(x,y,z), ...],
                'poses': [4x4 matrix, ...],
                'frame_info': [dict, ...]
            }
        """
        # TODO: Implementasi
        pass
    
    def visualize_trajectory_2d(self) -> np.ndarray:
        """Visualize trajectory dari atas (bird's eye view)"""
        # TODO: Implementasi
        pass
    
    def visualize_trajectory_3d(self):
        """3D visualization dengan matplotlib"""
        # TODO: Implementasi
        pass


# Testing
def test_visual_odometry():
    # Define camera matrix
    K = np.array([
        [718.856, 0, 607.1928],
        [0, 718.856, 185.2157],
        [0, 0, 1]
    ])
    
    # Load image sequence
    # TODO: Load test sequence (atau gunakan synthetic)
    
    vo = SimpleVisualOdometry(K, 'sift')
    result = vo.process_sequence(images)
    
    # Visualize
    vo.visualize_trajectory_2d()
    vo.visualize_trajectory_3d()
    
    # Compare dengan ground truth jika ada
```

---

## Format Pengumpulan

```
tugas_bab_07/
├── laporan.pdf
├── teori/
│   └── jawaban_teori.md
├── implementasi/
│   ├── harris_detector.py      # B1
│   ├── robust_matcher.py       # B2
│   └── panorama_stitcher.py    # B3
├── project/
│   ├── visual_odometry.py      # C
│   └── outputs/
├── data/
│   └── test_images/
└── README.md
```

---

## Rubrik Penilaian

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| Teori (A) | 30% | Pemahaman konsep |
| Harris (B1) | 15% | Implementasi benar |
| Matcher (B2) | 15% | RANSAC dan pipeline benar |
| Panorama (B3) | 10% | Stitching dan blending |
| Visual Odometry (C) | 30% | Pipeline lengkap |

---

## Referensi

1. Harris & Stephens (1988) - Harris Corner Detector
2. Lowe (2004) - SIFT Paper
3. Rublee et al. (2011) - ORB Paper
4. Fischler & Bolles (1981) - RANSAC
5. Hartley & Zisserman - Multiple View Geometry

---

**Selamat mengerjakan! 🚀**
