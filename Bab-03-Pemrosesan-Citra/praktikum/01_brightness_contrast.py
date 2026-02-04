# ============================================================
# PROGRAM: 01_brightness_contrast.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk mengatur brightness dan contrast gambar
# 
# Tujuan Pembelajaran:
#   1. Memahami operasi titik (point operations)
#   2. Mengatur kecerahan (brightness) gambar
#   3. Mengatur kontras gambar
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

# 2. Nilai brightness (kecerahan)
# Range: -255 sampai 255
# Positif = lebih terang, Negatif = lebih gelap
BRIGHTNESS = 50

# 3. Nilai contrast (kontras)
# Range: 0.1 sampai 3.0
# > 1.0 = kontras meningkat, < 1.0 = kontras menurun
CONTRAST = 1.5

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
    """Membuat gambar sample jika file tidak ditemukan"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Gradient background
    for i in range(400):
        for j in range(600):
            gambar[i, j] = [
                int(50 + i/4),      # B
                int(100 + j/6),     # G
                int(150 + i/4)      # R
            ]
    
    # Tambahkan beberapa objek
    cv2.rectangle(gambar, (50, 50), (200, 150), (0, 0, 200), -1)
    cv2.circle(gambar, (400, 200), 80, (200, 200, 0), -1)
    cv2.putText(gambar, "SAMPLE", (200, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    return gambar


# ============================================================
# FUNGSI BRIGHTNESS DAN CONTRAST
# ============================================================

def adjust_brightness(gambar, beta):
    """
    Mengatur brightness gambar
    
    Formula: g(x,y) = f(x,y) + beta
    
    Parameter:
    - gambar: input image (BGR)
    - beta: nilai brightness (-255 to 255)
    
    Return:
    - gambar dengan brightness yang sudah diatur
    """
    # Metode 1: Menggunakan cv2.convertScaleAbs
    hasil = cv2.convertScaleAbs(gambar, alpha=1.0, beta=beta)
    
    return hasil


def adjust_contrast(gambar, alpha):
    """
    Mengatur contrast gambar
    
    Formula: g(x,y) = alpha * f(x,y)
    
    Parameter:
    - gambar: input image (BGR)
    - alpha: nilai contrast (0.1 to 3.0)
    
    Return:
    - gambar dengan contrast yang sudah diatur
    """
    hasil = cv2.convertScaleAbs(gambar, alpha=alpha, beta=0)
    
    return hasil


def adjust_brightness_contrast(gambar, alpha, beta):
    """
    Mengatur brightness DAN contrast gambar sekaligus
    
    Formula: g(x,y) = alpha * f(x,y) + beta
    
    Parameter:
    - gambar: input image (BGR)
    - alpha: nilai contrast (0.1 to 3.0)
    - beta: nilai brightness (-255 to 255)
    
    Return:
    - gambar dengan brightness dan contrast yang sudah diatur
    """
    hasil = cv2.convertScaleAbs(gambar, alpha=alpha, beta=beta)
    
    return hasil


def adjust_brightness_manual(gambar, beta):
    """
    Implementasi manual brightness adjustment untuk pemahaman
    """
    # Konversi ke float untuk mencegah overflow
    gambar_float = gambar.astype(np.float32)
    
    # Tambahkan beta
    hasil = gambar_float + beta
    
    # Clip ke range valid [0, 255]
    hasil = np.clip(hasil, 0, 255)
    
    # Konversi kembali ke uint8
    return hasil.astype(np.uint8)


def adjust_contrast_manual(gambar, alpha):
    """
    Implementasi manual contrast adjustment untuk pemahaman
    """
    # Konversi ke float
    gambar_float = gambar.astype(np.float32)
    
    # Kalikan dengan alpha
    hasil = gambar_float * alpha
    
    # Clip ke range valid
    hasil = np.clip(hasil, 0, 255)
    
    return hasil.astype(np.uint8)


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_brightness():
    """
    Demonstrasi efek berbagai nilai brightness
    """
    print("\n" + "=" * 60)
    print("DEMONSTRASI BRIGHTNESS")
    print("=" * 60)
    
    print("""
BRIGHTNESS (Beta):
├── Beta > 0  : Gambar lebih terang
├── Beta = 0  : Tidak ada perubahan
└── Beta < 0  : Gambar lebih gelap

