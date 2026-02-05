"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 3: Perbandingan Teknik Blending

Deskripsi:
    Program ini membandingkan berbagai teknik blending untuk image stitching:
    1. No Blending - langsung overlay tanpa transisi
    2. Alpha Blending - weighted average dengan alpha tetap
    3. Feather Blending - alpha gradient di area overlap
    4. Laplacian Pyramid Blending - multi-scale blending

Teori Blending:
    Blending diperlukan untuk menghilangkan "seam" atau garis batas yang
    terlihat di area overlap antara dua gambar. Tanpa blending, perbedaan
    exposure, white balance, atau alignment akan terlihat jelas.

    1. No Blending: output = img1 OR img2
    2. Alpha Blending: output = α*img1 + (1-α)*img2
    3. Feather Blending: α berubah gradual di area overlap
    4. Pyramid Blending: blend di berbagai level frekuensi

Parameter yang dapat dimodifikasi:
    - BLEND_WIDTH: Lebar area blending (dalam pixel)
    - ALPHA_VALUE: Nilai alpha untuk fixed alpha blending
    - PYRAMID_LEVELS: Jumlah level untuk pyramid blending

Output:
    - Perbandingan visual semua teknik blending
    - Zoom pada area seam untuk analisis detail

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Lebar area blending (pixel)
# Semakin besar = transisi lebih gradual
# Typical range: 20-100
BLEND_WIDTH = 50

# Alpha value untuk fixed alpha blending (0.0-1.0)
# 0.5 = equal weight untuk kedua gambar
ALPHA_VALUE = 0.5

# Jumlah level untuk pyramid blending
# Semakin banyak = blending lebih halus tapi lebih lambat
# Typical range: 4-8
PYRAMID_LEVELS = 6

# Path ke gambar
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output3")

# ============================================================
# FUNGSI-FUNGSI BLENDING
# ============================================================

def create_overlap_scenario(img1, img2, overlap_ratio=0.3):
    """
    Buat skenario overlap simulasi dari dua gambar.
    Berguna untuk demonstrasi ketika tidak ada gambar panorama asli.
    
    Parameters:
        img1, img2: Dua gambar input
        overlap_ratio: Rasio area overlap
    
    Returns:
        left_part, right_part: Bagian kiri dan kanan untuk digabung
        overlap_width: Lebar area overlap
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Seragamkan tinggi
    target_h = min(h1, h2)
    if h1 != target_h:
        img1 = cv2.resize(img1, (int(w1 * target_h / h1), target_h))
    if h2 != target_h:
        img2 = cv2.resize(img2, (int(w2 * target_h / h2), target_h))
    
    h, w1 = img1.shape[:2]
    _, w2 = img2.shape[:2]
    
    # Hitung overlap
    overlap_width = int(min(w1, w2) * overlap_ratio)
    
    # Potong bagian yang akan overlap
    left_part = img1[:, :w1]
    right_part = img2[:, :w2]
    
    return left_part, right_part, overlap_width

def no_blending(img1, img2, overlap_width):
    """
    Gabungkan tanpa blending - langsung overlay.
    
    Seam akan sangat terlihat di batas kedua gambar.
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Seragamkan tinggi
    h = min(h1, h2)
    if h1 != h:
        img1 = cv2.resize(img1, (w1, h))
    if h2 != h:
        img2 = cv2.resize(img2, (w2, h))
    
    # Lebar total = w1 + w2 - overlap
    total_width = w1 + w2 - overlap_width
    result = np.zeros((h, total_width, 3), dtype=np.uint8)
    
    # Copy gambar 1
    result[:, :w1] = img1
    
    # Copy gambar 2 (overwrite overlap area)
    result[:, w1 - overlap_width:w1 - overlap_width + w2] = img2
    
    return result

