# ============================================================
# PROGRAM: 11_pyramids_wavelets.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Multi-resolution dengan Pyramids dan Wavelets
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep multi-resolution representation
#   2. Membuat Gaussian dan Laplacian pyramid
#   3. Aplikasi: image blending, compression
#   4. Memahami dasar wavelets
# 
# Teori:
#   - Gaussian Pyramid: recursive blur + downsample
#   - Laplacian Pyramid: bandpass images (perfect reconstruction)
#   - Application: seamless image blending
# ============================================================

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor modul pywt  # PyWavelets library.
import pywt  # PyWavelets library
# Keterangan: Impor modul os.
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# Pyramid parameters
# Keterangan: Inisialisasi atau perbarui variabel PYRAMID_LEVELS.
PYRAMID_LEVELS = 4         # Jumlah level pyramid
# Keterangan: Inisialisasi atau perbarui variabel BLUR_KERNEL.
BLUR_KERNEL = (5, 5)       # Kernel untuk Gaussian blur sebelum downsample
# Keterangan: Inisialisasi atau perbarui variabel BLUR_SIGMA.
BLUR_SIGMA = 0             # Sigma untuk Gaussian (0 = auto dari kernel size)

# Blending parameters
# Keterangan: Inisialisasi atau perbarui variabel BLEND_MASK_FEATHER.
BLEND_MASK_FEATHER = 50    # Smoothness transition di blend mask

# Wavelet parameters
# Keterangan: Inisialisasi atau perbarui variabel WAVELET_TYPE.
WAVELET_TYPE = 'haar'      # 'haar', 'db4', 'sym4', 'coif1'
# Keterangan: Inisialisasi atau perbarui variabel WAVELET_LEVEL.
WAVELET_LEVEL = 3          # Decomposition level

# ============================================================
# FUNGSI GAUSSIAN PYRAMID
# ============================================================

# Keterangan: Definisikan fungsi build_gaussian_pyramid.
def build_gaussian_pyramid(image, levels=4):
    """
    Membuat Gaussian pyramid
    
    Langkah per level:
    1. Blur dengan Gaussian
    2. Downsample 2× (ambil setiap 2 pixels)
    
    Parameter:
    - image: input image
    - levels: jumlah level pyramid
    
    Return:
    - gaussian_pyramid: list of images
    """
    # Keterangan: Jalankan perintah berikut.
    print(f"🔺 Building Gaussian pyramid dengan {levels} levels...")
    
    # Keterangan: Inisialisasi atau perbarui variabel gaussian_pyramid.
    gaussian_pyramid = [image]
    # Keterangan: Inisialisasi atau perbarui variabel current.
    current = image.copy()
    
    # Keterangan: Mulai loop dengan for i in range(levels - 1).
    for i in range(levels - 1):
        # Blur
        # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
        current = cv2.GaussianBlur(current, BLUR_KERNEL, BLUR_SIGMA)
        
        # Downsample (pyrDown lebih efisien)
        # Keterangan: Downsample gambar untuk membangun pyramid.
        current = cv2.pyrDown(current)
        
        # Keterangan: Jalankan perintah berikut.
        gaussian_pyramid.append(current)
        # Keterangan: Jalankan perintah berikut.
        print(f"   Level {i+1}: {current.shape[1]}×{current.shape[0]} "
              # Keterangan: Jalankan perintah berikut.
              f"({current.size} pixels, {current.size/(image.size)*100:.1f}%)")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gaussian_pyramid


# Keterangan: Definisikan fungsi build_laplacian_pyramid.
def build_laplacian_pyramid(image, levels=4):
    """
    Membuat Laplacian pyramid
    
    Laplacian = Original - Upsampled(Lower_level)
    (Band-pass images dengan perfect reconstruction)
    
    Parameter:
    - image: input image
    - levels: jumlah level
    
    Return:
    - laplacian_pyramid: list of band-pass images
    """
    # Keterangan: Jalankan perintah berikut.
    print(f"🔺 Building Laplacian pyramid dengan {levels} levels...")
    
    # Build Gaussian pyramid dulu
    # Keterangan: Inisialisasi atau perbarui variabel gaussian_pyramid.
    gaussian_pyramid = build_gaussian_pyramid(image, levels)
    # Keterangan: Inisialisasi atau perbarui variabel laplacian_pyramid.
    laplacian_pyramid = []
    
    # Keterangan: Mulai loop dengan for i in range(levels - 1).
    for i in range(levels - 1):
        # Get current level dari Gaussian pyramid
        # Keterangan: Inisialisasi atau perbarui variabel current.
        current = gaussian_pyramid[i]
        
        # Upsample next level (lower resolution)
        # Keterangan: Inisialisasi atau perbarui variabel next_level.
        next_level = gaussian_pyramid[i + 1]
        # Keterangan: Upsample gambar untuk membangun pyramid.
        upsampled = cv2.pyrUp(next_level, dstsize=(current.shape[1], current.shape[0]))
        
        # Laplacian = current - upsampled
        # (Ini adalah band-pass image)
        # Keterangan: Cek kondisi len(current.shape) == 3  # Color.
        if len(current.shape) == 3:  # Color
            # Keterangan: Inisialisasi atau perbarui variabel laplacian.
            laplacian = cv2.subtract(current, upsampled)
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:  # Grayscale
            # Keterangan: Inisialisasi atau perbarui variabel laplacian.
            laplacian = cv2.subtract(current, upsampled)
        
        # Keterangan: Jalankan perintah berikut.
        laplacian_pyramid.append(laplacian)
        
        # Statistics
        # Keterangan: Inisialisasi beberapa variabel (lap_min, lap_max).
        lap_min, lap_max = laplacian.min(), laplacian.max()
        # Keterangan: Jalankan perintah berikut.
        print(f"   Level {i}: range [{lap_min}, {lap_max}]")
    
    # Add the smallest Gaussian as last level
    # Keterangan: Jalankan perintah berikut.
    laplacian_pyramid.append(gaussian_pyramid[-1])
    
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Total pyramid size: {sum([img.size for img in laplacian_pyramid])} elements")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Original size: {image.size} elements")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Overhead: {(sum([img.size for img in laplacian_pyramid])/image.size - 1)*100:.1f}%")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return laplacian_pyramid


