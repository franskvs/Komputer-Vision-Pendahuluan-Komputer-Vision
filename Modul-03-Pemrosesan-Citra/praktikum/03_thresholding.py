# ============================================================
# PROGRAM: 03_thresholding.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk berbagai metode thresholding
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep thresholding untuk segmentasi
#   2. Perbedaan global vs adaptive thresholding
#   3. Menggunakan Otsu's automatic threshold
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

# 2. Threshold value untuk binary threshold
# Range: 0-255
# Keterangan: Inisialisasi atau perbarui variabel THRESHOLD_VALUE.
THRESHOLD_VALUE = 127

# 3. Maximum value (nilai untuk piksel yang melewati threshold)
# Keterangan: Inisialisasi atau perbarui variabel MAX_VALUE.
MAX_VALUE = 255

# 4. Block size untuk adaptive threshold (harus ganjil)
# Keterangan: Inisialisasi atau perbarui variabel BLOCK_SIZE.
BLOCK_SIZE = 11

# 5. Konstanta C untuk adaptive threshold
# Nilai yang dikurangi dari mean/weighted mean
# Keterangan: Inisialisasi atau perbarui variabel C_VALUE.
C_VALUE = 2

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


def buat_gambar_dokumen():
    """Membuat gambar simulasi dokumen dengan pencahayaan tidak merata"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600), dtype=np.uint8)
    
    # Background dengan gradient (simulasi pencahayaan tidak merata)
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Mulai loop dengan for j in range(600).
        for j in range(600):
            # Gradient dari kiri (gelap) ke kanan (terang)
            # Keterangan: Inisialisasi beberapa variabel (gambar[i, j]).
            gambar[i, j] = int(100 + j/4 + np.random.randint(-10, 10))
    
    # Tambahkan "teks" (garis hitam)
    # Keterangan: Mulai loop dengan for row in range(5).
    for row in range(5):
        # Keterangan: Inisialisasi atau perbarui variabel y.
        y = 50 + row * 70
        # Keterangan: Mulai loop dengan for line in range(3).
        for line in range(3):
            # Keterangan: Inisialisasi atau perbarui variabel x_start.
            x_start = 50 + line * 30
            # Keterangan: Inisialisasi atau perbarui variabel length.
            length = np.random.randint(100, 200)
            # Keterangan: Jalankan perintah berikut.
            cv2.line(gambar, (x_start, y + line*15), (x_start + length, y + line*15), 0, 2)
    
    # Tambahkan lingkaran (logo)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (500, 100), 40, 50, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (500, 100), 30, 0, -1)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# ============================================================
# FUNGSI THRESHOLDING
# ============================================================

# Keterangan: Definisikan fungsi binary_threshold.
def binary_threshold(gambar, thresh, max_val=255):
    """
    Binary threshold sederhana
    
    Formula:
    output(x,y) = max_val  if input(x,y) > thresh
    output(x,y) = 0        otherwise
    
    Parameter:
    - gambar: input grayscale image
    - thresh: threshold value
    - max_val: nilai untuk piksel yang melewati threshold
    
    Return:
    - gambar binary
    - threshold value yang digunakan
    """
    # Keterangan: Inisialisasi beberapa variabel (_, hasil).
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_BINARY)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, thresh


# Keterangan: Definisikan fungsi binary_threshold_inverse.
def binary_threshold_inverse(gambar, thresh, max_val=255):
    """
    Binary threshold inverse
    
    Formula:
    output(x,y) = 0        if input(x,y) > thresh
    output(x,y) = max_val  otherwise
    """
    # Keterangan: Inisialisasi beberapa variabel (_, hasil).
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_BINARY_INV)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, thresh


# Keterangan: Definisikan fungsi truncate_threshold.
def truncate_threshold(gambar, thresh, max_val=255):
    """
    Truncate threshold
    
    Formula:
    output(x,y) = thresh    if input(x,y) > thresh
    output(x,y) = input(x,y) otherwise
    """
    # Keterangan: Inisialisasi beberapa variabel (_, hasil).
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_TRUNC)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, thresh


# Keterangan: Definisikan fungsi to_zero_threshold.
def to_zero_threshold(gambar, thresh, max_val=255):
    """
    To-zero threshold
    
    Formula:
    output(x,y) = input(x,y)  if input(x,y) > thresh
    output(x,y) = 0           otherwise
    """
    # Keterangan: Inisialisasi beberapa variabel (_, hasil).
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_TOZERO)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, thresh


# Keterangan: Definisikan fungsi otsu_threshold.
def otsu_threshold(gambar, max_val=255):
    """
    Otsu's automatic thresholding
    
    Mencari threshold optimal yang memaksimalkan
    between-class variance (atau meminimalkan within-class variance)
    
    Parameter:
    - gambar: input grayscale image
    - max_val: nilai maksimum
    
    Return:
    - gambar binary
    - threshold value yang dihitung otomatis
    """
    # Keterangan: Inisialisasi beberapa variabel (thresh, hasil).
    thresh, hasil = cv2.threshold(gambar, 0, max_val, 
                                   # Keterangan: Jalankan perintah berikut.
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, thresh


# Keterangan: Definisikan fungsi adaptive_mean_threshold.
def adaptive_mean_threshold(gambar, max_val=255, block_size=11, C=2):
    """
    Adaptive mean thresholding
    
    Threshold dihitung untuk setiap piksel berdasarkan
    mean dari neighborhood (block_size x block_size)
    
    T(x,y) = mean(neighborhood) - C
    
    Parameter:
    - gambar: input grayscale image
    - max_val: nilai maksimum
    - block_size: ukuran neighborhood (harus ganjil)
    - C: konstanta yang dikurangi dari mean
    
    Return:
    - gambar binary
    """
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.adaptiveThreshold(gambar, max_val, 
                                   # Keterangan: Jalankan perintah berikut.
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   # Keterangan: Jalankan perintah berikut.
                                   cv2.THRESH_BINARY, block_size, C)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi adaptive_gaussian_threshold.
def adaptive_gaussian_threshold(gambar, max_val=255, block_size=11, C=2):
    """
    Adaptive Gaussian thresholding
    
    Seperti adaptive mean, tapi menggunakan weighted mean
    dengan Gaussian weights
    
    Parameter:
    - gambar: input grayscale image
    - max_val: nilai maksimum
    - block_size: ukuran neighborhood (harus ganjil)
    - C: konstanta yang dikurangi dari weighted mean
    
    Return:
    - gambar binary
    """
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.adaptiveThreshold(gambar, max_val,
                                   # Keterangan: Jalankan perintah berikut.
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   # Keterangan: Jalankan perintah berikut.
                                   cv2.THRESH_BINARY, block_size, C)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_threshold_types.
def demo_threshold_types():
    """
    Demonstrasi berbagai jenis threshold
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("BERBAGAI JENIS THRESHOLD")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
JENIS-JENIS THRESHOLD:

