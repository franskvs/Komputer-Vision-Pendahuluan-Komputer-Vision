# ============================================================
# PROGRAM: 07_morphological_operations.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk operasi morfologi (erosion, dilation, dll)
# 
# Tujuan Pembelajaran:
#   1. Memahami operasi morfologi dasar
#   2. Erosion, dilation, opening, closing
#   3. Gradient morfologi dan top-hat transform
#   4. Aplikasi untuk noise removal dan segmentation
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

# 2. Kernel size untuk operasi morfologi
# Keterangan: Inisialisasi atau perbarui variabel KERNEL_SIZE.
KERNEL_SIZE = 5

# 3. Kernel shape
# Opsi: 'rect', 'ellipse', 'cross'
# Keterangan: Inisialisasi atau perbarui variabel KERNEL_SHAPE.
KERNEL_SHAPE = 'rect'

# 4. Jumlah iterasi untuk erosion/dilation
# Keterangan: Inisialisasi atau perbarui variabel ITERATIONS.
ITERATIONS = 1

# 5. Threshold untuk binary image
# Keterangan: Inisialisasi atau perbarui variabel BINARY_THRESHOLD.
BINARY_THRESHOLD = 127

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
    """Membuat gambar biner sample untuk demonstrasi morfologi"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((300, 400), dtype=np.uint8)
    
    # Objek utama
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (150, 150), 255, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (280, 100), 50, 255, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillPoly(gambar, [np.array([[200, 250], [250, 180], [300, 250]])], 255)
    
    # Tambah text
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "MORPH", (100, 280), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# Keterangan: Definisikan fungsi buat_gambar_noisy.
def buat_gambar_noisy():
    """Membuat gambar dengan noise untuk demonstrasi"""
    gambar = buat_gambar_sample()
    
    # Tambah salt noise (white specks)
    salt = np.random.random(gambar.shape) < 0.02
    gambar[salt] = 255
    
    # Tambah pepper noise (black specks)  
    pepper = np.random.random(gambar.shape) < 0.02
    gambar[pepper] = 0
    
    return gambar


def dapatkan_kernel(shape='rect', size=5):
    """
    # Keterangan: Jalankan perintah berikut.
    Membuat structuring element (kernel) untuk operasi morfologi
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - shape: 'rect', 'ellipse', atau 'cross'
    # Keterangan: Jalankan perintah berikut.
    - size: ukuran kernel
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - structuring element
    """
    if shape == 'rect':
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    elif shape == 'ellipse':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    elif shape == 'cross':
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
    else:
        kernel = np.ones((size, size), np.uint8)
    
    return kernel


# ============================================================
# FUNGSI OPERASI MORFOLOGI DASAR
# ============================================================

def erosion(gambar, kernel, iterations=1):
    """
    # Keterangan: Jalankan perintah berikut.
    Erosi morfologi
    
    # Keterangan: Jalankan perintah berikut.
    Mengecilkan objek putih (foreground)
    # Keterangan: Jalankan perintah berikut.
    Menghilangkan noise kecil
    # Keterangan: Jalankan perintah berikut.
    Memisahkan objek yang terhubung
    
    # Keterangan: Mulai blok kode baru.
    Prinsip:
    # Keterangan: Jalankan perintah berikut.
    - Kernel slide di atas gambar
    # Keterangan: Inisialisasi atau perbarui variabel - Piksel output.
    - Piksel output = minimum dari piksel dalam kernel
    # Keterangan: Inisialisasi atau perbarui variabel - Untuk binary: output 1 hanya jika SEMUA piksel dalam kernel.
    - Untuk binary: output 1 hanya jika SEMUA piksel dalam kernel = 1
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    # Keterangan: Jalankan perintah berikut.
    - iterations: jumlah pengulangan
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar hasil erosi
    """
    hasil = cv2.erode(gambar, kernel, iterations=iterations)
    return hasil


def dilation(gambar, kernel, iterations=1):
    """
    # Keterangan: Jalankan perintah berikut.
    Dilasi morfologi
    
    # Keterangan: Jalankan perintah berikut.
    Memperbesar objek putih (foreground)
    # Keterangan: Jalankan perintah berikut.
    Mengisi lubang kecil
    # Keterangan: Jalankan perintah berikut.
    Menghubungkan objek yang terpisah
    
    # Keterangan: Mulai blok kode baru.
    Prinsip:
    # Keterangan: Jalankan perintah berikut.
    - Kernel slide di atas gambar
    # Keterangan: Inisialisasi atau perbarui variabel - Piksel output.
    - Piksel output = maximum dari piksel dalam kernel
    # Keterangan: Inisialisasi atau perbarui variabel - Untuk binary: output 1 jika SETIDAKNYA SATU piksel dalam kernel.
    - Untuk binary: output 1 jika SETIDAKNYA SATU piksel dalam kernel = 1
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    # Keterangan: Jalankan perintah berikut.
    - iterations: jumlah pengulangan
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar hasil dilasi
    """
    hasil = cv2.dilate(gambar, kernel, iterations=iterations)
    return hasil


def opening(gambar, kernel):
    """
    # Keterangan: Inisialisasi atau perbarui variabel Opening.
    Opening = Erosi + Dilasi
    
    # Keterangan: Jalankan perintah berikut.
    Menghilangkan noise kecil di foreground
    # Keterangan: Jalankan perintah berikut.
    Menjaga ukuran objek relatif sama
    
    # Keterangan: Jalankan perintah berikut.
    Urutan: Erosi dulu → baru Dilasi
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar hasil opening
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_OPEN, kernel)
    return hasil


