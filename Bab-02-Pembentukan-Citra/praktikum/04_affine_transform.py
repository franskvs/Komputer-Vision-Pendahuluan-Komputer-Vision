# ============================================================
# PROGRAM: 04_affine_transform.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: Program ini mendemonstrasikan transformasi affine
#            yang mencakup rotasi, scaling, translasi, dan shearing
# 
# Tujuan Pembelajaran:
#   1. Memahami transformasi affine dan komponennya
#   2. Menentukan transformation matrix dari 3 pasang titik
#   3. Mengimplementasikan berbagai jenis transformasi
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Gunakan backend non-GUI
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# ============================================================
# KONFIGURASI PATH
# ============================================================

# Dapatkan direktori script (praktikum folder)
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_SCRIPT, "data", "images")
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output4")

# Pastikan folder output ada
os.makedirs(DIR_OUTPUT, exist_ok=True)


# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Titik sumber (3 titik untuk transformasi affine)
#    Format: [(x1, y1), (x2, y2), (x3, y3)]
#    Biasanya: kiri-atas, kanan-atas, kiri-bawah
TITIK_SUMBER = None  # Akan diset otomatis berdasarkan ukuran gambar

# 3. Titik tujuan (akan ditentukan untuk berbagai efek)
TITIK_TUJUAN = None

# 4. Parameter shearing
SHEAR_X = 0.3  # Coba ubah: -0.5 sampai 0.5
SHEAR_Y = 0.0  # Coba ubah: -0.5 sampai 0.5

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(direktori_script, "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, "..", "..", 
                                  "Bab-01-Pendahuluan", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, nama_file)
    
    return path_data


