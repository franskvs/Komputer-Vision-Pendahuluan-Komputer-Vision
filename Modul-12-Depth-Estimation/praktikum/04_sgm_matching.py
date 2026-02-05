#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 4: SEMI-GLOBAL MATCHING (SGM)
=============================================================================
Deskripsi:
    Program untuk melakukan stereo matching menggunakan algoritma Semi-Global
    Matching (SGM). SGM adalah algoritma yang lebih advanced dari Block Matching,
    memberikan hasil yang lebih smooth dan akurat.

Konsep SGM:
    1. Hitung matching cost untuk setiap pixel (seperti BM)
    2. Agregasi cost secara global dengan meminimalkan energy function:
       E(D) = Σ[C(p, Dp) + P1·T[|Dp - Dq| = 1] + P2·T[|Dp - Dq| > 1]]
    3. P1 = penalty untuk perubahan disparity ±1
    4. P2 = penalty untuk perubahan disparity > 1
    5. Agregasi dilakukan dari berbagai arah (8 atau 16)

Kelebihan SGM vs Block Matching:
    - Hasil lebih smooth dan konsisten
    - Better handling of textureless regions
    - Edge-aware smoothing (P2 adaptive)
    - Reduced streaking artifacts

Parameter Penting:
    - numDisparities: range disparity
    - blockSize: lebih kecil dari BM (biasanya 3-5)
    - P1, P2: smoothness penalties (OpenCV: calculated automatically)
    - mode: SGBM_MODE_SGBM (5 directions) atau HH (8 directions)

Output:
    - Disparity map
    - Perbandingan dengan Block Matching
    - Analisis kualitas

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
Dependensi: opencv-python, numpy, matplotlib
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time

# =============================================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# =============================================================================

# Path ke gambar stereo
DATA_DIR = Path(__file__).parent / "data"
LEFT_IMAGE = DATA_DIR / "rectified" / "rectified_left.png"
RIGHT_IMAGE = DATA_DIR / "rectified" / "rectified_right.png"

# Fallback
LEFT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_left.png"
RIGHT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_right.png"

# Path output
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "disparity"

# Parameter SGM
NUM_DISPARITIES = 64  # Kelipatan 16
BLOCK_SIZE = 5  # Lebih kecil dari BM (biasanya 3, 5, 7)

# Minimum disparity
MIN_DISPARITY = 0

# Smoothness penalties (P1 < P2)
# Jika tidak diset, OpenCV menghitung otomatis:
# P1 = 8 * num_channels * blockSize^2
# P2 = 32 * num_channels * blockSize^2
P1_MULTIPLIER = 8
P2_MULTIPLIER = 32

# Mode: cv2.STEREO_SGBM_MODE_SGBM (5 dirs) atau cv2.STEREO_SGBM_MODE_HH (8 dirs)
# MODE_HH: lebih akurat tapi lebih lambat
USE_FULL_DP = True  # True = 8 directions, False = 5 directions

# Pre-filter cap
PREFILTER_CAP = 63

# Uniqueness ratio
UNIQUENESS_RATIO = 10

# Speckle filtering
SPECKLE_WINDOW_SIZE = 100
SPECKLE_RANGE = 32

# Disp12MaxDiff: untuk left-right consistency check
# -1 = disable, > 0 = max allowed difference
DISP12_MAX_DIFF = 1

# Colormap
COLORMAP = cv2.COLORMAP_TURBO

# Auto-close settings
AUTO_CLOSE_SECONDS = 2

# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def load_stereo_images():
    """Memuat gambar stereo dari file."""
    left = cv2.imread(str(LEFT_IMAGE))
    right = cv2.imread(str(RIGHT_IMAGE))
    
    if left is not None and right is not None:
        return left, right
    
    left = cv2.imread(str(LEFT_IMAGE_FALLBACK))
    right = cv2.imread(str(RIGHT_IMAGE_FALLBACK))
    
    if left is not None and right is not None:
        return left, right
    
    return None, None


