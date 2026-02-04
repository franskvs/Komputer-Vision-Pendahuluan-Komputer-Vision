"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 1: Lucas-Kanade Optical Flow

Deskripsi:
    Program ini mendemonstrasikan sparse optical flow menggunakan
    algoritma Lucas-Kanade. Metode ini melacak pergerakan features
    (keypoints) yang terdeteksi antar frame dalam video.

Teori:
    Lucas-Kanade mengasumsikan:
    1. Brightness constancy (intensitas piksel konstan)
    2. Spatial coherence (piksel tetangga bergerak sama)
    3. Small motion (gerakan kecil antar frame)
    
    Dengan menggunakan window di sekitar setiap point, algoritma
    mencari pergeseran (u, v) yang meminimalkan error.

Parameter yang dapat dimodifikasi:
    - MAX_CORNERS: Jumlah maksimum features untuk di-track
    - QUALITY_LEVEL: Threshold kualitas corner
    - MIN_DISTANCE: Jarak minimum antar features
    - WIN_SIZE: Ukuran window untuk Lucas-Kanade
    - MAX_LEVEL: Jumlah level pyramid

Output:
    - Video dengan tracking points dan trails
    - Visualisasi optical flow vectors

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

# Good Features to Track parameters
MAX_CORNERS = 100       # Jumlah maksimum corners/features
QUALITY_LEVEL = 0.3     # Kualitas minimum (0.0 - 1.0)
MIN_DISTANCE = 7        # Jarak minimum antar features (pixel)
BLOCK_SIZE = 7          # Ukuran block untuk corner detection

# Lucas-Kanade parameters
WIN_SIZE = (15, 15)     # Ukuran window untuk optical flow
MAX_LEVEL = 2           # Jumlah level pyramid (0 = no pyramid)

# Visualization parameters
TRACK_LENGTH = 30       # Panjang trail tracking

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output1")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def detect_features(gray):
    """
    Deteksi good features to track pada frame grayscale.
    
    Parameters:
        gray: Frame grayscale
    
    Returns:
        corners: Array of corner points (N, 1, 2)
    """
    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=MAX_CORNERS,
        qualityLevel=QUALITY_LEVEL,
        minDistance=MIN_DISTANCE,
        blockSize=BLOCK_SIZE
    )
    return corners

def calculate_optical_flow(prev_gray, curr_gray, prev_pts):
    """
    Hitung optical flow menggunakan Lucas-Kanade.
    
    Parameters:
        prev_gray: Frame grayscale sebelumnya
        curr_gray: Frame grayscale saat ini
        prev_pts: Points untuk di-track
    
    Returns:
        next_pts: Posisi baru dari points
        status: Status tracking (1=sukses, 0=gagal)
        error: Error tracking
    """
    # Parameter untuk Lucas-Kanade
    lk_params = dict(
        winSize=WIN_SIZE,
        maxLevel=MAX_LEVEL,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )
    
    next_pts, status, error = cv2.calcOpticalFlowPyrLK(
        prev_gray, curr_gray, prev_pts, None, **lk_params
    )
    
    return next_pts, status, error

def draw_tracks(frame, tracks, colors):
    """
    Gambar tracking trails pada frame.
    
    Parameters:
        frame: Frame untuk digambar
        tracks: List of track histories
        colors: Warna untuk setiap track
    
    Returns:
        frame: Frame dengan tracks
    """
    # Buat overlay untuk trails
    mask = np.zeros_like(frame)
    
    for i, track in enumerate(tracks):
        if len(track) > 1:
            color = colors[i % len(colors)].tolist()
            
            # Gambar trail line
            for j in range(1, len(track)):
                pt1 = tuple(map(int, track[j-1]))
                pt2 = tuple(map(int, track[j]))
                cv2.line(mask, pt1, pt2, color, 2)
            
            # Gambar current point
            cv2.circle(frame, tuple(map(int, track[-1])), 5, color, -1)
    
    # Combine frame dan mask
    output = cv2.add(frame, mask)
    
    return output

