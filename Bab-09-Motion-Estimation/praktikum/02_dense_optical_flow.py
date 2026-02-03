"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 2: Dense Optical Flow (Farneback)

Deskripsi:
    Program ini mendemonstrasikan dense optical flow menggunakan
    algoritma Farneback. Berbeda dengan Lucas-Kanade yang sparse,
    Farneback menghitung flow untuk setiap pixel dalam frame.

Teori:
    Farneback method menggunakan polynomial expansion untuk
    merepresentasikan neighborhood setiap pixel, kemudian
    mengestimasi displacement berdasarkan polynomial coefficients.
    
    Multi-scale pyramid digunakan untuk handle large displacements.

Visualisasi:
    - Hue: Direction of motion (0-360 degrees)
    - Saturation: Magnitude of motion
    - Value: Brightness

Parameter yang dapat dimodifikasi:
    - PYR_SCALE: Scale factor untuk pyramid
    - LEVELS: Jumlah level pyramid
    - WINSIZE: Window size
    - ITERATIONS: Jumlah iterasi per level
    - POLY_N: Neighborhood size
    - POLY_SIGMA: Gaussian std untuk polynomial

Output:
    - Visualisasi HSV dari optical flow
    - Flow magnitude map

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Farneback parameters
PYR_SCALE = 0.5     # Scale untuk pyramid (<1)
LEVELS = 3          # Jumlah level pyramid
WINSIZE = 15        # Averaging window size
ITERATIONS = 3      # Iterasi per level
POLY_N = 5          # Neighborhood size (5 atau 7)
POLY_SIGMA = 1.2    # Gaussian std untuk polynomial expansion

# Visualization parameters
FLOW_THRESHOLD = 2  # Threshold untuk visualisasi (filter noise)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def calculate_dense_flow(prev_gray, curr_gray):
    """
    Hitung dense optical flow menggunakan Farneback method.
    
    Parameters:
        prev_gray: Frame grayscale sebelumnya
        curr_gray: Frame grayscale saat ini
    
    Returns:
        flow: Flow field (H, W, 2) dengan (dx, dy) per pixel
    """
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        pyr_scale=PYR_SCALE,
        levels=LEVELS,
        winsize=WINSIZE,
        iterations=ITERATIONS,
        poly_n=POLY_N,
        poly_sigma=POLY_SIGMA,
        flags=cv2.OPTFLOW_FARNEBACK_GAUSSIAN
    )
    
    return flow

def flow_to_hsv(flow):
    """
    Konversi flow field ke visualisasi HSV.
    
    Hue = direction (angle)
    Saturation = 255
    Value = magnitude (normalized)
    
    Parameters:
        flow: Flow field (H, W, 2)
    
    Returns:
        hsv_rgb: RGB visualization dari flow
    """
    h, w = flow.shape[:2]
    
    # Hitung magnitude dan angle
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    # Buat HSV image
    hsv = np.zeros((h, w, 3), dtype=np.uint8)
    hsv[..., 0] = ang * 180 / np.pi / 2  # Hue (0-180 dalam OpenCV)
    hsv[..., 1] = 255  # Saturation
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)  # Value
    
    # Convert to RGB
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return rgb

