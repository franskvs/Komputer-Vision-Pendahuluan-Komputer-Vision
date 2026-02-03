# ============================================================
# PROGRAM: 05_perspektif_transform.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: Program ini mendemonstrasikan transformasi perspektif
#            (homography) untuk koreksi sudut pandang
# 
# Tujuan Pembelajaran:
#   1. Memahami transformasi perspektif dan homography
#   2. Menentukan transformation matrix dari 4 pasang titik
#   3. Aplikasi praktis untuk koreksi dokumen
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

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "sample.jpg"

# 2. Ukuran output untuk bird's eye view
OUTPUT_WIDTH = 400
OUTPUT_HEIGHT = 500

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(direktori_script, "..", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, "..", "..", 
                                  "Bab-01-Pendahuluan", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, nama_file)
    
    return path_data


def buat_gambar_perspektif():
    """Membuat gambar dengan objek dalam perspektif"""
    gambar = np.zeros((500, 600, 3), dtype=np.uint8)
    
    # Background gradient
    for i in range(500):
        gambar[i, :] = [int(30 + i/10), int(40 + i/15), int(50 + i/20)]
    
    # Gambar "dokumen" dalam perspektif (trapezoid)
    # Titik-titik sudut dokumen
    pts = np.array([
        [150, 80],    # top-left
        [450, 100],   # top-right
        [500, 400],   # bottom-right
        [100, 380]    # bottom-left
    ], np.int32)
    
    # Isi dokumen dengan warna cream
    cv2.fillPoly(gambar, [pts], (200, 220, 240))
    
    # Border dokumen
    cv2.polylines(gambar, [pts], True, (50, 50, 50), 3)
    
    # Konten dalam dokumen
    # Garis-garis teks (simulasi)
    for i in range(5):
        y_offset = 120 + i * 50
        # Interpolasi untuk menyesuaikan dengan perspektif
        left_x = int(160 + (100 - 160) * (y_offset - 80) / 300)
        right_x = int(440 + (490 - 440) * (y_offset - 100) / 300)
        cv2.line(gambar, (left_x + 20, y_offset), (right_x - 20, y_offset), 
                (100, 100, 100), 2)
    
    # Marker sudut
    for pt in pts:
        cv2.circle(gambar, tuple(pt), 8, (0, 0, 255), -1)
    
    return gambar, pts


# ============================================================
# FUNGSI TRANSFORMASI PERSPEKTIF
# ============================================================

def order_points(pts):
    """
    Mengurutkan 4 titik dalam urutan: top-left, top-right, bottom-right, bottom-left
    """
    pts = np.array(pts, dtype=np.float32)
    
    # Urutkan berdasarkan koordinat Y
    sorted_by_y = pts[np.argsort(pts[:, 1])]
    
    # 2 titik teratas dan 2 titik terbawah
    top_points = sorted_by_y[:2]
    bottom_points = sorted_by_y[2:]
    
    # Urutkan berdasarkan X
    top_left, top_right = top_points[np.argsort(top_points[:, 0])]
    bottom_left, bottom_right = bottom_points[np.argsort(bottom_points[:, 0])]
    
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)


def transformasi_perspektif(gambar, pts_src, lebar=None, tinggi=None):
    """
    Melakukan transformasi perspektif (bird's eye view)
    
    Parameter:
    - gambar: input image
    - pts_src: 4 titik sudut sumber (belum terurut)
    - lebar, tinggi: ukuran output
    
    Return:
    - gambar hasil transformasi
    - matrix perspektif
    """
    # Urutkan titik
    pts_src = order_points(pts_src)
    
    # Hitung dimensi output jika tidak diberikan
    if lebar is None or tinggi is None:
        # Gunakan jarak terbesar sebagai dimensi
        lebar_top = np.linalg.norm(pts_src[0] - pts_src[1])
        lebar_bottom = np.linalg.norm(pts_src[3] - pts_src[2])
        tinggi_left = np.linalg.norm(pts_src[0] - pts_src[3])
        tinggi_right = np.linalg.norm(pts_src[1] - pts_src[2])
        
        lebar = int(max(lebar_top, lebar_bottom))
        tinggi = int(max(tinggi_left, tinggi_right))
    
    # Titik tujuan (persegi panjang)
    pts_dst = np.float32([
        [0, 0],              # top-left
        [lebar - 1, 0],      # top-right
        [lebar - 1, tinggi - 1],  # bottom-right
        [0, tinggi - 1]      # bottom-left
    ])
    
    # Hitung perspective transform matrix
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    
    # Terapkan transformasi
    hasil = cv2.warpPerspective(gambar, M, (lebar, tinggi))
    
    return hasil, M, pts_src, pts_dst


