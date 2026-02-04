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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Sobel kernel size
# Opsi: 1, 3, 5, 7 (default: 3)
SOBEL_KSIZE = 3

# 3. Canny thresholds
# Low threshold: untuk edge linking (nilai kecil = lebih banyak edges)
# High threshold: untuk edge detection (nilai besar = hanya strong edges)
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150

# 4. Gaussian blur sebelum edge detection
# Untuk mengurangi noise (0 = tidak pakai blur)
BLUR_KERNEL_SIZE = 5

# 5. Laplacian kernel size (harus ganjil)
LAPLACIAN_KSIZE = 3

# ============================================================
# FUNGSI HELPER
# ============================================================

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
    gambar = np.zeros((400, 600), dtype=np.uint8)
    
    # Background gradient
    for i in range(400):
        gambar[i, :300] = 50
        gambar[i, 300:] = 200
    
    # Shapes dengan berbagai intensitas
    cv2.rectangle(gambar, (50, 50), (200, 150), 255, -1)
    cv2.circle(gambar, (400, 100), 60, 180, -1)
    cv2.fillPoly(gambar, [np.array([[250, 300], [350, 200], [450, 300]])], 255)
    
    # Text
    cv2.putText(gambar, "EDGE", (200, 380), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255, 2)
    
    return gambar


def preprocess_gambar(gambar, blur_ksize=5):
    """
    Preprocessing gambar sebelum edge detection
    
    Langkah:
    1. Convert ke grayscale (jika berwarna)
    2. Apply Gaussian blur untuk reduce noise
    """
    # Convert ke grayscale jika perlu
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Apply blur jika diminta
    if blur_ksize > 0:
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    
    return gray


# ============================================================
# FUNGSI EDGE DETECTION - FIRST DERIVATIVE
# ============================================================

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
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    
    # Convert ke absolute value
    sobelx_abs = np.absolute(sobelx)
    sobelx_8u = np.uint8(sobelx_abs / sobelx_abs.max() * 255)
    
    return sobelx_8u


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
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    sobely_abs = np.absolute(sobely)
    sobely_8u = np.uint8(sobely_abs / sobely_abs.max() * 255)
    
    return sobely_8u


def sobel_magnitude(gambar, ksize=3):
    """
    Magnitude dari gradient Sobel
    
    magnitude = sqrt(Gx² + Gy²)
    
    Mendeteksi edges di semua arah
    """
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    return magnitude


def sobel_direction(gambar, ksize=3):
    """
    Arah (direction) dari gradient Sobel
    
    direction = arctan(Gy / Gx)
    
    Berguna untuk mengetahui orientasi edge
    """
    sobelx = cv2.Sobel(gambar, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gambar, cv2.CV_64F, 0, 1, ksize=ksize)
    
    direction = np.arctan2(sobely, sobelx) * 180 / np.pi
    
    return direction


