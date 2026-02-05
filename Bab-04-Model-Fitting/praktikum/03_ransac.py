# ============================================================
# PROGRAM: 03_ransac.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk RANSAC (Random Sample Consensus)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep RANSAC untuk robust estimation
#   2. Implementasi RANSAC untuk line fitting
#   3. Perbandingan dengan least squares
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. Jumlah titik data
JUMLAH_INLIERS = 50      # Titik yang mengikuti model
JUMLAH_OUTLIERS = 20     # Titik yang tidak mengikuti model (noise)

# 2. Noise level untuk inliers
INLIER_NOISE = 5.0       # Deviasi dari garis ideal

# 3. Parameter RANSAC
RANSAC_ITERATIONS = 100   # Jumlah iterasi
RANSAC_THRESHOLD = 10.0   # Threshold untuk inlier
RANSAC_SAMPLE_SIZE = 2    # Jumlah sample per iterasi (2 untuk garis)

# 4. Parameter garis ideal (y = mx + c)
LINE_M = 1.5             # Slope
LINE_C = 50              # Intercept

# 5. Ukuran canvas
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 400

# 6. Auto-close plot (detik)
AUTO_CLOSE_SECONDS = 2.0

# ============================================================
# FUNGSI RANSAC
# ============================================================

def generate_line_data(n_inliers, n_outliers, m, c, noise_level, 
                       width=500, height=400):
    """
    Generate data points dengan inliers dan outliers
    
    Parameter:
    - n_inliers: jumlah titik yang mengikuti model
    - n_outliers: jumlah titik outlier (noise)
    - m, c: parameter garis (y = mx + c)
    - noise_level: noise untuk inliers
    
    Return:
    - points: array of (x, y) points
    - labels: 1 untuk inlier, 0 untuk outlier
    """
    points = []
    labels = []
    
    # Generate inliers (titik di sekitar garis)
    x_inliers = np.random.uniform(50, width - 50, n_inliers)
    for x in x_inliers:
        y_ideal = m * x + c
        y_noisy = y_ideal + np.random.normal(0, noise_level)
        # Pastikan dalam batas
        y_noisy = np.clip(y_noisy, 0, height)
        points.append([x, y_noisy])
        labels.append(1)  # Inlier
    
    # Generate outliers (titik random)
    for _ in range(n_outliers):
        x = np.random.uniform(0, width)
        y = np.random.uniform(0, height)
        points.append([x, y])
        labels.append(0)  # Outlier
    
    # Shuffle
    combined = list(zip(points, labels))
    np.random.shuffle(combined)
    points, labels = zip(*combined)
    
    return np.array(points), np.array(labels)


