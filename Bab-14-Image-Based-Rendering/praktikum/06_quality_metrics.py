"""
Praktikum 14.6: Quality Metrics for View Synthesis
=================================================

Program ini mendemonstrasikan quality metrics:
1. PSNR (Peak Signal-to-Noise Ratio)
2. SSIM (Structural Similarity Index)
3. MSE (Mean Squared Error)
4. Perceptual metrics
5. Comparison tools

Teori:
------
Quality metrics mengukur seberapa baik synthesized view
dibandingkan dengan ground truth.

PSNR = 10 * log10(MAX² / MSE)
SSIM mengukur luminance, contrast, dan structure similarity
LPIPS mengukur perceptual similarity

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output" / "output6"

# SSIM parameters
SSIM_K1 = 0.01                     # Stability constant
SSIM_K2 = 0.03                     # Stability constant
SSIM_WINDOW_SIZE = 11              # Window size untuk SSIM
SSIM_SIGMA = 1.5                   # Gaussian sigma

# Quality thresholds
PSNR_GOOD = 30                     # PSNR > 30 dB dianggap bagus
SSIM_GOOD = 0.9                    # SSIM > 0.9 dianggap bagus

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_opencv():
    """Periksa ketersediaan OpenCV."""
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        return True
    except ImportError:
        print("✗ OpenCV tidak terinstall!")
        return False

def load_test_images():
    """Load atau create test images."""
    import cv2
    
    # Cari existing images
    test_dir = DATA_DIR / "quality_test"
    if test_dir.exists():
        files = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
        if len(files) >= 2:
            gt = cv2.imread(str(files[0]))
            synth = cv2.imread(str(files[1]))
            if gt is not None and synth is not None:
                return gt, synth
    
    # Create synthetic test pair
    return create_synthetic_test_images()

def create_synthetic_test_images():
    """Buat synthetic test images."""
    import cv2
    
    h, w = 480, 640
    
    # Ground truth
    gt = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(h):
        for x in range(w):
            gt[y, x] = [
                int(50 + 150 * x / w),
                int(100 + 100 * y / h),
                int(200 - 100 * x / w)
            ]
    
    # Features
    np.random.seed(42)
    for _ in range(50):
        x = np.random.randint(50, w - 50)
        y = np.random.randint(50, h - 50)
        r = np.random.randint(10, 40)
        color = [np.random.randint(0, 255) for _ in range(3)]
        cv2.circle(gt, (x, y), r, color, -1)
    
    # Add text
    cv2.putText(gt, "Ground Truth", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Synthesized (dengan distortions)
    synth = gt.copy()
    
    # Add noise
    noise = np.random.normal(0, 15, synth.shape).astype(np.float32)
    synth = np.clip(synth.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    # Slight blur
    synth = cv2.GaussianBlur(synth, (3, 3), 0.5)
    
    # Color shift
    synth = synth.astype(np.float32)
    synth[:, :, 0] = np.clip(synth[:, :, 0] * 0.95, 0, 255)  # Reduce blue
    synth[:, :, 2] = np.clip(synth[:, :, 2] * 1.05, 0, 255)  # Increase red
    synth = synth.astype(np.uint8)
    
    return gt, synth

# ============================================================
# BASIC METRICS
# ============================================================

def compute_mse(img1, img2):
    """
    Compute Mean Squared Error.
    
    Args:
        img1, img2: Input images (sama size)
    
    Returns:
        MSE value
    """
    diff = img1.astype(float) - img2.astype(float)
    mse = np.mean(diff ** 2)
    return mse

def compute_rmse(img1, img2):
    """
    Compute Root Mean Squared Error.
    
    Args:
        img1, img2: Input images
    
    Returns:
        RMSE value
    """
    return np.sqrt(compute_mse(img1, img2))

def compute_mae(img1, img2):
    """
    Compute Mean Absolute Error.
    
    Args:
        img1, img2: Input images
    
    Returns:
        MAE value
    """
    diff = np.abs(img1.astype(float) - img2.astype(float))
    return np.mean(diff)

def compute_psnr(img1, img2, max_val=255):
    """
    Compute Peak Signal-to-Noise Ratio.
    
    PSNR = 10 * log10(MAX² / MSE)
    
    Args:
        img1, img2: Input images
        max_val: Maximum pixel value (255 untuk 8-bit)
    
    Returns:
        PSNR dalam dB
    """
    mse = compute_mse(img1, img2)
    
    if mse == 0:
        return float('inf')
    
    psnr = 10 * np.log10(max_val**2 / mse)
    return psnr

# ============================================================
# SSIM METRIC
# ============================================================

def gaussian_kernel(size, sigma):
    """Create Gaussian kernel."""
    x = np.arange(size) - size // 2
    kernel = np.exp(-x**2 / (2 * sigma**2))
    kernel = kernel / kernel.sum()
    return kernel

def compute_ssim_channel(img1, img2, k1=0.01, k2=0.03, L=255):
    """
    Compute SSIM untuk single channel.
    
    SSIM(x,y) = (2μxμy + c1)(2σxy + c2) / (μx² + μy² + c1)(σx² + σy² + c2)
    
    Args:
        img1, img2: Single channel images (float)
        k1, k2: Stability constants
        L: Dynamic range
    
    Returns:
        SSIM value, SSIM map
    """
    import cv2
    
    c1 = (k1 * L) ** 2
    c2 = (k2 * L) ** 2
    
    # Gaussian filtering
    sigma = SSIM_SIGMA
    win_size = SSIM_WINDOW_SIZE
    
    # Mean
    mu1 = cv2.GaussianBlur(img1, (win_size, win_size), sigma)
    mu2 = cv2.GaussianBlur(img2, (win_size, win_size), sigma)
    
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu12 = mu1 * mu2
    
    # Variance
    sigma1_sq = cv2.GaussianBlur(img1 ** 2, (win_size, win_size), sigma) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(img2 ** 2, (win_size, win_size), sigma) - mu2_sq
    sigma12 = cv2.GaussianBlur(img1 * img2, (win_size, win_size), sigma) - mu12
    
    # SSIM formula
    numerator = (2 * mu12 + c1) * (2 * sigma12 + c2)
    denominator = (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
    
    ssim_map = numerator / (denominator + 1e-10)
    ssim = np.mean(ssim_map)
    
    return ssim, ssim_map

def compute_ssim(img1, img2):
    """
    Compute SSIM untuk color image.
    
    Args:
        img1, img2: BGR images
    
    Returns:
        SSIM value, SSIM map
    """
    import cv2
    
    # Convert ke float
    img1 = img1.astype(float)
    img2 = img2.astype(float)
    
    # Compute per channel
    ssim_values = []
    ssim_maps = []
    
    for c in range(img1.shape[2]):
        ssim, ssim_map = compute_ssim_channel(img1[:, :, c], img2[:, :, c])
        ssim_values.append(ssim)
        ssim_maps.append(ssim_map)
    
    # Average
    mean_ssim = np.mean(ssim_values)
    mean_map = np.mean(ssim_maps, axis=0)
    
    return mean_ssim, mean_map

def compute_ms_ssim(img1, img2, weights=None):
    """
    Compute Multi-Scale SSIM.
    
    Args:
        img1, img2: Input images
        weights: Weights untuk setiap scale
    
    Returns:
        MS-SSIM value
    """
    import cv2
    
    if weights is None:
        weights = [0.0448, 0.2856, 0.3001, 0.2363, 0.1333]
    
    levels = len(weights)
    
    mssim = []
    mcs = []
    
    for level in range(levels):
        ssim, ssim_map = compute_ssim(img1, img2)
        
        # Compute contrast/structure term
        mu1 = cv2.GaussianBlur(img1.astype(float), (11, 11), 1.5)
        mu2 = cv2.GaussianBlur(img2.astype(float), (11, 11), 1.5)
        
        sigma1_sq = cv2.GaussianBlur(img1.astype(float)**2, (11, 11), 1.5) - mu1**2
        sigma2_sq = cv2.GaussianBlur(img2.astype(float)**2, (11, 11), 1.5) - mu2**2
        sigma12 = cv2.GaussianBlur(img1.astype(float)*img2.astype(float), (11, 11), 1.5) - mu1*mu2
        
        c2 = (0.03 * 255) ** 2
        cs = np.mean((2 * sigma12 + c2) / (sigma1_sq + sigma2_sq + c2))
        
        mssim.append(ssim)
        mcs.append(cs)
        
        if level < levels - 1:
            img1 = cv2.resize(img1, None, fx=0.5, fy=0.5)
            img2 = cv2.resize(img2, None, fx=0.5, fy=0.5)
    
    # Combine
    mcs = np.array(mcs)
    mssim = np.array(mssim)
    
    # MS-SSIM = product of CS^weight * SSIM^weight_last
    ms_ssim = np.prod(mcs[:-1] ** weights[:-1]) * (mssim[-1] ** weights[-1])
    
    return ms_ssim

# ============================================================
# PERCEPTUAL METRICS (Simplified)
# ============================================================

def compute_edge_similarity(img1, img2):
    """
    Compute edge-based similarity.
    
    Args:
        img1, img2: Input images
    
    Returns:
        Edge similarity score
    """
    import cv2
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Compute edges
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    
    # Compare
    intersection = np.logical_and(edges1 > 0, edges2 > 0)
    union = np.logical_or(edges1 > 0, edges2 > 0)
    
    if union.sum() == 0:
        return 1.0
    
    iou = intersection.sum() / union.sum()
    
    return iou

def compute_histogram_similarity(img1, img2, method='correlation'):
    """
    Compute histogram-based similarity.
    
    Args:
        img1, img2: Input images
        method: 'correlation', 'chi-square', 'intersection', 'bhattacharyya'
    
    Returns:
        Similarity score
    """
    import cv2
    
    # Compute histograms
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    
    # Normalize
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    
    # Compare
    methods = {
        'correlation': cv2.HISTCMP_CORREL,
        'chi-square': cv2.HISTCMP_CHISQR,
        'intersection': cv2.HISTCMP_INTERSECT,
        'bhattacharyya': cv2.HISTCMP_BHATTACHARYYA
    }
    
    metric = cv2.compareHist(hist1, hist2, methods[method])
    
    return metric

def compute_frequency_similarity(img1, img2):
    """
    Compute frequency domain similarity.
    
    Args:
        img1, img2: Input images
    
    Returns:
        Frequency similarity score
    """
    import cv2
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(float)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY).astype(float)
    
    # FFT
    fft1 = np.fft.fft2(gray1)
    fft2 = np.fft.fft2(gray2)
    
    # Magnitude spectrum
    mag1 = np.abs(fft1)
    mag2 = np.abs(fft2)
    
    # Normalize
    mag1 = mag1 / mag1.max()
    mag2 = mag2 / mag2.max()
    
    # Similarity
    similarity = 1 - np.mean(np.abs(mag1 - mag2))
    
    return similarity

# ============================================================
# VISUALIZATION
# ============================================================

def create_difference_map(img1, img2, amplify=3):
    """
    Create difference visualization.
    
    Args:
        img1, img2: Input images
        amplify: Amplification factor
    
    Returns:
        Difference map (color-coded)
    """
    import cv2
    
    diff = np.abs(img1.astype(float) - img2.astype(float))
    diff = np.mean(diff, axis=2)  # Average across channels
    
    # Amplify
    diff = diff * amplify
    diff = np.clip(diff, 0, 255).astype(np.uint8)
    
    # Color map
    diff_color = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
    
    return diff_color

def create_ssim_map_visualization(ssim_map):
    """
    Visualize SSIM map.
    
    Args:
        ssim_map: SSIM map (0-1)
    
    Returns:
        Visualization (color-coded)
    """
    import cv2
    
    # Invert (1 = similar = green, 0 = different = red)
    ssim_vis = ((1 - ssim_map) * 255).astype(np.uint8)
    ssim_color = cv2.applyColorMap(ssim_vis, cv2.COLORMAP_JET)
    
    return ssim_color

def create_error_histogram(img1, img2):
    """
    Create error distribution histogram.
    
    Args:
        img1, img2: Input images
    
    Returns:
        Histogram image
    """
    import cv2
    
    # Compute errors
    diff = np.abs(img1.astype(float) - img2.astype(float))
    errors = diff.flatten()
    
    # Create histogram
    hist_h, hist_w = 300, 400
    hist_img = np.ones((hist_h, hist_w, 3), dtype=np.uint8) * 255
    
    # Compute histogram
    bins = 50
    hist, bin_edges = np.histogram(errors, bins=bins, range=(0, 100))
    
    # Normalize
    max_count = hist.max() if hist.max() > 0 else 1
    
    # Draw bars
    bar_width = hist_w // bins
    for i, count in enumerate(hist):
        height = int((count / max_count) * (hist_h - 40))
        x = i * bar_width
        y = hist_h - 30 - height
        
        cv2.rectangle(hist_img, (x + 1, y), (x + bar_width - 1, hist_h - 30), (100, 100, 255), -1)
    
    # Labels
    cv2.putText(hist_img, "Error Distribution", (hist_w // 2 - 70, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(hist_img, "Error Value", (hist_w // 2 - 40, hist_h - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    cv2.putText(hist_img, "Count", (5, hist_h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    return hist_img

def create_metrics_report(metrics_dict, output_path=None):
    """
    Create visual metrics report.
    
    Args:
        metrics_dict: Dictionary of metric names and values
        output_path: Optional path untuk save
    
    Returns:
        Report image
    """
    import cv2
    
    # Create report image
    h, w = 400, 500
    report = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Title
    cv2.putText(report, "Quality Metrics Report", (w // 2 - 120, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    cv2.line(report, (50, 60), (w - 50, 60), (0, 0, 0), 2)
    
    # Metrics
    y = 100
    for name, value in metrics_dict.items():
        # Determine quality
        if 'PSNR' in name:
            quality = "Good" if value > PSNR_GOOD else "Poor"
            color = (0, 150, 0) if value > PSNR_GOOD else (0, 0, 200)
        elif 'SSIM' in name:
            quality = "Good" if value > SSIM_GOOD else "Poor"
            color = (0, 150, 0) if value > SSIM_GOOD else (0, 0, 200)
        else:
            quality = ""
            color = (0, 0, 0)
        
        # Format value
        if isinstance(value, float):
            value_str = f"{value:.4f}"
        else:
            value_str = str(value)
        
        # Draw
        cv2.putText(report, f"{name}:", (60, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(report, value_str, (250, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        if quality:
            cv2.putText(report, f"({quality})", (380, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        y += 35
    
    # Footer
    cv2.line(report, (50, h - 50), (w - 50, h - 50), (0, 0, 0), 1)
    cv2.putText(report, f"Thresholds: PSNR > {PSNR_GOOD} dB, SSIM > {SSIM_GOOD}", 
                (60, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1)
    
    if output_path:
        cv2.imwrite(str(output_path), report)
    
    return report

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_basic_metrics():
    """Demo basic quality metrics."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Basic Quality Metrics")
    print("="*60)
    
    # Load images
    gt, synth = load_test_images()
    print(f"\n  Ground truth: {gt.shape}")
    print(f"  Synthesized: {synth.shape}")
    
    # Save images
    cv2.imwrite(str(OUTPUT_DIR / "quality_gt.jpg"), gt)
    cv2.imwrite(str(OUTPUT_DIR / "quality_synth.jpg"), synth)
    
    # Compute metrics
    print("\n  Computing metrics...")
    
    mse = compute_mse(gt, synth)
    rmse = compute_rmse(gt, synth)
    mae = compute_mae(gt, synth)
    psnr = compute_psnr(gt, synth)
    
    print(f"\n  MSE:  {mse:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  MAE:  {mae:.2f}")
    print(f"  PSNR: {psnr:.2f} dB")
    
    # Difference map
    diff_map = create_difference_map(gt, synth)
    cv2.imwrite(str(OUTPUT_DIR / "quality_diff_map.jpg"), diff_map)
    print(f"\n  ✓ Saved: quality_diff_map.jpg")
    
    return mse, rmse, mae, psnr

