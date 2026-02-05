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

# 2. Kernel size untuk filter (harus ganjil: 3, 5, 7, ...)
# Keterangan: Inisialisasi atau perbarui variabel KERNEL_SIZE.
KERNEL_SIZE = 5

# 3. Gaussian sigma (standar deviasi)
# Semakin besar, semakin blur
# Keterangan: Inisialisasi atau perbarui variabel GAUSSIAN_SIGMA.
GAUSSIAN_SIGMA = 1.5

# 4. Bilateral filter parameters
# Keterangan: Inisialisasi atau perbarui variabel BILATERAL_D.
BILATERAL_D = 9          # Diameter neighborhood
# Keterangan: Inisialisasi atau perbarui variabel BILATERAL_SIGMA_COLOR.
BILATERAL_SIGMA_COLOR = 75    # Filter sigma in color space
# Keterangan: Inisialisasi atau perbarui variabel BILATERAL_SIGMA_SPACE.
BILATERAL_SIGMA_SPACE = 75    # Filter sigma in coordinate space

# 5. Sharpening strength (untuk unsharp masking)
# Range: 0.0 - 3.0 (1.0 = moderate, 2.0 = strong)
# Keterangan: Inisialisasi atau perbarui variabel SHARPENING_STRENGTH.
SHARPENING_STRENGTH = 1.5

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
    """Membuat gambar sample untuk demonstrasi filtering"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background gradient
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Mulai loop dengan for j in range(600).
        for j in range(600):
            # Keterangan: Inisialisasi beberapa variabel (gambar[i, j]).
            gambar[i, j] = [50 + j//4, 50, 50]
    
    # Shapes dengan edges yang jelas
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), (255, 100, 100), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 100), 60, (100, 255, 100), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillPoly(gambar, [np.array([[250, 300], [350, 200], [450, 300]])], 
                 # Keterangan: Jalankan perintah berikut.
                 (100, 100, 255))
    
    # Text
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "FILTER", (200, 380), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# Keterangan: Definisikan fungsi tambah_noise.
def tambah_noise(gambar, noise_type='gaussian', amount=25):
    """
    Menambahkan noise ke gambar
    
    Parameter:
    - gambar: input image
    - noise_type: 'gaussian' atau 'salt_pepper'
    - amount: intensitas noise
    """
    # Keterangan: Inisialisasi atau perbarui variabel noisy.
    noisy = gambar.copy().astype(np.float64)
    
    # Keterangan: Cek kondisi noise_type == 'gaussian'.
    if noise_type == 'gaussian':
        # Keterangan: Inisialisasi atau perbarui variabel noise.
        noise = np.random.normal(0, amount, gambar.shape)
        # Keterangan: Inisialisasi atau perbarui variabel noisy.
        noisy = noisy + noise
        
    # Keterangan: Cek kondisi alternatif noise_type == 'salt_pepper'.
    elif noise_type == 'salt_pepper':
        # Salt (white pixels)
        # Keterangan: Inisialisasi atau perbarui variabel salt.
        salt = np.random.random(gambar.shape[:2]) < (amount / 1000)
        # Keterangan: Inisialisasi atau perbarui variabel noisy[salt].
        noisy[salt] = 255
        
        # Pepper (black pixels)
        # Keterangan: Inisialisasi atau perbarui variabel pepper.
        pepper = np.random.random(gambar.shape[:2]) < (amount / 1000)
        # Keterangan: Inisialisasi atau perbarui variabel noisy[pepper].
        noisy[pepper] = 0
    
    # Keterangan: Inisialisasi atau perbarui variabel noisy.
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    # Keterangan: Kembalikan hasil dari fungsi.
    return noisy


# ============================================================
# FUNGSI SMOOTHING FILTERS
# ============================================================

# Keterangan: Definisikan fungsi average_filter.
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
    # Keterangan: Inisialisasi array bernilai satu.
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.filter2D(gambar, -1, kernel)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi gaussian_filter.
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
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    hasil = cv2.GaussianBlur(gambar, (kernel_size, kernel_size), sigma)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi median_filter.
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
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.medianBlur(gambar, kernel_size)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi bilateral_filter.
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
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.bilateralFilter(gambar, d, sigma_color, sigma_space)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# ============================================================
# FUNGSI SHARPENING FILTERS
# ============================================================

# Keterangan: Definisikan fungsi unsharp_masking.
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
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    blurred = cv2.GaussianBlur(gambar, (0, 0), sigma)
    
    # Unsharp masking formula
    # Keterangan: Inisialisasi atau perbarui variabel sharpened.
    sharpened = cv2.addWeighted(gambar, 1 + strength, blurred, -strength, 0)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return sharpened


# Keterangan: Definisikan fungsi laplacian_sharpening.
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
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Process setiap channel secara terpisah
        # Keterangan: Inisialisasi atau perbarui variabel channels.
        channels = cv2.split(gambar)
        # Keterangan: Inisialisasi atau perbarui variabel sharpened_channels.
        sharpened_channels = []
        
        # Keterangan: Mulai loop dengan for channel in channels.
        for channel in channels:
            # Keterangan: Hitung Laplacian untuk deteksi tepi.
            laplacian = cv2.Laplacian(channel, cv2.CV_64F)
            # Keterangan: Inisialisasi atau perbarui variabel sharpened.
            sharpened = channel.astype(np.float64) - laplacian
            # Keterangan: Inisialisasi atau perbarui variabel sharpened.
            sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
            # Keterangan: Jalankan perintah berikut.
            sharpened_channels.append(sharpened)
        
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = cv2.merge(sharpened_channels)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Hitung Laplacian untuk deteksi tepi.
        laplacian = cv2.Laplacian(gambar, cv2.CV_64F)
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = gambar.astype(np.float64) - laplacian
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = np.clip(hasil, 0, 255).astype(np.uint8)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi kernel_sharpening.
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
    # Keterangan: Inisialisasi atau perbarui variabel kernel.
    kernel = np.array([[0, -1, 0],
                       # Keterangan: Jalankan perintah berikut.
                       [-1, 5, -1],
                       # Keterangan: Jalankan perintah berikut.
                       [0, -1, 0]])
    
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.filter2D(gambar, -1, kernel)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi high_boost_filter.
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
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    lowpass = cv2.GaussianBlur(gambar, (kernel_size, kernel_size), 0)
    
    # High-boost formula
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.addWeighted(gambar, A, lowpass, -(A-1), 0)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_konvolusi.
def demo_konvolusi():
    """
    Demonstrasi konsep konvolusi
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("KONSEP KONVOLUSI (CONVOLUTION)")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
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
    # Keterangan: Inisialisasi atau perbarui variabel sample.
    sample = np.array([
        # Keterangan: Jalankan perintah berikut.
        [50, 50, 100, 100, 100],
        # Keterangan: Jalankan perintah berikut.
        [50, 50, 100, 100, 100],
        # Keterangan: Jalankan perintah berikut.
        [50, 50, 100, 100, 100],
        # Keterangan: Jalankan perintah berikut.
        [50, 50, 100, 100, 100],
        # Keterangan: Jalankan perintah berikut.
        [50, 50, 100, 100, 100]
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.uint8)
    
    # Kernel average 3x3
    # Keterangan: Inisialisasi array bernilai satu.
    kernel = np.ones((3, 3)) / 9
    
    # Hasil konvolusi
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = cv2.filter2D(sample, -1, kernel)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0].imshow(sample, cmap).
    axes[0].imshow(sample, cmap='gray', vmin=0, vmax=255)
    # Keterangan: Jalankan perintah berikut.
    axes[0].set_title("Input Image")
    # Keterangan: Mulai loop dengan for i in range(5).
    for i in range(5):
        # Keterangan: Mulai loop dengan for j in range(5).
        for j in range(5):
            # Keterangan: Inisialisasi beberapa variabel (axes[0].text(j, i, str(sample[i, j]), ha).
            axes[0].text(j, i, str(sample[i, j]), ha='center', va='center', 
                        # Keterangan: Inisialisasi atau perbarui variabel color.
                        color='white' if sample[i, j] < 128 else 'black')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1].imshow(kernel, cmap).
    axes[1].imshow(kernel, cmap='Blues')
    # Keterangan: Jalankan perintah berikut.
    axes[1].set_title("Kernel (Average 3×3)")
    # Keterangan: Mulai loop dengan for i in range(3).
    for i in range(3):
        # Keterangan: Mulai loop dengan for j in range(3).
        for j in range(3):
            # Keterangan: Inisialisasi beberapa variabel (axes[1].text(j, i, f"{kernel[i, j]:.2f}", ha).
            axes[1].text(j, i, f"{kernel[i, j]:.2f}", ha='center', va='center')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[2].imshow(result, cmap).
    axes[2].imshow(result, cmap='gray', vmin=0, vmax=255)
    # Keterangan: Jalankan perintah berikut.
    axes[2].set_title("Output (After Convolution)")
    # Keterangan: Mulai loop dengan for i in range(5).
    for i in range(5):
        # Keterangan: Mulai loop dengan for j in range(5).
        for j in range(5):
            # Keterangan: Inisialisasi beberapa variabel (axes[2].text(j, i, str(result[i, j]), ha).
            axes[2].text(j, i, str(result[i, j]), ha='center', va='center',
                        # Keterangan: Inisialisasi atau perbarui variabel color.
                        color='white' if result[i, j] < 128 else 'black')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Proses Konvolusi", fontsize).
    plt.suptitle("Proses Konvolusi", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_smoothing_filters.
def demo_smoothing_filters():
    """
    Perbandingan berbagai smoothing filters
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PERBANDINGAN SMOOTHING FILTERS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
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
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Tambahkan noise untuk demonstrasi
    # Keterangan: Inisialisasi atau perbarui variabel noisy_gaussian.
    noisy_gaussian = tambah_noise(gambar, 'gaussian', 25)
    # Keterangan: Inisialisasi atau perbarui variabel noisy_sp.
    noisy_sp = tambah_noise(gambar, 'salt_pepper', 50)
    
    # Demo dengan Gaussian noise
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(noisy_gaussian, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Gaussian Noise")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(average_filter(noisy_gaussian, KERNEL_SIZE), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title(f"Average Filter ({KERNEL_SIZE}×{KERNEL_SIZE})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 2].imshow(cv2.cvtColor(gaussian_filter(noisy_gaussian, KERNEL_SIZE, 
                                                    # Keterangan: Jalankan perintah berikut.
                                                    GAUSSIAN_SIGMA), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"Gaussian Filter (σ).
    axes[0, 2].set_title(f"Gaussian Filter (σ={GAUSSIAN_SIGMA})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Demo dengan salt-pepper noise
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(noisy_sp, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Salt & Pepper Noise")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(median_filter(noisy_sp, KERNEL_SIZE), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title(f"Median Filter ({KERNEL_SIZE}×{KERNEL_SIZE})")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 2].imshow(cv2.cvtColor(bilateral_filter(noisy_sp, BILATERAL_D,
                                                     # Keterangan: Jalankan perintah berikut.
                                                     BILATERAL_SIGMA_COLOR,
                                                     # Keterangan: Jalankan perintah berikut.
                                                     BILATERAL_SIGMA_SPACE),
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].set_title(f"Bilateral Filter (d).
    axes[1, 2].set_title(f"Bilateral Filter (d={BILATERAL_D})")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Smoothing Filters", fontsize).
    plt.suptitle("Perbandingan Smoothing Filters", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_sharpening_filters.
def demo_sharpening_filters():
    """
    Perbandingan berbagai sharpening methods
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PERBANDINGAN SHARPENING METHODS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
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
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Buat versi slightly blurred
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    blurred = cv2.GaussianBlur(gambar, (5, 5), 1.5)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Slightly Blurred Input")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(unsharp_masking(blurred, GAUSSIAN_SIGMA, 
                                                    # Keterangan: Jalankan perintah berikut.
                                                    SHARPENING_STRENGTH), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title(f"Unsharp Masking (strength).
    axes[0, 1].set_title(f"Unsharp Masking (strength={SHARPENING_STRENGTH})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 2].imshow(cv2.cvtColor(laplacian_sharpening(blurred), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Laplacian Sharpening")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Original (for reference)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(kernel_sharpening(blurred), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Kernel Sharpening")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 2].imshow(cv2.cvtColor(high_boost_filter(blurred, 2.0), 
                                    # Keterangan: Jalankan perintah berikut.
                                    cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].set_title("High-Boost Filter (A).
    axes[1, 2].set_title("High-Boost Filter (A=2.0)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Sharpening Methods", fontsize).
    plt.suptitle("Perbandingan Sharpening Methods", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_kernel_size_effect.
def demo_kernel_size_effect():
    """
    Demonstrasi pengaruh kernel size
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PENGARUH KERNEL SIZE")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
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
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Variasi kernel size
    # Keterangan: Inisialisasi atau perbarui variabel sizes.
    sizes = [3, 5, 9, 15]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, len(sizes), figsize=(16, 8))
    
    # Baris 1: Gaussian blur dengan berbagai kernel size
    # Keterangan: Mulai loop dengan for i, size in enumerate(sizes).
    for i, size in enumerate(sizes):
        # Keterangan: Inisialisasi atau perbarui variabel blurred.
        blurred = gaussian_filter(gambar, size, 0)
        # Keterangan: Konversi ruang warna gambar.
        axes[0, i].imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].set_title(f"Gaussian {size}×{size}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
    
    # Baris 2: Median filter dengan berbagai kernel size
    # Keterangan: Mulai loop dengan for i, size in enumerate(sizes).
    for i, size in enumerate(sizes):
        # Keterangan: Inisialisasi atau perbarui variabel filtered.
        filtered = median_filter(gambar, size)
        # Keterangan: Konversi ruang warna gambar.
        axes[1, i].imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].set_title(f"Median {size}×{size}")
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Pengaruh Kernel Size pada Filtering", fontsize).
    plt.suptitle("Pengaruh Kernel Size pada Filtering", fontsize=14)
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
    print("PRAKTIKUM: SPATIAL FILTERING")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
SPATIAL FILTERING adalah operasi pemrosesan citra
# Keterangan: Jalankan perintah berikut.
yang memodifikasi piksel berdasarkan nilai piksel
# Keterangan: Jalankan perintah berikut.
di sekitarnya (neighborhood).

# Keterangan: Mulai blok kode baru.
Dua kategori utama:
# Keterangan: Jalankan perintah berikut.
1. SMOOTHING (Low-pass filtering)
   # Keterangan: Jalankan perintah berikut.
   └── Mengurangi noise, blur edges
   
# Keterangan: Jalankan perintah berikut.
2. SHARPENING (High-pass filtering)
   # Keterangan: Jalankan perintah berikut.
   └── Enhance edges, meningkatkan detail

# Keterangan: Mulai blok kode baru.
Aplikasi:
# Keterangan: Jalankan perintah berikut.
├── Noise reduction (photo enhancement)
# Keterangan: Jalankan perintah berikut.
├── Edge enhancement (medical imaging)
# Keterangan: Jalankan perintah berikut.
├── Preprocessing untuk feature extraction
# Keterangan: Jalankan perintah berikut.
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
# Keterangan: Mulai blok kode baru.
FUNGSI OPENCV:

# SMOOTHING FILTERS
# Keterangan: Inisialisasi atau perbarui variabel blur.
blur = cv2.blur(img, (ksize, ksize))           # Average
# Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
blur = cv2.GaussianBlur(img, (ksize, ksize), sigma)  # Gaussian
# Keterangan: Inisialisasi atau perbarui variabel blur.
blur = cv2.medianBlur(img, ksize)              # Median
# Keterangan: Inisialisasi atau perbarui variabel blur.
blur = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)  # Bilateral

# SHARPENING (manual)
# Unsharp masking
# Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
blurred = cv2.GaussianBlur(img, (0, 0), sigma)
# Keterangan: Inisialisasi atau perbarui variabel sharpened.
sharpened = cv2.addWeighted(img, 1+strength, blurred, -strength, 0)

# Laplacian sharpening
# Keterangan: Hitung Laplacian untuk deteksi tepi.
laplacian = cv2.Laplacian(img, cv2.CV_64F)
# Keterangan: Inisialisasi atau perbarui variabel sharpened.
sharpened = img - laplacian

# Kernel sharpening
# Keterangan: Inisialisasi atau perbarui variabel kernel.
kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
# Keterangan: Inisialisasi atau perbarui variabel sharpened.
sharpened = cv2.filter2D(img, -1, kernel)

# Keterangan: Mulai blok kode baru.
PEMILIHAN FILTER:
# Keterangan: Jalankan perintah berikut.
├── Gaussian noise → Gaussian filter
# Keterangan: Jalankan perintah berikut.
├── Salt-pepper noise → Median filter
# Keterangan: Jalankan perintah berikut.
├── Edge-preserving smooth → Bilateral filter
# Keterangan: Jalankan perintah berikut.
├── Edge enhancement → Unsharp masking
# Keterangan: Jalankan perintah berikut.
└── Strong edge enhance → Laplacian

# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
1. Selalu mulai dengan kernel size kecil
# Keterangan: Jalankan perintah berikut.
2. Bilateral filter lambat tapi hasil terbaik
# Keterangan: Jalankan perintah berikut.
3. Untuk video real-time, gunakan Gaussian/Median
# Keterangan: Jalankan perintah berikut.
4. Sharpening dapat mengamplifikasi noise
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
