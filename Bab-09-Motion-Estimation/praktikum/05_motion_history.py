"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 5: Motion History Image

Deskripsi:
    Program ini mendemonstrasikan Motion History Image (MHI),
    sebuah teknik untuk memvisualisasikan history pergerakan
    dalam satu gambar. Piksel yang lebih terang menunjukkan
    gerakan yang lebih baru.

Teori:
    MHI merepresentasikan temporal information dalam spatial form:
    - Setiap kali ada motion, set nilai timestamp pada pixel
    - Nilai berkurang seiring waktu (decay)
    - Gradient pada MHI menunjukkan direction of motion

Kegunaan:
    - Gesture recognition
    - Action recognition
    - Silhouette analysis
    - Motion segmentation

Parameter yang dapat dimodifikasi:
    - MHI_DURATION: Durasi history (frames)
    - MOTION_THRESHOLD: Threshold untuk deteksi motion

Output:
    - Motion History Image
    - Motion gradient visualization
    - Motion segmentation

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

# Durasi history (dalam timestamp units)
MHI_DURATION = 0.5  # seconds

# Threshold untuk motion detection
MOTION_THRESHOLD = 32

# Minimum area untuk valid motion region
MIN_AREA = 1000

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output5")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def update_mhi(mhi, silhouette, timestamp, duration):
    """
    Update Motion History Image.
    
    Parameters:
        mhi: Current MHI
        silhouette: Binary motion mask
        timestamp: Current timestamp
        duration: Duration of history
    
    Returns:
        mhi: Updated MHI
    """
    # Update MHI
    cv2.motempl.updateMotionHistory(silhouette, mhi, timestamp, duration)
    return mhi

def calculate_motion_gradient(mhi, duration):
    """
    Hitung gradient dari MHI untuk mendapatkan direction of motion.
    
    Parameters:
        mhi: Motion History Image
        duration: Duration parameter
    
    Returns:
        magnitude: Motion magnitude
        orientation: Motion orientation (angle)
        mask: Valid motion mask
    """
    # Calculate motion gradient
    mg_mask, mg_orient = cv2.motempl.calcMotionGradient(
        mhi, 0.25, 0.05,
        apertureSize=5
    )
    
    return mg_mask, mg_orient

def visualize_mhi(mhi, timestamp, duration):
    """
    Visualisasi MHI dengan colormap.
    
    Parameters:
        mhi: Motion History Image
        timestamp: Current timestamp
        duration: Duration parameter
    
    Returns:
        vis: Colored visualization
    """
    # Normalize MHI for visualization
    # Recent motion is brighter
    vis = np.clip((mhi - (timestamp - duration)) / duration, 0, 1)
    vis = (vis * 255).astype(np.uint8)
    
    # Apply colormap
    vis_colored = cv2.applyColorMap(vis, cv2.COLORMAP_JET)
    
    return vis_colored

def visualize_motion_direction(frame, mhi, mg_mask, mg_orient, step=16):
    """
    Visualisasi arah gerakan dengan arrows.
    
    Parameters:
        frame: Original frame
        mhi: Motion History Image
        mg_mask: Motion gradient mask
        mg_orient: Motion orientation
        step: Sampling step
    
    Returns:
        vis: Frame dengan direction arrows
    """
    vis = frame.copy()
    h, w = mhi.shape
    
    for y in range(step, h - step, step):
        for x in range(step, w - step, step):
            # Check if there's valid motion
            if mg_mask[y, x] > 0 and mhi[y, x] > 0:
                angle = mg_orient[y, x]
                
                # Calculate arrow endpoint
                length = 15
                dx = int(length * np.cos(angle))
                dy = int(length * np.sin(angle))
                
                cv2.arrowedLine(vis, (x, y), (x + dx, y + dy), 
                              (0, 255, 0), 2, tipLength=0.3)
    
    return vis

