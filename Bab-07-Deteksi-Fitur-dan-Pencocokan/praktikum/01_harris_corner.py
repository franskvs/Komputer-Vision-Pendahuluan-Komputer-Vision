"""
=============================================================================
PRAKTIKUM 1: HARRIS CORNER DETECTION
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan algoritma Harris Corner Detection untuk
    mendeteksi sudut/corner pada gambar. Corner adalah titik di mana
    terjadi perubahan intensitas yang signifikan di berbagai arah.

Konsep Utama:
    - Harris menghitung matriks struktur M dari gradien gambar
    - Corner response R = det(M) - k * trace(M)²
    - R > threshold → corner terdeteksi

Aplikasi Dunia Nyata:
    - Kalibrasi kamera dengan checkerboard
    - Tracking objek dalam video
    - Image registration
    - Augmented Reality

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Ukuran neighborhood untuk perhitungan gradien
# Nilai lebih besar = corner lebih "smooth", nilai kecil = lebih detail
BLOCK_SIZE = 2  # Coba ubah: 2, 3, 5, 7

# Ukuran aperture Sobel (untuk menghitung gradien)
# Harus ganjil: 1, 3, 5, 7
KSIZE = 3  # Coba ubah: 1, 3, 5, 7

# Parameter Harris (k) - mengontrol sensitivitas
# Nilai kecil = lebih sensitif (lebih banyak corner)
# Nilai besar = kurang sensitif (hanya corner kuat)
K_VALUE = 0.04  # Coba ubah: 0.02, 0.04, 0.06, 0.08

# Threshold untuk deteksi corner (persentase dari nilai maksimum)
# Nilai kecil = lebih banyak corner, nilai besar = corner kuat saja
THRESHOLD_PERCENT = 0.01  # Coba ubah: 0.005, 0.01, 0.05, 0.1

# Warna untuk menandai corner (BGR format)
CORNER_COLOR = (0, 0, 255)  # Merah. Coba: (0,255,0) hijau, (255,0,0) biru

# Ukuran marker untuk corner
MARKER_SIZE = 3  # Coba ubah: 1, 3, 5, 7
# ======================================================================

import cv2
import numpy as np
import os
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def harris_corner_detection(image_path):
    """
    Melakukan Harris Corner Detection pada gambar
    
    Args:
        image_path: Path ke file gambar
        
    Returns:
        Tuple (original_image, result_image, corner_count, processing_time)
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    # Copy untuk hasil
    result = img.copy()
    
    # Konversi ke grayscale (Harris memerlukan gambar grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Konversi ke float32 (diperlukan oleh cornerHarris)
    gray_float = np.float32(gray)
    
    # Mulai timing
    start_time = time.time()
    
    # Aplikasikan Harris Corner Detection
    # Output: array dengan nilai response di setiap pixel
    harris_response = cv2.cornerHarris(
        gray_float,
        blockSize=BLOCK_SIZE,
        ksize=KSIZE,
        k=K_VALUE
    )
    
    processing_time = (time.time() - start_time) * 1000  # dalam ms
    
    # Dilasi untuk memperjelas corner (opsional)
    harris_response = cv2.dilate(harris_response, None)
    
    # Threshold: ambil corner dengan response tinggi
    threshold = THRESHOLD_PERCENT * harris_response.max()
    corner_mask = harris_response > threshold
    
    # Hitung jumlah corner
    corner_count = np.sum(corner_mask)
    
    # Tandai corner pada gambar hasil
    result[corner_mask] = CORNER_COLOR
    
    return img, result, corner_count, processing_time, harris_response

def create_visualization(original, result, harris_response, corner_count, proc_time):
    """
    Membuat visualisasi gabungan hasil deteksi
    """
    # Normalize harris response untuk visualisasi
    harris_norm = cv2.normalize(harris_response, None, 0, 255, cv2.NORM_MINMAX)
    harris_norm = np.uint8(harris_norm)
    harris_color = cv2.applyColorMap(harris_norm, cv2.COLORMAP_JET)
    
    # Resize jika gambar terlalu besar
    max_width = 600
    h, w = original.shape[:2]
    if w > max_width:
        scale = max_width / w
        original = cv2.resize(original, None, fx=scale, fy=scale)
        result = cv2.resize(result, None, fx=scale, fy=scale)
        harris_color = cv2.resize(harris_color, None, fx=scale, fy=scale)
    
    # Tambah teks informasi
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Penjelasan parameter cv2.putText:
    # cv2.putText(image, text, org, fontFace, fontScale, color, thickness, lineType)
    # - image: gambar target
    # - text: teks yang akan ditulis
    # - org: posisi (x, y) kiri-bawah teks
    # - fontFace: jenis font
    # - fontScale: skala ukuran font
    # - color: warna (BGR)
    # - thickness: ketebalan teks
    # - lineType: tipe garis (opsional)
    cv2.putText(original, "Original", (10, 30), font, 1, (0, 255, 0), 2)
    cv2.putText(result, f"Corners: {corner_count}", (10, 30), font, 1, (0, 255, 0), 2)
    cv2.putText(harris_color, "Harris Response", (10, 30), font, 1, (255, 255, 255), 2)
    
    # Gabungkan horizontal
    combined = np.hstack([original, result, harris_color])
    
    return combined

def main():
    print("=" * 70)
    print("PRAKTIKUM 1: HARRIS CORNER DETECTION")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - Block Size: {BLOCK_SIZE}")
    print(f"  - Aperture Size (ksize): {KSIZE}")
    print(f"  - K Value: {K_VALUE}")
    print(f"  - Threshold: {THRESHOLD_PERCENT * 100}% dari max response")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Gambar untuk diproses
    test_images = ["checkerboard.png", "building.jpg", "box.png"]
    
    for image_name in test_images:
        image_path = os.path.join(data_dir, image_name)
        
        if not os.path.exists(image_path):
            print(f"⚠ File tidak ditemukan: {image_name}")
            print("  Jalankan download_sample_data.py terlebih dahulu")
            continue
        
        print(f"Memproses: {image_name}")
        print("-" * 40)
        
        try:
            # Deteksi corner
            original, result, corner_count, proc_time, harris_resp = \
                harris_corner_detection(image_path)
            
            print(f"  Jumlah corner terdeteksi: {corner_count}")
            print(f"  Waktu proses: {proc_time:.2f} ms")
            
            # Buat visualisasi
            visualization = create_visualization(
                original.copy(), result, harris_resp, corner_count, proc_time
            )
            
            # Simpan hasil
            output_name = f"harris_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")
            
            # Tampilkan (opsional - uncomment jika ingin lihat)
            # cv2.imshow(f"Harris Corner - {image_name}", visualization)
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah BLOCK_SIZE dari 2 ke 7
   - Amati: Apakah corner lebih sedikit atau lebih banyak?
   - Mengapa: Block size besar = area averaging lebih luas
   
2. Ubah K_VALUE dari 0.04 ke 0.08
   - Amati: Bagaimana perubahan sensitivitas?
   - Mengapa: K besar = response formula lebih ketat
   
3. Ubah THRESHOLD_PERCENT dari 0.01 ke 0.1
   - Amati: Hanya corner kuat yang terdeteksi
   - Mengapa: Threshold tinggi = filter lebih ketat
   
4. Bandingkan hasil pada checkerboard vs building
   - Checkerboard: Corner teratur pada sudut kotak
   - Building: Corner alami pada fitur arsitektur
""")
    
    # Tunggu input jika ada window yang ditampilkan
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
