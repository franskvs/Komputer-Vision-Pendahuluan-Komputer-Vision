#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 3: BLOCK MATCHING STEREO
=============================================================================
Deskripsi:
    Program untuk melakukan stereo matching menggunakan algoritma Block
    Matching (BM). Block Matching adalah metode dasar untuk menghitung
    disparity map dari pasangan gambar stereo.

Konsep Block Matching:
    1. Untuk setiap pixel di gambar kiri, cari pixel yang matching di
       gambar kanan dengan membandingkan block/window
    2. Metric yang digunakan: Sum of Absolute Differences (SAD) atau
       Sum of Squared Differences (SSD)
    3. Disparity = posisi x di kiri - posisi x di kanan

Parameter Penting:
    - numDisparities: range pencarian disparity (harus kelipatan 16)
    - blockSize: ukuran window untuk matching (ganjil, >= 5)

Kelebihan:
    - Cepat dan sederhana
    - Cocok untuk real-time dengan hardware sederhana

Kekurangan:
    - Hasil noisy di area dengan texture rendah
    - Edge artifacts
    - Tidak handle occlusion dengan baik

Output:
    - Disparity map
    - Visualisasi dengan colormap
    - Analisis parameter

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

# Path ke gambar stereo (gunakan hasil rectification)
DATA_DIR = Path(__file__).parent / "data"
LEFT_IMAGE = DATA_DIR / "rectified" / "rectified_left.png"
RIGHT_IMAGE = DATA_DIR / "rectified" / "rectified_right.png"

# Jika tidak ada, coba gambar original
LEFT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_left.png"
RIGHT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_right.png"

# Path output
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "disparity"

# Parameter Block Matching
# numDisparities: max disparity - min disparity (kelipatan 16)
# Semakin besar, semakin besar range depth yang bisa dideteksi
# Nilai tipikal: 64, 128, 256
NUM_DISPARITIES = 64

# blockSize: ukuran window untuk matching
# Semakin besar, hasil lebih smooth tapi kurang detail
# Nilai tipikal: 5, 11, 15, 21
BLOCK_SIZE = 15

# Parameter tambahan
MIN_DISPARITY = 0  # Offset disparity minimum

# Pre-filter parameters (untuk meningkatkan kualitas matching)
PREFILTER_CAP = 31  # Clipping untuk prefilter (0-63)
PREFILTER_SIZE = 9  # Ukuran prefilter (5-255, ganjil)

# Texture threshold (untuk filter area low texture)
TEXTURE_THRESHOLD = 10

# Uniqueness ratio (untuk filter ambiguous matches)
# Match diterima jika cost <= (1 + uniquenessRatio/100) * second_best
UNIQUENESS_RATIO = 15

# Speckle filter parameters
SPECKLE_WINDOW_SIZE = 100  # Ukuran window untuk speckle filter
SPECKLE_RANGE = 32  # Max perbedaan disparity dalam blob

# Colormap untuk visualisasi
COLORMAP = cv2.COLORMAP_JET  # Pilihan: JET, TURBO, INFERNO, PLASMA

# Auto-close settings (untuk otomatis menutup window)
AUTO_CLOSE_SECONDS = 2


# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def load_stereo_images():
    """
    Memuat gambar stereo dari file.
    
    Returns:
        Tuple (img_left, img_right) atau (None, None) jika gagal
    """
    # Coba load gambar rectified dulu
    left = cv2.imread(str(LEFT_IMAGE))
    right = cv2.imread(str(RIGHT_IMAGE))
    
    if left is not None and right is not None:
        print(f"[OK] Loaded rectified images from {LEFT_IMAGE.parent}")
        return left, right
    
    # Fallback ke gambar original
    left = cv2.imread(str(LEFT_IMAGE_FALLBACK))
    right = cv2.imread(str(RIGHT_IMAGE_FALLBACK))
    
    if left is not None and right is not None:
        print(f"[OK] Loaded original images from {LEFT_IMAGE_FALLBACK.parent}")
        return left, right
    
    return None, None