1. BINARY:      > thresh → max_val, else → 0
2. BINARY_INV:  > thresh → 0, else → max_val
3. TRUNC:       > thresh → thresh, else → unchanged
4. TOZERO:      > thresh → unchanged, else → 0
5. TOZERO_INV:  > thresh → 0, else → unchanged
    """)
    
    # Buat gambar gradient untuk demonstrasi
    # Keterangan: Inisialisasi array bernilai nol.
    gradient = np.zeros((100, 256), dtype=np.uint8)
    # Keterangan: Mulai loop dengan for j in range(256).
    for j in range(256):
        # Keterangan: Inisialisasi beberapa variabel (gradient[:, j]).
        gradient[:, j] = j
    
    # Keterangan: Inisialisasi atau perbarui variabel thresh.
    thresh = 127
    
    # Berbagai jenis threshold
    # Keterangan: Inisialisasi atau perbarui variabel types.
    types = [
        # Keterangan: Jalankan perintah berikut.
        (cv2.THRESH_BINARY, "BINARY"),
        # Keterangan: Jalankan perintah berikut.
        (cv2.THRESH_BINARY_INV, "BINARY_INV"),
        # Keterangan: Jalankan perintah berikut.
        (cv2.THRESH_TRUNC, "TRUNC"),
        # Keterangan: Jalankan perintah berikut.
        (cv2.THRESH_TOZERO, "TOZERO"),
        # Keterangan: Jalankan perintah berikut.
        (cv2.THRESH_TOZERO_INV, "TOZERO_INV"),
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    # Keterangan: Inisialisasi atau perbarui variabel axes.
    axes = axes.flatten()
    
    # Original
    # Keterangan: Inisialisasi beberapa variabel (axes[0].imshow(gradient, cmap).
    axes[0].imshow(gradient, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0].set_title("Original Gradient")
    # Keterangan: Jalankan perintah berikut.
    axes[0].axis('off')
    
    # Keterangan: Mulai loop dengan for i, (thresh_type, name) in enumerate(types, 1).
    for i, (thresh_type, name) in enumerate(types, 1):
        # Keterangan: Inisialisasi beberapa variabel (_, hasil).
        _, hasil = cv2.threshold(gradient, thresh, 255, thresh_type)
        # Keterangan: Inisialisasi beberapa variabel (axes[i].imshow(hasil, cmap).
        axes[i].imshow(hasil, cmap='gray')
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"{name}\n(thresh.
        axes[i].set_title(f"{name}\n(thresh={thresh})")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Berbagai Jenis Threshold pada Gradient", fontsize).
    plt.suptitle("Berbagai Jenis Threshold pada Gradient", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_global_vs_adaptive.
def demo_global_vs_adaptive():
    """
    Perbandingan global threshold vs adaptive threshold
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("GLOBAL vs ADAPTIVE THRESHOLD")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
GLOBAL THRESHOLD:
├── Satu nilai threshold untuk seluruh gambar
├── Cepat dan sederhana
└── Tidak cocok untuk pencahayaan tidak merata

