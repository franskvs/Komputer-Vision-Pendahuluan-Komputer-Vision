# ============================================================
# PROGRAM: 06_edge_detection.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk edge detection (Sobel, Laplacian, Canny)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep edge detection
#   2. Operator gradient: Sobel, Prewitt, Scharr
#   3. Second derivative: Laplacian
#   4. Advanced edge detection: Canny
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor modul os.
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
# Keterangan: Inisialisasi atau perbarui variabel NAMA_FILE_GAMBAR.
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Sobel kernel size
# Opsi: 1, 3, 5, 7 (default: 3)
# Keterangan: Inisialisasi atau perbarui variabel SOBEL_KSIZE.
SOBEL_KSIZE = 3

# 3. Canny thresholds
# Low threshold: untuk edge linking (nilai kecil = lebih banyak edges)
# High threshold: untuk edge detection (nilai besar = hanya strong edges)
# Keterangan: Inisialisasi atau perbarui variabel CANNY_LOW_THRESHOLD.
CANNY_LOW_THRESHOLD = 50
# Keterangan: Inisialisasi atau perbarui variabel CANNY_HIGH_THRESHOLD.
CANNY_HIGH_THRESHOLD = 150

# 4. Gaussian blur sebelum edge detection
# Untuk mengurangi noise (0 = tidak pakai blur)
# Keterangan: Inisialisasi atau perbarui variabel BLUR_KERNEL_SIZE.
BLUR_KERNEL_SIZE = 5

# 5. Laplacian kernel size (harus ganjil)
# Keterangan: Inisialisasi atau perbarui variabel LAPLACIAN_KSIZE.
LAPLACIAN_KSIZE = 3

# ============================================================
# FUNGSI HELPER
# ============================================================

# Keterangan: Definisikan fungsi dapatkan_path_gambar.
def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    lokasi_potensial = [
        os.path.join(direktori_script, "data", "images", nama_file),
        os.path.join(direktori_script, "..", "..", "Bab-01-Pendahuluan", 
                     "data", "images", nama_file),
        os.path.join(direktori_script, nama_file),
    ]
    
    for path in lokasi_potensial:
        if os.path.exists(path):
            return path
    
    return lokasi_potensial[0]


