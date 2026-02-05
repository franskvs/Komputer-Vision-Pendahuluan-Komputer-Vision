#!/usr/bin/env python3
"""
=============================================================================
DOWNLOAD SAMPLE DATA - BAB 12: DEPTH ESTIMATION
=============================================================================
Deskripsi:
    Script untuk mendownload data sampel untuk praktikum Depth Estimation.
    Termasuk gambar stereo, dataset Middlebury, dan gambar untuk testing.

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
=============================================================================
"""

import os
import urllib.request
import zipfile
import shutil
from pathlib import Path
import hashlib

# =============================================================================
# KONFIGURASI
# =============================================================================

# Direktori output
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
STEREO_DIR = DATA_DIR / "stereo"
CALIBRATION_DIR = DATA_DIR / "calibration"
VIDEOS_DIR = DATA_DIR / "videos"

# URLs untuk sample data
SAMPLE_DATA_URLS = {
    # Middlebury stereo samples
    "tsukuba_left": "https://vision.middlebury.edu/stereo/data/scenes2005/FullSize/Tsukuba/view1.png",
    "tsukuba_right": "https://vision.middlebury.edu/stereo/data/scenes2005/FullSize/Tsukuba/view5.png",
    "tsukuba_disp": "https://vision.middlebury.edu/stereo/data/scenes2005/FullSize/Tsukuba/disp1.png",
}

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

