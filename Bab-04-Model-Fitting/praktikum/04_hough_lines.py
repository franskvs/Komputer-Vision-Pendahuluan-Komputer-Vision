# ============================================================
# PROGRAM: 04_hough_lines.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk Hough Line Transform
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep Hough Transform untuk deteksi garis
#   2. Perbandingan HoughLines vs HoughLinesP
#   3. Tuning parameter Hough Transform
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
NAMA_FILE_GAMBAR = "road.jpg"

# 2. Pilihan metode
# Opsi: 'standard', 'probabilistic', 'both'
HOUGH_METHOD = 'both'

# 3. Parameter Canny Edge Detection
CANNY_LOW = 50           # Lower threshold
CANNY_HIGH = 150         # Higher threshold

# 4. Parameter Standard Hough Transform (HoughLines)
RHO_RESOLUTION = 1        # Resolusi rho dalam pixels
THETA_RESOLUTION = np.pi/180  # Resolusi theta dalam radians
VOTE_THRESHOLD = 100      # Minimum votes untuk terdeteksi

# 5. Parameter Probabilistic Hough Transform (HoughLinesP)
MIN_LINE_LENGTH = 50      # Minimum panjang garis
MAX_LINE_GAP = 10         # Maximum gap between line segments

# 6. Warna dan ketebalan garis
LINE_COLOR = (0, 255, 0)   # Hijau
LINE_THICKNESS = 2

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    lokasi_potensial = [
        os.path.join(direktori_script, "..", "data", "images", nama_file),
        os.path.join(direktori_script, "..", "..", "Bab-01-Pendahuluan", 
                     "data", "images", nama_file),
        os.path.join(direktori_script, nama_file),
    ]
    
    for path in lokasi_potensial:
        if os.path.exists(path):
            return path
    
    return lokasi_potensial[0]


def buat_gambar_sample():
    """Membuat gambar sample dengan garis-garis"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    gambar[:, :] = [30, 30, 30]  # Dark background
    
    # Horizontal lines
    cv2.line(gambar, (50, 100), (550, 100), (255, 255, 255), 2)
    cv2.line(gambar, (100, 200), (500, 200), (255, 255, 255), 2)
    
    # Vertical lines
    cv2.line(gambar, (150, 50), (150, 350), (255, 255, 255), 2)
    cv2.line(gambar, (450, 50), (450, 350), (255, 255, 255), 2)
    
    # Diagonal lines
    cv2.line(gambar, (200, 50), (400, 350), (255, 255, 255), 2)
    cv2.line(gambar, (400, 50), (200, 350), (255, 255, 255), 2)
    
    # Rectangle
    cv2.rectangle(gambar, (250, 280), (350, 360), (255, 255, 255), 2)
    
    # Noise (some random points)
    for _ in range(100):
        x = np.random.randint(0, 600)
        y = np.random.randint(0, 400)
        gambar[y, x] = [200, 200, 200]
    
    return gambar


# ============================================================
# FUNGSI HOUGH TRANSFORM
# ============================================================

def preprocess_for_hough(gambar):
    """
    Preprocessing gambar untuk Hough Transform
    
    Hough Transform bekerja pada edge image,
    jadi perlu edge detection terlebih dahulu.
    
    Return:
    - edges: binary edge image
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Gaussian blur untuk noise reduction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny edge detection
    edges = cv2.Canny(blurred, CANNY_LOW, CANNY_HIGH)
    
    return edges


def standard_hough_lines(edges, rho, theta, threshold):
    """
    Standard Hough Line Transform (HoughLines)
    
    Representasi garis: r = x*cos(θ) + y*sin(θ)
    Dimana (r, θ) adalah parameter garis dalam polar coordinates.
    
    Parameter:
    - edges: binary edge image
    - rho: resolusi rho dalam pixels
    - theta: resolusi theta dalam radians
    - threshold: minimum votes
    
    Return:
    - lines: array of (rho, theta) untuk setiap garis
    """
    lines = cv2.HoughLines(edges, rho, theta, threshold)
    
    return lines


