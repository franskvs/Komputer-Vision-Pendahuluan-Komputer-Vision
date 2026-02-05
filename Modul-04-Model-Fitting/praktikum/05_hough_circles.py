# ============================================================
# PROGRAM: 05_hough_circles.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk Hough Circle Transform
# 
# Tujuan Pembelajaran:
#   1. Memahami Hough Transform untuk deteksi lingkaran
#   2. Tuning parameter HoughCircles
#   3. Aplikasi deteksi objek bulat
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

# 1. File gambar
NAMA_FILE_GAMBAR = "coins.jpg"

# 2. Parameter preprocessing
BLUR_KERNEL = 9          # Kernel size untuk Gaussian blur (harus ganjil)

# 3. Parameter Hough Circle Transform
METHOD = cv2.HOUGH_GRADIENT  # Metode (HOUGH_GRADIENT atau HOUGH_GRADIENT_ALT)
DP = 1.0                  # Inverse ratio of accumulator resolution
MIN_DIST = 30             # Minimum distance between circle centers
PARAM1 = 50               # Higher threshold untuk Canny (internal)
PARAM2 = 30               # Accumulator threshold
MIN_RADIUS = 10           # Minimum radius lingkaran
MAX_RADIUS = 100          # Maximum radius lingkaran (0 = no max)

# 4. Warna visualisasi
CIRCLE_COLOR = (0, 255, 0)   # Hijau untuk lingkaran
CENTER_COLOR = (255, 0, 0)   # Biru untuk center
CIRCLE_THICKNESS = 2

# 5. Auto-close plot (detik)
AUTO_CLOSE_SECONDS = 2.0

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
    """Membuat gambar sample dengan lingkaran"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    gambar[:, :] = [40, 40, 40]  # Dark background
    
    # Lingkaran dengan berbagai ukuran
    cv2.circle(gambar, (100, 100), 40, (255, 255, 255), 2)
    cv2.circle(gambar, (250, 150), 60, (200, 200, 200), -1)  # Filled
    cv2.circle(gambar, (450, 100), 35, (255, 255, 255), 3)
    cv2.circle(gambar, (150, 280), 50, (180, 180, 180), -1)
    cv2.circle(gambar, (350, 300), 45, (255, 255, 255), 2)
    cv2.circle(gambar, (500, 280), 55, (220, 220, 220), -1)
    
    # Lingkaran kecil (coins-like)
    for i in range(3):
        x = 200 + i * 80
        y = 350
        cv2.circle(gambar, (x, y), 25, (255, 255, 255), -1)
    
    # Noise
    noise = np.random.randint(0, 30, gambar.shape, dtype=np.uint8)
    gambar = cv2.add(gambar, noise)
    
    return gambar


def tampilkan_plot():
    """Tampilkan plot sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(AUTO_CLOSE_SECONDS)
    plt.close()


# ============================================================
# FUNGSI HOUGH CIRCLE
# ============================================================

def detect_circles(gambar, dp=1.0, min_dist=30, param1=50, param2=30,
                   min_radius=10, max_radius=100):
    """
    Hough Circle Transform
    
    Mendeteksi lingkaran dalam gambar menggunakan
    gradient-based Hough Transform.
    
    Parameter:
    - dp: inverse ratio of accumulator resolution
          dp=1 → accumulator sama dengan gambar
          dp=2 → accumulator setengah resolusi
    - min_dist: minimum distance antara center lingkaran
    - param1: higher Canny threshold (lower = param1/2)
    - param2: accumulator threshold untuk center detection
              semakin kecil → lebih banyak lingkaran
    - min_radius, max_radius: batas radius
    
    Return:
    - circles: array of (x, y, radius)
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Apply Gaussian blur untuk noise reduction
    blurred = cv2.GaussianBlur(gray, (BLUR_KERNEL, BLUR_KERNEL), 0)
    
    # Hough Circle Transform
    circles = cv2.HoughCircles(
        blurred,
        METHOD,
        dp=dp,
        minDist=min_dist,
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )
    
    return circles


def draw_circles(gambar, circles):
    """
    Draw detected circles pada gambar
    
    Return:
    - output: gambar dengan circles
    """
    output = gambar.copy()
    
    if circles is None:
        return output
    
    circles = np.uint16(np.around(circles))
    
    for circle in circles[0, :]:
        x, y, r = circle
        
        # Draw circle outline
        cv2.circle(output, (x, y), r, CIRCLE_COLOR, CIRCLE_THICKNESS)
        
        # Draw center point
        cv2.circle(output, (x, y), 3, CENTER_COLOR, -1)
        
        # Draw radius line
        cv2.line(output, (x, y), (x + r, y), CENTER_COLOR, 1)
    
    return output


def analyze_circles(circles):
    """Analisis lingkaran yang terdeteksi"""
    if circles is None:
        return None
    
    circles = circles[0]
    
    radii = circles[:, 2]
    
    analysis = {
        'count': len(circles),
        'min_radius': np.min(radii),
        'max_radius': np.max(radii),
        'mean_radius': np.mean(radii),
        'std_radius': np.std(radii)
    }
    
    return analysis


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_param2_effect():
    """Demonstrasi pengaruh param2 (accumulator threshold)"""
    print("\n" + "=" * 60)
    print("PENGARUH PARAM2 (ACCUMULATOR THRESHOLD)")
    print("=" * 60)
    
    print("""
