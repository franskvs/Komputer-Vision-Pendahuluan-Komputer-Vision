"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 3: Image Denoising

Deskripsi:
    Program ini membandingkan berbagai metode denoising:
    - Gaussian Blur (baseline)
    - Bilateral Filter (edge-preserving)
    - Non-Local Means (patch-based)
    - Morphological operations

Teori:
    Image denoising bertujuan mengurangi noise sambil
    mempertahankan detail dan edges.
    
    Trade-off utama:
    - Noise reduction vs Detail preservation
    - Speed vs Quality
    
    Non-Local Means (NLM) efektif karena:
    - Menggunakan self-similarity dalam gambar
    - Compare patches, bukan individual pixels
    - Preserve repeated textures

Metrics:
    - PSNR (Peak Signal-to-Noise Ratio): Higher = better
    - SSIM (Structural Similarity): 1.0 = identical

Parameter yang dapat dimodifikasi:
    - GAUSSIAN_KERNEL: Kernel size untuk Gaussian
    - BILATERAL_D: Diameter untuk bilateral
    - NLM_H: Filter strength untuk NLM

Output:
    - Denoised images dengan berbagai metode
    - Quantitative comparison (PSNR, SSIM)

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Gaussian blur
GAUSSIAN_KERNEL = 5

# Bilateral filter
BILATERAL_D = 9
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75

# Non-local means
NLM_H = 10              # Filter strength (higher = more denoising)
NLM_TEMPLATE_SIZE = 7   # Size of patch
NLM_SEARCH_SIZE = 21    # Size of search area

# Noise level untuk synthetic noise
NOISE_SIGMA = 30

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output3")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def add_gaussian_noise(image, sigma=NOISE_SIGMA):
    """
    Tambahkan Gaussian noise ke image.
    """
    noise = np.random.normal(0, sigma, image.shape)
    noisy = image.astype(np.float64) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)

