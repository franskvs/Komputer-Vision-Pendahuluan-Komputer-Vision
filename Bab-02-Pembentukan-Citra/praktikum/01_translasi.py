# ============================================================
# PROGRAM: 01_translasi.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: Program ini mendemonstrasikan translasi (pergeseran)
#            gambar menggunakan transformation matrix
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep translasi dalam transformasi geometri
#   2. Memahami penggunaan cv2.warpAffine()
#   3. Memahami struktur translation matrix
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

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Nilai translasi dalam piksel
#    tx: pergeseran horizontal (positif = ke kanan)
#    ty: pergeseran vertikal (positif = ke bawah)
TX = 100  # Coba ubah: -100, 0, 50, 150
TY = 50   # Coba ubah: -50, 0, 30, 100

# 3. Mode border (apa yang mengisi area kosong)
#    cv2.BORDER_CONSTANT: Warna solid (hitam default)
#    cv2.BORDER_REPLICATE: Replikasi piksel tepi
#    cv2.BORDER_REFLECT: Cermin
MODE_BORDER = cv2.BORDER_CONSTANT

# 4. Warna border jika BORDER_CONSTANT (BGR)
WARNA_BORDER = (50, 50, 50)  # Abu-abu gelap

# ============================================================
# KONFIGURASI PATH
# ============================================================

# Dapatkan direktori script (praktiukm folder)
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_SCRIPT, "data", "images")
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output1")