ADAPTIVE THRESHOLD:
├── Threshold berbeda untuk setiap region
├── Dihitung dari neighborhood lokal
├── Lebih baik untuk pencahayaan tidak merata
└── Parameter: block_size dan C
    """)
    
    # Buat gambar dengan pencahayaan tidak merata
    # Keterangan: Inisialisasi atau perbarui variabel gambar.
    gambar = buat_gambar_dokumen()
    
    # Apply different thresholds
    # Keterangan: Inisialisasi beberapa variabel (global_thresh, _).
    global_thresh, _ = binary_threshold(gambar, THRESHOLD_VALUE)
    # Keterangan: Inisialisasi beberapa variabel (otsu_result, otsu_thresh).
    otsu_result, otsu_thresh = otsu_threshold(gambar)
    # Keterangan: Inisialisasi atau perbarui variabel adaptive_mean.
    adaptive_mean = adaptive_mean_threshold(gambar, 255, BLOCK_SIZE, C_VALUE)
    # Keterangan: Inisialisasi atau perbarui variabel adaptive_gauss.
    adaptive_gauss = adaptive_gaussian_threshold(gambar, 255, BLOCK_SIZE, C_VALUE)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gambar, cmap).
    axes[0, 0].imshow(gambar, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original\n(pencahayaan tidak merata)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].hist(gambar.ravel(), 256, [0, 256])
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].axvline(x).
    axes[0, 1].axvline(x=THRESHOLD_VALUE, color='r', linestyle='--', label=f'Manual ({THRESHOLD_VALUE})')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].axvline(x).
    axes[0, 1].axvline(x=otsu_thresh, color='g', linestyle='--', label=f'Otsu ({otsu_thresh:.0f})')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].legend()
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Histogram")
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(global_thresh, cmap).
    axes[0, 2].imshow(global_thresh, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"Global Binary\n(thresh).
    axes[0, 2].set_title(f"Global Binary\n(thresh={THRESHOLD_VALUE})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Baris 2
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(otsu_result, cmap).
    axes[1, 0].imshow(otsu_result, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].set_title(f"Otsu's Method\n(auto thresh).
    axes[1, 0].set_title(f"Otsu's Method\n(auto thresh={otsu_thresh:.0f})")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(adaptive_mean, cmap).
    axes[1, 1].imshow(adaptive_mean, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].set_title(f"Adaptive Mean\n(block).
    axes[1, 1].set_title(f"Adaptive Mean\n(block={BLOCK_SIZE}, C={C_VALUE})")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(adaptive_gauss, cmap).
    axes[1, 2].imshow(adaptive_gauss, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].set_title(f"Adaptive Gaussian\n(block).
    axes[1, 2].set_title(f"Adaptive Gaussian\n(block={BLOCK_SIZE}, C={C_VALUE})")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Metode Thresholding", fontsize).
    plt.suptitle("Perbandingan Metode Thresholding", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_adaptive_parameters.
def demo_adaptive_parameters():
    """
    Demonstrasi pengaruh parameter adaptive threshold
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PENGARUH PARAMETER ADAPTIVE THRESHOLD")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
PARAMETER ADAPTIVE THRESHOLD:

BLOCK_SIZE:
├── Ukuran neighborhood untuk menghitung threshold lokal
├── Harus ganjil (3, 5, 7, 11, ...)
├── Nilai kecil: lebih sensitif terhadap detail
└── Nilai besar: lebih smooth, kurang noise

