"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 1: Simple Image Stitching dengan Homography Manual

Deskripsi:
    Program ini mendemonstrasikan proses dasar image stitching dengan
    menggunakan feature detection, matching, dan homography estimation.
    Ini adalah implementasi manual untuk memahami pipeline stitching.

Pipeline:
    1. Load gambar kiri dan kanan
    2. Deteksi fitur dengan ORB/SIFT
    3. Match fitur antar gambar
    4. Filter matches dengan ratio test
    5. Estimasi homography dengan RANSAC
    6. Warp gambar kanan ke perspektif gambar kiri
    7. Gabungkan kedua gambar

Teori:
    Homography adalah transformasi proyektif yang memetakan titik-titik
    dari satu bidang ke bidang lain. Dengan minimal 4 pasang titik koresponden,
    kita dapat menghitung matriks homography 3x3.

Parameter yang dapat dimodifikasi:
    - DETECTOR: Pilihan detector ('ORB' atau 'SIFT')
    - MIN_MATCH_COUNT: Minimum jumlah match yang diperlukan
    - RATIO_TEST: Threshold untuk Lowe's ratio test
    - RANSAC_THRESH: Threshold untuk RANSAC

Output:
    - Visualisasi feature matches
    - Hasil stitching

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Pilihan detector: 'ORB' atau 'SIFT'
# ORB: Lebih cepat, gratis, cocok untuk real-time
# SIFT: Lebih akurat, scale-invariant, cocok untuk presisi tinggi
DETECTOR = 'ORB'

# Minimum jumlah good matches untuk proceed stitching
# Semakin tinggi = lebih strict tapi lebih robust
# Typical range: 10-50
MIN_MATCH_COUNT = 10

# Ratio test threshold (Lowe's ratio test)
# Semakin rendah = lebih strict filtering
# Typical range: 0.6-0.8
RATIO_TEST = 0.75

# RANSAC threshold untuk outlier rejection
# Semakin rendah = lebih strict
# Typical range: 3.0-10.0
RANSAC_THRESH = 5.0

# Path ke gambar
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_images(img1_path, img2_path):
    """
    Load dua gambar untuk stitching.
    
    Parameters:
        img1_path: Path gambar pertama (kiri)
        img2_path: Path gambar kedua (kanan)
    
    Returns:
        img1, img2: Gambar dalam format BGR
    """
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None:
        raise ValueError(f"Tidak dapat membaca gambar: {img1_path}")
    if img2 is None:
        raise ValueError(f"Tidak dapat membaca gambar: {img2_path}")
    
    print(f"Gambar 1 dimuat: {img1.shape}")
    print(f"Gambar 2 dimuat: {img2.shape}")
    
    return img1, img2

