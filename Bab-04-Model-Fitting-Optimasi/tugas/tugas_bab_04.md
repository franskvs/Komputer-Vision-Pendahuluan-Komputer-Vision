# TUGAS BAB 4: MODEL FITTING DAN OPTIMISASI

## 📋 Informasi Tugas

| Aspek | Detail |
|-------|--------|
| **Deadline** | 1 minggu setelah praktikum |
| **Format** | Jupyter Notebook (.ipynb) atau Python (.py) + Laporan PDF |
| **Pengumpulan** | Melalui platform e-learning |

---

## Tugas 1: Teori (25 poin)

### Soal 1.1 (8 poin)
Diberikan data points berikut:
```
x: [1, 2, 3, 4, 5]
y: [2.1, 3.9, 6.2, 7.8, 10.1]
```

a) Hitung parameter garis y = mx + c menggunakan Least Squares secara manual (tunjukkan langkah-langkah perhitungan).

b) Hitung Sum of Squared Errors (SSE) dari hasil fitting Anda.

c) Jika ditambahkan satu outlier (x=3, y=20), apa yang akan terjadi pada hasil fitting? Jelaskan secara kualitatif.

### Soal 1.2 (7 poin)
Tentang RANSAC:

a) Jika data Anda memiliki 60% inlier ratio dan Anda ingin probabilitas sukses 99%, berapa iterasi minimum yang diperlukan untuk:
   - Fitting garis (2 titik)
   - Fitting homography (4 titik)
   - Fitting fundamental matrix (8 titik)
   
   Gunakan formula: $N = \frac{\log(1-p)}{\log(1-w^n)}$

b) Jelaskan mengapa RANSAC tidak optimal untuk data dengan outlier ratio > 50%.

c) Sebutkan dan jelaskan 3 variasi RANSAC beserta kelebihannya.

### Soal 1.3 (5 poin)
Tentang Hough Transform:

a) Jelaskan mengapa kita menggunakan representasi $\rho = x\cos\theta + y\sin\theta$ untuk garis, bukan $y = mx + c$.

b) Berapa dimensi accumulator yang diperlukan untuk:
   - Deteksi garis
   - Deteksi lingkaran (radius tidak diketahui)
   - Deteksi ellipse (semua parameter tidak diketahui)

c) Bagaimana cara menangani noise dalam Hough Transform?

### Soal 1.4 (5 poin)
Tentang Optimisasi:

a) Jelaskan perbedaan antara Gradient Descent, Gauss-Newton, dan Levenberg-Marquardt.

b) Apa keuntungan menggunakan momentum dalam gradient descent?

c) Jelaskan trade-off antara L1 dan L2 regularization.

---

## Tugas 2: Coding - Robust Fitting Toolkit (35 poin)

### 2.1 RANSAC Implementation (15 poin)

