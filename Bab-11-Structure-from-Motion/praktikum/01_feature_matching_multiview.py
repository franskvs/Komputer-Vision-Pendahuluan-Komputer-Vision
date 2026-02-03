#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 01_feature_matching_multiview.py

Deskripsi:
    Program ini mendemonstrasikan Feature Matching Multi-View untuk
    Structure from Motion (SfM). Fitur matching adalah langkah pertama
    dalam pipeline SfM yang mencocokkan titik-titik kunci antar gambar
    yang diambil dari sudut pandang berbeda.

Tujuan:
    1. Memahami cara mendeteksi fitur (keypoints) pada gambar
    2. Memahami cara menghitung deskriptor fitur
    3. Memahami cara mencocokkan fitur antar gambar
    4. Memahami Lowe's ratio test untuk filtering matches

Aplikasi Dunia Nyata:
    - Fotogrametri (pemetaan udara dengan drone)
    - Pembuatan model 3D dari foto
    - Visual effects dalam film (camera tracking)
    - Augmented Reality

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Pilih jenis detector fitur
# Opsi: 'SIFT', 'ORB', 'AKAZE', 'BRISK'
# SIFT: Lebih akurat tapi lebih lambat
# ORB: Cepat tapi kurang akurat di rotasi besar
# AKAZE: Balance antara kecepatan dan akurasi
DETECTOR_TYPE = 'SIFT'

# Jumlah maksimum fitur yang dideteksi
# Semakin banyak fitur = lebih banyak potential matches, tapi lebih lambat
# Range yang disarankan: 500 - 5000
MAX_FEATURES = 2000

# Lowe's ratio threshold untuk filtering matches
# Nilai lebih kecil = lebih ketat (lebih sedikit matches tapi lebih akurat)
# Nilai lebih besar = lebih longgar (lebih banyak matches tapi mungkin ada false matches)
# Range yang disarankan: 0.5 - 0.8
RATIO_THRESHOLD = 0.75

# Metode matching
# 'BF': Brute-Force (cocok untuk ORB, BRIEF)
# 'FLANN': Fast Library for Approximate Nearest Neighbors (cocok untuk SIFT, SURF)
MATCHER_TYPE = 'FLANN'

# Tampilkan top N matches untuk visualisasi
# Terlalu banyak akan membuat visualisasi tidak jelas
TOP_N_MATCHES = 100

# ============================================================================
# FUNGSI UTAMA
# ============================================================================

def create_feature_detector(detector_type, max_features):
    """
    Membuat objek feature detector berdasarkan jenis yang dipilih.
    
    Parameters:
        detector_type: Jenis detector ('SIFT', 'ORB', 'AKAZE', 'BRISK')
        max_features: Jumlah maksimum fitur
        
    Returns:
        detector: Objek feature detector
    """
    if detector_type == 'SIFT':
        # SIFT (Scale-Invariant Feature Transform)
        # Baik untuk gambar dengan perubahan skala dan rotasi
        detector = cv2.SIFT_create(nfeatures=max_features)
    elif detector_type == 'ORB':
        # ORB (Oriented FAST and Rotated BRIEF)
        # Cepat dan gratis (tidak ada patent)
        detector = cv2.ORB_create(nfeatures=max_features)
    elif detector_type == 'AKAZE':
        # AKAZE (Accelerated-KAZE)
        # Bagus untuk edge dan blob detection
        detector = cv2.AKAZE_create()
    elif detector_type == 'BRISK':
        # BRISK (Binary Robust Invariant Scalable Keypoints)
        # Cepat dengan binary descriptor
        detector = cv2.BRISK_create()
    else:
        raise ValueError(f"Detector tidak dikenal: {detector_type}")
    
    return detector


