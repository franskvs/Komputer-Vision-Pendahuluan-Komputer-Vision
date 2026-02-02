"""
PRAKTIKUM BAB 4: MODEL FITTING DAN OPTIMISASI
==============================================

Tujuan:
1. Mengimplementasikan berbagai metode fitting (Least Squares, RANSAC)
2. Memahami Hough Transform untuk deteksi garis dan lingkaran
3. Menerapkan berbagai algoritma optimisasi
4. Membandingkan metode robust vs non-robust

Kebutuhan:
- Python 3.8+
- OpenCV (cv2)
- NumPy
- Matplotlib
- SciPy
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.ndimage import rotate
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# BAGIAN 1: LEAST SQUARES FITTING
# ============================================================

print("=" * 60)
print("BAGIAN 1: LEAST SQUARES FITTING")
print("=" * 60)

def generate_line_data(n_points=50, noise_std=5, outlier_ratio=0):
    """
    Generate synthetic line data dengan noise dan outliers
    
    Parameters:
        n_points: jumlah total points
        noise_std: standard deviation noise
        outlier_ratio: rasio outliers (0-1)
    
    Returns:
        points: (N, 2) array
        true_params: (m, c) parameter sebenarnya
    """
    # True line: y = 2x + 10
    true_m, true_c = 2, 10
    
    x = np.random.uniform(0, 100, n_points)
    y = true_m * x + true_c + np.random.normal(0, noise_std, n_points)
    
    # Add outliers
    n_outliers = int(n_points * outlier_ratio)
    if n_outliers > 0:
        outlier_idx = np.random.choice(n_points, n_outliers, replace=False)
        y[outlier_idx] = np.random.uniform(y.min() - 50, y.max() + 50, n_outliers)
    
    points = np.column_stack([x, y])
    return points, (true_m, true_c)


def fit_line_least_squares(points):
    """
    Fit line y = mx + c menggunakan Ordinary Least Squares
    
    Parameters:
        points: (N, 2) array of (x, y) points
    
    Returns:
        m, c: slope and intercept
    """
    x = points[:, 0]
    y = points[:, 1]
    
    # Design matrix A: [x, 1]
    A = np.column_stack([x, np.ones(len(x))])
    
    # Solve A @ [m, c].T = y
    params, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
    
    return params[0], params[1]


def fit_line_total_least_squares(points):
    """
    Total Least Squares - minimize perpendicular distance
    
    Parameters:
        points: (N, 2) array
    
    Returns:
        a, b, c: coefficients for ax + by + c = 0
    """
    # Center data
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    
    # SVD
    U, S, Vt = np.linalg.svd(centered)
    
    # Line direction is first singular vector
    # Normal direction is second singular vector
    normal = Vt[-1]  # Last row
    a, b = normal
    c = -(a * centroid[0] + b * centroid[1])
    
    return a, b, c


def fit_line_weighted_least_squares(points, weights):
    """
    Weighted Least Squares
    
    Parameters:
        points: (N, 2) array
        weights: (N,) array of weights
    
    Returns:
        m, c: slope and intercept
    """
    x = points[:, 0]
    y = points[:, 1]
    
    W = np.diag(weights)
    A = np.column_stack([x, np.ones(len(x))])
    
    # (A.T @ W @ A)^-1 @ A.T @ W @ y
    params = np.linalg.solve(A.T @ W @ A, A.T @ W @ y)
    
    return params[0], params[1]


def demo_least_squares():
    """Demo berbagai metode least squares"""
    # Data dengan noise
    np.random.seed(42)
    points, (true_m, true_c) = generate_line_data(50, noise_std=10)
    
    # Fit dengan OLS
    m_ols, c_ols = fit_line_least_squares(points)
    
    # Fit dengan Total LS
    a, b, c = fit_line_total_least_squares(points)
    m_tls = -a / b
    c_tls = -c / b
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot points
    ax.scatter(points[:, 0], points[:, 1], c='blue', alpha=0.6, label='Data points')
    
    # Plot lines
    x_line = np.array([0, 100])
    
    ax.plot(x_line, true_m * x_line + true_c, 'g-', linewidth=2, label=f'True: y = {true_m}x + {true_c}')
    ax.plot(x_line, m_ols * x_line + c_ols, 'r--', linewidth=2, label=f'OLS: y = {m_ols:.2f}x + {c_ols:.2f}')
    ax.plot(x_line, m_tls * x_line + c_tls, 'm:', linewidth=2, label=f'TLS: y = {m_tls:.2f}x + {c_tls:.2f}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Least Squares Line Fitting')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output_least_squares.png', dpi=150)
    plt.show()
    
    print(f"✅ Least Squares demo selesai!")
    print(f"   True parameters: m={true_m}, c={true_c}")
    print(f"   OLS parameters:  m={m_ols:.3f}, c={c_ols:.3f}")
    print(f"   TLS parameters:  m={m_tls:.3f}, c={c_tls:.3f}")


# ============================================================
# BAGIAN 2: RANSAC (Random Sample Consensus)
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 2: RANSAC (Random Sample Consensus)")
print("=" * 60)

def fit_line_ransac(points, threshold=5.0, iterations=1000, p_success=0.99):
    """
    RANSAC line fitting
    
    Parameters:
        points: (N, 2) array
        threshold: inlier distance threshold
        iterations: max iterations
        p_success: desired probability of success
    
    Returns:
        best_params: (m, c)
        inliers: boolean mask
        info: dict dengan info tambahan
    """
    best_params = None
    best_inliers = None
    best_count = 0
    
    N = len(points)
    
    for i in range(iterations):
        # 1. Random sample 2 points
        idx = np.random.choice(N, 2, replace=False)
        p1, p2 = points[idx]
        
        # 2. Fit line through 2 points
        dx = p2[0] - p1[0]
        if abs(dx) < 1e-10:  # Avoid vertical lines
            continue
        
        m = (p2[1] - p1[1]) / dx
        c = p1[1] - m * p1[0]
        
        # 3. Calculate distances to line
        # Distance from point (x0, y0) to line ax + by + c = 0 is |ax0 + by0 + c| / sqrt(a^2 + b^2)
        # For y = mx + c, rewrite as mx - y + c = 0, so a=m, b=-1
        distances = np.abs(m * points[:, 0] - points[:, 1] + c) / np.sqrt(m**2 + 1)
        
        # 4. Count inliers
        inliers = distances < threshold
        count = np.sum(inliers)
        
        # 5. Update best if better
        if count > best_count:
            best_count = count
            best_params = (m, c)
            best_inliers = inliers
    
    # 6. Refit using all inliers
    if best_inliers is not None and np.sum(best_inliers) > 2:
        inlier_points = points[best_inliers]
        m, c = fit_line_least_squares(inlier_points)
        best_params = (m, c)
    
    info = {
        'inlier_ratio': best_count / N,
        'n_inliers': best_count
    }
    
    return best_params, best_inliers, info


def compare_ols_vs_ransac():
    """Bandingkan OLS vs RANSAC dengan outliers"""
    np.random.seed(42)
    
    # Data dengan 30% outliers
    points, (true_m, true_c) = generate_line_data(100, noise_std=5, outlier_ratio=0.3)
    
    # OLS
    m_ols, c_ols = fit_line_least_squares(points)
    
    # RANSAC
    (m_ransac, c_ransac), inliers, info = fit_line_ransac(points, threshold=10)
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot OLS
    ax = axes[0]
    ax.scatter(points[:, 0], points[:, 1], c='blue', alpha=0.6)
    x_line = np.array([0, 100])
    ax.plot(x_line, true_m * x_line + true_c, 'g-', linewidth=2, label=f'True')
    ax.plot(x_line, m_ols * x_line + c_ols, 'r--', linewidth=2, label=f'OLS')
    ax.set_title('Ordinary Least Squares (Affected by Outliers)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot RANSAC
    ax = axes[1]
    ax.scatter(points[inliers, 0], points[inliers, 1], c='blue', alpha=0.6, label='Inliers')
    ax.scatter(points[~inliers, 0], points[~inliers, 1], c='red', alpha=0.6, label='Outliers')
    ax.plot(x_line, true_m * x_line + true_c, 'g-', linewidth=2, label=f'True')
    ax.plot(x_line, m_ransac * x_line + c_ransac, 'b--', linewidth=2, label=f'RANSAC')
    ax.set_title(f'RANSAC (Inlier ratio: {info["inlier_ratio"]:.1%})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output_ols_vs_ransac.png', dpi=150)
    plt.show()
    
    print(f"✅ OLS vs RANSAC comparison selesai!")
    print(f"   True:   m={true_m}, c={true_c}")
    print(f"   OLS:    m={m_ols:.3f}, c={c_ols:.3f} (error affected by outliers)")
    print(f"   RANSAC: m={m_ransac:.3f}, c={c_ransac:.3f}")


# ============================================================
# BAGIAN 3: HOUGH TRANSFORM
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 3: HOUGH TRANSFORM")
print("=" * 60)

def hough_line_transform_manual(edge_image, theta_resolution=1, rho_resolution=1):
    """
    Implementasi manual Hough Transform untuk garis
    
    Parameters:
        edge_image: binary edge image
        theta_resolution: resolution untuk theta (degrees)
        rho_resolution: resolution untuk rho (pixels)
    
    Returns:
        accumulator: Hough space accumulator
        thetas: array of theta values
        rhos: array of rho values
    """
    height, width = edge_image.shape
    
    # Diagonal length
    diag = int(np.sqrt(height**2 + width**2))
    
    # Rho range: -diag to diag
    rhos = np.arange(-diag, diag + 1, rho_resolution)
    
    # Theta range: 0 to 180 degrees
    thetas = np.deg2rad(np.arange(0, 180, theta_resolution))
    
    # Initialize accumulator
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.int32)
    
    # Get edge points
    y_idx, x_idx = np.nonzero(edge_image)
    
    # Precompute cos and sin
    cos_thetas = np.cos(thetas)
    sin_thetas = np.sin(thetas)
    
    # Vote
    for i in range(len(x_idx)):
        x = x_idx[i]
        y = y_idx[i]
        
        for t_idx in range(len(thetas)):
            rho = x * cos_thetas[t_idx] + y * sin_thetas[t_idx]
            rho_idx = int((rho + diag) / rho_resolution)
            
            if 0 <= rho_idx < len(rhos):
                accumulator[rho_idx, t_idx] += 1
    
    return accumulator, thetas, rhos


def detect_lines_hough(image, threshold=100):
    """
    Deteksi garis menggunakan Hough Transform (OpenCV)
    
    Parameters:
        image: input grayscale image
        threshold: minimum votes untuk deteksi
    
    Returns:
        lines: list of (rho, theta) tuples
    """
    # Edge detection
    edges = cv2.Canny(image, 50, 150)
    
    # Hough Transform
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold)
    
    return lines, edges


def detect_lines_probabilistic_hough(image, threshold=50, min_line_length=50, max_line_gap=10):
    """
    Deteksi garis menggunakan Probabilistic Hough Transform
    
    Returns:
        lines: list of ((x1, y1), (x2, y2)) line segments
    """
    edges = cv2.Canny(image, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, 
                           minLineLength=min_line_length, 
                           maxLineGap=max_line_gap)
    return lines, edges


def demo_hough_lines():
    """Demonstrasi Hough Transform untuk deteksi garis"""
    # Buat gambar dengan garis-garis
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw beberapa garis
    cv2.line(img, (50, 50), (350, 100), 255, 2)
    cv2.line(img, (50, 200), (350, 200), 255, 2)
    cv2.line(img, (200, 50), (200, 350), 255, 2)
    cv2.line(img, (50, 350), (350, 50), 255, 2)
    
    # Add some noise
    noise = np.random.randint(0, 30, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    # Deteksi dengan standard Hough
    lines_std, edges = detect_lines_hough(img, threshold=80)
    
    # Deteksi dengan probabilistic Hough
    lines_prob, _ = detect_lines_probabilistic_hough(img)
    
    # Manual Hough (untuk visualisasi accumulator)
    accumulator, thetas, rhos = hough_line_transform_manual(edges)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    # Original
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    # Accumulator space
    axes[0, 1].imshow(accumulator, cmap='hot', aspect='auto',
                      extent=[np.rad2deg(thetas[0]), np.rad2deg(thetas[-1]), 
                             rhos[-1], rhos[0]])
    axes[0, 1].set_xlabel('Theta (degrees)')
    axes[0, 1].set_ylabel('Rho (pixels)')
    axes[0, 1].set_title('Hough Space (Accumulator)')
    
    # Standard Hough result
    result_std = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if lines_std is not None:
        for line in lines_std:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(result_std, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    axes[1, 0].imshow(cv2.cvtColor(result_std, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f'Standard Hough ({len(lines_std) if lines_std is not None else 0} lines)')
    axes[1, 0].axis('off')
    
    # Probabilistic Hough result
    result_prob = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if lines_prob is not None:
        for line in lines_prob:
            x1, y1, x2, y2 = line[0]
            cv2.line(result_prob, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    axes[1, 1].imshow(cv2.cvtColor(result_prob, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f'Probabilistic Hough ({len(lines_prob) if lines_prob is not None else 0} lines)')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_hough_lines.png', dpi=150)
    plt.show()
    
    print(f"✅ Hough Transform demo selesai!")


def demo_hough_circles():
    """Demonstrasi Hough Transform untuk deteksi lingkaran"""
    # Buat gambar dengan lingkaran
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw beberapa lingkaran
    cv2.circle(img, (100, 100), 40, 255, 2)
    cv2.circle(img, (300, 100), 30, 255, 2)
    cv2.circle(img, (200, 250), 60, 255, 2)
    cv2.circle(img, (100, 320), 25, 255, 2)
    
    # Add noise
    noise = np.random.randint(0, 20, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    # Blur untuk mengurangi noise
    img_blur = cv2.GaussianBlur(img, (5, 5), 1)
    
    # Deteksi lingkaran
    circles = cv2.HoughCircles(
        img_blur, 
        cv2.HOUGH_GRADIENT, 
        dp=1,           # Inverse ratio of resolution
        minDist=50,     # Minimum distance between circles
        param1=50,      # Upper threshold for Canny
        param2=30,      # Accumulator threshold
        minRadius=20,   # Minimum radius
        maxRadius=80    # Maximum radius
    )
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0]:
            x, y, r = circle
            # Draw circle
            cv2.circle(result, (x, y), r, (0, 255, 0), 2)
            # Draw center
            cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
    
    axes[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f'Detected Circles ({len(circles[0]) if circles is not None else 0})')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_hough_circles.png', dpi=150)
    plt.show()
    
    print(f"✅ Hough Circles demo selesai!")


# ============================================================
# BAGIAN 4: HOMOGRAPHY ESTIMATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 4: HOMOGRAPHY ESTIMATION")
print("=" * 60)

def compute_homography_dlt(src_pts, dst_pts):
    """
    Compute homography using Direct Linear Transform (DLT)
    
    Parameters:
        src_pts: (N, 2) source points (minimal 4)
        dst_pts: (N, 2) destination points
    
    Returns:
        H: (3, 3) homography matrix
    """
    N = len(src_pts)
    if N < 4:
        raise ValueError("Need at least 4 point correspondences")
    
    # Build matrix A (2N x 9)
    A = []
    for i in range(N):
        x, y = src_pts[i]
        xp, yp = dst_pts[i]
        
        A.append([-x, -y, -1, 0, 0, 0, x*xp, y*xp, xp])
        A.append([0, 0, 0, -x, -y, -1, x*yp, y*yp, yp])
    
    A = np.array(A)
    
    # SVD
    U, S, Vt = np.linalg.svd(A)
    
    # Last row of Vt is solution
    H = Vt[-1].reshape(3, 3)
    
    # Normalize
    H = H / H[2, 2]
    
    return H


def estimate_homography_ransac(src_pts, dst_pts, threshold=5.0, iterations=1000):
    """
    Estimate homography using RANSAC
    
    Parameters:
        src_pts: (N, 2) source points
        dst_pts: (N, 2) destination points
        threshold: inlier threshold (pixels)
        iterations: max RANSAC iterations
    
    Returns:
        H: (3, 3) homography matrix
        inliers: boolean mask
    """
    best_H = None
    best_inliers = None
    best_count = 0
    
    N = len(src_pts)
    
    for _ in range(iterations):
        # Sample 4 correspondences
        idx = np.random.choice(N, 4, replace=False)
        
        try:
            # Compute homography from 4 points
            H = compute_homography_dlt(src_pts[idx], dst_pts[idx])
            
            # Transform all source points
            src_h = np.column_stack([src_pts, np.ones(N)])
            projected = (H @ src_h.T).T
            projected = projected[:, :2] / projected[:, 2:3]
            
            # Compute errors
            errors = np.linalg.norm(projected - dst_pts, axis=1)
            
            # Count inliers
            inliers = errors < threshold
            count = np.sum(inliers)
            
            if count > best_count:
                best_count = count
                best_inliers = inliers
                best_H = H
                
        except np.linalg.LinAlgError:
            continue
    
    # Refit with all inliers
    if best_inliers is not None and np.sum(best_inliers) >= 4:
        H = compute_homography_dlt(src_pts[best_inliers], dst_pts[best_inliers])
        return H, best_inliers
    
    return best_H, best_inliers


def demo_homography():
    """Demonstrasi estimasi homography dengan RANSAC"""
    np.random.seed(42)
    
    # Definisikan source points (persegi)
    src_pts = np.array([
        [100, 100], [300, 100], [300, 300], [100, 300],
        [150, 150], [250, 150], [250, 250], [150, 250],
        [200, 125], [200, 275], [125, 200], [275, 200]
    ], dtype=np.float64)
    
    # True homography (rotation + perspective)
    H_true = np.array([
        [0.9, -0.1, 50],
        [0.2, 0.85, 30],
        [0.0003, 0.0002, 1]
    ])
    
    # Transform points
    src_h = np.column_stack([src_pts, np.ones(len(src_pts))])
    dst_h = (H_true @ src_h.T).T
    dst_pts = dst_h[:, :2] / dst_h[:, 2:3]
    
    # Add noise
    dst_pts += np.random.normal(0, 2, dst_pts.shape)
    
    # Add outliers
    n_outliers = 3
    outlier_idx = np.random.choice(len(dst_pts), n_outliers, replace=False)
    dst_pts[outlier_idx] += np.random.uniform(-100, 100, (n_outliers, 2))
    
    # Estimate with DLT (all points)
    H_dlt = compute_homography_dlt(src_pts, dst_pts)
    
    # Estimate with RANSAC
    H_ransac, inliers = estimate_homography_ransac(src_pts, dst_pts)
    
    # Verify using OpenCV
    H_cv2, mask_cv2 = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Source points
    ax = axes[0]
    ax.scatter(src_pts[:, 0], src_pts[:, 1], c='blue', s=100, label='Source')
    ax.set_title('Source Points')
    ax.set_xlim(0, 400)
    ax.set_ylim(400, 0)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # DLT result
    ax = axes[1]
    projected_dlt = (H_dlt @ src_h.T).T
    projected_dlt = projected_dlt[:, :2] / projected_dlt[:, 2:3]
    
    ax.scatter(dst_pts[:, 0], dst_pts[:, 1], c='green', s=100, marker='x', label='Destination')
    ax.scatter(projected_dlt[:, 0], projected_dlt[:, 1], c='red', s=50, label='DLT projection')
    ax.set_title('DLT (affected by outliers)')
    ax.set_xlim(0, 400)
    ax.set_ylim(400, 0)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # RANSAC result
    ax = axes[2]
    projected_ransac = (H_ransac @ src_h.T).T
    projected_ransac = projected_ransac[:, :2] / projected_ransac[:, 2:3]
    
    ax.scatter(dst_pts[inliers, 0], dst_pts[inliers, 1], c='green', s=100, marker='x', label='Inliers')
    ax.scatter(dst_pts[~inliers, 0], dst_pts[~inliers, 1], c='orange', s=100, marker='x', label='Outliers')
    ax.scatter(projected_ransac[:, 0], projected_ransac[:, 1], c='blue', s=50, label='RANSAC projection')
    ax.set_title(f'RANSAC ({np.sum(inliers)} inliers)')
    ax.set_xlim(0, 400)
    ax.set_ylim(400, 0)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('output_homography.png', dpi=150)
    plt.show()
    
    # Print errors
    err_dlt = np.mean(np.linalg.norm(projected_dlt - dst_pts, axis=1))
    err_ransac = np.mean(np.linalg.norm(projected_ransac[inliers] - dst_pts[inliers], axis=1))
    
    print(f"✅ Homography estimation demo selesai!")
    print(f"   DLT reprojection error (all): {err_dlt:.2f} pixels")
    print(f"   RANSAC reprojection error (inliers): {err_ransac:.2f} pixels")


# ============================================================
# BAGIAN 5: GRADIENT DESCENT OPTIMIZATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 5: GRADIENT DESCENT OPTIMIZATION")
print("=" * 60)

def gradient_descent(f, grad_f, x0, learning_rate=0.01, max_iter=1000, tol=1e-6):
    """
    Basic gradient descent
    
    Parameters:
        f: objective function
        grad_f: gradient function
        x0: initial point
        learning_rate: step size
        max_iter: maximum iterations
        tol: convergence tolerance
    
    Returns:
        x: optimal point
        history: list of (x, f(x)) tuples
    """
    x = np.array(x0, dtype=np.float64)
    history = [(x.copy(), f(x))]
    
    for _ in range(max_iter):
        grad = grad_f(x)
        x_new = x - learning_rate * grad
        
        history.append((x_new.copy(), f(x_new)))
        
        if np.linalg.norm(x_new - x) < tol:
            break
        
        x = x_new
    
    return x, history


def gradient_descent_momentum(f, grad_f, x0, learning_rate=0.01, momentum=0.9, 
                              max_iter=1000, tol=1e-6):
    """Gradient descent with momentum"""
    x = np.array(x0, dtype=np.float64)
    v = np.zeros_like(x)
    history = [(x.copy(), f(x))]
    
    for _ in range(max_iter):
        grad = grad_f(x)
        v = momentum * v + learning_rate * grad
        x_new = x - v
        
        history.append((x_new.copy(), f(x_new)))
        
        if np.linalg.norm(x_new - x) < tol:
            break
        
        x = x_new
    
    return x, history


def demo_optimization():
    """Demo berbagai metode optimisasi"""
    # Rosenbrock function (classic optimization benchmark)
    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    
    def rosenbrock_grad(x):
        dx = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2)
        dy = 200 * (x[1] - x[0]**2)
        return np.array([dx, dy])
    
    # Starting point
    x0 = np.array([-1.0, 1.0])
    
    # Gradient descent
    x_gd, history_gd = gradient_descent(rosenbrock, rosenbrock_grad, x0, 
                                        learning_rate=0.001, max_iter=10000)
    
    # Gradient descent with momentum
    x_mom, history_mom = gradient_descent_momentum(rosenbrock, rosenbrock_grad, x0,
                                                    learning_rate=0.001, momentum=0.9, 
                                                    max_iter=10000)
    
    # Scipy optimization (L-BFGS-B)
    result_scipy = optimize.minimize(rosenbrock, x0, jac=rosenbrock_grad, method='L-BFGS-B')
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Contour plot
    ax = axes[0]
    x_range = np.linspace(-2, 2, 100)
    y_range = np.linspace(-1, 3, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = (1 - X)**2 + 100 * (Y - X**2)**2
    
    ax.contour(X, Y, Z, levels=np.logspace(-1, 3, 20), cmap='viridis')
    
    # Plot paths
    path_gd = np.array([h[0] for h in history_gd])
    path_mom = np.array([h[0] for h in history_mom])
    
    ax.plot(path_gd[:, 0], path_gd[:, 1], 'r.-', alpha=0.7, label=f'GD ({len(history_gd)} iter)')
    ax.plot(path_mom[:, 0], path_mom[:, 1], 'b.-', alpha=0.7, label=f'Momentum ({len(history_mom)} iter)')
    ax.plot(1, 1, 'g*', markersize=15, label='Optimum')
    ax.plot(x0[0], x0[1], 'ko', markersize=10, label='Start')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Optimization Paths on Rosenbrock Function')
    ax.legend()
    
    # Loss curves
    ax = axes[1]
    losses_gd = [h[1] for h in history_gd]
    losses_mom = [h[1] for h in history_mom]
    
    ax.semilogy(losses_gd, 'r-', label='Gradient Descent')
    ax.semilogy(losses_mom, 'b-', label='Momentum')
    ax.axhline(y=rosenbrock([1, 1]), color='g', linestyle='--', label='Optimum')
    
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Loss (log scale)')
    ax.set_title('Convergence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output_optimization.png', dpi=150)
    plt.show()
    
    print(f"✅ Optimization demo selesai!")
    print(f"   True optimum: (1, 1)")
    print(f"   GD result: ({x_gd[0]:.4f}, {x_gd[1]:.4f})")
    print(f"   Momentum result: ({x_mom[0]:.4f}, {x_mom[1]:.4f})")
    print(f"   Scipy result: ({result_scipy.x[0]:.4f}, {result_scipy.x[1]:.4f})")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRAKTIKUM BAB 4: MODEL FITTING DAN OPTIMISASI")
    print("=" * 60)
    
    print("\n🚀 Menjalankan semua demo...\n")
    
    demo_least_squares()
    compare_ols_vs_ransac()
    demo_hough_lines()
    demo_hough_circles()
    demo_homography()
    demo_optimization()
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM SELESAI!")
    print("=" * 60)
    print("\nFile output yang dihasilkan:")
    print("  - output_least_squares.png")
    print("  - output_ols_vs_ransac.png")
    print("  - output_hough_lines.png")
    print("  - output_hough_circles.png")
    print("  - output_homography.png")
    print("  - output_optimization.png")
    print("\n📝 Tugas: Lihat file tugas/tugas_bab_04.md")