def probabilistic_hough_lines(edges, rho, theta, threshold, 
                              min_length, max_gap):
    """
    Probabilistic Hough Line Transform (HoughLinesP)
    
    Lebih efisien dari standard Hough.
    Return endpoints dari line segments.
    
    Parameter:
    - edges: binary edge image
    - rho, theta, threshold: sama dengan standard
    - min_length: minimum panjang garis
    - max_gap: maximum gap dalam garis
    
    Return:
    - lines: array of (x1, y1, x2, y2) untuk setiap garis
    """
    lines = cv2.HoughLinesP(edges, rho, theta, threshold,
                            minLineLength=min_length,
                            maxLineGap=max_gap)
    
    return lines


def draw_hough_lines(gambar, lines, method='standard'):
    """
    Draw detected lines pada gambar
    
    Parameter:
    - gambar: input image
    - lines: detected lines
    - method: 'standard' atau 'probabilistic'
    
    Return:
    - output: gambar dengan garis
    """
    output = gambar.copy()
    
    if lines is None:
        return output
    
    if method == 'standard':
        # Standard Hough: (rho, theta)
        for line in lines:
            rho, theta = line[0]
            
            # Convert polar ke Cartesian
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            
            # Extend line ke boundary gambar
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            
            cv2.line(output, (x1, y1), (x2, y2), LINE_COLOR, LINE_THICKNESS)
    else:
        # Probabilistic Hough: (x1, y1, x2, y2)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(output, (x1, y1), (x2, y2), LINE_COLOR, LINE_THICKNESS)
    
    return output