def calculate_psnr(original, processed):
    """
    Hitung PSNR (Peak Signal-to-Noise Ratio).
    """
    mse = np.mean((original.astype(np.float64) - processed.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10(255**2 / mse)

def calculate_ssim(original, processed):
    """
    Hitung SSIM (Structural Similarity Index).
    """
    # Convert to grayscale for SSIM
    if len(original.shape) == 3:
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        processed_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
    else:
        original_gray = original
        processed_gray = processed
    
    return ssim(original_gray, processed_gray)

def denoise_gaussian(image, kernel_size=GAUSSIAN_KERNEL):
    """
    Denoising dengan Gaussian blur.
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def denoise_bilateral(image, d=BILATERAL_D, sigmaColor=BILATERAL_SIGMA_COLOR, 
                      sigmaSpace=BILATERAL_SIGMA_SPACE):
    """
    Denoising dengan bilateral filter (edge-preserving).
    """
    return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

def denoise_nlm(image, h=NLM_H, templateWindowSize=NLM_TEMPLATE_SIZE, 
                searchWindowSize=NLM_SEARCH_SIZE):
    """
    Denoising dengan Non-Local Means.
    """
    if len(image.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(
            image, None, h, h, templateWindowSize, searchWindowSize
        )
    else:
        return cv2.fastNlMeansDenoising(
            image, None, h, templateWindowSize, searchWindowSize
        )

def denoise_morphological(image, kernel_size=3):
    """
    Denoising dengan morphological operations.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    return closed

def main():
    """
    Fungsi utama untuk denoising comparison demo.
    """
    print("=" * 60)
    print("IMAGE DENOISING COMPARISON")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load image
    clean_path = os.path.join(DATA_DIR, "clean_image.jpg")
    
    if not os.path.exists(clean_path):
        # Try alternative
        clean_path = os.path.join(DATA_DIR, "lena.png")
    
    if not os.path.exists(clean_path):
        print("Image tidak ditemukan! Jalankan download_sample_data.py")
        return
    
    print(f"\nLoading image: {clean_path}")
    clean = cv2.imread(clean_path)
    
    if clean is None:
        print("Failed to load image!")
        return
    
    print(f"Image size: {clean.shape}")
    
    # Add noise
    print(f"\nAdding Gaussian noise (sigma={NOISE_SIGMA})...")
    noisy = add_gaussian_noise(clean, NOISE_SIGMA)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_noisy_building.jpg"), noisy)
    
    # Calculate baseline PSNR
    baseline_psnr = calculate_psnr(clean, noisy)
    baseline_ssim = calculate_ssim(clean, noisy)
    print(f"Noisy image - PSNR: {baseline_psnr:.2f} dB, SSIM: {baseline_ssim:.4f}")
    
    # Apply denoising methods
    results = {}
    
    print("\n" + "-" * 40)
    print("Applying denoising methods...")
    
    # 1. Gaussian
    print("\n1. Gaussian Blur...")
    denoised_gaussian = denoise_gaussian(noisy)
    results['Gaussian'] = {
        'image': denoised_gaussian,
        'psnr': calculate_psnr(clean, denoised_gaussian),
        'ssim': calculate_ssim(clean, denoised_gaussian)
    }
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_denoised_gaussian.jpg"), denoised_gaussian)
    print(f"   PSNR: {results['Gaussian']['psnr']:.2f} dB, SSIM: {results['Gaussian']['ssim']:.4f}")
    
    # 2. Bilateral
    print("\n2. Bilateral Filter...")
    denoised_bilateral = denoise_bilateral(noisy)
    results['Bilateral'] = {
        'image': denoised_bilateral,
        'psnr': calculate_psnr(clean, denoised_bilateral),
        'ssim': calculate_ssim(clean, denoised_bilateral)
    }
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_denoised_bilateral.jpg"), denoised_bilateral)
    print(f"   PSNR: {results['Bilateral']['psnr']:.2f} dB, SSIM: {results['Bilateral']['ssim']:.4f}")
    
    # 3. Non-Local Means
    print("\n3. Non-Local Means...")
    denoised_nlm = denoise_nlm(noisy)
    results['NLM'] = {
        'image': denoised_nlm,
        'psnr': calculate_psnr(clean, denoised_nlm),
        'ssim': calculate_ssim(clean, denoised_nlm)
    }
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_denoised_nlm.jpg"), denoised_nlm)
    print(f"   PSNR: {results['NLM']['psnr']:.2f} dB, SSIM: {results['NLM']['ssim']:.4f}")
    
    # 4. Morphological
    print("\n4. Morphological...")
    denoised_morph = denoise_morphological(noisy)
    results['Morphological'] = {
        'image': denoised_morph,
        'psnr': calculate_psnr(clean, denoised_morph),
        'ssim': calculate_ssim(clean, denoised_morph)
    }
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_denoised_morphological.jpg"), denoised_morph)
    print(f"   PSNR: {results['Morphological']['psnr']:.2f} dB, SSIM: {results['Morphological']['ssim']:.4f}")
    
    # Create comparison figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Clean Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(noisy, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"Noisy (PSNR: {baseline_psnr:.1f})")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(results['Gaussian']['image'], cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f"Gaussian (PSNR: {results['Gaussian']['psnr']:.1f})")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(results['Bilateral']['image'], cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"Bilateral (PSNR: {results['Bilateral']['psnr']:.1f})")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(results['NLM']['image'], cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"NLM (PSNR: {results['NLM']['psnr']:.1f})")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(results['Morphological']['image'], cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title(f"Morphological (PSNR: {results['Morphological']['psnr']:.1f})")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "03_denoising_comparison.png"), dpi=150)
    plt.close()
    
    # Bar chart comparison
    methods = ['Noisy'] + list(results.keys())
    psnr_values = [baseline_psnr] + [r['psnr'] for r in results.values()]
    ssim_values = [baseline_ssim] + [r['ssim'] for r in results.values()]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    x = range(len(methods))
    ax1.bar(x, psnr_values, color=['red'] + ['blue']*4)
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods, rotation=45)
    ax1.set_ylabel('PSNR (dB)')
    ax1.set_title('PSNR Comparison')
    ax1.axhline(y=baseline_psnr, color='r', linestyle='--', alpha=0.5)
    
    ax2.bar(x, ssim_values, color=['red'] + ['blue']*4)
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods, rotation=45)
    ax2.set_ylabel('SSIM')
    ax2.set_title('SSIM Comparison')
    ax2.axhline(y=baseline_ssim, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "03_metrics_comparison.png"), dpi=150)
    plt.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"""
Denoising comparison complete!

Results (sorted by PSNR):""")
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['psnr'], reverse=True)
    for name, data in sorted_results:
        psnr_gain = data['psnr'] - baseline_psnr
        print(f"  {name:15s}: PSNR={data['psnr']:.2f} dB (+{psnr_gain:.2f}), SSIM={data['ssim']:.4f}")
    
    print(f"""
Best method: {sorted_results[0][0]}

Files generated:
  - 03_noisy_building.jpg
  - 03_denoised_gaussian.jpg
  - 03_denoised_bilateral.jpg
  - 03_denoised_nlm.jpg
  - 03_denoised_morphological.jpg
  - 03_denoising_comparison.png
  - 03_metrics_comparison.png
""")
    
    # Display
    cv2.imshow("Clean", clean)
    cv2.imshow("Noisy", noisy)
    cv2.imshow(f"Best: {sorted_results[0][0]}", sorted_results[0][1]['image'])
    print("\nMenampilkan hasil (akan otomatis tertutup dalam 2 detik)...")
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