def closing(gambar, kernel):
    """
    # Keterangan: Inisialisasi atau perbarui variabel Closing.
    Closing = Dilasi + Erosi
    
    # Keterangan: Jalankan perintah berikut.
    Mengisi lubang kecil di foreground
    # Keterangan: Jalankan perintah berikut.
    Menghubungkan komponen yang hampir tersambung
    
    # Keterangan: Jalankan perintah berikut.
    Urutan: Dilasi dulu → baru Erosi
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar hasil closing
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_CLOSE, kernel)
    return hasil


# ============================================================
# FUNGSI OPERASI MORFOLOGI LANJUTAN
# ============================================================

def morphological_gradient(gambar, kernel):
    """
    # Keterangan: Inisialisasi atau perbarui variabel Gradient Morfologi.
    Gradient Morfologi = Dilasi - Erosi
    
    # Keterangan: Jalankan perintah berikut.
    Menghasilkan outline/edge dari objek
    # Keterangan: Jalankan perintah berikut.
    Berguna untuk edge detection pada binary images
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar gradient
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_GRADIENT, kernel)
    return hasil


def top_hat(gambar, kernel):
    """
    # Keterangan: Inisialisasi atau perbarui variabel Top-Hat Transform.
    Top-Hat Transform = Original - Opening
    
    # Keterangan: Jalankan perintah berikut.
    Mengisolasi bright spots (peaks) yang lebih kecil dari kernel
    # Keterangan: Jalankan perintah berikut.
    Berguna untuk menemukan bright regions pada background gelap
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar top-hat
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_TOPHAT, kernel)
    return hasil


def black_hat(gambar, kernel):
    """
    # Keterangan: Inisialisasi atau perbarui variabel Black-Hat Transform.
    Black-Hat Transform = Closing - Original
    
    # Keterangan: Jalankan perintah berikut.
    Mengisolasi dark spots (valleys) yang lebih kecil dari kernel
    # Keterangan: Jalankan perintah berikut.
    Berguna untuk menemukan dark regions pada background terang
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary/grayscale image
    # Keterangan: Jalankan perintah berikut.
    - kernel: structuring element
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar black-hat
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_BLACKHAT, kernel)
    return hasil


