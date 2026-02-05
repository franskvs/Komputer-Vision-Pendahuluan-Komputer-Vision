"""
=============================================================================
PRAKTIKUM 9 (LANJUTAN): FAST FEATURE DETECTION
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan FAST (Features from Accelerated
    Segment Test) untuk deteksi keypoint yang sangat cepat.

Konsep Utama:
    - FAST mendeteksi sudut dengan membandingkan intensitas piksel
    - Sangat cepat untuk real-time
    - Tidak menghasilkan descriptor (hanya keypoints)

Catatan:
    FAST biasanya dipasangkan dengan BRIEF/ORB descriptor untuk matching.
    Di praktikum ini fokus pada deteksi keypoint FAST.

Aplikasi Dunia Nyata:
    - Real-time tracking
    - Mobile robotics
    - AR marker tracking

=============================================================================
PARAMETER YANG BISA DIUBAH (Silakan eksperimen!)
=============================================================================
"""

# ===================== PARAMETER YANG BISA DIUBAH =====================
# Threshold FAST
# Nilai kecil = lebih banyak keypoint
FAST_THRESHOLD = 20  # Coba ubah: 10, 20, 30

# Non-max suppression (mengurangi keypoint yang terlalu dekat)
NONMAX_SUPPRESSION = True

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

def fast_detection(image_path):
    """
    Melakukan FAST keypoint detection
    """
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")

    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Buat FAST detector
    fast = cv2.FastFeatureDetector_create(
        threshold=FAST_THRESHOLD,
        nonmaxSuppression=NONMAX_SUPPRESSION
    )

    # Mulai timing
    start_time = time.time()

    # Deteksi keypoints
    keypoints = fast.detect(gray, None)

    processing_time = (time.time() - start_time) * 1000

    # Gambar keypoints pada hasil
    result = cv2.drawKeypoints(
        img, keypoints, None,
        color=KEYPOINT_COLOR,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    return img, result, keypoints, processing_time

def compare_thresholds(image_path):
    """
    Membandingkan hasil FAST dengan berbagai threshold
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresholds = [10, 20, 30, 40]
    results = []

    for th in thresholds:
        fast = cv2.FastFeatureDetector_create(
            threshold=th,
            nonmaxSuppression=NONMAX_SUPPRESSION
        )
        kps = fast.detect(gray, None)
        vis = cv2.drawKeypoints(img, kps, None, color=KEYPOINT_COLOR)

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
        cv2.putText(vis, f"T={th}, kp={len(kps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        results.append(vis)

    # Resize untuk visualisasi
    max_width = 350
    h, w = results[0].shape[:2]
    if w > max_width:
        scale = max_width / w
        results = [cv2.resize(r, None, fx=scale, fy=scale) for r in results]

    row1 = np.hstack([results[0], results[1]])
    row2 = np.hstack([results[2], results[3]])
    comparison = np.vstack([row1, row2])

    return comparison

def main():
    print("=" * 70)
    print("PRAKTIKUM 9 (LANJUTAN): FAST FEATURE DETECTION")
    print("=" * 70)
    print()

    # Print parameter yang digunakan
    print("Parameter yang digunakan:")
    print(f"  - FAST Threshold: {FAST_THRESHOLD}")
    print(f"  - Nonmax Suppression: {NONMAX_SUPPRESSION}")
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
            # Deteksi FAST
            original, result, keypoints, proc_time = fast_detection(image_path)

            print(f"  Jumlah keypoints: {len(keypoints)}")
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
            cv2.putText(result, f"FAST: {len(keypoints)} keypoints", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Gabungkan
            visualization = np.hstack([original, result])

            # Simpan hasil
            output_name = f"fast_{os.path.splitext(image_name)[0]}.jpg"
            output_path = os.path.join(output_dir, output_name)
            cv2.imwrite(output_path, visualization)
            print(f"  Output disimpan: {output_path}")

        except Exception as e:
            print(f"  Error: {e}")

        print()

    # Perbandingan threshold
    print("Membuat perbandingan threshold...")
    comparison_image = "building.jpg"
    comparison_path = os.path.join(data_dir, comparison_image)

    if os.path.exists(comparison_path):
        comparison = compare_thresholds(comparison_path)
        if comparison is not None:
            output_path = os.path.join(output_dir, "fast_threshold_comparison.jpg")
            cv2.imwrite(output_path, comparison)
            print(f"  Perbandingan disimpan: {output_path}")

    print()
    print("=" * 70)
    print("EKSPERIMEN YANG DISARANKAN:")
    print("=" * 70)
    print("""
1. Ubah FAST_THRESHOLD dari 20 ke 10
   - Amati: keypoint lebih banyak
   - Mengapa: threshold lebih longgar

2. Ubah FAST_THRESHOLD dari 20 ke 40
   - Amati: keypoint lebih sedikit
   - Mengapa: threshold lebih ketat

3. Set NONMAX_SUPPRESSION = False
   - Amati: keypoint sangat banyak
   - Mengapa: tidak ada filtering
""")

    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
