"""
=============================================================================
PRAKTIKUM 3: SIFT FEATURE DETECTION
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan algoritma SIFT (Scale-Invariant Feature
    Transform) yang dapat mendeteksi keypoints yang invariant terhadap
    skala dan rotasi. SIFT juga menghasilkan descriptor 128-dimensi.

Konsep Utama:
    1. Scale-space extrema detection - mencari keypoint di berbagai skala
    2. Keypoint localization - menyaring keypoint yang tidak stabil
    3. Orientation assignment - menentukan orientasi dominan
    4. Keypoint descriptor - membuat descriptor 128-dimensi

Keunggulan SIFT:
    - Invariant terhadap skala (zoom in/out)
    - Invariant terhadap rotasi
    - Robust terhadap perubahan pencahayaan
    - Descriptor sangat diskriminatif

Catatan:
    SIFT sebelumnya adalah algoritma paten, tapi patennya sudah expired.
    Sejak OpenCV 4.4, SIFT tersedia di modul utama.

Aplikasi Dunia Nyata:
    - Object recognition
    - Image stitching (panorama)
    - 3D reconstruction
    - Robot navigation

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Jumlah fitur terbaik yang dipertahankan (0 = semua)
N_FEATURES = 500  # Coba ubah: 0, 100, 500, 1000, 2000

# Jumlah lapisan dalam setiap oktaf scale-space
N_OCTAVE_LAYERS = 3  # Coba ubah: 3, 4, 5

# Threshold untuk filter low-contrast keypoints
# Nilai lebih tinggi = lebih sedikit keypoint
CONTRAST_THRESHOLD = 0.04  # Coba ubah: 0.02, 0.04, 0.06, 0.08

# Threshold untuk filter edge-like keypoints
# Nilai lebih tinggi = lebih toleran terhadap edge
EDGE_THRESHOLD = 10  # Coba ubah: 5, 10, 15, 20

# Sigma untuk Gaussian blur di oktaf pertama
SIGMA = 1.6  # Coba ubah: 1.2, 1.6, 2.0

# Ukuran keypoint untuk visualisasi
DRAW_RICH_KEYPOINTS = True  # True = gambar ukuran dan orientasi
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def sift_detection(image_path):
    """
    Melakukan SIFT Feature Detection pada gambar
    
    Args:
        image_path: Path ke file gambar
        
    Returns:
        Tuple (original, result, keypoints, descriptors, processing_time)
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Buat SIFT detector dengan parameter
    sift = cv2.SIFT_create(
        nfeatures=N_FEATURES,
        nOctaveLayers=N_OCTAVE_LAYERS,
        contrastThreshold=CONTRAST_THRESHOLD,
        edgeThreshold=EDGE_THRESHOLD,
        sigma=SIGMA
    )
    
    # Mulai timing
    start_time = time.time()
    
    # Deteksi keypoints dan compute descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    processing_time = (time.time() - start_time) * 1000  # dalam ms
    
    # Gambar keypoints pada hasil
    flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS if DRAW_RICH_KEYPOINTS else 0
    result = cv2.drawKeypoints(
        img, keypoints, None, 
        color=(0, 255, 0),
        flags=flags
    )
    
    return img, result, keypoints, descriptors, processing_time

def analyze_keypoints(keypoints):
    """
    Menganalisis properti keypoints yang terdeteksi
    """
    if not keypoints:
        return None
    
    # Ekstrak properti
    sizes = [kp.size for kp in keypoints]
    responses = [kp.response for kp in keypoints]
    angles = [kp.angle for kp in keypoints]
    octaves = [kp.octave for kp in keypoints]
    
    analysis = {
        'count': len(keypoints),
        'size_min': min(sizes),
        'size_max': max(sizes),
        'size_mean': np.mean(sizes),
        'response_min': min(responses),
        'response_max': max(responses),
        'response_mean': np.mean(responses),
    }
    
    return analysis