def demo_perbedaan_affine_perspective(gambar, pts):
    """
    Membandingkan transformasi affine vs perspective
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN AFFINE vs PERSPECTIVE TRANSFORM")
    print("=" * 60)
    
    print("""
PERBEDAAN UTAMA:

AFFINE TRANSFORM:
├── Membutuhkan 3 pasang titik
├── DOF = 6
├── Garis paralel TETAP paralel
├── Matrix 2x3

PERSPECTIVE TRANSFORM:
├── Membutuhkan 4 pasang titik
├── DOF = 8
├── Garis paralel BISA tidak paralel
├── Matrix 3x3 (homography)
    """)
    
    tinggi, lebar = gambar.shape[:2]
    
    # Perspective transform
    hasil_persp, _, _, _ = transformasi_perspektif(gambar, pts, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    # Affine transform (gunakan 3 titik pertama)
    pts_src_affine = np.float32(pts[:3])
    pts_dst_affine = np.float32([
        [0, 0],
        [OUTPUT_WIDTH - 1, 0],
        [OUTPUT_WIDTH - 1, OUTPUT_HEIGHT - 1]
    ])
    M_affine = cv2.getAffineTransform(pts_src_affine, pts_dst_affine)
    hasil_affine = cv2.warpAffine(gambar, M_affine, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
    
    # Tampilkan perbandingan
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original dengan titik ditandai
    gambar_marked = gambar.copy()
    pts_ordered = order_points(pts)
    labels = ['TL', 'TR', 'BR', 'BL']
    colors = [(0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
    for i, (pt, label, color) in enumerate(zip(pts_ordered, labels, colors)):
        cv2.circle(gambar_marked, tuple(pt.astype(int)), 10, color, -1)
        cv2.putText(gambar_marked, label, (int(pt[0])+15, int(pt[1])), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    axes[0].imshow(cv2.cvtColor(gambar_marked, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original dengan 4 Titik")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil_affine, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Affine Transform\n(3 titik, distorsi terlihat)")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hasil_persp, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Perspective Transform\n(4 titik, koreksi sempurna)")
    axes[2].axis('off')
    
    plt.suptitle("Affine vs Perspective Transform", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_berbagai_perspektif():
    """
    Demonstrasi berbagai sudut perspektif
    """
    print("\n" + "=" * 60)
    print("DEMO BERBAGAI SUDUT PERSPEKTIF")
    print("=" * 60)
    
    # Buat gambar dasar (persegi)
    gambar = np.zeros((400, 400, 3), dtype=np.uint8)
    gambar[:] = (200, 220, 240)  # Cream background
    cv2.rectangle(gambar, (50, 50), (350, 350), (100, 100, 100), 2)
    
    # Grid
    for i in range(50, 350, 50):
        cv2.line(gambar, (i, 50), (i, 350), (150, 150, 150), 1)
        cv2.line(gambar, (50, i), (350, i), (150, 150, 150), 1)
    
    cv2.putText(gambar, "ORIGINAL", (130, 210), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
    
    tinggi, lebar = gambar.shape[:2]
    
    # Titik asli (persegi penuh)
    pts_orig = np.float32([
        [0, 0], [lebar-1, 0], [lebar-1, tinggi-1], [0, tinggi-1]
    ])
    
    # Berbagai perspektif tujuan
    perspektif_list = [
        (pts_orig, "Original"),
        (np.float32([[50, 0], [lebar-51, 0], [lebar-1, tinggi-1], [0, tinggi-1]]), 
         "View dari Bawah"),
        (np.float32([[0, 50], [lebar-1, 0], [lebar-1, tinggi-1], [0, tinggi-51]]), 
         "View dari Kanan"),
        (np.float32([[0, 0], [lebar-1, 50], [lebar-51, tinggi-1], [50, tinggi-1]]), 
         "View dari Atas"),
        (np.float32([[50, 50], [lebar-51, 0], [lebar-1, tinggi-51], [0, tinggi-1]]), 
         "Diagonal"),
        (np.float32([[80, 80], [lebar-81, 80], [lebar-81, tinggi-81], [80, tinggi-81]]), 
         "Zoom In"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (pts_dst, label) in enumerate(perspektif_list):
        M = cv2.getPerspectiveTransform(pts_orig, pts_dst)
        hasil = cv2.warpPerspective(gambar, M, (lebar, tinggi))
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(label)
        axes[i].axis('off')
    
    plt.suptitle("Berbagai Transformasi Perspektif", fontsize=14)
    plt.tight_layout()
    plt.show()


def visualisasi_homography_matrix():
    """
    Penjelasan struktur homography matrix
    """
    print("\n" + "=" * 60)
    print("STRUKTUR HOMOGRAPHY MATRIX")
    print("=" * 60)
    
    print("""
