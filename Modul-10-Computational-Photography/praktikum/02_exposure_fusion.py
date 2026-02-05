"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 2: Exposure Fusion (Mertens Method)

Deskripsi:
    Program ini mendemonstrasikan exposure fusion menggunakan
    metode Mertens-Kautz-Van Reeth. Berbeda dengan HDR yang memerlukan
    tone mapping, exposure fusion langsung menghasilkan LDR image.

Teori:
    Exposure fusion menggabungkan multiple exposures berdasarkan
    quality measures tanpa membuat HDR intermediate:
    
    1. Contrast: Laplacian filter untuk local contrast
    2. Saturation: Standar deviasi RGB channels
    3. Well-exposedness: Gaussian centered at 0.5
    
    Weight = Contrast^wC × Saturation^wS × Exposedness^wE
    
    Hasil akhir menggunakan Laplacian pyramid blending.

Keuntungan vs HDR:
    - Tidak perlu calibrate camera response
    - Tidak perlu tone mapping tuning
    - Hasil lebih natural
    - Lebih cepat

Parameter yang dapat dimodifikasi:
    - CONTRAST_WEIGHT: Bobot untuk contrast
    - SATURATION_WEIGHT: Bobot untuk saturation
    - EXPOSURE_WEIGHT: Bobot untuk well-exposedness

Output:
    - Fused image
    - Weight maps visualization

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Weights untuk quality measures (0.0 - 1.0)
CONTRAST_WEIGHT = 1.0
SATURATION_WEIGHT = 1.0
EXPOSURE_WEIGHT = 1.0

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output2")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_exposure_bracket(image_dir, pattern="scene_exp"):
    """
    Load exposure bracket images.
    """
    images = []
    
    for i in range(1, 10):
        filepath = os.path.join(image_dir, f"{pattern}{i}.jpg")
        if os.path.exists(filepath):
            img = cv2.imread(filepath)
            if img is not None:
                images.append(img)
                print(f"  Loaded: {pattern}{i}.jpg")
    
    return images

