"""
=============================================================================
PRAKTIKUM 7: HOMOGRAPHY ESTIMATION DENGAN RANSAC
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan estimasi homography menggunakan RANSAC
    (Random Sample Consensus) untuk menemukan transformasi perspektif
    antara dua gambar berdasarkan feature matches.

Konsep Utama:
    - Homography: Transformasi proyektif antara dua planar surfaces
    - RANSAC: Algoritma robust estimation yang menangani outliers
    - Inliers vs Outliers: Match yang benar vs match yang salah

Proses RANSAC:
    1. Pilih 4 match secara random (minimum untuk homography)
    2. Hitung homography dari 4 titik tersebut
    3. Hitung error untuk semua match
    4. Hitung jumlah inlier (error < threshold)
    5. Ulangi dan simpan model dengan inlier terbanyak

Aplikasi Dunia Nyata:
    - Image stitching (panorama)
    - Augmented Reality (AR markers)
    - Document scanning dan rectification
    - Visual odometry untuk robot/drone

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Algoritma feature detector
DETECTOR_TYPE = "ORB"  # Coba ubah: "ORB", "SIFT"

# Jumlah fitur
N_FEATURES = 1000  # Coba ubah: 500, 1000, 2000

# Ratio threshold untuk matching
RATIO_THRESHOLD = 0.75  # Coba ubah: 0.5, 0.7, 0.75, 0.8

# === RANSAC Parameters ===
# Threshold untuk menentukan inlier (dalam pixel)
# Nilai kecil = lebih ketat, hanya match sangat akurat yang jadi inlier
RANSAC_REPROJ_THRESHOLD = 5.0  # Coba ubah: 3.0, 5.0, 10.0

# Minimum match yang diperlukan untuk homography
MIN_MATCH_COUNT = 10  # Coba ubah: 4, 10, 20

# Warna visualisasi
INLIER_COLOR = (0, 255, 0)    # Hijau untuk inlier
OUTLIER_COLOR = (0, 0, 255)   # Merah untuk outlier
BORDER_COLOR = (255, 0, 0)    # Biru untuk border objek terdeteksi
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def create_detector(detector_type, n_features):
    """Membuat feature detector"""
    if detector_type == "ORB":
        return cv2.ORB_create(nfeatures=n_features)
    elif detector_type == "SIFT":
        return cv2.SIFT_create(nfeatures=n_features)
    else:
        raise ValueError(f"Detector tidak dikenal: {detector_type}")

def get_matcher(detector_type):
    """Membuat matcher sesuai detector type"""
    if detector_type == "ORB":
        return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    else:
        return cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

def homography_ransac(img1_path, img2_path):
    """
    Mengestimasi homography dengan RANSAC
    
    Args:
        img1_path: Path ke gambar template/objek
        img2_path: Path ke gambar scene
        
    Returns:
        Dict berisi hasil dan statistik
    """
    # Baca gambar
    img1 = cv2.imread(img1_path)  # Template/Object
    img2 = cv2.imread(img2_path)  # Scene
    
    if img1 is None or img2 is None:
        raise FileNotFoundError("Gambar tidak ditemukan")
    
    # Konversi ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Buat detector dan matcher
    detector = create_detector(DETECTOR_TYPE, N_FEATURES)
    matcher = get_matcher(DETECTOR_TYPE)
    
    # Mulai timing
    start_time = time.time()
    
    # Deteksi keypoints dan descriptors
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    if desc1 is None or desc2 is None:
        raise ValueError("Tidak ada descriptor yang ditemukan")
    
    # Feature matching dengan ratio test
    matches = matcher.knnMatch(desc1, desc2, k=2)
    
    good_matches = []
    for m_pair in matches:
        if len(m_pair) == 2:
            m, n = m_pair
            if m.distance < RATIO_THRESHOLD * n.distance:
                good_matches.append(m)
    
    result = {
        'kp1': len(kp1),
        'kp2': len(kp2),
        'good_matches': len(good_matches),
        'homography': None,
        'inliers': 0,
        'outliers': 0,
        'success': False
    }
    
    # Perlu minimal MIN_MATCH_COUNT matches untuk homography
    if len(good_matches) < MIN_MATCH_COUNT:
        print(f"  Tidak cukup matches ({len(good_matches)} < {MIN_MATCH_COUNT})")
        result['image'] = np.hstack([img1, img2])
        return result
    
    # Ekstrak lokasi keypoint
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Estimasi homography dengan RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, RANSAC_REPROJ_THRESHOLD)
    
    processing_time = (time.time() - start_time) * 1000
    
    if H is None:
        print("  Homography tidak ditemukan")
        result['image'] = np.hstack([img1, img2])
        return result
    
    # Hitung inliers dan outliers
    matches_mask = mask.ravel().tolist()
    inliers = sum(matches_mask)
    outliers = len(matches_mask) - inliers
    
    result['homography'] = H
    result['inliers'] = inliers
    result['outliers'] = outliers
    result['success'] = True
    result['time'] = processing_time
    
    # === Visualisasi ===
    
    # Gambar border objek yang terdeteksi di scene
    h1, w1 = img1.shape[:2]
    corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners, H)
    
    img2_with_border = img2.copy()
    cv2.polylines(img2_with_border, [np.int32(transformed_corners)], True, 
                  BORDER_COLOR, 3, cv2.LINE_AA)
    
    # Gambar matches dengan warna berbeda untuk inlier/outlier
    draw_params = dict(
        matchColor=None,  # Akan digambar manual
        singlePointColor=None,
        matchesMask=None,  # Gambar semua
        flags=2
    )
    
    result_img = cv2.drawMatches(img1, kp1, img2_with_border, kp2, 
                                  good_matches, None, **draw_params)
    
    # Gambar ulang dengan warna inlier/outlier
    h_offset = w1
    for i, m in enumerate(good_matches):
        pt1 = tuple(map(int, kp1[m.queryIdx].pt))
        pt2 = tuple(map(int, (kp2[m.trainIdx].pt[0] + h_offset, kp2[m.trainIdx].pt[1])))
        
        color = INLIER_COLOR if matches_mask[i] else OUTLIER_COLOR
        cv2.line(result_img, pt1, pt2, color, 1)
        cv2.circle(result_img, pt1, 3, color, -1)
        cv2.circle(result_img, pt2, 3, color, -1)
    
    # Tambah informasi
    font = cv2.FONT_HERSHEY_SIMPLEX
    info_text = f"Inliers: {inliers} (green) | Outliers: {outliers} (red)"
    cv2.putText(result_img, info_text, (10, 30), font, 0.7, (255, 255, 255), 2)
    
    result['image'] = result_img
    
    return result

def warp_perspective_demo(img1_path, img2_path):
    """
    Demonstrasi warping dengan homography
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        return None
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    detector = create_detector(DETECTOR_TYPE, N_FEATURES)
    matcher = get_matcher(DETECTOR_TYPE)
    
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    matches = matcher.knnMatch(desc1, desc2, k=2)
    good_matches = [m for m_pair in matches if len(m_pair) == 2 
                    for m in [m_pair[0]] if m.distance < 0.75 * m_pair[1].distance]
    
    if len(good_matches) < MIN_MATCH_COUNT:
        return None
    
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    if H is None:
        return None
    
    # Warp img1 ke perspektif img2
    h2, w2 = img2.shape[:2]
    warped = cv2.warpPerspective(img1, H, (w2, h2))
    
    # Buat visualisasi
    # Blend warped dengan scene
    alpha = 0.5
    blended = cv2.addWeighted(warped, alpha, img2, 1-alpha, 0)
    
    # Resize semua gambar ke ukuran yang sama untuk display
    target_h, target_w = 300, 400
    img1_show = cv2.resize(img1, (target_w, target_h))
    img2_show = cv2.resize(img2, (target_w, target_h))
    warped_show = cv2.resize(warped, (target_w, target_h))
    blended_show = cv2.resize(blended, (target_w, target_h))
    
    # Tambah label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img1_show, "Template", (10, 25), font, 0.6, (0, 255, 0), 2)
    cv2.putText(img2_show, "Scene", (10, 25), font, 0.6, (0, 255, 0), 2)
    cv2.putText(warped_show, "Warped", (10, 25), font, 0.6, (0, 255, 0), 2)
    cv2.putText(blended_show, "Blended", (10, 25), font, 0.6, (0, 255, 0), 2)
    
    # Gabung 2x2
    row1 = np.hstack([img1_show, img2_show])
    row2 = np.hstack([warped_show, blended_show])
    result = np.vstack([row1, row2])
    
    return result

