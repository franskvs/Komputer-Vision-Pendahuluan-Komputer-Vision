"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 8: Frame Interpolation (Optical Flow)

Deskripsi:
    Program ini membuat frame tengah (t=0.5) di antara dua frame
    menggunakan dense optical flow (Farneback) dan warping.

Aplikasi nyata:
    - Slow-motion video
    - Frame rate up-conversion (TV/monitor)
    - Video restoration

Output:
    - Gambar interpolasi
    - Perbandingan sebelum/sesudah

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
AUTO_CLOSE_SECONDS = 2.0  # Auto close window (detik)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output8")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def create_synthetic_pair(size=(480, 640), shift=(16, 0)):
    """Buat pasangan gambar sintetis untuk testing."""
    h, w = size
    base = np.zeros((h, w, 3), dtype=np.uint8)

    cv2.rectangle(base, (80, 120), (220, 260), (0, 255, 255), -1)
    cv2.circle(base, (420, 300), 45, (255, 0, 255), -1)
    cv2.putText(base, "Interp", (260, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    dx, dy = shift
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted = cv2.warpAffine(base, M, (w, h))

    return base, shifted


def warp_with_flow(img, flow):
    """Warp image dengan flow field."""
    h, w = img.shape[:2]
    grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (grid_x + flow[..., 0]).astype(np.float32)
    map_y = (grid_y + flow[..., 1]).astype(np.float32)
    return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img1_path = os.path.join(DATA_DIR, "frame1.png")
    img2_path = os.path.join(DATA_DIR, "frame2.png")

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("Frame sample tidak ditemukan, membuat pasangan sintetis...")
        img1, img2 = create_synthetic_pair()

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Optical flow forward & backward
    flow_12 = cv2.calcOpticalFlowFarneback(
        img1_gray, img2_gray, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    flow_21 = cv2.calcOpticalFlowFarneback(
        img2_gray, img1_gray, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )

    # Interpolate at t=0.5
    t = 0.5
    warp1 = warp_with_flow(img1, flow_12 * t)
    warp2 = warp_with_flow(img2, flow_21 * (1 - t))
    interp = cv2.addWeighted(warp1, 0.5, warp2, 0.5, 0)

    # Compose visualization
    combined = np.hstack([img1, interp, img2])
    cv2.putText(combined, "Frame 1", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined, "Interpolated", (img1.shape[1] + 20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined, "Frame 2", (img1.shape[1] * 2 + 20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    output_path = os.path.join(OUTPUT_DIR, "08_interpolated.png")
    cv2.imwrite(output_path, combined)

    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Output saved: {output_path}")

    start_time = time.time()
    while True:
        cv2.imshow("Frame Interpolation", combined)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if AUTO_CLOSE_SECONDS > 0 and (time.time() - start_time) >= AUTO_CLOSE_SECONDS:
            print("Auto-close: waktu uji selesai.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
