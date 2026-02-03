# ============================================================
# PROGRAM: 05_spatial_filtering.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk spatial filtering (smoothing & sharpening)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep konvolusi dan kernel
#   2. Filter smoothing: average, Gaussian, median, bilateral
#   3. Filter sharpening: unsharp masking, Laplacian
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

# 2. Kernel size untuk filter (harus ganjil: 3, 5, 7, ...)
KERNEL_SIZE = 5

# 3. Gaussian sigma (standar deviasi)
# Semakin besar, semakin blur
GAUSSIAN_SIGMA = 1.5

# 4. Bilateral filter parameters
BILATERAL_D = 9          # Diameter neighborhood
BILATERAL_SIGMA_COLOR = 75    # Filter sigma in color space
BILATERAL_SIGMA_SPACE = 75    # Filter sigma in coordinate space

# 5. Sharpening strength (untuk unsharp masking)
# Range: 0.0 - 3.0 (1.0 = moderate, 2.0 = strong)
SHARPENING_STRENGTH = 1.5

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
    """Membuat gambar sample untuk demonstrasi filtering"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background gradient
    for i in range(400):
        for j in range(600):
            gambar[i, j] = [50 + j//4, 50, 50]
    
    # Shapes dengan edges yang jelas
    cv2.rectangle(gambar, (50, 50), (200, 150), (255, 100, 100), -1)
    cv2.circle(gambar, (400, 100), 60, (100, 255, 100), -1)
    cv2.fillPoly(gambar, [np.array([[250, 300], [350, 200], [450, 300]])], 
                 (100, 100, 255))
    
    # Text
    cv2.putText(gambar, "FILTER", (200, 380), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    return gambar


def tambah_noise(gambar, noise_type='gaussian', amount=25):
    """
    Menambahkan noise ke gambar
    
    Parameter:
    - gambar: input image
    - noise_type: 'gaussian' atau 'salt_pepper'
    - amount: intensitas noise
    """
    noisy = gambar.copy().astype(np.float64)
    
    if noise_type == 'gaussian':
        noise = np.random.normal(0, amount, gambar.shape)
        noisy = noisy + noise
        
    elif noise_type == 'salt_pepper':
        # Salt (white pixels)
        salt = np.random.random(gambar.shape[:2]) < (amount / 1000)
        noisy[salt] = 255
        
        # Pepper (black pixels)
        pepper = np.random.random(gambar.shape[:2]) < (amount / 1000)
        noisy[pepper] = 0
    
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


# ============================================================
# FUNGSI SMOOTHING FILTERS
# ============================================================

def average_filter(gambar, kernel_size=3):
    """
    Average (Mean) Filter / Box Filter
    
    Setiap piksel diganti dengan rata-rata dari neighborhood-nya
    Sederhana tapi dapat menyebabkan blur pada edges
    
    Parameter:
    - gambar: input image
    - kernel_size: ukuran kernel (harus ganjil)
    
    Return:
    - gambar yang sudah di-smooth
    """
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    hasil = cv2.filter2D(gambar, -1, kernel)
    return hasil


def gaussian_filter(gambar, kernel_size=5, sigma=0):
    """
    Gaussian Filter
    
    Filter dengan weight berbentuk Gaussian distribution
    Lebih baik dari average filter karena memprioritaskan
    piksel yang lebih dekat ke center
    
    Parameter:
    - gambar: input image
    - kernel_size: ukuran kernel (harus ganjil)
    - sigma: standar deviasi (0 = auto calculate)
    
    Return:
    - gambar yang sudah di-smooth
    """
    hasil = cv2.GaussianBlur(gambar, (kernel_size, kernel_size), sigma)
    return hasil


def median_filter(gambar, kernel_size=5):
    """
    Median Filter
    
    Setiap piksel diganti dengan median dari neighborhood-nya
    Sangat efektif untuk menghilangkan salt-and-pepper noise
    Menjaga edges lebih baik dari average/Gaussian
    
    Parameter:
    - gambar: input image
    - kernel_size: ukuran kernel (harus ganjil)
    
    Return:
    - gambar yang sudah di-filter
    """
    hasil = cv2.medianBlur(gambar, kernel_size)
    return hasil


def bilateral_filter(gambar, d=9, sigma_color=75, sigma_space=75):
    """
    Bilateral Filter
    
    Filter yang mempertimbangkan:
    1. Jarak spasial (seperti Gaussian)
    2. Perbedaan intensitas (color similarity)
    
    Hasil: Smoothing yang menjaga edges dengan sangat baik
    
    Parameter:
    - gambar: input image
    - d: diameter of pixel neighborhood
    - sigma_color: filter sigma in color space
    - sigma_space: filter sigma in coordinate space
    
    Return:
    - gambar yang sudah di-filter
    """
    hasil = cv2.bilateralFilter(gambar, d, sigma_color, sigma_space)
    return hasil


# ============================================================
# FUNGSI SHARPENING FILTERS
# ============================================================

def unsharp_masking(gambar, sigma=1.0, strength=1.5):
    """
    Unsharp Masking
    
    Langkah:
    1. Buat blurred version dari gambar
    2. Kurangi blur dari original (high-pass)
    3. Tambahkan high-pass ke original
    
    sharpened = original + strength × (original - blurred)
    
    Parameter:
    - gambar: input image
    - sigma: sigma untuk Gaussian blur
    - strength: intensitas sharpening
    
    Return:
    - gambar yang sudah di-sharpen
    """
    # Buat versi blur
    blurred = cv2.GaussianBlur(gambar, (0, 0), sigma)
    
    # Unsharp masking formula
    sharpened = cv2.addWeighted(gambar, 1 + strength, blurred, -strength, 0)
    
    return sharpened


def laplacian_sharpening(gambar):
    """
    Laplacian Sharpening
    
    Menggunakan operator Laplacian (second derivative)
    untuk mendeteksi dan enhance edges
    
    sharpened = original - Laplacian(original)
    
    Parameter:
    - gambar: input image
    
    Return:
    - gambar yang sudah di-sharpen
    """
    # Konversi ke grayscale jika perlu
    if len(gambar.shape) == 3:
        # Process setiap channel secara terpisah
        channels = cv2.split(gambar)
        sharpened_channels = []
        
        for channel in channels:
            laplacian = cv2.Laplacian(channel, cv2.CV_64F)
            sharpened = channel.astype(np.float64) - laplacian
            sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
            sharpened_channels.append(sharpened)
        
        hasil = cv2.merge(sharpened_channels)
    else:
        laplacian = cv2.Laplacian(gambar, cv2.CV_64F)
        hasil = gambar.astype(np.float64) - laplacian
        hasil = np.clip(hasil, 0, 255).astype(np.uint8)
    
    return hasil


def kernel_sharpening(gambar):
    """
    Sharpening menggunakan kernel khusus
    
    Kernel: [ 0, -1,  0]
            [-1,  5, -1]
            [ 0, -1,  0]
    
    atau versi lebih kuat:
            [-1, -1, -1]
            [-1,  9, -1]
            [-1, -1, -1]
    """
    # Kernel sharpening standar
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    
    hasil = cv2.filter2D(gambar, -1, kernel)
    return hasil


def high_boost_filter(gambar, A=2.0, kernel_size=5):
    """
    High-Boost Filtering
    
    Variant dari unsharp masking dengan lebih control
    
    high_boost = A × original - lowpass(original)
               = (A-1) × original + (original - lowpass(original))
               = (A-1) × original + highpass(original)
    
    Parameter:
    - gambar: input image
    - A: amplification factor (>1 untuk sharpening)
    - kernel_size: ukuran kernel untuk lowpass
    
    Return:
    - gambar hasil high-boost filtering
    """
    # Lowpass filter
    lowpass = cv2.GaussianBlur(gambar, (kernel_size, kernel_size), 0)
    
    # High-boost formula
    hasil = cv2.addWeighted(gambar, A, lowpass, -(A-1), 0)
    
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_konvolusi():
    """
    Demonstrasi konsep konvolusi
    """
    print("\n" + "=" * 60)
    print("KONSEP KONVOLUSI (CONVOLUTION)")
    print("=" * 60)
    
    print("""