def detect_and_match_features(img1, img2, detector_type='ORB'):
    """
    Deteksi fitur dan match antar dua gambar.
    
    Parameters:
        img1, img2: Gambar input
        detector_type: 'ORB' atau 'SIFT'
    
    Returns:
        kp1, kp2: Keypoints
        good_matches: List good matches setelah ratio test
        match_img: Visualisasi matches
    """
    # Konversi ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Buat detector
    if detector_type == 'SIFT':
        detector = cv2.SIFT_create()
        # Untuk SIFT, gunakan FLANN matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
    else:  # ORB
        detector = cv2.ORB_create(nfeatures=3000)
        # Untuk ORB, gunakan BFMatcher dengan Hamming distance
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    # Deteksi keypoints dan compute descriptors
    print(f"\nDeteksi fitur dengan {detector_type}...")
    start = time.time()
    
    kp1, des1 = detector.detectAndCompute(gray1, None)
    kp2, des2 = detector.detectAndCompute(gray2, None)
    
    detect_time = time.time() - start
    print(f"  Keypoints gambar 1: {len(kp1)}")
    print(f"  Keypoints gambar 2: {len(kp2)}")
    print(f"  Waktu deteksi: {detect_time*1000:.2f} ms")
    
    # Cek apakah ada descriptors
    if des1 is None or des2 is None or len(des1) < 2 or len(des2) < 2:
        raise ValueError("Tidak cukup fitur yang terdeteksi!")
    
    # Match dengan KNN (k=2 untuk ratio test)
    print("\nMatching fitur...")
    start = time.time()
    
    # Untuk ORB dengan BFMatcher, gunakan descriptor asli (uint8)
    # Untuk SIFT dengan FLANN, sudah float32
    if detector_type == 'ORB':
        # Untuk ORB, gunakan knnMatch dengan BFMatcher langsung
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(des1, des2, k=2)
    else:
        matches = matcher.knnMatch(des1, des2, k=2)
    
    match_time = time.time() - start
    print(f"  Total matches: {len(matches)}")
    print(f"  Waktu matching: {match_time*1000:.2f} ms")
    
    # Apply ratio test (Lowe's ratio test)
    good_matches = []
    for m, n in matches:
        if m.distance < RATIO_TEST * n.distance:
            good_matches.append(m)
    
    print(f"  Good matches (ratio test {RATIO_TEST}): {len(good_matches)}")
    
    # Visualisasi matches
    match_img = cv2.drawMatches(
        img1, kp1, img2, kp2, good_matches, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return kp1, kp2, good_matches, match_img

def estimate_homography(kp1, kp2, good_matches):
    """
    Estimasi matriks homography menggunakan RANSAC.
    
    Parameters:
        kp1, kp2: Keypoints dari kedua gambar
        good_matches: Good matches hasil ratio test
    
    Returns:
        H: Matriks homography 3x3
        mask: Inlier mask dari RANSAC
    """
    if len(good_matches) < MIN_MATCH_COUNT:
        raise ValueError(f"Tidak cukup matches! "
                        f"Ditemukan {len(good_matches)}, "
                        f"minimum {MIN_MATCH_COUNT}")
    
    # Ekstrak koordinat titik dari matches
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Hitung homography dengan RANSAC
    print("\nEstimasi homography dengan RANSAC...")
    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, RANSAC_THRESH)
    
    # Hitung statistik inliers
    inliers = np.sum(mask)
    inlier_ratio = inliers / len(good_matches) * 100
    
    print(f"  Inliers: {inliers}/{len(good_matches)} ({inlier_ratio:.1f}%)")
    print(f"  Homography matrix:\n{H}")
    
    return H, mask

def stitch_images(img1, img2, H):
    """
    Gabungkan dua gambar menggunakan homography.
    
    Parameters:
        img1: Gambar base (kiri)
        img2: Gambar yang akan di-warp (kanan)
        H: Matriks homography
    
    Returns:
        result: Gambar hasil stitching
    """
    print("\nMelakukan warping dan stitching...")
    
    # Dapatkan dimensi
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Hitung corners dari gambar 2 setelah transformasi
    corners_img2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners_img2, H)
    
    # Hitung corners gabungan
    corners_img1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    all_corners = np.concatenate([corners_img1, transformed_corners], axis=0)
    
    # Hitung bounding box
    [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 0.5)
    
    # Translation matrix untuk shift ke koordinat positif
    translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
    
    # Warp gambar 2
    output_size = (x_max - x_min, y_max - y_min)
    result = cv2.warpPerspective(img2, translation @ H, output_size)
    
    # Overlay gambar 1
    result[-y_min:-y_min + h1, -x_min:-x_min + w1] = img1
    
    print(f"  Dimensi output: {result.shape}")
    
    return result

def simple_blend(img1, img2, H):
    """
    Gabungkan dua gambar dengan simple blending di area overlap.
    
    Parameters:
        img1: Gambar base (kiri)
        img2: Gambar yang akan di-warp (kanan)
        H: Matriks homography
    
    Returns:
        result: Gambar hasil stitching dengan blending
    """
    print("\nMelakukan warping dan blending...")
    
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Hitung bounding box seperti sebelumnya
    corners_img2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners_img2, H)
    
    corners_img1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    all_corners = np.concatenate([corners_img1, transformed_corners], axis=0)
    
    [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 0.5)
    
    translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
    output_size = (x_max - x_min, y_max - y_min)
    
    # Warp gambar 2
    warped2 = cv2.warpPerspective(img2, translation @ H, output_size)
    
    # Buat canvas kosong untuk gambar 1
    warped1 = np.zeros_like(warped2)
    warped1[-y_min:-y_min + h1, -x_min:-x_min + w1] = img1
    
    # Buat mask untuk blending
    mask1 = (warped1 > 0).astype(np.float32)
    mask2 = (warped2 > 0).astype(np.float32)
    
    # Area overlap
    overlap = mask1 * mask2
    
    # Simple averaging di area overlap
    result = np.zeros_like(warped1, dtype=np.float32)
    
    # Area hanya gambar 1
    only1 = mask1 * (1 - mask2[:,:,0:1])
    result += warped1.astype(np.float32) * only1
    
    # Area hanya gambar 2
    only2 = mask2 * (1 - mask1[:,:,0:1])
    result += warped2.astype(np.float32) * only2
    
    # Area overlap - average
    result += 0.5 * (warped1.astype(np.float32) + warped2.astype(np.float32)) * overlap
    
    return result.astype(np.uint8)