# Keterangan: Definisikan fungsi reconstruct_from_laplacian_pyramid.
def reconstruct_from_laplacian_pyramid(laplacian_pyramid):
    """
    Reconstruct gambar dari Laplacian pyramid
    
    Proses: 
    - Start dari level terkecil
    - Upsample dan add dengan next Laplacian level
    
    Parameter:
    - laplacian_pyramid: list of Laplacian images
    
    Return:
    - reconstructed image
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔄 Reconstructing dari Laplacian pyramid...")
    
    # Start dari smallest level (pure Gaussian)
    # Keterangan: Inisialisasi atau perbarui variabel current.
    current = laplacian_pyramid[-1].copy()
    
    # Go bottom-up
    # Keterangan: Mulai loop dengan for i in range(len(laplacian_pyramid) - 2, -1, -1).
    for i in range(len(laplacian_pyramid) - 2, -1, -1):
        # Upsample current
        # Keterangan: Inisialisasi atau perbarui variabel lap_shape.
        lap_shape = laplacian_pyramid[i].shape
        # Keterangan: Upsample gambar untuk membangun pyramid.
        current = cv2.pyrUp(current, dstsize=(lap_shape[1], lap_shape[0]))
        
        # Add Laplacian
        # Keterangan: Inisialisasi atau perbarui variabel current.
        current = cv2.add(current, laplacian_pyramid[i])
        
        # Keterangan: Jalankan perintah berikut.
        print(f"   Level {i}: reconstructed to {current.shape[1]}×{current.shape[0]}")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return current


# ============================================================
# FUNGSI PYRAMID BLENDING
# ============================================================

# Keterangan: Definisikan fungsi pyramid_blend.
def pyramid_blend(image1, image2, mask, levels=4):
    """
    Blend dua gambar menggunakan Laplacian pyramid
    
    Teknik:
    1. Build Laplacian pyramid untuk image1 dan image2
    2. Build Gaussian pyramid untuk mask
    3. Blend tiap level dengan weighted sum
    4. Reconstruct hasil akhir
    
    Parameter:
    - image1: first image
    - image2: second image
    - mask: blend mask (0-255, 0=image2, 255=image1)
    - levels: pyramid levels
    
    Return:
    - blended image
    """
    # Keterangan: Jalankan perintah berikut.
    print(f"🎨 Pyramid blending dengan {levels} levels...")
    
    # Ensure images same size
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image1.shape[:2]
    # Keterangan: Cek kondisi image2.shape[2] != (h, w).
    if image2.shape[:2] != (h, w):
        # Keterangan: Ubah ukuran gambar.
        image2 = cv2.resize(image2, (w, h))
    # Keterangan: Cek kondisi mask.shape[2] != (h, w).
    if mask.shape[:2] != (h, w):
        # Keterangan: Ubah ukuran gambar.
        mask = cv2.resize(mask, (w, h))
    
    # Build Laplacian pyramids
    # Keterangan: Jalankan perintah berikut.
    print("   Building Laplacian pyramids...")
    # Keterangan: Inisialisasi atau perbarui variabel lap1.
    lap1 = build_laplacian_pyramid(image1, levels)
    # Keterangan: Inisialisasi atau perbarui variabel lap2.
    lap2 = build_laplacian_pyramid(image2, levels)
    
    # Build Gaussian pyramid untuk mask
    # Keterangan: Jalankan perintah berikut.
    print("   Building mask pyramid...")
    # Keterangan: Cek kondisi len(mask.shape) == 3.
    if len(mask.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # Keterangan: Inisialisasi atau perbarui variabel mask_pyramid.
    mask_pyramid = build_gaussian_pyramid(mask, levels)
    
    # Blend each level
    # Keterangan: Jalankan perintah berikut.
    print("   Blending each level...")
    # Keterangan: Inisialisasi atau perbarui variabel blended_pyramid.
    blended_pyramid = []
    
    # Keterangan: Mulai loop dengan for i in range(levels).
    for i in range(levels):
        # Normalize mask to [0, 1]
        # Keterangan: Inisialisasi atau perbarui variabel mask_norm.
        mask_norm = mask_pyramid[i].astype(float) / 255.0
        
        # For color images, need 3 channels
        # Keterangan: Cek kondisi len(lap1[i].shape) == 3.
        if len(lap1[i].shape) == 3:
            # Keterangan: Inisialisasi atau perbarui variabel mask_3ch.
            mask_3ch = np.stack([mask_norm] * 3, axis=2)
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Keterangan: Inisialisasi atau perbarui variabel mask_3ch.
            mask_3ch = mask_norm
        
        # Weighted blend
        # Keterangan: Inisialisasi atau perbarui variabel blended.
        blended = (mask_3ch * lap1[i].astype(float) + 
                   # Keterangan: Jalankan perintah berikut.
                   (1 - mask_3ch) * lap2[i].astype(float))
        
        # Keterangan: Cek kondisi len(lap1[i].shape) == 3.
        if len(lap1[i].shape) == 3:
            # Keterangan: Inisialisasi atau perbarui variabel blended.
            blended = blended.astype(np.uint8)
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Keterangan: Inisialisasi atau perbarui variabel blended.
            blended = np.clip(blended, -128, 127).astype(np.int8)
        
        # Keterangan: Jalankan perintah berikut.
        blended_pyramid.append(blended)
    
    # Reconstruct
    # Keterangan: Jalankan perintah berikut.
    print("   Reconstructing blended image...")
    # Convert Laplacian levels back to proper type for reconstruction
    # Keterangan: Inisialisasi atau perbarui variabel lap_for_recon.
    lap_for_recon = []
    # Keterangan: Mulai loop dengan for i in range(len(blended_pyramid) - 1).
    for i in range(len(blended_pyramid) - 1):
        # Keterangan: Cek kondisi blended_pyramid[i].dtype == np.uint8.
        if blended_pyramid[i].dtype == np.uint8:
            # Keterangan: Jalankan perintah berikut.
            lap_for_recon.append(blended_pyramid[i])
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Convert back from signed
            # Keterangan: Jalankan perintah berikut.
            lap_for_recon.append(blended_pyramid[i].astype(np.int16))
    # Keterangan: Jalankan perintah berikut.
    lap_for_recon.append(blended_pyramid[-1])  # Gaussian base
    
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = reconstruct_from_laplacian_pyramid(lap_for_recon)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# ============================================================
# FUNGSI WAVELETS
# ============================================================

# Keterangan: Definisikan fungsi wavelet_decomposition.
def wavelet_decomposition(image, wavelet='haar', level=3):
    """
    Wavelet decomposition menggunakan PyWavelets
    
    Parameter:
    - image: grayscale image
    - wavelet: wavelet type ('haar', 'db4', 'sym4', etc)
    - level: decomposition level
    
    Return:
    - coefficients: wavelet coefficients
    """
    # Keterangan: Inisialisasi beberapa variabel (print(f"🌊 Wavelet decomposition ({wavelet}, level).
    print(f"🌊 Wavelet decomposition ({wavelet}, level={level})...")
    
    # Ensure grayscale
    # Keterangan: Cek kondisi len(image.shape) == 3.
    if len(image.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Wavelet decomposition
    # Keterangan: Inisialisasi atau perbarui variabel coeffs.
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    
    # Structure: [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]
    # cA = approximation (low-pass)
    # cH, cV, cD = horizontal, vertical, diagonal details (high-pass)
    
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Decomposition complete")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Approximation size: {coeffs[0].shape}")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Number of detail levels: {len(coeffs) - 1}")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return coeffs


# Keterangan: Definisikan fungsi wavelet_reconstruction.
def wavelet_reconstruction(coeffs, wavelet='haar'):
    """
    Reconstruct image dari wavelet coefficients
    
    Parameter:
    - coeffs: wavelet coefficients
    - wavelet: wavelet type
    
    Return:
    - reconstructed image
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔄 Wavelet reconstruction...")
    
    # Inverse wavelet transform
    # Keterangan: Inisialisasi atau perbarui variabel image_rec.
    image_rec = pywt.waverec2(coeffs, wavelet)
    
    # Clip and convert
    # Keterangan: Inisialisasi atau perbarui variabel image_rec.
    image_rec = np.clip(image_rec, 0, 255).astype(np.uint8)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return image_rec


