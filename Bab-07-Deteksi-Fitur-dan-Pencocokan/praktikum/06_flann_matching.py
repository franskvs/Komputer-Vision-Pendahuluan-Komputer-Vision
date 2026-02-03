"""
=============================================================================
PRAKTIKUM 6: FLANN FEATURE MATCHING
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan FLANN (Fast Library for Approximate
    Nearest Neighbors) untuk feature matching yang lebih efisien pada
    dataset besar. FLANN menggunakan algoritma approximate search yang
    jauh lebih cepat dari brute-force.

Konsep Utama:
    - FLANN menggunakan multiple randomized kd-trees atau LSH
    - Approximate nearest neighbor: tidak selalu menemukan exact nearest
    - Trade-off: kecepatan vs akurasi
    - Sangat efektif untuk dataset dengan ribuan keypoints

Kapan Menggunakan FLANN vs Brute-Force:
    - < 1000 keypoints: Brute-Force cukup cepat
    - > 1000 keypoints: FLANN lebih efisien
    - Real-time: FLANN lebih recommended

Konfigurasi FLANN:
    - KD-Tree: untuk floating-point descriptors (SIFT, SURF)
    - LSH: untuk binary descriptors (ORB, BRIEF, BRISK)

Aplikasi Dunia Nyata:
    - Large-scale image retrieval
    - Real-time tracking dengan banyak fitur
    - Visual vocabulary construction
    - Object detection dalam database besar

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Algoritma feature detector yang digunakan
DETECTOR_TYPE = "SIFT"  # Coba ubah: "ORB", "SIFT"

# Jumlah fitur untuk dideteksi
N_FEATURES = 1000  # Coba ubah: 500, 1000, 2000, 5000

# Ratio threshold untuk Lowe's ratio test
RATIO_THRESHOLD = 0.7  # Coba ubah: 0.5, 0.7, 0.8

# === FLANN Parameters untuk KD-Tree (SIFT/SURF) ===
FLANN_TREES = 5  # Jumlah KD-trees. Coba ubah: 1, 5, 10, 20
FLANN_CHECKS = 50  # Jumlah checks saat search. Coba ubah: 32, 50, 100, 200

# === FLANN Parameters untuk LSH (ORB/BRIEF) ===
LSH_TABLE_NUMBER = 6  # Jumlah hash tables. Coba ubah: 6, 12, 20
LSH_KEY_SIZE = 12  # Key size in bits. Coba ubah: 12, 20
LSH_MULTI_PROBE_LEVEL = 1  # Multi-probe level. Coba ubah: 1, 2

# Jumlah good matches yang ditampilkan
MAX_MATCHES_DISPLAY = 50
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def create_detector(detector_type, n_features):
    """Membuat feature detector sesuai tipe"""
    if detector_type == "ORB":
        return cv2.ORB_create(nfeatures=n_features)
    elif detector_type == "SIFT":
        return cv2.SIFT_create(nfeatures=n_features)
    else:
        raise ValueError(f"Detector tidak dikenal: {detector_type}")

def get_flann_matcher(detector_type):
    """
    Membuat FLANN matcher dengan konfigurasi sesuai detector type
    """
    if detector_type == "SIFT":
        # FLANN parameters untuk float descriptors (SIFT, SURF)
        index_params = dict(
            algorithm=1,  # FLANN_INDEX_KDTREE
            trees=FLANN_TREES
        )
    else:  # ORB, BRIEF, BRISK - binary descriptors
        # FLANN parameters untuk binary descriptors
        index_params = dict(
            algorithm=6,  # FLANN_INDEX_LSH
            table_number=LSH_TABLE_NUMBER,
            key_size=LSH_KEY_SIZE,
            multi_probe_level=LSH_MULTI_PROBE_LEVEL
        )
    
    search_params = dict(checks=FLANN_CHECKS)
    
    return cv2.FlannBasedMatcher(index_params, search_params)

def flann_matching(img1_path, img2_path):
    """
    Melakukan FLANN Feature Matching antara dua gambar
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
    
    detection_time = (time.time() - start_time) * 1000
    
    if desc1 is None or desc2 is None:
        raise ValueError("Tidak ada descriptor yang ditemukan")
    
    # Pastikan descriptor dalam format yang benar untuk FLANN
    if DETECTOR_TYPE == "ORB":
        # ORB descriptor perlu dikonversi untuk FLANN
        desc1 = desc1.astype(np.uint8)
        desc2 = desc2.astype(np.uint8)
    else:
        desc1 = desc1.astype(np.float32)
        desc2 = desc2.astype(np.float32)
    
    # Buat FLANN Matcher
    flann = get_flann_matcher(DETECTOR_TYPE)
    
    # Mulai timing matching
    start_time = time.time()
    
    # Lakukan matching
    matches = flann.knnMatch(desc1, desc2, k=2)
    
    matching_time = (time.time() - start_time) * 1000
    
    # Apply ratio test
    good_matches = []
    for match_pair in matches:
        if len(match_pair) == 2:
            m, n = match_pair
            if m.distance < RATIO_THRESHOLD * n.distance:
                good_matches.append(m)
    
    # Urutkan berdasarkan distance
    good_matches = sorted(good_matches, key=lambda x: x.distance)
    
    # Gambar hasil matching
    result = cv2.drawMatches(
        img1, kp1, img2, kp2,
        good_matches[:MAX_MATCHES_DISPLAY],
        None,
        matchColor=(0, 255, 0),
        singlePointColor=(255, 0, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return result, len(good_matches), len(matches), detection_time, matching_time, kp1, kp2

def compare_bf_vs_flann(img1_path, img2_path):
    """
    Membandingkan Brute-Force dengan FLANN
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        return None, None
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Gunakan SIFT untuk perbandingan yang fair
    sift = cv2.SIFT_create(nfeatures=N_FEATURES)
    kp1, desc1 = sift.detectAndCompute(gray1, None)
    kp2, desc2 = sift.detectAndCompute(gray2, None)
    
    if desc1 is None or desc2 is None:
        return None, None
    
    # === Brute-Force ===
    bf = cv2.BFMatcher(cv2.NORM_L2)
    start = time.time()
    matches_bf = bf.knnMatch(desc1, desc2, k=2)
    time_bf = (time.time() - start) * 1000
    
    good_bf = []
    for m_pair in matches_bf:
        if len(m_pair) == 2 and m_pair[0].distance < 0.7 * m_pair[1].distance:
            good_bf.append(m_pair[0])
    
    # === FLANN ===
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    start = time.time()
    matches_flann = flann.knnMatch(desc1, desc2, k=2)
    time_flann = (time.time() - start) * 1000
    
    good_flann = []
    for m_pair in matches_flann:
        if len(m_pair) == 2 and m_pair[0].distance < 0.7 * m_pair[1].distance:
            good_flann.append(m_pair[0])
    
    # Gambar hasil
    result_bf = cv2.drawMatches(
        img1, kp1, img2, kp2, good_bf[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    result_flann = cv2.drawMatches(
        img1, kp1, img2, kp2, good_flann[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    # Tambah label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(result_bf, f"BF: {len(good_bf)} matches, {time_bf:.1f}ms", 
                (10, 30), font, 0.8, (0, 255, 255), 2)
    cv2.putText(result_flann, f"FLANN: {len(good_flann)} matches, {time_flann:.1f}ms", 
                (10, 30), font, 0.8, (0, 255, 255), 2)
    
    # Resize
    max_width = 700
    h, w = result_bf.shape[:2]
    if w > max_width:
        scale = max_width / w
        result_bf = cv2.resize(result_bf, None, fx=scale, fy=scale)
        result_flann = cv2.resize(result_flann, None, fx=scale, fy=scale)
    
    comparison = np.vstack([result_bf, result_flann])
    
    timing = {'bf': time_bf, 'flann': time_flann, 
              'bf_matches': len(good_bf), 'flann_matches': len(good_flann)}
    
    return comparison, timing

def main():
    print("=" * 70)
    print("PRAKTIKUM 6: FLANN FEATURE MATCHING")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - Detector Type: {DETECTOR_TYPE}")
    print(f"  - N Features: {N_FEATURES}")
    print(f"  - Ratio Threshold: {RATIO_THRESHOLD}")
    if DETECTOR_TYPE == "SIFT":
        print(f"  - FLANN Trees: {FLANN_TREES}")
        print(f"  - FLANN Checks: {FLANN_CHECKS}")
    else:
        print(f"  - LSH Tables: {LSH_TABLE_NUMBER}")
        print(f"  - LSH Key Size: {LSH_KEY_SIZE}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(os.path.dirname(script_dir), "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Pasangan gambar untuk matching
    image_pairs = [
        ("box.png", "box_in_scene.png"),
        ("graf1.png", "graf3.png"),
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
            result, good_count, total_count, det_time, match_time, kp1, kp2 = \
                flann_matching(img1_path, img2_path)
            
            print(f"  Keypoints gambar 1: {len(kp1)}")
            print(f"  Keypoints gambar 2: {len(kp2)}")
            print(f"  Total matches: {total_count}")
            print(f"  Good matches: {good_count}")
            print(f"  Waktu deteksi: {det_time:.2f} ms")
            print(f"  Waktu matching: {match_time:.2f} ms")
            
            # Simpan hasil
            pair_name = f"{os.path.splitext(img1_name)[0]}_{os.path.splitext(img2_name)[0]}"
            output_name = f"flann_match_{pair_name}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, result)
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Perbandingan BF vs FLANN
    print("Membuat perbandingan Brute-Force vs FLANN...")
    test_pair = ("box.png", "box_in_scene.png")
    img1_path = os.path.join(data_dir, test_pair[0])
    img2_path = os.path.join(data_dir, test_pair[1])
    
    if os.path.exists(img1_path) and os.path.exists(img2_path):
        comparison, timing = compare_bf_vs_flann(img1_path, img2_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "bf_vs_flann_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan disimpan: {output_path}")
            print(f"  BF: {timing['bf']:.1f}ms, {timing['bf_matches']} matches")
            print(f"  FLANN: {timing['flann']:.1f}ms, {timing['flann_matches']} matches")
            if timing['bf'] > 0:
                speedup = timing['bf'] / timing['flann']
                print(f"  FLANN {speedup:.2f}x lebih cepat dari BF")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah N_FEATURES dari 1000 ke 5000
   - Amati: Speedup FLANN semakin signifikan
   - Mengapa: FLANN O(log n) vs BF O(n)
   
2. Ubah FLANN_TREES dari 5 ke 1
   - Amati: Matching lebih cepat, tapi akurasi berkurang
   - Trade-off: speed vs accuracy
   
3. Ubah FLANN_CHECKS dari 50 ke 200
   - Amati: Matching lebih akurat, tapi lebih lambat
   - Mengapa: Lebih banyak node yang diperiksa
   
4. Bandingkan DETECTOR_TYPE "SIFT" vs "ORB":
   - SIFT menggunakan KD-Tree (float descriptor)
   - ORB menggunakan LSH (binary descriptor)
   - Perhatikan perbedaan konfigurasi FLANN
   
5. Coba dengan gambar besar:
   - Dengan ribuan keypoints, FLANN jauh lebih cepat
   - BF menjadi sangat lambat
   
6. Analisis akurasi:
   - Apakah FLANN melewatkan beberapa good matches?
   - Bagaimana menentukan parameter optimal?
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