HOMOGRAPHY MATRIX (3x3):

    | h00  h01  h02 |     | x |     | x' × w |
    | h10  h11  h12 |  ×  | y |  =  | y' × w |
    | h20  h21  h22 |     | 1 |     |   w    |

Koordinat final:
    x_final = x' / w = (h00×x + h01×y + h02) / (h20×x + h21×y + h22)
    y_final = y' / w = (h10×x + h11×y + h12) / (h20×x + h21×y + h22)

MENGAPA 4 TITIK?
├── Matrix 3x3 dengan h22=1 memiliki 8 unknowns
├── Setiap titik memberikan 2 persamaan
├── 4 titik × 2 = 8 persamaan untuk 8 unknowns

DEGREE OF FREEDOM (DOF):
┌────────────────────┬──────┬─────────────────────────┐
│ Transformasi       │ DOF  │ Titik yang Dibutuhkan   │
├────────────────────┼──────┼─────────────────────────┤
│ Translasi          │ 2    │ 1 titik                 │
│ Euclidean (rigid)  │ 3    │ 2 titik                 │
│ Similarity         │ 4    │ 2 titik                 │
│ Affine             │ 6    │ 3 titik                 │
│ Projective (homog.)│ 8    │ 4 titik                 │
└────────────────────┴──────┴─────────────────────────┘

PROPERTI HOMOGRAPHY:
├── Garis lurus TETAP lurus (collinearity preserved)
├── Garis paralel BISA menjadi tidak paralel
├── Cross-ratio preserved
└── Dapat memodelkan rotasi 3D dari bidang datar
    """)


def demo_inverse_perspective():
    """
    Demonstrasi inverse perspective transform
    """
    print("\n" + "=" * 60)
    print("INVERSE PERSPECTIVE TRANSFORM")
    print("=" * 60)
    
    # Buat gambar dan transform
    gambar, pts = buat_gambar_perspektif()
    hasil, M, pts_src, pts_dst = transformasi_perspektif(gambar, pts, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    # Inverse transform
    M_inv = np.linalg.inv(M)
    tinggi_orig, lebar_orig = gambar.shape[:2]
    hasil_inv = cv2.warpPerspective(hasil, M_inv, (lebar_orig, tinggi_orig))
    
    # Tampilkan
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original (Perspective View)")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Bird's Eye View\n(Perspective Corrected)")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hasil_inv, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Inverse Transform\n(Kembali ke Perspective)")
    axes[2].axis('off')
    
    plt.suptitle("Forward dan Inverse Perspective Transform", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    print("\nPerspective Matrix (3x3):")
    print(M)
    print("\nInverse Matrix:")
    print(M_inv)


def demo_find_homography():
    """
    Demonstrasi cv2.findHomography untuk banyak titik
    """
    print("\n" + "=" * 60)
    print("FIND HOMOGRAPHY DENGAN BANYAK TITIK")
    print("=" * 60)
    
    print("""
cv2.findHomography() dapat menghitung homography dari:
- Lebih dari 4 pasang titik (menggunakan least squares)
- Dengan RANSAC untuk menangani outliers