def create_block_matcher(num_disparities, block_size, 
                         prefilter_cap=31, prefilter_size=9,
                         texture_thresh=10, uniqueness=15,
                         speckle_window=100, speckle_range=32):
    """
    Membuat objek StereoBM dengan parameter yang dikonfigurasi.
    
    Args:
        num_disparities: Range pencarian disparity
        block_size: Ukuran window matching
        prefilter_cap: Parameter prefilter
        prefilter_size: Ukuran prefilter
        texture_thresh: Threshold untuk texture
        uniqueness: Uniqueness ratio
        speckle_window: Window size untuk speckle filter
        speckle_range: Range untuk speckle filter
        
    Returns:
        cv2.StereoBM object
    """
    # Validasi parameter
    if num_disparities % 16 != 0:
        num_disparities = (num_disparities // 16 + 1) * 16
        print(f"[WARNING] numDisparities adjusted to {num_disparities}")
    
    if block_size % 2 == 0:
        block_size += 1
        print(f"[WARNING] blockSize adjusted to {block_size}")
    
    # Buat stereo matcher
    stereo = cv2.StereoBM_create(
        numDisparities=num_disparities,
        blockSize=block_size
    )
    
    # Set parameter tambahan
    stereo.setPreFilterCap(prefilter_cap)
    stereo.setPreFilterSize(prefilter_size)
    stereo.setTextureThreshold(texture_thresh)
    stereo.setUniquenessRatio(uniqueness)
    stereo.setSpeckleWindowSize(speckle_window)
    stereo.setSpeckleRange(speckle_range)
    stereo.setMinDisparity(MIN_DISPARITY)
    
    return stereo


def compute_disparity(stereo, img_left, img_right):
    """
    Menghitung disparity map menggunakan Block Matching.
    
    Args:
        stereo: cv2.StereoBM object
        img_left: Gambar kiri (grayscale)
        img_right: Gambar kanan (grayscale)
        
    Returns:
        Tuple (disparity_raw, disparity_normalized, computation_time)
    """
    # Pastikan grayscale
    if len(img_left.shape) == 3:
        gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    else:
        gray_left = img_left
        
    if len(img_right.shape) == 3:
        gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    else:
        gray_right = img_right
    
    # Hitung disparity
    start_time = time.time()
    disparity = stereo.compute(gray_left, gray_right)
    end_time = time.time()
    
    computation_time = (end_time - start_time) * 1000  # ms
    
    # Disparity dari OpenCV dalam format fixed-point (Q11.4)
    # Bagi dengan 16 untuk mendapat nilai pixel yang sebenarnya
    disparity_float = disparity.astype(np.float32) / 16.0
    
    # Normalize untuk visualisasi
    disparity_normalized = cv2.normalize(
        disparity_float, None, 0, 255, cv2.NORM_MINMAX
    )
    disparity_normalized = disparity_normalized.astype(np.uint8)
    
    return disparity_float, disparity_normalized, computation_time


def visualize_disparity(disparity, colormap=cv2.COLORMAP_JET):
    """
    Membuat visualisasi disparity map dengan colormap.
    
    Args:
        disparity: Disparity map (normalized 0-255)
        colormap: OpenCV colormap
        
    Returns:
        Colored disparity image
    """
    return cv2.applyColorMap(disparity, colormap)


def show_matplotlib_auto_close(seconds=AUTO_CLOSE_SECONDS):
    """Tampilkan matplotlib sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(seconds)
    plt.close('all')


def wait_with_timeout(seconds=AUTO_CLOSE_SECONDS):
    """Menunggu input atau timeout; tekan 'q' untuk keluar lebih cepat."""
    timeout_ms = int(seconds * 1000)
    key = cv2.waitKey(timeout_ms)
    return key


def analyze_disparity(disparity_float, img_left):
    """
    Menganalisis statistik disparity map.
    
    Args:
        disparity_float: Disparity map (float, nilai asli)
        img_left: Gambar kiri untuk referensi
        
    Returns:
        Dictionary dengan statistik
    """
    # Mask untuk disparity valid (> 0)
    valid_mask = disparity_float > 0
    valid_disparity = disparity_float[valid_mask]
    
    if len(valid_disparity) == 0:
        return {
            'valid_percentage': 0,
            'min': 0, 'max': 0, 'mean': 0, 'std': 0
        }
    
    stats = {
        'valid_percentage': (np.sum(valid_mask) / disparity_float.size) * 100,
        'min': float(np.min(valid_disparity)),
        'max': float(np.max(valid_disparity)),
        'mean': float(np.mean(valid_disparity)),
        'std': float(np.std(valid_disparity)),
        'median': float(np.median(valid_disparity))
    }
    
    return stats


def compare_parameters(img_left, img_right, param_sets):
    """
    Membandingkan hasil dengan berbagai kombinasi parameter.
    
    Args:
        img_left, img_right: Gambar stereo
        param_sets: List of (numDisparities, blockSize) tuples
        
    Returns:
        List of (params, disparity, time) tuples
    """
    results = []
    
    for num_disp, block_size in param_sets:
        print(f"\n  Testing: numDisparities={num_disp}, blockSize={block_size}")
        
        stereo = create_block_matcher(num_disp, block_size)
        disp_float, disp_norm, comp_time = compute_disparity(
            stereo, img_left, img_right
        )
        
        stats = analyze_disparity(disp_float, img_left)
        
        results.append({
            'params': (num_disp, block_size),
            'disparity': disp_norm,
            'disparity_float': disp_float,
            'time': comp_time,
            'stats': stats
        })
        
        print(f"    Time: {comp_time:.2f} ms, "
              f"Valid: {stats['valid_percentage']:.1f}%")
    
    return results


def create_comparison_figure(img_left, results):
    """
    Membuat figure perbandingan berbagai parameter.
    
    Args:
        img_left: Gambar kiri untuk referensi
        results: List dari compare_parameters()
    """
    n_results = len(results)
    fig, axes = plt.subplots(2, (n_results + 1) // 2 + 1, 
                             figsize=(15, 8))
    axes = axes.flatten()
    
    # Original image
    axes[0].imshow(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original Left")
    axes[0].axis('off')
    
    # Disparity results
    for i, result in enumerate(results):
        num_disp, block_size = result['params']
        disp_colored = visualize_disparity(result['disparity'])
        
        axes[i + 1].imshow(cv2.cvtColor(disp_colored, cv2.COLOR_BGR2RGB))
        axes[i + 1].set_title(
            f"numDisp={num_disp}, block={block_size}\n"
            f"Time: {result['time']:.1f}ms"
        )
        axes[i + 1].axis('off')
    
    # Hide unused axes
    for j in range(n_results + 1, len(axes)):
        axes[j].axis('off')
    
    plt.tight_layout()
    return fig


def create_synthetic_stereo():
    """
    Membuat gambar stereo sintetis untuk testing.
    """
    height, width = 480, 640
    
    # Create base image with texture
    np.random.seed(42)
    base = np.random.randint(100, 200, (height, width), dtype=np.uint8)
    
    # Add some structure
    cv2.circle(base, (200, 240), 80, 50, -1)
    cv2.rectangle(base, (400, 180), (550, 350), 150, -1)
    cv2.circle(base, (100, 350), 50, 80, -1)
    
    # Add texture
    for _ in range(100):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        cv2.circle(base, (x, y), 3, np.random.randint(0, 255), -1)
    
    # Create stereo pair with known disparity
    img_left = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)
    
    # Right image: shift objects by different amounts (simulate depth)
    img_right = img_left.copy()
    
    # Shift the entire image slightly (background disparity)
    M = np.float32([[1, 0, -10], [0, 1, 0]])
    img_right = cv2.warpAffine(img_right, M, (width, height))
    
    return img_left, img_right


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("BLOCK MATCHING STEREO")
    print("="*60)
    print(f"numDisparities: {NUM_DISPARITIES}")
    print(f"blockSize: {BLOCK_SIZE}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load images
    print("\n[STEP 1] Memuat gambar stereo...")
    img_left, img_right = load_stereo_images()
    
    if img_left is None:
        print("[WARNING] Gambar tidak ditemukan. Membuat gambar sintetis...")
        img_left, img_right = create_synthetic_stereo()
    
    print(f"  Image size: {img_left.shape[1]}x{img_left.shape[0]}")
    
    # Create Block Matcher
    print("\n[STEP 2] Membuat Block Matcher...")
    stereo = create_block_matcher(
        NUM_DISPARITIES, BLOCK_SIZE,
        PREFILTER_CAP, PREFILTER_SIZE,
        TEXTURE_THRESHOLD, UNIQUENESS_RATIO,
        SPECKLE_WINDOW_SIZE, SPECKLE_RANGE
    )
    
    # Compute disparity
    print("\n[STEP 3] Menghitung disparity map...")
    disp_float, disp_norm, comp_time = compute_disparity(
        stereo, img_left, img_right
    )
    print(f"  Computation time: {comp_time:.2f} ms")
    print(f"  Frame rate: {1000/comp_time:.1f} fps")
    
    # Analyze
    print("\n[STEP 4] Menganalisis hasil...")
    stats = analyze_disparity(disp_float, img_left)
    print(f"  Valid disparity: {stats['valid_percentage']:.1f}%")
    print(f"  Disparity range: {stats['min']:.1f} - {stats['max']:.1f} pixels")
    print(f"  Mean disparity: {stats['mean']:.1f} ± {stats['std']:.1f}")
    
    # Visualize
    print("\n[STEP 5] Membuat visualisasi...")
    disp_colored = visualize_disparity(disp_norm, COLORMAP)
    
    # Save results
    cv2.imwrite(str(OUTPUT_DIR / "disparity_bm.png"), disp_norm)
    cv2.imwrite(str(OUTPUT_DIR / "disparity_bm_colored.png"), disp_colored)
    
    # Save float disparity as numpy array for further processing
    np.save(str(OUTPUT_DIR / "disparity_bm_float.npy"), disp_float)
    
    print(f"  Saved: {OUTPUT_DIR / 'disparity_bm.png'}")
    print(f"  Saved: {OUTPUT_DIR / 'disparity_bm_colored.png'}")
    
    # Compare different parameters
    print("\n[STEP 6] Membandingkan berbagai parameter...")
    param_sets = [
        (48, 5),
        (64, 11),
        (64, 21),
        (128, 15),
    ]
    
    results = compare_parameters(img_left, img_right, param_sets)
    
    # Create comparison figure
    fig = create_comparison_figure(img_left, results)
    fig.savefig(str(OUTPUT_DIR / "bm_parameter_comparison.png"), 
                dpi=150, bbox_inches='tight')
    print(f"  Saved: {OUTPUT_DIR / 'bm_parameter_comparison.png'}")
    
    # Display results
    print("\n[STEP 7] Menampilkan hasil...")
    
    # Create side-by-side view
    disp_vis = cv2.resize(disp_colored, (img_left.shape[1], img_left.shape[0]))
    combined = np.hstack([img_left, disp_vis])
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(combined, "Left Image", (10, 30), font, 0.8, (255, 255, 255), 2)
    cv2.putText(combined, f"Disparity (BM, {comp_time:.1f}ms)", 
                (img_left.shape[1] + 10, 30), font, 0.8, (255, 255, 255), 2)
    
    cv2.imshow("Block Matching Stereo", combined)
    
    # Show matplotlib comparison
    show_matplotlib_auto_close()
    
    print(f"\nAuto close dalam {AUTO_CLOSE_SECONDS} detik (tekan 'q' untuk keluar)...")
    cv2.waitKey(int(AUTO_CLOSE_SECONDS * 1000))
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] Block Matching selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")
    
    # Print tips
    print("\n" + "="*60)
    print("TIPS PARAMETER TUNING")
    print("="*60)
    print("1. numDisparities: Tingkatkan jika objek dekat tidak terdeteksi")
    print("2. blockSize: Tingkatkan untuk hasil lebih smooth (tapi kurang detail)")
    print("3. uniquenessRatio: Tingkatkan untuk filter false matches")
    print("4. speckleWindowSize: Tingkatkan untuk remove noise lebih banyak")


if __name__ == "__main__":
    main()
