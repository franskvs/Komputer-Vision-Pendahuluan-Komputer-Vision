"""
Percobaan 16: Mesh Warping dan Morphing
========================================

Materi yang dicakup:
- Section 3.6.2: Mesh-based warping
- Section 3.6.3: Feature-based morphing
- Thin-Plate Spline (TPS) warping
- Beier-Neely line-based warping
- Triangular mesh warping
- Image morphing dengan blending
- Forward dan inverse warping

Referensi: Szeliski "Computer Vision: Algorithms and Applications" halaman 175-180

Author: Computer Vision Course
Date: 2024
"""

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul scipy.spatial.
from scipy.spatial import Delaunay
# Keterangan: Impor komponen dari modul scipy.interpolate.
from scipy.interpolate import griddata


# Keterangan: Definisikan fungsi compute_tps_weights.
def compute_tps_weights(src_points, dst_points, regularization=0.0):
    """
    Menghitung weights untuk Thin-Plate Spline (TPS) warping
    
    TPS meminimalkan bending energy: ∫∫(f_xx² + 2f_xy² + f_yy²) dx dy
    
    Parameters:
    - src_points: (N, 2) array koordinat source
    - dst_points: (N, 2) array koordinat destination
    - regularization: parameter regularization (lambda)
    
    Returns:
    - weights: TPS weights untuk warping
    """
    # Keterangan: Inisialisasi atau perbarui variabel n.
    n = len(src_points)
    
    # Compute pairwise distances
    # Keterangan: Inisialisasi array bernilai nol.
    K = np.zeros((n, n))
    # Keterangan: Mulai loop dengan for i in range(n).
    for i in range(n):
        # Keterangan: Mulai loop dengan for j in range(n).
        for j in range(n):
            # Keterangan: Inisialisasi atau perbarui variabel r.
            r = np.linalg.norm(src_points[i] - src_points[j])
            # Keterangan: Cek kondisi r > 0.
            if r > 0:
                # Keterangan: Inisialisasi beberapa variabel (K[i, j]).
                K[i, j] = r * r * np.log(r)
    
    # Build system matrix
    # Keterangan: Inisialisasi array bernilai satu.
    P = np.hstack([np.ones((n, 1)), src_points])
    
    # Upper block
    # Keterangan: Inisialisasi atau perbarui variabel upper.
    upper = np.hstack([K + regularization * np.eye(n), P])
    
    # Lower block
    # Keterangan: Inisialisasi array bernilai nol.
    lower = np.hstack([P.T, np.zeros((3, 3))])
    
    # Full matrix
    # Keterangan: Inisialisasi atau perbarui variabel L.
    L = np.vstack([upper, lower])
    
    # Right-hand side
    # Keterangan: Inisialisasi array bernilai nol.
    Y = np.vstack([dst_points, np.zeros((3, 2))])
    
    # Solve
    # Keterangan: Mulai blok try untuk menangani error.
    try:
        # Keterangan: Inisialisasi atau perbarui variabel weights.
        weights = np.linalg.solve(L, Y)
    # Keterangan: Tangani error pada blok except.
    except np.linalg.LinAlgError:
        # Keterangan: Inisialisasi atau perbarui variabel weights.
        weights = np.linalg.lstsq(L, Y, rcond=None)[0]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return weights


