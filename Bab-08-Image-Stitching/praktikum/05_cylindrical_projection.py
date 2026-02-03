"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 5: Cylindrical Projection

Deskripsi:
    Program ini mendemonstrasikan proyeksi silinder untuk pembuatan panorama
    dengan field of view (FOV) yang lebar (> 90°). Proyeksi planar biasa
    akan menghasilkan distorsi besar pada sudut lebar, sedangkan proyeksi
    silinder menjaga proporsi lebih baik.

Teori Cylindrical Projection:
    Untuk setiap piksel (x, y) pada gambar planar, koordinat silinder adalah:
    
    x' = f * arctan(x/f)
    y' = f * y / sqrt(x² + f²)
    
    dimana f adalah focal length dalam pixel.

Kegunaan:
    - Panorama horizontal 360°
    - Virtual tour
    - Aplikasi VR

Parameter yang dapat dimodifikasi:
    - FOCAL_LENGTH: Focal length (pixel), semakin besar = kurang curved
    - AUTO_FOCAL: Estimasi focal length otomatis dari ukuran gambar

Output:
    - Perbandingan proyeksi planar vs cylindrical
    - Panorama dengan proyeksi silinder

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Focal length dalam pixel
# Semakin besar = proyeksi lebih "flat"
# Typical range: 200-2000 (tergantung ukuran gambar)
FOCAL_LENGTH = 500

# Estimasi focal length otomatis dari ukuran gambar
# Jika True, FOCAL_LENGTH diabaikan
AUTO_FOCAL = True

# Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def cylindrical_warp(img, focal_length):
    """
    Warp gambar ke proyeksi silinder.
    
    Parameters:
        img: Gambar input
        focal_length: Focal length dalam pixel
    
    Returns:
        warped: Gambar dengan proyeksi silinder
        mask: Mask valid pixels
    """
    h, w = img.shape[:2]
    
    # Center point
    cx, cy = w // 2, h // 2
    
    # Buat coordinate grid untuk output
    # Output akan lebih kecil karena proyeksi
    out_w = int(2 * focal_length * np.arctan(w / (2 * focal_length)))
    out_h = h
    
    # Grid koordinat output
    y_out, x_out = np.mgrid[0:out_h, 0:out_w]
    
    # Konversi ke koordinat centered
    x_out = x_out - out_w // 2
    y_out = y_out - out_h // 2
    
    # Inverse cylindrical projection (output -> input)
    # Dari koordinat silinder ke koordinat planar
    theta = x_out / focal_length
    h_cyl = y_out / focal_length
    
    # Koordinat pada bidang planar
    x_in = focal_length * np.tan(theta)
    y_in = h_cyl * np.sqrt(x_in**2 + focal_length**2)
    
    # Shift ke koordinat image
    x_in = x_in + cx
    y_in = y_in + cy
    
    # Konversi ke float32 untuk remap
    map_x = x_in.astype(np.float32)
    map_y = y_in.astype(np.float32)
    
    # Warp menggunakan remap
    warped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, 
                       borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    
    # Buat mask untuk valid pixels
    mask = (map_x >= 0) & (map_x < w) & (map_y >= 0) & (map_y < h)
    mask = mask.astype(np.uint8) * 255
    
    return warped, mask

def estimate_focal_length(img_width, fov_degrees=60):
    """
    Estimasi focal length dari ukuran gambar dan assumed FOV.
    
    Parameters:
        img_width: Lebar gambar dalam pixel
        fov_degrees: Assumed field of view dalam derajat
    
    Returns:
        focal_length: Estimated focal length dalam pixel
    """
    fov_rad = np.radians(fov_degrees)
    focal_length = img_width / (2 * np.tan(fov_rad / 2))
    return focal_length

def cylindrical_stitch(images, focal_length):
    """
    Stitch gambar dengan proyeksi silinder.
    
    Parameters:
        images: List gambar untuk di-stitch
        focal_length: Focal length untuk proyeksi
    
    Returns:
        panorama: Hasil stitching
    """
    if len(images) < 2:
        return None
    
    # Warp semua gambar ke proyeksi silinder
    print("  Warping ke proyeksi silinder...")
    warped_images = []
    masks = []
    
    for i, img in enumerate(images):
        warped, mask = cylindrical_warp(img, focal_length)
        warped_images.append(warped)
        masks.append(mask)
        print(f"    Image {i+1}: {img.shape} -> {warped.shape}")
    
    # Gunakan OpenCV Stitcher pada gambar yang sudah di-warp
    print("  Stitching...")
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    status, panorama = stitcher.stitch(warped_images)
    
    if status == cv2.Stitcher_OK:
        return panorama
    else:
        print(f"    Stitcher failed with status {status}")
        return None

def compare_projections(img):
    """
    Bandingkan proyeksi planar vs cylindrical.
    """
    h, w = img.shape[:2]
    
    # Estimasi focal length
    if AUTO_FOCAL:
        focal = estimate_focal_length(w, fov_degrees=60)
    else:
        focal = FOCAL_LENGTH
    
    print(f"  Focal length: {focal:.1f} pixels")
    
    # Warp ke cylindrical
    warped, mask = cylindrical_warp(img, focal)
    
    return img, warped, focal