# Keterangan: Definisikan fungsi visualize_wavelet_coeffs.
def visualize_wavelet_coeffs(coeffs, title="Wavelet Decomposition"):
    """
    Visualize wavelet coefficients
    
    Parameter:
    - coeffs: wavelet coefficients dari wavedec2
    - title: plot title
    """
    # Extract approximation dan details
    # Keterangan: Inisialisasi atau perbarui variabel cA.
    cA = coeffs[0]  # Approximation
    # Keterangan: Inisialisasi atau perbarui variabel details.
    details = coeffs[1:]  # Detail tuples (cH, cV, cD)
    
    # Create figure
    # Keterangan: Inisialisasi atau perbarui variabel n_levels.
    n_levels = len(details)
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(n_levels + 1, 4, figsize=(15, 3 * (n_levels + 1)))
    
    # Approximation (level 0)
    # Keterangan: Cek kondisi n_levels > 0.
    if n_levels > 0:
        # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(cA, cmap).
        axes[0, 0].imshow(cA, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[0, 0].set_title(f"Approximation (Level {n_levels})\nSize: {cA.shape}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, 0].axis('off')
        # Keterangan: Mulai loop dengan for j in range(1, 4).
        for j in range(1, 4):
            # Keterangan: Jalankan perintah berikut.
            axes[0, j].axis('off')
    
    # Details untuk tiap level
    # Keterangan: Mulai loop dengan for i, (cH, cV, cD) in enumerate(details).
    for i, (cH, cV, cD) in enumerate(details):
        # Keterangan: Inisialisasi atau perbarui variabel level.
        level = n_levels - i
        
        # Keterangan: Inisialisasi beberapa variabel (axes[i + 1, 0].imshow(cH, cmap).
        axes[i + 1, 0].imshow(cH, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 0].set_title(f"Horizontal Details (Level {level})")
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 0].axis('off')
        
        # Keterangan: Inisialisasi beberapa variabel (axes[i + 1, 1].imshow(cV, cmap).
        axes[i + 1, 1].imshow(cV, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 1].set_title(f"Vertical Details (Level {level})")
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 1].axis('off')
        
        # Keterangan: Inisialisasi beberapa variabel (axes[i + 1, 2].imshow(cD, cmap).
        axes[i + 1, 2].imshow(cD, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 2].set_title(f"Diagonal Details (Level {level})")
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 2].axis('off')
        
        # Magnitude untuk comparison
        # Keterangan: Inisialisasi atau perbarui variabel magnitude.
        magnitude = np.sqrt(cH**2 + cV**2 + cD**2)
        # Keterangan: Inisialisasi beberapa variabel (axes[i + 1, 3].imshow(magnitude, cmap).
        axes[i + 1, 3].imshow(magnitude, cmap='hot')
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 3].set_title(f"Combined Magnitude (Level {level})")
        # Keterangan: Jalankan perintah berikut.
        axes[i + 1, 3].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle(title, fontsize).
    plt.suptitle(title, fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_gaussian_pyramid.
def demo_gaussian_pyramid():
    """
    Demo 1: Gaussian Pyramid construction
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 1: GAUSSIAN PYRAMID")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Add colorful patterns
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (100, 100), (400, 400), (255, 100, 100), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (256, 256), 120, (100, 255, 100), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (200, 200), (300, 300), (100, 100, 255), -1)
    
    # Add fine details
    # Keterangan: Mulai loop dengan for i in range(0, 512, 32).
    for i in range(0, 512, 32):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (i, 0), (i, 512), (255, 255, 255), 1)
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (0, i), (512, i), (255, 255, 255), 1)
    
    # Build pyramid
    # Keterangan: Inisialisasi atau perbarui variabel pyramid.
    pyramid = build_gaussian_pyramid(image, PYRAMID_LEVELS)
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(1, len(pyramid), figsize=(15, 4))
    
    # Keterangan: Mulai loop dengan for i, level_img in enumerate(pyramid).
    for i, level_img in enumerate(pyramid):
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(level_img, cv2.COLOR_BGR2RGB))
        # Keterangan: Jalankan perintah berikut.
        axes[i].set_title(f"Level {i}\n{level_img.shape[1]}×{level_img.shape[0]}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Gaussian Pyramid (Octave Pyramid)", fontsize).
    plt.suptitle("Gaussian Pyramid (Octave Pyramid)", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Analisis:")
    # Keterangan: Inisialisasi atau perbarui variabel total_pixels.
    total_pixels = sum([img.size for img in pyramid])
    # Keterangan: Jalankan perintah berikut.
    print(f"   Original: {image.size:,} pixels")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Pyramid total: {total_pixels:,} pixels")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Overhead: {(total_pixels/image.size - 1)*100:.1f}%")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Theory: ~33% overhead (1 + 1/4 + 1/16 + ...)")


# Keterangan: Definisikan fungsi demo_laplacian_pyramid.
def demo_laplacian_pyramid():
    """
    Demo 2: Laplacian Pyramid dan reconstruction
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 2: LAPLACIAN PYRAMID")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((256, 256), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (50, 50), (200, 200), 200, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (128, 128), 50, 255, -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "PENS", (85, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, 100, 2)
    
    # Build Laplacian pyramid
    # Keterangan: Inisialisasi atau perbarui variabel lap_pyramid.
    lap_pyramid = build_laplacian_pyramid(image, 4)
    
    # Reconstruct
    # Keterangan: Inisialisasi atau perbarui variabel reconstructed.
    reconstructed = reconstruct_from_laplacian_pyramid(lap_pyramid)
    
    # Verify perfect reconstruction
    # Keterangan: Inisialisasi atau perbarui variabel diff.
    diff = cv2.absdiff(image, reconstructed)
    # Keterangan: Inisialisasi atau perbarui variabel reconstruction_error.
    reconstruction_error = np.max(diff)
    
    # Keterangan: Jalankan perintah berikut.
    print(f"\n✓ Reconstruction error: {reconstruction_error} (should be 0 or very small)")
    
    # Display Laplacian pyramid
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Keterangan: Mulai loop dengan for i in range(4).
    for i in range(4):
        # Laplacian (band-pass) - need to scale untuk visualization
        # Keterangan: Inisialisasi atau perbarui variabel lap_display.
        lap_display = lap_pyramid[i].copy()
        
        # Keterangan: Cek kondisi i < 3  # Detail levels (signed values).
        if i < 3:  # Detail levels (signed values)
            # Shift ke positive range untuk display
            # Keterangan: Inisialisasi atau perbarui variabel lap_display.
            lap_display = cv2.normalize(lap_display, None, 0, 255, cv2.NORM_MINMAX)
        
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].imshow(lap_display, cmap).
        axes[0, i].imshow(lap_display, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].set_title(f"Laplacian Level {i}\n{lap_pyramid[i].shape}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
    
    # Row 2: Partial reconstructions
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(image, cmap).
    axes[1, 0].imshow(image, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(reconstructed, cmap).
    axes[1, 1].imshow(reconstructed, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Reconstructed\n(Perfect!)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(diff * 50, cmap).
    axes[1, 2].imshow(diff * 50, cmap='hot')  # Amplify untuk visibility
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title(f"Difference ×50\nMax error: {reconstruction_error}")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Show frequency content
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 3].text(0.1, 0.8, "Laplacian Pyramid:", fontsize).
    axes[1, 3].text(0.1, 0.8, "Laplacian Pyramid:", fontsize=12, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 3].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 3].text(0.1, 0.6, "✓ Perfect reconstruction", fontsize).
    axes[1, 3].text(0.1, 0.6, "✓ Perfect reconstruction", fontsize=10,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 3].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 3].text(0.1, 0.5, "✓ Each level).
    axes[1, 3].text(0.1, 0.5, "✓ Each level = band-pass", fontsize=10,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 3].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 3].text(0.1, 0.4, "✓ Compression ready", fontsize).
    axes[1, 3].text(0.1, 0.4, "✓ Compression ready", fontsize=10,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 3].transAxes)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 3].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Laplacian Pyramid with Perfect Reconstruction", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_pyramid_blending.