def main():
    """
    Fungsi utama untuk menjalankan simple stitching.
    """
    print("=" * 60)
    print("SIMPLE IMAGE STITCHING")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load gambar
    # Menggunakan gambar stereo left/right
    img1_path = os.path.join(DATA_DIR, "left01.jpg")
    img2_path = os.path.join(DATA_DIR, "right01.jpg")
    
    # Fallback ke gambar lain jika tidak ada
    if not os.path.exists(img1_path):
        img1_path = os.path.join(DATA_DIR, "graf1.png")
        img2_path = os.path.join(DATA_DIR, "graf3.png")
    
    if not os.path.exists(img1_path):
        print("ERROR: Gambar tidak ditemukan!")
        print("Jalankan download_sample_data.py terlebih dahulu.")
        return
    
    try:
        img1, img2 = load_images(img1_path, img2_path)
        
        # Resize jika terlalu besar
        max_dim = 800
        h1, w1 = img1.shape[:2]
        if max(h1, w1) > max_dim:
            scale = max_dim / max(h1, w1)
            img1 = cv2.resize(img1, None, fx=scale, fy=scale)
            img2 = cv2.resize(img2, None, fx=scale, fy=scale)
            print(f"\nGambar di-resize ke scale {scale:.2f}")
        
        # Deteksi dan match fitur
        kp1, kp2, good_matches, match_img = detect_and_match_features(
            img1, img2, DETECTOR
        )
        
        # Estimasi homography
        H, mask = estimate_homography(kp1, kp2, good_matches)
        
        # Stitch tanpa blending
        result_no_blend = stitch_images(img1, img2, H)
        
        # Stitch dengan simple blending
        result_blend = simple_blend(img1, img2, H)
        
        # Visualisasi hasil
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Gambar input
        combined_input = np.hstack([
            cv2.cvtColor(img1, cv2.COLOR_BGR2RGB),
            cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        ])
        axes[0, 0].imshow(combined_input)
        axes[0, 0].set_title("Input Images (Kiri | Kanan)")
        axes[0, 0].axis('off')
        
        # Feature matches
        axes[0, 1].imshow(cv2.cvtColor(match_img, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title(f"Feature Matches ({len(good_matches)} good matches)")
        axes[0, 1].axis('off')
        
        # Hasil tanpa blending
        axes[1, 0].imshow(cv2.cvtColor(result_no_blend, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title("Stitching Tanpa Blending")
        axes[1, 0].axis('off')
        
        # Hasil dengan blending
        axes[1, 1].imshow(cv2.cvtColor(result_blend, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title("Stitching Dengan Simple Blending")
        axes[1, 1].axis('off')
        
        plt.suptitle(f"Simple Image Stitching\n"
                    f"Detector: {DETECTOR}, Matches: {len(good_matches)}, "
                    f"Ratio: {RATIO_TEST}", fontsize=12)
        plt.tight_layout()
        
        # Simpan hasil
        output_path = os.path.join(OUTPUT_DIR, "01_simple_stitching_result.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\nHasil disimpan ke: {output_path}")
        
        # Simpan panorama
        pano_path = os.path.join(OUTPUT_DIR, "01_panorama.jpg")
        cv2.imwrite(pano_path, result_blend)
        print(f"Panorama disimpan ke: {pano_path}")
        
        plt.show()
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