def scharr_edge(gambar):
    """
    Scharr operator
    
    Lebih akurat dari Sobel untuk kernel 3x3
    
    Kernel Scharr X:
    [-3   0   3]
    [-10  0  10]
    [-3   0   3]
    """
    scharrx = cv2.Scharr(gambar, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(gambar, cv2.CV_64F, 0, 1)
    
    magnitude = np.sqrt(scharrx**2 + scharry**2)
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    return magnitude


def prewitt_edge(gambar):
    """
    Prewitt operator (implementasi manual)
    
    Lebih simple dari Sobel
    
    Kernel Prewitt X:
    [-1  0  1]
    [-1  0  1]
    [-1  0  1]
    """
    kernel_x = np.array([[-1, 0, 1],
                         [-1, 0, 1],
                         [-1, 0, 1]], dtype=np.float64)
    
    kernel_y = np.array([[-1, -1, -1],
                         [0, 0, 0],
                         [1, 1, 1]], dtype=np.float64)
    
    prewitt_x = cv2.filter2D(gambar.astype(np.float64), -1, kernel_x)
    prewitt_y = cv2.filter2D(gambar.astype(np.float64), -1, kernel_y)
    
    magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    
    return magnitude


# ============================================================
# FUNGSI EDGE DETECTION - SECOND DERIVATIVE
# ============================================================

def laplacian_edge(gambar, ksize=3):
    """
    Laplacian operator (second derivative)
    
    Mendeteksi area dengan perubahan intensitas cepat
    
    Kernel Laplacian (ksize=1):
    [0   1  0]
    [1  -4  1]
    [0   1  0]
    """
    laplacian = cv2.Laplacian(gambar, cv2.CV_64F, ksize=ksize)
    
    laplacian_abs = np.absolute(laplacian)
    laplacian_8u = np.uint8(laplacian_abs / laplacian_abs.max() * 255)
    
    return laplacian_8u


def laplacian_of_gaussian(gambar, sigma=1.0, ksize=5):
    """
    Laplacian of Gaussian (LoG)
    
    Langkah:
    1. Apply Gaussian blur (smoothing)
    2. Apply Laplacian (edge detection)
    
    Ini mengurangi noise sensitivity dari Laplacian biasa
    """
    # Gaussian blur
    blurred = cv2.GaussianBlur(gambar, (ksize, ksize), sigma)
    
    # Laplacian
    log = cv2.Laplacian(blurred, cv2.CV_64F)
    
    log_abs = np.absolute(log)
    log_8u = np.uint8(log_abs / log_abs.max() * 255)
    
    return log_8u


# ============================================================
# FUNGSI EDGE DETECTION - CANNY
# ============================================================

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
    edges = cv2.Canny(gambar, low_threshold, high_threshold)
    return edges


def canny_edge_with_aperture(gambar, low_threshold=50, high_threshold=150, 
                             aperture_size=3, L2gradient=False):
    """
    Canny dengan parameter tambahan
    
    Parameter:
    - aperture_size: ukuran kernel Sobel (3, 5, atau 7)
    - L2gradient: jika True, gunakan L2 norm (lebih akurat)
                  jika False, gunakan L1 norm (lebih cepat)
    """
    edges = cv2.Canny(gambar, low_threshold, high_threshold, 
                      apertureSize=aperture_size, L2gradient=L2gradient)
    return edges


def auto_canny(gambar, sigma=0.33):
    """
    Automatic Canny threshold selection
    
    Menghitung threshold secara otomatis berdasarkan
    median intensitas gambar
    """
    # Hitung median
    v = np.median(gambar)
    
    # Hitung thresholds
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    
    edges = cv2.Canny(gambar, lower, upper)
    
    return edges, lower, upper


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_edge_detection_concept():
    """
    Demonstrasi konsep edge detection
    """
    print("\n" + "=" * 60)
    print("KONSEP EDGE DETECTION")
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
    x = np.linspace(0, 10, 200)
    # Step function (edge)
    signal = np.where(x < 5, 50, 200)
    # Add transition
    signal[(x >= 4.5) & (x <= 5.5)] = 50 + (200-50) * (x[(x >= 4.5) & (x <= 5.5)] - 4.5)
    
    # Compute derivatives
    first_deriv = np.gradient(signal)
    second_deriv = np.gradient(first_deriv)
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    axes[0].plot(x, signal, 'b-', linewidth=2)
    axes[0].set_title("1D Signal (Step Function / Edge)")
    axes[0].set_ylabel("Intensity")
    axes[0].grid(True)
    
    axes[1].plot(x, first_deriv, 'r-', linewidth=2)
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    axes[1].set_title("First Derivative (Gradient)\nEdge = Peak lokasi")
    axes[1].set_ylabel("Gradient")
    axes[1].grid(True)
    
    axes[2].plot(x, second_deriv, 'g-', linewidth=2)
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    axes[2].set_title("Second Derivative (Laplacian)\nEdge = Zero crossing")
    axes[2].set_ylabel("Laplacian")
    axes[2].set_xlabel("Position")
    axes[2].grid(True)
    
    plt.suptitle("Konsep Edge Detection: Derivative", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_sobel_operator():
    """
    Demonstrasi Sobel operator
    """
    print("\n" + "=" * 60)
    print("SOBEL OPERATOR")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = buat_gambar_sample()
    
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Hitung Sobel
    sobelx = sobel_x(gray, SOBEL_KSIZE)
    sobely = sobel_y(gray, SOBEL_KSIZE)
    magnitude = sobel_magnitude(gray, SOBEL_KSIZE)
    direction = sobel_direction(gray, SOBEL_KSIZE)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(gray, cmap='gray')
    axes[0, 0].set_title("Original (Grayscale)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(sobelx, cmap='gray')
    axes[0, 1].set_title("Sobel X (Vertical Edges)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(sobely, cmap='gray')
    axes[0, 2].set_title("Sobel Y (Horizontal Edges)")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(magnitude, cmap='gray')
    axes[1, 0].set_title("Gradient Magnitude")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(direction, cmap='hsv')
    axes[1, 1].set_title("Gradient Direction")
    axes[1, 1].axis('off')
    
    # Combined visualization
    combined = cv2.addWeighted(gray, 0.5, magnitude, 0.5, 0)
    axes[1, 2].imshow(combined, cmap='gray')
    axes[1, 2].set_title("Original + Edges")
    axes[1, 2].axis('off')
    
    plt.suptitle(f"Sobel Edge Detection (ksize={SOBEL_KSIZE})", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_edge_operators_comparison():
    """
    Perbandingan berbagai edge operators
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN EDGE OPERATORS")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = buat_gambar_sample()
    
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Compute edges dengan berbagai operator
    sobel = sobel_magnitude(gray, SOBEL_KSIZE)
    scharr = scharr_edge(gray)
    prewitt = prewitt_edge(gray)
    laplacian = laplacian_edge(gray, LAPLACIAN_KSIZE)
    log = laplacian_of_gaussian(gray)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(gray, cmap='gray')
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(sobel, cmap='gray')
    axes[0, 1].set_title("Sobel")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(scharr, cmap='gray')
    axes[0, 2].set_title("Scharr")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(prewitt, cmap='gray')
    axes[1, 0].set_title("Prewitt")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(laplacian, cmap='gray')
    axes[1, 1].set_title("Laplacian")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(log, cmap='gray')
    axes[1, 2].set_title("Laplacian of Gaussian")
    axes[1, 2].axis('off')
    
    plt.suptitle("Perbandingan Edge Detection Operators", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_canny_edge():
    """
    Demonstrasi Canny Edge Detection
    """
    print("\n" + "=" * 60)
    print("CANNY EDGE DETECTION")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = buat_gambar_sample()
    
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Canny dengan parameter berbeda
    canny_default = canny_edge(gray, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
    canny_strict = canny_edge(gray, 100, 200)  # Lebih sedikit edges
    canny_loose = canny_edge(gray, 30, 100)    # Lebih banyak edges
    auto, low, high = auto_canny(gray)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(gray, cmap='gray')
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(canny_default, cmap='gray')
    axes[0, 1].set_title(f"Canny (low={CANNY_LOW_THRESHOLD}, high={CANNY_HIGH_THRESHOLD})")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(auto, cmap='gray')
    axes[0, 2].set_title(f"Auto Canny (low={low}, high={high})")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(canny_loose, cmap='gray')
    axes[1, 0].set_title("Loose (low=30, high=100)\nMore edges")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(canny_strict, cmap='gray')
    axes[1, 1].set_title("Strict (low=100, high=200)\nFewer edges")
    axes[1, 1].axis('off')
    
    # Overlay edges on original
    if len(gambar.shape) == 3:
        gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
    else:
        gambar_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    gambar_rgb[canny_default > 0] = [255, 0, 0]  # Red edges
    axes[1, 2].imshow(gambar_rgb)
    axes[1, 2].set_title("Edges Overlay (Red)")
    axes[1, 2].axis('off')
    
    plt.suptitle("Canny Edge Detection", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_threshold_tuning():
    """
    Demonstrasi tuning threshold untuk Canny
    """
    print("\n" + "=" * 60)
    print("THRESHOLD TUNING UNTUK CANNY")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = buat_gambar_sample()
    
    gray = preprocess_gambar(gray, BLUR_KERNEL_SIZE)
    
    # Variasi threshold
    low_thresholds = [25, 50, 100]
    high_thresholds = [50, 100, 150, 200]
    
    fig, axes = plt.subplots(len(low_thresholds), len(high_thresholds), 
                              figsize=(16, 12))
    
    for i, low in enumerate(low_thresholds):
        for j, high in enumerate(high_thresholds):
            if low < high:
                edges = canny_edge(gray, low, high)
                axes[i, j].imshow(edges, cmap='gray')
                axes[i, j].set_title(f"Low={low}, High={high}")
            else:
                axes[i, j].imshow(np.zeros_like(gray), cmap='gray')
                axes[i, j].set_title(f"Invalid (low≥high)")
            axes[i, j].axis('off')
    
    plt.suptitle("Pengaruh Threshold pada Canny Edge Detection", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: EDGE DETECTION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
EDGE DETECTION adalah teknik fundamental untuk menemukan
batas-batas objek dalam gambar dengan mendeteksi diskontinuitas
intensitas.

Aplikasi:
├── Object detection & recognition
├── Image segmentation
├── Lane detection (self-driving cars)
├── Document scanning
├── Medical image analysis
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
FUNGSI OPENCV:

# SOBEL
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # Gradient X
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Gradient Y
magnitude = np.sqrt(sobelx**2 + sobely**2)

# SCHARR (lebih akurat untuk 3x3)
scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)

# LAPLACIAN
laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)

# CANNY (paling populer)
edges = cv2.Canny(gray, low_threshold, high_threshold)
edges = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=True)

PEMILIHAN OPERATOR:
├── Canny: pilihan default, hasil terbaik untuk kebanyakan kasus
├── Sobel: jika butuh gradient magnitude & direction
├── Laplacian: untuk deteksi blob atau jika tidak butuh direction
└── Scharr: jika butuh presisi lebih dengan kernel 3×3

TIPS:
1. Selalu preprocessing dengan blur untuk reduce noise
2. Untuk Canny: mulai dengan ratio 3:1 (low:high)
3. Auto Canny: gunakan median intensity untuk threshold otomatis
4. Combine multiple operators untuk hasil lebih robust
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