# Keterangan: Definisikan fungsi apply_tps_warp.
def apply_tps_warp(img, src_points, dst_points, regularization=0.0):
    """
    Menerapkan Thin-Plate Spline warping ke image
    
    Parameters:
    - img: input image
    - src_points: (N, 2) control points di source
    - dst_points: (N, 2) control points di destination
    - regularization: TPS regularization
    
    Returns:
    - warped: warped image
    """
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = img.shape[:2]
    
    # Compute TPS weights
    # Keterangan: Inisialisasi atau perbarui variabel weights.
    weights = compute_tps_weights(src_points, dst_points, regularization)
    
    # Create destination grid
    # Keterangan: Buat range angka berjarak tetap.
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    # Keterangan: Inisialisasi atau perbarui variabel dst_grid.
    dst_grid = np.stack([x.ravel(), y.ravel()], axis=1).astype(np.float32)
    
    # Map destination ke source
    # Keterangan: Inisialisasi atau perbarui variabel n.
    n = len(src_points)
    # Keterangan: Inisialisasi array bernilai nol.
    src_grid = np.zeros_like(dst_grid)
    
    # Keterangan: Mulai loop dengan for i, (dx, dy) in enumerate(dst_grid).
    for i, (dx, dy) in enumerate(dst_grid):
        # Affine part
        # Keterangan: Inisialisasi atau perbarui variabel src_x.
        src_x = weights[n, 0] + weights[n+1, 0] * dx + weights[n+2, 0] * dy
        # Keterangan: Inisialisasi atau perbarui variabel src_y.
        src_y = weights[n, 1] + weights[n+1, 1] * dx + weights[n+2, 1] * dy
        
        # Non-linear part
        # Keterangan: Mulai loop dengan for j in range(n).
        for j in range(n):
            # Keterangan: Inisialisasi atau perbarui variabel r.
            r = np.sqrt((dx - dst_points[j, 0])**2 + (dy - dst_points[j, 1])**2)
            # Keterangan: Cek kondisi r > 0.
            if r > 0:
                # Keterangan: Inisialisasi atau perbarui variabel U.
                U = r * r * np.log(r)
                # Keterangan: Inisialisasi atau perbarui variabel src_x +.
                src_x += weights[j, 0] * U
                # Keterangan: Inisialisasi atau perbarui variabel src_y +.
                src_y += weights[j, 1] * U
        
        # Keterangan: Inisialisasi atau perbarui variabel src_grid[i].
        src_grid[i] = [src_x, src_y]
    
    # Reshape
    # Keterangan: Inisialisasi atau perbarui variabel map_x.
    map_x = src_grid[:, 0].reshape(h, w).astype(np.float32)
    # Keterangan: Inisialisasi atau perbarui variabel map_y.
    map_y = src_grid[:, 1].reshape(h, w).astype(np.float32)
    
    # Remap
    # Keterangan: Remap koordinat piksel untuk warping.
    warped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return warped