def alpha_blending(img1, img2, overlap_width, alpha=0.5):
    """
    Gabungkan dengan fixed alpha blending.
    
    Di area overlap: output = alpha*img1 + (1-alpha)*img2
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    h = min(h1, h2)
    if h1 != h:
        img1 = cv2.resize(img1, (w1, h))
    if h2 != h:
        img2 = cv2.resize(img2, (w2, h))
    
    total_width = w1 + w2 - overlap_width
    result = np.zeros((h, total_width, 3), dtype=np.uint8)
    
    # Copy gambar 1 (bagian non-overlap)
    result[:, :w1 - overlap_width] = img1[:, :w1 - overlap_width]
    
    # Copy gambar 2 (bagian non-overlap)
    result[:, w1:] = img2[:, overlap_width:]
    
    # Blend area overlap
    overlap1 = img1[:, w1 - overlap_width:].astype(np.float32)
    overlap2 = img2[:, :overlap_width].astype(np.float32)
    blended = alpha * overlap1 + (1 - alpha) * overlap2
    result[:, w1 - overlap_width:w1] = blended.astype(np.uint8)
    
    return result

def feather_blending(img1, img2, overlap_width):
    """
    Gabungkan dengan feather (gradient) blending.
    
    Alpha berubah secara gradual dari 1 ke 0 di area overlap.
    Ini memberikan transisi yang lebih smooth.
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    h = min(h1, h2)
    if h1 != h:
        img1 = cv2.resize(img1, (w1, h))
    if h2 != h:
        img2 = cv2.resize(img2, (w2, h))
    
    total_width = w1 + w2 - overlap_width
    result = np.zeros((h, total_width, 3), dtype=np.uint8)
    
    # Copy non-overlap areas
    result[:, :w1 - overlap_width] = img1[:, :w1 - overlap_width]
    result[:, w1:] = img2[:, overlap_width:]
    
    # Buat gradient alpha mask
    alpha = np.linspace(1, 0, overlap_width)
    alpha = alpha.reshape(1, -1, 1)  # Shape: (1, overlap_width, 1)
    alpha = np.tile(alpha, (h, 1, 3))  # Shape: (h, overlap_width, 3)
    
    # Blend overlap area
    overlap1 = img1[:, w1 - overlap_width:].astype(np.float32)
    overlap2 = img2[:, :overlap_width].astype(np.float32)
    blended = alpha * overlap1 + (1 - alpha) * overlap2
    result[:, w1 - overlap_width:w1] = blended.astype(np.uint8)
    
    return result

def build_gaussian_pyramid(img, levels):
    """
    Bangun Gaussian pyramid.
    """
    pyramid = [img.astype(np.float32)]
    for i in range(levels - 1):
        img = cv2.pyrDown(img)
        pyramid.append(img.astype(np.float32))
    return pyramid

def build_laplacian_pyramid(img, levels):
    """
    Bangun Laplacian pyramid dari gambar.
    """
    gaussian = build_gaussian_pyramid(img, levels)
    laplacian = []
    
    for i in range(levels - 1):
        size = (gaussian[i].shape[1], gaussian[i].shape[0])
        expanded = cv2.pyrUp(gaussian[i + 1], dstsize=size)
        lap = gaussian[i] - expanded
        laplacian.append(lap)
    
    laplacian.append(gaussian[-1])  # Lowest level is Gaussian
    return laplacian

def reconstruct_from_laplacian(pyramid):
    """
    Rekonstruksi gambar dari Laplacian pyramid.
    """
    img = pyramid[-1]
    for i in range(len(pyramid) - 2, -1, -1):
        size = (pyramid[i].shape[1], pyramid[i].shape[0])
        img = cv2.pyrUp(img, dstsize=size)
        img = img + pyramid[i]
    return img