PARAM2:

Parameter ini mengontrol sensitivitas deteksi.
Semakin kecil → lebih banyak lingkaran terdeteksi.
Semakin besar → hanya lingkaran yang jelas.

Nilai terlalu rendah: banyak false positives
Nilai terlalu tinggi: miss beberapa lingkaran
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    param2_values = [20, 30, 50, 80]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, p2 in enumerate(param2_values):
        circles = detect_circles(gambar, param2=p2)
        output = draw_circles(gambar, circles)
        n = circles.shape[1] if circles is not None else 0
        
        axes[i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"param2 = {p2}\n{n} circles detected")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh param2 pada Hough Circle Detection", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_min_dist_effect():
    """Demonstrasi pengaruh minDist"""
    print("\n" + "=" * 60)
    print("PENGARUH MIN_DIST")
    print("=" * 60)
    
    print("""
MIN_DIST:

Minimum distance antara center dari lingkaran yang terdeteksi.

minDist kecil:
├── Lingkaran yang berdekatan bisa terdeteksi
└── Risiko multiple detections untuk satu lingkaran

minDist besar:
├── Hanya lingkaran yang berjauhan
└── Mungkin miss lingkaran yang berdekatan
    """)
    
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    min_dist_values = [10, 30, 60, 100]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, md in enumerate(min_dist_values):
        circles = detect_circles(gambar, min_dist=md)
        output = draw_circles(gambar, circles)
        n = circles.shape[1] if circles is not None else 0
        
        axes[i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"minDist = {md}\n{n} circles detected")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh minDist pada Hough Circle Detection", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_radius_constraints():
    """Demonstrasi pengaruh radius constraints"""
    print("\n" + "=" * 60)
    print("PENGARUH RADIUS CONSTRAINTS")
    print("=" * 60)
    
    print("""
MIN_RADIUS dan MAX_RADIUS:

Membatasi ukuran lingkaran yang dicari.
Berguna untuk filtering berdasarkan ukuran objek yang diharapkan.

Contoh aplikasi:
├── Coin detection: radius 20-40
├── Eye detection: radius 10-30
└── Ball detection: tergantung jarak
    """)
    
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    radius_ranges = [
        (5, 30, "Small circles (5-30)"),
        (30, 60, "Medium circles (30-60)"),
        (60, 100, "Large circles (60-100)"),
        (5, 100, "All circles (5-100)")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, (min_r, max_r, desc) in enumerate(radius_ranges):
        circles = detect_circles(gambar, min_radius=min_r, max_radius=max_r)
        output = draw_circles(gambar, circles)
        n = circles.shape[1] if circles is not None else 0
        
        axes[i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{desc}\n{n} circles detected")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh Radius Constraints", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_preprocessing_effect():
    """Demonstrasi pengaruh preprocessing"""
    print("\n" + "=" * 60)
    print("PENGARUH PREPROCESSING (BLUR)")
    print("=" * 60)
    
    print("""
GAUSSIAN BLUR:

Blur diperlukan untuk mengurangi noise dan false edges.
Tapi blur terlalu banyak bisa menghilangkan detail lingkaran kecil.

Kernel size:
├── Kecil (3-5): detail preserved, lebih noise
├── Sedang (7-11): balance bagus
└── Besar (13+): smooth tapi kehilangan detail
    """)
    
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    kernel_sizes = [3, 7, 11, 21]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    for i, ks in enumerate(kernel_sizes):
        blurred = cv2.GaussianBlur(gray, (ks, ks), 0)
        
        circles = cv2.HoughCircles(
            blurred, METHOD, dp=DP, minDist=MIN_DIST,
            param1=PARAM1, param2=PARAM2,
            minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS
        )
        
        output = draw_circles(gambar, circles)
        n = circles.shape[1] if circles is not None else 0
        
        axes[0, i].imshow(blurred, cmap='gray')
        axes[0, i].set_title(f"Blur kernel={ks}")
        axes[0, i].axis('off')
        
        axes[1, i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f"{n} circles")
        axes[1, i].axis('off')
    
    plt.suptitle("Pengaruh Blur Preprocessing pada Circle Detection", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: HOUGH CIRCLE TRANSFORM")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
HOUGH CIRCLE TRANSFORM mendeteksi lingkaran dalam gambar.

REPRESENTASI LINGKARAN:
    (x - a)² + (y - b)² = r²

Dimana:
├── (a, b): center lingkaran
└── r: radius

ALGORITMA (HOUGH_GRADIENT):
1. Detect edges menggunakan Canny
2. Untuk setiap edge point, vote untuk possible centers
   berdasarkan gradient direction
3. Find peaks di accumulator (centers)
4. Untuk setiap center, cari radius terbaik

PARAMETER PENTING:

dp: Inverse ratio of accumulator resolution
├── dp=1: resolusi sama dengan gambar
└── dp=2: resolusi setengah (lebih cepat, kurang akurat)

minDist: Minimum distance antara circle centers
├── Terlalu kecil: multiple detections
└── Terlalu besar: miss circles yang berdekatan

param1: Higher Canny threshold
└── param2 = param1/2 digunakan sebagai lower threshold

param2: Accumulator threshold
├── Lebih kecil: lebih sensitif, lebih banyak deteksi
└── Lebih besar: hanya lingkaran yang jelas

APLIKASI:
├── Coin detection dan counting
├── Eye detection (iris)
├── Cell detection dalam biologi
├── Ball/puck tracking dalam sports
└── Wheel detection
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Membuat gambar sample...")
        gambar = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    
    # Print parameters
    print("\n[PARAMETERS]")
    print(f"   dp: {DP}")
    print(f"   minDist: {MIN_DIST}")
    print(f"   param1: {PARAM1}")
    print(f"   param2: {PARAM2}")
    print(f"   minRadius: {MIN_RADIUS}")
    print(f"   maxRadius: {MAX_RADIUS}")
    
    # Detect circles
    print("\n[STEP 1] Preprocessing...")
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (BLUR_KERNEL, BLUR_KERNEL), 0)
    print(f"   Gaussian blur kernel: {BLUR_KERNEL}")
    
    print("\n[STEP 2] Hough Circle Transform...")
    circles = detect_circles(gambar, DP, MIN_DIST, PARAM1, PARAM2,
                             MIN_RADIUS, MAX_RADIUS)
    
    if circles is not None:
        n_circles = circles.shape[1]
        print(f"   Detected: {n_circles} circles")
        
        analysis = analyze_circles(circles)
        print(f"\n[ANALYSIS]")
        print(f"   Min radius: {analysis['min_radius']:.1f}")
        print(f"   Max radius: {analysis['max_radius']:.1f}")
        print(f"   Mean radius: {analysis['mean_radius']:.1f}")
        print(f"   Std radius: {analysis['std_radius']:.1f}")
        
        # Print each circle
        print(f"\n[DETECTED CIRCLES]")
        for i, circle in enumerate(circles[0]):
            x, y, r = circle
            print(f"   {i+1}. Center=({x}, {y}), Radius={r}")
    else:
        print("   No circles detected!")
    
    # Visualisasi
    print("\n[STEP 3] Visualisasi...")
    
    output = draw_circles(gambar, circles)
    edges = cv2.Canny(blurred, PARAM1//2, PARAM1)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(blurred, cmap='gray')
    axes[0, 1].set_title("Blurred Grayscale")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(edges, cmap='gray')
    axes[1, 0].set_title("Canny Edges (internal)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    n = circles.shape[1] if circles is not None else 0
    axes[1, 1].set_title(f"Detected Circles: {n}")
    axes[1, 1].axis('off')
    
    plt.suptitle("Hough Circle Transform", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()
    
    # Demo tambahan
    demo_param2_effect()
    demo_min_dist_effect()
    demo_radius_constraints()
    demo_preprocessing_effect()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN HOUGH CIRCLE TRANSFORM")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Preprocessing
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 0)

# Hough Circle Detection
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,      # Method
    dp=1,                     # Accumulator resolution
    minDist=30,              # Min distance between centers
    param1=50,               # Canny higher threshold
    param2=30,               # Accumulator threshold
    minRadius=10,            # Minimum radius
    maxRadius=100            # Maximum radius (0 = no limit)
)

# Draw circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for x, y, r in circles[0]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)
        cv2.circle(output, (x, y), 2, (0, 0, 255), -1)

TIPS PARAMETER TUNING:

1. Start dengan param2 yang tinggi, turunkan perlahan
2. Sesuaikan minDist dengan expected spacing
3. Set radius constraints berdasarkan expected object size
4. Gunakan blur yang cukup untuk mengurangi noise
5. param1 biasanya 50-200 untuk Canny edge detection

ALTERNATIF METHOD (OpenCV 4.3+):
- HOUGH_GRADIENT_ALT: lebih akurat untuk lingkaran
  dengan contrast rendah, tapi lebih lambat
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
