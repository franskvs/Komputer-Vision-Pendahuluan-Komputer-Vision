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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "sample.jpg"

# 2. Kernel size untuk operasi morfologi
KERNEL_SIZE = 5

# 3. Kernel shape
# Opsi: 'rect', 'ellipse', 'cross'
KERNEL_SHAPE = 'rect'

# 4. Jumlah iterasi untuk erosion/dilation
ITERATIONS = 1

# 5. Threshold untuk binary image
BINARY_THRESHOLD = 127

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
    """Membuat gambar biner sample untuk demonstrasi morfologi"""
    gambar = np.zeros((300, 400), dtype=np.uint8)
    
    # Objek utama
    cv2.rectangle(gambar, (50, 50), (150, 150), 255, -1)
    cv2.circle(gambar, (280, 100), 50, 255, -1)
    cv2.fillPoly(gambar, [np.array([[200, 250], [250, 180], [300, 250]])], 255)
    
    # Tambah text
    cv2.putText(gambar, "MORPH", (100, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    
    return gambar


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
    Membuat structuring element (kernel) untuk operasi morfologi
    
    Parameter:
    - shape: 'rect', 'ellipse', atau 'cross'
    - size: ukuran kernel
    
    Return:
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
    Erosi morfologi
    
    Mengecilkan objek putih (foreground)
    Menghilangkan noise kecil
    Memisahkan objek yang terhubung
    
    Prinsip:
    - Kernel slide di atas gambar
    - Piksel output = minimum dari piksel dalam kernel
    - Untuk binary: output 1 hanya jika SEMUA piksel dalam kernel = 1
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    - iterations: jumlah pengulangan
    
    Return:
    - gambar hasil erosi
    """
    hasil = cv2.erode(gambar, kernel, iterations=iterations)
    return hasil


def dilation(gambar, kernel, iterations=1):
    """
    Dilasi morfologi
    
    Memperbesar objek putih (foreground)
    Mengisi lubang kecil
    Menghubungkan objek yang terpisah
    
    Prinsip:
    - Kernel slide di atas gambar
    - Piksel output = maximum dari piksel dalam kernel
    - Untuk binary: output 1 jika SETIDAKNYA SATU piksel dalam kernel = 1
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    - iterations: jumlah pengulangan
    
    Return:
    - gambar hasil dilasi
    """
    hasil = cv2.dilate(gambar, kernel, iterations=iterations)
    return hasil


def opening(gambar, kernel):
    """
    Opening = Erosi + Dilasi
    
    Menghilangkan noise kecil di foreground
    Menjaga ukuran objek relatif sama
    
    Urutan: Erosi dulu → baru Dilasi
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    
    Return:
    - gambar hasil opening
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_OPEN, kernel)
    return hasil


def closing(gambar, kernel):
    """
    Closing = Dilasi + Erosi
    
    Mengisi lubang kecil di foreground
    Menghubungkan komponen yang hampir tersambung
    
    Urutan: Dilasi dulu → baru Erosi
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    
    Return:
    - gambar hasil closing
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_CLOSE, kernel)
    return hasil


# ============================================================
# FUNGSI OPERASI MORFOLOGI LANJUTAN
# ============================================================

def morphological_gradient(gambar, kernel):
    """
    Gradient Morfologi = Dilasi - Erosi
    
    Menghasilkan outline/edge dari objek
    Berguna untuk edge detection pada binary images
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    
    Return:
    - gambar gradient
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_GRADIENT, kernel)
    return hasil


def top_hat(gambar, kernel):
    """
    Top-Hat Transform = Original - Opening
    
    Mengisolasi bright spots (peaks) yang lebih kecil dari kernel
    Berguna untuk menemukan bright regions pada background gelap
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    
    Return:
    - gambar top-hat
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_TOPHAT, kernel)
    return hasil


def black_hat(gambar, kernel):
    """
    Black-Hat Transform = Closing - Original
    
    Mengisolasi dark spots (valleys) yang lebih kecil dari kernel
    Berguna untuk menemukan dark regions pada background terang
    
    Parameter:
    - gambar: input binary/grayscale image
    - kernel: structuring element
    
    Return:
    - gambar black-hat
    """
    hasil = cv2.morphologyEx(gambar, cv2.MORPH_BLACKHAT, kernel)
    return hasil


def hit_or_miss(gambar, kernel1, kernel2=None):
    """
    Hit-or-Miss Transform
    
    Mendeteksi pattern spesifik dalam binary image
    Berguna untuk shape detection, thinning, pruning
    
    Parameter:
    - gambar: input binary image
    - kernel1: structuring element untuk foreground match
    - kernel2: structuring element untuk background match (optional)
    
    Return:
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
    Demonstrasi konsep dasar operasi morfologi
    """
    print("\n" + "=" * 60)
    print("KONSEP OPERASI MORFOLOGI")
    print("=" * 60)
    
    print("""
OPERASI MORFOLOGI adalah teknik pemrosesan citra berbasis
bentuk (shape) menggunakan structuring element (kernel).