KONVOLUSI adalah operasi matematika di mana kernel
"bergeser" di atas gambar dan menghasilkan output baru.

Untuk setiap posisi:
1. Tempatkan kernel pada lokasi (x, y)
2. Kalikan setiap elemen kernel dengan piksel di bawahnya
3. Jumlahkan semua hasil perkalian
4. Simpan hasil sebagai piksel output pada (x, y)

CONTOH KERNEL:

Average 3×3:           Gaussian approx:       Sharpen:
[1/9  1/9  1/9]       [1/16  2/16  1/16]     [ 0  -1   0]
[1/9  1/9  1/9]       [2/16  4/16  2/16]     [-1   5  -1]
[1/9  1/9  1/9]       [1/16  2/16  1/16]     [ 0  -1   0]
    """)
    
    # Visualisasi proses konvolusi
    # Buat gambar kecil untuk visualisasi
    sample = np.array([
        [50, 50, 100, 100, 100],
        [50, 50, 100, 100, 100],
        [50, 50, 100, 100, 100],
        [50, 50, 100, 100, 100],
        [50, 50, 100, 100, 100]
    ], dtype=np.uint8)
    
    # Kernel average 3x3
    kernel = np.ones((3, 3)) / 9
    
    # Hasil konvolusi
    result = cv2.filter2D(sample, -1, kernel)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    axes[0].imshow(sample, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title("Input Image")
    for i in range(5):
        for j in range(5):
            axes[0].text(j, i, str(sample[i, j]), ha='center', va='center', 
                        color='white' if sample[i, j] < 128 else 'black')
    
    axes[1].imshow(kernel, cmap='Blues')
    axes[1].set_title("Kernel (Average 3×3)")
    for i in range(3):
        for j in range(3):
            axes[1].text(j, i, f"{kernel[i, j]:.2f}", ha='center', va='center')
    
    axes[2].imshow(result, cmap='gray', vmin=0, vmax=255)
    axes[2].set_title("Output (After Convolution)")
    for i in range(5):
        for j in range(5):
            axes[2].text(j, i, str(result[i, j]), ha='center', va='center',
                        color='white' if result[i, j] < 128 else 'black')
    
    plt.suptitle("Proses Konvolusi", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_smoothing_filters():
    """
    Perbandingan berbagai smoothing filters
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN SMOOTHING FILTERS")
    print("=" * 60)
    
    print("""
AVERAGE FILTER:
├── Semua weight sama
├── Paling simple, paling cepat
└── Blur edges

GAUSSIAN FILTER:
├── Weight berbentuk bell curve
├── Lebih natural, lebih smooth
└── Masih blur edges

MEDIAN FILTER:
├── Non-linear (tidak pakai konvolusi)
├── Sangat bagus untuk salt-pepper noise
└── Menjaga edges lebih baik

BILATERAL FILTER:
├── Edge-preserving smoothing
├── Mempertimbangkan spatial dan intensity similarity
└── Paling bagus untuk noise removal tanpa blur edges
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Tambahkan noise untuk demonstrasi
    noisy_gaussian = tambah_noise(gambar, 'gaussian', 25)
    noisy_sp = tambah_noise(gambar, 'salt_pepper', 50)
    
    # Demo dengan Gaussian noise
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(noisy_gaussian, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Gaussian Noise")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(average_filter(noisy_gaussian, KERNEL_SIZE), 
                                    cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"Average Filter ({KERNEL_SIZE}×{KERNEL_SIZE})")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(gaussian_filter(noisy_gaussian, KERNEL_SIZE, 
                                                    GAUSSIAN_SIGMA), 
                                    cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f"Gaussian Filter (σ={GAUSSIAN_SIGMA})")
    axes[0, 2].axis('off')
    
    # Demo dengan salt-pepper noise
    axes[1, 0].imshow(cv2.cvtColor(noisy_sp, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title("Salt & Pepper Noise")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(median_filter(noisy_sp, KERNEL_SIZE), 
                                    cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"Median Filter ({KERNEL_SIZE}×{KERNEL_SIZE})")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(bilateral_filter(noisy_sp, BILATERAL_D,
                                                     BILATERAL_SIGMA_COLOR,
                                                     BILATERAL_SIGMA_SPACE),
                                    cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title(f"Bilateral Filter (d={BILATERAL_D})")
    axes[1, 2].axis('off')
    
    plt.suptitle("Perbandingan Smoothing Filters", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_sharpening_filters():
    """
    Perbandingan berbagai sharpening methods
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN SHARPENING METHODS")
    print("=" * 60)
    
    print("""
UNSHARP MASKING:
├── Paling populer dan fleksibel
├── Control dengan parameter sigma dan strength
└── Hasil natural

LAPLACIAN SHARPENING:
├── Menggunakan second derivative
├── Meningkatkan edges secara signifikan
└── Dapat mengamplifikasi noise

KERNEL SHARPENING:
├── Menggunakan predefined kernel
├── Simple dan cepat
└── Kurang fleksibel

HIGH-BOOST FILTERING:
├── Variant dari unsharp masking
├── Parameter A mengontrol enhancement
└── A=1 → no change, A>1 → sharpening
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Buat versi slightly blurred
    blurred = cv2.GaussianBlur(gambar, (5, 5), 1.5)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Slightly Blurred Input")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(unsharp_masking(blurred, GAUSSIAN_SIGMA, 
                                                    SHARPENING_STRENGTH), 
                                    cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"Unsharp Masking (strength={SHARPENING_STRENGTH})")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(laplacian_sharpening(blurred), 
                                    cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title("Laplacian Sharpening")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title("Original (for reference)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(kernel_sharpening(blurred), 
                                    cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title("Kernel Sharpening")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(high_boost_filter(blurred, 2.0), 
                                    cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title("High-Boost Filter (A=2.0)")
    axes[1, 2].axis('off')
    
    plt.suptitle("Perbandingan Sharpening Methods", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_kernel_size_effect():
    """
    Demonstrasi pengaruh kernel size
    """
    print("\n" + "=" * 60)
    print("PENGARUH KERNEL SIZE")
    print("=" * 60)
    
    print("""
KERNEL SIZE menentukan seberapa besar area yang
dipertimbangkan untuk setiap operasi filtering.

Kernel Kecil (3×3):
├── Efek minimal
├── Menjaga detail
└── Processing cepat

Kernel Besar (11×11, 15×15):
├── Efek lebih kuat
├── Menghilangkan detail
└── Processing lebih lambat

RULE OF THUMB:
└── Gunakan kernel terkecil yang memberikan hasil yang diinginkan
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Variasi kernel size
    sizes = [3, 5, 9, 15]
    
    fig, axes = plt.subplots(2, len(sizes), figsize=(16, 8))
    
    # Baris 1: Gaussian blur dengan berbagai kernel size
    for i, size in enumerate(sizes):
        blurred = gaussian_filter(gambar, size, 0)
        axes[0, i].imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
        axes[0, i].set_title(f"Gaussian {size}×{size}")
        axes[0, i].axis('off')
    
    # Baris 2: Median filter dengan berbagai kernel size
    for i, size in enumerate(sizes):
        filtered = median_filter(gambar, size)
        axes[1, i].imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f"Median {size}×{size}")
        axes[1, i].axis('off')
    
    plt.suptitle("Pengaruh Kernel Size pada Filtering", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: SPATIAL FILTERING")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
SPATIAL FILTERING adalah operasi pemrosesan citra
yang memodifikasi piksel berdasarkan nilai piksel
di sekitarnya (neighborhood).

Dua kategori utama:
1. SMOOTHING (Low-pass filtering)
   └── Mengurangi noise, blur edges
   
2. SHARPENING (High-pass filtering)
   └── Enhance edges, meningkatkan detail

Aplikasi:
├── Noise reduction (photo enhancement)
├── Edge enhancement (medical imaging)
├── Preprocessing untuk feature extraction
└── Artistic effects (Instagram filters)
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Membuat gambar sample...")
        gambar = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Kernel Size: {KERNEL_SIZE}")
    print(f"[INFO] Gaussian Sigma: {GAUSSIAN_SIGMA}")
    print(f"[INFO] Sharpening Strength: {SHARPENING_STRENGTH}")
    
    # Tampilkan original vs smoothed vs sharpened
    smoothed = bilateral_filter(gambar, BILATERAL_D, 
                                BILATERAL_SIGMA_COLOR, 
                                BILATERAL_SIGMA_SPACE)
    sharpened = unsharp_masking(gambar, GAUSSIAN_SIGMA, SHARPENING_STRENGTH)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(smoothed, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Smoothed (Bilateral Filter)")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Sharpened (Unsharp Masking)")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_konvolusi()
    demo_smoothing_filters()
    demo_sharpening_filters()
    demo_kernel_size_effect()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN SPATIAL FILTERING")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# SMOOTHING FILTERS
blur = cv2.blur(img, (ksize, ksize))           # Average
blur = cv2.GaussianBlur(img, (ksize, ksize), sigma)  # Gaussian
blur = cv2.medianBlur(img, ksize)              # Median
blur = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)  # Bilateral

# SHARPENING (manual)
# Unsharp masking
blurred = cv2.GaussianBlur(img, (0, 0), sigma)
sharpened = cv2.addWeighted(img, 1+strength, blurred, -strength, 0)

# Laplacian sharpening
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sharpened = img - laplacian

# Kernel sharpening
kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
sharpened = cv2.filter2D(img, -1, kernel)

PEMILIHAN FILTER:
├── Gaussian noise → Gaussian filter
├── Salt-pepper noise → Median filter
├── Edge-preserving smooth → Bilateral filter
├── Edge enhancement → Unsharp masking
└── Strong edge enhance → Laplacian

TIPS:
1. Selalu mulai dengan kernel size kecil
2. Bilateral filter lambat tapi hasil terbaik
3. Untuk video real-time, gunakan Gaussian/Median
4. Sharpening dapat mengamplifikasi noise
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
