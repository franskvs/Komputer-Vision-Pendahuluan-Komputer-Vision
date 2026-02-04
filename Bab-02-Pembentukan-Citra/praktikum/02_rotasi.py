# ============================================================
# PROGRAM: 02_rotasi.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: Program ini mendemonstrasikan rotasi gambar
#            dengan berbagai sudut dan titik pusat
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep rotasi dalam transformasi geometri
#   2. Memahami rotation matrix dan cara kerjanya
#   3. Mengatasi masalah gambar terpotong saat rotasi
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Gunakan backend non-GUI
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# ============================================================
# KONFIGURASI PATH
# ============================================================

# Dapatkan direktori script (praktikum folder)
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_SCRIPT, "data", "images")
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output2")

# Pastikan folder output ada
os.makedirs(DIR_OUTPUT, exist_ok=True)


# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Sudut rotasi dalam derajat
#    Positif = berlawanan arah jarum jam (counter-clockwise)
#    Negatif = searah jarum jam (clockwise)
SUDUT_ROTASI = 45  # Coba ubah: 15, 30, 45, 90, 180, -45

# 3. Skala saat rotasi (1.0 = ukuran asli)
SKALA = 1.0  # Coba ubah: 0.5, 0.8, 1.0, 1.2, 1.5

# 4. Titik pusat rotasi (None = tengah gambar)
#    Contoh: (0, 0) untuk sudut kiri atas
TITIK_PUSAT = None  # Coba ubah: (100, 100), (0, 0)

# 5. Apakah ingin bounding box diperbesar untuk menampung seluruh gambar?
AUTO_EXPAND = True

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(direktori_script, "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, "..", "..", 
                                  "Bab-01-Pendahuluan", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, nama_file)
    
    return path_data