STRUCTURING ELEMENT (KERNEL):
┌───────────────────────────────────────────────────┐
│  RECT (Rectangle)  │  ELLIPSE  │  CROSS          │
│  ■ ■ ■             │  · ■ ■ ■ ·│    ■            │
│  ■ ■ ■             │  ■ ■ ■ ■ ■│  ■ ■ ■          │
│  ■ ■ ■             │  ■ ■ ■ ■ ■│    ■            │
│                    │  · ■ ■ ■ ·│                 │
└───────────────────────────────────────────────────┘

OPERASI DASAR:
├── Erosion:  Mengecilkan objek (MIN operation)
├── Dilation: Memperbesar objek (MAX operation)
├── Opening:  Erosi + Dilasi (hapus noise kecil)
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
    Demonstrasi erosi dan dilasi
    """
    print("\n" + "=" * 60)
    print("EROSI DAN DILASI")
    print("=" * 60)
    
    print("""
EROSION (Erosi):
├── Piksel output = 1 hanya jika SEMUA piksel dalam kernel = 1
├── Efek: mengecilkan objek, memisahkan objek yang terhubung
├── Menghilangkan protrusions (tonjolan kecil)
└── Menghapus noise putih (salt noise)

DILATION (Dilasi):
├── Piksel output = 1 jika SETIDAKNYA SATU piksel dalam kernel = 1
├── Efek: memperbesar objek, menghubungkan objek yang terpisah
├── Mengisi lubang kecil
└── Menghapus noise hitam (pepper noise)

ITERATIONS:
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
    Demonstrasi opening dan closing untuk noise removal
    """
    print("\n" + "=" * 60)
    print("OPENING DAN CLOSING")
    print("=" * 60)
    
    print("""
OPENING = Erosi → Dilasi:
├── Menghilangkan small bright spots (salt noise)
├── Menghilangkan protrusions
├── Smoothing boundary dari luar
└── Tidak mengubah ukuran objek secara signifikan

CLOSING = Dilasi → Erosi:
├── Mengisi small dark spots (pepper noise, lubang)
├── Menyambung objek yang hampir terhubung
├── Smoothing boundary dari dalam
└── Tidak mengubah ukuran objek secara signifikan

KOMBINASI Opening + Closing:
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
    Demonstrasi operasi morfologi lanjutan
    """
    print("\n" + "=" * 60)
    print("OPERASI MORFOLOGI LANJUTAN")
    print("=" * 60)
    
    print("""
MORPHOLOGICAL GRADIENT = Dilasi - Erosi:
└── Menghasilkan outline/kontur dari objek

TOP-HAT = Original - Opening:
├── Mengisolasi bright spots (lebih kecil dari kernel)
└── Berguna untuk uneven illumination correction

BLACK-HAT = Closing - Original:
├── Mengisolasi dark spots (lebih kecil dari kernel)
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
    Demonstrasi pengaruh bentuk kernel
    """
    print("\n" + "=" * 60)
    print("PENGARUH BENTUK KERNEL")
    print("=" * 60)
    
    print("""
RECTANGULAR KERNEL:
├── All-direction operation
├── Paling umum digunakan
└── Baik untuk objek dengan edge lurus

ELLIPSE KERNEL:
├── Isotropic (uniform di semua arah)
├── Lebih smooth hasil
└── Baik untuk objek circular/rounded

CROSS KERNEL:
├── Only horizontal dan vertical
├── Menjaga corner
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
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: OPERASI MORFOLOGI")
    print("Bab 3 - Pemrosesan Citra")
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
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar_bgr = cv2.imread(path_gambar)
        gambar = cv2.cvtColor(gambar_bgr, cv2.COLOR_BGR2GRAY)
        _, gambar = cv2.threshold(gambar, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    else:
        print("[INFO] Membuat gambar sample...")
        gambar = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Kernel Size: {KERNEL_SIZE}")
    print(f"[INFO] Kernel Shape: {KERNEL_SHAPE}")
    print(f"[INFO] Iterations: {ITERATIONS}")
    
    kernel = dapatkan_kernel(KERNEL_SHAPE, KERNEL_SIZE)
    
    # Apply basic operations
    eroded = erosion(gambar, kernel, ITERATIONS)
    dilated = dilation(gambar, kernel, ITERATIONS)
    opened = opening(gambar, kernel)
    closed = closing(gambar, kernel)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(gambar, cmap='gray')
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(eroded, cmap='gray')
    axes[0, 1].set_title(f"Erosion (iter={ITERATIONS})")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(dilated, cmap='gray')
    axes[0, 2].set_title(f"Dilation (iter={ITERATIONS})")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(opened, cmap='gray')
    axes[1, 0].set_title("Opening\n(Erosi → Dilasi)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(closed, cmap='gray')
    axes[1, 1].set_title("Closing\n(Dilasi → Erosi)")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(morphological_gradient(gambar, kernel), cmap='gray')
    axes[1, 2].set_title("Morphological Gradient")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_konsep_morfologi()
    demo_erosion_dilation()
    demo_opening_closing()
    demo_advanced_operations()
    demo_kernel_shape_effect()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN OPERASI MORFOLOGI")
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
if __name__ == "__main__":
    main()
