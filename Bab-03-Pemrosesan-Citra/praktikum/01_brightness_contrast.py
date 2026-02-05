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
# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor modul os.
import os
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
# Keterangan: Inisialisasi atau perbarui variabel NAMA_FILE_GAMBAR.
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Nilai brightness (kecerahan)
# Range: -255 sampai 255
# Positif = lebih terang, Negatif = lebih gelap
# Keterangan: Inisialisasi atau perbarui variabel BRIGHTNESS.
BRIGHTNESS = 50

# 3. Nilai contrast (kontras)
# Range: 0.1 sampai 3.0
# > 1.0 = kontras meningkat, < 1.0 = kontras menurun
# Keterangan: Inisialisasi atau perbarui variabel CONTRAST.
CONTRAST = 1.5

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
    """Membuat gambar sample jika file tidak ditemukan"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Gradient background
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Mulai loop dengan for j in range(600).
        for j in range(600):
            # Keterangan: Inisialisasi beberapa variabel (gambar[i, j]).
            gambar[i, j] = [
                # Keterangan: Jalankan perintah berikut.
                int(50 + i/4),      # B
                # Keterangan: Jalankan perintah berikut.
                int(100 + j/6),     # G
                # Keterangan: Jalankan perintah berikut.
                int(150 + i/4)      # R
            # Keterangan: Jalankan perintah berikut.
            ]
    
    # Tambahkan beberapa objek
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), (0, 0, 200), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 200), 80, (200, 200, 0), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "SAMPLE", (200, 350), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# ============================================================
# FUNGSI BRIGHTNESS DAN CONTRAST
# ============================================================

# Keterangan: Definisikan fungsi adjust_brightness.
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
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.convertScaleAbs(gambar, alpha=1.0, beta=beta)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi adjust_contrast.
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
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.convertScaleAbs(gambar, alpha=alpha, beta=0)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi adjust_brightness_contrast.
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
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.convertScaleAbs(gambar, alpha=alpha, beta=beta)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi adjust_brightness_manual.
def adjust_brightness_manual(gambar, beta):
    """
    Implementasi manual brightness adjustment untuk pemahaman
    """
    # Konversi ke float untuk mencegah overflow
    # Keterangan: Inisialisasi atau perbarui variabel gambar_float.
    gambar_float = gambar.astype(np.float32)
    
    # Tambahkan beta
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = gambar_float + beta
    
    # Clip ke range valid [0, 255]
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = np.clip(hasil, 0, 255)
    
    # Konversi kembali ke uint8
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil.astype(np.uint8)


# Keterangan: Definisikan fungsi adjust_contrast_manual.
def adjust_contrast_manual(gambar, alpha):
    """
    Implementasi manual contrast adjustment untuk pemahaman
    """
    # Konversi ke float
    # Keterangan: Inisialisasi atau perbarui variabel gambar_float.
    gambar_float = gambar.astype(np.float32)
    
    # Kalikan dengan alpha
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = gambar_float * alpha
    
    # Clip ke range valid
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = np.clip(hasil, 0, 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil.astype(np.uint8)


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_brightness.
def demo_brightness():
    """
    Demonstrasi efek berbagai nilai brightness
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMONSTRASI BRIGHTNESS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
BRIGHTNESS (Beta):
├── Beta > 0  : Gambar lebih terang
├── Beta = 0  : Tidak ada perubahan
└── Beta < 0  : Gambar lebih gelap