```python
"""
Implementasikan RANSAC generik yang dapat digunakan untuk berbagai model
"""

import numpy as np
from abc import ABC, abstractmethod

class ModelEstimator(ABC):
    """Abstract base class untuk model estimator"""
    
    @property
    @abstractmethod
    def min_samples(self):
        """Minimum samples needed to fit model"""
        pass
    
    @abstractmethod
    def fit(self, data):
        """
        Fit model ke data
        
        Parameters:
            data: array dengan data points
        
        Returns:
            model_params: parameter model
        """
        pass
    
    @abstractmethod
    def residuals(self, model_params, data):
        """
        Hitung residuals untuk setiap data point
        
        Parameters:
            model_params: parameter model
            data: array dengan data points
        
        Returns:
            residuals: array of residuals
        """
        pass


class LineEstimator(ModelEstimator):
    """Estimator untuk garis 2D"""
    
    @property
    def min_samples(self):
        return 2
    
    def fit(self, data):
        """
        Fit line y = mx + c
        
        Parameters:
            data: (N, 2) array of (x, y) points
        
        Returns:
            (m, c): slope and intercept
        """
        # Implementasi Anda
        pass
    
    def residuals(self, model_params, data):
        """
        Hitung perpendicular distance ke line
        """
        # Implementasi Anda
        pass


class CircleEstimator(ModelEstimator):
    """Estimator untuk lingkaran"""
    
    @property
    def min_samples(self):
        return 3
    
    def fit(self, data):
        """
        Fit circle (x-a)^2 + (y-b)^2 = r^2
        
        Parameters:
            data: (N, 2) array of (x, y) points
        
        Returns:
            (a, b, r): center and radius
        """
        # Implementasi Anda - gunakan algebraic distance
        pass
    
    def residuals(self, model_params, data):
        """
        Hitung distance ke circle boundary
        """
        # Implementasi Anda
        pass


class HomographyEstimator(ModelEstimator):
    """Estimator untuk homography"""
    
    @property
    def min_samples(self):
        return 4
    
    def fit(self, data):
        """
        Fit homography H
        
        Parameters:
            data: (N, 4) array of (x, y, x', y') correspondences
        
        Returns:
            H: (3, 3) homography matrix
        """
        # Implementasi Anda - gunakan DLT
        pass
    
    def residuals(self, model_params, data):
        """
        Hitung symmetric transfer error
        """
        # Implementasi Anda
        pass


class RANSAC:
    """
    Generic RANSAC implementation
    """
    
    def __init__(self, estimator, threshold=5.0, p_success=0.99, max_iterations=1000):
        """
        Parameters:
            estimator: ModelEstimator instance
            threshold: inlier threshold
            p_success: desired probability of success
            max_iterations: maximum number of iterations
        """
        self.estimator = estimator
        self.threshold = threshold
        self.p_success = p_success
        self.max_iterations = max_iterations
    
    def calculate_iterations(self, inlier_ratio):
        """
        Calculate required iterations based on inlier ratio
        """
        # Implementasi Anda
        pass
    
    def fit(self, data, adaptive=True):
        """
        Fit model to data using RANSAC
        
        Parameters:
            data: input data
            adaptive: whether to adaptively update iteration count
        
        Returns:
            best_model: best model parameters
            inliers: boolean mask of inliers
            info: dictionary with fitting information
        """
        # Implementasi Anda
        pass


# Test
if __name__ == "__main__":
    np.random.seed(42)
    
    # Test Line RANSAC
    print("Testing Line RANSAC...")
    n_inliers = 80
    n_outliers = 20
    
    # Generate inliers
    x_inliers = np.random.uniform(0, 100, n_inliers)
    y_inliers = 2 * x_inliers + 10 + np.random.normal(0, 3, n_inliers)
    
    # Generate outliers
    x_outliers = np.random.uniform(0, 100, n_outliers)
    y_outliers = np.random.uniform(0, 300, n_outliers)
    
    data = np.column_stack([
        np.concatenate([x_inliers, x_outliers]),
        np.concatenate([y_inliers, y_outliers])
    ])
    
    line_estimator = LineEstimator()
    ransac = RANSAC(line_estimator, threshold=10)
    model, inliers, info = ransac.fit(data)
    
    print(f"True: m=2, c=10")
    print(f"Estimated: m={model[0]:.2f}, c={model[1]:.2f}")
    print(f"Inliers: {info['n_inliers']}/{len(data)}")
    
    # Test Circle RANSAC
    print("\nTesting Circle RANSAC...")
    # Generate circle data
    theta = np.random.uniform(0, 2*np.pi, 80)
    r_true, cx_true, cy_true = 50, 100, 100
    x_circle = cx_true + r_true * np.cos(theta) + np.random.normal(0, 2, 80)
    y_circle = cy_true + r_true * np.sin(theta) + np.random.normal(0, 2, 80)
    
    # Add outliers
    x_out = np.random.uniform(0, 200, 20)
    y_out = np.random.uniform(0, 200, 20)
    
    circle_data = np.column_stack([
        np.concatenate([x_circle, x_out]),
        np.concatenate([y_circle, y_out])
    ])
    
    circle_estimator = CircleEstimator()
    ransac_circle = RANSAC(circle_estimator, threshold=5)
    model_c, inliers_c, info_c = ransac_circle.fit(circle_data)
    
    print(f"True: center=({cx_true}, {cy_true}), r={r_true}")
    print(f"Estimated: center=({model_c[0]:.2f}, {model_c[1]:.2f}), r={model_c[2]:.2f}")
```