def demo_ssim():
    """Demo SSIM computation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: SSIM (Structural Similarity)")
    print("="*60)
    
    gt, synth = load_test_images()
    
    # Compute SSIM
    print("\n  Computing SSIM...")
    start = time.time()
    ssim, ssim_map = compute_ssim(gt, synth)
    elapsed = time.time() - start
    
    print(f"\n  SSIM: {ssim:.4f}")
    print(f"  Time: {elapsed:.3f}s")
    
    # Multi-scale SSIM
    print("\n  Computing MS-SSIM...")
    ms_ssim = compute_ms_ssim(gt, synth)
    print(f"  MS-SSIM: {ms_ssim:.4f}")
    
    # Visualize SSIM map
    ssim_vis = create_ssim_map_visualization(ssim_map)
    cv2.imwrite(str(OUTPUT_DIR / "quality_ssim_map.jpg"), ssim_vis)
    print(f"\n  ✓ Saved: quality_ssim_map.jpg")
    
    return ssim, ms_ssim, ssim_map

def demo_perceptual_metrics():
    """Demo perceptual-like metrics."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Perceptual Metrics")
    print("="*60)
    
    gt, synth = load_test_images()
    
    # Edge similarity
    print("\n  Computing edge similarity...")
    edge_sim = compute_edge_similarity(gt, synth)
    print(f"  Edge IoU: {edge_sim:.4f}")
    
    # Histogram similarity
    print("\n  Computing histogram similarity...")
    hist_corr = compute_histogram_similarity(gt, synth, 'correlation')
    hist_bhatt = compute_histogram_similarity(gt, synth, 'bhattacharyya')
    print(f"  Histogram correlation: {hist_corr:.4f}")
    print(f"  Bhattacharyya distance: {hist_bhatt:.4f}")
    
    # Frequency similarity
    print("\n  Computing frequency similarity...")
    freq_sim = compute_frequency_similarity(gt, synth)
    print(f"  Frequency similarity: {freq_sim:.4f}")
    
    return edge_sim, hist_corr, freq_sim