Formula: g(x,y) = f(x,y) + beta
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
        # Keterangan: Jalankan perintah berikut.
        print("[INFO] Menggunakan gambar sample...")
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Berbagai nilai brightness
    # Keterangan: Inisialisasi atau perbarui variabel brightness_values.
    brightness_values = [-100, -50, 0, 50, 100]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # Keterangan: Inisialisasi atau perbarui variabel axes.
    axes = axes.flatten()
    
    # Keterangan: Mulai loop dengan for i, beta in enumerate(brightness_values).
    for i, beta in enumerate(brightness_values):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adjust_brightness(gambar, beta)
        
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"Brightness.
        axes[i].set_title(f"Brightness = {beta}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
        
        # Info mean brightness
        # Keterangan: Inisialisasi atau perbarui variabel mean_val.
        mean_val = np.mean(hasil)
        # Keterangan: Jalankan perintah berikut.
        axes[i].text(0.5, -0.1, f"Mean: {mean_val:.1f}", 
                     # Keterangan: Inisialisasi atau perbarui variabel transform.
                     transform=axes[i].transAxes, ha='center')
    
    # Histogram pada subplot terakhir
    # Keterangan: Inisialisasi beberapa variabel (axes[5].hist(gambar.ravel(), 256, [0, 256], alpha).
    axes[5].hist(gambar.ravel(), 256, [0, 256], alpha=0.5, label='Original')
    # Keterangan: Jalankan perintah berikut.
    axes[5].hist(adjust_brightness(gambar, 50).ravel(), 256, [0, 256], 
                 # Keterangan: Inisialisasi atau perbarui variabel alpha.
                 alpha=0.5, label='Bright (+50)')
    # Keterangan: Jalankan perintah berikut.
    axes[5].hist(adjust_brightness(gambar, -50).ravel(), 256, [0, 256], 
                 # Keterangan: Inisialisasi atau perbarui variabel alpha.
                 alpha=0.5, label='Dark (-50)')
    # Keterangan: Jalankan perintah berikut.
    axes[5].legend()
    # Keterangan: Jalankan perintah berikut.
    axes[5].set_title("Histogram Comparison")
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Efek Brightness pada Gambar", fontsize).
    plt.suptitle("Efek Brightness pada Gambar", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_contrast.
def demo_contrast():
    """
    Demonstrasi efek berbagai nilai contrast
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMONSTRASI CONTRAST")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
CONTRAST (Alpha):
├── Alpha > 1  : Kontras meningkat (perbedaan lebih jelas)
├── Alpha = 1  : Tidak ada perubahan
└── Alpha < 1  : Kontras menurun (gambar "washed out")

Formula: g(x,y) = alpha * f(x,y)
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
    
    # Berbagai nilai contrast
    # Keterangan: Inisialisasi atau perbarui variabel contrast_values.
    contrast_values = [0.3, 0.5, 1.0, 1.5, 2.0, 2.5]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # Keterangan: Inisialisasi atau perbarui variabel axes.
    axes = axes.flatten()
    
    # Keterangan: Mulai loop dengan for i, alpha in enumerate(contrast_values).
    for i, alpha in enumerate(contrast_values):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adjust_contrast(gambar, alpha)
        
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"Contrast.
        axes[i].set_title(f"Contrast = {alpha}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
        
        # Info standard deviation (ukuran kontras)
        # Keterangan: Inisialisasi atau perbarui variabel std_val.
        std_val = np.std(hasil)
        # Keterangan: Jalankan perintah berikut.
        axes[i].text(0.5, -0.1, f"Std: {std_val:.1f}", 
                     # Keterangan: Inisialisasi atau perbarui variabel transform.
                     transform=axes[i].transAxes, ha='center')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Efek Contrast pada Gambar", fontsize).
    plt.suptitle("Efek Contrast pada Gambar", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_combined.
def demo_combined():
    """
    Demonstrasi kombinasi brightness dan contrast
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMONSTRASI KOMBINASI BRIGHTNESS & CONTRAST")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
KOMBINASI:
Formula: g(x,y) = alpha * f(x,y) + beta

Urutan operasi:
1. Contrast diterapkan dulu (perkalian)
2. Brightness diterapkan kemudian (penambahan)
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
    
    # Kombinasi parameter
    # Keterangan: Inisialisasi atau perbarui variabel kombinasi.
    kombinasi = [
        # Keterangan: Jalankan perintah berikut.
        (1.0, 0, "Original"),
        # Keterangan: Jalankan perintah berikut.
        (1.2, 20, "Slight Enhance"),
        # Keterangan: Jalankan perintah berikut.
        (1.5, 30, "Medium Enhance"),
        # Keterangan: Jalankan perintah berikut.
        (2.0, 50, "High Enhance"),
        # Keterangan: Jalankan perintah berikut.
        (0.5, -30, "Dimmed"),
        # Keterangan: Jalankan perintah berikut.
        (1.5, -30, "High Contrast, Lower Bright"),
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # Keterangan: Inisialisasi atau perbarui variabel axes.
    axes = axes.flatten()
    
    # Keterangan: Mulai loop dengan for i, (alpha, beta, label) in enumerate(kombinasi).
    for i, (alpha, beta, label) in enumerate(kombinasi):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adjust_brightness_contrast(gambar, alpha, beta)
        
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"{label}\nα.
        axes[i].set_title(f"{label}\nα={alpha}, β={beta}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Kombinasi Brightness & Contrast", fontsize).
    plt.suptitle("Kombinasi Brightness & Contrast", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_clipping.
def demo_clipping():
    """
    Demonstrasi efek clipping (nilai melebihi 0-255)
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMONSTRASI CLIPPING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
CLIPPING:
Ketika nilai piksel melebihi range [0, 255]:
├── Nilai > 255 → di-clip ke 255 (highlight clipping)
└── Nilai < 0   → di-clip ke 0 (shadow clipping)

Efek: Kehilangan detail pada area yang ter-clip
    """)
    
    # Buat gambar gradient untuk demonstrasi clipping
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((200, 400, 3), dtype=np.uint8)
    
    # Horizontal gradient dari 0 ke 255
    # Keterangan: Mulai loop dengan for j in range(400).
    for j in range(400):
        # Keterangan: Inisialisasi beberapa variabel (gambar[:, j]).
        gambar[:, j] = [int(j * 255 / 400)] * 3
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Baris 1: Gambar
    # Keterangan: Inisialisasi atau perbarui variabel brightness_values.
    brightness_values = [0, 100, -100]
    
    # Keterangan: Mulai loop dengan for i, beta in enumerate(brightness_values).
    for i, beta in enumerate(brightness_values):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adjust_brightness(gambar, beta)
        # Keterangan: Konversi ruang warna gambar.
        axes[0, i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi beberapa variabel (axes[0, i].set_title(f"Brightness).
        axes[0, i].set_title(f"Brightness = {beta}")
        # Keterangan: Jalankan perintah berikut.
        axes[0, i].axis('off')
    
    # Baris 2: Histogram
    # Keterangan: Mulai loop dengan for i, beta in enumerate(brightness_values).
    for i, beta in enumerate(brightness_values):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = adjust_brightness(gambar, beta)
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(hasil, cv2.COLOR_BGR2GRAY)
        
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].hist(gray.ravel(), 256, [0, 256])
        # Keterangan: Inisialisasi beberapa variabel (axes[1, i].set_title(f"Histogram (β).
        axes[1, i].set_title(f"Histogram (β={beta})")
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].set_xlim([0, 256])
        
        # Highlight clipping
        # Keterangan: Jalankan perintah berikut.
        count_0 = np.sum(gray == 0)
        # Keterangan: Jalankan perintah berikut.
        count_255 = np.sum(gray == 255)
        # Keterangan: Jalankan perintah berikut.
        axes[1, i].text(0.5, 0.95, f"Clip 0: {count_0}, Clip 255: {count_255}",
                       # Keterangan: Inisialisasi atau perbarui variabel transform.
                       transform=axes[1, i].transAxes, ha='center', va='top')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Efek Clipping pada Brightness Adjustment", fontsize).
    plt.suptitle("Efek Clipping pada Brightness Adjustment", fontsize=14)
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
    print("PRAKTIKUM: BRIGHTNESS & CONTRAST ADJUSTMENT")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Mulai blok kode baru.
POINT OPERATIONS:
# Keterangan: Jalankan perintah berikut.
Operasi yang dilakukan pada setiap piksel secara independen,
# Keterangan: Jalankan perintah berikut.
tanpa mempertimbangkan piksel tetangga.

# Keterangan: Jalankan perintah berikut.
Brightness & Contrast adalah point operations paling dasar
# Keterangan: Jalankan perintah berikut.
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
# Keterangan: Mulai blok kode baru.
FUNGSI OPENCV:
    # Keterangan: Inisialisasi beberapa variabel (cv2.convertScaleAbs(src, alpha).
    cv2.convertScaleAbs(src, alpha=1.0, beta=0)
    
    # Keterangan: Jalankan perintah berikut.
    - alpha: contrast factor (default 1.0)
    # Keterangan: Jalankan perintah berikut.
    - beta: brightness offset (default 0)
    
# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
├── Untuk gambar gelap: tingkatkan beta (brightness)
# Keterangan: Jalankan perintah berikut.
├── Untuk gambar "flat": tingkatkan alpha (contrast)
# Keterangan: Jalankan perintah berikut.
├── Hindari clipping dengan tidak menggunakan nilai ekstrem
# Keterangan: Jalankan perintah berikut.
└── Gunakan histogram sebagai panduan

# Keterangan: Mulai blok kode baru.
BEST PRACTICES:
# Keterangan: Jalankan perintah berikut.
1. Analisis histogram terlebih dahulu
# Keterangan: Jalankan perintah berikut.
2. Adjust contrast sebelum brightness
# Keterangan: Jalankan perintah berikut.
3. Gunakan nilai moderat (alpha: 0.5-2.0, beta: -100 to 100)
# Keterangan: Jalankan perintah berikut.
4. Perhatikan highlight dan shadow clipping
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
