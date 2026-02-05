#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 2: STEREO RECTIFICATION
=============================================================================
Deskripsi:
    Program untuk melakukan stereo rectification - proses transformasi gambar
    stereo sehingga epipolar lines menjadi horizontal dan sejajar.

Konsep:
    - Epipolar geometry: titik di satu gambar berkorespondensi dengan garis
      (epipolar line) di gambar lainnya
    - Rectification: rotasi image plane agar epipolar lines horizontal
    - Setelah rectification, stereo matching menjadi 1D search problem
    
Manfaat Rectification:
    - Mempercepat stereo matching (hanya search horizontal)
    - Menghilangkan distorsi lensa
    - Menyamakan focal length dan principal point

Output:
    - Gambar rectified (left dan right)
    - Visualisasi epipolar lines
    - Perbandingan sebelum dan sesudah rectification

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
Dependensi: opencv-python, numpy
=============================================================================
"""

import cv2
import numpy as np
from pathlib import Path
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# =============================================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# =============================================================================

# Path ke gambar stereo
DATA_DIR = Path(__file__).parent / "data"
LEFT_IMAGE = DATA_DIR / "stereo" / "synthetic_left.png"
RIGHT_IMAGE = DATA_DIR / "stereo" / "synthetic_right.png"

# Path ke file kalibrasi (dari praktikum 01)
CALIB_FILE = DATA_DIR / "calibration_results" / "stereo_calibration.yaml"

# Path output
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "rectified"

# Warna untuk epipolar lines
EPIPOLAR_COLORS = [
    (0, 255, 0),    # Green
    (255, 0, 0),    # Blue
    (0, 0, 255),    # Red
    (255, 255, 0),  # Cyan
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Yellow
]

# Jumlah epipolar lines untuk visualisasi
NUM_EPIPOLAR_LINES = 10

# Auto-close settings
AUTO_CLOSE_SECONDS = 2

# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def load_calibration(calib_path):
    """
    Memuat parameter kalibrasi dari file YAML.
    
    Args:
        calib_path: Path ke file kalibrasi
        
    Returns:
        Dictionary dengan parameter kalibrasi
    """
    if not Path(calib_path).exists():
        print(f"[WARNING] File kalibrasi tidak ditemukan: {calib_path}")
        return None
    
    fs = cv2.FileStorage(str(calib_path), cv2.FILE_STORAGE_READ)
    
    calib = {
        'K1': fs.getNode('K1').mat(),
        'D1': fs.getNode('D1').mat(),
        'K2': fs.getNode('K2').mat(),
        'D2': fs.getNode('D2').mat(),
        'R': fs.getNode('R').mat(),
        'T': fs.getNode('T').mat(),
        'image_width': int(fs.getNode('image_width').real()),
        'image_height': int(fs.getNode('image_height').real())
    }
    
    # Cek jika parameter rectification sudah ada
    R1_node = fs.getNode('R1')
    if not R1_node.empty():
        calib['R1'] = R1_node.mat()
        calib['R2'] = fs.getNode('R2').mat()
        calib['P1'] = fs.getNode('P1').mat()
        calib['P2'] = fs.getNode('P2').mat()
        calib['Q'] = fs.getNode('Q').mat()
    
    fs.release()
    return calib


def compute_rectification_maps(calib, image_size):
    """
    Menghitung rectification maps dari parameter kalibrasi.
    
    Proses:
    1. stereoRectify() - menghitung matriks rotasi untuk rectification
    2. initUndistortRectifyMap() - membuat lookup table untuk remapping
    
    Args:
        calib: Dictionary parameter kalibrasi
        image_size: Tuple (width, height)
        
    Returns:
        Dictionary dengan maps dan parameter rectification
    """
    # Hitung parameter rectification
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        calib['K1'], calib['D1'],
        calib['K2'], calib['D2'],
        image_size,
        calib['R'], calib['T'],
        alpha=0,  # 0 = zoom in, 1 = keep all pixels
        newImageSize=image_size,
        flags=cv2.CALIB_ZERO_DISPARITY
    )
    
    # Buat lookup maps untuk remapping
    map1_left, map2_left = cv2.initUndistortRectifyMap(
        calib['K1'], calib['D1'], R1, P1, image_size, cv2.CV_32FC1
    )
    
    map1_right, map2_right = cv2.initUndistortRectifyMap(
        calib['K2'], calib['D2'], R2, P2, image_size, cv2.CV_32FC1
    )
    
    # Hitung baseline dari Q matrix
    # Q[3,2] = -1/Tx, sehingga baseline = -1/Q[3,2]
    baseline = 1.0 / Q[3, 2] if Q[3, 2] != 0 else 0
    
    # Focal length dari P1 (setelah rectification)
    focal = P1[0, 0]
    
    return {
        'R1': R1,
        'R2': R2,
        'P1': P1,
        'P2': P2,
        'Q': Q,
        'roi1': roi1,
        'roi2': roi2,
        'map_left': (map1_left, map2_left),
        'map_right': (map1_right, map2_right),
        'baseline': abs(baseline),
        'focal': focal
    }


def apply_rectification(img_left, img_right, rect_maps):
    """
    Menerapkan rectification ke gambar stereo.
    
    Args:
        img_left: Gambar kiri (BGR)
        img_right: Gambar kanan (BGR)
        rect_maps: Dictionary dari compute_rectification_maps()
        
    Returns:
        Tuple (rectified_left, rectified_right)
    """
    # Remap menggunakan lookup tables
    rect_left = cv2.remap(
        img_left,
        rect_maps['map_left'][0], rect_maps['map_left'][1],
        cv2.INTER_LINEAR
    )
    
    rect_right = cv2.remap(
        img_right,
        rect_maps['map_right'][0], rect_maps['map_right'][1],
        cv2.INTER_LINEAR
    )
    
    return rect_left, rect_right


def draw_epipolar_lines(img_left, img_right, num_lines=10):
    """
    Menggambar epipolar lines horizontal pada gambar stereo.
    
    Setelah rectification, semua epipolar lines harus horizontal.
    Ini berarti pixel di baris y pada gambar kiri berkorespondensi
    dengan pixel di baris y yang sama pada gambar kanan.
    
    Args:
        img_left: Gambar kiri (BGR)
        img_right: Gambar kanan (BGR)
        num_lines: Jumlah garis
        
    Returns:
        Gambar dengan epipolar lines
    """
    height = img_left.shape[0]
    
    # Copy gambar untuk visualisasi
    vis_left = img_left.copy()
    vis_right = img_right.copy()
    
    # Hitung posisi garis dengan spacing merata
    step = height // (num_lines + 1)
    
    for i in range(num_lines):
        y = step * (i + 1)
        color = EPIPOLAR_COLORS[i % len(EPIPOLAR_COLORS)]
        
        # Gambar garis horizontal
        cv2.line(vis_left, (0, y), (vis_left.shape[1], y), color, 1)
        cv2.line(vis_right, (0, y), (vis_right.shape[1], y), color, 1)
    
    # Gabungkan side by side
    combined = np.hstack([vis_left, vis_right])
    
    return combined


def visualize_before_after(orig_left, orig_right, rect_left, rect_right):
    """
    Membuat visualisasi perbandingan sebelum dan sesudah rectification.
    
    Args:
        orig_left, orig_right: Gambar original
        rect_left, rect_right: Gambar setelah rectification
        
    Returns:
        Gambar perbandingan
    """
    # Draw epipolar lines on both
    orig_combined = draw_epipolar_lines(orig_left, orig_right)
    rect_combined = draw_epipolar_lines(rect_left, rect_right)
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(orig_combined, "SEBELUM RECTIFICATION", 
                (10, 30), font, 0.8, (255, 255, 255), 2)
    cv2.putText(rect_combined, "SESUDAH RECTIFICATION", 
                (10, 30), font, 0.8, (255, 255, 255), 2)
    
    # Stack vertically
    comparison = np.vstack([orig_combined, rect_combined])
    
    return comparison


def validate_rectification(rect_left, rect_right):
    """
    Memvalidasi hasil rectification dengan menghitung y-disparity.
    
    Setelah rectification yang baik, matching points harus berada
    di baris yang sama (y-disparity = 0).
    
    Args:
        rect_left, rect_right: Gambar setelah rectification
        
    Returns:
        Dictionary dengan metrics validasi
    """
    gray_left = cv2.cvtColor(rect_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(rect_right, cv2.COLOR_BGR2GRAY)
    
    # Deteksi features
    orb = cv2.ORB_create(nfeatures=500)
    kp1, des1 = orb.detectAndCompute(gray_left, None)
    kp2, des2 = orb.detectAndCompute(gray_right, None)
    
    if des1 is None or des2 is None:
        return {'y_disparity_mean': float('nan'), 'y_disparity_std': float('nan')}
    
    # Match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Hitung y-disparity
    y_disparities = []
    for m in matches:
        y1 = kp1[m.queryIdx].pt[1]
        y2 = kp2[m.trainIdx].pt[1]
        y_disparities.append(abs(y1 - y2))
    
    if len(y_disparities) == 0:
        return {'y_disparity_mean': float('nan'), 'y_disparity_std': float('nan')}
    
    return {
        'y_disparity_mean': np.mean(y_disparities),
        'y_disparity_std': np.std(y_disparities),
        'num_matches': len(y_disparities)
    }


def create_synthetic_calibration(image_size):
    """
    Membuat parameter kalibrasi sintetis untuk demo.
    """
    width, height = image_size
    
    # Kamera dengan sedikit perbedaan (simulasi real stereo)
    K1 = np.array([
        [500, 0, width/2],
        [0, 500, height/2],
        [0, 0, 1]
    ], dtype=np.float64)
    
    K2 = np.array([
        [502, 0, width/2 + 2],  # Sedikit berbeda
        [0, 498, height/2 - 1],
        [0, 0, 1]
    ], dtype=np.float64)
    
    D1 = np.zeros(5, dtype=np.float64)
    D2 = np.zeros(5, dtype=np.float64)
    
    # Rotation: sedikit tilt
    R = cv2.Rodrigues(np.array([0.01, -0.02, 0.005]))[0]
    
    # Translation: baseline 120mm ke kanan
    T = np.array([[-120.0], [1.0], [0.5]], dtype=np.float64)
    
    return {
        'K1': K1, 'D1': D1,
        'K2': K2, 'D2': D2,
        'R': R, 'T': T,
        'image_width': width,
        'image_height': height
    }


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("STEREO RECTIFICATION")
    print("="*60)
    
    # Buat output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load gambar
    print("\n[STEP 1] Memuat gambar stereo...")
    
    img_left = cv2.imread(str(LEFT_IMAGE))
    img_right = cv2.imread(str(RIGHT_IMAGE))
    
    if img_left is None or img_right is None:
        print("[WARNING] Gambar tidak ditemukan. Membuat gambar sintetis...")
        
        # Buat gambar sintetis sederhana
        height, width = 480, 640
        img_left = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
        img_right = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
        
        # Tambah pattern untuk matching
        cv2.circle(img_left, (200, 200), 50, (255, 0, 0), -1)
        cv2.circle(img_right, (180, 202), 50, (255, 0, 0), -1)  # Shifted
        
        cv2.rectangle(img_left, (400, 300), (500, 400), (0, 255, 0), -1)
        cv2.rectangle(img_right, (370, 298), (470, 398), (0, 255, 0), -1)
    
    image_size = (img_left.shape[1], img_left.shape[0])
    print(f"Image size: {image_size}")
    
    # Load atau buat kalibrasi
    print("\n[STEP 2] Memuat parameter kalibrasi...")
    
    calib = load_calibration(CALIB_FILE)
    
    if calib is None:
        print("[INFO] Menggunakan kalibrasi sintetis untuk demo...")
        calib = create_synthetic_calibration(image_size)
    
    # Hitung rectification maps
    print("\n[STEP 3] Menghitung rectification maps...")
    rect_maps = compute_rectification_maps(calib, image_size)
    
    print(f"  - Baseline: {rect_maps['baseline']:.2f} mm")
    print(f"  - Focal length: {rect_maps['focal']:.2f} pixels")
    
    # Apply rectification
    print("\n[STEP 4] Menerapkan rectification...")
    rect_left, rect_right = apply_rectification(img_left, img_right, rect_maps)
    
    # Validate
    print("\n[STEP 5] Validasi hasil rectification...")
    validation = validate_rectification(rect_left, rect_right)
    
    print(f"  - Mean y-disparity: {validation['y_disparity_mean']:.3f} pixels")
    print(f"  - Std y-disparity: {validation['y_disparity_std']:.3f} pixels")
    if not np.isnan(validation['y_disparity_mean']):
        print(f"  - Number of matches: {validation['num_matches']}")
    
    if validation['y_disparity_mean'] < 1.0:
        print("  [OK] Rectification quality: EXCELLENT")
    elif validation['y_disparity_mean'] < 2.0:
        print("  [OK] Rectification quality: GOOD")
    else:
        print("  [WARNING] Rectification quality: POOR - cek kalibrasi")
    
    # Visualisasi
    print("\n[STEP 6] Membuat visualisasi...")
    
    # Simpan gambar rectified
    cv2.imwrite(str(OUTPUT_DIR / "rectified_left.png"), rect_left)
    cv2.imwrite(str(OUTPUT_DIR / "rectified_right.png"), rect_right)
    print(f"  - Saved: {OUTPUT_DIR / 'rectified_left.png'}")
    print(f"  - Saved: {OUTPUT_DIR / 'rectified_right.png'}")
    
    # Buat visualisasi perbandingan
    comparison = visualize_before_after(img_left, img_right, rect_left, rect_right)
    cv2.imwrite(str(OUTPUT_DIR / "rectification_comparison.png"), comparison)
    print(f"  - Saved: {OUTPUT_DIR / 'rectification_comparison.png'}")
    
    # Tampilkan
    print("\n[STEP 7] Menampilkan hasil...")
    
    # Resize jika terlalu besar
    max_width = 1200
    if comparison.shape[1] > max_width:
        scale = max_width / comparison.shape[1]
        comparison = cv2.resize(comparison, None, fx=scale, fy=scale)
    
    cv2.imshow("Rectification Comparison", comparison)
    
    # Epipolar lines visualization
    epipolar_vis = draw_epipolar_lines(rect_left, rect_right, NUM_EPIPOLAR_LINES)
    cv2.imshow("Epipolar Lines (Rectified)", epipolar_vis)
    
    print(f"\nAuto close dalam {AUTO_CLOSE_SECONDS} detik (tekan 'q' untuk keluar)...")
    cv2.waitKey(int(AUTO_CLOSE_SECONDS * 1000))
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] Stereo rectification selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")
    
    # Print Q matrix info
    print("\n" + "="*60)
    print("INFORMASI DISPARITY-TO-DEPTH (Q MATRIX)")
    print("="*60)
    print("Q matrix digunakan untuk konversi disparity ke 3D:")
    print("  [X]   [x]")
    print("  [Y] = Q * [y]")
    print("  [Z]   [d]")
    print("  [W]   [1]")
    print(f"\nQ matrix:\n{rect_maps['Q']}")


if __name__ == "__main__":
    main()