C (Constant):
├── Nilai yang dikurangi dari mean/weighted mean
├── C > 0: threshold lebih rendah (lebih banyak foreground)
└── C < 0: threshold lebih tinggi (lebih banyak background)
    """)
    
    # Keterangan: Inisialisasi atau perbarui variabel gambar.
    gambar = buat_gambar_dokumen()
    
    # Variasi block size
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Baris 1: Variasi block size
    # Keterangan: Inisialisasi atau perbarui variabel block_sizes.
    block_sizes = [3, 7, 11, 21]
    # Keterangan: Mulai loop dengan for i, bs in enumerate(block_sizes).
    for i, bs in enumerate(block_sizes):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adaptive_gaussian_threshold(gambar, 255, bs, C_VALUE)
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].imshow(hasil, cmap).
        axes[0, i].imshow(hasil, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].set_title(f"Block Size).
        axes[0, i].set_title(f"Block Size = {bs}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
    
    # Baris 2: Variasi C
    # Keterangan: Inisialisasi atau perbarui variabel c_values.
    c_values = [-5, 0, 5, 10]
    # Keterangan: Mulai loop dengan for i, c in enumerate(c_values).
    for i, c in enumerate(c_values):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adaptive_gaussian_threshold(gambar, 255, BLOCK_SIZE, c)
        # Keterangan: Inisialisasi beberapa variabel (axes[1, i].imshow(hasil, cmap).
        axes[1, i].imshow(hasil, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (axes[1, i].set_title(f"C).
        axes[1, i].set_title(f"C = {c}")
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle(f"Pengaruh Parameter (atas: block_size variasi, C).
    plt.suptitle(f"Pengaruh Parameter (atas: block_size variasi, C={C_VALUE})\n(bawah: C variasi, block_size={BLOCK_SIZE})", fontsize=12)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_otsu_bimodal.
def demo_otsu_bimodal():
    """
    Demonstrasi kapan Otsu's method bekerja dengan baik
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("OTSU'S METHOD DAN HISTOGRAM BIMODAL")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
OTSU'S METHOD bekerja optimal ketika:
├── Histogram BIMODAL (dua puncak)
├── Background dan foreground memiliki intensitas berbeda
└── Transisi yang jelas antara keduanya