def compare_ransac_thresholds(img1_path, img2_path):
    """
    Membandingkan berbagai RANSAC threshold
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        return None
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    detector = create_detector(DETECTOR_TYPE, N_FEATURES)
    matcher = get_matcher(DETECTOR_TYPE)
    
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    matches = matcher.knnMatch(desc1, desc2, k=2)
    good_matches = [m for m_pair in matches if len(m_pair) == 2 
                    for m in [m_pair[0]] if m.distance < 0.75 * m_pair[1].distance]
    
    if len(good_matches) < MIN_MATCH_COUNT:
        return None
    
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    thresholds = [1.0, 3.0, 5.0, 10.0]
    results = []
    
    for thresh in thresholds:
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, thresh)
        
        if H is not None:
            inliers = sum(mask.ravel())
        else:
            inliers = 0
        
        # Buat visualisasi sederhana
        result = img2.copy()
        
        if H is not None:
            h1, w1 = img1.shape[:2]
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
            transformed = cv2.perspectiveTransform(corners, H)
            cv2.polylines(result, [np.int32(transformed)], True, (0, 255, 0), 2)
        
        cv2.putText(result, f"Thresh={thresh}: {inliers} inliers", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        results.append(result)
    
    # Resize
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
    print("PRAKTIKUM 7: HOMOGRAPHY ESTIMATION DENGAN RANSAC")
    print("=" * 70)
    print()
    
    # Print parameter
    print("Parameter yang digunakan:")
    print(f"  - Detector Type: {DETECTOR_TYPE}")
    print(f"  - N Features: {N_FEATURES}")
    print(f"  - Ratio Threshold: {RATIO_THRESHOLD}")
    print(f"  - RANSAC Reproj Threshold: {RANSAC_REPROJ_THRESHOLD}")
    print(f"  - Min Match Count: {MIN_MATCH_COUNT}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Pasangan gambar untuk homography
    image_pairs = [
        ("box.png", "box_in_scene.png"),
    ]
    
    for img1_name, img2_name in image_pairs:
        img1_path = os.path.join(data_dir, img1_name)
        img2_path = os.path.join(data_dir, img2_name)
        
        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            print(f"⚠ File tidak ditemukan: {img1_name} atau {img2_name}")
            continue
        
        print(f"Homography: {img1_name} → {img2_name}")
        print("-" * 40)
        
        try:
            result = homography_ransac(img1_path, img2_path)
            
            print(f"  Keypoints template: {result['kp1']}")
            print(f"  Keypoints scene: {result['kp2']}")
            print(f"  Good matches: {result['good_matches']}")
            
            if result['success']:
                print(f"  ✓ Homography ditemukan!")
                print(f"  Inliers: {result['inliers']}")
                print(f"  Outliers: {result['outliers']}")
                print(f"  Inlier ratio: {result['inliers']/(result['inliers']+result['outliers'])*100:.1f}%")
                print(f"  Waktu proses: {result['time']:.2f} ms")
            else:
                print(f"  ✗ Homography tidak ditemukan")
            
            # Simpan hasil
            pair_name = f"{os.path.splitext(img1_name)[0]}_{os.path.splitext(img2_name)[0]}"
            output_name = f"homography_{pair_name}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, result['image'])
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Warp perspective demo
    print("Membuat demo perspective warp...")
    test_pair = ("box.png", "box_in_scene.png")
    img1_path = os.path.join(data_dir, test_pair[0])
    img2_path = os.path.join(data_dir, test_pair[1])
    
    if os.path.exists(img1_path) and os.path.exists(img2_path):
        warp_demo = warp_perspective_demo(img1_path, img2_path)
        if warp_demo is not None:
            output_path = os.path.join(output_dir, "homography_warp_demo.jpg")
            cv2.imwrite(output_path, warp_demo)
            print(f"  Demo warp disimpan: {output_path}")
    
    # Perbandingan RANSAC thresholds
    print("\nMembuat perbandingan RANSAC thresholds...")
    if os.path.exists(img1_path) and os.path.exists(img2_path):
        comparison = compare_ransac_thresholds(img1_path, img2_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "ransac_threshold_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan threshold disimpan: {output_path}")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah RANSAC_REPROJ_THRESHOLD dari 5.0 ke 1.0
   - Amati: Lebih sedikit inliers
   - Mengapa: Filter lebih ketat
   
2. Ubah RANSAC_REPROJ_THRESHOLD dari 5.0 ke 10.0
   - Amati: Lebih banyak inliers (termasuk yang kurang akurat)
   - Trade-off: Robustness vs accuracy
   
3. Gunakan gambar dengan banyak outliers:
   - RANSAC tetap bisa menemukan homography
   - Ini adalah keunggulan RANSAC dibanding least squares biasa
   
4. Analisis output:
   - Hijau = Inlier (match yang konsisten dengan homography)
   - Merah = Outlier (match yang tidak konsisten)
   - Border biru = Objek template yang terdeteksi di scene
   
5. Coba dengan gambar sendiri:
   - Foto objek planar (buku, poster, kotak)
   - Foto objek tersebut dari sudut berbeda
   - Lihat apakah homography terdeteksi dengan benar
   
6. Inlier Ratio yang baik:
   - > 50%: Cukup baik
   - > 70%: Baik
   - > 90%: Sangat baik
   - < 30%: Mungkin ada masalah dengan gambar/matching
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