def buat_gambar_sample():
    """Membuat gambar sample untuk demonstrasi"""
    gambar = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Background dengan grid
    for i in range(0, 400, 50):
        cv2.line(gambar, (i, 0), (i, 400), (40, 40, 40), 1)
        cv2.line(gambar, (0, i), (400, i), (40, 40, 40), 1)
    
    # Rectangle
    cv2.rectangle(gambar, (100, 100), (300, 300), (255, 255, 255), 2)
    
    # Diagonal
    cv2.line(gambar, (100, 100), (300, 300), (0, 255, 255), 2)
    cv2.line(gambar, (300, 100), (100, 300), (255, 255, 0), 2)
    
    # Center
    cv2.circle(gambar, (200, 200), 5, (0, 0, 255), -1)
    
    # Text
    cv2.putText(gambar, "AFFINE", (130, 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return gambar


# ============================================================
# FUNGSI TRANSFORMASI AFFINE
# ============================================================

def transformasi_affine(gambar, pts_src, pts_dst):
    """
    Melakukan transformasi affine berdasarkan 3 pasang titik
    
    Parameter:
    - gambar: input image
    - pts_src: 3 titik sumber [(x1,y1), (x2,y2), (x3,y3)]
    - pts_dst: 3 titik tujuan
    
    Return:
    - gambar hasil transformasi
    - affine matrix
    """
    # Convert ke numpy array float32
    pts_src = np.float32(pts_src)
    pts_dst = np.float32(pts_dst)
    
    # Hitung affine matrix
    # Matrix 2x3 yang memetakan src ke dst
    M = cv2.getAffineTransform(pts_src, pts_dst)
    
    # Terapkan transformasi
    tinggi, lebar = gambar.shape[:2]
    hasil = cv2.warpAffine(gambar, M, (lebar, tinggi))
    
    return hasil, M


def buat_matrix_affine_manual(tx=0, ty=0, sx=1, sy=1, 
                               sudut=0, shx=0, shy=0):
    """
    Membuat affine matrix secara manual dengan parameter spesifik
    
    Parameter:
    - tx, ty: translasi
    - sx, sy: skala
    - sudut: rotasi (derajat)
    - shx, shy: shearing
    
    Return:
    - affine matrix 2x3
    """
    theta = np.radians(sudut)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    
    # Rotation matrix
    R = np.array([
        [cos_t, -sin_t],
        [sin_t, cos_t]
    ])
    
    # Scaling matrix
    S = np.array([
        [sx, 0],
        [0, sy]
    ])
    
    # Shearing matrix
    H = np.array([
        [1, shx],
        [shy, 1]
    ])
    
    # Kombinasi: Scaling * Shearing * Rotation
    combined = S @ H @ R
    
    # Buat matrix 2x3 dengan translasi
    M = np.array([
        [combined[0, 0], combined[0, 1], tx],
        [combined[1, 0], combined[1, 1], ty]
    ], dtype=np.float32)
    
    return M


def demo_komponen_transformasi(gambar):
    """
    Demonstrasi setiap komponen transformasi affine secara terpisah
    """
    print("\n" + "=" * 60)
    print("KOMPONEN TRANSFORMASI AFFINE")
    print("=" * 60)
    
    tinggi, lebar = gambar.shape[:2]
    
    print("""
AFFINE TRANSFORMATION terdiri dari:
1. Translasi  - Pergeseran posisi
2. Rotasi     - Pemutaran
3. Scaling    - Perubahan ukuran
4. Shearing   - Pergeseran sejajar
    """)
    
    transformasi_list = [
        (buat_matrix_affine_manual(tx=50, ty=30), "Translasi\n(tx=50, ty=30)"),
        (buat_matrix_affine_manual(sudut=30), "Rotasi 30°"),
        (buat_matrix_affine_manual(sx=0.7, sy=0.7), "Scale 0.7x"),
        (buat_matrix_affine_manual(shx=0.3), "Shear X 0.3"),
        (buat_matrix_affine_manual(shy=0.3), "Shear Y 0.3"),
        (buat_matrix_affine_manual(sudut=15, sx=0.8, shx=0.2, tx=30), "Kombinasi"),
    ]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    # Original
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    for i, (M, label) in enumerate(transformasi_list):
        hasil = cv2.warpAffine(gambar, M, (lebar, tinggi))
        axes[i+1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i+1].set_title(label)
        axes[i+1].axis('off')
    
    axes[7].axis('off')  # Kosongkan
    
    plt.suptitle("Komponen Transformasi Affine", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def demo_transformasi_dengan_titik(gambar):
    """
    Demonstrasi transformasi affine dengan mendefinisikan titik
    """
    print("\n" + "=" * 60)
    print("TRANSFORMASI AFFINE DENGAN TITIK")
    print("=" * 60)
    
    tinggi, lebar = gambar.shape[:2]
    
    # Titik sumber: 3 sudut gambar
    # Kiri-atas, Kanan-atas, Kiri-bawah
    pts_src = np.float32([
        [0, 0],
        [lebar-1, 0],
        [0, tinggi-1]
    ])
    
    print(f"""
TRANSFORMASI AFFINE membutuhkan 3 pasang titik korespondensi.
Mengapa 3 titik? Karena matrix affine 2x3 memiliki 6 parameter:
    
    | a  b  tx |     a, b   : rotasi + scaling + shearing
    | c  d  ty |     c, d   : rotasi + scaling + shearing
                     tx, ty : translasi
    
6 unknowns butuh 6 equations = 3 titik × 2 koordinat
    """)
    
    # Berbagai transformasi
    transformasi_list = [
        (pts_src, "Original"),
        # Shear horizontal
        (np.float32([[50, 0], [lebar-1+50, 0], [0, tinggi-1]]), "Shear Kanan"),
        # Shear vertikal
        (np.float32([[0, 0], [lebar-1, 50], [0, tinggi-1+50]]), "Shear Bawah"),
        # Perspective-like (tapi affine)
        (np.float32([[50, 50], [lebar-1-50, 50], [0, tinggi-1]]), "Trapezoid"),
        # Mirror horizontal
        (np.float32([[lebar-1, 0], [0, 0], [lebar-1, tinggi-1]]), "Mirror Horizontal"),
        # Kombinasi
        (np.float32([[100, 50], [lebar-1, 0], [50, tinggi-1]]), "Kombinasi"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (pts_dst, label) in enumerate(transformasi_list):
        if i == 0:
            hasil = gambar.copy()
        else:
            M = cv2.getAffineTransform(pts_src, pts_dst)
            hasil = cv2.warpAffine(gambar, M, (lebar, tinggi))
        
        # Gambar titik-titik
        hasil_vis = hasil.copy()
        for j, pt in enumerate(pts_dst):
            pt_int = (int(pt[0]), int(pt[1]))
            if 0 <= pt_int[0] < lebar and 0 <= pt_int[1] < tinggi:
                cv2.circle(hasil_vis, pt_int, 8, (0, 255, 0), -1)
                cv2.putText(hasil_vis, str(j+1), (pt_int[0]+10, pt_int[1]+5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        axes[i].imshow(cv2.cvtColor(hasil_vis, cv2.COLOR_BGR2RGB))
        axes[i].set_title(label)
        axes[i].axis('off')
        
        print(f"[{i+1}] {label}")
        print(f"    Titik tujuan: {pts_dst.tolist()}")
    
    plt.suptitle("Transformasi Affine dengan Berbagai Titik Tujuan", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def demo_shearing(gambar):
    """
    Demonstrasi shearing dengan berbagai nilai
    """
    print("\n" + "=" * 60)
    print("DEMO SHEARING")
    print("=" * 60)
    
    print("""
SHEARING (Geseran):
- Menggeser titik-titik secara paralel
- Shear X: Menggeser horizontal berdasarkan koordinat Y
- Shear Y: Menggeser vertikal berdasarkan koordinat X

Matrix Shearing:
    | 1   shx |     x' = x + shx * y
    | shy  1  |     y' = shy * x + y
    """)
    
    tinggi, lebar = gambar.shape[:2]
    
    # Berbagai nilai shear
    shear_values = [
        (0, 0, "Original"),
        (0.3, 0, "Shear X = 0.3"),
        (-0.3, 0, "Shear X = -0.3"),
        (0, 0.3, "Shear Y = 0.3"),
        (0, -0.3, "Shear Y = -0.3"),
        (0.2, 0.2, "Shear X,Y = 0.2"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (shx, shy, label) in enumerate(shear_values):
        M = buat_matrix_affine_manual(shx=shx, shy=shy)
        
        # Perbesar canvas untuk menampung hasil shearing
        new_lebar = int(lebar * (1 + abs(shx)))
        new_tinggi = int(tinggi * (1 + abs(shy)))
        
        hasil = cv2.warpAffine(gambar, M, (new_lebar, new_tinggi))
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(label)
        axes[i].axis('off')
    
    plt.suptitle("Efek Shearing pada Gambar", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def demo_inverse_affine(gambar):
    """
    Demonstrasi inverse affine transform
    """
    print("\n" + "=" * 60)
    print("INVERSE AFFINE TRANSFORM")
    print("=" * 60)
    
    print("""
INVERSE TRANSFORM:
Jika kita tahu transformasi yang diterapkan, kita bisa
mengembalikan gambar ke bentuk aslinya dengan inverse matrix.

    M × M⁻¹ = I (Identity Matrix)
    
Ini berguna untuk:
- Image rectification
- Undo transformasi
- Menghitung transformasi balik
    """)
    
    tinggi, lebar = gambar.shape[:2]
    
    # Buat transformasi
    M = buat_matrix_affine_manual(sudut=30, sx=0.8, shx=0.2)
    
    # Transform
    hasil_transform = cv2.warpAffine(gambar, M, (lebar, tinggi))
    
    # Inverse transform
    M_full = np.vstack([M, [0, 0, 1]])  # 3x3
    M_inv = np.linalg.inv(M_full)[:2]   # 2x3
    
    hasil_inverse = cv2.warpAffine(hasil_transform, M_inv, (lebar, tinggi))
    
    # Tampilkan
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil_transform, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Setelah Transform\n(rotasi 30°, scale 0.8, shear 0.2)")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hasil_inverse, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Setelah Inverse Transform\n(kembali ke bentuk asal)")
    axes[2].axis('off')
    
    plt.suptitle("Forward dan Inverse Affine Transform", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()
    
    print(f"\nTransformation Matrix M:")
    print(M)
    print(f"\nInverse Matrix M⁻¹:")
    print(M_inv)


def visualisasi_affine_matrix():
    """
    Visualisasi struktur affine matrix
    """
    print("\n" + "=" * 60)
    print("STRUKTUR AFFINE MATRIX")
    print("=" * 60)
    
    print("""
AFFINE MATRIX (2x3):

    | a  b  tx |     | x |     | a*x + b*y + tx |
    |          |  ×  |   |  =  |                |
    | c  d  ty |     | y |     | c*x + d*y + ty |
                     | 1 |

DEKOMPOSISI:
    
    a = sx * cos(θ) + shx * sy * sin(θ)
    b = -sx * sin(θ) + shx * sy * cos(θ)
    c = shy * sx * cos(θ) + sy * sin(θ)
    d = -shy * sx * sin(θ) + sy * cos(θ)

PROPERTI AFFINE TRANSFORM:
    ✓ Garis lurus tetap lurus
    ✓ Garis paralel tetap paralel
    ✓ Titik tengah garis tetap di tengah
    ✗ Sudut BISA berubah
    ✗ Jarak BISA berubah

COMPARISON DENGAN TRANSFORMASI LAIN:
┌────────────────────────┬─────────┬────────┬────────┐
│ Properti               │ Euclidean│ Affine │ Projective│
├────────────────────────┼─────────┼────────┼────────┤
│ Garis → Garis          │ ✓       │ ✓      │ ✓      │
│ Paralel → Paralel      │ ✓       │ ✓      │ ✗      │
│ Rasio Jarak Dipertahankan│ ✓     │ ✓      │ ✗      │
│ Sudut Dipertahankan    │ ✓       │ ✗      │ ✗      │
│ Jarak Dipertahankan    │ ✓       │ ✗      │ ✗      │
│ Degree of Freedom      │ 3       │ 6      │ 8      │
└────────────────────────┴─────────┴────────┴────────┘
    """)


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: TRANSFORMASI AFFINE")
    print("Bab 2 - Pembentukan Citra")
    print("=" * 60)
    
    # Muat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    gambar = cv2.imread(path_gambar)
    
    if gambar is None:
        print(f"[WARNING] Gambar {NAMA_FILE_GAMBAR} tidak ditemukan")
        print("[INFO] Menggunakan gambar sample...")
        gambar = buat_gambar_sample()
    else:
        print(f"[SUKSES] Gambar dimuat: {path_gambar}")
        # Resize ke ukuran standar
        gambar = cv2.resize(gambar, (400, 400))
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    
    # 1. Penjelasan struktur matrix
    visualisasi_affine_matrix()
    
    # 2. Demo komponen transformasi
    demo_komponen_transformasi(gambar)
    
    # 3. Demo transformasi dengan titik
    demo_transformasi_dengan_titik(gambar)
    
    # 4. Demo shearing
    demo_shearing(gambar)
    
    # 5. Demo inverse transform
    demo_inverse_affine(gambar)
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN TRANSFORMASI AFFINE")
    print("=" * 60)
    print("""
FUNGSI UTAMA:
    M = cv2.getAffineTransform(src_pts, dst_pts)
    hasil = cv2.warpAffine(src, M, (width, height))

KOMPONEN TRANSFORMASI:
├── Translasi  : Pergeseran (tx, ty)
├── Rotasi     : Pemutaran (θ)
├── Scaling    : Perubahan ukuran (sx, sy)
└── Shearing   : Geseran sejajar (shx, shy)

KARAKTERISTIK AFFINE:
├── Membutuhkan 3 pasang titik korespondensi
├── Menjaga garis lurus dan paralel
├── Tidak menjaga sudut dan jarak
└── DOF = 6 (6 parameter bebas)

PENGGUNAAN UMUM:
├── Image alignment
├── Correcting skew
├── Normalisasi untuk recognition
└── Augmentasi data training
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