def main():
    """
    Fungsi utama untuk cylindrical projection demo.
    """
    print("=" * 60)
    print("CYLINDRICAL PROJECTION")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load gambar
    # Coba gunakan gambar building atau apapun yang tersedia
    img_files = ["building.jpg", "home.jpg", "left01.jpg", "lena.jpg"]
    img = None
    img_name = ""
    
    for f in img_files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            img = cv2.imread(path)
            img_name = f
            break
    
    if img is None:
        # Coba file apapun
        files = glob.glob(os.path.join(DATA_DIR, "*.[jp][pn][g]*"))
        if files:
            img = cv2.imread(files[0])
            img_name = os.path.basename(files[0])
    
    if img is None:
        print("ERROR: Tidak ada gambar yang tersedia!")
        return
    
    print(f"\nMenggunakan gambar: {img_name}")
    print(f"Ukuran: {img.shape}")
    
    # Resize jika perlu
    max_dim = 600
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, None, fx=scale, fy=scale)
        print(f"Resized ke: {img.shape}")
    
    # Demo 1: Perbandingan proyeksi
    print("\nDemo 1: Perbandingan Proyeksi")
    original, cylindrical, focal = compare_projections(img)
    
    # Demo 2: Efek focal length
    print("\nDemo 2: Efek Focal Length")
    focal_lengths = [200, 400, 800]
    warped_results = []
    
    for f in focal_lengths:
        warped, _ = cylindrical_warp(img, f)
        warped_results.append(warped)
        print(f"  f={f}: output shape = {warped.shape}")
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Row 1: Original vs Cylindrical
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title(f"Original (Planar)\n{original.shape[1]}x{original.shape[0]}")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(cylindrical, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"Cylindrical Projection\nf={focal:.0f}")
    axes[0, 1].axis('off')
    
    # Overlay grid untuk visualisasi distorsi
    grid_img = original.copy()
    grid_cyl = cylindrical.copy()
    
    # Draw grid pada original
    for x in range(0, grid_img.shape[1], 50):
        cv2.line(grid_img, (x, 0), (x, grid_img.shape[0]), (0, 255, 0), 1)
    for y in range(0, grid_img.shape[0], 50):
        cv2.line(grid_img, (0, y), (grid_img.shape[1], y), (0, 255, 0), 1)
    
    # Draw grid pada cylindrical
    for x in range(0, grid_cyl.shape[1], 50):
        cv2.line(grid_cyl, (x, 0), (x, grid_cyl.shape[0]), (0, 255, 0), 1)
    for y in range(0, grid_cyl.shape[0], 50):
        cv2.line(grid_cyl, (0, y), (grid_cyl.shape[1], y), (0, 255, 0), 1)
    
    axes[0, 2].imshow(cv2.cvtColor(np.hstack([grid_img, grid_cyl]), cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title("Grid Comparison\n(Planar | Cylindrical)")
    axes[0, 2].axis('off')
    
    # Row 2: Efek focal length
    for i, (f, warped) in enumerate(zip(focal_lengths, warped_results)):
        axes[1, i].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f"f = {f}\n(semakin kecil = lebih curved)")
        axes[1, i].axis('off')
    
    plt.suptitle("Cylindrical Projection untuk Panorama", fontsize=14)
    plt.tight_layout()
    
    # Simpan
    output_path = os.path.join(OUTPUT_DIR, "05_cylindrical_projection.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nHasil disimpan ke: {output_path}")
    
    plt.show()
    
    # Demo 3: Cylindrical stitching (jika ada multiple gambar)
    print("\n" + "=" * 60)
    print("Demo 3: Cylindrical Stitching")
    print("=" * 60)
    
    # Load beberapa gambar
    pano_folder = os.path.join(DATA_DIR, "panorama_set")
    images = []
    
    if os.path.exists(pano_folder):
        files = sorted(glob.glob(os.path.join(pano_folder, "*.[jp][pn][g]*")))
        for f in files[:5]:  # Max 5 gambar
            im = cv2.imread(f)
            if im is not None:
                h, w = im.shape[:2]
                if max(h, w) > 400:
                    scale = 400 / max(h, w)
                    im = cv2.resize(im, None, fx=scale, fy=scale)
                images.append(im)
    
    if len(images) < 2:
        # Fallback
        for f in ["left01.jpg", "right01.jpg"]:
            path = os.path.join(DATA_DIR, f)
            if os.path.exists(path):
                im = cv2.imread(path)
                if im is not None:
                    h, w = im.shape[:2]
                    if max(h, w) > 400:
                        scale = 400 / max(h, w)
                        im = cv2.resize(im, None, fx=scale, fy=scale)
                    images.append(im)
    
    if len(images) >= 2:
        focal_for_stitch = estimate_focal_length(images[0].shape[1], 60)
        panorama = cylindrical_stitch(images, focal_for_stitch)
        
        if panorama is not None:
            print(f"\nCylindrical panorama berhasil!")
            print(f"Dimensi: {panorama.shape}")
            
            # Simpan
            pano_path = os.path.join(OUTPUT_DIR, "05_cylindrical_panorama.jpg")
            cv2.imwrite(pano_path, panorama)
            print(f"Disimpan ke: {pano_path}")
            
            # Tampilkan
            plt.figure(figsize=(14, 6))
            plt.imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
            plt.title(f"Cylindrical Panorama ({len(images)} images)")
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "05_cylindrical_pano_full.png"), 
                       dpi=150, bbox_inches='tight')
            plt.show()
    else:
        print("Tidak cukup gambar untuk cylindrical stitching")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
Cylindrical Projection:
- Digunakan untuk panorama dengan FOV > 90°
- Mencegah distorsi di tepi gambar
- Focal length menentukan "curvature"
  - Kecil = lebih curved (cocok untuk FOV lebar)
  - Besar = lebih flat (mirip planar)
  
Kapan Menggunakan:
- Planar: FOV < 90°, 2-3 gambar
- Cylindrical: FOV 90-360° horizontal
- Spherical: Full 360° vertical dan horizontal
    """)

if __name__ == "__main__":
    main()
