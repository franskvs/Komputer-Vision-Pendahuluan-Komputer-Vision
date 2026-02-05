"""
===============================================================================
PRAKTIKUM COMPUTER VISION
Bab 06: Recognition - Program 01: Face Detection dengan OpenCV
===============================================================================

Deskripsi:
    Program ini mendemonstrasikan berbagai metode face detection menggunakan
    OpenCV, termasuk Haar Cascades dan HOG+SVM (dlib).

Konsep yang dipelajari:
    1. Haar Cascade Classifier (Viola-Jones Algorithm)
    2. HOG (Histogram of Oriented Gradients) features
    3. Parameter tuning untuk detection
    4. Perbandingan metode tradisional

Dependencies:
    pip install opencv-python numpy matplotlib

Kompatibilitas:
    - Windows/Linux/MacOS
    - Python 3.7+
    
Author: Praktikum Computer Vision
===============================================================================
"""

import cv2
import numpy as np
import os
import urllib.request
from pathlib import Path
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# =====================================================================
# BAGIAN 1: SETUP DAN UTILITIES
# =====================================================================

def create_output_directory():
    """
    Membuat direktori untuk menyimpan hasil output.
    
    Returns:
        Path: Path ke direktori output
    """
    output_dir = Path("output_face_detection")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def download_cascade_files():
    """
    Download Haar Cascade files jika belum ada.
    OpenCV biasanya menyertakan file ini, tapi kita pastikan.
    
    Haar Cascade adalah classifier berbasis machine learning yang
    dilatih dengan banyak sampel positif dan negatif untuk mendeteksi
    objek tertentu (dalam hal ini wajah).
    """
    cascade_dir = Path("cascades")
    cascade_dir.mkdir(exist_ok=True)
    
    # List cascade files yang diperlukan
    cascades = {
        'frontal_face': 'haarcascade_frontalface_default.xml',
        'profile_face': 'haarcascade_profileface.xml',
        'eye': 'haarcascade_eye.xml',
        'smile': 'haarcascade_smile.xml'
    }
    
    base_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/"
    
    for name, filename in cascades.items():
        filepath = cascade_dir / filename
        
        # Cek juga di OpenCV data directory
        opencv_data = cv2.data.haarcascades
        opencv_path = Path(opencv_data) / filename
        
        if opencv_path.exists():
            print(f"✓ {name}: Menggunakan file dari OpenCV data")
        elif filepath.exists():
            print(f"✓ {name}: File sudah ada di lokal")
        else:
            print(f"⬇ Mendownload {filename}...")
            try:
                urllib.request.urlretrieve(base_url + filename, filepath)
                print(f"  ✓ Download selesai")
            except Exception as e:
                print(f"  ✗ Gagal download: {e}")
    
    return cascade_dir

def get_cascade_path(cascade_name):
    """
    Dapatkan path ke cascade file.
    Prioritas: OpenCV data dir -> local cascades dir
    
    Args:
        cascade_name: Nama file cascade
        
    Returns:
        str: Path ke cascade file
    """
    # Coba dari OpenCV data directory
    opencv_path = cv2.data.haarcascades + cascade_name
    if os.path.exists(opencv_path):
        return opencv_path
    
    # Coba dari local directory
    local_path = f"cascades/{cascade_name}"
    if os.path.exists(local_path):
        return local_path
    
    return opencv_path  # Default ke OpenCV path

