# ============================================================
# PROGRAM: 04_histogram_equalization.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk histogram equalization dan CLAHE
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep histogram equalization
#   2. Perbedaan global equalization vs CLAHE
#   3. Aplikasi untuk peningkatan kontras
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

# 2. CLAHE Clip Limit
# Membatasi amplifikasi kontras untuk menghindari noise amplification
# Range: 1.0 - 10.0 (default: 2.0)
# Keterangan: Inisialisasi atau perbarui variabel CLAHE_CLIP_LIMIT.
CLAHE_CLIP_LIMIT = 2.0

# 3. CLAHE Tile Grid Size
# Ukuran tile untuk local histogram equalization
# Keterangan: Inisialisasi atau perbarui variabel CLAHE_TILE_SIZE.
CLAHE_TILE_SIZE = (8, 8)

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


def buat_gambar_low_contrast():
    """Membuat gambar dengan kontras rendah"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background dengan range intensitas sempit (100-150)
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Mulai loop dengan for j in range(600).
        for j in range(600):
            # Keterangan: Inisialisasi atau perbarui variabel base.
            base = 125 + np.random.randint(-25, 25)
            # Keterangan: Inisialisasi beberapa variabel (gambar[i, j]).
            gambar[i, j] = [base, base, base]
    
    # Objek dengan intensitas sedikit berbeda
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), (110, 110, 110), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 200), 80, (140, 140, 140), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "LOW", (200, 350), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 2, (115, 115, 115), 5)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# ============================================================
# FUNGSI HISTOGRAM
# ============================================================

# Keterangan: Definisikan fungsi hitung_histogram.
def hitung_histogram(gambar):
    """
    Menghitung histogram dari gambar grayscale
    
    Parameter:
    - gambar: input image (grayscale)
    
    Return:
    - histogram: array 256 nilai
    """
    # Keterangan: Inisialisasi atau perbarui variabel hist.
    hist = cv2.calcHist([gambar], [0], None, [256], [0, 256])
    # Keterangan: Kembalikan hasil dari fungsi.
    return hist.flatten()


# Keterangan: Definisikan fungsi hitung_cdf.
def hitung_cdf(histogram):
    """
    Menghitung Cumulative Distribution Function (CDF)
    
    Parameter:
    - histogram: array histogram
    
    Return:
    - cdf: cumulative distribution function
    """
    # Keterangan: Inisialisasi atau perbarui variabel cdf.
    cdf = histogram.cumsum()
    # Keterangan: Inisialisasi atau perbarui variabel cdf_normalized.
    cdf_normalized = cdf / cdf.max()  # Normalize to [0, 1]
    # Keterangan: Kembalikan hasil dari fungsi.
    return cdf_normalized


# Keterangan: Definisikan fungsi histogram_equalization_manual.
def histogram_equalization_manual(gambar):
    """
    Implementasi manual histogram equalization untuk pemahaman
    
    Langkah-langkah:
    1. Hitung histogram
    2. Hitung CDF
    3. Normalize CDF ke range [0, 255]
    4. Map setiap piksel ke nilai baru
    """
    # Hitung histogram
    # Keterangan: Inisialisasi atau perbarui variabel hist.
    hist = hitung_histogram(gambar)
    
    # Hitung CDF
    # Keterangan: Inisialisasi atau perbarui variabel cdf.
    cdf = hist.cumsum()
    
    # Mask CDF di mana nilai = 0
    # Keterangan: Inisialisasi atau perbarui variabel cdf_masked.
    cdf_masked = np.ma.masked_equal(cdf, 0)
    
    # Normalize CDF ke range [0, 255]
    # Keterangan: Inisialisasi atau perbarui variabel cdf_normalized.
    cdf_normalized = ((cdf_masked - cdf_masked.min()) * 255 / 
                      # Keterangan: Jalankan perintah berikut.
                      (cdf_masked.max() - cdf_masked.min()))
    # Keterangan: Inisialisasi atau perbarui variabel cdf_final.
    cdf_final = np.ma.filled(cdf_normalized, 0).astype(np.uint8)
    
    # Map nilai piksel
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cdf_final[gambar]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi histogram_equalization.
def histogram_equalization(gambar):
    """
    Histogram equalization menggunakan OpenCV
    
    Parameter:
    - gambar: input grayscale image
    
    Return:
    - gambar dengan kontras yang sudah di-equalize
    """
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.equalizeHist(gambar)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi clahe_equalization.
def clahe_equalization(gambar, clip_limit=2.0, tile_size=(8, 8)):
    """
    Contrast Limited Adaptive Histogram Equalization (CLAHE)
    
    Parameter:
    - gambar: input grayscale image
    - clip_limit: threshold untuk contrast limiting (default 2.0)
    - tile_size: ukuran tile untuk AHE
    
    Return:
    - gambar dengan CLAHE applied
    """
    # Keterangan: Inisialisasi atau perbarui variabel clahe.
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = clahe.apply(gambar)
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi histogram_equalization_color.
def histogram_equalization_color(gambar):
    """
    Histogram equalization untuk gambar berwarna
    
    Metode: Convert ke YCrCb, equalize channel Y (luminance)
    """
    # Convert BGR ke YCrCb
    # Keterangan: Konversi ruang warna gambar.
    ycrcb = cv2.cvtColor(gambar, cv2.COLOR_BGR2YCrCb)
    
    # Equalize channel Y (luminance)
    # Keterangan: Inisialisasi beberapa variabel (ycrcb[:, :, 0]).
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    
    # Convert kembali ke BGR
    # Keterangan: Konversi ruang warna gambar.
    hasil = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi clahe_color.
def clahe_color(gambar, clip_limit=2.0, tile_size=(8, 8)):
    """
    CLAHE untuk gambar berwarna
    """
    # Convert BGR ke LAB
    # Keterangan: Konversi ruang warna gambar.
    lab = cv2.cvtColor(gambar, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE ke channel L (lightness)
    # Keterangan: Inisialisasi atau perbarui variabel clahe.
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    # Keterangan: Inisialisasi beberapa variabel (lab[:, :, 0]).
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    
    # Convert kembali ke BGR
    # Keterangan: Konversi ruang warna gambar.
    hasil = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_histogram_equalization_step.
def demo_histogram_equalization_step():
    """
    Demonstrasi langkah-langkah histogram equalization
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("LANGKAH-LANGKAH HISTOGRAM EQUALIZATION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
ALGORITMA HISTOGRAM EQUALIZATION:

1. Hitung histogram h(k) untuk k = 0, 1, ..., 255
2. Hitung CDF: c(k) = Σ h(i) untuk i = 0 sampai k
3. Normalize CDF: s(k) = round((L-1) × c(k) / total_pixels)
4. Map setiap piksel: output(x,y) = s(input(x,y))

Tujuan: Mendistribusikan intensitas secara merata
        sehingga CDF mendekati garis linear
    """)
    
    # Buat gambar low contrast
    # Keterangan: Inisialisasi atau perbarui variabel gambar_bgr.
    gambar_bgr = buat_gambar_low_contrast()
    # Keterangan: Konversi ruang warna gambar.
    gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Hitung histogram dan CDF sebelum
    # Keterangan: Inisialisasi atau perbarui variabel hist_before.
    hist_before = hitung_histogram(gambar)
    # Keterangan: Inisialisasi atau perbarui variabel cdf_before.
    cdf_before = hitung_cdf(hist_before)
    
    # Apply equalization
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = histogram_equalization(gambar)
    
    # Hitung histogram dan CDF sesudah
    # Keterangan: Inisialisasi atau perbarui variabel hist_after.
    hist_after = hitung_histogram(hasil)
    # Keterangan: Inisialisasi atau perbarui variabel cdf_after.
    cdf_after = hitung_cdf(hist_after)
    
    # Visualisasi
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1: Sebelum
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gambar, cmap).
    axes[0, 0].imshow(gambar, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original (Low Contrast)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].bar(range(256), hist_before, width).
    axes[0, 1].bar(range(256), hist_before, width=1)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Histogram Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_xlim([0, 256])
    
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].plot(cdf_before)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].plot([0, 255], [0, 1], 'r--', alpha).
    axes[0, 2].plot([0, 255], [0, 1], 'r--', alpha=0.5, label='Ideal')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("CDF Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].legend()
    
    # Baris 2: Sesudah
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(hasil, cmap).
    axes[1, 0].imshow(hasil, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("After Equalization")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].bar(range(256), hist_after, width).
    axes[1, 1].bar(range(256), hist_after, width=1)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Histogram Equalized")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_xlim([0, 256])
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].plot(cdf_after)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].plot([0, 255], [0, 1], 'r--', alpha).
    axes[1, 2].plot([0, 255], [0, 1], 'r--', alpha=0.5, label='Ideal')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("CDF Equalized")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].legend()
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Histogram Equalization: Step by Step", fontsize).
    plt.suptitle("Histogram Equalization: Step by Step", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_global_vs_clahe.
def demo_global_vs_clahe():
    """
    Perbandingan global equalization vs CLAHE
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("GLOBAL EQUALIZATION vs CLAHE")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
GLOBAL HISTOGRAM EQUALIZATION:
├── Menggunakan histogram dari seluruh gambar
├── Cepat dan sederhana
├── Dapat over-enhance beberapa area
└── Tidak cocok untuk pencahayaan tidak merata

CLAHE (Contrast Limited Adaptive Histogram Equalization):
├── Membagi gambar menjadi tiles
├── Equalize histogram per tile
├── Clip limit mencegah over-amplification
├── Interpolasi antar tile untuk menghindari artifacts
└── Lebih baik untuk gambar dengan variasi lokal
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar_bgr.
        gambar_bgr = buat_gambar_low_contrast()
        # Keterangan: Konversi ruang warna gambar.
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Apply different methods
    # Keterangan: Inisialisasi atau perbarui variabel global_eq.
    global_eq = histogram_equalization(gambar)
    # Keterangan: Inisialisasi atau perbarui variabel clahe_result.
    clahe_result = clahe_equalization(gambar, CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1: Gambar
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gambar, cmap).
    axes[0, 0].imshow(gambar, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(global_eq, cmap).
    axes[0, 1].imshow(global_eq, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Global Equalization")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(clahe_result, cmap).
    axes[0, 2].imshow(clahe_result, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"CLAHE (clip).
    axes[0, 2].set_title(f"CLAHE (clip={CLAHE_CLIP_LIMIT}, tile={CLAHE_TILE_SIZE})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Baris 2: Histogram
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].hist(gambar.ravel(), 256, [0, 256])
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Histogram Original")
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].hist(global_eq.ravel(), 256, [0, 256])
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Histogram Global Eq")
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].hist(clahe_result.ravel(), 256, [0, 256])
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Histogram CLAHE")
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Global Equalization vs CLAHE", fontsize).
    plt.suptitle("Perbandingan Global Equalization vs CLAHE", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_clahe_parameters.
def demo_clahe_parameters():
    """
    Demonstrasi pengaruh parameter CLAHE
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PENGARUH PARAMETER CLAHE")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
PARAMETER CLAHE:

CLIP LIMIT:
├── Threshold untuk histogram clipping
├── Nilai rendah: enhancement lebih subtle
├── Nilai tinggi: enhancement lebih kuat, tapi bisa noisy
└── Default: 2.0

TILE GRID SIZE:
├── Ukuran tile untuk local processing
├── Tile kecil: lebih detail, tapi bisa artifacts
├── Tile besar: lebih smooth, kurang detail lokal
└── Default: (8, 8)
    """)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar_bgr.
        gambar_bgr = buat_gambar_low_contrast()
        # Keterangan: Konversi ruang warna gambar.
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Variasi clip limit
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Baris 1: Variasi clip limit
    # Keterangan: Inisialisasi atau perbarui variabel clip_limits.
    clip_limits = [1.0, 2.0, 4.0, 8.0]
    # Keterangan: Mulai loop dengan for i, clip in enumerate(clip_limits).
    for i, clip in enumerate(clip_limits):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = clahe_equalization(gambar, clip, (8, 8))
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].imshow(hasil, cmap).
        axes[0, i].imshow(hasil, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].set_title(f"Clip Limit).
        axes[0, i].set_title(f"Clip Limit = {clip}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
    
    # Baris 2: Variasi tile size
    # Keterangan: Inisialisasi atau perbarui variabel tile_sizes.
    tile_sizes = [(4, 4), (8, 8), (16, 16), (32, 32)]
    # Keterangan: Mulai loop dengan for i, tile in enumerate(tile_sizes).
    for i, tile in enumerate(tile_sizes):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = clahe_equalization(gambar, 2.0, tile)
        # Keterangan: Inisialisasi beberapa variabel (axes[1, i].imshow(hasil, cmap).
        axes[1, i].imshow(hasil, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (axes[1, i].set_title(f"Tile Size).
        axes[1, i].set_title(f"Tile Size = {tile}")
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Pengaruh Parameter CLAHE", fontsize).
    plt.suptitle("Pengaruh Parameter CLAHE", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_color_equalization.
def demo_color_equalization():
    """
    Demonstrasi histogram equalization untuk gambar berwarna
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("HISTOGRAM EQUALIZATION UNTUK GAMBAR BERWARNA")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
STRATEGI UNTUK GAMBAR BERWARNA:

SALAH (jangan lakukan):
├── Equalize setiap channel RGB secara terpisah
└── Dapat mengubah warna secara tidak natural

BENAR:
├── Convert ke color space dengan luminance terpisah
│   ├── YCrCb (Y = luminance)
│   ├── LAB (L = lightness)
│   └── HSV (V = value)
├── Equalize hanya channel luminance/lightness
└── Convert kembali ke RGB
    """)
    
    # Load gambar berwarna
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_low_contrast()
    
    # Method 1: Equalize RGB channels separately (SALAH!)
    # Keterangan: Konversi ruang warna gambar.
    gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
    # Keterangan: Inisialisasi atau perbarui variabel equalized_wrong.
    equalized_wrong = np.stack([
        # Keterangan: Jalankan perintah berikut.
        cv2.equalizeHist(gambar_rgb[:, :, i]) 
        # Keterangan: Mulai loop dengan for i in range(3).
        for i in range(3)
    # Keterangan: Inisialisasi beberapa variabel (], axis).
    ], axis=-1)
    
    # Method 2: Equalize luminance only (BENAR)
    # Keterangan: Konversi ruang warna gambar.
    equalized_correct = cv2.cvtColor(
        # Keterangan: Jalankan perintah berikut.
        histogram_equalization_color(gambar), cv2.COLOR_BGR2RGB
    # Keterangan: Jalankan perintah berikut.
    )
    
    # Method 3: CLAHE on color
    # Keterangan: Konversi ruang warna gambar.
    clahe_result = cv2.cvtColor(clahe_color(gambar), cv2.COLOR_BGR2RGB)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].imshow(equalized_wrong)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("RGB Equalized (SALAH)\nWarna berubah tidak natural")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].imshow(equalized_correct)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Luminance Equalized (BENAR)\nWarna terjaga")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].imshow(clahe_result)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("CLAHE on LAB\n(Best for most cases)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Histogram Equalization pada Gambar Berwarna", fontsize).
    plt.suptitle("Histogram Equalization pada Gambar Berwarna", fontsize=14)
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
    print("PRAKTIKUM: HISTOGRAM EQUALIZATION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
HISTOGRAM EQUALIZATION adalah teknik untuk meningkatkan
# Keterangan: Jalankan perintah berikut.
kontras gambar dengan mendistribusikan ulang intensitas
# Keterangan: Jalankan perintah berikut.
piksel sehingga histogram menjadi lebih uniform.

# Keterangan: Mulai blok kode baru.
Aplikasi:
# Keterangan: Jalankan perintah berikut.
├── Medical imaging (X-ray, CT, MRI enhancement)
# Keterangan: Jalankan perintah berikut.
├── Satellite image processing
# Keterangan: Jalankan perintah berikut.
├── Low-light image enhancement
# Keterangan: Jalankan perintah berikut.
├── Preprocessing untuk computer vision
# Keterangan: Jalankan perintah berikut.
└── Photo editing / auto-enhance
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar_bgr = cv2.imread(path_gambar)
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    else:
        print("[INFO] Membuat gambar low contrast sample...")
        gambar_bgr = buat_gambar_low_contrast()
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] CLAHE Clip Limit: {CLAHE_CLIP_LIMIT}")
    print(f"[INFO] CLAHE Tile Size: {CLAHE_TILE_SIZE}")
    
    # Terapkan equalization
    hasil_global = histogram_equalization(gambar)
    hasil_clahe = clahe_equalization(gambar, CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(gambar, cmap='gray')
    axes[0].set_title(f"Original\nMean: {np.mean(gambar):.1f}, Std: {np.std(gambar):.1f}")
    axes[0].axis('off')
    
    axes[1].imshow(hasil_global, cmap='gray')
    axes[1].set_title(f"Global Equalization\nMean: {np.mean(hasil_global):.1f}, Std: {np.std(hasil_global):.1f}")
    axes[1].axis('off')
    
    axes[2].imshow(hasil_clahe, cmap='gray')
    axes[2].set_title(f"CLAHE\nMean: {np.mean(hasil_clahe):.1f}, Std: {np.std(hasil_clahe):.1f}")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_histogram_equalization_step()
    demo_global_vs_clahe()
    demo_clahe_parameters()
    demo_color_equalization()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN HISTOGRAM EQUALIZATION")
    print("=" * 60)
    print("""
# Keterangan: Mulai blok kode baru.
FUNGSI OPENCV:

# Global Histogram Equalization (Grayscale)
# Keterangan: Inisialisasi atau perbarui variabel result.
result = cv2.equalizeHist(gray_image)

# CLAHE
# Keterangan: Inisialisasi atau perbarui variabel clahe.
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# Keterangan: Inisialisasi atau perbarui variabel result.
result = clahe.apply(gray_image)

# Untuk gambar berwarna (YCrCb)
# Keterangan: Konversi ruang warna gambar.
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# Keterangan: Inisialisasi beberapa variabel (ycrcb[:,:,0]).
ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0])
# Keterangan: Konversi ruang warna gambar.
result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# Untuk gambar berwarna (LAB) - CLAHE
# Keterangan: Konversi ruang warna gambar.
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# Keterangan: Inisialisasi beberapa variabel (lab[:,:,0]).
lab[:,:,0] = clahe.apply(lab[:,:,0])
# Keterangan: Konversi ruang warna gambar.
result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Keterangan: Mulai blok kode baru.
KAPAN MENGGUNAKAN:
# Keterangan: Jalankan perintah berikut.
├── Global: gambar dengan kontras uniform rendah
# Keterangan: Jalankan perintah berikut.
├── CLAHE: gambar dengan variasi lokal, medical imaging
# Keterangan: Jalankan perintah berikut.
└── Hindari untuk gambar yang sudah high contrast

# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
1. Untuk gambar berwarna, equalize luminance saja
# Keterangan: Jalankan perintah berikut.
2. CLAHE dengan clip_limit rendah untuk hasil natural
# Keterangan: Jalankan perintah berikut.
3. Tile size kecil untuk detail lokal, besar untuk smooth
# Keterangan: Jalankan perintah berikut.
4. Preprocessing blur dapat membantu mengurangi noise
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