def create_matcher(matcher_type, detector_type):
    """
    Membuat objek matcher berdasarkan jenis detector.
    
    Parameters:
        matcher_type: 'BF' atau 'FLANN'
        detector_type: Jenis detector yang digunakan
        
    Returns:
        matcher: Objek matcher
    """
    if matcher_type == 'BF':
        # Brute-Force Matcher
        if detector_type in ['ORB', 'BRISK', 'AKAZE']:
            # Untuk binary descriptors, gunakan Hamming distance
            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:
            # Untuk float descriptors (SIFT, SURF), gunakan L2 distance
            matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    else:
        # FLANN Matcher (lebih cepat untuk dataset besar)
        if detector_type in ['ORB', 'BRISK', 'AKAZE']:
            # Index params untuk binary descriptors
            FLANN_INDEX_LSH = 6
            index_params = dict(algorithm=FLANN_INDEX_LSH,
                              table_number=6,
                              key_size=12,
                              multi_probe_level=1)
        else:
            # Index params untuk float descriptors
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
    
    return matcher


def detect_and_compute(image, detector):
    """
    Mendeteksi keypoints dan menghitung descriptors.
    
    Parameters:
        image: Gambar input (BGR atau grayscale)
        detector: Objek feature detector
        
    Returns:
        keypoints: List keypoints yang terdeteksi
        descriptors: Array descriptors
    """
    # Konversi ke grayscale jika perlu
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Deteksi keypoints dan hitung descriptors
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def match_features(desc1, desc2, matcher, ratio_threshold):
    """
    Mencocokkan features antara dua gambar menggunakan Lowe's ratio test.
    
    Lowe's ratio test: Untuk setiap fitur, bandingkan jarak ke match terbaik
    dengan jarak ke match kedua terbaik. Jika rasionya < threshold,
    match dianggap baik.
    
    Parameters:
        desc1, desc2: Descriptors dari dua gambar
        matcher: Objek matcher
        ratio_threshold: Threshold untuk ratio test
        
    Returns:
        good_matches: List matches yang lolos ratio test
    """
    if desc1 is None or desc2 is None:
        return []
    
    # KNN matching dengan k=2
    # Untuk setiap descriptor di desc1, cari 2 nearest neighbors di desc2
    matches = matcher.knnMatch(desc1, desc2, k=2)
    
    # Apply Lowe's ratio test
    good_matches = []
    for match_pair in matches:
        if len(match_pair) == 2:
            m, n = match_pair
            # Jika match terbaik jauh lebih baik dari match kedua, simpan
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
    
    return good_matches