def draw_flow_vectors(frame, prev_pts, next_pts, status):
    """
    Gambar flow vectors pada frame.
    
    Parameters:
        frame: Frame untuk digambar
        prev_pts: Points sebelumnya
        next_pts: Points saat ini
        status: Status tracking
    
    Returns:
        frame: Frame dengan flow vectors
    """
    if prev_pts is None or next_pts is None:
        return frame
    
    for i, (prev, next_, st) in enumerate(zip(prev_pts, next_pts, status)):
        if st[0] == 1:
            x1, y1 = map(int, prev.ravel())
            x2, y2 = map(int, next_.ravel())
            
            # Gambar arrow
            cv2.arrowedLine(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (x1, y1), 3, (0, 0, 255), -1)
    
    return frame

def main():
    """
    Fungsi utama untuk Lucas-Kanade optical flow demo.
    """
    print("=" * 60)
    print("LUCAS-KANADE OPTICAL FLOW")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Cari video input
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
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video properties: {width}x{height} @ {fps} FPS")
    
    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "01_lucas_kanade_output.avi"),
        fourcc, fps, (width, height)
    )
    
    # Initialize
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame!")
        return
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_pts = detect_features(prev_gray)
    
    # Generate random colors for tracks
    colors = np.random.randint(0, 255, (MAX_CORNERS, 3))
    
    # Track histories
    tracks = [[] for _ in range(MAX_CORNERS)]
    
    if prev_pts is not None:
        for i, pt in enumerate(prev_pts):
            tracks[i].append(pt.ravel())
    
    frame_count = 0
    
    print("\nMulai tracking...")
    print("Tekan 'q' untuk keluar, 'r' untuk reset features")
    print("Tekan 's' untuk save screenshot")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if not using_webcam:
                # Loop video
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break
        
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_pts is not None and len(prev_pts) > 0:
            # Calculate optical flow
            next_pts, status, error = calculate_optical_flow(
                prev_gray, curr_gray, prev_pts
            )
            
            # Filter good points
            if next_pts is not None:
                good_new = next_pts[status.flatten() == 1]
                good_old = prev_pts[status.flatten() == 1]
                
                # Update tracks
                track_idx = 0
                for i, st in enumerate(status.flatten()):
                    if st == 1 and track_idx < len(good_new):
                        tracks[i].append(good_new[track_idx].ravel())
                        # Limit track length
                        if len(tracks[i]) > TRACK_LENGTH:
                            tracks[i] = tracks[i][-TRACK_LENGTH:]
                        track_idx += 1
                
                # Draw
                vis_frame = frame.copy()
                vis_frame = draw_tracks(vis_frame, tracks, colors)
                vis_frame = draw_flow_vectors(vis_frame, good_old.reshape(-1, 1, 2), 
                                             good_new.reshape(-1, 1, 2), 
                                             status[status.flatten() == 1].reshape(-1, 1))
                
                prev_pts = good_new.reshape(-1, 1, 2)
            else:
                vis_frame = frame.copy()
        else:
            vis_frame = frame.copy()
            # Re-detect features
            prev_pts = detect_features(curr_gray)
            tracks = [[] for _ in range(MAX_CORNERS)]
            if prev_pts is not None:
                for i, pt in enumerate(prev_pts):
                    if i < len(tracks):
                        tracks[i].append(pt.ravel())
        
        # Add info text
        cv2.putText(vis_frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(vis_frame, f"Points: {len(prev_pts) if prev_pts is not None else 0}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(vis_frame, "q:quit r:reset s:save", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Write to output
        out.write(vis_frame)
        
        # Display
        cv2.imshow("Lucas-Kanade Optical Flow", vis_frame)
        
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Reset features
            prev_pts = detect_features(curr_gray)
            tracks = [[] for _ in range(MAX_CORNERS)]
            if prev_pts is not None:
                for i, pt in enumerate(prev_pts):
                    if i < len(tracks):
                        tracks[i].append(pt.ravel())
            print(f"Reset: detected {len(prev_pts) if prev_pts is not None else 0} features")
        elif key == ord('s'):
            screenshot_path = os.path.join(OUTPUT_DIR, f"01_screenshot_{frame_count}.png")
            cv2.imwrite(screenshot_path, vis_frame)
            print(f"Saved: {screenshot_path}")
        
        prev_gray = curr_gray.copy()
        frame_count += 1
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\nSelesai! Total frames: {frame_count}")
    print(f"Output saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