def compare_scale_invariance(image_path):
    """
    Mendemonstrasikan scale invariance SIFT
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # SIFT detector
    sift = cv2.SIFT_create(nfeatures=200)
    
    # Original
    kp1, _ = sift.detectAndCompute(gray, None)
    result1 = cv2.drawKeypoints(img, kp1, None, color=(0, 255, 0),
                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Scaled down 50%
    scaled = cv2.resize(gray, None, fx=0.5, fy=0.5)
    kp2, _ = sift.detectAndCompute(scaled, None)
    scaled_color = cv2.resize(img, None, fx=0.5, fy=0.5)
    result2 = cv2.drawKeypoints(scaled_color, kp2, None, color=(0, 255, 0),
                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Scale back up untuk perbandingan
    result2 = cv2.resize(result2, (result1.shape[1], result1.shape[0]))
    
    # Rotated 45 degrees
    h, w = gray.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated = cv2.warpAffine(gray, M, (w, h))
    rotated_color = cv2.warpAffine(img, M, (w, h))
    kp3, _ = sift.detectAndCompute(rotated, None)
    result3 = cv2.drawKeypoints(rotated_color, kp3, None, color=(0, 255, 0),
                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Tambah label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(result1, f"Original: {len(kp1)} kp", (10, 30), font, 0.7, (0, 255, 255), 2)
    cv2.putText(result2, f"Scaled 50%: {len(kp2)} kp", (10, 30), font, 0.7, (0, 255, 255), 2)
    cv2.putText(result3, f"Rotated 45°: {len(kp3)} kp", (10, 30), font, 0.7, (0, 255, 255), 2)
    
    # Resize untuk visualisasi
    max_width = 400
    h, w = result1.shape[:2]
    if w > max_width:
        scale = max_width / w
        result1 = cv2.resize(result1, None, fx=scale, fy=scale)
        result2 = cv2.resize(result2, None, fx=scale, fy=scale)
        result3 = cv2.resize(result3, None, fx=scale, fy=scale)
    
    # Gabungkan
    comparison = np.hstack([result1, result2, result3])
    
    return comparison, len(kp1), len(kp2), len(kp3)

def main():
    print("=" * 70)
    print("PRAKTIKUM 3: SIFT FEATURE DETECTION")
    print("=" * 70)
    print()
    
    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - N Features: {N_FEATURES}")
    print(f"  - N Octave Layers: {N_OCTAVE_LAYERS}")
    print(f"  - Contrast Threshold: {CONTRAST_THRESHOLD}")
    print(f"  - Edge Threshold: {EDGE_THRESHOLD}")
    print(f"  - Sigma: {SIGMA}")
    print()
    
    # Path setup
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, "data", "images")
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Gambar untuk diproses
    test_images = ["building.jpg", "box.png", "butterfly.jpg"]
    
    for image_name in test_images:
        image_path = os.path.join(data_dir, image_name)
        
        if not os.path.exists(image_path):
            print(f"⚠ File tidak ditemukan: {image_name}")
            continue
        
        print(f"Memproses: {image_name}")
        print("-" * 40)
        
        try:
            # Deteksi SIFT
            original, result, keypoints, descriptors, proc_time = \
                sift_detection(image_path)
            
            print(f"  Jumlah keypoints: {len(keypoints)}")
            print(f"  Dimensi descriptor: {descriptors.shape if descriptors is not None else 'N/A'}")
            print(f"  Waktu proses: {proc_time:.2f} ms")
            
            # Analisis keypoints
            analysis = analyze_keypoints(keypoints)
            if analysis:
                print(f"  Ukuran keypoint: min={analysis['size_min']:.1f}, max={analysis['size_max']:.1f}")
                print(f"  Response rata-rata: {analysis['response_mean']:.4f}")
            
            # Resize untuk visualisasi
            max_width = 600
            h, w = original.shape[:2]
            if w > max_width:
                scale = max_width / w
                original = cv2.resize(original, None, fx=scale, fy=scale)
                result = cv2.resize(result, None, fx=scale, fy=scale)
            
            # Tambah label
            cv2.putText(original, "Original", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(result, f"SIFT: {len(keypoints)} keypoints", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Gabungkan
            visualization = np.hstack([original, result])
            
            # Simpan hasil
            output_name = f"sift_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Demonstrasi scale/rotation invariance
    print("Membuat demo scale/rotation invariance...")
    demo_image = "building.jpg"
    demo_path = os.path.join(data_dir, demo_image)
    
    if os.path.exists(demo_path):
        result = compare_scale_invariance(demo_path)
        if result is not None:
            comparison, n1, n2, n3 = result
            output_path = os.path.join(output_dir, "sift_invariance_demo.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Demo invariance disimpan: {output_path}")
            print(f"  Original: {n1} kp, Scaled: {n2} kp, Rotated: {n3} kp")
    
    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah N_FEATURES dari 500 ke 2000
   - Amati: Lebih banyak keypoint terdeteksi
   - Pertanyaan: Apakah semua keypoint berkualitas sama?
   
2. Ubah CONTRAST_THRESHOLD dari 0.04 ke 0.08
   - Amati: Keypoint low-contrast difilter
   - Mengapa: Hanya fitur yang "kuat" yang dipertahankan
   
3. Ubah EDGE_THRESHOLD dari 10 ke 5
   - Amati: Keypoint di sekitar edge difilter
   - Mengapa: Edge response mirip dengan corner

4. Set DRAW_RICH_KEYPOINTS = True
   - Amati: Lingkaran menunjukkan skala keypoint
   - Amati: Garis menunjukkan orientasi dominan
   
5. Bandingkan descriptor size:
   - SIFT menghasilkan 128-dimensi descriptor
   - Setiap keypoint memiliki vektor 128 nilai
   - Digunakan untuk matching di praktikum berikutnya

6. Perhatikan output "invariance demo":
   - Keypoint tetap terdeteksi meski gambar di-scale/rotate
   - Ini adalah keunggulan utama SIFT!
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