Formula: g(x,y) = f(x,y) + beta
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Menggunakan gambar sample...")
        gambar = buat_gambar_sample()
    
    # Berbagai nilai brightness
    brightness_values = [-100, -50, 0, 50, 100]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, beta in enumerate(brightness_values):
        hasil = adjust_brightness(gambar, beta)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"Brightness = {beta}")
        axes[i].axis('off')
        
        # Info mean brightness
        mean_val = np.mean(hasil)
        axes[i].text(0.5, -0.1, f"Mean: {mean_val:.1f}", 
                     transform=axes[i].transAxes, ha='center')
    
    # Histogram pada subplot terakhir
    axes[5].hist(gambar.ravel(), 256, [0, 256], alpha=0.5, label='Original')
    axes[5].hist(adjust_brightness(gambar, 50).ravel(), 256, [0, 256], 
                 alpha=0.5, label='Bright (+50)')
    axes[5].hist(adjust_brightness(gambar, -50).ravel(), 256, [0, 256], 
                 alpha=0.5, label='Dark (-50)')
    axes[5].legend()
    axes[5].set_title("Histogram Comparison")
    
    plt.suptitle("Efek Brightness pada Gambar", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_contrast():
    """
    Demonstrasi efek berbagai nilai contrast
    """
    print("\n" + "=" * 60)
    print("DEMONSTRASI CONTRAST")
    print("=" * 60)
    
    print("""
CONTRAST (Alpha):
├── Alpha > 1  : Kontras meningkat (perbedaan lebih jelas)
├── Alpha = 1  : Tidak ada perubahan
└── Alpha < 1  : Kontras menurun (gambar "washed out")

Formula: g(x,y) = alpha * f(x,y)
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Berbagai nilai contrast
    contrast_values = [0.3, 0.5, 1.0, 1.5, 2.0, 2.5]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, alpha in enumerate(contrast_values):
        hasil = adjust_contrast(gambar, alpha)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"Contrast = {alpha}")
        axes[i].axis('off')
        
        # Info standard deviation (ukuran kontras)
        std_val = np.std(hasil)
        axes[i].text(0.5, -0.1, f"Std: {std_val:.1f}", 
                     transform=axes[i].transAxes, ha='center')
    
    plt.suptitle("Efek Contrast pada Gambar", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_combined():
    """
    Demonstrasi kombinasi brightness dan contrast
    """
    print("\n" + "=" * 60)
    print("DEMONSTRASI KOMBINASI BRIGHTNESS & CONTRAST")
    print("=" * 60)
    
    print("""
KOMBINASI:
Formula: g(x,y) = alpha * f(x,y) + beta

Urutan operasi:
1. Contrast diterapkan dulu (perkalian)
2. Brightness diterapkan kemudian (penambahan)
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Kombinasi parameter
    kombinasi = [
        (1.0, 0, "Original"),
        (1.2, 20, "Slight Enhance"),
        (1.5, 30, "Medium Enhance"),
        (2.0, 50, "High Enhance"),
        (0.5, -30, "Dimmed"),
        (1.5, -30, "High Contrast, Lower Bright"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (alpha, beta, label) in enumerate(kombinasi):
        hasil = adjust_brightness_contrast(gambar, alpha, beta)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{label}\nα={alpha}, β={beta}")
        axes[i].axis('off')
    
    plt.suptitle("Kombinasi Brightness & Contrast", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_clipping():
    """
    Demonstrasi efek clipping (nilai melebihi 0-255)
    """
    print("\n" + "=" * 60)
    print("DEMONSTRASI CLIPPING")
    print("=" * 60)
    
    print("""
CLIPPING:
Ketika nilai piksel melebihi range [0, 255]:
├── Nilai > 255 → di-clip ke 255 (highlight clipping)
└── Nilai < 0   → di-clip ke 0 (shadow clipping)

Efek: Kehilangan detail pada area yang ter-clip
    """)
    
    # Buat gambar gradient untuk demonstrasi clipping
    gambar = np.zeros((200, 400, 3), dtype=np.uint8)
    
    # Horizontal gradient dari 0 ke 255
    for j in range(400):
        gambar[:, j] = [int(j * 255 / 400)] * 3
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Baris 1: Gambar
    brightness_values = [0, 100, -100]
    
    for i, beta in enumerate(brightness_values):
        hasil = adjust_brightness(gambar, beta)
        axes[0, i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[0, i].set_title(f"Brightness = {beta}")
        axes[0, i].axis('off')
    
    # Baris 2: Histogram
    for i, beta in enumerate(brightness_values):
        hasil = adjust_brightness(gambar, beta)
        gray = cv2.cvtColor(hasil, cv2.COLOR_BGR2GRAY)
        
        axes[1, i].hist(gray.ravel(), 256, [0, 256])
        axes[1, i].set_title(f"Histogram (β={beta})")
        axes[1, i].set_xlim([0, 256])
        
        # Highlight clipping
        count_0 = np.sum(gray == 0)
        count_255 = np.sum(gray == 255)
        axes[1, i].text(0.5, 0.95, f"Clip 0: {count_0}, Clip 255: {count_255}",
                       transform=axes[1, i].transAxes, ha='center', va='top')
    
    plt.suptitle("Efek Clipping pada Brightness Adjustment", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: BRIGHTNESS & CONTRAST ADJUSTMENT")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
POINT OPERATIONS:
Operasi yang dilakukan pada setiap piksel secara independen,
tanpa mempertimbangkan piksel tetangga.

Brightness & Contrast adalah point operations paling dasar
untuk image enhancement.
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
    print(f"[INFO] Brightness (beta): {BRIGHTNESS}")
    print(f"[INFO] Contrast (alpha): {CONTRAST}")
    
    # Terapkan adjustment
    hasil = adjust_brightness_contrast(gambar, CONTRAST, BRIGHTNESS)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"Original\nMean: {np.mean(gambar):.1f}, Std: {np.std(gambar):.1f}")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Adjusted (α={CONTRAST}, β={BRIGHTNESS})\nMean: {np.mean(hasil):.1f}, Std: {np.std(hasil):.1f}")
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_brightness()
    demo_contrast()
    demo_combined()
    demo_clipping()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN BRIGHTNESS & CONTRAST")
    print("=" * 60)
    print("""
FUNGSI OPENCV:
    cv2.convertScaleAbs(src, alpha=1.0, beta=0)
    
    - alpha: contrast factor (default 1.0)
    - beta: brightness offset (default 0)
    
TIPS:
├── Untuk gambar gelap: tingkatkan beta (brightness)
├── Untuk gambar "flat": tingkatkan alpha (contrast)
├── Hindari clipping dengan tidak menggunakan nilai ekstrem
└── Gunakan histogram sebagai panduan

BEST PRACTICES:
1. Analisis histogram terlebih dahulu
2. Adjust contrast sebelum brightness
3. Gunakan nilai moderat (alpha: 0.5-2.0, beta: -100 to 100)
4. Perhatikan highlight dan shadow clipping
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