### 2.2 Hough Transform Implementation (10 poin)

```python
"""
Implementasikan Hough Transform untuk berbagai bentuk
"""

def hough_line_transform(edge_image, theta_bins=180, rho_bins=None):
    """
    Hough Transform untuk garis
    
    Parameters:
        edge_image: binary edge image
        theta_bins: number of theta bins
        rho_bins: number of rho bins (auto if None)
    
    Returns:
        accumulator: Hough accumulator
        thetas: theta values
        rhos: rho values
    """
    # Implementasi Anda
    pass


def hough_circle_transform(edge_image, r_min, r_max, r_step=1, gradient=None):
    """
    Hough Transform untuk lingkaran
    
    Parameters:
        edge_image: binary edge image
        r_min, r_max: radius range
        r_step: radius step
        gradient: optional gradient direction image untuk voting lebih akurat
    
    Returns:
        accumulator: 3D accumulator (a, b, r)
        params: (a_values, b_values, r_values)
    """
    # Implementasi Anda
    pass


def find_peaks(accumulator, threshold=0.5, min_distance=10):
    """
    Find peaks in Hough accumulator
    
    Parameters:
        accumulator: Hough accumulator array
        threshold: fraction of max value
        min_distance: minimum distance between peaks
    
    Returns:
        peaks: list of peak coordinates
    """
    # Implementasi Anda - gunakan non-maximum suppression
    pass


def visualize_hough_space(accumulator, thetas, rhos, title="Hough Space"):
    """
    Visualisasi Hough accumulator
    """
    # Implementasi Anda
    pass
```

### 2.3 Iteratively Reweighted Least Squares (10 poin)

```python
"""
Implementasikan IRLS untuk robust regression
"""

def huber_weights(residuals, delta=1.345):
    """
    Compute weights for Huber loss
    
    Parameters:
        residuals: array of residuals
        delta: threshold
    
    Returns:
        weights: array of weights
    """
    # Implementasi Anda
    # w = 1 for |r| <= delta
    # w = delta / |r| for |r| > delta
    pass


def tukey_weights(residuals, c=4.685):
    """
    Compute weights for Tukey's biweight
    
    Parameters:
        residuals: array of residuals
        c: tuning constant
    
    Returns:
        weights: array of weights
    """
    # Implementasi Anda
    # w = (1 - (r/c)^2)^2 for |r| <= c
    # w = 0 for |r| > c
    pass


def irls_line_fit(points, weight_func=huber_weights, max_iter=100, tol=1e-6):
    """
    Fit line using Iteratively Reweighted Least Squares
    
    Parameters:
        points: (N, 2) array
        weight_func: function to compute weights from residuals
        max_iter: maximum iterations
        tol: convergence tolerance
    
    Returns:
        m, c: line parameters
        weights: final weights
        history: list of parameters per iteration
    """
    # Implementasi Anda
    # 1. Initialize with OLS
    # 2. Loop:
    #    a. Compute residuals
    #    b. Compute weights
    #    c. Solve weighted least squares
    #    d. Check convergence
    pass


# Test
if __name__ == "__main__":
    # Generate data with outliers
    np.random.seed(42)
    
    x = np.random.uniform(0, 100, 100)
    y = 2 * x + 10 + np.random.normal(0, 5, 100)
    
    # Add outliers
    outlier_idx = np.random.choice(100, 20, replace=False)
    y[outlier_idx] = np.random.uniform(-50, 200, 20)
    
    points = np.column_stack([x, y])
    
    # Compare methods
    m_ols, c_ols = fit_line_least_squares(points)
    m_huber, c_huber, _, _ = irls_line_fit(points, huber_weights)
    m_tukey, c_tukey, _, _ = irls_line_fit(points, tukey_weights)
    
    print(f"True: m=2, c=10")
    print(f"OLS: m={m_ols:.3f}, c={c_ols:.3f}")
    print(f"Huber: m={m_huber:.3f}, c={c_huber:.3f}")
    print(f"Tukey: m={m_tukey:.3f}, c={c_tukey:.3f}")
```

