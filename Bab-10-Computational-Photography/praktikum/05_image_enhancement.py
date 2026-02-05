"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 5: Image Enhancement

Deskripsi:
    Program ini mendemonstrasikan berbagai teknik image enhancement:
    - Contrast enhancement (CLAHE, histogram equalization)
    - Color correction (white balance, saturation)
    - Sharpening
    - Auto-levels

Teori:
    Image enhancement bertujuan meningkatkan visual quality tanpa
    menambah informasi baru:
    
    1. CLAHE (Contrast Limited Adaptive Histogram Equalization):
       - Local contrast enhancement
       - Clip limit untuk menghindari over-amplification
    
    2. White Balance:
       - Correct color cast
       - Gray world assumption atau specific illuminant
    
    3. Unsharp Mask:
       - Sharpen = Original + k * (Original - Blurred)

Parameter yang dapat dimodifikasi:
    - CLAHE_CLIP_LIMIT: Clip limit untuk CLAHE
    - CLAHE_TILE_SIZE: Tile grid size
    - SHARPEN_AMOUNT: Sharpening strength
    - SATURATION_FACTOR: Color saturation multiplier

Output:
    - Enhanced images
    - Before/after comparison

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# CLAHE parameters
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_SIZE = (8, 8)

# Sharpening
SHARPEN_AMOUNT = 1.0
SHARPEN_RADIUS = 1

# Saturation
SATURATION_FACTOR = 1.2

# Gamma correction
GAMMA = 1.0

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output5")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def apply_clahe(image, clip_limit=CLAHE_CLIP_LIMIT, tile_size=CLAHE_TILE_SIZE):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).
    """
    # Convert ke LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    l_clahe = clahe.apply(l)
    
    # Merge back
    lab_clahe = cv2.merge([l_clahe, a, b])
    result = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    
    return result

def histogram_equalization(image):
    """
    Apply histogram equalization.
    """
    # Convert ke YUV
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

def auto_white_balance_gray_world(image):
    """
    White balance dengan Gray World assumption.
    Asumsi: rata-rata scene adalah abu-abu.
    """
    result = image.astype(np.float32)
    
    # Calculate channel means
    avg_b = np.mean(result[:, :, 0])
    avg_g = np.mean(result[:, :, 1])
    avg_r = np.mean(result[:, :, 2])
    
    # Average of all channels
    avg = (avg_b + avg_g + avg_r) / 3
    
    # Scale channels
    result[:, :, 0] = result[:, :, 0] * (avg / avg_b)
    result[:, :, 1] = result[:, :, 1] * (avg / avg_g)
    result[:, :, 2] = result[:, :, 2] * (avg / avg_r)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def auto_white_balance_white_patch(image):
    """
    White balance dengan White Patch assumption.
    Asumsi: piksel paling terang adalah putih.
    """
    result = image.astype(np.float32)
    
    # Find max in each channel
    max_b = np.percentile(result[:, :, 0], 99)
    max_g = np.percentile(result[:, :, 1], 99)
    max_r = np.percentile(result[:, :, 2], 99)
    
    # Scale to make max white (255)
    result[:, :, 0] = result[:, :, 0] * (255 / max_b)
    result[:, :, 1] = result[:, :, 1] * (255 / max_g)
    result[:, :, 2] = result[:, :, 2] * (255 / max_r)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def adjust_saturation(image, factor=SATURATION_FACTOR):
    """
    Adjust color saturation.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = hsv[:, :, 1] * factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def unsharp_mask(image, amount=SHARPEN_AMOUNT, radius=SHARPEN_RADIUS):
    """
    Apply unsharp mask sharpening.
    """
    # Create blurred version
    ksize = radius * 2 + 1
    blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
    
    # Sharpen = Original + amount * (Original - Blurred)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    
    return sharpened