def flow_to_arrows(frame, flow, step=16, scale=1.0):
    """
    Visualisasi flow dengan arrow overlay.
    
    Parameters:
        frame: Frame untuk overlay
        flow: Flow field
        step: Step size untuk sampling
        scale: Scale factor untuk arrows
    
    Returns:
        output: Frame dengan arrows
    """
    h, w = flow.shape[:2]
    output = frame.copy()
    
    # Sample points
    y, x = np.mgrid[step//2:h:step, step//2:w:step].reshape(2, -1).astype(int)
    
    fx = flow[y, x, 0] * scale
    fy = flow[y, x, 1] * scale
    
    # Draw arrows
    for i in range(len(x)):
        if np.sqrt(fx[i]**2 + fy[i]**2) > FLOW_THRESHOLD:
            pt1 = (x[i], y[i])
            pt2 = (int(x[i] + fx[i]), int(y[i] + fy[i]))
            cv2.arrowedLine(output, pt1, pt2, (0, 255, 0), 1, tipLength=0.3)
    
    return output

def create_color_wheel():
    """
    Buat color wheel legend untuk visualisasi.
    """
    size = 100
    wheel = np.zeros((size, size, 3), dtype=np.uint8)
    
    center = size // 2
    
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            r = np.sqrt(dx**2 + dy**2)
            
            if r <= center:
                angle = np.arctan2(dy, dx)
                hue = int((angle + np.pi) * 90 / np.pi)  # 0-180
                sat = 255
                val = int(r * 255 / center)
                
                wheel[y, x] = [hue, sat, val]
    
    wheel = cv2.cvtColor(wheel, cv2.COLOR_HSV2BGR)
    return wheel

def main():
    """
    Fungsi utama untuk dense optical flow demo.
    """
    print("=" * 60)
    print("DENSE OPTICAL FLOW (FARNEBACK)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Cari video
    video_path = os.path.join(DATA_DIR, "moving_object.avi")
    
    if not os.path.exists(video_path):
        print("Video tidak ditemukan, menggunakan webcam...")
        cap = cv2.VideoCapture(0)
        using_webcam = True
    else:
        cap = cv2.VideoCapture(video_path)
        using_webcam = False
        print(f"Menggunakan video: {video_path}")
    
    if not cap.isOpened():
        print("ERROR: Tidak dapat membuka video/webcam!")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Resize untuk performance
    scale = 1.0
    if width > 640:
        scale = 640 / width
        width = 640
        height = int(height * scale)
    
    print(f"Processing at: {width}x{height}")
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "02_dense_flow_output.avi"),
        fourcc, fps, (width * 2, height)  # Side by side
    )
    
    # Read first frame
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame!")
        return
    
    if scale != 1.0:
        frame = cv2.resize(frame, (width, height))
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Color wheel legend
    color_wheel = create_color_wheel()
    
    frame_count = 0
    
    print("\nProcessing...")
    print("Tekan 'q' untuk keluar, 's' untuk save")
    print("\nLegend: Warna = arah gerakan, Brightness = kecepatan")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if not using_webcam:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            break
        
        if scale != 1.0:
            frame = cv2.resize(frame, (width, height))
        
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate dense flow
        flow = calculate_dense_flow(prev_gray, curr_gray)
        
        # Visualizations
        flow_hsv = flow_to_hsv(flow)
        flow_arrows = flow_to_arrows(frame, flow, step=20, scale=3.0)
        
        # Add color wheel legend
        wheel_h, wheel_w = color_wheel.shape[:2]
        flow_hsv[10:10+wheel_h, width-wheel_w-10:width-10] = color_wheel
        cv2.putText(flow_hsv, "Direction", (width-wheel_w-10, wheel_h+30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Calculate average motion
        mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        avg_motion = np.mean(mag)
        max_motion = np.max(mag)
        
        # Add info
        cv2.putText(flow_hsv, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(flow_hsv, f"Avg motion: {avg_motion:.2f}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(flow_hsv, f"Max motion: {max_motion:.2f}", (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.putText(flow_arrows, "Flow Vectors", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Combine views
        combined = np.hstack([flow_arrows, flow_hsv])
        
        # Write output
        out.write(combined)
        
        # Display
        cv2.imshow("Dense Optical Flow", combined)
        
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"02_dense_flow_{frame_count}.png"), combined)
            print(f"Saved frame {frame_count}")
        
        prev_gray = curr_gray.copy()
        frame_count += 1
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\nSelesai! Total frames: {frame_count}")
    print(f"Output saved to: {OUTPUT_DIR}")
    
    # Print parameter summary
    print("\n" + "=" * 60)
    print("PARAMETER YANG DIGUNAKAN:")
    print("=" * 60)
    print(f"  pyr_scale: {PYR_SCALE}")
    print(f"  levels: {LEVELS}")
    print(f"  winsize: {WINSIZE}")
    print(f"  iterations: {ITERATIONS}")
    print(f"  poly_n: {POLY_N}")
    print(f"  poly_sigma: {POLY_SIGMA}")

if __name__ == "__main__":
    main()
