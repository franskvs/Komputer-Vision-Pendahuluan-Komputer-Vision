# ============================================================
# PROGRAM: 02_feature_matching.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk feature matching (BF, FLANN, Ratio Test)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep feature matching
#   2. Perbandingan Brute-Force dan FLANN matcher
#   3. Implementasi Lowe's ratio test
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar (2 gambar untuk matching)
GAMBAR_1 = "object1.jpg"    # Gambar referensi (query)
GAMBAR_2 = "object2.jpg"    # Gambar target (train)

# 2. Jenis Detector untuk feature extraction
# Opsi: 'orb', 'sift', 'akaze'
DETECTOR_TYPE = 'orb'

# 3. Jenis Matcher
# Opsi: 'bf' (Brute-Force), 'flann' (Fast Library for Approximate NN)
MATCHER_TYPE = 'bf'

# 4. Ratio Test Threshold (Lowe's Ratio Test)
# Nilai 0.7-0.8 biasanya bagus
RATIO_THRESHOLD = 0.75

# 5. Cross-check untuk Brute-Force
BF_CROSS_CHECK = False

# 6. Jumlah top matches untuk ditampilkan
TOP_MATCHES = 50

# 7. Parameter ORB
ORB_NFEATURES = 1000

# 8. FLANN Parameters
FLANN_INDEX_KDTREE = 1
FLANN_INDEX_LSH = 6
FLANN_TREES = 5
FLANN_CHECKS = 50

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
    """Membuat sepasang gambar sample untuk matching"""
    # Gambar 1 - Original
    gambar1 = np.zeros((300, 400, 3), dtype=np.uint8)
    gambar1[:, :] = [50, 50, 50]
    
    # Pattern yang sama di kedua gambar
    cv2.rectangle(gambar1, (100, 50), (200, 150), (255, 200, 100), -1)
    cv2.circle(gambar1, (300, 100), 40, (100, 200, 255), -1)
    cv2.fillPoly(gambar1, [np.array([[50, 250], [100, 180], [150, 250]])], 
                 (200, 100, 200))
    
    # Checkerboard
    for i in range(4):
        for j in range(4):
            x = 200 + j * 25
            y = 180 + i * 25
            if (i + j) % 2 == 0:
                cv2.rectangle(gambar1, (x, y), (x+25, y+25), (255, 255, 255), -1)
    
    cv2.putText(gambar1, "QUERY", (150, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Gambar 2 - Transformed (rotated & scaled)
    h, w = gambar1.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 15, 0.9)  # 15 derajat, 0.9x scale
    gambar2 = cv2.warpAffine(gambar1, M, (w, h))
    
    # Tambah sedikit noise
    noise = np.random.randint(0, 20, gambar2.shape, dtype=np.uint8)
    gambar2 = cv2.add(gambar2, noise)
    
    # Ubah text
    cv2.rectangle(gambar2, (100, 250), (250, 290), (50, 50, 50), -1)
    cv2.putText(gambar2, "TRAIN", (150, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return gambar1, gambar2


# ============================================================
# FUNGSI FEATURE MATCHING
# ============================================================

def detect_features(gambar, detector_type='orb'):
    """
    Detect features dan compute descriptors
    
    Parameter:
    - gambar: input image
    - detector_type: 'orb', 'sift', atau 'akaze'
    
    Return:
    - keypoints: detected keypoints
    - descriptors: feature descriptors
    """
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY) if len(gambar.shape) == 3 else gambar
    
    if detector_type == 'orb':
        detector = cv2.ORB_create(nfeatures=ORB_NFEATURES)
    elif detector_type == 'sift':
        detector = cv2.SIFT_create()
    elif detector_type == 'akaze':
        detector = cv2.AKAZE_create()
    else:
        raise ValueError(f"Unknown detector: {detector_type}")
    
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def brute_force_matching(desc1, desc2, detector_type='orb', cross_check=False):
    """
    Brute-Force Matching
    
    Membandingkan setiap descriptor dari gambar 1 dengan
    semua descriptors dari gambar 2.
    
    Parameter:
    - desc1, desc2: descriptors dari kedua gambar
    - detector_type: untuk menentukan norm type
    - cross_check: enable cross-checking
    
    Return:
    - matches: list of DMatch objects
    """
    # Pilih norm berdasarkan descriptor type
    if detector_type == 'orb':
        # ORB menggunakan binary descriptors
        norm_type = cv2.NORM_HAMMING
    else:
        # SIFT, AKAZE menggunakan float descriptors
        norm_type = cv2.NORM_L2
    
    # Create BF Matcher
    bf = cv2.BFMatcher(norm_type, crossCheck=cross_check)
    
    if cross_check:
        # Cross-check mode - returns single matches
        matches = bf.match(desc1, desc2)
        return sorted(matches, key=lambda x: x.distance)
    else:
        # KNN mode - returns k nearest matches
        matches = bf.knnMatch(desc1, desc2, k=2)
        return matches


def flann_matching(desc1, desc2, detector_type='orb'):
    """
    FLANN (Fast Library for Approximate Nearest Neighbors) Matching
    
    Lebih cepat dari Brute-Force untuk large datasets.
    Menggunakan approximate nearest neighbor search.
    
    Parameter:
    - desc1, desc2: descriptors dari kedua gambar
    - detector_type: untuk menentukan index type
    
    Return:
    - matches: list of DMatch objects
    """
    if detector_type == 'orb':
        # ORB - gunakan LSH index untuk binary descriptors
        index_params = dict(
            algorithm=FLANN_INDEX_LSH,
            table_number=6,
            key_size=12,
            multi_probe_level=1
        )
    else:
        # SIFT/AKAZE - gunakan KD-Tree untuk float descriptors
        index_params = dict(
            algorithm=FLANN_INDEX_KDTREE,
            trees=FLANN_TREES
        )
    
    search_params = dict(checks=FLANN_CHECKS)
    
    # Convert descriptors ke float32 jika perlu
    if desc1.dtype != np.float32:
        desc1 = desc1.astype(np.float32)
        desc2 = desc2.astype(np.float32)
    
    # Create FLANN matcher
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    # KNN Match
    matches = flann.knnMatch(desc1, desc2, k=2)
    
    return matches


def apply_ratio_test(matches, ratio=0.75):
    """
    Lowe's Ratio Test
    
    Filter matches berdasarkan rasio jarak antara
    best match dan second best match.
    
    Jika d(best) / d(second) < ratio, match diterima.
    
    Parameter:
    - matches: list of knn matches (k=2)
    - ratio: threshold ratio
    
    Return:
    - good_matches: filtered matches
    """
    good_matches = []
    
    for match_pair in matches:
        # Pastikan ada 2 matches
        if len(match_pair) == 2:
            m, n = match_pair
            # Lowe's ratio test
            if m.distance < ratio * n.distance:
                good_matches.append(m)
    
    return good_matches


def visualize_matches(img1, kp1, img2, kp2, matches, title="Matches"):
    """Visualisasi feature matches"""
    # Draw matches
    img_matches = cv2.drawMatches(
        img1, kp1, img2, kp2, matches[:TOP_MATCHES], None,
        matchColor=(0, 255, 0),
        singlePointColor=(255, 0, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return img_matches


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_ratio_test_effect():
    """Demonstrasi pengaruh ratio threshold"""
    print("\n" + "=" * 60)
    print("PENGARUH RATIO THRESHOLD")
    print("=" * 60)
    
    print("""
LOWE'S RATIO TEST:

Konsep: Bandingkan jarak best match (m) dengan second best (n)
        Jika m.distance < ratio * n.distance → match valid

Threshold rendah (0.5-0.6):
├── Sangat strict, hanya match yang sangat confident
└── Sedikit matches, tapi hampir tidak ada false positives

Threshold sedang (0.7-0.75):
├── Balance antara quantity dan quality
└── Rekomendasi untuk kebanyakan aplikasi

Threshold tinggi (0.8-0.9):
├── Lebih banyak matches
└── Risiko lebih banyak false positives
    """)
    
    # Load atau buat gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        gambar1 = cv2.imread(path1)
        gambar2 = cv2.imread(path2)
    else:
        gambar1, gambar2 = buat_gambar_sample_pair()
    
    # Detect features
    kp1, desc1 = detect_features(gambar1, 'sift')
    kp2, desc2 = detect_features(gambar2, 'sift')
    
    # BF matching
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    # Test different ratios
    ratios = [0.5, 0.65, 0.75, 0.85]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, ratio in enumerate(ratios):
        good = apply_ratio_test(matches, ratio)
        
        img_matches = cv2.drawMatches(
            gambar1, kp1, gambar2, kp2, good[:30], None,
            matchColor=(0, 255, 0),
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        
        axes[i].imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"Ratio = {ratio}\n{len(good)} matches")
        axes[i].axis('off')
    
    plt.suptitle("Pengaruh Ratio Threshold pada Matching", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_bf_vs_flann():
    """Perbandingan BF vs FLANN"""
    print("\n" + "=" * 60)
    print("BRUTE-FORCE vs FLANN MATCHING")
    print("=" * 60)
    
    print("""
BRUTE-FORCE MATCHER:
├── Exact nearest neighbor search
├── Membandingkan setiap descriptor
├── Akurat tapi lambat untuk dataset besar
└── Cocok untuk: dataset kecil, akurasi penting

FLANN MATCHER:
├── Approximate nearest neighbor search
├── Menggunakan indexing untuk mempercepat
├── Lebih cepat tapi tidak selalu exact match
└── Cocok untuk: dataset besar, real-time applications

COMPARISON:
| Aspect      | Brute-Force | FLANN      |
|-------------|-------------|------------|
| Accuracy    | 100%        | ~95-99%    |
| Speed       | O(n*m)      | O(log n)   |
| Memory      | Low         | Higher     |
| Use Case    | Small data  | Large data |
    """)
    
    # Load atau buat gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        gambar1 = cv2.imread(path1)
        gambar2 = cv2.imread(path2)
    else:
        gambar1, gambar2 = buat_gambar_sample_pair()
    
    # SIFT detection
    kp1, desc1 = detect_features(gambar1, 'sift')
    kp2, desc2 = detect_features(gambar2, 'sift')
    
    print(f"\nDetected: {len(kp1)} keypoints (img1), {len(kp2)} keypoints (img2)")
    
    # BF Matching
    start = time.time()
    bf_matches = brute_force_matching(desc1, desc2, 'sift', False)
    bf_good = apply_ratio_test(bf_matches, RATIO_THRESHOLD)
    bf_time = (time.time() - start) * 1000
    
    # FLANN Matching
    start = time.time()
    flann_matches = flann_matching(desc1, desc2, 'sift')
    flann_good = apply_ratio_test(flann_matches, RATIO_THRESHOLD)
    flann_time = (time.time() - start) * 1000
    
    print(f"\nResults:")
    print(f"BF Matcher:    {len(bf_good)} matches, {bf_time:.2f} ms")
    print(f"FLANN Matcher: {len(flann_good)} matches, {flann_time:.2f} ms")
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    bf_img = cv2.drawMatches(
        gambar1, kp1, gambar2, kp2, bf_good[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    flann_img = cv2.drawMatches(
        gambar1, kp1, gambar2, kp2, flann_good[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    axes[0].imshow(cv2.cvtColor(bf_img, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"Brute-Force Matching\n{len(bf_good)} matches, {bf_time:.1f}ms")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(flann_img, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"FLANN Matching\n{len(flann_good)} matches, {flann_time:.1f}ms")
    axes[1].axis('off')
    
    plt.suptitle("Brute-Force vs FLANN Matching Comparison", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_cross_check():
    """Demonstrasi cross-check matching"""
    print("\n" + "=" * 60)
    print("CROSS-CHECK MATCHING")
    print("=" * 60)
    
    print("""
CROSS-CHECK:

Konsep: Match diterima hanya jika keduanya saling match
        A → B dan B → A harus sama

Keuntungan:
├── Mengurangi false positives
├── Tidak perlu ratio test
└── Lebih simple

Kekurangan:
├── Lebih strict, mungkin kehilangan good matches
└── Tidak bisa menggunakan knnMatch
    """)
    
    # Load atau buat gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        gambar1 = cv2.imread(path1)
        gambar2 = cv2.imread(path2)
    else:
        gambar1, gambar2 = buat_gambar_sample_pair()
    
    # ORB detection
    kp1, desc1 = detect_features(gambar1, 'orb')
    kp2, desc2 = detect_features(gambar2, 'orb')
    
    # Without cross-check + ratio test
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches_knn = bf.knnMatch(desc1, desc2, k=2)
    good_ratio = apply_ratio_test(matches_knn, RATIO_THRESHOLD)
    
    # With cross-check
    bf_cross = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches_cross = bf_cross.match(desc1, desc2)
    matches_cross = sorted(matches_cross, key=lambda x: x.distance)
    
    print(f"\nRatio Test: {len(good_ratio)} matches")
    print(f"Cross-Check: {len(matches_cross)} matches")
    
    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    img1 = cv2.drawMatches(
        gambar1, kp1, gambar2, kp2, good_ratio[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    img2 = cv2.drawMatches(
        gambar1, kp1, gambar2, kp2, matches_cross[:30], None,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    axes[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"Ratio Test (0.75)\n{len(good_ratio)} matches")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Cross-Check\n{len(matches_cross)} matches")
    axes[1].axis('off')
    
    plt.suptitle("Ratio Test vs Cross-Check Comparison", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: FEATURE MATCHING")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
FEATURE MATCHING adalah proses menemukan korespondensi
antara features di dua atau lebih gambar.

METODE MATCHING:

1. BRUTE-FORCE:
   └── Bandingkan setiap descriptor dengan semua descriptor lain

2. FLANN (Fast Library for Approximate NN):
   └── Gunakan indexing untuk pencarian lebih cepat

TEKNIK FILTERING:

1. RATIO TEST (Lowe's):
   └── Filter berdasarkan rasio best/second best match

2. CROSS-CHECK:
   └── Match harus mutual (A→B dan B→A)

3. DISTANCE THRESHOLD:
   └── Filter berdasarkan distance threshold

APLIKASI:
├── Image stitching (panorama)
├── Object recognition
├── Visual tracking
├── 3D reconstruction
└── Augmented Reality
    """)
    
    # Load gambar
    path1 = dapatkan_path_gambar(GAMBAR_1)
    path2 = dapatkan_path_gambar(GAMBAR_2)
    
    if os.path.exists(path1) and os.path.exists(path2):
        print(f"[INFO] Memuat gambar: {path1}")
        print(f"[INFO] Memuat gambar: {path2}")
        gambar1 = cv2.imread(path1)
        gambar2 = cv2.imread(path2)
    else:
        print("[INFO] Membuat gambar sample...")
        gambar1, gambar2 = buat_gambar_sample_pair()
    
    print(f"[INFO] Detector: {DETECTOR_TYPE}")
    print(f"[INFO] Matcher: {MATCHER_TYPE}")
    print(f"[INFO] Ratio Threshold: {RATIO_THRESHOLD}")
    
    # Feature detection
    print("\n[STEP 1] Feature Detection...")
    start = time.time()
    kp1, desc1 = detect_features(gambar1, DETECTOR_TYPE)
    kp2, desc2 = detect_features(gambar2, DETECTOR_TYPE)
    detect_time = (time.time() - start) * 1000
    
    print(f"   Gambar 1: {len(kp1)} keypoints")
    print(f"   Gambar 2: {len(kp2)} keypoints")
    print(f"   Waktu: {detect_time:.2f} ms")
    
    # Feature matching
    print("\n[STEP 2] Feature Matching...")
    start = time.time()
    
    if MATCHER_TYPE == 'bf':
        if BF_CROSS_CHECK:
            matches = brute_force_matching(desc1, desc2, DETECTOR_TYPE, True)
            good_matches = matches[:TOP_MATCHES]
        else:
            matches = brute_force_matching(desc1, desc2, DETECTOR_TYPE, False)
            good_matches = apply_ratio_test(matches, RATIO_THRESHOLD)
    else:
        matches = flann_matching(desc1, desc2, DETECTOR_TYPE)
        good_matches = apply_ratio_test(matches, RATIO_THRESHOLD)
    
    match_time = (time.time() - start) * 1000
    
    print(f"   Good matches: {len(good_matches)}")
    print(f"   Waktu: {match_time:.2f} ms")
    
    # Visualisasi hasil
    print("\n[STEP 3] Visualisasi...")
    
    img_matches = visualize_matches(gambar1, kp1, gambar2, kp2, good_matches)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
    plt.title(f"Feature Matching: {DETECTOR_TYPE.upper()} + {MATCHER_TYPE.upper()}\n"
              f"{len(good_matches)} matches (ratio={RATIO_THRESHOLD})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_ratio_test_effect()
    demo_bf_vs_flann()
    demo_cross_check()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN FEATURE MATCHING")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Brute-Force Matcher
bf = cv2.BFMatcher(cv2.NORM_L2)      # untuk SIFT
bf = cv2.BFMatcher(cv2.NORM_HAMMING) # untuk ORB/binary

# Cross-check
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(desc1, desc2)

# KNN Match untuk Ratio Test
matches = bf.knnMatch(desc1, desc2, k=2)

# FLANN Matcher
index_params = dict(algorithm=1, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc1, desc2, k=2)

# Lowe's Ratio Test
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

# Visualisasi
img = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)

TIPS:
1. ORB → gunakan NORM_HAMMING (binary descriptor)
2. SIFT → gunakan NORM_L2 (float descriptor)
3. Ratio 0.7-0.75 biasanya optimal
4. FLANN lebih cepat untuk dataset besar
5. Cross-check bagus jika tidak perlu banyak matches
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