# Pastikan folder output ada
os.makedirs(DIR_OUTPUT, exist_ok=True)

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(direktori_script, "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        # Coba folder Bab-01
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
        gambar[i, :] = [int(i/2), int(100 + i/4), int(200 - i/4)]
    
    # Shapes untuk referensi posisi
    cv2.rectangle(gambar, (50, 50), (150, 150), (255, 255, 255), -1)
    cv2.circle(gambar, (300, 200), 60, (0, 255, 255), -1)
    cv2.putText(gambar, "OpenCV", (200, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    # Garis referensi
    cv2.line(gambar, (0, 200), (600, 200), (128, 128, 128), 1)
    cv2.line(gambar, (300, 0), (300, 400), (128, 128, 128), 1)
    
    return gambar


# ============================================================
# FUNGSI TRANSLASI
# ============================================================

def translasi_gambar(gambar, tx, ty, border_mode=cv2.BORDER_CONSTANT, 
                     border_value=(0, 0, 0)):
    """
    Melakukan translasi (pergeseran) gambar
    
    Parameter:
    - gambar: input image
    - tx: pergeseran horizontal (piksel)
    - ty: pergeseran vertikal (piksel)
    - border_mode: cara mengisi area kosong
    - border_value: warna border jika BORDER_CONSTANT
    
    Return:
    - gambar yang sudah ditranslasi
    """
    tinggi, lebar = gambar.shape[:2]
    
    # Translation Matrix:
    # | 1  0  tx |
    # | 0  1  ty |
    #
    # Persamaan:
    # x' = 1*x + 0*y + tx = x + tx
    # y' = 0*x + 1*y + ty = y + ty
    
    translation_matrix = np.float32([
        [1, 0, tx],  # x' = x + tx
        [0, 1, ty]   # y' = y + ty
    ])
    
    # Terapkan transformasi
    hasil = cv2.warpAffine(
        gambar, 
        translation_matrix, 
        (lebar, tinggi),
        borderMode=border_mode,
        borderValue=border_value
    )
    
    return hasil, translation_matrix


def demo_translasi_berbagai_arah(gambar):
    """
    Demonstrasi translasi ke berbagai arah
    """
    print("\n" + "=" * 60)
    print("DEMO TRANSLASI KE BERBAGAI ARAH")
    print("=" * 60)
    
    translasi_list = [
        (0, 0, "Original"),
        (100, 0, "Kanan (+tx)"),
        (-100, 0, "Kiri (-tx)"),
        (0, 80, "Bawah (+ty)"),
        (0, -80, "Atas (-ty)"),
        (100, 80, "Kanan-Bawah"),
        (-100, -80, "Kiri-Atas"),
    ]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for i, (tx, ty, label) in enumerate(translasi_list):
        hasil, _ = translasi_gambar(gambar, tx, ty, 
                                    border_mode=cv2.BORDER_CONSTANT,
                                    border_value=WARNA_BORDER)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{label}\ntx={tx}, ty={ty}")
        axes[i].axis('off')
        
        print(f"[{i+1}] {label}: tx={tx}, ty={ty}")
    
    # Kosongkan subplot terakhir
    axes[7].axis('off')
    
    plt.suptitle("Translasi Gambar ke Berbagai Arah", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, 'demo_arah.png')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"[SAVED] Gambar disimpan ke: {output_path}")
    plt.close()


def demo_border_modes(gambar):
    """
    Demonstrasi berbagai mode border
    """
    print("\n" + "=" * 60)
    print("DEMO BERBAGAI MODE BORDER")
    print("=" * 60)
    
    # Translasi cukup besar untuk lihat efek border
    tx, ty = 150, 100
    
    border_modes = [
        (cv2.BORDER_CONSTANT, (0, 0, 0), "BORDER_CONSTANT (Hitam)"),
        (cv2.BORDER_CONSTANT, (255, 0, 0), "BORDER_CONSTANT (Biru)"),
        (cv2.BORDER_REPLICATE, None, "BORDER_REPLICATE"),
        (cv2.BORDER_REFLECT, None, "BORDER_REFLECT"),
        (cv2.BORDER_WRAP, None, "BORDER_WRAP"),
        (cv2.BORDER_REFLECT_101, None, "BORDER_REFLECT_101"),
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (mode, value, label) in enumerate(border_modes):
        if value is None:
            value = (0, 0, 0)
        
        hasil, _ = translasi_gambar(gambar, tx, ty, 
                                    border_mode=mode,
                                    border_value=value)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{label}")
        axes[i].axis('off')
        
        print(f"[{i+1}] {label}")
    
    plt.suptitle(f"Perbandingan Border Mode (tx={tx}, ty={ty})", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, 'demo_border_modes.png')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"[SAVED] Gambar disimpan ke: {output_path}")
    plt.close()


def visualisasi_matrix_translasi(gambar):
    """
    Visualisasi bagaimana translation matrix bekerja
    """
    print("\n" + "=" * 60)
    print("VISUALISASI TRANSLATION MATRIX")
    print("=" * 60)
    
    print("""
TRANSLATION MATRIX:
    
    | 1  0  tx |     | x |     | x + tx |
    |          |  x  |   |  =  |        |
    | 0  1  ty |     | y |     | y + ty |
    
Dimana:
- (x, y) adalah koordinat piksel asli
- (tx, ty) adalah nilai pergeseran
- Hasil adalah koordinat baru (x + tx, y + ty)

CONTOH:
Jika tx = 100, ty = 50
- Piksel di (0, 0) → pindah ke (100, 50)
- Piksel di (50, 30) → pindah ke (150, 80)
- Piksel di (100, 100) → pindah ke (200, 150)
""")
    
    # Tampilkan matrix untuk nilai saat ini
    print(f"\nTranslation Matrix untuk tx={TX}, ty={TY}:")
    print(f"    | 1  0  {TX:3d} |")
    print(f"    | 0  1  {TY:3d} |")
    
    # Visualisasi dengan titik-titik
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gambar asli dengan titik referensi
    gambar_ref = gambar.copy()
    points = [(100, 100), (300, 100), (300, 300), (100, 300)]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    
    for pt, color in zip(points, colors):
        cv2.circle(gambar_ref, pt, 10, color, -1)
        cv2.putText(gambar_ref, f"({pt[0]},{pt[1]})", (pt[0]+15, pt[1]), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    axes[0].imshow(cv2.cvtColor(gambar_ref, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Gambar Asli dengan Titik Referensi")
    axes[0].axis('off')
    
    # Gambar hasil translasi dengan titik baru
    hasil, _ = translasi_gambar(gambar, TX, TY, cv2.BORDER_CONSTANT, WARNA_BORDER)
    
    for pt, color in zip(points, colors):
        new_pt = (pt[0] + TX, pt[1] + TY)
        if 0 <= new_pt[0] < hasil.shape[1] and 0 <= new_pt[1] < hasil.shape[0]:
            cv2.circle(hasil, new_pt, 10, color, -1)
            cv2.putText(hasil, f"({new_pt[0]},{new_pt[1]})", (new_pt[0]+15, new_pt[1]), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Setelah Translasi (tx={TX}, ty={TY})")
    axes[1].axis('off')
    
    plt.suptitle("Pergerakan Titik Referensi Setelah Translasi", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, 'demo_matrix_visualization.png')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"[SAVED] Gambar disimpan ke: {output_path}")
    plt.close()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: TRANSLASI GAMBAR")
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
        if gambar.shape[1] > 800:
            scale = 800 / gambar.shape[1]
            gambar = cv2.resize(gambar, None, fx=scale, fy=scale)
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    
    # 1. Demo translasi sederhana
    print("\n[1] Translasi dengan nilai tx={}, ty={}".format(TX, TY))
    hasil, matrix = translasi_gambar(gambar, TX, TY, MODE_BORDER, WARNA_BORDER)
    
    # Tampilkan
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Gambar Asli")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Setelah Translasi\ntx={TX}, ty={TY}")
    axes[1].axis('off')
    
    plt.suptitle("Demonstrasi Translasi Gambar", fontsize=14)
    plt.tight_layout()
    output_path = os.path.join(DIR_OUTPUT, 'demo_translasi_simple.png')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"[SAVED] Gambar disimpan ke: {output_path}")
    plt.close()
    
    # 2. Demo translasi berbagai arah
    demo_translasi_berbagai_arah(gambar)
    
    # 3. Demo berbagai border mode
    demo_border_modes(gambar)
    
    # 4. Visualisasi matrix
    visualisasi_matrix_translasi(gambar)
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN TRANSLASI GAMBAR")
    print("=" * 60)
    print("""
TRANSLATION MATRIX:
    M = | 1  0  tx |
        | 0  1  ty |

PENGGUNAAN:
    cv2.warpAffine(src, M, (width, height), 
                   borderMode=..., borderValue=...)

BORDER MODES:
├── cv2.BORDER_CONSTANT  : Warna solid
├── cv2.BORDER_REPLICATE : Replikasi tepi
├── cv2.BORDER_REFLECT   : Cermin
├── cv2.BORDER_WRAP      : Wrapping
└── cv2.BORDER_REFLECT_101: Cermin tanpa duplikat tepi

TIPS:
- tx positif → gambar geser ke kanan
- tx negatif → gambar geser ke kiri
- ty positif → gambar geser ke bawah
- ty negatif → gambar geser ke atas
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