def visualize_matches(img1, kp1, img2, kp2, matches, output_path, title):
    """
    Memvisualisasikan hasil feature matching.
    """
    # Gambar matches
    img_matches = cv2.drawMatches(
        img1, kp1, img2, kp2, matches,
        None,
        matchColor=(0, 255, 0),      # Warna garis match (hijau)
        singlePointColor=(255, 0, 0), # Warna keypoint tanpa match (biru)
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    # Konversi BGR ke RGB untuk matplotlib
    img_matches_rgb = cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(img_matches_rgb)
    plt.title(f'{title}\nJumlah Good Matches: {len(matches)}', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def visualize_keypoints(image, keypoints, output_path, title):
    """
    Memvisualisasikan keypoints yang terdeteksi.
    """
    img_kp = cv2.drawKeypoints(
        image, keypoints, None,
        color=(0, 255, 0),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    img_kp_rgb = cv2.cvtColor(img_kp, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(img_kp_rgb)
    plt.title(f'{title}\nJumlah Keypoints: {len(keypoints)}', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("FEATURE MATCHING MULTI-VIEW UNTUK STRUCTURE FROM MOTION")
    print("="*70)
    print(f"\nKonfigurasi:")
    print(f"  - Detector: {DETECTOR_TYPE}")
    print(f"  - Max Features: {MAX_FEATURES}")
    print(f"  - Ratio Threshold: {RATIO_THRESHOLD}")
    print(f"  - Matcher: {MATCHER_TYPE}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    data_dir = script_dir.parent / "data" / "images"
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Load gambar - gunakan gambar sampel atau buat dummy
    img1_path = data_dir / "building1.jpg"
    img2_path = data_dir / "building2.jpg"
    
    # Jika gambar tidak ada, gunakan gambar sample atau buat dummy
    if not img1_path.exists() or not img2_path.exists():
        print("Gambar sampel tidak ditemukan. Membuat gambar dummy untuk demo...")
        
        # Buat gambar dummy dengan fitur yang bisa di-match
        img1 = np.zeros((480, 640, 3), dtype=np.uint8)
        img2 = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Tambahkan pattern yang bisa dideteksi
        for i in range(5):
            for j in range(5):
                x1, y1 = 50 + i*120, 50 + j*80
                cv2.circle(img1, (x1, y1), 20, (255, 255, 255), -1)
                cv2.rectangle(img1, (x1+30, y1-20), (x1+70, y1+20), (200, 200, 200), -1)
                
                # Gambar 2 dengan sedikit offset (simulasi sudut berbeda)
                x2, y2 = x1 + 20, y1 + 10
                cv2.circle(img2, (x2, y2), 20, (255, 255, 255), -1)
                cv2.rectangle(img2, (x2+30, y2-20), (x2+70, y2+20), (200, 200, 200), -1)
        
        # Tambahkan noise untuk realisme
        noise1 = np.random.randint(0, 30, img1.shape, dtype=np.uint8)
        noise2 = np.random.randint(0, 30, img2.shape, dtype=np.uint8)
        img1 = cv2.add(img1, noise1)
        img2 = cv2.add(img2, noise2)
        
        print("Gambar dummy dibuat.")
    else:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
        print(f"Gambar loaded: {img1_path.name}, {img2_path.name}")
    
    if img1 is None or img2 is None:
        print("Error: Tidak dapat membaca gambar!")
        return
    
    print(f"\nUkuran gambar 1: {img1.shape}")
    print(f"Ukuran gambar 2: {img2.shape}")
    
    # Step 1: Buat feature detector
    print("\n[1] Membuat feature detector...")
    detector = create_feature_detector(DETECTOR_TYPE, MAX_FEATURES)
    
    # Step 2: Deteksi keypoints dan hitung descriptors
    print("[2] Mendeteksi keypoints...")
    kp1, desc1 = detect_and_compute(img1, detector)
    kp2, desc2 = detect_and_compute(img2, detector)
    
    print(f"    Gambar 1: {len(kp1)} keypoints terdeteksi")
    print(f"    Gambar 2: {len(kp2)} keypoints terdeteksi")
    
    # Visualisasi keypoints
    print("[3] Memvisualisasikan keypoints...")
    visualize_keypoints(img1, kp1, 
                       output_dir / f"01_keypoints_img1_{DETECTOR_TYPE}.png",
                       f"Keypoints Gambar 1 ({DETECTOR_TYPE})")
    visualize_keypoints(img2, kp2,
                       output_dir / f"01_keypoints_img2_{DETECTOR_TYPE}.png", 
                       f"Keypoints Gambar 2 ({DETECTOR_TYPE})")
    
    # Step 3: Buat matcher
    print("[4] Membuat feature matcher...")
    matcher = create_matcher(MATCHER_TYPE, DETECTOR_TYPE)
    
    # Step 4: Match features
    print("[5] Mencocokkan features...")
    good_matches = match_features(desc1, desc2, matcher, RATIO_THRESHOLD)
    print(f"    Jumlah good matches: {len(good_matches)}")
    
    # Sort matches by distance
    good_matches = sorted(good_matches, key=lambda x: x.distance)
    
    # Step 5: Visualisasi matches
    print("[6] Memvisualisasikan matches...")
    visualize_matches(
        img1, kp1, img2, kp2,
        good_matches[:TOP_N_MATCHES],
        output_dir / f"01_feature_matches_{DETECTOR_TYPE}.png",
        f"Feature Matching dengan {DETECTOR_TYPE}"
    )
    
    # Statistik
    print("\n" + "="*50)
    print("STATISTIK HASIL")
    print("="*50)
    print(f"Detector: {DETECTOR_TYPE}")
    print(f"Keypoints Gambar 1: {len(kp1)}")
    print(f"Keypoints Gambar 2: {len(kp2)}")
    print(f"Total Matches: {len(good_matches)}")
    print(f"Match Rate: {len(good_matches)/min(len(kp1), len(kp2))*100:.1f}%")
    
    if good_matches:
        distances = [m.distance for m in good_matches]
        print(f"Jarak Match Min: {min(distances):.2f}")
        print(f"Jarak Match Max: {max(distances):.2f}")
        print(f"Jarak Match Rata-rata: {np.mean(distances):.2f}")
    
    print("\n✓ Program selesai!")
    print(f"Output disimpan di: {output_dir}")


if __name__ == "__main__":
    main()
