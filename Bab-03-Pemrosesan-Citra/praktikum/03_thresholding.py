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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Threshold value untuk binary threshold
# Range: 0-255
THRESHOLD_VALUE = 127

# 3. Maximum value (nilai untuk piksel yang melewati threshold)
MAX_VALUE = 255

# 4. Block size untuk adaptive threshold (harus ganjil)
BLOCK_SIZE = 11

# 5. Konstanta C untuk adaptive threshold
# Nilai yang dikurangi dari mean/weighted mean
C_VALUE = 2

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


def buat_gambar_dokumen():
    """Membuat gambar simulasi dokumen dengan pencahayaan tidak merata"""
    gambar = np.zeros((400, 600), dtype=np.uint8)
    
    # Background dengan gradient (simulasi pencahayaan tidak merata)
    for i in range(400):
        for j in range(600):
            # Gradient dari kiri (gelap) ke kanan (terang)
            gambar[i, j] = int(100 + j/4 + np.random.randint(-10, 10))
    
    # Tambahkan "teks" (garis hitam)
    for row in range(5):
        y = 50 + row * 70
        for line in range(3):
            x_start = 50 + line * 30
            length = np.random.randint(100, 200)
            cv2.line(gambar, (x_start, y + line*15), (x_start + length, y + line*15), 0, 2)
    
    # Tambahkan lingkaran (logo)
    cv2.circle(gambar, (500, 100), 40, 50, -1)
    cv2.circle(gambar, (500, 100), 30, 0, -1)
    
    return gambar


# ============================================================
# FUNGSI THRESHOLDING
# ============================================================

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
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_BINARY)
    return hasil, thresh


def binary_threshold_inverse(gambar, thresh, max_val=255):
    """
    Binary threshold inverse
    
    Formula:
    output(x,y) = 0        if input(x,y) > thresh
    output(x,y) = max_val  otherwise
    """
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_BINARY_INV)
    return hasil, thresh


def truncate_threshold(gambar, thresh, max_val=255):
    """
    Truncate threshold
    
    Formula:
    output(x,y) = thresh    if input(x,y) > thresh
    output(x,y) = input(x,y) otherwise
    """
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_TRUNC)
    return hasil, thresh