def hit_or_miss(gambar, kernel1, kernel2=None):
    """
    # Keterangan: Jalankan perintah berikut.
    Hit-or-Miss Transform
    
    # Keterangan: Jalankan perintah berikut.
    Mendeteksi pattern spesifik dalam binary image
    # Keterangan: Jalankan perintah berikut.
    Berguna untuk shape detection, thinning, pruning
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - gambar: input binary image
    # Keterangan: Jalankan perintah berikut.
    - kernel1: structuring element untuk foreground match
    # Keterangan: Jalankan perintah berikut.
    - kernel2: structuring element untuk background match (optional)
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - gambar hasil hit-or-miss
    """
    if kernel2 is None:
        # Buat kernel komplementer
        hasil = cv2.morphologyEx(gambar, cv2.MORPH_HITMISS, kernel1)
    else:
        eroded1 = cv2.erode(gambar, kernel1)
        eroded2 = cv2.erode(255 - gambar, kernel2)
        hasil = cv2.bitwise_and(eroded1, eroded2)
    
    return hasil


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_konsep_morfologi():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi konsep dasar operasi morfologi
    """
    print("\n" + "=" * 60)
    print("KONSEP OPERASI MORFOLOGI")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
OPERASI MORFOLOGI adalah teknik pemrosesan citra berbasis
# Keterangan: Jalankan perintah berikut.
bentuk (shape) menggunakan structuring element (kernel).

# Keterangan: Mulai blok kode baru.
STRUCTURING ELEMENT (KERNEL):
# Keterangan: Jalankan perintah berikut.
┌───────────────────────────────────────────────────┐
# Keterangan: Jalankan perintah berikut.
│  RECT (Rectangle)  │  ELLIPSE  │  CROSS          │
# Keterangan: Jalankan perintah berikut.
│  ■ ■ ■             │  · ■ ■ ■ ·│    ■            │
# Keterangan: Jalankan perintah berikut.
│  ■ ■ ■             │  ■ ■ ■ ■ ■│  ■ ■ ■          │
# Keterangan: Jalankan perintah berikut.
│  ■ ■ ■             │  ■ ■ ■ ■ ■│    ■            │
# Keterangan: Jalankan perintah berikut.
│                    │  · ■ ■ ■ ·│                 │
# Keterangan: Jalankan perintah berikut.
└───────────────────────────────────────────────────┘

# Keterangan: Mulai blok kode baru.
OPERASI DASAR:
# Keterangan: Jalankan perintah berikut.
├── Erosion:  Mengecilkan objek (MIN operation)
# Keterangan: Jalankan perintah berikut.
├── Dilation: Memperbesar objek (MAX operation)
# Keterangan: Jalankan perintah berikut.
├── Opening:  Erosi + Dilasi (hapus noise kecil)
# Keterangan: Jalankan perintah berikut.
└── Closing:  Dilasi + Erosi (isi lubang kecil)
    """)
    
    # Visualisasi kernel shapes
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    shapes = ['rect', 'ellipse', 'cross']
    for i, shape in enumerate(shapes):
        kernel = dapatkan_kernel(shape, 5)
        axes[i].imshow(kernel, cmap='gray', vmin=0, vmax=1)
        axes[i].set_title(f"Kernel: {shape.upper()}")
        for y in range(5):
            for x in range(5):
                axes[i].text(x, y, str(kernel[y, x]), 
                           ha='center', va='center',
                           color='white' if kernel[y, x] == 0 else 'black')
        axes[i].axis('off')
    
    plt.suptitle("Structuring Elements (Kernels)", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_erosion_dilation():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi erosi dan dilasi
    """
    print("\n" + "=" * 60)
    print("EROSI DAN DILASI")
    print("=" * 60)
    
    print("""
# Keterangan: Mulai blok kode baru.
EROSION (Erosi):
# Keterangan: Inisialisasi atau perbarui variabel ├── Piksel output.
├── Piksel output = 1 hanya jika SEMUA piksel dalam kernel = 1
# Keterangan: Jalankan perintah berikut.
├── Efek: mengecilkan objek, memisahkan objek yang terhubung
# Keterangan: Jalankan perintah berikut.
├── Menghilangkan protrusions (tonjolan kecil)
# Keterangan: Jalankan perintah berikut.
└── Menghapus noise putih (salt noise)

# Keterangan: Mulai blok kode baru.
DILATION (Dilasi):
# Keterangan: Inisialisasi atau perbarui variabel ├── Piksel output.
├── Piksel output = 1 jika SETIDAKNYA SATU piksel dalam kernel = 1
# Keterangan: Jalankan perintah berikut.
├── Efek: memperbesar objek, menghubungkan objek yang terpisah
# Keterangan: Jalankan perintah berikut.
├── Mengisi lubang kecil
# Keterangan: Jalankan perintah berikut.
└── Menghapus noise hitam (pepper noise)

# Keterangan: Mulai blok kode baru.
ITERATIONS:
# Keterangan: Jalankan perintah berikut.
└── Semakin banyak iterasi, semakin kuat efeknya
    """)
    
    gambar = buat_gambar_sample()
    kernel = dapatkan_kernel(KERNEL_SHAPE, KERNEL_SIZE)
    
    # Variasi iterasi
    iterations = [1, 2, 3, 5]
    
    fig, axes = plt.subplots(3, len(iterations) + 1, figsize=(16, 10))
    
    # Baris 1: Original dan erosi
    axes[0, 0].imshow(gambar, cmap='gray')
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    for i, itr in enumerate(iterations):
        eroded = erosion(gambar, kernel, itr)
        axes[0, i + 1].imshow(eroded, cmap='gray')
        axes[0, i + 1].set_title(f"Erosion (iter={itr})")
        axes[0, i + 1].axis('off')
    
    # Baris 2: Dilasi
    axes[1, 0].imshow(gambar, cmap='gray')
    axes[1, 0].set_title("Original")
    axes[1, 0].axis('off')
    
    for i, itr in enumerate(iterations):
        dilated = dilation(gambar, kernel, itr)
        axes[1, i + 1].imshow(dilated, cmap='gray')
        axes[1, i + 1].set_title(f"Dilation (iter={itr})")
        axes[1, i + 1].axis('off')
    
    # Baris 3: Perbandingan
    axes[2, 0].imshow(gambar, cmap='gray')
    axes[2, 0].set_title("Original")
    axes[2, 0].axis('off')
    
    axes[2, 1].imshow(erosion(gambar, kernel, 2), cmap='gray')
    axes[2, 1].set_title("Eroded (smaller)")
    axes[2, 1].axis('off')
    
    axes[2, 2].imshow(dilation(gambar, kernel, 2), cmap='gray')
    axes[2, 2].set_title("Dilated (larger)")
    axes[2, 2].axis('off')
    
    # Difference visualization
    diff = cv2.absdiff(dilation(gambar, kernel, 2), 
                       erosion(gambar, kernel, 2))
    axes[2, 3].imshow(diff, cmap='gray')
    axes[2, 3].set_title("Difference\n(Dilated - Eroded)")
    axes[2, 3].axis('off')
    
    # Hide remaining axes
    for i in range(4, len(iterations) + 1):
        axes[2, i].axis('off')
    
    plt.suptitle(f"Erosion vs Dilation (Kernel: {KERNEL_SHAPE} {KERNEL_SIZE}×{KERNEL_SIZE})", 
                 fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_opening_closing():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi opening dan closing untuk noise removal
    """
    print("\n" + "=" * 60)
    print("OPENING DAN CLOSING")
    print("=" * 60)
    
    print("""
# Keterangan: Inisialisasi atau perbarui variabel OPENING.
OPENING = Erosi → Dilasi:
# Keterangan: Jalankan perintah berikut.
├── Menghilangkan small bright spots (salt noise)
# Keterangan: Jalankan perintah berikut.
├── Menghilangkan protrusions
# Keterangan: Jalankan perintah berikut.
├── Smoothing boundary dari luar
# Keterangan: Jalankan perintah berikut.
└── Tidak mengubah ukuran objek secara signifikan

# Keterangan: Inisialisasi atau perbarui variabel CLOSING.
CLOSING = Dilasi → Erosi:
# Keterangan: Jalankan perintah berikut.
├── Mengisi small dark spots (pepper noise, lubang)
# Keterangan: Jalankan perintah berikut.
├── Menyambung objek yang hampir terhubung
# Keterangan: Jalankan perintah berikut.
├── Smoothing boundary dari dalam
# Keterangan: Jalankan perintah berikut.
└── Tidak mengubah ukuran objek secara signifikan

# Keterangan: Mulai blok kode baru.
KOMBINASI Opening + Closing:
# Keterangan: Jalankan perintah berikut.
└── Efektif untuk menghilangkan noise di foreground DAN background
    """)
    
    gambar_noisy = buat_gambar_noisy()
    kernel = dapatkan_kernel(KERNEL_SHAPE, KERNEL_SIZE)
    
    # Apply operations
    opened = opening(gambar_noisy, kernel)
    closed = closing(gambar_noisy, kernel)
    
    # Combined: Opening then Closing
    combined = closing(opened, kernel)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(gambar_noisy, cmap='gray')
    axes[0, 0].set_title("Noisy Image\n(Salt & Pepper noise)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(opened, cmap='gray')
    axes[0, 1].set_title("After Opening\n(Erosi → Dilasi)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(closed, cmap='gray')
    axes[0, 2].set_title("After Closing\n(Dilasi → Erosi)")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(buat_gambar_sample(), cmap='gray')
    axes[1, 0].set_title("Original (Clean)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(combined, cmap='gray')
    axes[1, 1].set_title("Opening + Closing\n(Best result)")
    axes[1, 1].axis('off')
    
    # Difference
    diff = cv2.absdiff(buat_gambar_sample(), combined)
    axes[1, 2].imshow(diff, cmap='gray')
    axes[1, 2].set_title("Difference\n(Original - Processed)")
    axes[1, 2].axis('off')
    
    plt.suptitle("Opening & Closing untuk Noise Removal", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_advanced_operations():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi operasi morfologi lanjutan
    """
    print("\n" + "=" * 60)
    print("OPERASI MORFOLOGI LANJUTAN")
    print("=" * 60)
    
    print("""
# Keterangan: Inisialisasi atau perbarui variabel MORPHOLOGICAL GRADIENT.
MORPHOLOGICAL GRADIENT = Dilasi - Erosi:
# Keterangan: Jalankan perintah berikut.
└── Menghasilkan outline/kontur dari objek

# Keterangan: Inisialisasi atau perbarui variabel TOP-HAT.
TOP-HAT = Original - Opening:
# Keterangan: Jalankan perintah berikut.
├── Mengisolasi bright spots (lebih kecil dari kernel)
# Keterangan: Jalankan perintah berikut.
└── Berguna untuk uneven illumination correction

# Keterangan: Inisialisasi atau perbarui variabel BLACK-HAT.
BLACK-HAT = Closing - Original:
# Keterangan: Jalankan perintah berikut.
├── Mengisolasi dark spots (lebih kecil dari kernel)
# Keterangan: Jalankan perintah berikut.
└── Berguna untuk menemukan dark regions
    """)
    
    # Load gambar grayscale (untuk top-hat/black-hat)
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    else:
        # Buat gambar dengan variasi intensitas
        gambar = np.zeros((300, 400), dtype=np.uint8)
        # Gradient background
        for i in range(300):
            gambar[i, :] = 50 + i // 3
        # Add bright and dark spots
        cv2.circle(gambar, (100, 100), 30, 255, -1)
        cv2.circle(gambar, (300, 200), 30, 0, -1)
    
    kernel = dapatkan_kernel(KERNEL_SHAPE, KERNEL_SIZE)
    
    # Binary version
    _, binary = cv2.threshold(gambar, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    
    # Apply operations
    gradient_binary = morphological_gradient(binary, kernel)
    gradient_gray = morphological_gradient(gambar, kernel)
    tophat = top_hat(gambar, kernel)
    blackhat = black_hat(gambar, kernel)
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Baris 1: Binary operations
    axes[0, 0].imshow(binary, cmap='gray')
    axes[0, 0].set_title("Binary Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(gradient_binary, cmap='gray')
    axes[0, 1].set_title("Morph Gradient\n(Binary)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(gambar, cmap='gray')
    axes[0, 2].set_title("Grayscale Image")
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(gradient_gray, cmap='gray')
    axes[0, 3].set_title("Morph Gradient\n(Grayscale)")
    axes[0, 3].axis('off')
    
    # Baris 2: Top-hat and Black-hat
    axes[1, 0].imshow(gambar, cmap='gray')
    axes[1, 0].set_title("Original Grayscale")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(tophat, cmap='gray')
    axes[1, 1].set_title("Top-Hat\n(Original - Opening)")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(blackhat, cmap='gray')
    axes[1, 2].set_title("Black-Hat\n(Closing - Original)")
    axes[1, 2].axis('off')
    
    # Corrected image using top-hat
    corrected = cv2.add(gambar, tophat)
    axes[1, 3].imshow(corrected, cmap='gray')
    axes[1, 3].set_title("Corrected\n(Original + Top-Hat)")
    axes[1, 3].axis('off')
    
    plt.suptitle("Operasi Morfologi Lanjutan", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_kernel_shape_effect():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi pengaruh bentuk kernel
    """
    print("\n" + "=" * 60)
    print("PENGARUH BENTUK KERNEL")
    print("=" * 60)
    
    print("""
# Keterangan: Mulai blok kode baru.
RECTANGULAR KERNEL:
# Keterangan: Jalankan perintah berikut.
├── All-direction operation
# Keterangan: Jalankan perintah berikut.
├── Paling umum digunakan
# Keterangan: Jalankan perintah berikut.
└── Baik untuk objek dengan edge lurus

# Keterangan: Mulai blok kode baru.
ELLIPSE KERNEL:
# Keterangan: Jalankan perintah berikut.
├── Isotropic (uniform di semua arah)
# Keterangan: Jalankan perintah berikut.
├── Lebih smooth hasil
# Keterangan: Jalankan perintah berikut.
└── Baik untuk objek circular/rounded

# Keterangan: Mulai blok kode baru.
CROSS KERNEL:
# Keterangan: Jalankan perintah berikut.
├── Only horizontal dan vertical
# Keterangan: Jalankan perintah berikut.
├── Menjaga corner
# Keterangan: Jalankan perintah berikut.
└── Baik untuk text processing
    """)
    
    gambar = buat_gambar_sample()
    shapes = ['rect', 'ellipse', 'cross']
    
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    for i, shape in enumerate(shapes):
        kernel = dapatkan_kernel(shape, KERNEL_SIZE)
        
        axes[i, 0].imshow(gambar, cmap='gray')
        axes[i, 0].set_title(f"Original ({shape})")
        axes[i, 0].axis('off')
        
        axes[i, 1].imshow(erosion(gambar, kernel, 2), cmap='gray')
        axes[i, 1].set_title(f"Erosion ({shape})")
        axes[i, 1].axis('off')
        
        axes[i, 2].imshow(dilation(gambar, kernel, 2), cmap='gray')
        axes[i, 2].set_title(f"Dilation ({shape})")
        axes[i, 2].axis('off')
        
        axes[i, 3].imshow(morphological_gradient(gambar, kernel), cmap='gray')
        axes[i, 3].set_title(f"Gradient ({shape})")
        axes[i, 3].axis('off')
    
    plt.suptitle(f"Pengaruh Bentuk Kernel (Size: {KERNEL_SIZE}×{KERNEL_SIZE})", 
                 fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PRAKTIKUM: OPERASI MORFOLOGI")
    # Keterangan: Jalankan perintah berikut.
    print("Bab 3 - Pemrosesan Citra")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
OPERASI MORFOLOGI adalah teknik pemrosesan citra yang
beroperasi berdasarkan bentuk (shape) objek dalam gambar.

Operasi Dasar:
├── Erosion:  Mengecilkan objek
├── Dilation: Memperbesar objek
├── Opening:  Erosi + Dilasi (hapus noise)
└── Closing:  Dilasi + Erosi (isi lubang)

Aplikasi:
├── Noise removal
├── Object segmentation
├── Shape analysis
├── Text extraction
├── Medical image processing
└── Industrial inspection
    """)
    
    # Load atau buat gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Jalankan perintah berikut.
        print(f"[INFO] Memuat gambar: {path_gambar}")
        # Keterangan: Baca gambar dari file ke array.
        gambar_bgr = cv2.imread(path_gambar)
        # Keterangan: Konversi ruang warna gambar.
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
        # Keterangan: Inisialisasi beberapa variabel (_, gambar).
        _, gambar = cv2.threshold(gambar, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Jalankan perintah berikut.
        print("[INFO] Membuat gambar sample...")
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Kernel Size: {KERNEL_SIZE}")
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Kernel Shape: {KERNEL_SHAPE}")
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Iterations: {ITERATIONS}")
    
    # Keterangan: Inisialisasi atau perbarui variabel kernel.
    kernel = dapatkan_kernel(KERNEL_SHAPE, KERNEL_SIZE)
    
    # Apply basic operations
    # Keterangan: Inisialisasi atau perbarui variabel eroded.
    eroded = erosion(gambar, kernel, ITERATIONS)
    # Keterangan: Inisialisasi atau perbarui variabel dilated.
    dilated = dilation(gambar, kernel, ITERATIONS)
    # Keterangan: Inisialisasi atau perbarui variabel opened.
    opened = opening(gambar, kernel)
    # Keterangan: Inisialisasi atau perbarui variabel closed.
    closed = closing(gambar, kernel)
    
    # Tampilkan hasil
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(gambar, cmap).
    axes[0, 0].imshow(gambar, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(eroded, cmap).
    axes[0, 1].imshow(eroded, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title(f"Erosion (iter).
    axes[0, 1].set_title(f"Erosion (iter={ITERATIONS})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(dilated, cmap).
    axes[0, 2].imshow(dilated, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].set_title(f"Dilation (iter).
    axes[0, 2].set_title(f"Dilation (iter={ITERATIONS})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(opened, cmap).
    axes[1, 0].imshow(opened, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Opening\n(Erosi → Dilasi)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(closed, cmap).
    axes[1, 1].imshow(closed, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Closing\n(Dilasi → Erosi)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(morphological_gradient(gambar, kernel), cmap).
    axes[1, 2].imshow(morphological_gradient(gambar, kernel), cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Morphological Gradient")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Demo tambahan
    # Keterangan: Jalankan perintah berikut.
    demo_konsep_morfologi()
    # Keterangan: Jalankan perintah berikut.
    demo_erosion_dilation()
    # Keterangan: Jalankan perintah berikut.
    demo_opening_closing()
    # Keterangan: Jalankan perintah berikut.
    demo_advanced_operations()
    # Keterangan: Jalankan perintah berikut.
    demo_kernel_shape_effect()
    
    # Ringkasan
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("RINGKASAN OPERASI MORFOLOGI")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# STRUCTURING ELEMENT
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

# OPERASI DASAR
eroded = cv2.erode(img, kernel, iterations=1)
dilated = cv2.dilate(img, kernel, iterations=1)

# OPERASI KOMBINASI
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

PEMILIHAN OPERASI:
├── Noise putih (salt)  → Opening
├── Noise hitam (pepper)→ Closing
├── Noise campuran     → Opening + Closing
├── Edge detection     → Morphological Gradient
├── Uneven illumination→ Top-hat + Original
└── Lubang dalam objek → Closing

TIPS:
1. Kernel size tergantung ukuran noise/fitur
2. Gunakan iterasi > 1 untuk efek lebih kuat
3. Ellipse kernel untuk hasil lebih smooth
4. Selalu convert ke binary dulu untuk hasil terbaik
""")


# Jalankan program utama
# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Jalankan perintah berikut.
    main()
