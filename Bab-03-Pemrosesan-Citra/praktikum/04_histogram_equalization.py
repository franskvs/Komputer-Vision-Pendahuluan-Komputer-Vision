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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. CLAHE Clip Limit
# Membatasi amplifikasi kontras untuk menghindari noise amplification
# Range: 1.0 - 10.0 (default: 2.0)
CLAHE_CLIP_LIMIT = 2.0

# 3. CLAHE Tile Grid Size
# Ukuran tile untuk local histogram equalization
CLAHE_TILE_SIZE = (8, 8)

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


def buat_gambar_low_contrast():
    """Membuat gambar dengan kontras rendah"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background dengan range intensitas sempit (100-150)
    for i in range(400):
        for j in range(600):
            base = 125 + np.random.randint(-25, 25)
            gambar[i, j] = [base, base, base]
    
    # Objek dengan intensitas sedikit berbeda
    cv2.rectangle(gambar, (50, 50), (200, 150), (110, 110, 110), -1)
    cv2.circle(gambar, (400, 200), 80, (140, 140, 140), -1)
    cv2.putText(gambar, "LOW", (200, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (115, 115, 115), 5)
    
    return gambar


# ============================================================
# FUNGSI HISTOGRAM
# ============================================================

def hitung_histogram(gambar):
    """
    Menghitung histogram dari gambar grayscale
    
    Parameter:
    - gambar: input image (grayscale)
    
    Return:
    - histogram: array 256 nilai
    """
    hist = cv2.calcHist([gambar], [0], None, [256], [0, 256])
    return hist.flatten()


def hitung_cdf(histogram):
    """
    Menghitung Cumulative Distribution Function (CDF)
    
    Parameter:
    - histogram: array histogram
    
    Return:
    - cdf: cumulative distribution function
    """
    cdf = histogram.cumsum()
    cdf_normalized = cdf / cdf.max()  # Normalize to [0, 1]
    return cdf_normalized


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
    hist = hitung_histogram(gambar)
    
    # Hitung CDF
    cdf = hist.cumsum()
    
    # Mask CDF di mana nilai = 0
    cdf_masked = np.ma.masked_equal(cdf, 0)
    
    # Normalize CDF ke range [0, 255]
    cdf_normalized = ((cdf_masked - cdf_masked.min()) * 255 / 
                      (cdf_masked.max() - cdf_masked.min()))
    cdf_final = np.ma.filled(cdf_normalized, 0).astype(np.uint8)
    
    # Map nilai piksel
    hasil = cdf_final[gambar]
    
    return hasil


def histogram_equalization(gambar):
    """
    Histogram equalization menggunakan OpenCV
    
    Parameter:
    - gambar: input grayscale image
    
    Return:
    - gambar dengan kontras yang sudah di-equalize
    """
    hasil = cv2.equalizeHist(gambar)
    return hasil


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
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    hasil = clahe.apply(gambar)
    return hasil


def histogram_equalization_color(gambar):
    """
    Histogram equalization untuk gambar berwarna
    
    Metode: Convert ke YCrCb, equalize channel Y (luminance)
    """
    # Convert BGR ke YCrCb
    ycrcb = cv2.cvtColor(gambar, cv2.COLOR_BGR2YCrCb)
    
    # Equalize channel Y (luminance)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    
    # Convert kembali ke BGR
    hasil = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    
    return hasil


def clahe_color(gambar, clip_limit=2.0, tile_size=(8, 8)):
    """
    CLAHE untuk gambar berwarna
    """
    # Convert BGR ke LAB
    lab = cv2.cvtColor(gambar, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE ke channel L (lightness)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    
    # Convert kembali ke BGR
    hasil = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_histogram_equalization_step():
    """
    Demonstrasi langkah-langkah histogram equalization
    """
    print("\n" + "=" * 60)
    print("LANGKAH-LANGKAH HISTOGRAM EQUALIZATION")
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
    gambar_bgr = buat_gambar_low_contrast()
    gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Hitung histogram dan CDF sebelum
    hist_before = hitung_histogram(gambar)
    cdf_before = hitung_cdf(hist_before)
    
    # Apply equalization
    hasil = histogram_equalization(gambar)
    
    # Hitung histogram dan CDF sesudah
    hist_after = hitung_histogram(hasil)
    cdf_after = hitung_cdf(hist_after)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1: Sebelum
    axes[0, 0].imshow(gambar, cmap='gray')
    axes[0, 0].set_title("Original (Low Contrast)")
    axes[0, 0].axis('off')
    
    axes[0, 1].bar(range(256), hist_before, width=1)
    axes[0, 1].set_title("Histogram Original")
    axes[0, 1].set_xlim([0, 256])
    
    axes[0, 2].plot(cdf_before)
    axes[0, 2].plot([0, 255], [0, 1], 'r--', alpha=0.5, label='Ideal')
    axes[0, 2].set_title("CDF Original")
    axes[0, 2].legend()
    
    # Baris 2: Sesudah
    axes[1, 0].imshow(hasil, cmap='gray')
    axes[1, 0].set_title("After Equalization")
    axes[1, 0].axis('off')
    
    axes[1, 1].bar(range(256), hist_after, width=1)
    axes[1, 1].set_title("Histogram Equalized")
    axes[1, 1].set_xlim([0, 256])
    
    axes[1, 2].plot(cdf_after)
    axes[1, 2].plot([0, 255], [0, 1], 'r--', alpha=0.5, label='Ideal')
    axes[1, 2].set_title("CDF Equalized")
    axes[1, 2].legend()
    
    plt.suptitle("Histogram Equalization: Step by Step", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_global_vs_clahe():
    """
    Perbandingan global equalization vs CLAHE
    """
    print("\n" + "=" * 60)
    print("GLOBAL EQUALIZATION vs CLAHE")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    else:
        gambar_bgr = buat_gambar_low_contrast()
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Apply different methods
    global_eq = histogram_equalization(gambar)
    clahe_result = clahe_equalization(gambar, CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Baris 1: Gambar
    axes[0, 0].imshow(gambar, cmap='gray')
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(global_eq, cmap='gray')
    axes[0, 1].set_title("Global Equalization")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(clahe_result, cmap='gray')
    axes[0, 2].set_title(f"CLAHE (clip={CLAHE_CLIP_LIMIT}, tile={CLAHE_TILE_SIZE})")
    axes[0, 2].axis('off')
    
    # Baris 2: Histogram
    axes[1, 0].hist(gambar.ravel(), 256, [0, 256])
    axes[1, 0].set_title("Histogram Original")
    
    axes[1, 1].hist(global_eq.ravel(), 256, [0, 256])
    axes[1, 1].set_title("Histogram Global Eq")
    
    axes[1, 2].hist(clahe_result.ravel(), 256, [0, 256])
    axes[1, 2].set_title("Histogram CLAHE")
    
    plt.suptitle("Perbandingan Global Equalization vs CLAHE", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_clahe_parameters():
    """
    Demonstrasi pengaruh parameter CLAHE
    """
    print("\n" + "=" * 60)
    print("PENGARUH PARAMETER CLAHE")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    else:
        gambar_bgr = buat_gambar_low_contrast()
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
    
    # Variasi clip limit
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Baris 1: Variasi clip limit
    clip_limits = [1.0, 2.0, 4.0, 8.0]
    for i, clip in enumerate(clip_limits):
        hasil = clahe_equalization(gambar, clip, (8, 8))
        axes[0, i].imshow(hasil, cmap='gray')
        axes[0, i].set_title(f"Clip Limit = {clip}")
        axes[0, i].axis('off')
    
    # Baris 2: Variasi tile size
    tile_sizes = [(4, 4), (8, 8), (16, 16), (32, 32)]
    for i, tile in enumerate(tile_sizes):
        hasil = clahe_equalization(gambar, 2.0, tile)
        axes[1, i].imshow(hasil, cmap='gray')
        axes[1, i].set_title(f"Tile Size = {tile}")
        axes[1, i].axis('off')
    
    plt.suptitle("Pengaruh Parameter CLAHE", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_color_equalization():
    """
    Demonstrasi histogram equalization untuk gambar berwarna
    """
    print("\n" + "=" * 60)
    print("HISTOGRAM EQUALIZATION UNTUK GAMBAR BERWARNA")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_low_contrast()
    
    # Method 1: Equalize RGB channels separately (SALAH!)
    gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
    equalized_wrong = np.stack([
        cv2.equalizeHist(gambar_rgb[:, :, i]) 
        for i in range(3)
    ], axis=-1)
    
    # Method 2: Equalize luminance only (BENAR)
    equalized_correct = cv2.cvtColor(
        histogram_equalization_color(gambar), cv2.COLOR_BGR2RGB
    )
    
    # Method 3: CLAHE on color
    clahe_result = cv2.cvtColor(clahe_color(gambar), cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(equalized_wrong)
    axes[0, 1].set_title("RGB Equalized (SALAH)\nWarna berubah tidak natural")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(equalized_correct)
    axes[1, 0].set_title("Luminance Equalized (BENAR)\nWarna terjaga")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(clahe_result)
    axes[1, 1].set_title("CLAHE on LAB\n(Best for most cases)")
    axes[1, 1].axis('off')
    
    plt.suptitle("Histogram Equalization pada Gambar Berwarna", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: HISTOGRAM EQUALIZATION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
HISTOGRAM EQUALIZATION adalah teknik untuk meningkatkan
kontras gambar dengan mendistribusikan ulang intensitas
piksel sehingga histogram menjadi lebih uniform.

Aplikasi:
├── Medical imaging (X-ray, CT, MRI enhancement)
├── Satellite image processing
├── Low-light image enhancement
├── Preprocessing untuk computer vision
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
FUNGSI OPENCV:

# Global Histogram Equalization (Grayscale)
result = cv2.equalizeHist(gray_image)

# CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
result = clahe.apply(gray_image)

# Untuk gambar berwarna (YCrCb)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0])
result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# Untuk gambar berwarna (LAB) - CLAHE
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
lab[:,:,0] = clahe.apply(lab[:,:,0])
result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

KAPAN MENGGUNAKAN:
├── Global: gambar dengan kontras uniform rendah
├── CLAHE: gambar dengan variasi lokal, medical imaging
└── Hindari untuk gambar yang sudah high contrast

TIPS:
1. Untuk gambar berwarna, equalize luminance saja
2. CLAHE dengan clip_limit rendah untuk hasil natural
3. Tile size kecil untuk detail lokal, besar untuk smooth
4. Preprocessing blur dapat membantu mengurangi noise
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