def demo_degradation_levels():
    """Demo metrics dengan berbagai degradation levels."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Degradation Level Comparison")
    print("="*60)
    
    gt, _ = load_test_images()
    
    # Create degraded versions
    degradations = []
    
    # Level 1: Slight noise
    noisy1 = gt.copy().astype(float)
    noisy1 += np.random.normal(0, 5, noisy1.shape)
    noisy1 = np.clip(noisy1, 0, 255).astype(np.uint8)
    degradations.append(("Noise σ=5", noisy1))
    
    # Level 2: More noise
    noisy2 = gt.copy().astype(float)
    noisy2 += np.random.normal(0, 20, noisy2.shape)
    noisy2 = np.clip(noisy2, 0, 255).astype(np.uint8)
    degradations.append(("Noise σ=20", noisy2))
    
    # Level 3: Heavy noise
    noisy3 = gt.copy().astype(float)
    noisy3 += np.random.normal(0, 40, noisy3.shape)
    noisy3 = np.clip(noisy3, 0, 255).astype(np.uint8)
    degradations.append(("Noise σ=40", noisy3))
    
    # Level 4: Blur
    blur = cv2.GaussianBlur(gt, (11, 11), 3)
    degradations.append(("Blur σ=3", blur))
    
    # Level 5: JPEG compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
    _, encoded = cv2.imencode('.jpg', gt, encode_param)
    jpeg = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    degradations.append(("JPEG Q=20", jpeg))
    
    # Compute metrics
    print("\n  Degradation Analysis:")
    print("-" * 60)
    print(f"  {'Degradation':<20} {'PSNR':>10} {'SSIM':>10}")
    print("-" * 60)
    
    results = []
    for name, deg in degradations:
        psnr = compute_psnr(gt, deg)
        ssim, _ = compute_ssim(gt, deg)
        
        results.append({
            'name': name,
            'psnr': psnr,
            'ssim': ssim,
            'image': deg
        })
        
        print(f"  {name:<20} {psnr:>10.2f} {ssim:>10.4f}")
    
    print("-" * 60)
    
    # Save comparison
    images = [gt] + [d['image'] for d in results]
    labels = ["Original"] + [d['name'] for d in results]
    
    # Create grid - ensure consistent sizing
    h, w = gt.shape[:2]
    scale = min(150 / h, 150 / w)
    target_h, target_w = int(h * scale), int(w * scale)
    
    # Resize all images to same size
    resized = []
    for img in images:
        img_resized = cv2.resize(img, (target_w, target_h))
        resized.append(img_resized)
    
    # Add labels
    for i, (img, label) in enumerate(zip(resized, labels)):
        cv2.putText(img, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Create grid with proper padding if needed
    n_images = len(resized)
    n_per_row = 3
    n_rows = (n_images + n_per_row - 1) // n_per_row  # Ceiling division
    
    # Pad with empty images if needed
    while len(resized) % n_per_row != 0 and len(resized) < n_rows * n_per_row:
        resized.append(np.zeros_like(resized[0]))
    
    # Create rows
    rows = []
    for i in range(0, len(resized), n_per_row):
        row_images = resized[i:i + n_per_row]
        if len(row_images) == n_per_row:
            rows.append(np.hstack(row_images))
    
    # Combine rows
    if len(rows) > 0:
        comparison = np.vstack(rows)
        cv2.imwrite(str(OUTPUT_DIR / "quality_degradation_comparison.jpg"), comparison)
        print(f"\n  ✓ Saved: quality_degradation_comparison.jpg")
    
    
    return results

def demo_comprehensive_report():
    """Demo comprehensive quality report."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: Comprehensive Quality Report")
    print("="*60)
    
    gt, synth = load_test_images()
    
    # Compute all metrics
    print("\n  Computing all metrics...")
    
    metrics = {
        'MSE': compute_mse(gt, synth),
        'RMSE': compute_rmse(gt, synth),
        'MAE': compute_mae(gt, synth),
        'PSNR (dB)': compute_psnr(gt, synth),
        'SSIM': compute_ssim(gt, synth)[0],
        'MS-SSIM': compute_ms_ssim(gt, synth),
        'Edge IoU': compute_edge_similarity(gt, synth),
        'Hist Corr': compute_histogram_similarity(gt, synth, 'correlation'),
        'Freq Sim': compute_frequency_similarity(gt, synth),
    }
    
    # Create report
    report = create_metrics_report(metrics, OUTPUT_DIR / "quality_report.jpg")
    print(f"\n  ✓ Saved: quality_report.jpg")
    
    # Error histogram
    hist = create_error_histogram(gt, synth)
    cv2.imwrite(str(OUTPUT_DIR / "quality_error_histogram.jpg"), hist)
    print(f"  ✓ Saved: quality_error_histogram.jpg")
    
    # Combined visualization
    diff_map = create_difference_map(gt, synth)
    ssim_map = create_ssim_map_visualization(compute_ssim(gt, synth)[1])
    
    # Resize semua
    h, w = 240, 320
    gt_r = cv2.resize(gt, (w, h))
    synth_r = cv2.resize(synth, (w, h))
    diff_r = cv2.resize(diff_map, (w, h))
    ssim_r = cv2.resize(ssim_map, (w, h))
    
    row1 = np.hstack([gt_r, synth_r])
    row2 = np.hstack([diff_r, ssim_r])
    combined = np.vstack([row1, row2])
    
    # Labels
    cv2.putText(combined, "Ground Truth", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(combined, "Synthesized", (w + 10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(combined, "Difference", (10, h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(combined, "SSIM Map", (w + 10, h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imwrite(str(OUTPUT_DIR / "quality_combined_visualization.jpg"), combined)
    print(f"  ✓ Saved: quality_combined_visualization.jpg")
    
    return metrics

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.6: QUALITY METRICS FOR VIEW SYNTHESIS")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_basic_metrics()
    
    demo_ssim()
    
    demo_perceptual_metrics()
    
    demo_degradation_levels()
    
    demo_comprehensive_report()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nQuality Metrics:")
    print("  1. Pixel-based: MSE, RMSE, MAE, PSNR")
    print("  2. Structural: SSIM, MS-SSIM")
    print("  3. Perceptual: Edge, Histogram, Frequency")
    
    print("\nInterpretation:")
    print(f"  - PSNR > {PSNR_GOOD} dB → Good quality")
    print(f"  - SSIM > {SSIM_GOOD} → High similarity")
    
    print("\nUse Cases:")
    print("  - Benchmarking view synthesis methods")
    print("  - Quality assessment for IBR")
    print("  - Compression artifact detection")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
