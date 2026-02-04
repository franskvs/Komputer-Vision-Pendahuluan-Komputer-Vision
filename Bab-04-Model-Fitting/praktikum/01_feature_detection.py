# ============================================================
# PROGRAM: 01_feature_detection.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk feature detection (Harris, ORB, SIFT, AKAZE)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep feature detection
#   2. Perbandingan berbagai detector
#   3. Visualisasi keypoints
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

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Jenis Detector
# Opsi: 'harris', 'orb', 'sift', 'akaze', 'fast', 'all'
DETECTOR_TYPE = 'all'

# 3. Parameter Harris Corner Detector
HARRIS_BLOCK_SIZE = 2       # Ukuran neighborhood
HARRIS_KSIZE = 3            # Aperture parameter untuk Sobel
HARRIS_K = 0.04             # Harris detector free parameter
HARRIS_THRESHOLD = 0.01     # Threshold untuk corner response

# 4. Parameter ORB Detector
ORB_NFEATURES = 500         # Jumlah maksimum keypoints
ORB_SCALE_FACTOR = 1.2      # Pyramid decimation ratio
ORB_NLEVELS = 8             # Number of pyramid levels

# 5. Parameter SIFT Detector
SIFT_NFEATURES = 0          # 0 = semua features
SIFT_CONTRASTTHRESHOLD = 0.04
SIFT_EDGETHRESHOLD = 10

# 6. Parameter AKAZE Detector
AKAZE_THRESHOLD = 0.001     # Detector response threshold

# 7. Parameter FAST Detector
FAST_THRESHOLD = 20         # Threshold untuk FAST
FAST_NONMAX_SUPPRESSION = True

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


