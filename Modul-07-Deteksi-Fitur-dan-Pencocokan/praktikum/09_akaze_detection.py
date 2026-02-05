"""
=============================================================================
PRAKTIKUM 8 (LANJUTAN): AKAZE FEATURE DETECTION
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan AKAZE (Accelerated KAZE) untuk deteksi
    dan deskripsi fitur dengan keseimbangan antara kecepatan dan akurasi.

Konsep Utama:
    - AKAZE bekerja di non-linear scale space
    - Lebih cepat dari KAZE, lebih akurat dari ORB pada beberapa kasus
    - Descriptor biner (MLDB) → matching cepat

Aplikasi Dunia Nyata:
    - Tracking real-time pada perangkat mobile
    - Image stitching dengan trade-off speed/accuracy
    - Visual odometry pada robot

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Threshold untuk deteksi keypoint
# Nilai kecil = lebih banyak keypoint
AKAZE_THRESHOLD = 0.001  # Coba ubah: 0.0005, 0.001, 0.005

# Gunakan mode aman (default AKAZE) untuk stabilitas
# True = gunakan parameter default OpenCV
USE_SAFE_DEFAULTS = True

# Ukuran descriptor (0 = default)
DESCRIPTOR_SIZE = 0  # Coba ubah: 0, 64, 128

# Tipe descriptor
# 0: DESCRIPTOR_MLDB, 1: DESCRIPTOR_MLDB_UPRIGHT
DESCRIPTOR_TYPE = 0

# Warna keypoint
KEYPOINT_COLOR = (0, 255, 0)
# ======================================================================

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Mendapatkan direktori script ini berada"""
    return os.path.dirname(os.path.abspath(__file__))

def akaze_detection(image_path):
    """
    Melakukan AKAZE feature detection
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")

    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Buat AKAZE detector
    # Mode aman: gunakan parameter default OpenCV
    if USE_SAFE_DEFAULTS:
        akaze = cv2.AKAZE_create()
    else:
        akaze = cv2.AKAZE_create(
            descriptor_type=DESCRIPTOR_TYPE,
            descriptor_size=DESCRIPTOR_SIZE,
            threshold=AKAZE_THRESHOLD
        )

    # Mulai timing
    start_time = time.time()

    # Deteksi keypoints dan descriptors
    keypoints, descriptors = akaze.detectAndCompute(gray, None)

    processing_time = (time.time() - start_time) * 1000

    # Gambar keypoints pada hasil
    result = cv2.drawKeypoints(
        img, keypoints, None,
        color=KEYPOINT_COLOR,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    return img, result, keypoints, descriptors, processing_time

def main():
    print("=" * 70)
    print("PRAKTIKUM 8 (LANJUTAN): AKAZE FEATURE DETECTION")
    print("=" * 70)
    print()

    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - Safe Defaults: {USE_SAFE_DEFAULTS}")
    print(f"  - AKAZE Threshold: {AKAZE_THRESHOLD}")
    print(f"  - Descriptor Size: {DESCRIPTOR_SIZE}")
    print(f"  - Descriptor Type: {DESCRIPTOR_TYPE}")
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
            # Deteksi AKAZE
            original, result, keypoints, descriptors, proc_time = akaze_detection(image_path)

            print(f"  Jumlah keypoints: {len(keypoints)}")
            print(f"  Dimensi descriptor: {descriptors.shape if descriptors is not None else 'N/A'}")
            print(f"  Waktu proses: {proc_time:.2f} ms")

            # Resize untuk visualisasi
            max_width = 600
            h, w = original.shape[:2]
            if w > max_width:
                scale = max_width / w
                original = cv2.resize(original, None, fx=scale, fy=scale)
                result = cv2.resize(result, None, fx=scale, fy=scale)

            # Penjelasan parameter cv2.putText:
            # cv2.putText(image, text, org, fontFace, fontScale, color, thickness, lineType)
            # - image: gambar target
            # - text: teks yang akan ditulis
            # - org: posisi (x, y) kiri-bawah teks
            # - fontFace: jenis font
            # - fontScale: skala ukuran font
            # - color: warna (BGR)
            # - thickness: ketebalan teks
            # - lineType: tipe garis (opsional)
            cv2.putText(original, "Original", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(result, f"AKAZE: {len(keypoints)} keypoints", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Gabungkan
            visualization = np.hstack([original, result])

            # Simpan hasil
            output_name = f"akaze_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")

        except Exception as e:
            print(f"  Error: {e}")

        print()

    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah AKAZE_THRESHOLD dari 0.001 ke 0.005
   - Amati: jumlah keypoint berkurang
   - Mengapa: threshold lebih ketat

2. Ubah DESCRIPTOR_SIZE dari 0 ke 64
   - Amati: ukuran descriptor berubah
   - Pengaruh: kecepatan matching

3. Bandingkan AKAZE vs ORB:
   - AKAZE cenderung lebih stabil pada beberapa kasus
   - ORB lebih cepat untuk real-time
""")

    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