# Keterangan: Definisikan fungsi beier_neely_warp.
def beier_neely_warp(img, src_lines, dst_lines, p=0.5, a=1.0, b=2.0):
    """
    Implementasi Beier-Neely line-based warping
    
    Paper: "Feature-Based Image Metamorphosis" (Beier & Neely, 1992)
    
    Parameters:
    - img: input image
    - src_lines: list of [(x1,y1), (x2,y2)] di source
    - dst_lines: list of [(x1,y1), (x2,y2)] di destination
    - p, a, b: weight parameters
    
    Returns:
    - warped: warped image
    """
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = img.shape[:2]
    
    # Create destination grid
    # Keterangan: Buat range angka berjarak tetap.
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    # Keterangan: Inisialisasi atau perbarui variabel dst_x.
    dst_x = x.astype(np.float32)
    # Keterangan: Inisialisasi atau perbarui variabel dst_y.
    dst_y = y.astype(np.float32)
    
    # Initialize displacement
    # Keterangan: Inisialisasi array bernilai nol.
    sum_x = np.zeros((h, w), dtype=np.float32)
    # Keterangan: Inisialisasi array bernilai nol.
    sum_y = np.zeros((h, w), dtype=np.float32)
    # Keterangan: Inisialisasi array bernilai nol.
    weight_sum = np.zeros((h, w), dtype=np.float32)
    
    # Keterangan: Mulai loop dengan for src_line, dst_line in zip(src_lines, dst_lines).
    for src_line, dst_line in zip(src_lines, dst_lines):
        # Destination line
        # Keterangan: Inisialisasi atau perbarui variabel P.
        P = np.array(dst_line[0], dtype=np.float32)
        # Keterangan: Inisialisasi atau perbarui variabel Q.
        Q = np.array(dst_line[1], dtype=np.float32)
        
        # Source line
        # Keterangan: Inisialisasi atau perbarui variabel P_prime.
        P_prime = np.array(src_line[0], dtype=np.float32)
        # Keterangan: Inisialisasi atau perbarui variabel Q_prime.
        Q_prime = np.array(src_line[1], dtype=np.float32)
        
        # Line vector
        # Keterangan: Inisialisasi atau perbarui variabel v.
        v = Q - P
        # Keterangan: Inisialisasi atau perbarui variabel v_len.
        v_len = np.linalg.norm(v)
        # Keterangan: Cek kondisi v_len < 1e-6.
        if v_len < 1e-6:
            # Keterangan: Jalankan perintah berikut.
            continue
        
        # Keterangan: Inisialisasi atau perbarui variabel v_normalized.
        v_normalized = v / v_len
        
        # Perpendicular
        # Keterangan: Inisialisasi atau perbarui variabel perp.
        perp = np.array([-v[1], v[0]]) / v_len
        
        # For each pixel
        # Keterangan: Mulai loop dengan for i in range(h).
        for i in range(h):
            # Keterangan: Mulai loop dengan for j in range(w).
            for j in range(w):
                # Keterangan: Inisialisasi atau perbarui variabel X.
                X = np.array([j, i], dtype=np.float32)
                
                # Vector dari P ke X
                # Keterangan: Inisialisasi atau perbarui variabel PX.
                PX = X - P
                
                # u: position along line
                # Keterangan: Inisialisasi atau perbarui variabel u.
                u = np.dot(PX, v_normalized) / v_len
                
                # v: perpendicular distance
                # Keterangan: Inisialisasi atau perbarui variabel v_dist.
                v_dist = np.dot(PX, perp)
                
                # Corresponding point di source
                # Keterangan: Inisialisasi atau perbarui variabel v_prime.
                v_prime = Q_prime - P_prime
                # Keterangan: Inisialisasi atau perbarui variabel v_prime_len.
                v_prime_len = np.linalg.norm(v_prime)
                # Keterangan: Cek kondisi v_prime_len < 1e-6.
                if v_prime_len < 1e-6:
                    # Keterangan: Jalankan perintah berikut.
                    continue
                
                # Keterangan: Inisialisasi atau perbarui variabel v_prime_normalized.
                v_prime_normalized = v_prime / v_prime_len
                # Keterangan: Inisialisasi atau perbarui variabel perp_prime.
                perp_prime = np.array([-v_prime[1], v_prime[0]]) / v_prime_len
                
                # Keterangan: Inisialisasi atau perbarui variabel X_prime.
                X_prime = P_prime + u * v_prime + v_dist * perp_prime * v_prime_len
                
                # Displacement
                # Keterangan: Inisialisasi atau perbarui variabel disp.
                disp = X_prime - X
                
                # Distance ke line
                # Keterangan: Cek kondisi u < 0.
                if u < 0:
                    # Keterangan: Inisialisasi atau perbarui variabel dist.
                    dist = np.linalg.norm(X - P)
                # Keterangan: Cek kondisi alternatif u > 1.
                elif u > 1:
                    # Keterangan: Inisialisasi atau perbarui variabel dist.
                    dist = np.linalg.norm(X - Q)
                # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
                else:
                    # Keterangan: Inisialisasi atau perbarui variabel dist.
                    dist = abs(v_dist)
                
                # Weight
                # Keterangan: Inisialisasi atau perbarui variabel weight.
                weight = (v_len ** p / (a + dist)) ** b
                
                # Keterangan: Inisialisasi beberapa variabel (sum_x[i, j] +).
                sum_x[i, j] += disp[0] * weight
                # Keterangan: Inisialisasi beberapa variabel (sum_y[i, j] +).
                sum_y[i, j] += disp[1] * weight
                # Keterangan: Inisialisasi beberapa variabel (weight_sum[i, j] +).
                weight_sum[i, j] += weight
    
    # Average displacement
    # Keterangan: Inisialisasi atau perbarui variabel mask.
    mask = weight_sum > 1e-6
    # Keterangan: Inisialisasi array bernilai nol.
    avg_x = np.zeros((h, w), dtype=np.float32)
    # Keterangan: Inisialisasi array bernilai nol.
    avg_y = np.zeros((h, w), dtype=np.float32)
    
    # Keterangan: Inisialisasi atau perbarui variabel avg_x[mask].
    avg_x[mask] = dst_x[mask] + sum_x[mask] / weight_sum[mask]
    # Keterangan: Inisialisasi atau perbarui variabel avg_y[mask].
    avg_y[mask] = dst_y[mask] + sum_y[mask] / weight_sum[mask]
    
    # Remap
    # Keterangan: Remap koordinat piksel untuk warping.
    warped = cv2.remap(img, avg_x, avg_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return warped


# Keterangan: Definisikan fungsi triangular_mesh_warp.
def triangular_mesh_warp(img, src_tri, dst_tri):
    """
    Melakukan warping menggunakan affine transform per triangle
    
    Parameters:
    - img: input image
    - src_tri: (3, 2) array vertices source triangle
    - dst_tri: (3, 2) array vertices destination triangle
    
    Returns:
    - warped: warped region
    """
    # Compute affine transform
    # Keterangan: Inisialisasi atau perbarui variabel src_tri.
    src_tri = src_tri.astype(np.float32)
    # Keterangan: Inisialisasi atau perbarui variabel dst_tri.
    dst_tri = dst_tri.astype(np.float32)
    
    # Keterangan: Inisialisasi atau perbarui variabel M.
    M = cv2.getAffineTransform(src_tri, dst_tri)
    
    # Get bounding box
    # Keterangan: Inisialisasi beberapa variabel (x, y, w, h).
    x, y, w, h = cv2.boundingRect(dst_tri.astype(np.int32))
    
    # Warp triangle
    # Keterangan: Terapkan transformasi affine pada gambar.
    warped = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    
    # Mask
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillConvexPoly(mask, dst_tri.astype(np.int32), 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return warped, mask


# Keterangan: Definisikan fungsi full_mesh_warp.
def full_mesh_warp(img, src_points, dst_points):
    """
    Melakukan full mesh warping dengan Delaunay triangulation
    
    Parameters:
    - img: input image
    - src_points: (N, 2) control points di source
    - dst_points: (N, 2) control points di destination
    
    Returns:
    - warped: warped image
    """
    # Delaunay triangulation di destination
    # Keterangan: Inisialisasi atau perbarui variabel tri.
    tri = Delaunay(dst_points)
    
    # Output image
    # Keterangan: Inisialisasi array bernilai nol.
    warped = np.zeros_like(img)
    
    # Process setiap triangle
    # Keterangan: Mulai loop dengan for simplex in tri.simplices.
    for simplex in tri.simplices:
        # Get vertices
        # Keterangan: Inisialisasi atau perbarui variabel src_tri.
        src_tri = src_points[simplex]
        # Keterangan: Inisialisasi atau perbarui variabel dst_tri.
        dst_tri = dst_points[simplex]
        
        # Warp triangle
        # Keterangan: Inisialisasi beberapa variabel (tri_warped, mask).
        tri_warped, mask = triangular_mesh_warp(img, src_tri, dst_tri)
        
        # Composite
        # Keterangan: Inisialisasi atau perbarui variabel warped[mask > 0].
        warped[mask > 0] = tri_warped[mask > 0]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return warped


# Keterangan: Definisikan fungsi morph_images.
def morph_images(img1, img2, src_points, dst_points, alpha=0.5):
    """
    Melakukan morphing antara dua images
    
    Morphing = Warping + Cross-dissolve
    
    Parameters:
    - img1: source image
    - img2: destination image
    - src_points: control points di img1
    - dst_points: control points di img2
    - alpha: morphing parameter (0=img1, 1=img2)
    
    Returns:
    - morphed: morphed image
    """
    # Intermediate control points
    # Keterangan: Inisialisasi atau perbarui variabel inter_points.
    inter_points = (1 - alpha) * src_points + alpha * dst_points
    
    # Warp img1 ke intermediate
    # Keterangan: Inisialisasi atau perbarui variabel warp1.
    warp1 = full_mesh_warp(img1, src_points, inter_points)
    
    # Warp img2 ke intermediate
    # Keterangan: Inisialisasi atau perbarui variabel warp2.
    warp2 = full_mesh_warp(img2, dst_points, inter_points)
    
    # Cross-dissolve
    # Keterangan: Inisialisasi atau perbarui variabel morphed.
    morphed = ((1 - alpha) * warp1.astype(np.float32) + 
               # Keterangan: Jalankan perintah berikut.
               alpha * warp2.astype(np.float32))
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(morphed, 0, 255).astype(np.uint8)


# ==================== DEMONSTRATION FUNCTIONS ====================

# Keterangan: Definisikan fungsi demo_tps_warping.
def demo_tps_warping():
    """Demo 1: Thin-Plate Spline Warping"""
    print("\n=== Demo 1: TPS Warping ===")
    
    # Create test image
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw grid
    for i in range(0, 400, 40):
        cv2.line(img, (i, 0), (i, 400), (200, 200, 200), 1)
        cv2.line(img, (0, i), (400, i), (200, 200, 200), 1)
    
    # Draw circles
    for i in range(100, 400, 100):
        for j in range(100, 400, 100):
            cv2.circle(img, (i, j), 20, (0, 0, 255), -1)
    
    # Control points (grid)
    src_points = []
    for i in range(0, 400, 100):
        for j in range(0, 400, 100):
            src_points.append([i, j])
    src_points = np.array(src_points, dtype=np.float32)
    
    # Different warps
    results = []
    results.append(('Original', img.copy()))
    
    # Warp 1: Barrel distortion
    dst_points1 = src_points.copy()
    center = np.array([200, 200])
    for i in range(len(dst_points1)):
        diff = dst_points1[i] - center
        dist = np.linalg.norm(diff)
        if dist > 0:
            factor = 1 + 0.3 * (dist / 200) ** 2
            dst_points1[i] = center + diff * factor
    
    warp1 = apply_tps_warp(img, src_points, dst_points1)
    results.append(('Barrel Distortion', warp1))
    
    # Warp 2: Pincushion
    dst_points2 = src_points.copy()
    for i in range(len(dst_points2)):
        diff = dst_points2[i] - center
        dist = np.linalg.norm(diff)
        if dist > 0:
            factor = 1 - 0.2 * (dist / 200) ** 2
            dst_points2[i] = center + diff * factor
    
    warp2 = apply_tps_warp(img, src_points, dst_points2)
    results.append(('Pincushion', warp2))
    
    # Warp 3: Wave
    dst_points3 = src_points.copy()
    for i in range(len(dst_points3)):
        x, y = dst_points3[i]
        dst_points3[i, 0] += 20 * np.sin(y * np.pi / 100)
        dst_points3[i, 1] += 20 * np.sin(x * np.pi / 100)
    
    warp3 = apply_tps_warp(img, src_points, dst_points3)
    results.append(('Wave', warp3))
    
    # Visualize
    plt.figure(figsize=(12, 8))
    
    for idx, (name, result) in enumerate(results):
        plt.subplot(2, 2, idx + 1)
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.title(name)
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('16_tps_warping.png', dpi=150, bbox_inches='tight')
    print("Saved: 16_tps_warping.png")
    plt.close()


def demo_beier_neely():
    """Demo 2: Beier-Neely Line-Based Warping"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 2: Beier-Neely Warping ===")
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai satu.
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw face-like pattern
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img, (200, 200), 100, (0, 0, 0), 2)  # Face
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img, (170, 180), 10, (0, 0, 0), -1)  # Left eye
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img, (230, 180), 10, (0, 0, 0), -1)  # Right eye
    # Keterangan: Jalankan perintah berikut.
    cv2.ellipse(img, (200, 240), (40, 20), 0, 0, 180, (0, 0, 0), 2)  # Mouth
    
    # Define line pairs untuk smile
    # Keterangan: Inisialisasi atau perbarui variabel src_lines.
    src_lines = [
        # Keterangan: Jalankan perintah berikut.
        [(160, 240), (240, 240)],  # Mouth (straight)
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Inisialisasi atau perbarui variabel dst_lines.
    dst_lines = [
        # Keterangan: Jalankan perintah berikut.
        [(160, 230), (240, 230)],  # Mouth (curved up)
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Warp with different parameters
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = []
    # Keterangan: Jalankan perintah berikut.
    results.append(('Original', img.copy()))
    
    # Keterangan: Inisialisasi atau perbarui variabel param_sets.
    param_sets = [
        # Keterangan: Inisialisasi beberapa variabel ((0.0, 0.5, 2.0, 'p).
        (0.0, 0.5, 2.0, 'p=0.0, a=0.5, b=2.0'),
        # Keterangan: Inisialisasi beberapa variabel ((0.5, 1.0, 2.0, 'p).
        (0.5, 1.0, 2.0, 'p=0.5, a=1.0, b=2.0'),
        # Keterangan: Inisialisasi beberapa variabel ((1.0, 1.0, 2.0, 'p).
        (1.0, 1.0, 2.0, 'p=1.0, a=1.0, b=2.0'),
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Mulai loop dengan for p, a, b, label in param_sets.
    for p, a, b, label in param_sets:
        # Keterangan: Inisialisasi atau perbarui variabel warped.
        warped = beier_neely_warp(img, src_lines, dst_lines, p=p, a=a, b=b)
        # Keterangan: Jalankan perintah berikut.
        results.append((label, warped))
    
    # Visualize
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(12, 8))
    
    # Keterangan: Mulai loop dengan for idx, (name, result) in enumerate(results).
    for idx, (name, result) in enumerate(results):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(2, 2, idx + 1)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(name)
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('16_beier_neely.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 16_beier_neely.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_mesh_warp.
def demo_mesh_warp():
    """Demo 3: Triangular Mesh Warping"""
    print("\n=== Demo 3: Mesh Warping ===")
    
    # Create test image dengan pattern
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Checkerboard
    cell_size = 40
    for i in range(0, 400, cell_size):
        for j in range(0, 400, cell_size):
            if ((i // cell_size) + (j // cell_size)) % 2 == 0:
                img[i:i+cell_size, j:j+cell_size] = [255, 100, 100]
            else:
                img[i:i+cell_size, j:j+cell_size] = [100, 100, 255]
    
    # Control points (grid)
    src_points = []
    for y in range(0, 401, 100):
        for x in range(0, 401, 100):
            src_points.append([x, y])
    src_points = np.array(src_points, dtype=np.float32)
    
    # Destination points (deformed)
    dst_points = src_points.copy()
    
    # Central point (2,2) moved
    center_idx = 2 * 5 + 2  # Row 2, col 2
    dst_points[center_idx] = [200, 150]  # Move up
    
    # Adjacent points slightly moved
    dst_points[center_idx - 5] = [200, 50]   # Top
    dst_points[center_idx + 5] = [200, 350]  # Bottom
    dst_points[center_idx - 1] = [100, 200]  # Left
    dst_points[center_idx + 1] = [300, 200]  # Right
    
    # Warp
    warped = full_mesh_warp(img, src_points, dst_points)
    
    # Visualize dengan triangulation
    plt.figure(figsize=(15, 5))
    
    # Original dengan mesh
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    tri = Delaunay(src_points)
    plt.triplot(src_points[:, 0], src_points[:, 1], tri.simplices, 'g-', linewidth=1)
    plt.plot(src_points[:, 0], src_points[:, 1], 'ro', markersize=5)
    plt.title('Original + Source Mesh')
    plt.axis('off')
    
    # Destination mesh
    plt.subplot(1, 3, 2)
    tri_dst = Delaunay(dst_points)
    plt.triplot(dst_points[:, 0], dst_points[:, 1], tri_dst.simplices, 'b-', linewidth=1)
    plt.plot(dst_points[:, 0], dst_points[:, 1], 'ro', markersize=5)
    plt.xlim(0, 400)
    plt.ylim(400, 0)
    plt.title('Destination Mesh')
    plt.axis('off')
    
    # Warped result
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    plt.title('Warped Result')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('16_mesh_warp.png', dpi=150, bbox_inches='tight')
    print("Saved: 16_mesh_warp.png")
    plt.close()


def demo_morphing_sequence():
    """Demo 4: Image Morphing Sequence"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 4: Morphing Sequence ===")
    
    # Create two simple shapes
    # Keterangan: Inisialisasi array bernilai satu.
    img1 = np.ones((300, 300, 3), dtype=np.uint8) * 255
    # Keterangan: Inisialisasi array bernilai satu.
    img2 = np.ones((300, 300, 3), dtype=np.uint8) * 255
    
    # Shape 1: Square
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(img1, (75, 75), (225, 225), (255, 0, 0), -1)
    
    # Shape 2: Circle
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img2, (150, 150), 75, (0, 0, 255), -1)
    
    # Control points
    # Square corners + center
    # Keterangan: Inisialisasi atau perbarui variabel src_points.
    src_points = np.array([
        # Keterangan: Jalankan perintah berikut.
        [75, 75], [225, 75], [225, 225], [75, 225],  # Corners
        # Keterangan: Jalankan perintah berikut.
        [150, 75], [225, 150], [150, 225], [75, 150],  # Midpoints
        # Keterangan: Jalankan perintah berikut.
        [150, 150]  # Center
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.float32)
    
    # Circle (same topology)
    # Keterangan: Buat range angka berjarak linier.
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    # Keterangan: Inisialisasi atau perbarui variabel dst_points.
    dst_points = []
    # Keterangan: Mulai loop dengan for angle in angles.
    for angle in angles:
        # Keterangan: Inisialisasi atau perbarui variabel x.
        x = 150 + 75 * np.cos(angle)
        # Keterangan: Inisialisasi atau perbarui variabel y.
        y = 150 + 75 * np.sin(angle)
        # Keterangan: Jalankan perintah berikut.
        dst_points.append([x, y])
    # Keterangan: Jalankan perintah berikut.
    dst_points.append([150, 150])  # Center
    # Keterangan: Inisialisasi atau perbarui variabel dst_points.
    dst_points = np.array(dst_points, dtype=np.float32)
    
    # Morphing sequence
    # Keterangan: Inisialisasi atau perbarui variabel alphas.
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    # Keterangan: Inisialisasi atau perbarui variabel morphed_images.
    morphed_images = []
    
    # Keterangan: Mulai loop dengan for alpha in alphas.
    for alpha in alphas:
        # Keterangan: Inisialisasi atau perbarui variabel morphed.
        morphed = morph_images(img1, img2, src_points, dst_points, alpha=alpha)
        # Keterangan: Inisialisasi atau perbarui variabel morphed_images.append((f'α.
        morphed_images.append((f'α={alpha:.2f}', morphed))
    
    # Visualize
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 3))
    
    # Keterangan: Mulai loop dengan for idx, (name, result) in enumerate(morphed_images).
    for idx, (name, result) in enumerate(morphed_images):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(1, 5, idx + 1)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(name)
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('16_morphing_sequence.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 16_morphing_sequence.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_forward_vs_inverse.
def demo_forward_vs_inverse():
    """Demo 5: Forward vs Inverse Warping"""
    print("\n=== Demo 5: Forward vs Inverse Warping ===")
    
    # Create simple test image
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), (255, 255, 255), -1)
    cv2.circle(img, (100, 100), 30, (255, 0, 0), -1)
    
    # Simple rotation transform
    angle = 30
    center = (100, 100)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Forward warping (manual implementation)
    forward_result = np.zeros_like(img)
    h, w = img.shape[:2]
    
    for y in range(h):
        for x in range(w):
            # Transform coordinate
            src = np.array([x, y, 1])
            dst = M @ src
            
            dst_x, dst_y = int(round(dst[0])), int(round(dst[1]))
            
            if 0 <= dst_x < w and 0 <= dst_y < h:
                forward_result[dst_y, dst_x] = img[y, x]
    
    # Inverse warping (OpenCV standard)
    inverse_result = cv2.warpAffine(img, M, (w, h))
    
    # Visualize
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(forward_result, cv2.COLOR_BGR2RGB))
    plt.title('Forward Warping\n(holes)')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(inverse_result, cv2.COLOR_BGR2RGB))
    plt.title('Inverse Warping\n(no holes)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('16_forward_vs_inverse.png', dpi=150, bbox_inches='tight')
    print("Saved: 16_forward_vs_inverse.png")
    plt.close()


def demo_complex_morphing():
    """Demo 6: Complex Multi-Feature Morphing"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 6: Complex Morphing ===")
    
    # Create two face-like images
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = 400, 300
    
    # Image 1: Sad face
    # Keterangan: Inisialisasi array bernilai satu.
    img1 = np.ones((h, w, 3), dtype=np.uint8) * 255
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (150, 200), 100, (0, 0, 0), 2)  # Face
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (120, 180), 10, (0, 0, 0), -1)  # Left eye
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (180, 180), 10, (0, 0, 0), -1)  # Right eye
    # Keterangan: Jalankan perintah berikut.
    cv2.ellipse(img1, (150, 260), (40, 15), 0, 180, 360, (0, 0, 0), 2)  # Sad mouth
    
    # Image 2: Happy face
    # Keterangan: Inisialisasi array bernilai satu.
    img2 = np.ones((h, w, 3), dtype=np.uint8) * 255
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img2, (150, 200), 100, (0, 0, 0), 2)  # Face
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img2, (120, 180), 10, (0, 0, 0), -1)  # Left eye
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img2, (180, 180), 10, (0, 0, 0), -1)  # Right eye
    # Keterangan: Jalankan perintah berikut.
    cv2.ellipse(img2, (150, 240), (40, 15), 0, 0, 180, (0, 0, 0), 2)  # Happy mouth
    
    # Detailed control points
    # Keterangan: Inisialisasi atau perbarui variabel src_points.
    src_points = np.array([
        # Face outline
        # Keterangan: Jalankan perintah berikut.
        [50, 200], [150, 100], [250, 200], [150, 300],
        # Eyes
        # Keterangan: Jalankan perintah berikut.
        [120, 180], [180, 180],
        # Mouth (sad)
        # Keterangan: Jalankan perintah berikut.
        [110, 260], [150, 275], [190, 260],
        # Corners
        # Keterangan: Jalankan perintah berikut.
        [0, 0], [300, 0], [300, 400], [0, 400],
        # Center
        # Keterangan: Jalankan perintah berikut.
        [150, 200]
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.float32)
    
    # Keterangan: Inisialisasi atau perbarui variabel dst_points.
    dst_points = src_points.copy()
    # Modify mouth points untuk happy
    # Keterangan: Inisialisasi atau perbarui variabel dst_points[6].
    dst_points[6] = [110, 240]  # Left mouth
    # Keterangan: Inisialisasi atau perbarui variabel dst_points[7].
    dst_points[7] = [150, 225]  # Center mouth
    # Keterangan: Inisialisasi atau perbarui variabel dst_points[8].
    dst_points[8] = [190, 240]  # Right mouth
    
    # Morphing frames
    # Keterangan: Inisialisasi atau perbarui variabel num_frames.
    num_frames = 7
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(18, 3))
    
    # Keterangan: Mulai loop dengan for i in range(num_frames).
    for i in range(num_frames):
        # Keterangan: Inisialisasi atau perbarui variabel alpha.
        alpha = i / (num_frames - 1)
        # Keterangan: Inisialisasi atau perbarui variabel morphed.
        morphed = morph_images(img1, img2, src_points, dst_points, alpha=alpha)
        
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(1, num_frames, i + 1)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(morphed, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(f't={alpha:.2f}')
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('16_complex_morphing.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 16_complex_morphing.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    # Keterangan: Jalankan perintah berikut.
    print("Percobaan 16: Mesh Warping dan Morphing")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Keterangan: Jalankan perintah berikut.
    demo_tps_warping()
    # Keterangan: Jalankan perintah berikut.
    demo_beier_neely()
    # Keterangan: Jalankan perintah berikut.
    demo_mesh_warp()
    # Keterangan: Jalankan perintah berikut.
    demo_morphing_sequence()
    # Keterangan: Jalankan perintah berikut.
    demo_forward_vs_inverse()
    # Keterangan: Jalankan perintah berikut.
    demo_complex_morphing()
    
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("Semua demo selesai!")
    # Keterangan: Jalankan perintah berikut.
    print("File output:")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_tps_warping.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_beier_neely.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_mesh_warp.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_morphing_sequence.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_forward_vs_inverse.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 16_complex_morphing.png")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