def buat_gambar_sample():
    """Membuat gambar sample dengan shapes untuk demonstrasi"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background gradient
    for i in range(400):
        gambar[i, :] = [int(100 + i/4), int(150 - i/8), int(200 - i/4)]
    
    # Rectangle untuk melihat rotasi
    cv2.rectangle(gambar, (100, 100), (500, 300), (255, 255, 255), 2)
    cv2.rectangle(gambar, (120, 120), (480, 280), (0, 255, 255), 2)
    
    # Teks
    cv2.putText(gambar, "ROTASI", (200, 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Titik pusat
    cv2.circle(gambar, (300, 200), 5, (0, 0, 255), -1)
    cv2.putText(gambar, "Pusat", (310, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    return gambar


# ============================================================
# FUNGSI ROTASI
# ============================================================

def rotasi_gambar(gambar, sudut, skala=1.0, pusat=None):
    """
    Melakukan rotasi gambar (tanpa expand)
    
    Parameter:
    - gambar: input image
    - sudut: sudut rotasi dalam derajat
    - skala: faktor skala
    - pusat: titik pusat rotasi (default: tengah)
    
    Return:
    - gambar hasil rotasi
    - rotation matrix
    """
    tinggi, lebar = gambar.shape[:2]
    
    # Default pusat adalah tengah gambar
    if pusat is None:
        pusat = (lebar // 2, tinggi // 2)
    
    # Dapatkan rotation matrix
    # cv2.getRotationMatrix2D(center, angle, scale)
    rotation_matrix = cv2.getRotationMatrix2D(pusat, sudut, skala)
    
    # Terapkan rotasi
    hasil = cv2.warpAffine(gambar, rotation_matrix, (lebar, tinggi))
    
    return hasil, rotation_matrix


def rotasi_gambar_expand(gambar, sudut, skala=1.0):
    """
    Melakukan rotasi gambar dengan memperbesar canvas
    agar seluruh gambar terlihat
    
    Parameter:
    - gambar: input image
    - sudut: sudut rotasi dalam derajat
    - skala: faktor skala
    
    Return:
    - gambar hasil rotasi (ukuran lebih besar)
    - rotation matrix
    """
    tinggi, lebar = gambar.shape[:2]
    pusat = (lebar // 2, tinggi // 2)
    
    # Dapatkan rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(pusat, sudut, skala)
    
    # Hitung ukuran baru yang dibutuhkan
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    
    # Hitung bounding box baru
    lebar_baru = int((tinggi * sin) + (lebar * cos))
    tinggi_baru = int((tinggi * cos) + (lebar * sin))
    
    # Sesuaikan rotation matrix untuk translasi ke tengah canvas baru
    rotation_matrix[0, 2] += (lebar_baru / 2) - pusat[0]
    rotation_matrix[1, 2] += (tinggi_baru / 2) - pusat[1]
    
    # Terapkan rotasi dengan ukuran baru
    hasil = cv2.warpAffine(gambar, rotation_matrix, (lebar_baru, tinggi_baru))
    
    return hasil, rotation_matrix


def demo_rotasi_berbagai_sudut(gambar):
    """
    Demonstrasi rotasi dengan berbagai sudut
    """
    print("\n" + "=" * 60)
    print("DEMO ROTASI BERBAGAI SUDUT")
    print("=" * 60)
    
    sudut_list = [0, 30, 45, 60, 90, 120, 180, 270]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for i, sudut in enumerate(sudut_list):
        hasil, _ = rotasi_gambar(gambar, sudut)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"Rotasi {sudut}°")
        axes[i].axis('off')
        
        print(f"[{i+1}] Rotasi {sudut}°")
    
    plt.suptitle("Rotasi Gambar dengan Berbagai Sudut (tanpa expand)", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def demo_rotasi_expand_vs_normal(gambar):
    """
    Membandingkan rotasi normal vs dengan expand
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN ROTASI NORMAL VS EXPAND")
    print("=" * 60)
    
    sudut = 45
    
    # Rotasi normal (gambar terpotong)
    hasil_normal, _ = rotasi_gambar(gambar, sudut)
    
    # Rotasi dengan expand (gambar utuh)
    hasil_expand, _ = rotasi_gambar_expand(gambar, sudut)
    
    print(f"Sudut rotasi: {sudut}°")
    print(f"Ukuran asli   : {gambar.shape[1]} x {gambar.shape[0]}")
    print(f"Ukuran normal : {hasil_normal.shape[1]} x {hasil_normal.shape[0]}")
    print(f"Ukuran expand : {hasil_expand.shape[1]} x {hasil_expand.shape[0]}")
    
    # Tampilkan
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"Original\n{gambar.shape[1]}x{gambar.shape[0]}")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil_normal, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Rotasi {sudut}° (Normal)\n{hasil_normal.shape[1]}x{hasil_normal.shape[0]}\nSudut terpotong!")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hasil_expand, cv2.COLOR_BGR2RGB))
    axes[2].set_title(f"Rotasi {sudut}° (Expand)\n{hasil_expand.shape[1]}x{hasil_expand.shape[0]}\nGambar utuh")
    axes[2].axis('off')
    
    plt.suptitle("Perbandingan Rotasi Normal vs Expand", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def demo_rotasi_titik_pusat_berbeda(gambar):
    """
    Demonstrasi rotasi dengan titik pusat berbeda
    """
    print("\n" + "=" * 60)
    print("DEMO ROTASI DENGAN TITIK PUSAT BERBEDA")
    print("=" * 60)
    
    tinggi, lebar = gambar.shape[:2]
    sudut = 45
    
    # Berbagai titik pusat
    pusat_list = [
        ((lebar//2, tinggi//2), "Tengah"),
        ((0, 0), "Kiri Atas (0,0)"),
        ((lebar-1, 0), "Kanan Atas"),
        ((0, tinggi-1), "Kiri Bawah"),
        ((lebar//4, tinggi//4), "1/4 dari kiri atas"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Original
    gambar_marked = gambar.copy()
    for pusat, _ in pusat_list:
        cv2.circle(gambar_marked, pusat, 8, (0, 255, 0), -1)
    axes[0].imshow(cv2.cvtColor(gambar_marked, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original dengan titik pusat")
    axes[0].axis('off')
    
    for i, (pusat, label) in enumerate(pusat_list):
        hasil, _ = rotasi_gambar(gambar, sudut, pusat=pusat)
        
        # Tandai titik pusat pada hasil
        if 0 <= pusat[0] < hasil.shape[1] and 0 <= pusat[1] < hasil.shape[0]:
            cv2.circle(hasil, pusat, 8, (0, 255, 0), -1)
        
        axes[i+1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i+1].set_title(f"Pusat: {label}")
        axes[i+1].axis('off')
        
        print(f"[{i+1}] Rotasi {sudut}° dengan pusat di {label}")
    
    plt.suptitle(f"Rotasi {sudut}° dengan Titik Pusat Berbeda", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


def visualisasi_rotation_matrix(sudut):
    """
    Visualisasi rotation matrix
    """
    print("\n" + "=" * 60)
    print("PENJELASAN ROTATION MATRIX")
    print("=" * 60)
    
    # Convert ke radian
    theta = np.radians(sudut)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    
    print(f"""
ROTATION MATRIX (2D):

Untuk sudut θ = {sudut}°:

    | cos(θ)  -sin(θ) |     | {cos_t:7.4f}  {-sin_t:7.4f} |
R = |                 |  =  |                        |
    | sin(θ)   cos(θ) |     | {sin_t:7.4f}   {cos_t:7.4f} |

OpenCV Rotation Matrix (dengan translation dan scale):

    | α   β   (1-α)·cx - β·cy |
M = |                          |
    | -β  α   β·cx + (1-α)·cy |

Dimana:
    α = scale × cos(θ)
    β = scale × sin(θ)
    (cx, cy) = titik pusat rotasi

PERSAMAAN TRANSFORMASI:
    x' = α·x + β·y + (1-α)·cx - β·cy
    y' = -β·x + α·y + β·cx + (1-α)·cy

CATATAN:
- Sudut positif → rotasi counter-clockwise
- Sudut negatif → rotasi clockwise
- Scale = 1.0 → ukuran tetap
- Scale > 1.0 → diperbesar
- Scale < 1.0 → diperkecil
""")


def demo_rotasi_dengan_skala(gambar):
    """
    Demonstrasi rotasi dengan berbagai skala
    """
    print("\n" + "=" * 60)
    print("DEMO ROTASI DENGAN SKALA BERBEDA")
    print("=" * 60)
    
    kombinasi = [
        (0, 1.0, "Original"),
        (45, 0.5, "Rotasi 45°, Scale 0.5"),
        (45, 1.0, "Rotasi 45°, Scale 1.0"),
        (45, 1.5, "Rotasi 45°, Scale 1.5"),
        (90, 0.8, "Rotasi 90°, Scale 0.8"),
        (180, 1.2, "Rotasi 180°, Scale 1.2"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (sudut, skala, label) in enumerate(kombinasi):
        hasil, _ = rotasi_gambar(gambar, sudut, skala)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{label}")
        axes[i].axis('off')
        
        print(f"[{i+1}] {label}")
    
    plt.suptitle("Rotasi dengan Berbagai Kombinasi Sudut dan Skala", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: ROTASI GAMBAR")
    print("Bab 2 - Pembentukan Citra")
    print("=" * 60)
    
    # Muat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    gambar = cv2.imread(path_gambar)
    
    if gambar is None:
        print(f"[WARNING] Gambar {NAMA_FILE_GAMBAR} tidak ditemukan")
        print("[INFO] Menggunakan gambar sample...")
        gambar = buat_gambar_sample()
    else:
        print(f"[SUKSES] Gambar dimuat: {path_gambar}")
        # Resize jika terlalu besar
        if gambar.shape[1] > 600:
            scale = 600 / gambar.shape[1]
            gambar = cv2.resize(gambar, None, fx=scale, fy=scale)
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    
    # 1. Penjelasan rotation matrix
    visualisasi_rotation_matrix(SUDUT_ROTASI)
    
    # 2. Rotasi sederhana
    print(f"\n[DEMO] Rotasi dengan sudut={SUDUT_ROTASI}°, skala={SKALA}")
    
    if AUTO_EXPAND:
        hasil, matrix = rotasi_gambar_expand(gambar, SUDUT_ROTASI, SKALA)
    else:
        hasil, matrix = rotasi_gambar(gambar, SUDUT_ROTASI, SKALA, TITIK_PUSAT)
    
    # Tampilkan
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Gambar Asli")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Rotasi {SUDUT_ROTASI}°, Skala {SKALA}")
    axes[1].axis('off')
    
    plt.suptitle("Demonstrasi Rotasi Gambar", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, "output.png")

    plt.savefig(output_path, dpi=100, bbox_inches="tight")

    print(f"[SAVED] {output_path}")

    plt.close()
    
    # 3. Demo berbagai sudut
    demo_rotasi_berbagai_sudut(gambar)
    
    # 4. Demo expand vs normal
    demo_rotasi_expand_vs_normal(gambar)
    
    # 5. Demo titik pusat berbeda
    demo_rotasi_titik_pusat_berbeda(gambar)
    
    # 6. Demo dengan skala
    demo_rotasi_dengan_skala(gambar)
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN ROTASI GAMBAR")
    print("=" * 60)
    print("""
FUNGSI UTAMA:
    M = cv2.getRotationMatrix2D(center, angle, scale)
    hasil = cv2.warpAffine(src, M, (width, height))

PARAMETER:
├── center: titik pusat rotasi (x, y)
├── angle: sudut dalam derajat (positif = CCW)
└── scale: faktor skala

TIPS MENGHINDARI GAMBAR TERPOTONG:
1. Hitung bounding box baru berdasarkan cos dan sin
2. Sesuaikan translation pada matrix
3. Gunakan ukuran output yang lebih besar

RUMUS BOUNDING BOX BARU:
    new_width = height × |sin(θ)| + width × |cos(θ)|
    new_height = height × |cos(θ)| + width × |sin(θ)|

EKSPERIMEN:
- Ubah SUDUT_ROTASI dan SKALA di awal program
- Bandingkan hasil expand vs normal
- Coba berbagai titik pusat rotasi
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
