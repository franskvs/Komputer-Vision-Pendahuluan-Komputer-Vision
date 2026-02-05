# ============================================================
# PROGRAM: 06_homography.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk Homography estimation
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep homography matrix
#   2. Estimasi homography dengan feature matching
#   3. Penggunaan RANSAC untuk robust estimation
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar
GAMBAR_1 = "book1.jpg"    # Gambar sumber
GAMBAR_2 = "book2.jpg"    # Gambar target (transformed)

# 2. Feature Detector
# Opsi: 'orb', 'sift', 'akaze'
DETECTOR_TYPE = 'sift'

# 3. Parameter Feature Detection
ORB_NFEATURES = 1000
SIFT_NFEATURES = 0

# 4. Ratio Test Threshold
RATIO_THRESHOLD = 0.75

# 5. RANSAC Parameters
RANSAC_REPROJ_THRESHOLD = 5.0  # Maximum reprojection error
MIN_MATCH_COUNT = 10           # Minimum matches required

# 6. Visualisasi
DRAW_MATCHES = True
SHOW_WARPED = True

# 7. Auto-close plot (detik)
AUTO_CLOSE_SECONDS = 2.0

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    lokasi_potensial = [
        os.path.join(direktori_script, "data", "images", nama_file),
        os.path.join(direktori_script, "..", "..", "Bab-01-Pendahuluan", 
                     "data", "images", nama_file),
        os.path.join(direktori_script, nama_file),
    ]
    
    for path in lokasi_potensial:
        if os.path.exists(path):
            return path
    
    return lokasi_potensial[0]


