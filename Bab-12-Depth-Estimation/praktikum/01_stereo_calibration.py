#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 1: STEREO CAMERA CALIBRATION
=============================================================================
Deskripsi:
    Program untuk mengkalibrasi sistem stereo camera menggunakan checkerboard
    pattern. Menghasilkan parameter intrinsik, extrinsik, dan distortion
    coefficients untuk kedua kamera.

Konsep:
    - Camera calibration menggunakan checkerboard
    - Stereo calibration untuk mendapatkan relative pose
    - Parameter intrinsik: focal length, principal point
    - Parameter extrinsik: rotation dan translation antar kamera

Output:
    - Parameter kalibrasi dalam format YAML
    - Reprojection error untuk validasi
    - Visualisasi hasil deteksi corner

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
Dependensi: opencv-python, numpy
=============================================================================
"""

import cv2
import numpy as np
from pathlib import Path
import glob

# =============================================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# =============================================================================

# Ukuran checkerboard (jumlah inner corners)
# Contoh: checkerboard 10x7 kotak memiliki 9x6 inner corners
CHECKERBOARD_SIZE = (9, 6)  # (columns, rows)

# Ukuran setiap kotak dalam mm (atau unit yang konsisten)
SQUARE_SIZE = 25.0  # mm

# Path ke folder gambar kalibrasi
# Gambar left harus bernama: left_*.png atau left_*.jpg
# Gambar right harus bernama: right_*.png atau right_*.jpg
CALIB_IMAGES_DIR = Path(__file__).parent.parent / "data" / "calibration"

# Path untuk menyimpan hasil kalibrasi
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "calibration_results"

# Flag untuk menampilkan corner detection
SHOW_CORNERS = True

# Kriteria terminasi untuk corner refinement
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def create_object_points(checkerboard_size, square_size, num_images):
    """
    Membuat object points untuk checkerboard.
    
    Object points adalah koordinat 3D dari corner checkerboard dalam
    world coordinate system. Kita asumsikan checkerboard berada di Z=0.
    
    Args:
        checkerboard_size: Tuple (columns, rows) inner corners
        square_size: Ukuran kotak dalam mm
        num_images: Jumlah gambar kalibrasi
        
    Returns:
        List of object points arrays
    """
    # Membuat grid koordinat untuk satu checkerboard
    objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard_size[0], 
                           0:checkerboard_size[1]].T.reshape(-1, 2)
    objp *= square_size
    
    # Duplicate untuk setiap gambar
    return [objp.copy() for _ in range(num_images)]


def find_checkerboard_corners(image_paths, checkerboard_size, show=False):
    """
    Mencari corner checkerboard di semua gambar.
    
    Args:
        image_paths: List of image file paths
        checkerboard_size: Tuple (columns, rows)
        show: Boolean untuk menampilkan hasil
        
    Returns:
        Tuple (image_points, valid_images, image_size)
    """
    image_points = []
    valid_images = []
    image_size = None
    
    for img_path in image_paths:
        # Baca gambar
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"[WARNING] Tidak bisa membaca: {img_path}")
            continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Simpan ukuran gambar
        if image_size is None:
            image_size = gray.shape[::-1]
        
        # Cari corner
        ret, corners = cv2.findChessboardCorners(
            gray, checkerboard_size,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
        )
        
        if ret:
            # Refine corner positions
            corners_refined = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), CRITERIA
            )
            image_points.append(corners_refined)
            valid_images.append(img_path)
            
            if show:
                # Draw corners untuk visualisasi
                vis = img.copy()
                cv2.drawChessboardCorners(vis, checkerboard_size, 
                                         corners_refined, ret)
                cv2.imshow(f'Corners: {Path(img_path).name}', vis)
                cv2.waitKey(500)
        else:
            print(f"[WARNING] Corner tidak ditemukan: {img_path}")
    
    if show:
        cv2.destroyAllWindows()
    
    return image_points, valid_images, image_size


def calibrate_single_camera(object_points, image_points, image_size):
    """
    Kalibrasi single camera.
    
    Args:
        object_points: List of 3D points
        image_points: List of 2D points
        image_size: Tuple (width, height)
        
    Returns:
        Dictionary with calibration results
    """
    # Perform calibration
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        object_points, image_points, image_size, None, None
    )
    
    # Hitung reprojection error
    total_error = 0
    for i in range(len(object_points)):
        img_points2, _ = cv2.projectPoints(
            object_points[i], rvecs[i], tvecs[i], 
            camera_matrix, dist_coeffs
        )
        error = cv2.norm(image_points[i], img_points2, cv2.NORM_L2)
        total_error += error ** 2
    
    mean_error = np.sqrt(total_error / len(object_points))
    
    return {
        'camera_matrix': camera_matrix,
        'dist_coeffs': dist_coeffs,
        'rvecs': rvecs,
        'tvecs': tvecs,
        'rms_error': ret,
        'mean_reprojection_error': mean_error
    }


def calibrate_stereo(object_points, img_points_left, img_points_right,
                     camera_matrix_left, dist_left, 
                     camera_matrix_right, dist_right, image_size):
    """
    Kalibrasi stereo camera untuk mendapatkan relative pose.
    
    Args:
        object_points: List of 3D points
        img_points_left: List of 2D points kamera kiri
        img_points_right: List of 2D points kamera kanan
        camera_matrix_left, dist_left: Parameter kamera kiri
        camera_matrix_right, dist_right: Parameter kamera kanan
        image_size: Tuple (width, height)
        
    Returns:
        Dictionary with stereo calibration results
    """
    # Flags untuk stereo calibration
    # CALIB_FIX_INTRINSIC: menggunakan intrinsic yang sudah ada
    flags = cv2.CALIB_FIX_INTRINSIC
    
    ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(
        object_points,
        img_points_left, img_points_right,
        camera_matrix_left, dist_left,
        camera_matrix_right, dist_right,
        image_size,
        criteria=CRITERIA,
        flags=flags
    )
    
    return {
        'R': R,           # Rotation matrix dari kamera kiri ke kanan
        'T': T,           # Translation vector dari kamera kiri ke kanan
        'E': E,           # Essential matrix
        'F': F,           # Fundamental matrix
        'rms_error': ret,
        'baseline': np.linalg.norm(T)  # Jarak antar kamera
    }


def compute_rectification(K1, D1, K2, D2, R, T, image_size):
    """
    Menghitung parameter rectification untuk stereo.
    
    Rectification membuat kedua image plane coplanar sehingga
    epipolar lines menjadi horizontal.
    
    Args:
        K1, D1: Parameter kamera kiri
        K2, D2: Parameter kamera kanan
        R, T: Relative pose
        image_size: Tuple (width, height)
        
    Returns:
        Dictionary with rectification parameters
    """
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        K1, D1, K2, D2, image_size, R, T,
        alpha=0,  # 0 = crop, 1 = keep all pixels
        newImageSize=image_size
    )
    
    # Compute undistort+rectify maps
    map1_left, map2_left = cv2.initUndistortRectifyMap(
        K1, D1, R1, P1, image_size, cv2.CV_32FC1
    )
    map1_right, map2_right = cv2.initUndistortRectifyMap(
        K2, D2, R2, P2, image_size, cv2.CV_32FC1
    )
    
    return {
        'R1': R1,
        'R2': R2,
        'P1': P1,
        'P2': P2,
        'Q': Q,  # Disparity-to-depth mapping matrix
        'roi1': roi1,
        'roi2': roi2,
        'map_left': (map1_left, map2_left),
        'map_right': (map1_right, map2_right)
    }


def save_calibration_yaml(output_path, calib_data):
    """
    Menyimpan hasil kalibrasi ke file YAML menggunakan OpenCV.
    
    Args:
        output_path: Path file output
        calib_data: Dictionary dengan parameter kalibrasi
    """
    fs = cv2.FileStorage(str(output_path), cv2.FILE_STORAGE_WRITE)
    
    for key, value in calib_data.items():
        if isinstance(value, np.ndarray):
            fs.write(key, value)
        elif isinstance(value, (int, float)):
            fs.write(key, value)
        elif isinstance(value, tuple) and len(value) == 2:
            fs.write(key, np.array(value))
    
    fs.release()
    print(f"[OK] Kalibrasi disimpan ke: {output_path}")


def print_calibration_results(left_calib, right_calib, stereo_calib):
    """Menampilkan hasil kalibrasi dengan format yang rapi"""
    
    print("\n" + "="*60)
    print("HASIL KALIBRASI STEREO")
    print("="*60)
    
    print("\n[KAMERA KIRI]")
    print("-"*40)
    K = left_calib['camera_matrix']
    print(f"Focal Length (fx, fy): ({K[0,0]:.2f}, {K[1,1]:.2f}) pixels")
    print(f"Principal Point (cx, cy): ({K[0,2]:.2f}, {K[1,2]:.2f}) pixels")
    print(f"RMS Reprojection Error: {left_calib['rms_error']:.4f} pixels")
    
    print("\n[KAMERA KANAN]")
    print("-"*40)
    K = right_calib['camera_matrix']
    print(f"Focal Length (fx, fy): ({K[0,0]:.2f}, {K[1,1]:.2f}) pixels")
    print(f"Principal Point (cx, cy): ({K[0,2]:.2f}, {K[1,2]:.2f}) pixels")
    print(f"RMS Reprojection Error: {right_calib['rms_error']:.4f} pixels")
    
    print("\n[STEREO]")
    print("-"*40)
    print(f"Baseline: {stereo_calib['baseline']:.2f} mm")
    print(f"Stereo RMS Error: {stereo_calib['rms_error']:.4f} pixels")
    print(f"\nRotation Matrix:")
    print(stereo_calib['R'])
    print(f"\nTranslation Vector:")
    print(stereo_calib['T'].flatten())


def demo_with_synthetic_images():
    """
    Demo menggunakan gambar sintetis jika gambar real tidak tersedia.
    """
    print("\n[INFO] Menjalankan demo dengan gambar sintetis...")
    
    # Generate synthetic checkerboard images
    num_images = 10
    image_size = (640, 480)
    
    # Synthetic camera parameters
    K_true = np.array([
        [500, 0, 320],
        [0, 500, 240],
        [0, 0, 1]
    ], dtype=np.float64)
    
    D_true = np.zeros(5)
    
    # Generate object points
    objp = np.zeros((CHECKERBOARD_SIZE[0] * CHECKERBOARD_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD_SIZE[0], 
                           0:CHECKERBOARD_SIZE[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE
    
    object_points = []
    img_points_left = []
    img_points_right = []
    
    np.random.seed(42)
    
    for i in range(num_images):
        # Random rotation and translation
        rvec = np.random.uniform(-0.3, 0.3, 3)
        tvec = np.array([
            np.random.uniform(-50, 50),
            np.random.uniform(-50, 50),
            np.random.uniform(200, 400)
        ])
        
        # Project to left camera
        pts_left, _ = cv2.projectPoints(objp, rvec, tvec, K_true, D_true)
        
        # Stereo: right camera is shifted
        baseline = 120.0  # mm
        tvec_right = tvec.copy()
        tvec_right[0] -= baseline
        
        pts_right, _ = cv2.projectPoints(objp, rvec, tvec_right, K_true, D_true)
        
        # Check if all points are within image
        if (pts_left.min() > 10 and pts_left[:,:,0].max() < image_size[0] - 10 and
            pts_left[:,:,1].max() < image_size[1] - 10 and
            pts_right.min() > 10 and pts_right[:,:,0].max() < image_size[0] - 10 and
            pts_right[:,:,1].max() < image_size[1] - 10):
            
            object_points.append(objp)
            img_points_left.append(pts_left.reshape(-1, 1, 2).astype(np.float32))
            img_points_right.append(pts_right.reshape(-1, 1, 2).astype(np.float32))
    
    print(f"[INFO] Generated {len(object_points)} valid synthetic image pairs")
    
    # Calibrate left camera
    print("\n[STEP 1] Kalibrasi kamera kiri...")
    left_calib = calibrate_single_camera(object_points, img_points_left, image_size)
    
    # Calibrate right camera
    print("[STEP 2] Kalibrasi kamera kanan...")
    right_calib = calibrate_single_camera(object_points, img_points_right, image_size)
    
    # Stereo calibration
    print("[STEP 3] Kalibrasi stereo...")
    stereo_calib = calibrate_stereo(
        object_points, img_points_left, img_points_right,
        left_calib['camera_matrix'], left_calib['dist_coeffs'],
        right_calib['camera_matrix'], right_calib['dist_coeffs'],
        image_size
    )
    
    # Print results
    print_calibration_results(left_calib, right_calib, stereo_calib)
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    calib_data = {
        'K1': left_calib['camera_matrix'],
        'D1': left_calib['dist_coeffs'],
        'K2': right_calib['camera_matrix'],
        'D2': right_calib['dist_coeffs'],
        'R': stereo_calib['R'],
        'T': stereo_calib['T'],
        'E': stereo_calib['E'],
        'F': stereo_calib['F'],
        'image_width': image_size[0],
        'image_height': image_size[1]
    }
    
    save_calibration_yaml(OUTPUT_DIR / "stereo_calibration.yaml", calib_data)
    
    return left_calib, right_calib, stereo_calib


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("STEREO CAMERA CALIBRATION")
    print("="*60)
    print(f"Checkerboard Size: {CHECKERBOARD_SIZE}")
    print(f"Square Size: {SQUARE_SIZE} mm")
    print(f"Calibration Images: {CALIB_IMAGES_DIR}")
    
    # Check for real images
    left_images = sorted(glob.glob(str(CALIB_IMAGES_DIR / "left_*.png")))
    left_images += sorted(glob.glob(str(CALIB_IMAGES_DIR / "left_*.jpg")))
    
    right_images = sorted(glob.glob(str(CALIB_IMAGES_DIR / "right_*.png")))
    right_images += sorted(glob.glob(str(CALIB_IMAGES_DIR / "right_*.jpg")))
    
    if len(left_images) < 3 or len(right_images) < 3:
        print("\n[WARNING] Tidak cukup gambar kalibrasi ditemukan.")
        print("Menjalankan demo dengan data sintetis...")
        demo_with_synthetic_images()
        return
    
    print(f"\n[INFO] Ditemukan {len(left_images)} gambar kiri, {len(right_images)} gambar kanan")
    
    # Find corners
    print("\n[STEP 1] Mencari corner di gambar kiri...")
    img_points_left, valid_left, image_size = find_checkerboard_corners(
        left_images, CHECKERBOARD_SIZE, SHOW_CORNERS
    )
    
    print(f"\n[STEP 2] Mencari corner di gambar kanan...")
    img_points_right, valid_right, _ = find_checkerboard_corners(
        right_images, CHECKERBOARD_SIZE, SHOW_CORNERS
    )
    
    # Match pairs
    valid_pairs = min(len(img_points_left), len(img_points_right))
    print(f"\n[INFO] Valid pairs: {valid_pairs}")
    
    if valid_pairs < 3:
        print("[ERROR] Tidak cukup pasangan gambar yang valid!")
        return
    
    # Create object points
    object_points = create_object_points(CHECKERBOARD_SIZE, SQUARE_SIZE, valid_pairs)
    
    # Calibrate
    print("\n[STEP 3] Kalibrasi kamera kiri...")
    left_calib = calibrate_single_camera(
        object_points, img_points_left[:valid_pairs], image_size
    )
    
    print("[STEP 4] Kalibrasi kamera kanan...")
    right_calib = calibrate_single_camera(
        object_points, img_points_right[:valid_pairs], image_size
    )
    
    print("[STEP 5] Kalibrasi stereo...")
    stereo_calib = calibrate_stereo(
        object_points,
        img_points_left[:valid_pairs], img_points_right[:valid_pairs],
        left_calib['camera_matrix'], left_calib['dist_coeffs'],
        right_calib['camera_matrix'], right_calib['dist_coeffs'],
        image_size
    )
    
    # Compute rectification
    print("[STEP 6] Menghitung parameter rectification...")
    rect_params = compute_rectification(
        left_calib['camera_matrix'], left_calib['dist_coeffs'],
        right_calib['camera_matrix'], right_calib['dist_coeffs'],
        stereo_calib['R'], stereo_calib['T'],
        image_size
    )
    
    # Print results
    print_calibration_results(left_calib, right_calib, stereo_calib)
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    calib_data = {
        'K1': left_calib['camera_matrix'],
        'D1': left_calib['dist_coeffs'],
        'K2': right_calib['camera_matrix'],
        'D2': right_calib['dist_coeffs'],
        'R': stereo_calib['R'],
        'T': stereo_calib['T'],
        'E': stereo_calib['E'],
        'F': stereo_calib['F'],
        'R1': rect_params['R1'],
        'R2': rect_params['R2'],
        'P1': rect_params['P1'],
        'P2': rect_params['P2'],
        'Q': rect_params['Q'],
        'image_width': image_size[0],
        'image_height': image_size[1]
    }
    
    save_calibration_yaml(OUTPUT_DIR / "stereo_calibration.yaml", calib_data)
    
    print("\n[SUCCESS] Kalibrasi selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