Berguna untuk:
├── Feature matching (SIFT, ORB, dll)
├── Panorama stitching
└── Object detection dengan template matching
    """)
    
    # Simulasi titik-titik dengan beberapa outlier
    np.random.seed(42)
    
    # Titik sumber (grid 4x4)
    pts_src = []
    for i in range(4):
        for j in range(4):
            pts_src.append([100 + j*100, 100 + i*100])
    pts_src = np.float32(pts_src)
    
    # True homography (rotasi 15 derajat + perspektif)
    angle = np.radians(15)
    H_true = np.array([
        [np.cos(angle), -np.sin(angle), 50],
        [np.sin(angle), np.cos(angle), 30],
        [0.0001, 0.0002, 1]
    ])
    
    # Transformasi titik
    pts_dst = []
    for pt in pts_src:
        pt_h = np.array([pt[0], pt[1], 1])
        pt_t = H_true @ pt_h
        pts_dst.append([pt_t[0]/pt_t[2], pt_t[1]/pt_t[2]])
    pts_dst = np.float32(pts_dst)
    
    # Tambahkan noise
    noise = np.random.randn(*pts_dst.shape) * 3
    pts_dst_noisy = pts_dst + noise
    
    # Tambahkan outliers
    pts_dst_noisy[5] += [100, 100]  # Outlier
    pts_dst_noisy[10] += [-80, 50]  # Outlier
    
    # Find homography dengan berbagai metode
    H_lsq, _ = cv2.findHomography(pts_src, pts_dst_noisy, 0)  # Least squares
    H_ransac, mask_ransac = cv2.findHomography(pts_src, pts_dst_noisy, cv2.RANSAC, 5.0)
    H_lmeds, mask_lmeds = cv2.findHomography(pts_src, pts_dst_noisy, cv2.LMEDS)
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    methods = [
        (H_lsq, None, "Least Squares\n(tanpa rejection)"),
        (H_ransac, mask_ransac, "RANSAC\n(outlier rejection)"),
        (H_lmeds, mask_lmeds, "LMedS\n(outlier rejection)"),
    ]
    
    for ax, (H, mask, title) in zip(axes, methods):
        ax.scatter(pts_src[:, 0], pts_src[:, 1], c='blue', s=50, label='Source')
        ax.scatter(pts_dst_noisy[:, 0], pts_dst_noisy[:, 1], c='red', s=50, label='Destination (noisy)')
        
        if mask is not None:
            inliers = mask.ravel() == 1
            ax.scatter(pts_src[inliers, 0], pts_src[inliers, 1], 
                      facecolors='none', edgecolors='green', s=100, linewidths=2, label='Inliers')
        
        ax.set_title(title)
        ax.legend()
        ax.set_xlim(0, 500)
        ax.set_ylim(500, 0)
        ax.set_aspect('equal')
    
    plt.suptitle("Perbandingan Metode findHomography", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: TRANSFORMASI PERSPEKTIF")
    print("Bab 2 - Pembentukan Citra")
    print("=" * 60)
    
    # Buat gambar dengan perspektif
    gambar, pts = buat_gambar_perspektif()
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Titik sudut dokumen: {pts.tolist()}")
    
    # 1. Penjelasan homography matrix
    visualisasi_homography_matrix()
    
    # 2. Demo transformasi dasar
    hasil, M, pts_src, pts_dst = transformasi_perspektif(gambar, pts, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Gambar asli dengan titik ditandai
    gambar_marked = gambar.copy()
    for i, pt in enumerate(pts):
        cv2.circle(gambar_marked, tuple(pt), 8, (0, 255, 0), -1)
        cv2.putText(gambar_marked, str(i+1), (pt[0]+10, pt[1]), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    axes[0].imshow(cv2.cvtColor(gambar_marked, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Gambar Asli (Perspective View)")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Bird's Eye View\n({OUTPUT_WIDTH}x{OUTPUT_HEIGHT})")
    axes[1].axis('off')
    
    plt.suptitle("Koreksi Perspektif Dokumen", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # 3. Perbandingan affine vs perspective
    demo_perbedaan_affine_perspective(gambar, pts)
    
    # 4. Demo berbagai perspektif
    demo_berbagai_perspektif()
    
    # 5. Demo inverse perspective
    demo_inverse_perspective()
    
    # 6. Demo find homography
    demo_find_homography()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN TRANSFORMASI PERSPEKTIF")
    print("=" * 60)
    print("""
FUNGSI UTAMA:
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)  # Tepat 4 titik
    M = cv2.findHomography(src_pts, dst_pts, method)   # ≥4 titik + outlier handling
    hasil = cv2.warpPerspective(src, M, (width, height))

PARAMETER findHomography:
├── method = 0        : Least squares (semua titik)
├── method = RANSAC   : Random sample consensus
└── method = LMEDS    : Least median of squares

PERBEDAAN DENGAN AFFINE:
├── Affine: 3 titik, DOF=6, paralel tetap paralel
└── Perspective: 4 titik, DOF=8, paralel bisa konvergen

APLIKASI:
├── Document scanner
├── Augmented reality
├── Panorama stitching
├── Camera calibration
└── 3D reconstruction

TIPS:
- Urutan titik: top-left, top-right, bottom-right, bottom-left
- Gunakan RANSAC jika ada outlier pada feature matching
- Inverse transform dengan np.linalg.inv(M)
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