def tampilkan_plot():
    """Tampilkan plot sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(AUTO_CLOSE_SECONDS)
    plt.close()


def fit_line_least_squares(points):
    """
    Fit line menggunakan Least Squares
    
    Least Squares: Minimize sum of squared errors
    Sensitif terhadap outliers!
    
    Return:
    - m, c: parameter garis (y = mx + c)
    """
    x = points[:, 0]
    y = points[:, 1]
    
    # Least squares solution
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)
    
    # Calculate slope and intercept
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x + 1e-10)
    c = (sum_y - m * sum_x) / n
    
    return m, c


def calculate_distance_to_line(points, m, c):
    """
    Hitung jarak titik ke garis
    
    Jarak dari titik (x0, y0) ke garis ax + by + c = 0:
    d = |ax0 + by0 + c| / sqrt(a² + b²)
    
    Untuk y = mx + c → mx - y + c = 0
    """
    x = points[:, 0]
    y = points[:, 1]
    
    # Line: mx - y + c = 0 → a=m, b=-1, c=c
    distances = np.abs(m * x - y + c) / np.sqrt(m * m + 1)
    
    return distances


def ransac_line_fitting(points, n_iterations, threshold, sample_size=2):
    """
    RANSAC untuk Line Fitting
    
    Algoritma:
    1. Random sample n points
    2. Fit model dari sample
    3. Hitung inliers (titik dengan error < threshold)
    4. Jika inliers > best, simpan model
    5. Ulangi
    6. Refit model dengan semua inliers
    
    Parameter:
    - points: array of (x, y) points
    - n_iterations: jumlah iterasi
    - threshold: threshold untuk inlier
    - sample_size: jumlah sample per iterasi
    
    Return:
    - best_m, best_c: parameter garis terbaik
    - best_inliers: mask inliers
    - history: history of fitting process
    """
    n_points = len(points)
    best_inliers = None
    best_n_inliers = 0
    best_m = None
    best_c = None
    history = []
    
    for i in range(n_iterations):
        # 1. Random sample
        sample_idx = np.random.choice(n_points, sample_size, replace=False)
        sample_points = points[sample_idx]
        
        # 2. Fit line dari sample (2 titik menentukan 1 garis)
        x1, y1 = sample_points[0]
        x2, y2 = sample_points[1]
        
        # Avoid division by zero
        if abs(x2 - x1) < 1e-10:
            continue
        
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        
        # 3. Calculate distances and find inliers
        distances = calculate_distance_to_line(points, m, c)
        inliers = distances < threshold
        n_inliers = np.sum(inliers)
        
        # 4. Update best model
        if n_inliers > best_n_inliers:
            best_n_inliers = n_inliers
            best_inliers = inliers
            best_m = m
            best_c = c
        
        # Save history
        history.append({
            'iteration': i,
            'm': m, 'c': c,
            'n_inliers': n_inliers,
            'best_n_inliers': best_n_inliers
        })
    
    # 5. Refit dengan semua inliers
    if best_inliers is not None and np.sum(best_inliers) > 2:
        inlier_points = points[best_inliers]
        best_m, best_c = fit_line_least_squares(inlier_points)
    
    return best_m, best_c, best_inliers, history


def calculate_ransac_iterations(p_success, p_inlier, n_samples):
    """
    Hitung jumlah iterasi RANSAC yang diperlukan
    
    Formula: k = log(1 - p_success) / log(1 - p_inlier^n)
    
    Parameter:
    - p_success: probabilitas sukses yang diinginkan (0.99)
    - p_inlier: proporsi inliers dalam data
    - n_samples: jumlah sample per iterasi
    
    Return:
    - k: jumlah iterasi yang diperlukan
    """
    k = np.log(1 - p_success) / np.log(1 - p_inlier ** n_samples + 1e-10)
    return int(np.ceil(k))


# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_comparison(points, labels, ls_params, ransac_params, ransac_inliers):
    """Visualisasi perbandingan Least Squares vs RANSAC"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # True inliers vs outliers
    inlier_mask = labels == 1
    
    # Plot 1: Data dengan ground truth
    ax = axes[0]
    ax.scatter(points[inlier_mask, 0], points[inlier_mask, 1], 
               c='blue', label='Inliers (True)', alpha=0.6)
    ax.scatter(points[~inlier_mask, 0], points[~inlier_mask, 1], 
               c='red', label='Outliers (True)', alpha=0.6)
    
    # Draw ideal line
    x_line = np.array([0, CANVAS_WIDTH])
    y_line = LINE_M * x_line + LINE_C
    ax.plot(x_line, y_line, 'g--', linewidth=2, label=f'Ideal: y={LINE_M}x+{LINE_C}')
    
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(0, CANVAS_HEIGHT)
    ax.set_title("Data dengan Ground Truth")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Least Squares
    ax = axes[1]
    ax.scatter(points[:, 0], points[:, 1], c='gray', alpha=0.6)
    
    # Draw LS line
    ls_m, ls_c = ls_params
    y_ls = ls_m * x_line + ls_c
    ax.plot(x_line, y_ls, 'r-', linewidth=2, label=f'LS: y={ls_m:.2f}x+{ls_c:.2f}')
    ax.plot(x_line, y_line, 'g--', linewidth=2, label='Ideal')
    
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(0, CANVAS_HEIGHT)
    ax.set_title("Least Squares (Sensitif Outliers)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: RANSAC
    ax = axes[2]
    ax.scatter(points[ransac_inliers, 0], points[ransac_inliers, 1], 
               c='blue', label='RANSAC Inliers', alpha=0.6)
    ax.scatter(points[~ransac_inliers, 0], points[~ransac_inliers, 1], 
               c='red', label='RANSAC Outliers', alpha=0.6)
    
    # Draw RANSAC line
    ransac_m, ransac_c = ransac_params
    y_ransac = ransac_m * x_line + ransac_c
    ax.plot(x_line, y_ransac, 'b-', linewidth=2, 
            label=f'RANSAC: y={ransac_m:.2f}x+{ransac_c:.2f}')
    ax.plot(x_line, y_line, 'g--', linewidth=2, label='Ideal')
    
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(0, CANVAS_HEIGHT)
    ax.set_title("RANSAC (Robust)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    tampilkan_plot()


def visualize_ransac_progress(history):
    """Visualisasi progress RANSAC"""
    iterations = [h['iteration'] for h in history]
    n_inliers = [h['n_inliers'] for h in history]
    best_inliers = [h['best_n_inliers'] for h in history]
    
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, n_inliers, 'b.', alpha=0.3, label='Inliers per iteration')
    plt.plot(iterations, best_inliers, 'r-', linewidth=2, label='Best inliers')
    plt.xlabel('Iteration')
    plt.ylabel('Number of Inliers')
    plt.title('RANSAC Progress')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    tampilkan_plot()


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_outlier_ratio_effect():
    """Demonstrasi pengaruh rasio outliers"""
    print("\n" + "=" * 60)
    print("PENGARUH RASIO OUTLIERS")
    print("=" * 60)
    
    outlier_ratios = [0.1, 0.3, 0.5]
    n_total = 100
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    for i, ratio in enumerate(outlier_ratios):
        n_outliers = int(n_total * ratio)
        n_inliers = n_total - n_outliers
        
        # Generate data
        points, labels = generate_line_data(n_inliers, n_outliers, 
                                            LINE_M, LINE_C, INLIER_NOISE)
        
        # Least Squares
        ls_m, ls_c = fit_line_least_squares(points)
        
        # RANSAC
        p_inlier = 1 - ratio
        n_iter = calculate_ransac_iterations(0.99, p_inlier, 2)
        ransac_m, ransac_c, ransac_inliers, _ = ransac_line_fitting(
            points, max(n_iter, 50), RANSAC_THRESHOLD
        )
        
        # Plot LS
        ax = axes[0, i]
        ax.scatter(points[:, 0], points[:, 1], c='gray', alpha=0.5)
        x_line = np.array([0, CANVAS_WIDTH])
        y_ls = ls_m * x_line + ls_c
        y_ideal = LINE_M * x_line + LINE_C
        ax.plot(x_line, y_ls, 'r-', linewidth=2, label='LS')
        ax.plot(x_line, y_ideal, 'g--', linewidth=2, label='Ideal')
        ax.set_title(f"Least Squares\nOutlier Ratio: {ratio*100:.0f}%")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot RANSAC
        ax = axes[1, i]
        ax.scatter(points[ransac_inliers, 0], points[ransac_inliers, 1], 
                   c='blue', alpha=0.5, label='Inliers')
        ax.scatter(points[~ransac_inliers, 0], points[~ransac_inliers, 1], 
                   c='red', alpha=0.5, label='Outliers')
        y_ransac = ransac_m * x_line + ransac_c
        ax.plot(x_line, y_ransac, 'b-', linewidth=2, label='RANSAC')
        ax.plot(x_line, y_ideal, 'g--', linewidth=2, label='Ideal')
        ax.set_title(f"RANSAC\nIterations: {n_iter}")
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle("Pengaruh Rasio Outliers pada Least Squares vs RANSAC", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_threshold_effect():
    """Demonstrasi pengaruh threshold RANSAC"""
    print("\n" + "=" * 60)
    print("PENGARUH THRESHOLD RANSAC")
    print("=" * 60)
    
    print("""
THRESHOLD:

Threshold menentukan batas jarak untuk dianggap inlier.

Threshold kecil (strict):
├── Hanya titik yang sangat dekat dianggap inlier
├── Lebih akurat tapi mungkin miss beberapa inliers
└── Cocok untuk data low-noise

Threshold besar (relaxed):
├── Lebih banyak titik dianggap inlier
├── Risiko memasukkan outliers
└── Cocok untuk data high-noise
    """)
    
    # Generate data
    points, labels = generate_line_data(JUMLAH_INLIERS, JUMLAH_OUTLIERS,
                                        LINE_M, LINE_C, INLIER_NOISE)
    
    thresholds = [3, 10, 30]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, thresh in enumerate(thresholds):
        ransac_m, ransac_c, ransac_inliers, _ = ransac_line_fitting(
            points, RANSAC_ITERATIONS, thresh
        )
        
        ax = axes[i]
        ax.scatter(points[ransac_inliers, 0], points[ransac_inliers, 1], 
                   c='blue', alpha=0.6, label='Inliers')
        ax.scatter(points[~ransac_inliers, 0], points[~ransac_inliers, 1], 
                   c='red', alpha=0.6, label='Outliers')
        
        x_line = np.array([0, CANVAS_WIDTH])
        y_ransac = ransac_m * x_line + ransac_c
        y_ideal = LINE_M * x_line + LINE_C
        ax.plot(x_line, y_ransac, 'b-', linewidth=2)
        ax.plot(x_line, y_ideal, 'g--', linewidth=2)
        
        ax.set_title(f"Threshold = {thresh}\nInliers: {np.sum(ransac_inliers)}")
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle("Pengaruh Threshold pada RANSAC", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: RANSAC (Random Sample Consensus)")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
RANSAC adalah algoritma robust estimation untuk fitting model
dengan data yang mengandung banyak outliers.

KONSEP:
├── Inliers: titik yang mengikuti model
└── Outliers: titik yang tidak mengikuti model (noise)

ALGORITMA:
1. Random sample: pilih minimal sample untuk fit model
2. Fit model dari sample
3. Hitung inliers (titik dengan error < threshold)
4. Jika inliers > best, simpan model
5. Ulangi sampai iterasi selesai
6. Refit model dengan semua inliers

KEUNTUNGAN:
├── Robust terhadap outliers (hingga 50%+)
├── Tidak perlu mengetahui outliers terlebih dahulu
└── Applicable untuk berbagai model fitting

FORMULA ITERASI:
k = log(1 - p) / log(1 - w^n)
├── p = probabilitas sukses (misal 0.99)
├── w = proporsi inliers
└── n = jumlah sample per iterasi
    """)
    
    # Generate data
    print("\n[STEP 1] Generate Data...")
    points, labels = generate_line_data(
        JUMLAH_INLIERS, JUMLAH_OUTLIERS,
        LINE_M, LINE_C, INLIER_NOISE,
        CANVAS_WIDTH, CANVAS_HEIGHT
    )
    
    true_inliers = np.sum(labels == 1)
    true_outliers = np.sum(labels == 0)
    outlier_ratio = true_outliers / len(labels)
    
    print(f"   Total points: {len(points)}")
    print(f"   True inliers: {true_inliers}")
    print(f"   True outliers: {true_outliers}")
    print(f"   Outlier ratio: {outlier_ratio*100:.1f}%")
    
    # Calculate optimal iterations
    p_inlier = 1 - outlier_ratio
    optimal_iter = calculate_ransac_iterations(0.99, p_inlier, RANSAC_SAMPLE_SIZE)
    print(f"   Optimal iterations (p=0.99): {optimal_iter}")
    
    # Least Squares fitting
    print("\n[STEP 2] Least Squares Fitting...")
    ls_m, ls_c = fit_line_least_squares(points)
    print(f"   Result: y = {ls_m:.3f}x + {ls_c:.3f}")
    print(f"   Ideal:  y = {LINE_M:.3f}x + {LINE_C:.3f}")
    
    ls_error_m = abs(ls_m - LINE_M)
    ls_error_c = abs(ls_c - LINE_C)
    print(f"   Error: slope={ls_error_m:.3f}, intercept={ls_error_c:.3f}")
    
    # RANSAC fitting
    print("\n[STEP 3] RANSAC Fitting...")
    print(f"   Iterations: {RANSAC_ITERATIONS}")
    print(f"   Threshold: {RANSAC_THRESHOLD}")
    
    ransac_m, ransac_c, ransac_inliers, history = ransac_line_fitting(
        points, RANSAC_ITERATIONS, RANSAC_THRESHOLD, RANSAC_SAMPLE_SIZE
    )
    
    print(f"   Result: y = {ransac_m:.3f}x + {ransac_c:.3f}")
    print(f"   Ideal:  y = {LINE_M:.3f}x + {LINE_C:.3f}")
    
    ransac_error_m = abs(ransac_m - LINE_M)
    ransac_error_c = abs(ransac_c - LINE_C)
    print(f"   Error: slope={ransac_error_m:.3f}, intercept={ransac_error_c:.3f}")
    print(f"   Detected inliers: {np.sum(ransac_inliers)}")
    
    # Visualisasi
    print("\n[STEP 4] Visualisasi...")
    visualize_comparison(points, labels, (ls_m, ls_c), (ransac_m, ransac_c), 
                         ransac_inliers)
    visualize_ransac_progress(history)
    
    # Demo tambahan
    demo_outlier_ratio_effect()
    demo_threshold_effect()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN RANSAC")
    print("=" * 60)
    print(f"""
HASIL PERBANDINGAN:

                    Least Squares    RANSAC
Slope (m)           {ls_m:10.3f}      {ransac_m:10.3f}
Intercept (c)       {ls_c:10.3f}      {ransac_c:10.3f}
Error slope         {ls_error_m:10.3f}      {ransac_error_m:10.3f}
Error intercept     {ls_error_c:10.3f}      {ransac_error_c:10.3f}

Ground Truth: y = {LINE_M}x + {LINE_C}

KESIMPULAN:
├── Least Squares sensitif terhadap outliers
├── RANSAC robust terhadap outliers
└── RANSAC lebih baik untuk data dengan noise tinggi

PENGGUNAAN OPENCV:

# RANSAC untuk Homography
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# RANSAC untuk Fundamental Matrix  
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

# RANSAC untuk Affine Transform
M, mask = cv2.estimateAffine2D(src_pts, dst_pts, method=cv2.RANSAC)

PARAMETER PENTING:
1. threshold: sesuaikan dengan expected noise level
2. iterations: gunakan formula atau cukup besar (100-1000)
3. confidence: biasanya 0.99 untuk hasil reliable
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