def laplacian_pyramid_blending(img1, img2, overlap_width, levels=6):
    """
    Gabungkan dengan Laplacian pyramid blending.
    
    Ini adalah teknik blending paling advanced yang bekerja dengan
    memisahkan gambar ke berbagai level frekuensi dan blend masing-masing.
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    h = min(h1, h2)
    if h1 != h:
        img1 = cv2.resize(img1, (w1, h))
    if h2 != h:
        img2 = cv2.resize(img2, (w2, h))
    
    total_width = w1 + w2 - overlap_width
    
    # Adjust dimensions to be divisible by 2^levels
    divisor = 2 ** levels
    h_adj = (h // divisor) * divisor
    w1_adj = (w1 // divisor) * divisor
    w2_adj = (w2 // divisor) * divisor
    total_adj = (total_width // divisor) * divisor
    
    img1 = cv2.resize(img1, (w1_adj, h_adj))
    img2 = cv2.resize(img2, (w2_adj, h_adj))
    
    # Recalculate overlap
    overlap_adj = w1_adj + w2_adj - total_adj
    
    # Buat canvas untuk kedua gambar
    canvas1 = np.zeros((h_adj, total_adj, 3), dtype=np.uint8)
    canvas2 = np.zeros((h_adj, total_adj, 3), dtype=np.uint8)
    
    # Tempatkan gambar
    canvas1[:, :w1_adj] = img1
    canvas2[:, total_adj - w2_adj:] = img2
    
    # Buat mask untuk blending
    mask = np.zeros((h_adj, total_adj), dtype=np.float32)
    blend_center = w1_adj - overlap_adj // 2
    
    # Gradient mask
    for x in range(total_adj):
        if x < blend_center - overlap_adj // 2:
            mask[:, x] = 1.0
        elif x > blend_center + overlap_adj // 2:
            mask[:, x] = 0.0
        else:
            mask[:, x] = 1.0 - (x - (blend_center - overlap_adj // 2)) / overlap_adj
    
    mask = cv2.merge([mask, mask, mask])
    
    # Build Laplacian pyramids
    lap1 = build_laplacian_pyramid(canvas1, levels)
    lap2 = build_laplacian_pyramid(canvas2, levels)
    mask_pyr = build_gaussian_pyramid(mask, levels)
    
    # Blend di setiap level
    blended_pyr = []
    for l1, l2, m in zip(lap1, lap2, mask_pyr):
        blended = l1 * m + l2 * (1 - m)
        blended_pyr.append(blended)
    
    # Rekonstruksi
    result = reconstruct_from_laplacian(blended_pyr)
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return result

def main():
    """
    Fungsi utama untuk membandingkan teknik blending.
    """
    print("=" * 60)
    print("PERBANDINGAN TEKNIK BLENDING")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load gambar
    img1_path = os.path.join(DATA_DIR, "left01.jpg")
    img2_path = os.path.join(DATA_DIR, "right01.jpg")
    
    # Fallback
    if not os.path.exists(img1_path):
        img1_path = os.path.join(DATA_DIR, "graf1.png")
        img2_path = os.path.join(DATA_DIR, "graf3.png")
    
    if not os.path.exists(img1_path):
        # Gunakan gambar apapun yang tersedia
        files = [f for f in os.listdir(DATA_DIR) 
                if f.endswith(('.jpg', '.png', '.jpeg'))]
        if len(files) >= 2:
            img1_path = os.path.join(DATA_DIR, files[0])
            img2_path = os.path.join(DATA_DIR, files[1])
        else:
            print("ERROR: Tidak ada gambar yang tersedia!")
            return
    
    print(f"\nMemuat gambar...")
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        print("ERROR: Gagal memuat gambar!")
        return
    
    # Resize untuk efisiensi
    max_dim = 400
    for i, img in enumerate([img1, img2]):
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            if i == 0:
                img1 = cv2.resize(img1, None, fx=scale, fy=scale)
            else:
                img2 = cv2.resize(img2, None, fx=scale, fy=scale)
    
    print(f"Gambar 1: {img1.shape}")
    print(f"Gambar 2: {img2.shape}")
    
    # Tentukan overlap
    overlap_width = BLEND_WIDTH * 2  # Area overlap
    
    # Jalankan berbagai teknik blending
    print(f"\nMenjalankan blending dengan overlap width: {overlap_width}...")
    
    results = {}
    
    # 1. No Blending
    print("  1. No Blending...", end=" ")
    start = time.time()
    results['no_blend'] = no_blending(img1, img2, overlap_width)
    print(f"({(time.time()-start)*1000:.1f} ms)")
    
    # 2. Alpha Blending
    print(f"  2. Alpha Blending (α={ALPHA_VALUE})...", end=" ")
    start = time.time()
    results['alpha'] = alpha_blending(img1, img2, overlap_width, ALPHA_VALUE)
    print(f"({(time.time()-start)*1000:.1f} ms)")
    
    # 3. Feather Blending
    print("  3. Feather Blending...", end=" ")
    start = time.time()
    results['feather'] = feather_blending(img1, img2, overlap_width)
    print(f"({(time.time()-start)*1000:.1f} ms)")
    
    # 4. Laplacian Pyramid Blending
    print(f"  4. Laplacian Pyramid Blending ({PYRAMID_LEVELS} levels)...", end=" ")
    start = time.time()
    results['pyramid'] = laplacian_pyramid_blending(img1, img2, overlap_width, PYRAMID_LEVELS)
    print(f"({(time.time()-start)*1000:.1f} ms)")
    
    # Visualisasi
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    
    # Input images
    combined_input = np.hstack([
        cv2.cvtColor(img1, cv2.COLOR_BGR2RGB),
        cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    ])
    axes[0, 0].imshow(combined_input)
    axes[0, 0].set_title("Input Images")
    axes[0, 0].axis('off')
    
    # No Blending
    axes[0, 1].imshow(cv2.cvtColor(results['no_blend'], cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("No Blending\n(Seam sangat terlihat)")
    axes[0, 1].axis('off')
    # Tandai area seam
    h, w = results['no_blend'].shape[:2]
    seam_x = img1.shape[1]
    axes[0, 1].axvline(x=seam_x, color='r', linestyle='--', linewidth=2)
    
    # Alpha Blending
    axes[1, 0].imshow(cv2.cvtColor(results['alpha'], cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"Alpha Blending (α={ALPHA_VALUE})\n(Transisi rata di overlap)")
    axes[1, 0].axis('off')
    
    # Feather Blending
    axes[1, 1].imshow(cv2.cvtColor(results['feather'], cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"Feather Blending (width={BLEND_WIDTH})\n(Gradient halus)")
    axes[1, 1].axis('off')
    
    # Laplacian Pyramid Blending
    axes[2, 0].imshow(cv2.cvtColor(results['pyramid'], cv2.COLOR_BGR2RGB))
    axes[2, 0].set_title(f"Laplacian Pyramid ({PYRAMID_LEVELS} levels)\n(Multi-scale, paling halus)")
    axes[2, 0].axis('off')
    
    # Perbandingan zoom pada seam area
    # Crop area seam dari setiap hasil
    seam_start = img1.shape[1] - overlap_width
    seam_end = img1.shape[1] + overlap_width
    
    zoom_strips = []
    labels = ['No Blend', 'Alpha', 'Feather', 'Pyramid']
    for key in ['no_blend', 'alpha', 'feather', 'pyramid']:
        result = results[key]
        h = result.shape[0]
        # Pastikan bounds valid
        end = min(seam_end, result.shape[1])
        start = max(0, seam_start)
        if start < end:
            zoom = result[h//3:2*h//3, start:end]
            zoom_strips.append(cv2.cvtColor(zoom, cv2.COLOR_BGR2RGB))
    
    if zoom_strips:
        # Seragamkan ukuran
        min_h = min(z.shape[0] for z in zoom_strips)
        min_w = min(z.shape[1] for z in zoom_strips)
        zoom_strips = [cv2.resize(z, (min_w, min_h)) for z in zoom_strips]
        
        # Stack vertikal
        zoom_comparison = np.vstack(zoom_strips)
        axes[2, 1].imshow(zoom_comparison)
        axes[2, 1].set_title("Zoom pada Area Seam\n(Atas→Bawah: No Blend, Alpha, Feather, Pyramid)")
        axes[2, 1].axis('off')
        
        # Garis pemisah
        for i in range(1, 4):
            axes[2, 1].axhline(y=i*min_h, color='white', linestyle='-', linewidth=1)
    
    plt.suptitle(f"Perbandingan Teknik Blending\nOverlap: {overlap_width}px, Blend Width: {BLEND_WIDTH}px", 
                fontsize=14)
    plt.tight_layout()
    
    # Simpan
    output_path = os.path.join(OUTPUT_DIR, "03_blending_comparison.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nHasil disimpan ke: {output_path}")
    
    # Simpan hasil terbaik (pyramid)
    best_path = os.path.join(OUTPUT_DIR, "03_best_blend_pyramid.jpg")
    cv2.imwrite(best_path, results['pyramid'])
    print(f"Best blend disimpan ke: {best_path}")
    
    # Auto-close setelah 2 detik
    print("\n[INFO] Menampilkan hasil... (akan auto-close dalam 2 detik)")
    plt.show(block=False)
    plt.pause(2)
    plt.close('all')
    print("[INFO] Selesai!")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY TEKNIK BLENDING")
    print("=" * 60)
    print("""
┌────────────────────┬────────────────────────────────────────┐
│ Teknik             │ Karakteristik                          │
├────────────────────┼────────────────────────────────────────┤
│ No Blending        │ Cepat, seam sangat terlihat            │
│ Alpha Blending     │ Sederhana, ghosting di area bergerak   │
│ Feather Blending   │ Transisi halus, cukup untuk kebanyakan │
│ Pyramid Blending   │ Paling bagus, handle exposure berbeda  │
└────────────────────┴────────────────────────────────────────┘
    """)

if __name__ == "__main__":
    main()