def create_sgbm_matcher(num_disparities, block_size, num_channels=3):
    """
    Membuat objek StereoSGBM dengan parameter yang dikonfigurasi.
    
    OpenCV StereoSGBM adalah implementasi dari algoritma Semi-Global
    Block Matching yang diperkenalkan oleh Hirschmuller (2005, 2008).
    
    Args:
        num_disparities: Range pencarian disparity
        block_size: Ukuran window (lebih kecil dari BM)
        num_channels: Jumlah channel gambar (1 untuk grayscale, 3 untuk color)
        
    Returns:
        cv2.StereoSGBM object
    """
    # Validasi parameter
    if num_disparities % 16 != 0:
        num_disparities = (num_disparities // 16 + 1) * 16
    
    if block_size % 2 == 0:
        block_size += 1
    
    # Hitung P1 dan P2
    P1 = P1_MULTIPLIER * num_channels * block_size ** 2
    P2 = P2_MULTIPLIER * num_channels * block_size ** 2
    
    # Mode
    if USE_FULL_DP:
        mode = cv2.STEREO_SGBM_MODE_HH  # 8 directions
    else:
        mode = cv2.STEREO_SGBM_MODE_SGBM  # 5 directions
    
    # Buat SGBM matcher
    sgbm = cv2.StereoSGBM_create(
        minDisparity=MIN_DISPARITY,
        numDisparities=num_disparities,
        blockSize=block_size,
        P1=P1,
        P2=P2,
        disp12MaxDiff=DISP12_MAX_DIFF,
        preFilterCap=PREFILTER_CAP,
        uniquenessRatio=UNIQUENESS_RATIO,
        speckleWindowSize=SPECKLE_WINDOW_SIZE,
        speckleRange=SPECKLE_RANGE,
        mode=mode
    )
    
    return sgbm


def create_bm_matcher(num_disparities, block_size):
    """Membuat Block Matcher untuk perbandingan."""
    if num_disparities % 16 != 0:
        num_disparities = (num_disparities // 16 + 1) * 16
    
    bm = cv2.StereoBM_create(
        numDisparities=num_disparities,
        blockSize=max(block_size * 2 + 1, 15)  # BM butuh blockSize lebih besar
    )
    bm.setMinDisparity(MIN_DISPARITY)
    bm.setUniquenessRatio(15)
    bm.setSpeckleWindowSize(SPECKLE_WINDOW_SIZE)
    bm.setSpeckleRange(SPECKLE_RANGE)
    
    return bm


def compute_disparity(stereo, img_left, img_right, is_sgbm=True):
    """
    Menghitung disparity map.
    
    Args:
        stereo: Stereo matcher (SGBM atau BM)
        img_left, img_right: Gambar stereo
        is_sgbm: True jika menggunakan SGBM (bisa input color)
        
    Returns:
        Tuple (disparity_float, disparity_normalized, computation_time)
    """
    # SGBM bisa langsung menggunakan color image
    # BM memerlukan grayscale
    if not is_sgbm:
        if len(img_left.shape) == 3:
            img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
            img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    
    # Compute disparity
    start_time = time.time()
    disparity = stereo.compute(img_left, img_right)
    end_time = time.time()
    
    computation_time = (end_time - start_time) * 1000
    
    # Convert to float (divide by 16 for fixed-point format)
    disparity_float = disparity.astype(np.float32) / 16.0
    
    # Normalize for visualization
    disparity_normalized = cv2.normalize(
        disparity_float, None, 0, 255, cv2.NORM_MINMAX
    )
    disparity_normalized = disparity_normalized.astype(np.uint8)
    
    return disparity_float, disparity_normalized, computation_time


def apply_wls_filter(img_left, disparity_left, disparity_right=None):
    """
    Menerapkan Weighted Least Squares (WLS) filter untuk post-processing.
    
    WLS filter membantu:
    - Mengisi holes
    - Edge-preserving smoothing
    - Mengurangi noise
    
    Args:
        img_left: Gambar kiri (untuk guided filtering)
        disparity_left: Disparity dari left-to-right matching
        disparity_right: Disparity dari right-to-left matching (opsional)
        
    Returns:
        Filtered disparity
    """
    # Lambda dan sigma untuk WLS
    wls_lambda = 8000
    wls_sigma = 1.5
    
    # Buat WLS filter
    wls_filter = cv2.ximgproc.createDisparityWLSFilterGeneric(False)
    wls_filter.setLambda(wls_lambda)
    wls_filter.setSigmaColor(wls_sigma)
    
    # Apply filter
    if disparity_right is not None:
        filtered = wls_filter.filter(disparity_left, img_left, 
                                     disparity_map_right=disparity_right)
    else:
        filtered = wls_filter.filter(disparity_left, img_left)
    
    return filtered


def show_matplotlib_auto_close(seconds=AUTO_CLOSE_SECONDS):
    """Tampilkan matplotlib sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(seconds)
    plt.close('all')


def compute_with_lr_check(sgbm, img_left, img_right):
    """
    Menghitung disparity dengan left-right consistency check.
    
    Args:
        sgbm: StereoSGBM matcher
        img_left, img_right: Gambar stereo
        
    Returns:
        Tuple (disparity_left, disparity_right, filtered)
    """
    # Left to right
    disparity_left = sgbm.compute(img_left, img_right)
    
    # Create right matcher
    right_matcher = cv2.ximgproc.createRightMatcher(sgbm)
    
    # Right to left
    disparity_right = right_matcher.compute(img_right, img_left)
    
    # Apply WLS filter
    filtered = apply_wls_filter(img_left, disparity_left, disparity_right)
    
    return disparity_left, disparity_right, filtered


def analyze_disparity_quality(disparity_float, reference=None):
    """
    Menganalisis kualitas disparity map.
    
    Args:
        disparity_float: Disparity map
        reference: Ground truth disparity (opsional)
        
    Returns:
        Dictionary dengan metrics
    """
    valid_mask = disparity_float > 0
    valid_disp = disparity_float[valid_mask]
    
    metrics = {
        'valid_percentage': (np.sum(valid_mask) / disparity_float.size) * 100,
        'min': float(np.min(valid_disp)) if len(valid_disp) > 0 else 0,
        'max': float(np.max(valid_disp)) if len(valid_disp) > 0 else 0,
        'mean': float(np.mean(valid_disp)) if len(valid_disp) > 0 else 0,
        'std': float(np.std(valid_disp)) if len(valid_disp) > 0 else 0,
    }
    
    if reference is not None:
        # Hitung error metrics
        valid_both = (disparity_float > 0) & (reference > 0)
        if np.sum(valid_both) > 0:
            error = np.abs(disparity_float[valid_both] - reference[valid_both])
            metrics['mae'] = float(np.mean(error))
            metrics['rmse'] = float(np.sqrt(np.mean(error ** 2)))
            metrics['bad_1'] = float(np.mean(error > 1) * 100)  # % error > 1
            metrics['bad_2'] = float(np.mean(error > 2) * 100)  # % error > 2
    
    return metrics


def create_comparison_visualization(img_left, bm_disp, sgbm_disp, wls_disp=None):
    """
    Membuat visualisasi perbandingan BM vs SGM.
    
    Args:
        img_left: Gambar kiri
        bm_disp: Disparity dari Block Matching
        sgbm_disp: Disparity dari SGBM
        wls_disp: Disparity setelah WLS filter (opsional)
        
    Returns:
        Combined visualization image
    """
    # Apply colormap
    bm_colored = cv2.applyColorMap(bm_disp, COLORMAP)
    sgbm_colored = cv2.applyColorMap(sgbm_disp, COLORMAP)
    
    if wls_disp is not None:
        wls_norm = cv2.normalize(wls_disp, None, 0, 255, cv2.NORM_MINMAX)
        wls_colored = cv2.applyColorMap(wls_norm.astype(np.uint8), COLORMAP)
        
        # Create 2x2 grid
        h, w = img_left.shape[:2]
        grid = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)
        
        grid[:h, :w] = img_left
        grid[:h, w:] = bm_colored
        grid[h:, :w] = sgbm_colored
        grid[h:, w:] = wls_colored
        
        # Add labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(grid, "Original", (10, 30), font, 0.8, (255, 255, 255), 2)
        cv2.putText(grid, "Block Matching", (w + 10, 30), font, 0.8, (255, 255, 255), 2)
        cv2.putText(grid, "SGBM", (10, h + 30), font, 0.8, (255, 255, 255), 2)
        cv2.putText(grid, "SGBM + WLS Filter", (w + 10, h + 30), font, 0.8, (255, 255, 255), 2)
    else:
        # Create 1x3 grid
        h, w = img_left.shape[:2]
        grid = np.zeros((h, w * 3, 3), dtype=np.uint8)
        
        grid[:, :w] = img_left
        grid[:, w:2*w] = bm_colored
        grid[:, 2*w:] = sgbm_colored
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(grid, "Original", (10, 30), font, 0.8, (255, 255, 255), 2)
        cv2.putText(grid, "Block Matching", (w + 10, 30), font, 0.8, (255, 255, 255), 2)
        cv2.putText(grid, "SGBM", (2*w + 10, 30), font, 0.8, (255, 255, 255), 2)
    
    return grid


def create_synthetic_stereo():
    """Membuat gambar stereo sintetis untuk testing."""
    height, width = 480, 640
    
    np.random.seed(42)
    
    # Create textured background
    left = np.zeros((height, width, 3), dtype=np.uint8)
    right = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Gradient background
    for y in range(height):
        left[y, :] = [100 + y//4, 80, 60]
        right[y, :] = [100 + y//4, 80, 60]
    
    # Add random texture
    noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
    left = cv2.add(left, noise)
    right = cv2.add(right, noise)
    
    # Add objects with different disparities
    objects = [
        (150, 200, 30, 60, (255, 100, 100)),  # x, y, disp, radius, color
        (320, 250, 20, 80, (100, 255, 100)),
        (480, 180, 40, 50, (100, 100, 255)),
    ]
    
    for cx, cy, disp, radius, color in objects:
        cv2.circle(left, (cx, cy), radius, color, -1)
        cv2.circle(right, (cx - disp, cy), radius, color, -1)
    
    return left, right


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("SEMI-GLOBAL MATCHING (SGM)")
    print("="*60)
    print(f"numDisparities: {NUM_DISPARITIES}")
    print(f"blockSize: {BLOCK_SIZE}")
    print(f"Full DP (8 directions): {USE_FULL_DP}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load images
    print("\n[STEP 1] Memuat gambar stereo...")
    img_left, img_right = load_stereo_images()
    
    if img_left is None:
        print("[WARNING] Gambar tidak ditemukan. Membuat gambar sintetis...")
        img_left, img_right = create_synthetic_stereo()
    
    print(f"  Image size: {img_left.shape[1]}x{img_left.shape[0]}")
    
    # Create matchers
    print("\n[STEP 2] Membuat stereo matchers...")
    num_channels = 1 if len(img_left.shape) == 2 else img_left.shape[2]
    
    sgbm = create_sgbm_matcher(NUM_DISPARITIES, BLOCK_SIZE, num_channels)
    bm = create_bm_matcher(NUM_DISPARITIES, BLOCK_SIZE)
    
    # Compute disparity with BM
    print("\n[STEP 3] Menghitung disparity dengan Block Matching...")
    bm_float, bm_norm, bm_time = compute_disparity(bm, img_left, img_right, is_sgbm=False)
    print(f"  Time: {bm_time:.2f} ms ({1000/bm_time:.1f} fps)")
    
    # Compute disparity with SGBM
    print("\n[STEP 4] Menghitung disparity dengan SGBM...")
    sgbm_float, sgbm_norm, sgbm_time = compute_disparity(sgbm, img_left, img_right, is_sgbm=True)
    print(f"  Time: {sgbm_time:.2f} ms ({1000/sgbm_time:.1f} fps)")
    
    # Try WLS filtering if opencv-contrib is available
    wls_float = None
    wls_norm = None
    try:
        print("\n[STEP 5] Menerapkan WLS filter...")
        start = time.time()
        disp_left, disp_right, wls_float = compute_with_lr_check(sgbm, img_left, img_right)
        wls_time = (time.time() - start) * 1000
        
        wls_float = wls_float.astype(np.float32) / 16.0
        wls_norm = cv2.normalize(wls_float, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        print(f"  Time with WLS: {wls_time:.2f} ms")
    except AttributeError:
        print("  [WARNING] WLS filter tidak tersedia (butuh opencv-contrib)")
    
    # Analyze results
    print("\n[STEP 6] Menganalisis hasil...")
    
    bm_metrics = analyze_disparity_quality(bm_float)
    sgbm_metrics = analyze_disparity_quality(sgbm_float)
    
    print("\n  Block Matching:")
    print(f"    Valid: {bm_metrics['valid_percentage']:.1f}%")
    print(f"    Range: {bm_metrics['min']:.1f} - {bm_metrics['max']:.1f}")
    print(f"    Mean: {bm_metrics['mean']:.2f} ± {bm_metrics['std']:.2f}")
    
    print("\n  SGBM:")
    print(f"    Valid: {sgbm_metrics['valid_percentage']:.1f}%")
    print(f"    Range: {sgbm_metrics['min']:.1f} - {sgbm_metrics['max']:.1f}")
    print(f"    Mean: {sgbm_metrics['mean']:.2f} ± {sgbm_metrics['std']:.2f}")
    
    if wls_float is not None:
        wls_metrics = analyze_disparity_quality(wls_float)
        print("\n  SGBM + WLS:")
        print(f"    Valid: {wls_metrics['valid_percentage']:.1f}%")
        print(f"    Range: {wls_metrics['min']:.1f} - {wls_metrics['max']:.1f}")
        print(f"    Mean: {wls_metrics['mean']:.2f} ± {wls_metrics['std']:.2f}")
    
    # Save results
    print("\n[STEP 7] Menyimpan hasil...")
    
    cv2.imwrite(str(OUTPUT_DIR / "disparity_sgbm.png"), sgbm_norm)
    cv2.imwrite(str(OUTPUT_DIR / "disparity_sgbm_colored.png"), 
                cv2.applyColorMap(sgbm_norm, COLORMAP))
    np.save(str(OUTPUT_DIR / "disparity_sgbm_float.npy"), sgbm_float)
    
    if wls_norm is not None:
        cv2.imwrite(str(OUTPUT_DIR / "disparity_sgbm_wls.png"), wls_norm)
        cv2.imwrite(str(OUTPUT_DIR / "disparity_sgbm_wls_colored.png"),
                    cv2.applyColorMap(wls_norm, COLORMAP))
    
    # Create comparison visualization
    comparison = create_comparison_visualization(img_left, bm_norm, sgbm_norm, wls_norm)
    cv2.imwrite(str(OUTPUT_DIR / "comparison_bm_vs_sgbm.png"), comparison)
    
    print(f"  Saved to: {OUTPUT_DIR}")
    
    # Display
    print("\n[STEP 8] Menampilkan hasil...")
    
    # Resize if too large
    max_width = 1400
    if comparison.shape[1] > max_width:
        scale = max_width / comparison.shape[1]
        comparison = cv2.resize(comparison, None, fx=scale, fy=scale)
    
    cv2.imshow("BM vs SGBM Comparison", comparison)
    
    # Create matplotlib figure for detailed analysis
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Left Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(sgbm_float, cmap='turbo')
    axes[0, 1].set_title(f"SGBM Disparity\n({sgbm_time:.1f} ms)")
    axes[0, 1].axis('off')
    plt.colorbar(axes[0, 1].images[0], ax=axes[0, 1], label='Disparity (pixels)')
    
    axes[1, 0].hist(sgbm_float[sgbm_float > 0].flatten(), bins=50, color='blue', alpha=0.7)
    axes[1, 0].set_title("Disparity Histogram")
    axes[1, 0].set_xlabel("Disparity (pixels)")
    axes[1, 0].set_ylabel("Frequency")
    
    # Speed comparison
    methods = ['BM', 'SGBM']
    times = [bm_time, sgbm_time]
    colors = ['green', 'blue']
    
    if wls_float is not None:
        methods.append('SGBM+WLS')
        times.append(wls_time)
        colors.append('orange')
    
    axes[1, 1].barh(methods, times, color=colors)
    axes[1, 1].set_xlabel("Time (ms)")
    axes[1, 1].set_title("Computation Time Comparison")
    
    for i, t in enumerate(times):
        axes[1, 1].text(t + 1, i, f"{t:.1f} ms", va='center')
    
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "sgbm_analysis.png"), dpi=150, bbox_inches='tight')
    
    show_matplotlib_auto_close()
    
    print(f"\nAuto close dalam {AUTO_CLOSE_SECONDS} detik (tekan 'q' untuk keluar)...")
    cv2.waitKey(int(AUTO_CLOSE_SECONDS * 1000))
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] SGBM selesai!")
    
    # Print comparison summary
    print("\n" + "="*60)
    print("PERBANDINGAN BM vs SGBM")
    print("="*60)
    print(f"{'Metric':<25} {'Block Matching':<20} {'SGBM':<20}")
    print("-"*65)
    print(f"{'Computation Time':<25} {bm_time:.2f} ms{'':<12} {sgbm_time:.2f} ms")
    print(f"{'Valid Pixels':<25} {bm_metrics['valid_percentage']:.1f}%{'':<14} {sgbm_metrics['valid_percentage']:.1f}%")
    print(f"{'Mean Disparity':<25} {bm_metrics['mean']:.2f}{'':<15} {sgbm_metrics['mean']:.2f}")
    print(f"{'Std Disparity':<25} {bm_metrics['std']:.2f}{'':<15} {sgbm_metrics['std']:.2f}")


if __name__ == "__main__":
    main()