---

## Tugas 3: Mini Project - Robust Feature Matching (40 poin)

### Deskripsi
Buat sistem untuk melakukan feature matching antara dua gambar dan estimasi homography dengan RANSAC.

### Requirements

```python
"""
Robust Feature Matching and Homography Estimation
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

class RobustFeatureMatcher:
    """
    Class untuk feature matching dan homography estimation
    """
    
    def __init__(self, detector='sift', matcher='bf'):
        """
        Parameters:
            detector: 'sift', 'orb', 'akaze'
            matcher: 'bf' (brute force), 'flann'
        """
        self.detector = self._create_detector(detector)
        self.matcher = self._create_matcher(matcher, detector)
        self.img1 = None
        self.img2 = None
        self.kp1, self.des1 = None, None
        self.kp2, self.des2 = None, None
        self.matches = None
        self.homography = None
        self.inliers = None
    
    def _create_detector(self, detector):
        """Create feature detector"""
        # Implementasi Anda
        pass
    
    def _create_matcher(self, matcher, detector):
        """Create feature matcher"""
        # Implementasi Anda
        pass
    
    def detect_features(self, img1, img2):
        """
        Detect keypoints and compute descriptors
        
        Returns:
            n_kp1, n_kp2: number of keypoints in each image
        """
        # Implementasi Anda
        pass
    
    def match_features(self, ratio_threshold=0.75):
        """
        Match features using ratio test
        
        Parameters:
            ratio_threshold: Lowe's ratio threshold
        
        Returns:
            n_matches: number of good matches
        """
        # Implementasi Anda
        pass
    
    def estimate_homography_ransac(self, threshold=5.0, max_iterations=1000):
        """
        Estimate homography using custom RANSAC implementation
        
        Returns:
            H: homography matrix
            n_inliers: number of inliers
        """
        # Implementasi Anda - gunakan implementasi RANSAC Anda sendiri
        pass
    
    def estimate_homography_opencv(self, threshold=5.0):
        """
        Estimate homography using OpenCV RANSAC
        
        Returns:
            H: homography matrix
            n_inliers: number of inliers
        """
        # Implementasi Anda - untuk perbandingan
        pass
    
    def warp_image(self, which='second'):
        """
        Warp image using estimated homography
        
        Parameters:
            which: 'first' or 'second'
        
        Returns:
            warped: warped image
        """
        # Implementasi Anda
        pass
    
    def stitch_images(self, blend=True):
        """
        Stitch two images using estimated homography
        
        Parameters:
            blend: whether to blend overlapping regions
        
        Returns:
            panorama: stitched image
        """
        # Implementasi Anda
        pass
    
    def visualize_matches(self, show_inliers_only=False):
        """
        Visualize matches between images
        """
        # Implementasi Anda
        pass
    
    def visualize_homography(self):
        """
        Visualize homography by drawing transformed rectangle
        """
        # Implementasi Anda
        pass
    
    def evaluate_homography(self):
        """
        Evaluate homography quality
        
        Returns:
            metrics: dict with evaluation metrics
                - reprojection_error: mean reprojection error
                - inlier_ratio: fraction of inliers
                - symmetry_error: error from inverse transform
        """
        # Implementasi Anda
        pass
    
    def compare_ransac_implementations(self, n_trials=10):
        """
        Compare custom vs OpenCV RANSAC
        
        Returns:
            comparison: dict with comparison results
        """
        # Implementasi Anda
        pass


class MultiImageStitcher:
    """
    Class untuk stitching multiple images
    """
    
    def __init__(self, detector='sift'):
        self.detector = detector
        self.images = []
        self.homographies = []
    
    def add_image(self, image):
        """Add image to collection"""
        # Implementasi Anda
        pass
    
    def compute_pairwise_homographies(self):
        """
        Compute homographies between adjacent images
        """
        # Implementasi Anda
        pass
    
    def stitch_all(self, reference_idx=None):
        """
        Stitch all images into panorama
        
        Parameters:
            reference_idx: index of reference image (middle if None)
        
        Returns:
            panorama: stitched panorama
        """
        # Implementasi Anda
        pass


# Demo
if __name__ == "__main__":
    # Load two images
    img1 = cv2.imread('image1.jpg')
    img2 = cv2.imread('image2.jpg')
    
    if img1 is None or img2 is None:
        print("Please provide test images")
        exit()
    
    # Create matcher
    matcher = RobustFeatureMatcher(detector='sift')
    
    # Detect and match
    n_kp1, n_kp2 = matcher.detect_features(img1, img2)
    print(f"Keypoints: {n_kp1}, {n_kp2}")
    
    n_matches = matcher.match_features(ratio_threshold=0.75)
    print(f"Good matches: {n_matches}")
    
    # Estimate homography
    H, n_inliers = matcher.estimate_homography_ransac()
    print(f"Inliers: {n_inliers}")
    
    # Evaluate
    metrics = matcher.evaluate_homography()
    print(f"Reprojection error: {metrics['reprojection_error']:.2f} pixels")
    
    # Visualize
    matcher.visualize_matches(show_inliers_only=True)
    matcher.visualize_homography()
    
    # Stitch
    panorama = matcher.stitch_images(blend=True)
    
    plt.figure(figsize=(15, 5))
    plt.imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
    plt.title('Panorama')
    plt.axis('off')
    plt.show()
```