def gamma_correction(image, gamma=GAMMA):
    """
    Apply gamma correction.
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(256)]).astype(np.uint8)
    return cv2.LUT(image, table)

def auto_levels(image):
    """
    Auto-adjust levels (stretch histogram).
    """
    result = image.copy()
    
    for i in range(3):
        channel = result[:, :, i]
        min_val = np.percentile(channel, 1)
        max_val = np.percentile(channel, 99)
        
        if max_val > min_val:
            result[:, :, i] = np.clip(
                (channel - min_val) * 255.0 / (max_val - min_val),
                0, 255
            ).astype(np.uint8)
    
    return result

def enhance_pipeline(image, apply_clahe_flag=True, apply_wb=True, 
                     apply_sharpen=True, apply_saturation=True):
    """
    Complete enhancement pipeline.
    """
    result = image.copy()
    
    if apply_wb:
        result = auto_white_balance_gray_world(result)
    
    if apply_clahe_flag:
        result = apply_clahe(result)
    
    if apply_saturation:
        result = adjust_saturation(result, SATURATION_FACTOR)
    
    if apply_sharpen:
        result = unsharp_mask(result, SHARPEN_AMOUNT)
    
    return result

def plot_histogram(image, title, ax):
    """
    Plot histogram dari image.
    """
    colors = ('b', 'g', 'r')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        ax.plot(hist, color=color)
    ax.set_xlim([0, 256])
    ax.set_title(title)

def main():
    """
    Fungsi utama untuk image enhancement demo.
    """
    print("=" * 60)
    print("IMAGE ENHANCEMENT")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load image
    image_path = os.path.join(DATA_DIR, "building.jpg")
    
    if not os.path.exists(image_path):
        image_path = os.path.join(DATA_DIR, "lena.png")
    
    if not os.path.exists(image_path):
        print("Image tidak ditemukan! Jalankan download_sample_data.py")
        return
    
    print(f"\nLoading image: {image_path}")
    original = cv2.imread(image_path)
    
    if original is None:
        print("Failed to load image!")
        return
    
    print(f"Image size: {original.shape}")
    
    # Apply individual enhancements
    print("\nApplying enhancement techniques...")
    
    results = {}
    
    # 1. CLAHE
    print("  1. CLAHE...")
    results['CLAHE'] = apply_clahe(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_clahe.jpg"), results['CLAHE'])
    
    # 2. Histogram Equalization
    print("  2. Histogram Equalization...")
    results['Hist Eq'] = histogram_equalization(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_histeq.jpg"), results['Hist Eq'])
    
    # 3. White Balance
    print("  3. White Balance (Gray World)...")
    results['WB Gray'] = auto_white_balance_gray_world(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_wb_gray.jpg"), results['WB Gray'])
    
    # 4. White Balance (White Patch)
    print("  4. White Balance (White Patch)...")
    results['WB White'] = auto_white_balance_white_patch(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_wb_white.jpg"), results['WB White'])
    
    # 5. Sharpening
    print("  5. Sharpening...")
    results['Sharpen'] = unsharp_mask(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_sharpen.jpg"), results['Sharpen'])
    
    # 6. Auto Levels
    print("  6. Auto Levels...")
    results['Auto Levels'] = auto_levels(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_autolevels.jpg"), results['Auto Levels'])
    
    # 7. Saturation
    print("  7. Saturation Boost...")
    results['Saturation'] = adjust_saturation(original, 1.5)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_saturation.jpg"), results['Saturation'])
    
    # 8. Complete Pipeline
    print("  8. Complete Pipeline...")
    results['Pipeline'] = enhance_pipeline(original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_enhanced_pipeline.jpg"), results['Pipeline'])
    
    # Create comparison figure
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    for i, (name, img) in enumerate(list(results.items())[:8]):
        row = (i + 1) // 3
        col = (i + 1) % 3
        axes[row, col].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[row, col].set_title(name)
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "05_enhancement_comparison.png"), dpi=150)
    plt.close()
    
    # Histogram comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    plot_histogram(original, "Original Histogram", axes[0, 0])
    plot_histogram(results['CLAHE'], "CLAHE Histogram", axes[0, 1])
    plot_histogram(results['Hist Eq'], "Hist Eq Histogram", axes[1, 0])
    plot_histogram(results['Auto Levels'], "Auto Levels Histogram", axes[1, 1])
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "05_histogram_comparison.png"), dpi=150)
    plt.close()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"""
Image enhancement complete!

Techniques applied:
  - CLAHE: Adaptive contrast enhancement
  - Histogram Equalization: Global contrast
  - White Balance: Color cast correction
  - Sharpening: Detail enhancement
  - Auto Levels: Histogram stretching
  - Saturation: Color boost
  - Pipeline: Combined enhancement

Files generated:
  - 05_enhanced_*.jpg: Individual enhancements
  - 05_enhancement_comparison.png: Visual comparison
  - 05_histogram_comparison.png: Histogram analysis

Parameters used:
  - CLAHE clip limit: {CLAHE_CLIP_LIMIT}
  - Sharpen amount: {SHARPEN_AMOUNT}
  - Saturation factor: {SATURATION_FACTOR}
""")
    
    # Display
    cv2.imshow("Original", original)
    cv2.imshow("Enhanced (Pipeline)", results['Pipeline'])
    print("\nMenampilkan hasil (akan otomatis tertutup dalam 2 detik)...")
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