def create_sample_image():
    """
    Membuat sample image dengan gambar wajah sederhana.
    Dalam praktik nyata, gunakan gambar asli.
    
    Returns:
        numpy.ndarray: Sample image
    """
    # Buat canvas
    img = np.ones((480, 640, 3), dtype=np.uint8) * 240
    
    # Gambar beberapa "wajah" sederhana
    faces = [
        (150, 200, 80),   # (x, y, radius)
        (350, 200, 70),
        (500, 200, 60),
        (250, 350, 65)
    ]
    
    for x, y, r in faces:
        # Wajah (oval)
        cv2.ellipse(img, (x, y), (r, int(r*1.2)), 0, 0, 360, (200, 170, 140), -1)
        cv2.ellipse(img, (x, y), (r, int(r*1.2)), 0, 0, 360, (100, 80, 60), 2)
        
        # Mata
        eye_y = y - r//4
        eye_offset = r//3
        cv2.circle(img, (x - eye_offset, eye_y), r//8, (255, 255, 255), -1)
        cv2.circle(img, (x + eye_offset, eye_y), r//8, (255, 255, 255), -1)
        cv2.circle(img, (x - eye_offset, eye_y), r//16, (50, 50, 50), -1)
        cv2.circle(img, (x + eye_offset, eye_y), r//16, (50, 50, 50), -1)
        
        # Hidung
        nose_y = y + r//6
        cv2.line(img, (x, y), (x, nose_y), (150, 120, 100), 2)
        
        # Mulut
        mouth_y = y + r//2
        cv2.ellipse(img, (x, mouth_y), (r//3, r//6), 0, 10, 170, (150, 100, 100), 2)
    
    # Tambah teks
    cv2.putText(img, "Sample Image with Face-like Shapes", 
                (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    
    return img

# =====================================================================
# BAGIAN 2: HAAR CASCADE DETECTION
# =====================================================================

def demo_haar_cascade_basic():
    """
    Demo dasar Haar Cascade face detection.
    
    Viola-Jones Algorithm (Haar Cascade):
    1. Integral Image: Percepat perhitungan fitur
    2. Haar-like Features: Pola sederhana (edge, line, center-surround)
    3. AdaBoost: Seleksi fitur terbaik
    4. Cascade: Reject cepat untuk non-face regions
    
    Kelebihan:
    - Sangat cepat
    - Tidak butuh GPU
    - Tersedia di OpenCV
    
    Kekurangan:
    - Kurang akurat untuk pose miring
    - Sensitif terhadap pencahayaan
    - High false positive rate
    """
    print("\n" + "="*60)
    print("DEMO: Haar Cascade Face Detection - Basic")
    print("="*60)
    
    # Load cascade classifier
    cascade_path = get_cascade_path('haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        print("Error: Gagal load cascade classifier!")
        print(f"Path yang dicoba: {cascade_path}")
        return
    
    print(f"\n✓ Cascade classifier loaded dari: {cascade_path}")
    
    # Load atau buat sample image
    sample_images = list(Path(".").glob("*.jpg")) + list(Path(".").glob("*.png"))
    face_images = [f for f in sample_images if 'face' in str(f).lower() or 'wajah' in str(f).lower()]
    
    if face_images:
        img = cv2.imread(str(face_images[0]))
        print(f"\n✓ Menggunakan gambar: {face_images[0]}")
    else:
        print("\n⚠ Tidak ada gambar wajah ditemukan, menggunakan sample image")
        img = create_sample_image()
    
    # Convert ke grayscale (Haar Cascade bekerja dengan grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Histogram equalization untuk improve contrast
    gray = cv2.equalizeHist(gray)
    
    # Deteksi wajah
    print("\n📍 Melakukan face detection...")
    
    # Parameter detectMultiScale:
    # - scaleFactor: Seberapa besar image di-reduce di setiap scale (1.1 = 10%)
    # - minNeighbors: Minimum neighbors untuk retain detection (filter false positives)
    # - minSize: Ukuran minimum wajah yang dideteksi
    
    start_time = time.time()
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,     # Image pyramid scale factor
        minNeighbors=5,      # Minimum neighbors untuk validasi
        minSize=(30, 30),    # Minimum face size
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    detection_time = time.time() - start_time
    
    print(f"\n📊 Hasil Deteksi:")
    print(f"   - Waktu deteksi: {detection_time*1000:.2f} ms")
    print(f"   - Wajah terdeteksi: {len(faces)}")
    
    # Gambar bounding box
    img_result = img.copy()
    
    for i, (x, y, w, h) in enumerate(faces):
        # Bounding box
        cv2.rectangle(img_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Label
        label = f"Face {i+1}"
        cv2.putText(img_result, label, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        print(f"   - Face {i+1}: position=({x},{y}), size=({w}x{h})")
    
    # Simpan hasil
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "01_haar_basic.jpg"), img_result)
    print(f"\n✓ Hasil disimpan: {output_dir}/01_haar_basic.jpg")
    
    # Tampilkan (jika tidak headless)
    try:
        cv2.imshow("Haar Cascade Face Detection", img_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print("(Display tidak tersedia, hasil disimpan ke file)")

def demo_haar_cascade_parameters():
    """
    Demo pengaruh parameter pada Haar Cascade detection.
    
    Parameter penting:
    1. scaleFactor: Berapa persen image di-reduce per level pyramid
       - Lebih kecil (1.05): Lebih akurat tapi lebih lambat
       - Lebih besar (1.3): Lebih cepat tapi bisa miss faces
    
    2. minNeighbors: Minimum detections yang overlap untuk dianggap valid
       - Lebih kecil (1-2): Lebih sensitif, lebih banyak false positives
       - Lebih besar (6+): Lebih strict, bisa miss beberapa faces
    """
    print("\n" + "="*60)
    print("DEMO: Pengaruh Parameter Haar Cascade")
    print("="*60)
    
    # Load cascade
    cascade_path = get_cascade_path('haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        print("Error: Gagal load cascade classifier!")
        return
    
    # Buat atau load sample image
    img = create_sample_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    # Test berbagai parameter
    parameters = [
        # (scaleFactor, minNeighbors, description)
        (1.05, 3, "Sensitive (1.05, 3)"),
        (1.1, 4, "Balanced (1.1, 4)"),
        (1.1, 6, "Strict (1.1, 6)"),
        (1.2, 3, "Fast (1.2, 3)"),
        (1.3, 5, "Very Fast (1.3, 5)"),
    ]
    
    results = []
    
    for scale, neighbors, desc in parameters:
        start_time = time.time()
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale,
            minNeighbors=neighbors,
            minSize=(30, 30)
        )
        elapsed = time.time() - start_time
        
        results.append({
            'params': (scale, neighbors),
            'description': desc,
            'faces': len(faces),
            'time_ms': elapsed * 1000
        })
    
    # Tampilkan hasil perbandingan
    print("\n📊 Perbandingan Parameter:")
    print("-" * 65)
    print(f"{'Parameter':<25} {'Faces':<10} {'Time (ms)':<15} {'Note':<20}")
    print("-" * 65)
    
    for r in results:
        note = ""
        if r['faces'] > 4:
            note = "Mungkin false positives"
        elif r['faces'] < 2:
            note = "Mungkin miss faces"
        else:
            note = "OK"
        
        print(f"{r['description']:<25} {r['faces']:<10} {r['time_ms']:<15.2f} {note:<20}")
    
    # Visualisasi perbandingan
    fig_width = 800
    fig_height = len(parameters) * 250 + 100
    comparison_img = np.ones((fig_height, fig_width, 3), dtype=np.uint8) * 255
    
    for i, (scale, neighbors, desc) in enumerate(parameters):
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=scale, minNeighbors=neighbors, minSize=(30, 30)
        )
        
        # Resize image untuk visualisasi
        small_img = cv2.resize(img.copy(), (300, 200))
        small_gray = cv2.resize(gray, (300, 200))
        
        # Scale detections
        scale_x = 300 / img.shape[1]
        scale_y = 200 / img.shape[0]
        
        for (x, y, w, h) in faces:
            x_s = int(x * scale_x)
            y_s = int(y * scale_y)
            w_s = int(w * scale_x)
            h_s = int(h * scale_y)
            cv2.rectangle(small_img, (x_s, y_s), (x_s+w_s, y_s+h_s), (0, 255, 0), 2)
        
        # Tempatkan di comparison image
        y_offset = i * 250 + 50
        comparison_img[y_offset:y_offset+200, 50:350] = small_img
        
        # Label
        cv2.putText(comparison_img, desc, (380, y_offset + 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(comparison_img, f"Detected: {len(faces)} faces", (380, y_offset + 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 1)
    
    # Title
    cv2.putText(comparison_img, "Parameter Comparison", (280, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "01_haar_parameters.jpg"), comparison_img)
    print(f"\n✓ Visualisasi disimpan: {output_dir}/01_haar_parameters.jpg")

def demo_haar_cascade_types():
    """
    Demo berbagai tipe Haar Cascade untuk deteksi berbeda.
    
    OpenCV menyediakan cascade untuk:
    - Frontal face
    - Profile face
    - Eyes
    - Smile
    - Upper body
    - Full body
    - Dan lainnya
    """
    print("\n" + "="*60)
    print("DEMO: Berbagai Tipe Haar Cascade")
    print("="*60)
    
    # Load berbagai cascade
    cascades = {
        'Frontal Face': get_cascade_path('haarcascade_frontalface_default.xml'),
        'Profile Face': get_cascade_path('haarcascade_profileface.xml'),
        'Eyes': get_cascade_path('haarcascade_eye.xml'),
        'Smile': get_cascade_path('haarcascade_smile.xml'),
    }
    
    # Buat sample image
    img = create_sample_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    print("\n📍 Mendeteksi dengan berbagai cascade:")
    
    for name, cascade_path in cascades.items():
        cascade = cv2.CascadeClassifier(cascade_path)
        
        if cascade.empty():
            print(f"   ⚠ {name}: Cascade tidak tersedia")
            continue
        
        # Deteksi
        if name == 'Smile':
            # Smile detection perlu parameter berbeda
            detections = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=25)
        else:
            detections = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        print(f"   ✓ {name}: {len(detections)} detections")
    
    # Demonstrasi combined detection (face + eyes)
    print("\n📍 Combined Detection (Face + Eyes in Face):")
    
    face_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_frontalface_default.xml'))
    eye_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_eye.xml'))
    
    img_result = img.copy()
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    for (x, y, w, h) in faces:
        # Gambar face box
        cv2.rectangle(img_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # ROI untuk deteksi mata (hanya area wajah)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img_result[y:y+h, x:x+w]
        
        # Deteksi mata dalam ROI wajah
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        for (ex, ey, ew, eh) in eyes:
            center = (ex + ew//2, ey + eh//2)
            cv2.circle(roi_color, center, ew//2, (255, 0, 0), 2)
        
        cv2.putText(img_result, f"{len(eyes)} eyes", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "01_haar_combined.jpg"), img_result)
    print(f"\n✓ Hasil combined detection disimpan: {output_dir}/01_haar_combined.jpg")

# =====================================================================
# BAGIAN 3: HOG FACE DETECTION (dengan simulasi jika dlib tidak ada)
# =====================================================================

def demo_hog_detection():
    """
    Demo HOG (Histogram of Oriented Gradients) face detection.
    
    HOG Features:
    1. Compute gradients (arah dan magnitude)
    2. Divide image ke cells (8x8 pixels)
    3. Compute histogram of gradients untuk setiap cell
    4. Normalize dengan blocks (2x2 cells)
    5. Concatenate semua features
    
    HOG + SVM untuk Face Detection:
    - dlib menyediakan pretrained HOG face detector
    - Lebih robust terhadap pencahayaan dibanding Haar
    - Medium speed (lebih lambat dari Haar)
    """
    print("\n" + "="*60)
    print("DEMO: HOG Face Detection")
    print("="*60)
    
    # Coba import dlib
    try:
        import dlib
        HAS_DLIB = True
        print("\n✓ dlib tersedia, menggunakan HOG detector dari dlib")
    except ImportError:
        HAS_DLIB = False
        print("\n⚠ dlib tidak tersedia, akan demo konsep HOG features saja")
        print("   Install dengan: pip install dlib")
    
    # Buat sample image
    img = create_sample_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if HAS_DLIB:
        # Gunakan dlib HOG detector
        detector = dlib.get_frontal_face_detector()
        
        print("\n📍 Melakukan HOG face detection dengan dlib...")
        
        start_time = time.time()
        # Upsample 1 berarti process gambar asli
        # Upsample 2 berarti upscale 2x untuk deteksi wajah kecil
        faces = detector(gray, 1)
        detection_time = time.time() - start_time
        
        print(f"\n📊 Hasil Deteksi:")
        print(f"   - Waktu deteksi: {detection_time*1000:.2f} ms")
        print(f"   - Wajah terdeteksi: {len(faces)}")
        
        img_result = img.copy()
        
        for i, face in enumerate(faces):
            x, y = face.left(), face.top()
            w, h = face.width(), face.height()
            
            cv2.rectangle(img_result, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img_result, f"HOG {i+1}", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        output_dir = create_output_directory()
        cv2.imwrite(str(output_dir / "01_hog_detection.jpg"), img_result)
        print(f"\n✓ Hasil disimpan: {output_dir}/01_hog_detection.jpg")
    
    else:
        demo_hog_features_visualization(gray)

def demo_hog_features_visualization(gray_image=None):
    """
    Visualisasi HOG features untuk pemahaman konsep.
    
    HOG descriptor process:
    1. Gamma/color normalization
    2. Compute gradients (Sobel)
    3. Spatial/orientation binning
    4. Normalization over blocks
    """
    print("\n📍 Demonstrasi HOG Features Visualization...")
    
    if gray_image is None:
        img = create_sample_image()
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute gradients menggunakan Sobel
    gx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    
    # Magnitude dan direction
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx) * 180 / np.pi
    
    # Normalize untuk visualisasi
    magnitude_vis = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    direction_vis = ((direction + 180) / 360 * 255).astype(np.uint8)
    
    # HOG-like visualization (simplified)
    cell_size = 8
    h, w = gray_image.shape
    hog_vis = np.zeros((h, w, 3), dtype=np.uint8)
    
    for i in range(0, h - cell_size, cell_size):
        for j in range(0, w - cell_size, cell_size):
            # Get cell
            cell_mag = magnitude[i:i+cell_size, j:j+cell_size]
            cell_dir = direction[i:i+cell_size, j:j+cell_size]
            
            # Dominant gradient direction
            avg_mag = np.mean(cell_mag)
            avg_dir = np.mean(cell_dir)
            
            if avg_mag > 10:  # Threshold
                # Draw gradient arrow
                cx, cy = j + cell_size//2, i + cell_size//2
                length = min(avg_mag / 10, cell_size//2)
                rad = avg_dir * np.pi / 180
                
                dx = int(length * np.cos(rad))
                dy = int(length * np.sin(rad))
                
                cv2.line(hog_vis, (cx-dx, cy-dy), (cx+dx, cy+dy), (0, 255, 0), 1)
    
    # Buat comparison image
    fig_width = 900
    fig_height = 400
    comparison = np.ones((fig_height, fig_width, 3), dtype=np.uint8) * 255
    
    # Original
    img_small = cv2.resize(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), (280, 280))
    comparison[60:340, 10:290] = img_small
    cv2.putText(comparison, "Original", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Gradient Magnitude
    mag_color = cv2.applyColorMap(cv2.resize(magnitude_vis, (280, 280)), cv2.COLORMAP_JET)
    comparison[60:340, 310:590] = mag_color
    cv2.putText(comparison, "Gradient Magnitude", (360, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # HOG-like visualization
    hog_small = cv2.resize(hog_vis, (280, 280))
    comparison[60:340, 610:890] = hog_small
    cv2.putText(comparison, "HOG-like Features", (670, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "01_hog_visualization.jpg"), comparison)
    print(f"\n✓ HOG visualization disimpan: {output_dir}/01_hog_visualization.jpg")
    
    print("\n📚 Penjelasan HOG Features:")
    print("   1. Compute gradient (Sobel) untuk setiap pixel")
    print("   2. Divide gambar ke cells (8x8 pixels)")
    print("   3. Hitung histogram gradient orientations per cell")
    print("   4. Normalize dengan neighboring blocks")
    print("   5. Concatenate semua histograms → HOG descriptor")

# =====================================================================
# BAGIAN 4: PERBANDINGAN METODE
# =====================================================================

def demo_method_comparison():
    """
    Perbandingan berbagai metode face detection.
    """
    print("\n" + "="*60)
    print("DEMO: Perbandingan Metode Face Detection")
    print("="*60)
    
    # Buat sample image
    img = create_sample_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    results = []
    
    # Method 1: Haar Cascade
    print("\n📍 Testing Haar Cascade...")
    haar_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_frontalface_default.xml'))
    
    start = time.time()
    haar_faces = haar_cascade.detectMultiScale(gray, 1.1, 5)
    haar_time = (time.time() - start) * 1000
    
    results.append({
        'method': 'Haar Cascade',
        'faces': len(haar_faces),
        'time_ms': haar_time,
        'detections': haar_faces
    })
    
    # Method 2: Haar with LBP (Local Binary Pattern)
    print("📍 Testing Haar Cascade (tuned)...")
    start = time.time()
    haar_tuned = haar_cascade.detectMultiScale(gray, 1.05, 6, minSize=(50, 50))
    haar_tuned_time = (time.time() - start) * 1000
    
    results.append({
        'method': 'Haar (tuned)',
        'faces': len(haar_tuned),
        'time_ms': haar_tuned_time,
        'detections': haar_tuned
    })
    
    # Method 3: HOG (if dlib available)
    try:
        import dlib
        print("📍 Testing HOG (dlib)...")
        detector = dlib.get_frontal_face_detector()
        
        start = time.time()
        hog_faces = detector(gray, 1)
        hog_time = (time.time() - start) * 1000
        
        # Convert dlib rectangles to numpy array
        hog_dets = [(f.left(), f.top(), f.width(), f.height()) for f in hog_faces]
        
        results.append({
            'method': 'HOG (dlib)',
            'faces': len(hog_faces),
            'time_ms': hog_time,
            'detections': hog_dets
        })
    except ImportError:
        print("⚠ dlib tidak tersedia, skipping HOG test")
    
    # Tampilkan hasil perbandingan
    print("\n" + "="*60)
    print("📊 HASIL PERBANDINGAN:")
    print("="*60)
    print(f"{'Method':<20} {'Faces':<10} {'Time (ms)':<15}")
    print("-"*45)
    
    for r in results:
        print(f"{r['method']:<20} {r['faces']:<10} {r['time_ms']:<15.2f}")
    
    # Visualisasi perbandingan
    create_comparison_visualization(img, results)
    
    # Analisis
    print("\n📝 Analisis:")
    print("-"*45)
    
    fastest = min(results, key=lambda x: x['time_ms'])
    most_faces = max(results, key=lambda x: x['faces'])
    
    print(f"   • Tercepat: {fastest['method']} ({fastest['time_ms']:.2f} ms)")
    print(f"   • Paling banyak deteksi: {most_faces['method']} ({most_faces['faces']} faces)")
    
    print("\n💡 Rekomendasi:")
    print("   • Real-time (webcam): Haar Cascade (fastest)")
    print("   • Akurasi tinggi: HOG atau Deep Learning")
    print("   • Embedded device: Haar Cascade (ringan)")

def create_comparison_visualization(img, results):
    """
    Buat visualisasi perbandingan metode.
    """
    n_methods = len(results)
    fig_width = 350 * n_methods
    fig_height = 450
    
    comparison = np.ones((fig_height, fig_width, 3), dtype=np.uint8) * 255
    
    for i, r in enumerate(results):
        x_offset = i * 350 + 25
        
        # Resize image
        img_small = cv2.resize(img.copy(), (300, 250))
        
        # Scale factor untuk detections
        scale_x = 300 / img.shape[1]
        scale_y = 250 / img.shape[0]
        
        # Gambar detections
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        color = colors[i % len(colors)]
        
        for det in r['detections']:
            if len(det) == 4:
                x, y, w, h = det
            else:
                continue
            
            x_s = int(x * scale_x)
            y_s = int(y * scale_y)
            w_s = int(w * scale_x)
            h_s = int(h * scale_y)
            
            cv2.rectangle(img_small, (x_s, y_s), (x_s+w_s, y_s+h_s), color, 2)
        
        # Place image
        comparison[80:330, x_offset:x_offset+300] = img_small
        
        # Labels
        cv2.putText(comparison, r['method'], (x_offset + 80, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(comparison, f"Faces: {r['faces']}", (x_offset + 100, 360),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 1)
        cv2.putText(comparison, f"Time: {r['time_ms']:.1f}ms", (x_offset + 100, 385),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 0, 0), 1)
    
    # Title
    cv2.putText(comparison, "Face Detection Methods Comparison", (fig_width//2 - 200, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "01_method_comparison.jpg"), comparison)
    print(f"\n✓ Comparison disimpan: {output_dir}/01_method_comparison.jpg")

# =====================================================================
# BAGIAN 5: WEBCAM REAL-TIME DETECTION
# =====================================================================

def demo_realtime_detection():
    """
    Demo real-time face detection menggunakan webcam.
    """
    print("\n" + "="*60)
    print("DEMO: Real-time Face Detection (Webcam)")
    print("="*60)
    
    # Load cascade
    face_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_frontalface_default.xml'))
    eye_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_eye.xml'))
    
    if face_cascade.empty():
        print("Error: Gagal load face cascade!")
        return
    
    # Buka webcam
    print("\n📷 Mencoba membuka webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("⚠ Webcam tidak tersedia, melakukan simulasi dengan sample image")
        demo_simulated_realtime()
        return
    
    print("✓ Webcam terbuka!")
    print("\n📌 Kontrol:")
    print("   - 'q': Quit")
    print("   - 's': Screenshot")
    print("   - '1': Haar only")
    print("   - '2': Haar + Eyes")
    
    mode = 1
    frame_count = 0
    fps_start = time.time()
    fps = 0
    
    output_dir = create_output_directory()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Calculate FPS
        if frame_count % 30 == 0:
            fps = 30 / (time.time() - fps_start)
            fps_start = time.time()
        
        # Convert ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Deteksi wajah
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        
        # Gambar detections
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if mode == 2:
                # Deteksi mata dalam ROI wajah
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
        
        # Info overlay
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Mode: {'Haar+Eyes' if mode==2 else 'Haar only'}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display
        cv2.imshow("Real-time Face Detection", frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = output_dir / f"screenshot_{frame_count}.jpg"
            cv2.imwrite(str(filename), frame)
            print(f"✓ Screenshot saved: {filename}")
        elif key == ord('1'):
            mode = 1
        elif key == ord('2'):
            mode = 2
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Real-time detection selesai")

def demo_simulated_realtime():
    """
    Simulasi real-time detection untuk environment tanpa webcam.
    """
    print("\n📍 Running simulated real-time detection...")
    
    face_cascade = cv2.CascadeClassifier(get_cascade_path('haarcascade_frontalface_default.xml'))
    
    # Buat sequence frames
    for i in range(30):
        # Buat frame dengan variasi
        img = create_sample_image()
        
        # Simulasi variasi (brightness)
        factor = 0.8 + 0.4 * (i / 30)
        img = cv2.convertScaleAbs(img, alpha=factor, beta=0)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.putText(img, f"Frame: {i+1}/30", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, f"Faces: {len(faces)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if i == 15:  # Save middle frame
            output_dir = create_output_directory()
            cv2.imwrite(str(output_dir / "01_simulated_realtime.jpg"), img)
    
    print("✓ Simulasi selesai (30 frames processed)")

# =====================================================================
# MENU UTAMA
# =====================================================================

def main():
    """
    Menu utama program face detection dengan OpenCV.
    """
    print("="*60)
    print("PRAKTIKUM COMPUTER VISION")
    print("Bab 06: Face Detection dengan OpenCV")
    print("="*60)
    
    # Download cascade files jika perlu
    download_cascade_files()
    
    while True:
        print("\n" + "-"*40)
        print("MENU:")
        print("-"*40)
        print("1. Haar Cascade - Basic Detection")
        print("2. Haar Cascade - Parameter Tuning")
        print("3. Haar Cascade - Various Types")
        print("4. HOG Face Detection")
        print("5. Method Comparison")
        print("6. Real-time Detection (Webcam)")
        print("0. Exit")
        print("-"*40)
        
        try:
            choice = input("\nPilih menu [0-6]: ").strip()
        except EOFError:
            choice = "0"
        
        if choice == "1":
            demo_haar_cascade_basic()
        elif choice == "2":
            demo_haar_cascade_parameters()
        elif choice == "3":
            demo_haar_cascade_types()
        elif choice == "4":
            demo_hog_detection()
        elif choice == "5":
            demo_method_comparison()
        elif choice == "6":
            demo_realtime_detection()
        elif choice == "0":
            print("\n👋 Terima kasih telah menggunakan program ini!")
            break
        else:
            print("⚠ Pilihan tidak valid!")

if __name__ == "__main__":
    main()