def demo_pyramid_blending():
    """
    Demo 3: Seamless image blending dengan pyramid
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 3: PYRAMID BLENDING (SEAMLESS)")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create apple (red)
    # Keterangan: Inisialisasi array bernilai nol.
    apple = np.zeros((400, 400, 3), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(apple, (200, 200), 150, (0, 0, 200), -1)  # Red circle
    # Add texture
    # Keterangan: Mulai loop dengan for i in range(0, 400, 20).
    for i in range(0, 400, 20):
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(apple, (np.random.randint(50, 350), np.random.randint(50, 350)), 
                   # Keterangan: Jalankan perintah berikut.
                   5, (0, 0, np.random.randint(180, 220)), -1)
    
    # Create orange (orange)
    # Keterangan: Inisialisasi array bernilai nol.
    orange = np.zeros((400, 400, 3), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(orange, (200, 200), 150, (0, 165, 255), -1)  # Orange circle
    # Add texture
    # Keterangan: Mulai loop dengan for i in range(0, 400, 20).
    for i in range(0, 400, 20):
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(orange, (np.random.randint(50, 350), np.random.randint(50, 350)),
                   # Keterangan: Jalankan perintah berikut.
                   5, (0, np.random.randint(140, 180), np.random.randint(230, 255)), -1)
    
    # Create mask: vertical split dengan smooth transition
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros((400, 400), dtype=np.uint8)
    # Keterangan: Mulai loop dengan for j in range(400).
    for j in range(400):
        # Linear gradient di tengah dengan feathering
        # Keterangan: Cek kondisi j < 200 - BLEND_MASK_FEATHER.
        if j < 200 - BLEND_MASK_FEATHER:
            # Keterangan: Inisialisasi beberapa variabel (mask[:, j]).
            mask[:, j] = 255
        # Keterangan: Cek kondisi alternatif j > 200 + BLEND_MASK_FEATHER.
        elif j > 200 + BLEND_MASK_FEATHER:
            # Keterangan: Inisialisasi beberapa variabel (mask[:, j]).
            mask[:, j] = 0
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Linear transition
            # Keterangan: Inisialisasi atau perbarui variabel alpha.
            alpha = (200 + BLEND_MASK_FEATHER - j) / (2 * BLEND_MASK_FEATHER)
            # Keterangan: Inisialisasi beberapa variabel (mask[:, j]).
            mask[:, j] = int(alpha * 255)
    
    # Method 1: Direct blend (ghosting)
    # Keterangan: Inisialisasi atau perbarui variabel mask_norm.
    mask_norm = mask.astype(float) / 255.0
    # Keterangan: Inisialisasi atau perbarui variabel mask_3ch.
    mask_3ch = np.stack([mask_norm] * 3, axis=2)
    # Keterangan: Inisialisasi atau perbarui variabel direct_blend.
    direct_blend = (mask_3ch * apple.astype(float) + 
                    # Keterangan: Jalankan perintah berikut.
                    (1 - mask_3ch) * orange.astype(float)).astype(np.uint8)
    
    # Method 2: Pyramid blend (seamless)
    # Keterangan: Inisialisasi atau perbarui variabel pyramid_result.
    pyramid_result = pyramid_blend(apple, orange, mask, 5)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 1)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(apple, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Apple (Red)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 2)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(orange, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Orange")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(mask, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title(f"Blend Mask\n(feather={BLEND_MASK_FEATHER})")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 4)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(direct_blend, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Direct Blend\n(visible color seam)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 5)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(pyramid_result, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Pyramid Blend\n(seamless!)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Zoom on seam
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 6)
    # Keterangan: Inisialisasi atau perbarui variabel zoom_region.
    zoom_region = pyramid_result[150:250, 150:250]
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(zoom_region, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Zoomed: Blend Seam\n(smooth transition)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Pyramid Blending: The Famous Apple-Orange Example", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🏆 Mengapa Pyramid Blending Seamless?")
    # Keterangan: Jalankan perintah berikut.
    print("   1. Low frequencies: blended smoothly (wide transition)")
    # Keterangan: Jalankan perintah berikut.
    print("   2. High frequencies: blended quickly (sharp textures)")
    # Keterangan: Jalankan perintah berikut.
    print("   3. No ghosting, no visible seam")
    # Keterangan: Jalankan perintah berikut.
    print("   4. Applications: panorama stitching, compositing")


# Keterangan: Definisikan fungsi demo_wavelet_basics.
def demo_wavelet_basics():
    """
    Demo 4: Basic wavelet decomposition
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 4: WAVELET DECOMPOSITION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((256, 256), dtype=np.uint8)
    
    # Add patterns
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (50, 50), (200, 200), 200, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (128, 128), 40, 255, -1)
    
    # Add horizontal and vertical edges
    # Keterangan: Jalankan perintah berikut.
    cv2.line(image, (30, 128), (220, 128), 150, 3)
    # Keterangan: Jalankan perintah berikut.
    cv2.line(image, (128, 30), (128, 220), 150, 3)
    
    # Wavelet decomposition
    # Keterangan: Inisialisasi atau perbarui variabel coeffs.
    coeffs = wavelet_decomposition(image, WAVELET_TYPE, WAVELET_LEVEL)
    
    # Visualize
    # Keterangan: Jalankan perintah berikut.
    visualize_wavelet_coeffs(coeffs, f"Wavelet Decomposition ({WAVELET_TYPE})")
    
    # Reconstruct
    # Keterangan: Inisialisasi atau perbarui variabel reconstructed.
    reconstructed = wavelet_reconstruction(coeffs, WAVELET_TYPE)
    
    # Verify
    # Keterangan: Inisialisasi atau perbarui variabel diff.
    diff = cv2.absdiff(image, reconstructed)
    # Keterangan: Inisialisasi atau perbarui variabel max_error.
    max_error = np.max(diff)
    
    # Keterangan: Jalankan perintah berikut.
    print(f"\n✓ Reconstruction error: {max_error}")
    
    # Display reconstruction
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(12, 4))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Original")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(reconstructed, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Reconstructed")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(diff * 10, cmap='hot')
    # Keterangan: Set judul subplot.
    plt.title(f"Difference ×10\nMax: {max_error}")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Wavelet Perfect Reconstruction", fontsize).
    plt.suptitle("Wavelet Perfect Reconstruction", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Interpretasi Wavelet Coefficients:")
    # Keterangan: Jalankan perintah berikut.
    print("   🔵 Approximation (cA): low-frequency content")
    # Keterangan: Jalankan perintah berikut.
    print("   ➡️  Horizontal details (cH): vertical edges")
    # Keterangan: Jalankan perintah berikut.
    print("   ⬇️  Vertical details (cV): horizontal edges")
    # Keterangan: Jalankan perintah berikut.
    print("   ↘️  Diagonal details (cD): diagonal edges/corners")


# Keterangan: Definisikan fungsi demo_wavelet_denoising.
def demo_wavelet_denoising():
    """
    Demo 5: Image denoising menggunakan wavelet
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 5: WAVELET DENOISING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create clean image
    # Keterangan: Inisialisasi array bernilai nol.
    image_clean = np.zeros((256, 256), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image_clean, (50, 50), (200, 200), 200, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image_clean, (128, 128), 50, 255, -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image_clean, "CV", (95, 145), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 100, 3)
    
    # Add noise
    # Keterangan: Inisialisasi atau perbarui variabel noise.
    noise = np.random.normal(0, 25, image_clean.shape)
    # Keterangan: Inisialisasi atau perbarui variabel image_noisy.
    image_noisy = np.clip(image_clean.astype(float) + noise, 0, 255).astype(np.uint8)
    
    # Wavelet decomposition
    # Keterangan: Inisialisasi atau perbarui variabel coeffs.
    coeffs = wavelet_decomposition(image_noisy, 'db4', 3)
    
    # Denoising: threshold small wavelet coefficients (coring)
    # Strategy: small coefficients = noise, large = signal
    # Keterangan: Inisialisasi atau perbarui variabel threshold.
    threshold = 30  # Threshold value
    
    # Keterangan: Inisialisasi atau perbarui variabel coeffs_denoised.
    coeffs_denoised = [coeffs[0]]  # Keep approximation as-is
    
    # Keterangan: Mulai loop dengan for detail_coeffs in coeffs[1].
    for detail_coeffs in coeffs[1:]:
        # Each detail_coeffs is tuple (cH, cV, cD)
        # Keterangan: Inisialisasi beberapa variabel (cH, cV, cD).
        cH, cV, cD = detail_coeffs
        
        # Soft thresholding
        # Keterangan: Inisialisasi atau perbarui variabel cH_thresh.
        cH_thresh = pywt.threshold(cH, threshold, mode='soft')
        # Keterangan: Inisialisasi atau perbarui variabel cV_thresh.
        cV_thresh = pywt.threshold(cV, threshold, mode='soft')
        # Keterangan: Inisialisasi atau perbarui variabel cD_thresh.
        cD_thresh = pywt.threshold(cD, threshold, mode='soft')
        
        # Keterangan: Jalankan perintah berikut.
        coeffs_denoised.append((cH_thresh, cV_thresh, cD_thresh))
    
    # Reconstruct
    # Keterangan: Inisialisasi atau perbarui variabel image_denoised.
    image_denoised = wavelet_reconstruction(coeffs_denoised, 'db4')
    
    # Calculate PSNR
    # Keterangan: Inisialisasi atau perbarui variabel mse_noisy.
    mse_noisy = np.mean((image_clean.astype(float) - image_noisy.astype(float))**2)
    # Keterangan: Inisialisasi atau perbarui variabel mse_denoised.
    mse_denoised = np.mean((image_clean.astype(float) - image_denoised.astype(float))**2)
    
    # Keterangan: Inisialisasi atau perbarui variabel psnr_noisy.
    psnr_noisy = 10 * np.log10(255**2 / mse_noisy) if mse_noisy > 0 else float('inf')
    # Keterangan: Inisialisasi atau perbarui variabel psnr_denoised.
    psnr_denoised = 10 * np.log10(255**2 / mse_denoised) if mse_denoised > 0 else float('inf')
    
    # Keterangan: Jalankan perintah berikut.
    print(f"\n📊 Quality Metrics:")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Noisy PSNR: {psnr_noisy:.2f} dB")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Denoised PSNR: {psnr_denoised:.2f} dB")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Improvement: {psnr_denoised - psnr_noisy:.2f} dB")
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 5))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image_clean, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Original (Clean)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image_noisy, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title(f"Noisy\nPSNR: {psnr_noisy:.1f} dB")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image_denoised, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title(f"Wavelet Denoised\nPSNR: {psnr_denoised:.1f} dB")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 4)
    # Show coefficients before/after thresholding
    # Keterangan: Inisialisasi atau perbarui variabel cH_before.
    cH_before = coeffs[1][0]  # Level 1 horizontal
    # Keterangan: Inisialisasi atau perbarui variabel cH_after.
    cH_after = coeffs_denoised[1][0]
    
    # Keterangan: Inisialisasi beberapa variabel (plt.hist(cH_before.ravel(), bins).
    plt.hist(cH_before.ravel(), bins=50, alpha=0.5, label='Before', range=(-100, 100))
    # Keterangan: Inisialisasi beberapa variabel (plt.hist(cH_after.ravel(), bins).
    plt.hist(cH_after.ravel(), bins=50, alpha=0.5, label='After', range=(-100, 100))
    # Keterangan: Inisialisasi atau perbarui variabel plt.axvline(x.
    plt.axvline(x=-threshold, color='r', linestyle='--', label='Threshold')
    # Keterangan: Inisialisasi atau perbarui variabel plt.axvline(x.
    plt.axvline(x=threshold, color='r', linestyle='--')
    # Keterangan: Set judul subplot.
    plt.title("Wavelet Coefficients Distribution\n(Level 1 Horizontal)")
    # Keterangan: Jalankan perintah berikut.
    plt.legend()
    # Keterangan: Inisialisasi beberapa variabel (plt.grid(True, alpha).
    plt.grid(True, alpha=0.3)
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Wavelet Denoising via Coefficient Thresholding", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n💡 Wavelet Denoising Principle:")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 1. Noise.
    print("   1. Noise = spread across all frequencies (small coeffs)")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 2. Signal.
    print("   2. Signal = concentrated in large coeffs")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 3. Thresholding removes small coeffs.
    print("   3. Thresholding removes small coeffs = removes noise")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 4. Keep large coeffs.
    print("   4. Keep large coeffs = preserve edges & details")


# Keterangan: Definisikan fungsi demo_multi_resolution_application.
def demo_multi_resolution_application():
    """
    Demo 6: Aplikasi multi-resolution - Coarse-to-fine search
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 6: MULTI-RESOLUTION APPLICATION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create scene
    # Keterangan: Inisialisasi atau perbarui variabel scene.
    scene = np.random.randint(80, 120, (512, 512), dtype=np.uint8)
    
    # Add objects di various locations
    # Keterangan: Inisialisasi atau perbarui variabel objects.
    objects = [
        # Keterangan: Jalankan perintah berikut.
        ((100, 100), 40),
        # Keterangan: Jalankan perintah berikut.
        ((300, 150), 35),
        # Keterangan: Jalankan perintah berikut.
        ((400, 400), 45),
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Mulai loop dengan for (cx, cy), radius in objects.
    for (cx, cy), radius in objects:
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(scene, (cx, cy), radius, 255, -1)
    
    # Create template (small object to find)
    # Keterangan: Inisialisasi array bernilai nol.
    template = np.zeros((90, 90), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(template, (45, 45), 40, 255, -1)
    
    # Build pyramid untuk scene
    # Keterangan: Inisialisasi atau perbarui variabel scene_pyramid.
    scene_pyramid = build_gaussian_pyramid(scene, 4)
    # Keterangan: Inisialisasi atau perbarui variabel template_pyramid.
    template_pyramid = build_gaussian_pyramid(template, 4)
    
    # Search coarse to fine
    # Keterangan: Jalankan perintah berikut.
    print("\n🔍 Coarse-to-fine search simulation...")
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Keterangan: Mulai loop dengan for i in range(4).
    for i in range(4):
        # Scene pyramid
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].imshow(scene_pyramid[i], cmap).
        axes[0, i].imshow(scene_pyramid[i], cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].set_title(f"Scene Level {i}\n{scene_pyramid[i].shape}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
        
        # Template pyramid
        # Keterangan: Cek kondisi i < len(template_pyramid).
        if i < len(template_pyramid):
            # Keterangan: Inisialisasi beberapa variabel (axes[1, i].imshow(template_pyramid[i], cmap).
            axes[1, i].imshow(template_pyramid[i], cmap='gray')
            # Keterangan: Jalankan perintah berikut.
            axes[1, i].set_title(f"Template Level {i}\n{template_pyramid[i].shape}")
            # Keterangan: Jalankan perintah berikut.
            axes[1, i].axis('off')
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Keterangan: Jalankan perintah berikut.
            axes[1, i].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Multi-Resolution Pyramid for Fast Search", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🏆 Aplikasi Multi-Resolution:")
    # Keterangan: Jalankan perintah berikut.
    print("   🔍 Face detection (search at multiple scales)")
    # Keterangan: Jalankan perintah berikut.
    print("   🎯 Template matching (coarse-to-fine speedup)")
    # Keterangan: Jalankan perintah berikut.
    print("   📷 Image stitching (multi-scale alignment)")
    # Keterangan: Jalankan perintah berikut.
    print("   🎬 Motion estimation (hierarchical search)")
    # Keterangan: Jalankan perintah berikut.
    print("   🎨 Image editing (detail-preserving operations)")


# ============================================================
# MAIN PROGRAM
# ============================================================

# Keterangan: Definisikan fungsi main.
def main():
    """Program utama"""
    print("\n" + "="*60)
    print("      PRAKTIKUM COMPUTER VISION - BAB 3")
    print("      PYRAMIDS DAN WAVELETS")
    print("="*60)
    
    print("\n📚 Konsep yang akan dipelajari:")
    print("   1. Gaussian pyramid: multi-scale representation")
    print("   2. Laplacian pyramid: band-pass + perfect reconstruction")
    print("   3. Pyramid blending: seamless image compositing")
    print("   4. Wavelets: oriented multi-scale decomposition")
    print("   5. Applications: blending, compression, denoising")
    
    print("\n🎯 Perbedaan Pyramid vs Wavelet:")
    print("   Pyramid:")
    print("   - Overcomplete (~33% overhead)")
    print("   - Fast computation")
    print("   - Used: blending, search, display")
    print("   Wavelet:")
    print("   - Tight frame (same size as original)")
    print("   - Orientation selective")
    print("   - Used: compression, denoising, analysis")
    
    try:
        # Demo 1: Gaussian pyramid
        demo_gaussian_pyramid()
        
        # Demo 2: Laplacian pyramid
        demo_laplacian_pyramid()
        
        # Demo 3: Pyramid blending
        demo_pyramid_blending()
        
        # Demo 4: Wavelet basics
        demo_wavelet_basics()
        
        # Demo 5: Wavelet denoising
        demo_wavelet_denoising()
        
        # Demo 6: Multi-resolution application
        demo_multi_resolution_application()
        
        print("\n" + "="*60)
        print("✅ SEMUA DEMO SELESAI")
        print("="*60)
        
        print("\n💡 Key Takeaways:")
        print("   1. Pyramids = hierarchical multi-scale representation")
        print("   2. Gaussian pyramid untuk search, analysis")
        print("   3. Laplacian pyramid untuk blending, editing")
        print("   4. Wavelets untuk compression, denoising")
        print("   5. Multi-resolution critical untuk many CV tasks")
        
        print("\n🔬 Eksperimen Lanjutan:")
        print("   - Ubah PYRAMID_LEVELS untuk see tradeoff")
        print("   - Coba berbagai WAVELET_TYPE ('haar', 'db4', 'sym4')")
        print("   - Eksperimen BLEND_MASK_FEATHER untuk seam quality")
        print("   - Implement image stitching dengan pyramid blending")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
