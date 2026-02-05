"""
=============================================================================
PRAKTIKUM 4: ORB FEATURE DETECTION
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan algoritma ORB (Oriented FAST and Rotated
    BRIEF) yang merupakan alternatif cepat dan gratis untuk SIFT/SURF.
    ORB menggabungkan FAST detector dengan BRIEF descriptor yang dirotasi.

Konsep Utama:
    - FAST (Features from Accelerated Segment Test) untuk deteksi keypoint
    - BRIEF (Binary Robust Independent Elementary Features) untuk descriptor
    - Penambahan orientasi untuk rotation invariance
    - Descriptor binary 256-bit (sangat compact dan cepat)

Keunggulan ORB:
    - 10-100x lebih cepat dari SIFT
    - Free dan tidak ada paten
    - Binary descriptor = matching sangat cepat
    - Cocok untuk real-time applications

Kekurangan ORB:
    - Kurang robust terhadap perubahan skala besar
    - Performa di bawah SIFT untuk beberapa kasus

Aplikasi Dunia Nyata:
    - Real-time tracking
    - Mobile AR applications
    - Robotics (karena computational efficiency)
    - Embedded systems

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Jumlah maksimum fitur yang dipertahankan
N_FEATURES = 500  # Coba ubah: 100, 500, 1000, 2000

# Faktor skala piramida (harus > 1)
# Nilai mendekati 1 = lebih banyak level, lebih lambat tapi lebih baik
SCALE_FACTOR = 1.2  # Coba ubah: 1.1, 1.2, 1.5, 2.0

# Jumlah level piramida
N_LEVELS = 8  # Coba ubah: 4, 8, 12, 16

# Threshold untuk edge detection di FAST
EDGE_THRESHOLD = 31  # Coba ubah: 15, 31, 45

# Ukuran patch untuk orientasi
PATCH_SIZE = 31  # Default, biasanya tidak perlu diubah

# FAST threshold
FAST_THRESHOLD = 20  # Coba ubah: 10, 20, 30

# Score type: HARRIS_SCORE atau FAST_SCORE
USE_HARRIS_SCORE = True  # True = Harris, False = FAST
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def orb_detection(image_path):
    """
    Melakukan ORB Feature Detection pada gambar
    
    Args:
        image_path: Path ke file gambar
        
    Returns:
        Tuple (original, result, keypoints, descriptors, processing_time)
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Tentukan score type
    score_type = cv2.ORB_HARRIS_SCORE if USE_HARRIS_SCORE else cv2.ORB_FAST_SCORE
    
    # Buat ORB detector dengan parameter
    orb = cv2.ORB_create(
        nfeatures=N_FEATURES,
        scaleFactor=SCALE_FACTOR,
        nlevels=N_LEVELS,
        edgeThreshold=EDGE_THRESHOLD,
        patchSize=PATCH_SIZE,
        fastThreshold=FAST_THRESHOLD,
        scoreType=score_type
    )
    
    # Mulai timing
    start_time = time.time()
    
    # Deteksi keypoints dan compute descriptors
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    processing_time = (time.time() - start_time) * 1000  # dalam ms
    
    # Gambar keypoints pada hasil
    result = cv2.drawKeypoints(
        img, keypoints, None, 
        color=(0, 255, 0),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    return img, result, keypoints, descriptors, processing_time

def compare_orb_sift(image_path):
    """
    Membandingkan ORB dengan SIFT
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ORB
    orb = cv2.ORB_create(nfeatures=500)
    start = time.time()
    kp_orb, desc_orb = orb.detectAndCompute(gray, None)
    time_orb = (time.time() - start) * 1000
    
    # SIFT
    sift = cv2.SIFT_create(nfeatures=500)
    start = time.time()
    kp_sift, desc_sift = sift.detectAndCompute(gray, None)
    time_sift = (time.time() - start) * 1000
    
    # Gambar hasil
    result_orb = cv2.drawKeypoints(img.copy(), kp_orb, None, color=(0, 255, 0),
                                    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    result_sift = cv2.drawKeypoints(img.copy(), kp_sift, None, color=(0, 255, 0),
                                     flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Tambah label
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
    cv2.putText(result_orb, f"ORB: {len(kp_orb)} kp, {time_orb:.1f}ms", 
                (10, 30), font, 0.7, (0, 255, 255), 2)
    cv2.putText(result_sift, f"SIFT: {len(kp_sift)} kp, {time_sift:.1f}ms", 
                (10, 30), font, 0.7, (0, 255, 255), 2)
    
    # Resize
    max_width = 500
    h, w = result_orb.shape[:2]
    if w > max_width:
        scale = max_width / w
        result_orb = cv2.resize(result_orb, None, fx=scale, fy=scale)
        result_sift = cv2.resize(result_sift, None, fx=scale, fy=scale)
    
    comparison = np.hstack([result_orb, result_sift])
    
    return comparison, time_orb, time_sift

def compare_scale_factors(image_path):
    """
    Membandingkan berbagai scale factor
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    scale_factors = [1.1, 1.2, 1.5, 2.0]
    results = []
    
    for sf in scale_factors:
        orb = cv2.ORB_create(nfeatures=300, scaleFactor=sf, nlevels=8)
        kp, _ = orb.detectAndCompute(gray, None)
        
        result = cv2.drawKeypoints(img.copy(), kp, None, color=(0, 255, 0),
                                    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        cv2.putText(result, f"SF={sf}: {len(kp)} kp", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        results.append(result)
    
    # Resize
    max_width = 350
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
    print("PRAKTIKUM 4: ORB FEATURE DETECTION")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - N Features: {N_FEATURES}")
    print(f"  - Scale Factor: {SCALE_FACTOR}")
    print(f"  - N Levels: {N_LEVELS}")
    print(f"  - Edge Threshold: {EDGE_THRESHOLD}")
    print(f"  - FAST Threshold: {FAST_THRESHOLD}")
    print(f"  - Score Type: {'HARRIS' if USE_HARRIS_SCORE else 'FAST'}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Gambar untuk diproses
    test_images = ["building.jpg", "box.png", "butterfly.jpg"]
    
    for image_name in test_images:
        image_path = os.path.join(data_dir, image_name)
        
        if not os.path.exists(image_path):
            print(f"⚠ File tidak ditemukan: {image_name}")
            continue
        
        print(f"Memproses: {image_name}")
        print("-" * 40)
        
        try:
            # Deteksi ORB
            original, result, keypoints, descriptors, proc_time = \
                orb_detection(image_path)
            
            print(f"  Jumlah keypoints: {len(keypoints)}")
            if descriptors is not None:
                print(f"  Dimensi descriptor: {descriptors.shape}")
                print(f"  Ukuran per descriptor: {descriptors.shape[1]} bits (binary)")
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
            cv2.putText(result, f"ORB: {len(keypoints)} keypoints", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Gabungkan
            visualization = np.hstack([original, result])
            
            # Simpan hasil
            output_name = f"orb_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Perbandingan ORB vs SIFT
    print("Membuat perbandingan ORB vs SIFT...")
    compare_image = "building.jpg"
    compare_path = os.path.join(data_dir, compare_image)
    
    if os.path.exists(compare_path):
        result = compare_orb_sift(compare_path)
        if result is not None:
            comparison, t_orb, t_sift = result
            output_path = os.path.join(output_dir, "orb_vs_sift_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan ORB vs SIFT disimpan: {output_path}")
            print(f"  Speedup ORB: {t_sift/t_orb:.1f}x lebih cepat dari SIFT")
    
    # Perbandingan scale factor
    print("\nMembuat perbandingan scale factors...")
    if os.path.exists(compare_path):
        comparison = compare_scale_factors(compare_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "orb_scale_factor_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan scale factor disimpan: {output_path}")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah N_FEATURES dari 500 ke 2000
   - Amati: Waktu proses meningkat
   - Pertanyaan: Apakah speedup masih signifikan dibanding SIFT?
   
2. Ubah SCALE_FACTOR dari 1.2 ke 2.0
   - Amati: Jumlah keypoint berkurang
   - Mengapa: Lebih sedikit level piramida dihitung
   
3. Ubah FAST_THRESHOLD dari 20 ke 10
   - Amati: Lebih banyak keypoint terdeteksi
   - Trade-off: Bisa termasuk noise
   
4. Bandingkan descriptor size:
   - ORB: 32 bytes (256 bits, binary)
   - SIFT: 512 bytes (128 float)
   - ORB 16x lebih compact!

5. Perhatikan output "orb_vs_sift_comparison":
   - ORB jauh lebih cepat
   - Kualitas keypoint cukup baik untuk kebanyakan aplikasi
   
6. USE_HARRIS_SCORE:
   - True: Menggunakan Harris response (lebih akurat)
   - False: Menggunakan FAST response (lebih cepat)
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