TIDAK OPTIMAL ketika:
├── Histogram MULTIMODAL (lebih dari dua puncak)
├── Pencahayaan tidak merata
└── Object dan background memiliki intensitas serupa
    """)
    
    # Buat gambar dengan histogram bimodal (ideal untuk Otsu)
    # Keterangan: Inisialisasi array bernilai nol.
    gambar_bimodal = np.zeros((200, 200), dtype=np.uint8)
    # Keterangan: Inisialisasi beberapa variabel (gambar_bimodal[:100, :]).
    gambar_bimodal[:100, :] = np.random.randint(40, 80, (100, 200))  # Background
    # Keterangan: Inisialisasi beberapa variabel (gambar_bimodal[100:, :]).
    gambar_bimodal[100:, :] = np.random.randint(180, 220, (100, 200))  # Foreground
    
    # Buat gambar dengan histogram unimodal (tidak ideal)
    # Keterangan: Inisialisasi atau perbarui variabel gambar_unimodal.
    gambar_unimodal = np.random.randint(100, 160, (200, 200), dtype=np.uint8)
    
    # Apply Otsu
    # Keterangan: Inisialisasi beberapa variabel (hasil_bimodal, thresh_bimodal).
    hasil_bimodal, thresh_bimodal = otsu_threshold(gambar_bimodal)
    # Keterangan: Inisialisasi beberapa variabel (hasil_unimodal, thresh_unimodal).
    hasil_unimodal, thresh_unimodal = otsu_threshold(gambar_unimodal)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Bimodal
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gambar_bimodal, cmap).
    axes[0, 0].imshow(gambar_bimodal, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Bimodal Image")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].hist(gambar_bimodal.ravel(), 256, [0, 256])
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].axvline(x).
    axes[0, 1].axvline(x=thresh_bimodal, color='r', linestyle='--', label=f'Otsu: {thresh_bimodal:.0f}')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].legend()
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Histogram (BIMODAL)")
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(hasil_bimodal, cmap).
    axes[0, 2].imshow(hasil_bimodal, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"Otsu Result (thresh).
    axes[0, 2].set_title(f"Otsu Result (thresh={thresh_bimodal:.0f})\n✓ Bekerja dengan baik")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Unimodal
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(gambar_unimodal, cmap).
    axes[1, 0].imshow(gambar_unimodal, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Unimodal Image")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].hist(gambar_unimodal.ravel(), 256, [0, 256])
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].axvline(x).
    axes[1, 1].axvline(x=thresh_unimodal, color='r', linestyle='--', label=f'Otsu: {thresh_unimodal:.0f}')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].legend()
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Histogram (UNIMODAL)")
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(hasil_unimodal, cmap).
    axes[1, 2].imshow(hasil_unimodal, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].set_title(f"Otsu Result (thresh).
    axes[1, 2].set_title(f"Otsu Result (thresh={thresh_unimodal:.0f})\n✗ Hasil kurang optimal")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Otsu's Method: Bimodal vs Unimodal Histogram", fontsize).
    plt.suptitle("Otsu's Method: Bimodal vs Unimodal Histogram", fontsize=14)
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
    print("PRAKTIKUM: THRESHOLDING")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
THRESHOLDING adalah teknik segmentasi sederhana
# Keterangan: Jalankan perintah berikut.
untuk memisahkan objek dari background berdasarkan
# Keterangan: Jalankan perintah berikut.
intensitas piksel.

# Keterangan: Mulai blok kode baru.
Aplikasi:
# Keterangan: Jalankan perintah berikut.
├── Document binarization (OCR preprocessing)
# Keterangan: Jalankan perintah berikut.
├── Object detection sederhana
# Keterangan: Jalankan perintah berikut.
├── Background removal
# Keterangan: Jalankan perintah berikut.
└── Quality inspection
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    else:
        print("[INFO] Membuat gambar dokumen sample...")
        gambar = buat_gambar_dokumen()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Threshold value: {THRESHOLD_VALUE}")
    print(f"[INFO] Block size: {BLOCK_SIZE}")
    print(f"[INFO] C value: {C_VALUE}")
    
    # Terapkan threshold
    hasil_binary, _ = binary_threshold(gambar, THRESHOLD_VALUE)
    hasil_adaptive = adaptive_gaussian_threshold(gambar, 255, BLOCK_SIZE, C_VALUE)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(gambar, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(hasil_binary, cmap='gray')
    axes[1].set_title(f"Binary Threshold (T={THRESHOLD_VALUE})")
    axes[1].axis('off')
    
    axes[2].imshow(hasil_adaptive, cmap='gray')
    axes[2].set_title(f"Adaptive Gaussian (block={BLOCK_SIZE}, C={C_VALUE})")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_threshold_types()
    demo_global_vs_adaptive()
    demo_adaptive_parameters()
    demo_otsu_bimodal()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN THRESHOLDING")
    print("=" * 60)
    print("""
# Keterangan: Mulai blok kode baru.
FUNGSI OPENCV:

# Global Threshold
# Keterangan: Inisialisasi beberapa variabel (ret, result).
ret, result = cv2.threshold(src, thresh, maxval, type)
# type: THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO

# Otsu's Method
# Keterangan: Inisialisasi beberapa variabel (ret, result).
ret, result = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive Threshold
# Keterangan: Inisialisasi atau perbarui variabel result.
result = cv2.adaptiveThreshold(src, maxval, adaptiveMethod, 
                                # Keterangan: Jalankan perintah berikut.
                                thresholdType, blockSize, C)
# adaptiveMethod: ADAPTIVE_THRESH_MEAN_C, ADAPTIVE_THRESH_GAUSSIAN_C

# Keterangan: Mulai blok kode baru.
KAPAN MENGGUNAKAN:
# Keterangan: Jalankan perintah berikut.
├── Global: pencahayaan merata, objek kontras tinggi
# Keterangan: Jalankan perintah berikut.
├── Otsu: histogram bimodal, tidak tahu threshold optimal
# Keterangan: Jalankan perintah berikut.
└── Adaptive: pencahayaan tidak merata, dokumen, shadow

# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
1. Analisis histogram untuk memilih metode
# Keterangan: Jalankan perintah berikut.
2. Preprocessing (blur) dapat membantu mengurangi noise
# Keterangan: Jalankan perintah berikut.
3. Untuk dokumen, adaptive Gaussian biasanya lebih baik
# Keterangan: Jalankan perintah berikut.
4. Block size yang lebih besar untuk gambar resolusi tinggi
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