def compute_contrast(image):
    """
    Hitung contrast weight menggunakan Laplacian.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return np.abs(laplacian)

def compute_saturation(image):
    """
    Hitung saturation weight (std dev dari RGB).
    """
    img_float = image.astype(np.float64) / 255.0
    mean = np.mean(img_float, axis=2)
    sat = np.sqrt(np.mean((img_float - mean[:,:,np.newaxis])**2, axis=2))
    return sat

def compute_exposedness(image, sigma=0.2):
    """
    Hitung well-exposedness weight.
    Pixels mendekati 0.5 dianggap well-exposed.
    """
    img_float = image.astype(np.float64) / 255.0
    exp = np.exp(-0.5 * ((img_float - 0.5) / sigma)**2)
    return np.prod(exp, axis=2)

def compute_weights(images, wC=CONTRAST_WEIGHT, wS=SATURATION_WEIGHT, wE=EXPOSURE_WEIGHT):
    """
    Hitung weight maps untuk setiap exposure.
    """
    weights = []
    
    for img in images:
        C = compute_contrast(img)
        S = compute_saturation(img)
        E = compute_exposedness(img)
        
        # Combine dengan power weights
        W = (C ** wC) * (S ** wS) * (E ** wE) + 1e-12  # Avoid division by zero
        weights.append(W)
    
    # Normalize weights
    total = np.sum(weights, axis=0)
    weights = [w / total for w in weights]
    
    return weights

def gaussian_pyramid(img, levels):
    """
    Build Gaussian pyramid.
    """
    pyramid = [img.astype(np.float64)]
    
    for i in range(levels):
        img = cv2.pyrDown(pyramid[-1])
        pyramid.append(img)
    
    return pyramid

def laplacian_pyramid(img, levels):
    """
    Build Laplacian pyramid.
    """
    gaussian = gaussian_pyramid(img, levels)
    pyramid = []
    
    for i in range(levels):
        h, w = gaussian[i].shape[:2]
        up = cv2.pyrUp(gaussian[i+1], dstsize=(w, h))
        laplacian = gaussian[i] - up
        pyramid.append(laplacian)
    
    # Add the smallest level (residual)
    pyramid.append(gaussian[-1])
    
    return pyramid

def reconstruct_from_laplacian(pyramid):
    """
    Reconstruct image from Laplacian pyramid.
    """
    img = pyramid[-1]
    
    for i in range(len(pyramid) - 2, -1, -1):
        h, w = pyramid[i].shape[:2]
        img = cv2.pyrUp(img, dstsize=(w, h))
        img = img + pyramid[i]
    
    return img

def exposure_fusion_manual(images, weights, levels=5):
    """
    Manual implementation of exposure fusion dengan pyramid blending.
    """
    # Build Laplacian pyramids untuk images
    img_pyramids = [laplacian_pyramid(img, levels) for img in images]
    
    # Build Gaussian pyramids untuk weights
    weight_pyramids = []
    for w in weights:
        w_3ch = np.stack([w, w, w], axis=2)  # Make 3-channel
        weight_pyramids.append(gaussian_pyramid(w_3ch, levels))
    
    # Blend at each level
    blended_pyramid = []
    for level in range(levels + 1):
        blended = np.zeros_like(img_pyramids[0][level])
        for img_pyr, w_pyr in zip(img_pyramids, weight_pyramids):
            blended += w_pyr[level] * img_pyr[level]
        blended_pyramid.append(blended)
    
    # Reconstruct
    result = reconstruct_from_laplacian(blended_pyramid)
    return np.clip(result, 0, 255).astype(np.uint8)

def exposure_fusion_opencv(images):
    """
    OpenCV built-in exposure fusion (Mertens method).
    """
    merge_mertens = cv2.createMergeMertens(
        contrast_weight=CONTRAST_WEIGHT,
        saturation_weight=SATURATION_WEIGHT,
        exposure_weight=EXPOSURE_WEIGHT
    )
    fusion = merge_mertens.process(images)
    return np.clip(fusion * 255, 0, 255).astype(np.uint8)

def visualize_weights(images, weights, output_path):
    """
    Visualisasi weight maps.
    """
    n = len(images)
    fig, axes = plt.subplots(2, n, figsize=(4*n, 8))
    
    for i, (img, w) in enumerate(zip(images, weights)):
        # Original image
        axes[0, i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[0, i].set_title(f"Exposure {i+1}")
        axes[0, i].axis('off')
        
        # Weight map
        axes[1, i].imshow(w, cmap='hot')
        axes[1, i].set_title(f"Weight Map {i+1}")
        axes[1, i].axis('off')
    
    plt.suptitle("Exposure Images dan Weight Maps")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Weight visualization saved to: {output_path}")

def main():
    """
    Fungsi utama untuk exposure fusion demo.
    """
    # Cetak header program
    print("=" * 60)
    # Cetak judul demo
    print("EXPOSURE FUSION (MERTENS METHOD)")
    # Cetak garis pemisah
    print("=" * 60)
    
    # Pastikan folder output tersedia
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Tentukan folder exposure bracket
    hdr_dir = os.path.join(DATA_DIR, "hdr_bracket")
    
    # Informasi proses loading
    print("\nLoading exposure bracket...")
    # Muat gambar exposure
    images = load_exposure_bracket(hdr_dir)
    
    # Validasi jumlah exposure
    if len(images) < 2:
        # Pesan jika data kurang
        print("\nTidak cukup images!")
        # Instruksi download data
        print("Jalankan download_sample_data.py terlebih dahulu.")
        # Hentikan program
        return
    
    # Tampilkan jumlah exposure
    print(f"\nLoaded {len(images)} exposures")
    # Tampilkan ukuran gambar
    print(f"Image size: {images[0].shape}")
    
    # Informasi perhitungan quality measures
    print("\nComputing quality measures...")
    # Tampilkan bobot contrast
    print(f"  Contrast weight: {CONTRAST_WEIGHT}")
    # Tampilkan bobot saturation
    print(f"  Saturation weight: {SATURATION_WEIGHT}")
    # Tampilkan bobot exposure
    print(f"  Exposure weight: {EXPOSURE_WEIGHT}")
    
    # Hitung weight maps
    weights = compute_weights(images)
    
    # Visualisasikan weight maps
    visualize_weights(images, weights, os.path.join(OUTPUT_DIR, "02_weight_maps.png"))
    
    # Informasi metode Mertens
    print("\nFusion dengan OpenCV Mertens...")
    # Fusion dengan OpenCV
    fusion_opencv = exposure_fusion_opencv(images)
    # Simpan hasil Mertens
    cv2.imwrite(os.path.join(OUTPUT_DIR, "02_fusion_mertens.jpg"), fusion_opencv)
    
    # Informasi metode manual
    print("Fusion dengan manual pyramid blending...")
    # Fusion manual pyramid
    fusion_manual = exposure_fusion_manual(images, weights)
    # Simpan hasil manual
    cv2.imwrite(os.path.join(OUTPUT_DIR, "02_fusion_manual.jpg"), fusion_manual)
    
    # Siapkan figure perbandingan
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot exposure asli
    for i, img in enumerate(images[:3]):
        # Konversi BGR ke RGB untuk matplotlib
        axes[0, i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # Judul tiap exposure
        axes[0, i].set_title(f"Exposure {i+1}")
        # Matikan axis
        axes[0, i].axis('off')
    
    # Plot hasil Mertens
    axes[1, 0].imshow(cv2.cvtColor(fusion_opencv, cv2.COLOR_BGR2RGB))
    # Judul hasil Mertens
    axes[1, 0].set_title("OpenCV Mertens")
    # Matikan axis
    axes[1, 0].axis('off')
    
    # Plot hasil manual
    axes[1, 1].imshow(cv2.cvtColor(fusion_manual, cv2.COLOR_BGR2RGB))
    # Judul hasil manual
    axes[1, 1].set_title("Manual Pyramid")
    # Matikan axis
    axes[1, 1].axis('off')
    
    # Hitung perbedaan hasil
    diff = cv2.absdiff(fusion_opencv, fusion_manual)
    # Tampilkan perbedaan (diperkuat)
    axes[1, 2].imshow(diff * 5)  # Amplify for visibility
    # Judul perbedaan
    axes[1, 2].set_title("Difference (5x)")
    # Matikan axis
    axes[1, 2].axis('off')
    
    # Rapikan layout
    plt.tight_layout()
    # Simpan gambar perbandingan
    plt.savefig(os.path.join(OUTPUT_DIR, "02_fusion_comparison.png"), dpi=150)
    # Tutup figure
    plt.close()
    
    # Cetak ringkasan
    print("\n" + "=" * 60)
    # Judul ringkasan
    print("SUMMARY")
    # Garis pemisah ringkasan
    print("=" * 60)
    # Tampilkan daftar output
    print(f"""
Exposure fusion complete!

Files generated:
  - 02_weight_maps.png: Quality measures visualization
  - 02_fusion_mertens.jpg: OpenCV Mertens result
  - 02_fusion_manual.jpg: Manual pyramid blending
  - 02_fusion_comparison.png: Side-by-side comparison

Quality Measures:
  - Contrast: Laplacian-based local contrast
  - Saturation: RGB standard deviation
  - Well-exposedness: Distance from 0.5
""")
    
    # Tampilkan exposure tengah
    cv2.imshow("Original (middle exposure)", images[len(images)//2])
    # Tampilkan hasil fusion
    cv2.imshow("Exposure Fusion", fusion_opencv)
    # Informasi auto-close
    print("\nMenampilkan hasil (akan otomatis tertutup dalam 2 detik)...")
    # Tunggu 2 detik
    cv2.waitKey(2000)
    # Tutup semua window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
