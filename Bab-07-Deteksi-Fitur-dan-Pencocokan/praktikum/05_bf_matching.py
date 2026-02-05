"""
=============================================================================
PRAKTIKUM 5: BRUTE-FORCE FEATURE MATCHING
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan Brute-Force Feature Matching untuk
    mencocokkan fitur antara dua gambar. Brute-Force membandingkan
    setiap descriptor dari gambar pertama dengan semua descriptor di
    gambar kedua.

Konsep Utama:
    - Brute-Force: mencari nearest neighbor dengan exhaustive search
    - Distance metric: L2 untuk SIFT/SURF, Hamming untuk ORB/BRIEF
    - Ratio test (Lowe's test): memfilter match yang ambiguous

Ratio Test:
    - Untuk setiap keypoint, cari 2 nearest neighbors
    - Jika distance_1 / distance_2 < threshold → good match
    - Threshold biasanya 0.75 (dari paper Lowe)

Aplikasi Dunia Nyata:
    - Object recognition dalam scene
    - Image stitching
    - Planar object tracking
    - Document scanning dan alignment

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Algoritma feature detector yang digunakan
DETECTOR_TYPE = "ORB"  # Coba ubah: "ORB", "SIFT", "AKAZE"

# Jumlah fitur untuk dideteksi
N_FEATURES = 500  # Coba ubah: 200, 500, 1000

# Ratio threshold untuk Lowe's ratio test
# Nilai lebih kecil = lebih ketat (lebih sedikit match)
# Nilai lebih besar = lebih longgar (lebih banyak match, termasuk false match)
RATIO_THRESHOLD = 0.75  # Coba ubah: 0.5, 0.7, 0.75, 0.8, 0.9

# Jumlah good matches yang ditampilkan
MAX_MATCHES_DISPLAY = 50  # Coba ubah: 20, 50, 100

# Cross check (untuk brute-force tanpa ratio test)
CROSS_CHECK = False  # Coba ubah: True, False

# Warna garis untuk matches
MATCH_COLOR = (0, 255, 0)  # Hijau untuk good matches
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def create_detector(detector_type, n_features):
    """
    Membuat feature detector sesuai tipe yang dipilih
    """
    if detector_type == "ORB":
        return cv2.ORB_create(nfeatures=n_features)
    elif detector_type == "SIFT":
        return cv2.SIFT_create(nfeatures=n_features)
    elif detector_type == "AKAZE":
        return cv2.AKAZE_create()
    else:
        raise ValueError(f"Detector tidak dikenal: {detector_type}")

def get_norm_type(detector_type):
    """
    Menentukan norm type untuk matcher berdasarkan detector
    """
    if detector_type in ["ORB", "BRISK", "AKAZE"]:
        return cv2.NORM_HAMMING
    else:  # SIFT, SURF
        return cv2.NORM_L2

def bf_matching(img1_path, img2_path):
    """
    Melakukan Brute-Force Feature Matching antara dua gambar
    
    Args:
        img1_path: Path ke gambar pertama (query/template)
        img2_path: Path ke gambar kedua (train/scene)
        
    Returns:
        Tuple (result_image, good_matches, total_matches, processing_time)
    """
    # Baca gambar
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        raise FileNotFoundError("Gambar tidak ditemukan")
    
    # Konversi ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Buat detector
    detector = create_detector(DETECTOR_TYPE, N_FEATURES)
    
    # Mulai timing
    start_time = time.time()
    
    # Deteksi keypoints dan compute descriptors
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    if desc1 is None or desc2 is None:
        raise ValueError("Tidak ada descriptor yang ditemukan")
    
    # Tentukan norm type
    norm_type = get_norm_type(DETECTOR_TYPE)
    
    # Buat Brute-Force Matcher
    # knnMatch memerlukan k=2 untuk ratio test
    bf = cv2.BFMatcher(norm_type, crossCheck=False)
    
    # Lakukan matching dengan k=2 nearest neighbors
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    # Apply ratio test (Lowe's test)
    good_matches = []
    for match_pair in matches:
        if len(match_pair) == 2:
            m, n = match_pair
            if m.distance < RATIO_THRESHOLD * n.distance:
                good_matches.append(m)
    
    processing_time = (time.time() - start_time) * 1000
    
    # Urutkan berdasarkan distance
    good_matches = sorted(good_matches, key=lambda x: x.distance)
    
    # Gambar hasil matching
    result = cv2.drawMatches(
        img1, kp1, img2, kp2,
        good_matches[:MAX_MATCHES_DISPLAY],
        None,
        matchColor=MATCH_COLOR,
        singlePointColor=(255, 0, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return result, len(good_matches), len(matches), processing_time, kp1, kp2

def compare_ratio_thresholds(img1_path, img2_path):
    """
    Membandingkan berbagai ratio threshold
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        return None
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    detector = create_detector(DETECTOR_TYPE, N_FEATURES)
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    if desc1 is None or desc2 is None:
        return None
    
    norm_type = get_norm_type(DETECTOR_TYPE)
    bf = cv2.BFMatcher(norm_type, crossCheck=False)
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    thresholds = [0.5, 0.7, 0.8, 0.9]
    results = []
    
    for thresh in thresholds:
        good = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < thresh * n.distance:
                    good.append(m)
        
        good = sorted(good, key=lambda x: x.distance)[:30]
        
        result = cv2.drawMatches(
            img1, kp1, img2, kp2, good, None,
            matchColor=(0, 255, 0),
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        cv2.putText(result, f"Ratio={thresh}: {len(good)} matches", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        results.append(result)
    
    # Resize
    max_width = 600
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
    print("PRAKTIKUM 5: BRUTE-FORCE FEATURE MATCHING")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - Detector Type: {DETECTOR_TYPE}")
    print(f"  - N Features: {N_FEATURES}")
    print(f"  - Ratio Threshold: {RATIO_THRESHOLD}")
    print(f"  - Max Matches Display: {MAX_MATCHES_DISPLAY}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Pasangan gambar untuk matching
    image_pairs = [
        ("box.png", "box_in_scene.png"),
        ("graf1.png", "graf3.png"),
        ("left01.jpg", "right01.jpg"),
    ]
    
    for img1_name, img2_name in image_pairs:
        img1_path = os.path.join(data_dir, img1_name)
        img2_path = os.path.join(data_dir, img2_name)
        
        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            print(f"⚠ File tidak ditemukan: {img1_name} atau {img2_name}")
            continue
        
        print(f"Matching: {img1_name} ↔ {img2_name}")
        print("-" * 40)
        
        try:
            # Lakukan matching
            result, good_count, total_count, proc_time, kp1, kp2 = \
                bf_matching(img1_path, img2_path)
            
            print(f"  Keypoints gambar 1: {len(kp1)}")
            print(f"  Keypoints gambar 2: {len(kp2)}")
            print(f"  Total matches: {total_count}")
            print(f"  Good matches (setelah ratio test): {good_count}")
            print(f"  Waktu proses: {proc_time:.2f} ms")
            
            # Simpan hasil
            pair_name = f"{os.path.splitext(img1_name)[0]}_{os.path.splitext(img2_name)[0]}"
            output_name = f"bf_match_{pair_name}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, result)
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Perbandingan ratio threshold
    print("Membuat perbandingan ratio thresholds...")
    test_pair = ("box.png", "box_in_scene.png")
    img1_path = os.path.join(data_dir, test_pair[0])
    img2_path = os.path.join(data_dir, test_pair[1])
    
    if os.path.exists(img1_path) and os.path.exists(img2_path):
        comparison = compare_ratio_thresholds(img1_path, img2_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "bf_ratio_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan ratio disimpan: {output_path}")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah RATIO_THRESHOLD dari 0.75 ke 0.5
   - Amati: Lebih sedikit matches
   - Mengapa: Filter lebih ketat, hanya match yang sangat distinct
   
2. Ubah RATIO_THRESHOLD dari 0.75 ke 0.9
   - Amati: Lebih banyak matches, termasuk false matches
   - Mengapa: Filter lebih longgar
   
3. Ubah DETECTOR_TYPE dari "ORB" ke "SIFT"
   - Amati: Perbedaan jumlah dan kualitas matches
   - Perhatikan: Waktu proses SIFT lebih lama
   
4. Coba dengan gambar berbeda:
   - box.png ↔ box_in_scene.png: Objek dalam scene
   - graf1.png ↔ graf3.png: Viewpoint change
   - left01.jpg ↔ right01.jpg: Stereo pair
   
5. Analisis hasil matching:
   - Apakah garis match menghubungkan titik yang benar?
   - Ada berapa false matches yang terlihat?
   - Bagaimana ratio test membantu filtering?
   
6. Cross-Check vs Ratio Test:
   - Set CROSS_CHECK = True dan RATIO_THRESHOLD = 1.0
   - Bandingkan hasil dengan ratio test biasa
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
