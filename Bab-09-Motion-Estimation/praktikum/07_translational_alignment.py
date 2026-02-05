"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 7: Translational Alignment (SSD & Phase Correlation)

Deskripsi:
    Program ini menunjukkan cara memperkirakan pergeseran translasi
    antar dua frame menggunakan:
    1) Pencarian SSD (sum of squared differences) berbasis window
    2) Phase correlation (FFT) untuk estimasi cepat

Aplikasi nyata:
    - Image registration untuk stabilisasi video
    - Penyelarasan frame sebelum kompresi
    - Estimasi motion sederhana pada kamera statis

Output:
    - Estimasi dx, dy dari dua metode
    - Visualisasi overlay sebelum/sesudah align
    - File output PNG

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import time

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================
SEARCH_RANGE = 20  # Range pencarian SSD (+/- pixel)
AUTO_CLOSE_SECONDS = 2.0  # Auto close window (detik)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output7")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def create_synthetic_pair(size=(480, 640), shift=(12, -8)):
    """Buat pasangan gambar sintetis untuk testing."""
    h, w = size
    base = np.zeros((h, w, 3), dtype=np.uint8)

    cv2.rectangle(base, (50, 50), (200, 200), (0, 255, 0), -1)
    cv2.circle(base, (450, 300), 40, (255, 0, 0), -1)
    cv2.putText(base, "Motion", (250, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    dx, dy = shift
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted = cv2.warpAffine(base, M, (w, h))

    return base, shifted


def ssd_alignment(img1_gray, img2_gray, search_range=20):
    """Cari pergeseran terbaik dengan SSD (integer shift)."""
    h, w = img1_gray.shape
    best_score = float("inf")  # Skor terbaik (minimum SSD)
    best_shift = (0, 0)  # Shift terbaik (dx, dy)

    # Brute force search: coba semua kemungkinan shift dalam range
    for dy in range(-search_range, search_range + 1):
        for dx in range(-search_range, search_range + 1):
            # Hitung overlap region untuk shift (dx, dy)
            x1 = max(0, dx)   # Start x di img1
            y1 = max(0, dy)   # Start y di img1
            x2 = max(0, -dx)  # Start x di img2
            y2 = max(0, -dy)  # Start y di img2

            ww = w - abs(dx)  # Width overlap region
            hh = h - abs(dy)  # Height overlap region
            if ww <= 0 or hh <= 0:  # Skip jika tidak ada overlap
                continue

            # Ambil patch yang overlap dari kedua gambar
            patch1 = img1_gray[y1:y1 + hh, x1:x1 + ww]
            patch2 = img2_gray[y2:y2 + hh, x2:x2 + ww]

            # Hitung SSD: Sum of Squared Differences
            ssd = np.sum((patch1.astype(np.float32) - patch2.astype(np.float32)) ** 2)
            # Update best jika skor lebih kecil (lebih mirip)
            if ssd < best_score:
                best_score = ssd
                best_shift = (dx, dy)

    return best_shift, best_score


def apply_shift(img, shift):
    """Warp image dengan translasi."""
    dx, dy = shift
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))


def load_frame_pair():
    """Coba ambil pasangan frame dari video, lalu fallback ke images/synthetic."""
    video_path = os.path.join(DATA_DIR, "videos", "moving_object.avi")
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        ret1, f1 = cap.read()
        ret2, f2 = cap.read()
        cap.release()
        if ret1 and ret2:
            return f1, f2

    img1_path = os.path.join(DATA_DIR, "images", "frame1.png")
    img2_path = os.path.join(DATA_DIR, "images", "frame2.png")

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is not None and img2 is not None and img1.shape == img2.shape:
        return img1, img2

    print("Frame sample tidak ditemukan/ukuran tidak cocok, membuat pasangan sintetis...")
    return create_synthetic_pair()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img1, img2 = load_frame_pair()

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # SSD alignment (brute force, integer precision)
    (dx_ssd, dy_ssd), ssd_score = ssd_alignment(img1_gray, img2_gray, SEARCH_RANGE)

    # cv2.phaseCorrelate: Estimasi shift dengan FFT-based phase correlation
    # Lebih cepat dari SSD, bisa sub-pixel precision
    # Input: dua grayscale image sebagai float32
    # Output: (dx,dy) shift dan response quality
    shift_pc, response = cv2.phaseCorrelate(np.float32(img1_gray), np.float32(img2_gray))
    dx_pc, dy_pc = shift_pc  # Unpack shift

    # Apply shift untuk align gambar ke img1
    # Shift negatif karena kita align img2 ke img1 (balik arah shift)
    aligned_ssd = apply_shift(img2, (-dx_ssd, -dy_ssd))  # Align dengan SSD result
    aligned_pc = apply_shift(img2, (-dx_pc, -dy_pc))      # Align dengan phase correlation

    overlay_before = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    overlay_ssd = cv2.addWeighted(img1, 0.5, aligned_ssd, 0.5, 0)
    overlay_pc = cv2.addWeighted(img1, 0.5, aligned_pc, 0.5, 0)

    # Compose visualization
    top = np.hstack([img1, img2])
    bottom = np.hstack([overlay_before, overlay_ssd])
    combined = np.vstack([top, bottom])

    cv2.putText(combined, f"SSD shift: ({dx_ssd}, {dy_ssd})", (10, combined.shape[0] - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined, f"PhaseCorr shift: ({dx_pc:.2f}, {dy_pc:.2f})", (10, combined.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    output_path = os.path.join(OUTPUT_DIR, "07_alignment_result.png")
    cv2.imwrite(output_path, combined)

    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"SSD shift: ({dx_ssd}, {dy_ssd}) | score: {ssd_score:.2f}")
    print(f"Phase correlation shift: ({dx_pc:.2f}, {dy_pc:.2f}) | response: {response:.3f}")
    print(f"Output saved: {output_path}")

    start_time = time.time()
    while True:
        cv2.imshow("Translational Alignment", combined)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if AUTO_CLOSE_SECONDS > 0 and (time.time() - start_time) >= AUTO_CLOSE_SECONDS:
            print("Auto-close: waktu uji selesai.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