def buat_gambar_sample():
    """Membuat gambar sample dengan edges yang jelas"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600), dtype=np.uint8)
    
    # Background gradient
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Inisialisasi beberapa variabel (gambar[i, :300]).
        gambar[i, :300] = 50
        # Keterangan: Inisialisasi beberapa variabel (gambar[i, 300:]).
        gambar[i, 300:] = 200
    
    # Shapes dengan berbagai intensitas
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), 255, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 100), 60, 180, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillPoly(gambar, [np.array([[250, 300], [350, 200], [450, 300]])], 255)
    
    # Text
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "EDGE", (200, 380), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255, 2)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# Keterangan: Definisikan fungsi preprocess_gambar.
def preprocess_gambar(gambar, blur_ksize=5):
    """
    Preprocessing gambar sebelum edge detection
    
    Langkah:
    1. Convert ke grayscale (jika berwarna)
    2. Apply Gaussian blur untuk reduce noise
    """
    # Convert ke grayscale jika perlu
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = gambar.copy()
    
    # Apply blur jika diminta
    # Keterangan: Cek kondisi blur_ksize > 0.
    if blur_ksize > 0:
        # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gray


# ============================================================
# FUNGSI EDGE DETECTION - FIRST DERIVATIVE
# ============================================================

# Keterangan: Definisikan fungsi sobel_x.
def sobel_x(gambar, ksize=3):
    """
    Sobel operator untuk horizontal edges (gradient X)
    
    Mendeteksi perubahan intensitas horizontal
    (edge vertikal)
    
    Kernel Sobel X (ksize=3):
    [-1  0  1]
    [-2  0  2]
    [-1  0  1]
    """
    # cv2.CV_64F untuk menangkap gradient negatif
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    
    # Convert ke absolute value
    # Keterangan: Inisialisasi atau perbarui variabel sobelx_abs.
    sobelx_abs = np.absolute(sobelx)
    # Keterangan: Inisialisasi atau perbarui variabel sobelx_8u.
    sobelx_8u = np.uint8(sobelx_abs / sobelx_abs.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return sobelx_8u


# Keterangan: Definisikan fungsi sobel_y.
def sobel_y(gambar, ksize=3):
    """
    Sobel operator untuk vertical edges (gradient Y)
    
    Mendeteksi perubahan intensitas vertikal
    (edge horizontal)
    
    Kernel Sobel Y (ksize=3):
    [-1 -2 -1]
    [ 0  0  0]
    [ 1  2  1]
    """
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Keterangan: Inisialisasi atau perbarui variabel sobely_abs.
    sobely_abs = np.absolute(sobely)
    # Keterangan: Inisialisasi atau perbarui variabel sobely_8u.
    sobely_8u = np.uint8(sobely_abs / sobely_abs.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return sobely_8u


# Keterangan: Definisikan fungsi sobel_magnitude.
def sobel_magnitude(gambar, ksize=3):
    """
    Magnitude dari gradient Sobel
    
    magnitude = sqrt(Gx² + Gy²)
    
    Mendeteksi edges di semua arah
    """
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return magnitude


# Keterangan: Definisikan fungsi sobel_direction.
def sobel_direction(gambar, ksize=3):
    """
    Arah (direction) dari gradient Sobel
    
    direction = arctan(Gy / Gx)
    
    Berguna untuk mengetahui orientasi edge
    """
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Keterangan: Inisialisasi atau perbarui variabel direction.
    direction = np.arctan2(sobely, sobelx) * 180 / np.pi
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return direction


# Keterangan: Definisikan fungsi scharr_edge.
def scharr_edge(gambar):
    """
    Scharr operator
    
    Lebih akurat dari Sobel untuk kernel 3x3
    
    Kernel Scharr X:
    [-3   0   3]
    [-10  0  10]
    [-3   0   3]
    """
    # Keterangan: Inisialisasi atau perbarui variabel scharrx.
    scharrx = cv2.Scharr(gambar, cv2.CV_64F, 1, 0)
    # Keterangan: Inisialisasi atau perbarui variabel scharry.
    scharry = cv2.Scharr(gambar, cv2.CV_64F, 0, 1)
    
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.sqrt(scharrx**2 + scharry**2)
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return magnitude


# Keterangan: Definisikan fungsi prewitt_edge.
def prewitt_edge(gambar):
    """
    Prewitt operator (implementasi manual)
    
    Lebih simple dari Sobel
    
    Kernel Prewitt X:
    [-1  0  1]
    [-1  0  1]
    [-1  0  1]
    """
    # Keterangan: Inisialisasi atau perbarui variabel kernel_x.
    kernel_x = np.array([[-1, 0, 1],
                         # Keterangan: Jalankan perintah berikut.
                         [-1, 0, 1],
                         # Keterangan: Inisialisasi beberapa variabel ([-1, 0, 1]], dtype).
                         [-1, 0, 1]], dtype=np.float64)
    
    # Keterangan: Inisialisasi atau perbarui variabel kernel_y.
    kernel_y = np.array([[-1, -1, -1],
                         # Keterangan: Jalankan perintah berikut.
                         [0, 0, 0],
                         # Keterangan: Inisialisasi beberapa variabel ([1, 1, 1]], dtype).
                         [1, 1, 1]], dtype=np.float64)
    
    # Keterangan: Inisialisasi atau perbarui variabel prewitt_x.
    prewitt_x = cv2.filter2D(gambar.astype(np.float64), -1, kernel_x)
    # Keterangan: Inisialisasi atau perbarui variabel prewitt_y.
    prewitt_y = cv2.filter2D(gambar.astype(np.float64), -1, kernel_y)
    
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return magnitude


# ============================================================
# FUNGSI EDGE DETECTION - SECOND DERIVATIVE
# ============================================================

# Keterangan: Definisikan fungsi laplacian_edge.
def laplacian_edge(gambar, ksize=3):
    """
    Laplacian operator (second derivative)
    
    Mendeteksi area dengan perubahan intensitas cepat
    
    Kernel Laplacian (ksize=1):
    [0   1  0]
    [1  -4  1]
    [0   1  0]
    """
    # Keterangan: Hitung Laplacian untuk deteksi tepi.
    laplacian = cv2.Laplacian(gambar, cv2.CV_64F, ksize=ksize)
    
    # Keterangan: Inisialisasi atau perbarui variabel laplacian_abs.
    laplacian_abs = np.absolute(laplacian)
    # Keterangan: Inisialisasi atau perbarui variabel laplacian_8u.
    laplacian_8u = np.uint8(laplacian_abs / laplacian_abs.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return laplacian_8u


# Keterangan: Definisikan fungsi laplacian_of_gaussian.
def laplacian_of_gaussian(gambar, sigma=1.0, ksize=5):
    """
    Laplacian of Gaussian (LoG)
    
    Langkah:
    1. Apply Gaussian blur (smoothing)
    2. Apply Laplacian (edge detection)
    
    Ini mengurangi noise sensitivity dari Laplacian biasa
    """
    # Gaussian blur
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    blurred = cv2.GaussianBlur(gambar, (ksize, ksize), sigma)
    
    # Laplacian
    # Keterangan: Hitung Laplacian untuk deteksi tepi.
    log = cv2.Laplacian(blurred, cv2.CV_64F)
    
    # Keterangan: Inisialisasi atau perbarui variabel log_abs.
    log_abs = np.absolute(log)
    # Keterangan: Inisialisasi atau perbarui variabel log_8u.
    log_8u = np.uint8(log_abs / log_abs.max() * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return log_8u


# ============================================================
# FUNGSI EDGE DETECTION - CANNY
# ============================================================

# Keterangan: Definisikan fungsi canny_edge.
def canny_edge(gambar, low_threshold=50, high_threshold=150):
    """
    Canny Edge Detection
    
    Algoritma multi-stage:
    1. Gaussian smoothing
    2. Gradient calculation (Sobel)
    3. Non-maximum suppression
    4. Double thresholding
    5. Edge tracking by hysteresis
    
    Parameter:
    - low_threshold: minimum gradient untuk weak edge
    - high_threshold: minimum gradient untuk strong edge
    
    Return:
    - binary edge map
    """
    # Keterangan: Inisialisasi atau perbarui variabel edges.
    edges = cv2.Canny(gambar, low_threshold, high_threshold)
    # Keterangan: Kembalikan hasil dari fungsi.
    return edges


# Keterangan: Definisikan fungsi canny_edge_with_aperture.
def canny_edge_with_aperture(gambar, low_threshold=50, high_threshold=150, 
                             # Keterangan: Inisialisasi atau perbarui variabel aperture_size.
                             aperture_size=3, L2gradient=False):
    """
    Canny dengan parameter tambahan
    
    Parameter:
    - aperture_size: ukuran kernel Sobel (3, 5, atau 7)
    - L2gradient: jika True, gunakan L2 norm (lebih akurat)
                  jika False, gunakan L1 norm (lebih cepat)
    """
    # Keterangan: Inisialisasi atau perbarui variabel edges.
    edges = cv2.Canny(gambar, low_threshold, high_threshold, 
                      # Keterangan: Inisialisasi atau perbarui variabel apertureSize.
                      apertureSize=aperture_size, L2gradient=L2gradient)
    # Keterangan: Kembalikan hasil dari fungsi.
    return edges


# Keterangan: Definisikan fungsi auto_canny.
def auto_canny(gambar, sigma=0.33):
    """
    Automatic Canny threshold selection
    
    Menghitung threshold secara otomatis berdasarkan
    median intensitas gambar
    """
    # Hitung median
    # Keterangan: Inisialisasi atau perbarui variabel v.
    v = np.median(gambar)
    
    # Hitung thresholds
    # Keterangan: Inisialisasi atau perbarui variabel lower.
    lower = int(max(0, (1.0 - sigma) * v))
    # Keterangan: Inisialisasi atau perbarui variabel upper.
    upper = int(min(255, (1.0 + sigma) * v))
    
    # Keterangan: Inisialisasi atau perbarui variabel edges.
    edges = cv2.Canny(gambar, lower, upper)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return edges, lower, upper


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_edge_detection_concept.
def demo_edge_detection_concept():
    """
    Demonstrasi konsep edge detection
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("KONSEP EDGE DETECTION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
EDGE adalah perubahan signifikan dalam intensitas gambar.
Edge detection bertujuan untuk menemukan lokasi-lokasi ini.

FIRST DERIVATIVE (Gradient):
├── Sobel, Prewitt, Scharr
├── Mendeteksi rate of change
└── Edge = lokasi dengan gradient tinggi

SECOND DERIVATIVE (Laplacian):
├── Mendeteksi perubahan rate of change
└── Edge = zero crossing

PROSES UMUM:
1. Smoothing (reduce noise)
2. Gradient computation
3. Edge localization
4. Thresholding
    """)
    
    # Buat 1D signal untuk visualisasi
    # Keterangan: Buat range angka berjarak linier.
    x = np.linspace(0, 10, 200)
    # Step function (edge)
    # Keterangan: Inisialisasi atau perbarui variabel signal.
    signal = np.where(x < 5, 50, 200)
    # Add transition
    # Keterangan: Inisialisasi atau perbarui variabel signal[(x >.
    signal[(x >= 4.5) & (x <= 5.5)] = 50 + (200-50) * (x[(x >= 4.5) & (x <= 5.5)] - 4.5)
    
    # Compute derivatives
    # Keterangan: Inisialisasi atau perbarui variabel first_deriv.
    first_deriv = np.gradient(signal)
    # Keterangan: Inisialisasi atau perbarui variabel second_deriv.
    second_deriv = np.gradient(first_deriv)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0].plot(x, signal, 'b-', linewidth).
    axes[0].plot(x, signal, 'b-', linewidth=2)
    # Keterangan: Jalankan perintah berikut.
    axes[0].set_title("1D Signal (Step Function / Edge)")
    # Keterangan: Jalankan perintah berikut.
    axes[0].set_ylabel("Intensity")
    # Keterangan: Jalankan perintah berikut.
    axes[0].grid(True)
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1].plot(x, first_deriv, 'r-', linewidth).
    axes[1].plot(x, first_deriv, 'r-', linewidth=2)
    # Keterangan: Inisialisasi atau perbarui variabel axes[1].axhline(y.
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    # Keterangan: Inisialisasi atau perbarui variabel axes[1].set_title("First Derivative (Gradient)\nEdge.
    axes[1].set_title("First Derivative (Gradient)\nEdge = Peak lokasi")
    # Keterangan: Jalankan perintah berikut.
    axes[1].set_ylabel("Gradient")
    # Keterangan: Jalankan perintah berikut.
    axes[1].grid(True)
    
    # Keterangan: Inisialisasi beberapa variabel (axes[2].plot(x, second_deriv, 'g-', linewidth).
    axes[2].plot(x, second_deriv, 'g-', linewidth=2)
    # Keterangan: Inisialisasi atau perbarui variabel axes[2].axhline(y.
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    # Keterangan: Inisialisasi atau perbarui variabel axes[2].set_title("Second Derivative (Laplacian)\nEdge.
    axes[2].set_title("Second Derivative (Laplacian)\nEdge = Zero crossing")
    # Keterangan: Jalankan perintah berikut.
    axes[2].set_ylabel("Laplacian")
    # Keterangan: Jalankan perintah berikut.
    axes[2].set_xlabel("Position")
    # Keterangan: Jalankan perintah berikut.
    axes[2].grid(True)
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Konsep Edge Detection: Derivative", fontsize).
    plt.suptitle("Konsep Edge Detection: Derivative", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_sobel_operator.
def demo_sobel_operator():
    """
    Demonstrasi Sobel operator
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("SOBEL OPERATOR")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
SOBEL OPERATOR menggunakan konvolusi dengan kernel
yang menghitung gradient (first derivative).

Sobel X (mendeteksi edge vertikal):
[-1  0  1]
[-2  0  2]
[-1  0  1]

Sobel Y (mendeteksi edge horizontal):
[-1 -2 -1]
[ 0  0  0]
[ 1  2  1]

Magnitude = sqrt(Gx² + Gy²)
Direction = arctan(Gy / Gx)
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = buat_gambar_sample()
    
    # Keterangan: Inisialisasi atau perbarui variabel gray.
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Hitung Sobel
    # Keterangan: Inisialisasi atau perbarui variabel sobelx.
    sobelx = sobel_x(gray, SOBEL_KSIZE)
    # Keterangan: Inisialisasi atau perbarui variabel sobely.
    sobely = sobel_y(gray, SOBEL_KSIZE)
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = sobel_magnitude(gray, SOBEL_KSIZE)
    # Keterangan: Inisialisasi atau perbarui variabel direction.
    direction = sobel_direction(gray, SOBEL_KSIZE)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gray, cmap).
    axes[0, 0].imshow(gray, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original (Grayscale)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(sobelx, cmap).
    axes[0, 1].imshow(sobelx, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Sobel X (Vertical Edges)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(sobely, cmap).
    axes[0, 2].imshow(sobely, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Sobel Y (Horizontal Edges)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(magnitude, cmap).
    axes[1, 0].imshow(magnitude, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Gradient Magnitude")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(direction, cmap).
    axes[1, 1].imshow(direction, cmap='hsv')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Gradient Direction")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Combined visualization
    # Keterangan: Inisialisasi atau perbarui variabel combined.
    combined = cv2.addWeighted(gray, 0.5, magnitude, 0.5, 0)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(combined, cmap).
    axes[1, 2].imshow(combined, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Original + Edges")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi atau perbarui variabel plt.suptitle(f"Sobel Edge Detection (ksize.
    plt.suptitle(f"Sobel Edge Detection (ksize={SOBEL_KSIZE})", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_edge_operators_comparison.
def demo_edge_operators_comparison():
    """
    Perbandingan berbagai edge operators
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PERBANDINGAN EDGE OPERATORS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
SOBEL:
├── Smooth derivative menggunakan weighted kernel
├── Lebih noise-resistant dari Prewitt
└── Standar untuk kebanyakan aplikasi

SCHARR:
├── Optimized untuk kernel 3×3
├── Lebih akurat untuk sudut tertentu
└── Gunakan jika butuh presisi lebih

PREWITT:
├── Simple equal-weighted kernel
├── Lebih sensitive terhadap noise
└── Faster computation

LAPLACIAN:
├── Second derivative (mendeteksi rate of change)
├── Tidak memberikan informasi direction
└── Sensitive terhadap noise
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = buat_gambar_sample()
    
    # Keterangan: Inisialisasi atau perbarui variabel gray.
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Compute edges dengan berbagai operator
    # Keterangan: Inisialisasi atau perbarui variabel sobel.
    sobel = sobel_magnitude(gray, SOBEL_KSIZE)
    # Keterangan: Inisialisasi atau perbarui variabel scharr.
    scharr = scharr_edge(gray)
    # Keterangan: Inisialisasi atau perbarui variabel prewitt.
    prewitt = prewitt_edge(gray)
    # Keterangan: Inisialisasi atau perbarui variabel laplacian.
    laplacian = laplacian_edge(gray, LAPLACIAN_KSIZE)
    # Keterangan: Inisialisasi atau perbarui variabel log.
    log = laplacian_of_gaussian(gray)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gray, cmap).
    axes[0, 0].imshow(gray, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(sobel, cmap).
    axes[0, 1].imshow(sobel, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Sobel")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(scharr, cmap).
    axes[0, 2].imshow(scharr, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Scharr")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(prewitt, cmap).
    axes[1, 0].imshow(prewitt, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Prewitt")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(laplacian, cmap).
    axes[1, 1].imshow(laplacian, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Laplacian")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(log, cmap).
    axes[1, 2].imshow(log, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Laplacian of Gaussian")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Edge Detection Operators", fontsize).
    plt.suptitle("Perbandingan Edge Detection Operators", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_canny_edge.
def demo_canny_edge():
    """
    Demonstrasi Canny Edge Detection
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("CANNY EDGE DETECTION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
CANNY adalah multi-stage edge detection algorithm:

1. GAUSSIAN SMOOTHING
   └── Reduce noise (built-in dalam cv2.Canny)

2. GRADIENT COMPUTATION
   └── Sobel untuk magnitude dan direction

3. NON-MAXIMUM SUPPRESSION
   └── Thin edges ke 1-pixel width
   └── Hanya keep pixel dengan gradient maksimum lokal

4. DOUBLE THRESHOLDING
   └── Strong edge: gradient > high_threshold
   └── Weak edge: low_threshold < gradient < high_threshold

5. EDGE TRACKING BY HYSTERESIS
   └── Weak edges keep jika connect ke strong edge
   └── Otherwise, discard weak edges
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = buat_gambar_sample()
    
    # Keterangan: Inisialisasi atau perbarui variabel gray.
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Canny dengan parameter berbeda
    # Keterangan: Inisialisasi atau perbarui variabel canny_default.
    canny_default = canny_edge(gray, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
    # Keterangan: Inisialisasi atau perbarui variabel canny_strict.
    canny_strict = canny_edge(gray, 100, 200)  # Lebih sedikit edges
    # Keterangan: Inisialisasi atau perbarui variabel canny_loose.
    canny_loose = canny_edge(gray, 30, 100)    # Lebih banyak edges
    # Keterangan: Inisialisasi beberapa variabel (auto, low, high).
    auto, low, high = auto_canny(gray)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gray, cmap).
    axes[0, 0].imshow(gray, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(canny_default, cmap).
    axes[0, 1].imshow(canny_default, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title(f"Canny (low).
    axes[0, 1].set_title(f"Canny (low={CANNY_LOW_THRESHOLD}, high={CANNY_HIGH_THRESHOLD})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(auto, cmap).
    axes[0, 2].imshow(auto, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"Auto Canny (low).
    axes[0, 2].set_title(f"Auto Canny (low={low}, high={high})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(canny_loose, cmap).
    axes[1, 0].imshow(canny_loose, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].set_title("Loose (low).
    axes[1, 0].set_title("Loose (low=30, high=100)\nMore edges")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(canny_strict, cmap).
    axes[1, 1].imshow(canny_strict, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].set_title("Strict (low).
    axes[1, 1].set_title("Strict (low=100, high=200)\nFewer edges")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Overlay edges on original
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Konversi ruang warna gambar.
        gambar_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    # Keterangan: Inisialisasi atau perbarui variabel gambar_rgb[canny_default > 0].
    gambar_rgb[canny_default > 0] = [255, 0, 0]  # Red edges
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].imshow(gambar_rgb)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Edges Overlay (Red)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Canny Edge Detection", fontsize).
    plt.suptitle("Canny Edge Detection", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_threshold_tuning.
def demo_threshold_tuning():
    """
    Demonstrasi tuning threshold untuk Canny
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("THRESHOLD TUNING UNTUK CANNY")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
RATIO GUIDELINE:
├── Recommended: high/low ratio antara 2:1 sampai 3:1
├── Example: low=50, high=150 (ratio 3:1)
└── Adjust berdasarkan image content

LOW THRESHOLD:
├── Nilai kecil: lebih banyak weak edges terdeteksi
└── Nilai besar: hanya strong edges yang terdeteksi

HIGH THRESHOLD:
├── Menentukan minimum gradient untuk strong edge
└── Strong edges pasti di-keep
└── Weak edges hanya di-keep jika connect ke strong edge
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = buat_gambar_sample()
    
    # Keterangan: Inisialisasi atau perbarui variabel gray.
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Variasi threshold
    # Keterangan: Inisialisasi atau perbarui variabel low_thresholds.
    low_thresholds = [25, 50, 100]
    # Keterangan: Inisialisasi atau perbarui variabel high_thresholds.
    high_thresholds = [50, 100, 150, 200]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(len(low_thresholds), len(high_thresholds), 
                              # Keterangan: Inisialisasi atau perbarui variabel figsize.
                              figsize=(16, 12))
    
    # Keterangan: Mulai loop dengan for i, low in enumerate(low_thresholds).
    for i, low in enumerate(low_thresholds):
        # Keterangan: Mulai loop dengan for j, high in enumerate(high_thresholds).
        for j, high in enumerate(high_thresholds):
            # Keterangan: Cek kondisi low < high.
            if low < high:
                # Keterangan: Inisialisasi atau perbarui variabel edges.
                edges = canny_edge(gray, low, high)
                # Keterangan: Inisialisasi beberapa variabel (axes[i, j].imshow(edges, cmap).
                axes[i, j].imshow(edges, cmap='gray')
                # Keterangan: Inisialisasi beberapa variabel (axes[i, j].set_title(f"Low).
                axes[i, j].set_title(f"Low={low}, High={high}")
            # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
            else:
                # Keterangan: Inisialisasi array bernilai nol.
                axes[i, j].imshow(np.zeros_like(gray), cmap='gray')
                # Keterangan: Jalankan perintah berikut.
                axes[i, j].set_title(f"Invalid (low≥high)")
            # Keterangan: Jalankan perintah berikut.
            axes[i, j].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Pengaruh Threshold pada Canny Edge Detection", fontsize).
    plt.suptitle("Pengaruh Threshold pada Canny Edge Detection", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

# Keterangan: Definisikan fungsi main.
def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: EDGE DETECTION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
EDGE DETECTION adalah teknik fundamental untuk menemukan
# Keterangan: Jalankan perintah berikut.
batas-batas objek dalam gambar dengan mendeteksi diskontinuitas
# Keterangan: Jalankan perintah berikut.
intensitas.

# Keterangan: Mulai blok kode baru.
Aplikasi:
# Keterangan: Jalankan perintah berikut.
├── Object detection & recognition
# Keterangan: Jalankan perintah berikut.
├── Image segmentation
# Keterangan: Jalankan perintah berikut.
├── Lane detection (self-driving cars)
# Keterangan: Jalankan perintah berikut.
├── Document scanning
# Keterangan: Jalankan perintah berikut.
├── Medical image analysis
# Keterangan: Jalankan perintah berikut.
└── Feature extraction untuk computer vision
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        print("[INFO] Membuat gambar sample...")
        gray = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gray.shape}")
    print(f"[INFO] Sobel Kernel Size: {SOBEL_KSIZE}")
    print(f"[INFO] Canny Thresholds: low={CANNY_LOW_THRESHOLD}, high={CANNY_HIGH_THRESHOLD}")
    print(f"[INFO] Blur Kernel Size: {BLUR_KERNEL_SIZE}")
    
    # Preprocess
    preprocessed = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Apply edge detection
    sobel_result = sobel_magnitude(preprocessed, SOBEL_KSIZE)
    canny_result = canny_edge(preprocessed, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(gray, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(sobel_result, cmap='gray')
    axes[1].set_title("Sobel Magnitude")
    axes[1].axis('off')
    
    axes[2].imshow(canny_result, cmap='gray')
    axes[2].set_title("Canny Edges")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_edge_detection_concept()
    demo_sobel_operator()
    demo_edge_operators_comparison()
    demo_canny_edge()
    demo_threshold_tuning()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN EDGE DETECTION")
    print("=" * 60)
    print("""
# Keterangan: Mulai blok kode baru.
FUNGSI OPENCV:

# SOBEL
# Keterangan: Hitung gradien Sobel untuk deteksi tepi.
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # Gradient X
# Keterangan: Hitung gradien Sobel untuk deteksi tepi.
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Gradient Y
# Keterangan: Inisialisasi atau perbarui variabel magnitude.
magnitude = np.sqrt(sobelx**2 + sobely**2)

# SCHARR (lebih akurat untuk 3x3)
# Keterangan: Inisialisasi atau perbarui variabel scharrx.
scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
# Keterangan: Inisialisasi atau perbarui variabel scharry.
scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)

# LAPLACIAN
# Keterangan: Hitung Laplacian untuk deteksi tepi.
laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)

# CANNY (paling populer)
# Keterangan: Inisialisasi atau perbarui variabel edges.
edges = cv2.Canny(gray, low_threshold, high_threshold)
# Keterangan: Inisialisasi atau perbarui variabel edges.
edges = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=True)

# Keterangan: Mulai blok kode baru.
PEMILIHAN OPERATOR:
# Keterangan: Jalankan perintah berikut.
├── Canny: pilihan default, hasil terbaik untuk kebanyakan kasus
# Keterangan: Jalankan perintah berikut.
├── Sobel: jika butuh gradient magnitude & direction
# Keterangan: Jalankan perintah berikut.
├── Laplacian: untuk deteksi blob atau jika tidak butuh direction
# Keterangan: Jalankan perintah berikut.
└── Scharr: jika butuh presisi lebih dengan kernel 3×3

# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
1. Selalu preprocessing dengan blur untuk reduce noise
# Keterangan: Jalankan perintah berikut.
2. Untuk Canny: mulai dengan ratio 3:1 (low:high)
# Keterangan: Jalankan perintah berikut.
3. Auto Canny: gunakan median intensity untuk threshold otomatis
# Keterangan: Jalankan perintah berikut.
4. Combine multiple operators untuk hasil lebih robust
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