def segment_motion(mhi, timestamp, duration, min_area=MIN_AREA):
    """
    Segment motion regions dari MHI.
    
    Parameters:
        mhi: Motion History Image
        timestamp: Current timestamp
        duration: Duration parameter
        min_area: Minimum area for valid segment
    
    Returns:
        segments: List of motion segments (boundingRect)
    """
    # Create binary mask of recent motion
    mask = ((mhi > (timestamp - duration * 0.5)) * 255).astype(np.uint8)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    segments = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area:
            x, y, w, h = cv2.boundingRect(contour)
            segments.append((x, y, w, h, area))
    
    return segments

def main():
    """
    Fungsi utama untuk Motion History Image demo.
    """
    print("=" * 60)
    print("MOTION HISTORY IMAGE")
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
    
    print(f"Video: {width}x{height} @ {fps} FPS")
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "05_motion_history_output.avi"),
        fourcc, fps, (width * 2, height)
    )
    
    # Initialize MHI
    mhi = np.zeros((height, width), np.float32)
    
    # Read first frame
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame!")
        return
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    frame_count = 0
    start_time = time.time()
    
    print("\nProcessing...")
    print("Tekan 'q' untuk keluar, 's' untuk save")
    print("Tekan '+'/'-' untuk adjust duration")
    
    current_duration = MHI_DURATION
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if not using_webcam:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                mhi = np.zeros((height, width), np.float32)
                continue
            break
        
        timestamp = time.time() - start_time
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate frame difference
        diff = cv2.absdiff(gray, prev_gray)
        _, silhouette = cv2.threshold(diff, MOTION_THRESHOLD, 1, cv2.THRESH_BINARY)
        
        # Update MHI
        mhi = update_mhi(mhi, silhouette, timestamp, current_duration)
        
        # Calculate motion gradient
        mg_mask, mg_orient = calculate_motion_gradient(mhi, current_duration)
        
        # Visualizations
        mhi_vis = visualize_mhi(mhi, timestamp, current_duration)
        direction_vis = visualize_motion_direction(frame, mhi, mg_mask, mg_orient)
        
        # Segment motion
        segments = segment_motion(mhi, timestamp, current_duration)
        
        # Draw segments on original frame
        vis_frame = frame.copy()
        for (x, y, w, h, area) in segments:
            cv2.rectangle(vis_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Add info
        cv2.putText(mhi_vis, "Motion History Image", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(mhi_vis, f"Duration: {current_duration:.2f}s", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(mhi_vis, f"Segments: {len(segments)}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.putText(vis_frame, "Motion Segments", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(vis_frame, f"Frame: {frame_count}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(vis_frame, "+/-: duration q:quit s:save", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Color bar for MHI
        # Recent motion = red/yellow, old motion = blue
        bar_h = 20
        bar_w = width - 40
        color_bar = np.zeros((bar_h, bar_w, 3), dtype=np.uint8)
        for i in range(bar_w):
            val = int(255 * i / bar_w)
            color_bar[:, i] = cv2.applyColorMap(np.array([[val]], dtype=np.uint8), 
                                                 cv2.COLORMAP_JET)[0, 0]
        mhi_vis[height - 40:height - 20, 20:20 + bar_w] = color_bar
        cv2.putText(mhi_vis, "Old", (20, height - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(mhi_vis, "Recent", (width - 60, height - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Combine
        combined = np.hstack([vis_frame, mhi_vis])
        
        # Write
        out.write(combined)
        
        # Display
        cv2.imshow("Motion History Image", combined)
        
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"05_mhi_{frame_count}.png"), combined)
            print(f"Saved frame {frame_count}")
        elif key == ord('+') or key == ord('='):
            current_duration = min(2.0, current_duration + 0.1)
            print(f"Duration: {current_duration:.2f}s")
        elif key == ord('-'):
            current_duration = max(0.1, current_duration - 0.1)
            print(f"Duration: {current_duration:.2f}s")
        
        prev_gray = gray.copy()
        frame_count += 1
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\nSelesai! Total frames: {frame_count}")
    print(f"Output saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