### Kriteria Penilaian Mini Project

| Kriteria | Poin |
|----------|------|
| Feature detection & matching | 8 |
| Custom RANSAC implementation | 10 |
| Homography estimation accurate | 8 |
| Image warping & stitching | 8 |
| Visualization & evaluation | 6 |
| **Bonus: Multi-image stitching** | +10 |

---

## Rubrik Penilaian Total

| Komponen | Poin |
|----------|------|
| Tugas 1: Teori | 25 |
| Tugas 2: Coding | 35 |
| Tugas 3: Mini Project | 40 |
| **Total** | **100** |
| Bonus | +10 |

---

## Ketentuan Pengumpulan

1. **Nama file**: `Tugas4_NIM_Nama.zip`
2. **Isi ZIP**:
   - `tugas1_teori.pdf` - Jawaban teori
   - `tugas2_ransac.py` - RANSAC implementation
   - `tugas2_hough.py` - Hough Transform
   - `tugas2_irls.py` - IRLS implementation
   - `mini_project/` - Folder mini project
   - `README.md` - Dokumentasi
   - `sample_outputs/` - Contoh hasil
3. **Keterlambatan**: -10 poin per hari

---

## Tips

1. Untuk RANSAC, pastikan minimal sample cukup untuk menentukan model secara unik
2. Gunakan normalization untuk meningkatkan stabilitas numerik
3. Test dengan data synthetic dulu sebelum real images
4. Untuk homography, symmetric transfer error lebih robust
5. Visualisasi intermediate results untuk debugging

---

**Selamat mengerjakan!** 🎉
