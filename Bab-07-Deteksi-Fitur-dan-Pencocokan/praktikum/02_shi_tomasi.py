"""
=============================================================================
PRAKTIKUM 2: SHI-TOMASI CORNER DETECTION (Good Features to Track)
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan algoritma Shi-Tomasi yang merupakan
    perbaikan dari Harris Corner Detection. Shi-Tomasi menggunakan
    minimum eigenvalue sebagai kriteria, menghasilkan corner yang lebih
    cocok untuk tracking.

Konsep Utama:
    - Harris: R = λ1*λ2 - k*(λ1+λ2)²
    - Shi-Tomasi: R = min(λ1, λ2)
    - Corner yang baik untuk tracking lebih stabil

Perbedaan dengan Harris:
    - Lebih stabil untuk aplikasi tracking
    - Hasil lebih konsisten antar frame
    - Digunakan dalam Lucas-Kanade optical flow

Aplikasi Dunia Nyata:
    - Video tracking (mengikuti objek bergerak)
    - Stabilisasi video
    - Motion estimation
    - SLAM (Simultaneous Localization and Mapping)

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Jumlah maksimum corner yang ingin dideteksi
# Algoritma akan memilih N corner terbaik
MAX_CORNERS = 100  # Coba ubah: 50, 100, 200, 500

# Quality level (0-1) - minimum eigenvalue ratio
# Corner dengan quality < qualityLevel * maxQuality akan dibuang
QUALITY_LEVEL = 0.01  # Coba ubah: 0.005, 0.01, 0.05, 0.1

# Jarak minimum antar corner (dalam pixel)
# Corner yang terlalu dekat akan digabung
MIN_DISTANCE = 10  # Coba ubah: 5, 10, 20, 30

# Ukuran block untuk perhitungan corner
BLOCK_SIZE = 3  # Coba ubah: 3, 5, 7

# Gunakan Harris detector sebagai basis? (True/False)
USE_HARRIS = False  # Coba ubah: True, False

# K parameter jika USE_HARRIS = True
K_HARRIS = 0.04  # Coba ubah: 0.04, 0.06

# Warna dan ukuran marker
CORNER_COLOR = (0, 255, 0)  # Hijau
CIRCLE_RADIUS = 5  # Coba ubah: 3, 5, 7, 10
# ======================================================================

import cv2
import numpy as np
import os
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def shi_tomasi_detection(image_path):
    """
    Melakukan Shi-Tomasi Corner Detection pada gambar
    
    Args:
        image_path: Path ke file gambar
        
    Returns:
        Tuple (original_image, result_image, corners, processing_time)
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    # Copy untuk hasil
    result = img.copy()
    
    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Mulai timing
    start_time = time.time()
    
    # Aplikasikan Shi-Tomasi Corner Detection
    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=MAX_CORNERS,
        qualityLevel=QUALITY_LEVEL,
        minDistance=MIN_DISTANCE,
        blockSize=BLOCK_SIZE,
        useHarrisDetector=USE_HARRIS,
        k=K_HARRIS if USE_HARRIS else 0.04
    )
    
    processing_time = (time.time() - start_time) * 1000  # dalam ms
    
    # Gambar corner pada hasil
    if corners is not None:
        corners = np.int32(corners)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(result, (x, y), CIRCLE_RADIUS, CORNER_COLOR, -1)
    
    return img, result, corners, processing_time