def analyze_detected_lines(lines, method='standard'):
    """Analisis garis yang terdeteksi"""
    if lines is None:
        return None
    
    analysis = {
        'count': len(lines),
        'horizontal': 0,
        'vertical': 0,
        'diagonal': 0
    }
    
    for line in lines:
        if method == 'standard':
            rho, theta = line[0]
            angle = np.degrees(theta)
        else:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angle = (angle + 180) % 180  # Normalize to 0-180
        
        # Classify line orientation
        if 80 <= angle <= 100:  # ~vertical
            analysis['vertical'] += 1
        elif angle <= 10 or angle >= 170:  # ~horizontal
            analysis['horizontal'] += 1
        else:
            analysis['diagonal'] += 1
    
    return analysis


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_threshold_effect():
    """Demonstrasi pengaruh threshold"""
    print("\n" + "=" * 60)
    print("PENGARUH VOTE THRESHOLD")
    print("=" * 60)
    
    print("""
VOTE THRESHOLD:

Setiap edge point "vote" untuk semua garis yang mungkin
melewatinya. Threshold menentukan minimum votes untuk
garis dianggap terdeteksi.

Threshold rendah:
├── Lebih banyak garis terdeteksi
├── Risiko false positives
└── Cocok untuk gambar dengan garis lemah

Threshold tinggi:
├── Hanya garis yang kuat terdeteksi
├── Lebih reliable
└── Mungkin miss garis pendek/lemah
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Preprocess
    edges = preprocess_for_hough(gambar)
    
    thresholds = [50, 100, 150, 200]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, thresh in enumerate(thresholds):
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, thresh,
                                minLineLength=MIN_LINE_LENGTH,
                                maxLineGap=MAX_LINE_GAP)
        
        output = draw_hough_lines(gambar, lines, 'probabilistic')
        n_lines = len(lines) if lines is not None else 0
        
        axes[i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"Threshold = {thresh}\n{n_lines} lines detected")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh Vote Threshold pada Hough Lines", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_minlength_maxgap():
    """Demonstrasi pengaruh minLineLength dan maxLineGap"""
    print("\n" + "=" * 60)
    print("PENGARUH MIN_LINE_LENGTH DAN MAX_LINE_GAP")
    print("=" * 60)
    
    print("""
MIN_LINE_LENGTH:
└── Minimum panjang garis untuk diterima

MAX_LINE_GAP:
└── Maximum gap yang masih dianggap satu garis
    
Contoh:
- minLineLength tinggi → hanya garis panjang
- maxLineGap tinggi → garis putus-putus jadi satu
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    edges = preprocess_for_hough(gambar)
    
    params = [
        (20, 5, "Short lines, small gaps"),
        (20, 30, "Short lines, large gaps"),
        (100, 5, "Long lines, small gaps"),
        (100, 30, "Long lines, large gaps")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, (min_len, max_gap, desc) in enumerate(params):
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, VOTE_THRESHOLD,
                                minLineLength=min_len,
                                maxLineGap=max_gap)
        
        output = draw_hough_lines(gambar, lines, 'probabilistic')
        n_lines = len(lines) if lines is not None else 0
        
        axes[i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"minLen={min_len}, maxGap={max_gap}\n{desc}\n{n_lines} lines")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh minLineLength dan maxLineGap", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_hough_space():
    """Visualisasi Hough Space"""
    print("\n" + "=" * 60)
    print("VISUALISASI HOUGH SPACE")
    print("=" * 60)
    
    print("""
HOUGH SPACE:

Setiap titik (x, y) di image space menjadi sinusoid di Hough space.
Garis di image space menjadi titik di Hough space (interseksi sinusoid).

Accumulator Array:
├── Sumbu horizontal: theta (0 - π)
├── Sumbu vertikal: rho (-diagonal - +diagonal)
└── Nilai: jumlah votes

Peak di accumulator = garis terdeteksi
    """)
    
    # Buat gambar sederhana dengan beberapa garis
    gambar = np.zeros((300, 300), dtype=np.uint8)
    cv2.line(gambar, (50, 50), (250, 50), 255, 2)    # Horizontal
    cv2.line(gambar, (50, 50), (50, 250), 255, 2)    # Vertical
    cv2.line(gambar, (50, 250), (250, 50), 255, 2)   # Diagonal
    
    # Create accumulator manually
    h, w = gambar.shape
    diagonal = int(np.sqrt(h**2 + w**2))
    thetas = np.deg2rad(np.arange(0, 180, 1))
    rhos = np.arange(-diagonal, diagonal, 1)
    
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)
    
    # Get edge points
    y_edges, x_edges = np.nonzero(gambar)
    
    # Vote
    for i in range(len(x_edges)):
        x = x_edges[i]
        y = y_edges[i]
        
        for j, theta in enumerate(thetas):
            rho = int(x * np.cos(theta) + y * np.sin(theta))
            rho_idx = np.argmin(np.abs(rhos - rho))
            accumulator[rho_idx, j] += 1
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(gambar, cmap='gray')
    axes[0].set_title("Input Image (Edges)")
    axes[0].axis('off')
    
    axes[1].imshow(accumulator, cmap='hot', aspect='auto',
                   extent=[0, 180, diagonal, -diagonal])
    axes[1].set_xlabel('Theta (degrees)')
    axes[1].set_ylabel('Rho (pixels)')
    axes[1].set_title("Hough Space (Accumulator)")
    
    # Show detected lines
    lines = cv2.HoughLines(gambar, 1, np.pi/180, 80)
    output = cv2.cvtColor(gambar, cv2.COLOR_GRAY2BGR)
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    axes[2].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    axes[2].set_title(f"Detected Lines ({len(lines) if lines is not None else 0})")
    axes[2].axis('off')
    
    plt.suptitle("Hough Transform Visualization", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: HOUGH LINE TRANSFORM")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
HOUGH TRANSFORM adalah teknik untuk mendeteksi shapes
(garis, lingkaran, dll) dalam gambar.

KONSEP DASAR:

Representasi garis di Polar Coordinates:
    ρ = x·cos(θ) + y·sin(θ)

Dimana:
├── ρ (rho): jarak garis dari origin
└── θ (theta): sudut normal terhadap sumbu x

ALGORITMA:
1. Untuk setiap edge point (x, y)
2. Hitung semua (ρ, θ) yang mungkin
3. Increment accumulator di posisi tersebut
4. Find peaks di accumulator

DUA METODE:

1. Standard Hough (cv2.HoughLines):
   ├── Return (ρ, θ) untuk setiap garis
   ├── Lebih lengkap tapi perlu post-processing
   └── Cocok untuk analisis

2. Probabilistic Hough (cv2.HoughLinesP):
   ├── Return endpoints (x1,y1,x2,y2)
   ├── Lebih efisien, langsung dapat segment
   └── Cocok untuk aplikasi praktis

APLIKASI:
├── Lane detection (self-driving cars)
├── Document scanning
├── Building detection
└── Barcode reading
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
    print(f"[INFO] Metode: {HOUGH_METHOD}")
    
    # Preprocessing
    print("\n[STEP 1] Preprocessing (Edge Detection)...")
    edges = preprocess_for_hough(gambar)
    print(f"   Canny threshold: {CANNY_LOW} - {CANNY_HIGH}")
    print(f"   Edge pixels: {np.sum(edges > 0)}")
    
    # Hough Transform
    print("\n[STEP 2] Hough Line Transform...")
    
    if HOUGH_METHOD in ['standard', 'both']:
        print("\n   Standard Hough Transform:")
        lines_std = standard_hough_lines(edges, RHO_RESOLUTION, THETA_RESOLUTION, 
                                         VOTE_THRESHOLD)
        n_std = len(lines_std) if lines_std is not None else 0
        print(f"   Detected: {n_std} lines")
        
        if lines_std is not None:
            analysis = analyze_detected_lines(lines_std, 'standard')
            print(f"   Horizontal: {analysis['horizontal']}")
            print(f"   Vertical: {analysis['vertical']}")
            print(f"   Diagonal: {analysis['diagonal']}")
        
        output_std = draw_hough_lines(gambar, lines_std, 'standard')
    
    if HOUGH_METHOD in ['probabilistic', 'both']:
        print("\n   Probabilistic Hough Transform:")
        lines_prob = probabilistic_hough_lines(edges, RHO_RESOLUTION, THETA_RESOLUTION,
                                               VOTE_THRESHOLD, MIN_LINE_LENGTH, MAX_LINE_GAP)
        n_prob = len(lines_prob) if lines_prob is not None else 0
        print(f"   Detected: {n_prob} line segments")
        
        if lines_prob is not None:
            analysis = analyze_detected_lines(lines_prob, 'probabilistic')
            print(f"   Horizontal: {analysis['horizontal']}")
            print(f"   Vertical: {analysis['vertical']}")
            print(f"   Diagonal: {analysis['diagonal']}")
        
        output_prob = draw_hough_lines(gambar, lines_prob, 'probabilistic')
    
    # Visualisasi
    print("\n[STEP 3] Visualisasi...")
    
    if HOUGH_METHOD == 'both':
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title("Original Image")
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(edges, cmap='gray')
        axes[0, 1].set_title("Canny Edges")
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(output_std, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title(f"Standard Hough\n{n_std} lines")
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(cv2.cvtColor(output_prob, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title(f"Probabilistic Hough\n{n_prob} segments")
        axes[1, 1].axis('off')
    else:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
        axes[0].set_title("Original Image")
        axes[0].axis('off')
        
        axes[1].imshow(edges, cmap='gray')
        axes[1].set_title("Canny Edges")
        axes[1].axis('off')
        
        if HOUGH_METHOD == 'standard':
            axes[2].imshow(cv2.cvtColor(output_std, cv2.COLOR_BGR2RGB))
            axes[2].set_title(f"Standard Hough: {n_std} lines")
        else:
            axes[2].imshow(cv2.cvtColor(output_prob, cv2.COLOR_BGR2RGB))
            axes[2].set_title(f"Probabilistic Hough: {n_prob} segments")
        axes[2].axis('off')
    
    plt.suptitle("Hough Line Transform", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_hough_space()
    demo_threshold_effect()
    demo_minlength_maxgap()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN HOUGH LINE TRANSFORM")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Preprocessing (Edge Detection)
edges = cv2.Canny(gray, low_threshold, high_threshold)

# Standard Hough Transform
lines = cv2.HoughLines(edges, rho, theta, threshold)
# Returns: array of (rho, theta)

# Probabilistic Hough Transform
lines = cv2.HoughLinesP(edges, rho, theta, threshold,
                        minLineLength=50,
                        maxLineGap=10)
# Returns: array of (x1, y1, x2, y2)

PARAMETER PENTING:

1. rho: resolusi ρ (biasanya 1 pixel)
2. theta: resolusi θ (biasanya π/180 = 1 derajat)
3. threshold: minimum votes
4. minLineLength: minimum panjang segment (HoughLinesP)
5. maxLineGap: maximum gap dalam segment (HoughLinesP)

TIPS:
1. Gunakan Canny edge detection terlebih dahulu
2. Adjust threshold sesuai kompleksitas gambar
3. HoughLinesP lebih praktis untuk kebanyakan aplikasi
4. Untuk garis yang presisi, gunakan standard Hough

APLIKASI:
├── Lane detection: minLineLength tinggi, filter sudut
├── Document: threshold tinggi untuk garis jelas
└── Building: kombinasi horizontal dan vertical
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