def buat_gambar_sample_pair():
    """Membuat sepasang gambar untuk homography estimation"""
    # Gambar 1 - Original
    gambar1 = np.zeros((400, 500, 3), dtype=np.uint8)
    gambar1[:, :] = [50, 50, 50]
    
    # Book-like pattern
    cv2.rectangle(gambar1, (100, 50), (400, 350), (200, 200, 200), -1)
    cv2.rectangle(gambar1, (100, 50), (400, 350), (100, 100, 100), 3)
    
    # Text content
    cv2.putText(gambar1, "COMPUTER", (130, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 2)
    cv2.putText(gambar1, "VISION", (170, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 2)
    
    # Some patterns
    for i in range(3):
        y = 240 + i * 30
        cv2.line(gambar1, (120, y), (380, y), (80, 80, 80), 1)
    
    cv2.rectangle(gambar1, (150, 280), (350, 320), (100, 150, 200), -1)
    
    # Gambar 2 - Perspective transformed
    h, w = gambar1.shape[:2]
    
    # Define source and destination points for perspective transform
    src_pts = np.float32([[100, 50], [400, 50], [400, 350], [100, 350]])
    dst_pts = np.float32([[150, 80], [420, 30], [380, 380], [80, 320]])
    
    # Get perspective transform matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    # Apply perspective transform
    gambar2 = cv2.warpPerspective(gambar1, M, (w, h))
    
    # Add some noise
    noise = np.random.randint(0, 20, gambar2.shape, dtype=np.uint8)
    gambar2 = cv2.add(gambar2, noise)
    
    return gambar1, gambar2


def tampilkan_plot():
    """Tampilkan plot sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(AUTO_CLOSE_SECONDS)
    plt.close()


# ============================================================
# FUNGSI HOMOGRAPHY
# ============================================================

def detect_and_match_features(img1, img2, detector_type='sift', ratio=0.75):
    """
    Detect features dan match antara dua gambar
    
    Return:
    - kp1, kp2: keypoints
    - good_matches: filtered matches
    """
    # Convert ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Create detector
    if detector_type == 'orb':
        detector = cv2.ORB_create(nfeatures=ORB_NFEATURES)
        norm_type = cv2.NORM_HAMMING
    elif detector_type == 'sift':
        detector = cv2.SIFT_create(nfeatures=SIFT_NFEATURES)
        norm_type = cv2.NORM_L2
    elif detector_type == 'akaze':
        detector = cv2.AKAZE_create()
        norm_type = cv2.NORM_HAMMING
    
    # Detect and compute
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    # Match
    bf = cv2.BFMatcher(norm_type)
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good_matches.append(m)
    
    return kp1, kp2, good_matches


def estimate_homography(kp1, kp2, matches, ransac_thresh=5.0):
    """
    Estimate homography matrix menggunakan RANSAC
    
    Homography Matrix (3x3):
    | h11 h12 h13 |   | x |   | x' |
    | h21 h22 h23 | × | y | = | y' |
    | h31 h32 h33 |   | 1 |   | w  |
    
    Where: x'_norm = x'/w, y'_norm = y'/w
    
    Return:
    - H: homography matrix (3x3)
    - mask: inlier mask
    """
    if len(matches) < 4:
        return None, None
    
    # Extract matched point coordinates
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Find homography using RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_thresh)
    
    return H, mask


def warp_image(img, H, output_size=None):
    """
    Warp image menggunakan homography matrix
    
    Return:
    - warped: transformed image
    """
    if output_size is None:
        output_size = (img.shape[1], img.shape[0])
    
    warped = cv2.warpPerspective(img, H, output_size)
    
    return warped


def decompose_homography(H):
    """
    Decompose homography matrix untuk analisis
    
    Return:
    - rotation, translation, scale info
    """
    # Normalize
    H = H / H[2, 2]
    
    # Extract approximate scale
    scale_x = np.sqrt(H[0, 0]**2 + H[1, 0]**2)
    scale_y = np.sqrt(H[0, 1]**2 + H[1, 1]**2)
    
    # Extract approximate rotation
    rotation = np.arctan2(H[1, 0], H[0, 0])
    
    # Translation
    tx = H[0, 2]
    ty = H[1, 2]
    
    return {
        'scale_x': scale_x,
        'scale_y': scale_y,
        'rotation_deg': np.degrees(rotation),
        'translation': (tx, ty)
    }


def draw_homography_result(img1, img2, kp1, kp2, matches, H, mask):
    """Visualisasi hasil homography estimation"""
    h, w = img1.shape[:2]
    
    # Draw bounding box dari img1 yang di-transform ke img2
    corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    
    if H is not None:
        transformed_corners = cv2.perspectiveTransform(corners, H)
        img2_with_box = img2.copy()
        cv2.polylines(img2_with_box, [np.int32(transformed_corners)], 
                      True, (0, 255, 0), 3)
    else:
        img2_with_box = img2.copy()
    
    # Draw matches
    if mask is not None:
        matches_mask = mask.ravel().tolist()
    else:
        matches_mask = None
    
    draw_params = dict(
        matchColor=(0, 255, 0),
        singlePointColor=(255, 0, 0),
        matchesMask=matches_mask,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    img_matches = cv2.drawMatches(img1, kp1, img2_with_box, kp2, 
                                   matches, None, **draw_params)
    
    return img_matches


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_ransac_effect():
    """Demonstrasi pengaruh RANSAC threshold"""
    print("\n" + "=" * 60)
    print("PENGARUH RANSAC REPROJECTION THRESHOLD")
    print("=" * 60)
    
    print("""
RANSAC THRESHOLD:

Threshold menentukan maximum reprojection error untuk
dianggap sebagai inlier.

Threshold kecil (1-3):
├── Sangat strict
├── Hanya matches yang sangat akurat
└── Mungkin terlalu sedikit inliers

Threshold sedang (4-6):
├── Balance bagus
└── Cocok untuk kebanyakan kasus

Threshold besar (8+):
├── Lebih toleran terhadap noise
├── Risiko memasukkan outliers
└── Cocok untuk data noisy
    """)
    
    # Load atau buat gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
    else:
        img1, img2 = buat_gambar_sample_pair()
    
    # Detect features
    kp1, kp2, matches = detect_and_match_features(img1, img2, DETECTOR_TYPE)
    
    thresholds = [1.0, 3.0, 5.0, 10.0]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for i, thresh in enumerate(thresholds):
        H, mask = estimate_homography(kp1, kp2, matches, thresh)
        
        if H is not None and mask is not None:
            n_inliers = np.sum(mask)
            inlier_ratio = n_inliers / len(matches) * 100
            
            result = draw_homography_result(img1, img2, kp1, kp2, matches, H, mask)
            
            axes[i].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            axes[i].set_title(f"Threshold = {thresh}\n"
                             f"Inliers: {n_inliers}/{len(matches)} ({inlier_ratio:.1f}%)")
        else:
            axes[i].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
            axes[i].set_title(f"Threshold = {thresh}\nFailed to estimate")
        
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh RANSAC Threshold pada Homography Estimation", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_manual_homography():
    """Demonstrasi homography dengan titik manual"""
    print("\n" + "=" * 60)
    print("HOMOGRAPHY DENGAN TITIK MANUAL")
    print("=" * 60)
    
    print("""
Homography dapat dihitung dari 4 pasangan titik korespondensi:

Source points → Destination points

Contoh:
├── Mengoreksi perspektif dokumen
├── Meluruskan gambar dari sudut
└── Virtual billboards
    """)
    
    # Buat gambar sederhana
    img = np.zeros((400, 500, 3), dtype=np.uint8)
    img[:, :] = [50, 50, 50]
    
    # Draw trapezoid (simulating tilted view)
    pts_src = np.array([[100, 300], [150, 100], [350, 100], [400, 300]])
    cv2.fillPoly(img, [pts_src], (200, 200, 200))
    cv2.putText(img, "TEXT", (200, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 50, 50), 2)
    
    # Destination points (rectangle)
    pts_dst = np.array([[100, 300], [100, 100], [400, 100], [400, 300]])
    
    # Calculate homography
    H = cv2.getPerspectiveTransform(
        np.float32(pts_src),
        np.float32(pts_dst)
    )
    
    # Warp
    warped = cv2.warpPerspective(img, H, (img.shape[1], img.shape[0]))
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    for pt in pts_src:
        axes[0].plot(pt[0], pt[1], 'ro', markersize=10)
    axes[0].set_title("Source Image\n(Perspective distorted)")
    axes[0].axis('off')
    
    # Show H matrix
    axes[1].text(0.1, 0.5, f"Homography Matrix:\n\n{H[0,0]:8.4f} {H[0,1]:8.4f} {H[0,2]:8.4f}\n"
                           f"{H[1,0]:8.4f} {H[1,1]:8.4f} {H[1,2]:8.4f}\n"
                           f"{H[2,0]:8.4f} {H[2,1]:8.4f} {H[2,2]:8.4f}",
                 fontfamily='monospace', fontsize=12, transform=axes[1].transAxes)
    axes[1].axis('off')
    axes[1].set_title("Homography Matrix")
    
    axes[2].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    for pt in pts_dst:
        axes[2].plot(pt[0], pt[1], 'go', markersize=10)
    axes[2].set_title("Warped Image\n(Perspective corrected)")
    axes[2].axis('off')
    
    plt.suptitle("Manual Homography with 4 Point Correspondences", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_homography_decomposition():
    """Demonstrasi decomposition homography"""
    print("\n" + "=" * 60)
    print("DECOMPOSITION HOMOGRAPHY MATRIX")
    print("=" * 60)
    
    # Load atau buat gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
    else:
        img1, img2 = buat_gambar_sample_pair()
    
    # Estimate homography
    kp1, kp2, matches = detect_and_match_features(img1, img2, DETECTOR_TYPE)
    H, mask = estimate_homography(kp1, kp2, matches)
    
    if H is not None:
        print("\nHomography Matrix:")
        print(H)
        
        decomp = decompose_homography(H)
        
        print(f"\nDecomposition (approximate):")
        print(f"Scale X: {decomp['scale_x']:.4f}")
        print(f"Scale Y: {decomp['scale_y']:.4f}")
        print(f"Rotation: {decomp['rotation_deg']:.2f} degrees")
        print(f"Translation: ({decomp['translation'][0]:.2f}, {decomp['translation'][1]:.2f})")


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: HOMOGRAPHY ESTIMATION")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
HOMOGRAPHY adalah transformasi projective yang memetakan
titik-titik dari satu plane ke plane lain.

HOMOGRAPHY MATRIX (3x3):

    | h11 h12 h13 |
H = | h21 h22 h23 |
    | h31 h32 h33 |

Transformasi:
    | x' |       | x |
    | y' | = H × | y |
    | w  |       | 1 |

Dimana: x'_final = x'/w, y'_final = y'/w

PROPERTIES:
├── 8 degrees of freedom (9 elements - 1 scale)
├── Memerlukan minimal 4 point correspondences
├── Mempertahankan garis lurus (lines → lines)
└── Tidak mempertahankan parallelism

ESTIMASI:
├── Direct Linear Transform (DLT)
├── Least Squares (sensitif outliers)
└── RANSAC (robust terhadap outliers)

APLIKASI:
├── Panorama stitching
├── Augmented Reality
├── Document scanning
├── Planar object tracking
└── Virtual billboards
    """)
    
    # Load gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        print(f"[INFO] Memuat gambar: {path1}")
        print(f"[INFO] Memuat gambar: {path2}")
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
    else:
        print("[INFO] Membuat gambar sample...")
        img1, img2 = buat_gambar_sample_pair()
    
    print(f"[INFO] Image 1 size: {img1.shape}")
    print(f"[INFO] Image 2 size: {img2.shape}")
    print(f"[INFO] Detector: {DETECTOR_TYPE}")
    
    # Step 1: Feature detection dan matching
    print("\n[STEP 1] Feature Detection & Matching...")
    kp1, kp2, matches = detect_and_match_features(img1, img2, DETECTOR_TYPE, 
                                                   RATIO_THRESHOLD)
    
    print(f"   Keypoints img1: {len(kp1)}")
    print(f"   Keypoints img2: {len(kp2)}")
    print(f"   Good matches: {len(matches)}")
    
    if len(matches) < MIN_MATCH_COUNT:
        print(f"\n[ERROR] Not enough matches ({len(matches)}/{MIN_MATCH_COUNT})")
        return
    
    # Step 2: Homography estimation
    print("\n[STEP 2] Homography Estimation (RANSAC)...")
    print(f"   RANSAC threshold: {RANSAC_REPROJ_THRESHOLD}")
    
    H, mask = estimate_homography(kp1, kp2, matches, RANSAC_REPROJ_THRESHOLD)
    
    if H is None:
        print("[ERROR] Failed to estimate homography!")
        return
    
    n_inliers = np.sum(mask)
    inlier_ratio = n_inliers / len(matches) * 100
    
    print(f"   Inliers: {n_inliers}/{len(matches)} ({inlier_ratio:.1f}%)")
    
    # Print homography matrix
    print("\n[HOMOGRAPHY MATRIX]")
    print(f"   {H[0,0]:10.6f} {H[0,1]:10.6f} {H[0,2]:10.6f}")
    print(f"   {H[1,0]:10.6f} {H[1,1]:10.6f} {H[1,2]:10.6f}")
    print(f"   {H[2,0]:10.6f} {H[2,1]:10.6f} {H[2,2]:10.6f}")
    
    # Decomposition
    decomp = decompose_homography(H)
    print(f"\n[DECOMPOSITION]")
    print(f"   Scale X: {decomp['scale_x']:.4f}")
    print(f"   Scale Y: {decomp['scale_y']:.4f}")
    print(f"   Rotation: {decomp['rotation_deg']:.2f}°")
    print(f"   Translation: ({decomp['translation'][0]:.2f}, {decomp['translation'][1]:.2f})")
    
    # Step 3: Visualisasi
    print("\n[STEP 3] Visualisasi...")
    
    # Result with matches
    result = draw_homography_result(img1, img2, kp1, kp2, matches, H, mask)
    
    # Warp img1 ke perspektif img2
    warped = warp_image(img1, H, (img2.shape[1], img2.shape[0]))
    
    # Blend untuk comparison
    alpha = 0.5
    blended = cv2.addWeighted(warped, alpha, img2, 1-alpha, 0)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Source Image (img1)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Target Image (img2)")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"Feature Matches\nInliers: {n_inliers}/{len(matches)}")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title("Warped img1 blended with img2")
    axes[1, 1].axis('off')
    
    plt.suptitle("Homography Estimation", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()
    
    # Demo tambahan
    demo_ransac_effect()
    demo_manual_homography()
    demo_homography_decomposition()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN HOMOGRAPHY")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Feature detection & matching
kp1, desc1 = detector.detectAndCompute(img1, None)
kp2, desc2 = detector.detectAndCompute(img2, None)
matches = bf.knnMatch(desc1, desc2, k=2)

# Extract point correspondences
src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

# Estimate homography with RANSAC
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Manual homography from 4 points
H = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Warp image
warped = cv2.warpPerspective(img, H, (width, height))

# Transform points
new_pts = cv2.perspectiveTransform(pts, H)

METODE ESTIMASI:
├── 0 atau cv2.LMEDS: Least-Median (tanpa threshold)
├── cv2.RANSAC: RANSAC robust estimation
├── cv2.RHO: PROSAC-based robust method
└── cv2.USAC_DEFAULT: Universal RANSAC

TIPS:
1. Minimal 4 point correspondences
2. Gunakan RANSAC untuk data dengan outliers
3. Threshold 3-10 biasanya bagus
4. Cek inlier ratio (>50% bagus)
5. Homography hanya valid untuk planar scenes
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