def compare_parameters(image_path):
    """
    Membandingkan hasil dengan berbagai parameter
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Parameter berbeda untuk perbandingan
    param_sets = [
        {"maxCorners": 50, "qualityLevel": 0.01, "minDistance": 10, "label": "50 corners"},
        {"maxCorners": 100, "qualityLevel": 0.01, "minDistance": 10, "label": "100 corners"},
        {"maxCorners": 200, "qualityLevel": 0.01, "minDistance": 10, "label": "200 corners"},
        {"maxCorners": 100, "qualityLevel": 0.05, "minDistance": 10, "label": "High quality"},
    ]
    
    results = []
    
    for params in param_sets:
        result = img.copy()
        
        corners = cv2.goodFeaturesToTrack(
            gray,
            maxCorners=params["maxCorners"],
            qualityLevel=params["qualityLevel"],
            minDistance=params["minDistance"],
            blockSize=3
        )
        
        if corners is not None:
            corners = np.int32(corners)
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(result, (x, y), 4, (0, 255, 0), -1)
        
        # Tambah label
        label = f"{params['label']}: {len(corners) if corners is not None else 0}"

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
        cv2.putText(result, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (0, 255, 255), 2)
        
        results.append(result)
    
    # Resize dan gabungkan
    max_width = 400
    h, w = results[0].shape[:2]
    if w > max_width:
        scale = max_width / w
        results = [cv2.resize(r, None, fx=scale, fy=scale) for r in results]
    
    # Gabung 2x2
    row1 = np.hstack([results[0], results[1]])
    row2 = np.hstack([results[2], results[3]])
    comparison = np.vstack([row1, row2])
    
    return comparison

def main():
    print("=" * 70)
    print("PRAKTIKUM 2: SHI-TOMASI CORNER DETECTION")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - Max Corners: {MAX_CORNERS}")
    print(f"  - Quality Level: {QUALITY_LEVEL}")
    print(f"  - Min Distance: {MIN_DISTANCE} pixels")
    print(f"  - Block Size: {BLOCK_SIZE}")
    print(f"  - Use Harris: {USE_HARRIS}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Gambar untuk diproses
    test_images = ["checkerboard.png", "building.jpg", "butterfly.jpg"]
    
    for image_name in test_images:
        image_path = os.path.join(data_dir, image_name)
        
        if not os.path.exists(image_path):
            print(f"⚠ File tidak ditemukan: {image_name}")
            continue
        
        print(f"Memproses: {image_name}")
        print("-" * 40)
        
        try:
            # Deteksi corner
            original, result, corners, proc_time = shi_tomasi_detection(image_path)
            
            corner_count = len(corners) if corners is not None else 0
            print(f"  Jumlah corner terdeteksi: {corner_count}")
            print(f"  Waktu proses: {proc_time:.2f} ms")
            
            # Resize untuk visualisasi
            max_width = 600
            h, w = original.shape[:2]
            if w > max_width:
                scale = max_width / w
                original = cv2.resize(original, None, fx=scale, fy=scale)
                result = cv2.resize(result, None, fx=scale, fy=scale)
            
            # Tambah label
            cv2.putText(original, "Original", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(result, f"Shi-Tomasi: {corner_count} corners", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Gabungkan
            visualization = np.hstack([original, result])
            
            # Simpan hasil
            output_name = f"shi_tomasi_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Buat perbandingan parameter
    print("Membuat perbandingan parameter...")
    comparison_image = "building.jpg"
    comparison_path = os.path.join(data_dir, comparison_image)
    
    if os.path.exists(comparison_path):
        comparison = compare_parameters(comparison_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "shi_tomasi_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan disimpan: {output_path}")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah MAX_CORNERS dari 100 ke 500
   - Amati: Distribusi corner pada gambar
   - Pertanyaan: Apakah semua corner berkualitas sama?
   
2. Ubah QUALITY_LEVEL dari 0.01 ke 0.1
   - Amati: Corner dengan eigenvalue rendah dibuang
   - Mengapa: Hanya corner "kuat" yang tersisa
   
3. Ubah MIN_DISTANCE dari 10 ke 30
   - Amati: Corner menjadi lebih tersebar
   - Mengapa: Mencegah clustering di area kaya fitur
   
4. Set USE_HARRIS = True
   - Amati: Perbedaan dengan mode default
   - Perbandingan: Harris vs min eigenvalue
   
5. Perbandingan dengan Harris (Praktikum 1):
   - Jalankan kedua program pada gambar yang sama
   - Bandingkan lokasi dan jumlah corner
   - Mana yang lebih cocok untuk tracking?
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