def to_zero_threshold(gambar, thresh, max_val=255):
    """
    To-zero threshold
    
    Formula:
    output(x,y) = input(x,y)  if input(x,y) > thresh
    output(x,y) = 0           otherwise
    """
    _, hasil = cv2.threshold(gambar, thresh, max_val, cv2.THRESH_TOZERO)
    return hasil, thresh


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
    thresh, hasil = cv2.threshold(gambar, 0, max_val, 
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return hasil, thresh


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
    hasil = cv2.adaptiveThreshold(gambar, max_val, 
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, block_size, C)
    return hasil


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
    hasil = cv2.adaptiveThreshold(gambar, max_val,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, block_size, C)
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_threshold_types():
    """
    Demonstrasi berbagai jenis threshold
    """
    print("\n" + "=" * 60)
    print("BERBAGAI JENIS THRESHOLD")
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
    gradient = np.zeros((100, 256), dtype=np.uint8)
    for j in range(256):
        gradient[:, j] = j
    
    thresh = 127
    
    # Berbagai jenis threshold
    types = [
        (cv2.THRESH_BINARY, "BINARY"),
        (cv2.THRESH_BINARY_INV, "BINARY_INV"),
        (cv2.THRESH_TRUNC, "TRUNC"),
        (cv2.THRESH_TOZERO, "TOZERO"),
        (cv2.THRESH_TOZERO_INV, "TOZERO_INV"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    # Original
    axes[0].imshow(gradient, cmap='gray')
    axes[0].set_title("Original Gradient")
    axes[0].axis('off')
    
    for i, (thresh_type, name) in enumerate(types, 1):
        _, hasil = cv2.threshold(gradient, thresh, 255, thresh_type)
        axes[i].imshow(hasil, cmap='gray')
        axes[i].set_title(f"{name}\n(thresh={thresh})")
        axes[i].axis('off')
    
    plt.suptitle("Berbagai Jenis Threshold pada Gradient", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_global_vs_adaptive():
    """
    Perbandingan global threshold vs adaptive threshold
    """
    print("\n" + "=" * 60)
    print("GLOBAL vs ADAPTIVE THRESHOLD")
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
    gambar = buat_gambar_dokumen()
    
    # Apply different thresholds
    global_thresh, _ = binary_threshold(gambar, THRESHOLD_VALUE)
    otsu_result, otsu_thresh = otsu_threshold(gambar)
    adaptive_mean = adaptive_mean_threshold(gambar, 255, BLOCK_SIZE, C_VALUE)
    adaptive_gauss = adaptive_gaussian_threshold(gambar, 255, BLOCK_SIZE, C_VALUE)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1
    axes[0, 0].imshow(gambar, cmap='gray')
    axes[0, 0].set_title("Original\n(pencahayaan tidak merata)")
    axes[0, 0].axis('off')
    
    axes[0, 1].hist(gambar.ravel(), 256, [0, 256])
    axes[0, 1].axvline(x=THRESHOLD_VALUE, color='r', linestyle='--', label=f'Manual ({THRESHOLD_VALUE})')
    axes[0, 1].axvline(x=otsu_thresh, color='g', linestyle='--', label=f'Otsu ({otsu_thresh:.0f})')
    axes[0, 1].legend()
    axes[0, 1].set_title("Histogram")
    
    axes[0, 2].imshow(global_thresh, cmap='gray')
    axes[0, 2].set_title(f"Global Binary\n(thresh={THRESHOLD_VALUE})")
    axes[0, 2].axis('off')
    
    # Baris 2
    axes[1, 0].imshow(otsu_result, cmap='gray')
    axes[1, 0].set_title(f"Otsu's Method\n(auto thresh={otsu_thresh:.0f})")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(adaptive_mean, cmap='gray')
    axes[1, 1].set_title(f"Adaptive Mean\n(block={BLOCK_SIZE}, C={C_VALUE})")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(adaptive_gauss, cmap='gray')
    axes[1, 2].set_title(f"Adaptive Gaussian\n(block={BLOCK_SIZE}, C={C_VALUE})")
    axes[1, 2].axis('off')
    
    plt.suptitle("Perbandingan Metode Thresholding", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_adaptive_parameters():
    """
    Demonstrasi pengaruh parameter adaptive threshold
    """
    print("\n" + "=" * 60)
    print("PENGARUH PARAMETER ADAPTIVE THRESHOLD")
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
    
    gambar = buat_gambar_dokumen()
    
    # Variasi block size
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Baris 1: Variasi block size
    block_sizes = [3, 7, 11, 21]
    for i, bs in enumerate(block_sizes):
        hasil = adaptive_gaussian_threshold(gambar, 255, bs, C_VALUE)
        axes[0, i].imshow(hasil, cmap='gray')
        axes[0, i].set_title(f"Block Size = {bs}")
        axes[0, i].axis('off')
    
    # Baris 2: Variasi C
    c_values = [-5, 0, 5, 10]
    for i, c in enumerate(c_values):
        hasil = adaptive_gaussian_threshold(gambar, 255, BLOCK_SIZE, c)
        axes[1, i].imshow(hasil, cmap='gray')
        axes[1, i].set_title(f"C = {c}")
        axes[1, i].axis('off')
    
    plt.suptitle(f"Pengaruh Parameter (atas: block_size variasi, C={C_VALUE})\n(bawah: C variasi, block_size={BLOCK_SIZE})", fontsize=12)
    plt.tight_layout()
    plt.show()


def demo_otsu_bimodal():
    """
    Demonstrasi kapan Otsu's method bekerja dengan baik
    """
    print("\n" + "=" * 60)
    print("OTSU'S METHOD DAN HISTOGRAM BIMODAL")
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
    gambar_bimodal = np.zeros((200, 200), dtype=np.uint8)
    gambar_bimodal[:100, :] = np.random.randint(40, 80, (100, 200))  # Background
    gambar_bimodal[100:, :] = np.random.randint(180, 220, (100, 200))  # Foreground
    
    # Buat gambar dengan histogram unimodal (tidak ideal)
    gambar_unimodal = np.random.randint(100, 160, (200, 200), dtype=np.uint8)
    
    # Apply Otsu
    hasil_bimodal, thresh_bimodal = otsu_threshold(gambar_bimodal)
    hasil_unimodal, thresh_unimodal = otsu_threshold(gambar_unimodal)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Bimodal
    axes[0, 0].imshow(gambar_bimodal, cmap='gray')
    axes[0, 0].set_title("Bimodal Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].hist(gambar_bimodal.ravel(), 256, [0, 256])
    axes[0, 1].axvline(x=thresh_bimodal, color='r', linestyle='--', label=f'Otsu: {thresh_bimodal:.0f}')
    axes[0, 1].legend()
    axes[0, 1].set_title("Histogram (BIMODAL)")
    
    axes[0, 2].imshow(hasil_bimodal, cmap='gray')
    axes[0, 2].set_title(f"Otsu Result (thresh={thresh_bimodal:.0f})\n✓ Bekerja dengan baik")
    axes[0, 2].axis('off')
    
    # Unimodal
    axes[1, 0].imshow(gambar_unimodal, cmap='gray')
    axes[1, 0].set_title("Unimodal Image")
    axes[1, 0].axis('off')
    
    axes[1, 1].hist(gambar_unimodal.ravel(), 256, [0, 256])
    axes[1, 1].axvline(x=thresh_unimodal, color='r', linestyle='--', label=f'Otsu: {thresh_unimodal:.0f}')
    axes[1, 1].legend()
    axes[1, 1].set_title("Histogram (UNIMODAL)")
    
    axes[1, 2].imshow(hasil_unimodal, cmap='gray')
    axes[1, 2].set_title(f"Otsu Result (thresh={thresh_unimodal:.0f})\n✗ Hasil kurang optimal")
    axes[1, 2].axis('off')
    
    plt.suptitle("Otsu's Method: Bimodal vs Unimodal Histogram", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: THRESHOLDING")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
THRESHOLDING adalah teknik segmentasi sederhana
untuk memisahkan objek dari background berdasarkan
intensitas piksel.

Aplikasi:
├── Document binarization (OCR preprocessing)
├── Object detection sederhana
├── Background removal
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
FUNGSI OPENCV:

# Global Threshold
ret, result = cv2.threshold(src, thresh, maxval, type)
# type: THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO

# Otsu's Method
ret, result = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive Threshold
result = cv2.adaptiveThreshold(src, maxval, adaptiveMethod, 
                                thresholdType, blockSize, C)
# adaptiveMethod: ADAPTIVE_THRESH_MEAN_C, ADAPTIVE_THRESH_GAUSSIAN_C

KAPAN MENGGUNAKAN:
├── Global: pencahayaan merata, objek kontras tinggi
├── Otsu: histogram bimodal, tidak tahu threshold optimal
└── Adaptive: pencahayaan tidak merata, dokumen, shadow

TIPS:
1. Analisis histogram untuk memilih metode
2. Preprocessing (blur) dapat membantu mengurangi noise
3. Untuk dokumen, adaptive Gaussian biasanya lebih baik
4. Block size yang lebih besar untuk gambar resolusi tinggi
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