def create_directories():
    """Membuat struktur direktori yang diperlukan"""
    directories = [DATA_DIR, IMAGES_DIR, STEREO_DIR, CALIBRATION_DIR, VIDEOS_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Direktori siap: {directory}")

def download_file(url, destination, description=""):
    """Download file dari URL dengan progress indicator"""
    try:
        print(f"[DOWNLOADING] {description or url}")
        
        # Custom opener dengan user agent
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(url, destination)
        print(f"[OK] Downloaded: {destination}")
        return True
    except Exception as e:
        print(f"[ERROR] Gagal download {url}: {e}")
        return False

def create_synthetic_stereo_pair():
    """Membuat pasangan gambar stereo sintetis jika download gagal"""
    try:
        import numpy as np
        import cv2
        
        print("\n[INFO] Membuat gambar stereo sintetis...")
        
        # Buat scene sintetis dengan objek 3D
        width, height = 640, 480
        baseline = 0.1  # 10cm baseline
        focal = 500  # focal length in pixels
        
        # Background gradient
        left_img = np.zeros((height, width, 3), dtype=np.uint8)
        right_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(height):
            left_img[y, :] = [100 + y//4, 80, 60]
            right_img[y, :] = [100 + y//4, 80, 60]
        
        # Draw objects at different depths
        objects = [
            # (center_x, center_y, depth_meters, radius, color)
            (160, 240, 2.0, 50, (255, 0, 0)),    # Blue sphere at 2m
            (320, 200, 4.0, 70, (0, 255, 0)),    # Green sphere at 4m
            (480, 280, 3.0, 40, (0, 0, 255)),    # Red sphere at 3m
            (400, 350, 5.0, 60, (255, 255, 0)),  # Cyan sphere at 5m
            (200, 350, 1.5, 35, (255, 0, 255)),  # Magenta sphere at 1.5m
        ]
        
        for cx, cy, depth, radius, color in objects:
            # Calculate disparity
            disparity = (focal * baseline) / depth
            
            # Draw on left image
            cv2.circle(left_img, (cx, cy), radius, color, -1)
            cv2.circle(left_img, (cx, cy), radius, (200, 200, 200), 2)
            
            # Draw on right image (shifted by disparity)
            cx_right = int(cx - disparity)
            if 0 < cx_right < width:
                cv2.circle(right_img, (cx_right, cy), radius, color, -1)
                cv2.circle(right_img, (cx_right, cy), radius, (200, 200, 200), 2)
        
        # Add texture to background
        np.random.seed(42)
        noise = np.random.randint(0, 20, (height, width, 3), dtype=np.uint8)
        left_img = cv2.add(left_img, noise)
        right_img = cv2.add(right_img, noise)
        
        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(left_img, "LEFT", (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(right_img, "RIGHT", (10, 30), font, 1, (255, 255, 255), 2)
        
        # Save images
        cv2.imwrite(str(STEREO_DIR / "synthetic_left.png"), left_img)
        cv2.imwrite(str(STEREO_DIR / "synthetic_right.png"), right_img)
        
        print(f"[OK] Gambar stereo sintetis disimpan di {STEREO_DIR}")
        
        # Create ground truth disparity
        disp_gt = np.zeros((height, width), dtype=np.float32)
        for cx, cy, depth, radius, color in objects:
            disparity = (focal * baseline) / depth
            cv2.circle(disp_gt, (cx, cy), radius, disparity, -1)
        
        # Normalize dan save
        disp_vis = cv2.normalize(disp_gt, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        cv2.imwrite(str(STEREO_DIR / "synthetic_disp_gt.png"), disp_vis)
        
        # Save camera parameters
        camera_params = f"""# Camera Parameters for Synthetic Stereo
# Format: YAML-like
focal_length: {focal}
baseline: {baseline}
image_width: {width}
image_height: {height}
cx: {width/2}
cy: {height/2}
"""
        with open(STEREO_DIR / "camera_params.txt", "w") as f:
            f.write(camera_params)
        
        print("[OK] Ground truth disparity dan parameter kamera disimpan")
        return True
        
    except ImportError:
        print("[WARNING] OpenCV tidak tersedia, tidak bisa membuat gambar sintetis")
        return False

def create_calibration_images():
    """Membuat gambar checkerboard sintetis untuk kalibrasi"""
    try:
        import numpy as np
        import cv2
        
        print("\n[INFO] Membuat gambar kalibrasi...")
        
        # Checkerboard parameters
        rows, cols = 6, 9
        square_size = 30  # pixels
        
        # Create checkerboard
        board_width = cols * square_size
        board_height = rows * square_size
        
        checkerboard = np.zeros((board_height, board_width), dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    y1, y2 = i * square_size, (i + 1) * square_size
                    x1, x2 = j * square_size, (j + 1) * square_size
                    checkerboard[y1:y2, x1:x2] = 255
        
        # Create multiple views
        for idx in range(5):
            # Random rotation and translation
            np.random.seed(idx)
            angle = np.random.uniform(-20, 20)
            scale = np.random.uniform(0.8, 1.2)
            tx = np.random.uniform(-50, 50)
            ty = np.random.uniform(-50, 50)
            
            # Create canvas
            canvas = np.ones((480, 640), dtype=np.uint8) * 200
            
            # Transform checkerboard
            M = cv2.getRotationMatrix2D((board_width//2, board_height//2), angle, scale)
            M[0, 2] += 320 - board_width//2 + tx
            M[1, 2] += 240 - board_height//2 + ty
            
            transformed = cv2.warpAffine(checkerboard, M, (640, 480), 
                                         borderValue=200)
            
            # Save
            filename = f"checkerboard_{idx+1:02d}.png"
            cv2.imwrite(str(CALIBRATION_DIR / filename), transformed)
        
        print(f"[OK] {5} gambar kalibrasi disimpan di {CALIBRATION_DIR}")
        return True
        
    except ImportError:
        print("[WARNING] OpenCV tidak tersedia")
        return False

def create_sample_single_image():
    """Membuat gambar untuk monocular depth estimation"""
    try:
        import numpy as np
        import cv2
        
        print("\n[INFO] Membuat gambar sampel untuk monocular depth...")
        
        width, height = 640, 480
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky gradient
        for y in range(height // 3):
            blue = 255 - y
            img[y, :] = [blue, 200, 150]
        
        # Ground plane with texture
        for y in range(height // 3, height):
            ratio = (y - height // 3) / (2 * height // 3)
            green = int(50 + 100 * (1 - ratio))
            img[y, :] = [50, green, 30]
        
        # Add road
        road_width_top = 80
        road_width_bottom = 400
        pts = np.array([
            [width//2 - road_width_top//2, height//3],
            [width//2 + road_width_top//2, height//3],
            [width//2 + road_width_bottom//2, height],
            [width//2 - road_width_bottom//2, height]
        ], np.int32)
        cv2.fillPoly(img, [pts], (100, 100, 100))
        
        # Add buildings
        building_colors = [(80, 80, 120), (100, 90, 80), (70, 100, 110)]
        for i, x in enumerate([50, 550]):
            color = building_colors[i % len(building_colors)]
            building_width = 100
            building_height = 200
            y_bottom = height // 3
            cv2.rectangle(img, (x, y_bottom - building_height), 
                         (x + building_width, y_bottom), color, -1)
            # Windows
            for wy in range(y_bottom - building_height + 20, y_bottom - 20, 40):
                for wx in range(x + 15, x + building_width - 15, 30):
                    cv2.rectangle(img, (wx, wy), (wx + 15, wy + 25), (200, 200, 150), -1)
        
        # Add car
        car_y = height - 100
        car_x = width // 2 - 40
        cv2.rectangle(img, (car_x, car_y), (car_x + 80, car_y + 40), (0, 0, 180), -1)
        cv2.rectangle(img, (car_x + 15, car_y - 25), (car_x + 65, car_y), (0, 0, 150), -1)
        cv2.circle(img, (car_x + 15, car_y + 40), 12, (30, 30, 30), -1)
        cv2.circle(img, (car_x + 65, car_y + 40), 12, (30, 30, 30), -1)
        
        # Add sun
        cv2.circle(img, (550, 50), 40, (0, 255, 255), -1)
        
        # Save
        cv2.imwrite(str(IMAGES_DIR / "street_scene.png"), img)
        print(f"[OK] Gambar street scene disimpan")
        
        return True
        
    except ImportError:
        print("[WARNING] OpenCV tidak tersedia")
        return False

def download_middlebury_samples():
    """Download sample dari Middlebury stereo dataset"""
    print("\n[INFO] Mencoba download sampel Middlebury...")
    
    for name, url in SAMPLE_DATA_URLS.items():
        destination = STEREO_DIR / f"{name}.png"
        success = download_file(url, destination, f"Middlebury {name}")
        
        if not success:
            print(f"[WARNING] Gagal download {name}")

def verify_data():
    """Verifikasi data yang sudah didownload"""
    print("\n" + "="*60)
    print("VERIFIKASI DATA")
    print("="*60)
    
    all_files = []
    
    # Check stereo images
    stereo_files = list(STEREO_DIR.glob("*.png"))
    print(f"\n[STEREO] {len(stereo_files)} files:")
    for f in stereo_files:
        print(f"  - {f.name}")
        all_files.append(f)
    
    # Check calibration images
    calib_files = list(CALIBRATION_DIR.glob("*.png"))
    print(f"\n[CALIBRATION] {len(calib_files)} files:")
    for f in calib_files:
        print(f"  - {f.name}")
        all_files.append(f)
    
    # Check single images
    image_files = list(IMAGES_DIR.glob("*.png")) + list(IMAGES_DIR.glob("*.jpg"))
    print(f"\n[IMAGES] {len(image_files)} files:")
    for f in image_files:
        print(f"  - {f.name}")
        all_files.append(f)
    
    print("\n" + "="*60)
    print(f"TOTAL: {len(all_files)} files downloaded")
    print("="*60)
    
    return len(all_files) > 0

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*60)
    print("DOWNLOAD SAMPLE DATA - BAB 12: DEPTH ESTIMATION")
    print("="*60)
    
    # Step 1: Create directories
    print("\n[STEP 1] Membuat struktur direktori...")
    create_directories()
    
    # Step 2: Try to download Middlebury samples
    print("\n[STEP 2] Download sampel Middlebury...")
    download_middlebury_samples()
    
    # Step 3: Create synthetic data (always create as backup)
    print("\n[STEP 3] Membuat data sintetis...")
    create_synthetic_stereo_pair()
    
    # Step 4: Create calibration images
    print("\n[STEP 4] Membuat gambar kalibrasi...")
    create_calibration_images()
    
    # Step 5: Create sample images for monocular depth
    print("\n[STEP 5] Membuat gambar sampel...")
    create_sample_single_image()
    
    # Step 6: Verify
    print("\n[STEP 6] Verifikasi data...")
    success = verify_data()
    
    if success:
        print("\n[SUCCESS] Download selesai!")
        print(f"Data tersimpan di: {DATA_DIR}")
    else:
        print("\n[WARNING] Beberapa data mungkin tidak tersedia")
    
    print("\nGunakan data ini untuk praktikum Depth Estimation.")
    print("Jalankan program praktikum di folder praktikum/")

if __name__ == "__main__":
    main()