def buat_gambar_sample():
    """Membuat gambar sample dengan corner dan edges"""
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background gradient
    for i in range(400):
        for j in range(600):
            gambar[i, j] = [50 + j//6, 50, 50]
    
    # Shapes dengan corners
    cv2.rectangle(gambar, (50, 50), (200, 150), (255, 255, 255), 2)
    cv2.rectangle(gambar, (250, 50), (350, 180), (200, 200, 200), -1)
    cv2.circle(gambar, (480, 100), 50, (150, 200, 250), 2)
    cv2.fillPoly(gambar, [np.array([[400, 300], [500, 200], [550, 300]])], 
                 (100, 150, 200))
    
    # Checkerboard pattern (banyak corners)
    for i in range(5):
        for j in range(5):
            x = 60 + j * 30
            y = 220 + i * 30
            if (i + j) % 2 == 0:
                cv2.rectangle(gambar, (x, y), (x+30, y+30), (255, 255, 255), -1)
    
    # Text
    cv2.putText(gambar, "FEATURES", (320, 380), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return gambar


# ============================================================
# FUNGSI FEATURE DETECTION
# ============================================================

def harris_corner_detection(gambar, block_size=2, ksize=3, k=0.04, threshold=0.01):
    """
    Harris Corner Detection
    
    Mendeteksi corners (sudut) dalam gambar berdasarkan
    perubahan intensitas di kedua arah x dan y.
    
    Parameter:
    - block_size: ukuran neighborhood
    - ksize: aperture parameter untuk Sobel
    - k: Harris detector free parameter (0.04-0.06)
    - threshold: threshold untuk corner response
    
    Return:
    - keypoints: list of detected corners
    - response: corner response image
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    gray = np.float32(gray)
    
    # Harris corner detection
    dst = cv2.cornerHarris(gray, block_size, ksize, k)
    
    # Dilate untuk memperjelas corners
    dst = cv2.dilate(dst, None)
    
    # Threshold dan dapatkan corner coordinates
    corners = np.where(dst > threshold * dst.max())
    
    # Convert ke keypoints
    keypoints = [cv2.KeyPoint(float(x), float(y), 1) 
                 for y, x in zip(corners[0], corners[1])]
    
    return keypoints, dst


def orb_detection(gambar, nfeatures=500, scale_factor=1.2, nlevels=8):
    """
    ORB (Oriented FAST and Rotated BRIEF) Detection
    
    Detector cepat dan efisien, cocok untuk real-time applications.
    Kombinasi FAST detector dan BRIEF descriptor.
    
    Parameter:
    - nfeatures: jumlah maksimum keypoints
    - scale_factor: pyramid decimation ratio
    - nlevels: jumlah pyramid levels
    
    Return:
    - keypoints: detected keypoints
    - descriptors: feature descriptors
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Create ORB detector
    orb = cv2.ORB_create(
        nfeatures=nfeatures,
        scaleFactor=scale_factor,
        nlevels=nlevels
    )
    
    # Detect keypoints dan compute descriptors
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def sift_detection(gambar, nfeatures=0, contrast_threshold=0.04, edge_threshold=10):
    """
    SIFT (Scale-Invariant Feature Transform) Detection
    
    Robust terhadap scale dan rotation changes.
    Lebih lambat dari ORB tapi lebih akurat.
    
    Parameter:
    - nfeatures: jumlah maksimum keypoints (0 = semua)
    - contrast_threshold: threshold untuk filter low-contrast features
    - edge_threshold: threshold untuk filter edge-like features
    
    Return:
    - keypoints: detected keypoints
    - descriptors: feature descriptors (128-dim)
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Create SIFT detector
    sift = cv2.SIFT_create(
        nfeatures=nfeatures,
        contrastThreshold=contrast_threshold,
        edgeThreshold=edge_threshold
    )
    
    # Detect keypoints dan compute descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def akaze_detection(gambar, threshold=0.001):
    """
    AKAZE (Accelerated-KAZE) Detection
    
    Non-linear scale space untuk feature detection.
    Lebih akurat dari ORB untuk beberapa kasus.
    
    Parameter:
    - threshold: detector response threshold
    
    Return:
    - keypoints: detected keypoints
    - descriptors: feature descriptors
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Create AKAZE detector
    akaze = cv2.AKAZE_create(threshold=threshold)
    
    # Detect keypoints dan compute descriptors
    keypoints, descriptors = akaze.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def fast_detection(gambar, threshold=20, nonmax_suppression=True):
    """
    FAST (Features from Accelerated Segment Test) Detection
    
    Sangat cepat, cocok untuk real-time applications.
    Hanya detector, tidak ada descriptor.
    
    Parameter:
    - threshold: threshold untuk FAST
    - nonmax_suppression: whether to apply non-maximum suppression
    
    Return:
    - keypoints: detected keypoints
    """
    # Convert ke grayscale
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar.copy()
    
    # Create FAST detector
    fast = cv2.FastFeatureDetector_create(
        threshold=threshold,
        nonmaxSuppression=nonmax_suppression
    )
    
    # Detect keypoints
    keypoints = fast.detect(gray, None)
    
    return keypoints


def draw_keypoints_with_info(gambar, keypoints, detector_name, time_ms):
    """Menggambar keypoints dengan informasi"""
    output = gambar.copy()
    
    # Draw keypoints
    if detector_name.lower() == 'harris':
        # Untuk Harris, gambar sebagai circles
        output = cv2.drawKeypoints(gambar, keypoints, output, 
                                    color=(0, 255, 0),
                                    flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
    else:
        # Untuk detector lain, gambar dengan size dan orientation
        output = cv2.drawKeypoints(gambar, keypoints, output,
                                    color=(0, 255, 0),
                                    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Add text info
    info = f"{detector_name}: {len(keypoints)} keypoints, {time_ms:.1f}ms"
    cv2.putText(output, info, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return output


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_harris_parameter():
    """Demonstrasi pengaruh parameter Harris"""
    print("\n" + "=" * 60)
    print("PENGARUH PARAMETER HARRIS CORNER DETECTOR")
    print("=" * 60)
    
    print("""
PARAMETER HARRIS:

BLOCK_SIZE:
├── Ukuran neighborhood untuk gradient computation
├── Nilai kecil: lebih sensitif ke detail
└── Nilai besar: lebih smooth

KSIZE (Sobel Aperture):
├── Ukuran kernel Sobel untuk gradient
├── Nilai kecil: lebih detail
└── Nilai besar: lebih robust terhadap noise

K (Free Parameter):
├── Harris free parameter (biasanya 0.04-0.06)
├── Nilai kecil: lebih banyak corners
└── Nilai besar: lebih sedikit, tapi lebih robust

THRESHOLD:
├── Relative threshold untuk corner response
├── Nilai kecil: lebih banyak corners
└── Nilai besar: hanya strong corners
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Variasi block_size
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    block_sizes = [2, 3, 5]
    for i, bs in enumerate(block_sizes):
        kps, _ = harris_corner_detection(gambar, block_size=bs)
        output = draw_keypoints_with_info(gambar, kps, f"Harris (block={bs})", 0)
        axes[0, i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[0, i].set_title(f"block_size = {bs}\n{len(kps)} keypoints")
        axes[0, i].axis('off')
    
    # Variasi k
    ks = [0.02, 0.04, 0.06]
    for i, k in enumerate(ks):
        kps, _ = harris_corner_detection(gambar, k=k)
        output = draw_keypoints_with_info(gambar, kps, f"Harris (k={k})", 0)
        axes[1, i].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f"k = {k}\n{len(kps)} keypoints")
        axes[1, i].axis('off')
    
    plt.suptitle("Pengaruh Parameter pada Harris Corner Detection", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_detector_comparison():
    """Perbandingan berbagai feature detectors"""
    print("\n" + "=" * 60)
    print("PERBANDINGAN FEATURE DETECTORS")
    print("=" * 60)
    
    print("""
PERBANDINGAN:

| Detector | Speed     | Accuracy | Scale-Inv | Rotation-Inv |
|----------|-----------|----------|-----------|--------------|
| Harris   | Fast      | Low      | No        | Partial      |
| FAST     | Very Fast | Low      | No        | No           |
| ORB      | Fast      | Medium   | Yes       | Yes          |
| AKAZE    | Medium    | High     | Yes       | Yes          |
| SIFT     | Slow      | High     | Yes       | Yes          |
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    detectors = {
        'Harris': lambda: harris_corner_detection(gambar, HARRIS_BLOCK_SIZE, 
                                                   HARRIS_KSIZE, HARRIS_K, 
                                                   HARRIS_THRESHOLD),
        'FAST': lambda: (fast_detection(gambar, FAST_THRESHOLD), None),
        'ORB': lambda: orb_detection(gambar, ORB_NFEATURES),
        'AKAZE': lambda: akaze_detection(gambar, AKAZE_THRESHOLD),
        'SIFT': lambda: sift_detection(gambar, SIFT_NFEATURES)
    }
    
    results = {}
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Original
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original Image")
    axes[0].axis('off')
    
    for idx, (name, detect_func) in enumerate(detectors.items()):
        start = time.time()
        result = detect_func()
        elapsed = (time.time() - start) * 1000
        
        if name == 'Harris':
            kps, _ = result
        elif name == 'FAST':
            kps = result[0]
        else:
            kps, _ = result
        
        results[name] = {'keypoints': len(kps), 'time': elapsed}
        
        output = draw_keypoints_with_info(gambar, kps, name, elapsed)
        axes[idx + 1].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        axes[idx + 1].set_title(f"{name}\n{len(kps)} keypoints, {elapsed:.1f}ms")
        axes[idx + 1].axis('off')
    
    plt.suptitle("Perbandingan Feature Detectors", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\nSUMMARY:")
    print("-" * 50)
    for name, data in results.items():
        print(f"{name:10s}: {data['keypoints']:5d} keypoints, {data['time']:8.2f} ms")


def demo_scale_rotation():
    """Demo scale dan rotation invariance"""
    print("\n" + "=" * 60)
    print("SCALE DAN ROTATION INVARIANCE")
    print("=" * 60)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Resize gambar ke ukuran standard
    gambar = cv2.resize(gambar, (400, 300))
    
    # Create transformed versions
    # Scaled (0.5x)
    scaled = cv2.resize(gambar, None, fx=0.5, fy=0.5)
    
    # Rotated (45 degrees)
    h, w = gambar.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated = cv2.warpAffine(gambar, M, (w, h))
    
    # Detect with different detectors
    detectors = ['FAST', 'ORB', 'SIFT']
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    
    for i, detector in enumerate(detectors):
        for j, (img, name) in enumerate([(gambar, 'Original'), 
                                          (scaled, 'Scaled 0.5x'),
                                          (rotated, 'Rotated 45°')]):
            if detector == 'FAST':
                kps = fast_detection(img, FAST_THRESHOLD)
            elif detector == 'ORB':
                kps, _ = orb_detection(img, ORB_NFEATURES)
            else:
                kps, _ = sift_detection(img)
            
            output = cv2.drawKeypoints(img, kps, None, color=(0, 255, 0),
                                       flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            axes[i, j].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            axes[i, j].set_title(f"{detector} - {name}\n{len(kps)} keypoints")
            axes[i, j].axis('off')
    
    plt.suptitle("Scale dan Rotation Invariance Test", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: FEATURE DETECTION")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
FEATURE DETECTION adalah proses menemukan titik-titik
khusus (keypoints) dalam gambar yang memiliki karakteristik
unik dan dapat diidentifikasi kembali di gambar lain.

Karakteristik good features:
├── Repeatability: terdeteksi di berbagai kondisi
├── Distinctiveness: unik dan dapat dibedakan
├── Locality: lokal, tidak terpengaruh oleh area lain
└── Quantity: cukup banyak untuk matching

Aplikasi:
├── Image matching & stitching
├── Object recognition
├── Visual SLAM
├── Augmented Reality
└── 3D reconstruction
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Membuat gambar sample...")
        gambar = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Detector Type: {DETECTOR_TYPE}")
    
    # Detect features berdasarkan pilihan
    if DETECTOR_TYPE == 'all':
        demo_detector_comparison()
    else:
        start = time.time()
        
        if DETECTOR_TYPE == 'harris':
            kps, response = harris_corner_detection(
                gambar, HARRIS_BLOCK_SIZE, HARRIS_KSIZE, 
                HARRIS_K, HARRIS_THRESHOLD
            )
        elif DETECTOR_TYPE == 'fast':
            kps = fast_detection(gambar, FAST_THRESHOLD, FAST_NONMAX_SUPPRESSION)
        elif DETECTOR_TYPE == 'orb':
            kps, desc = orb_detection(gambar, ORB_NFEATURES, 
                                       ORB_SCALE_FACTOR, ORB_NLEVELS)
        elif DETECTOR_TYPE == 'sift':
            kps, desc = sift_detection(gambar, SIFT_NFEATURES,
                                        SIFT_CONTRASTTHRESHOLD, 
                                        SIFT_EDGETHRESHOLD)
        elif DETECTOR_TYPE == 'akaze':
            kps, desc = akaze_detection(gambar, AKAZE_THRESHOLD)
        
        elapsed = (time.time() - start) * 1000
        
        print(f"[INFO] Detected {len(kps)} keypoints in {elapsed:.2f} ms")
        
        # Visualisasi
        output = draw_keypoints_with_info(gambar, kps, DETECTOR_TYPE.upper(), elapsed)
        
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        plt.title(f"{DETECTOR_TYPE.upper()} Feature Detection")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    # Demo tambahan
    demo_harris_parameter()
    demo_scale_rotation()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN FEATURE DETECTION")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Harris Corner
dst = cv2.cornerHarris(gray, blockSize, ksize, k)

# FAST
fast = cv2.FastFeatureDetector_create(threshold=20)
keypoints = fast.detect(gray, None)

# ORB
orb = cv2.ORB_create(nfeatures=500)
keypoints, descriptors = orb.detectAndCompute(gray, None)

# SIFT
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)

# AKAZE
akaze = cv2.AKAZE_create(threshold=0.001)
keypoints, descriptors = akaze.detectAndCompute(gray, None)

# Visualisasi
output = cv2.drawKeypoints(img, keypoints, None, 
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

PEMILIHAN DETECTOR:
├── Real-time: FAST atau ORB
├── Akurasi tinggi: SIFT atau AKAZE
├── Balance: ORB atau AKAZE
└── Simple corners: Harris

TIPS:
1. SIFT lebih robust tapi lambat
2. ORB bagus untuk real-time dengan akurasi cukup
3. Harris cocok untuk simple corner detection
4. AKAZE bagus untuk textureless regions
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
