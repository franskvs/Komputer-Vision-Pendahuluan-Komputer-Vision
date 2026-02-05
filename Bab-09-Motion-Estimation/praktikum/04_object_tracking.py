"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 4: Object Tracking

Deskripsi:
    Program ini mendemonstrasikan tracking objek menggunakan
    berbagai algoritma tracking dari OpenCV. User dapat memilih
    objek untuk di-track, dan sistem akan mengikuti objek tersebut.

Tracker yang Tersedia:
    - CSRT: Accurate, slower (recommended for most cases)
    - KCF: Fast, good accuracy
    - MOSSE: Very fast, less accurate
    - MIL: Multiple Instance Learning

Teori:
    Object tracking berbeda dari detection:
    - Detection: menemukan objek di setiap frame independen
    - Tracking: mengikuti objek yang sama antar frames
    
    Tracking lebih efisien karena menggunakan informasi dari
    frame sebelumnya untuk memprediksi lokasi di frame berikutnya.

Parameter yang dapat dimodifikasi:
    - TRACKER_TYPE: Tipe tracker yang digunakan
    - TRAIL_LENGTH: Panjang trail trajectory

Output:
    - Video dengan bounding box tracking
    - Trajectory visualization

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import time
from collections import deque

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Tipe tracker: 'CSRT', 'KCF', 'MOSSE', 'MIL'
TRACKER_TYPE = 'CSRT'

# Panjang trail trajectory
TRAIL_LENGTH = 50

# Auto close window (detik) untuk testing cepat
AUTO_CLOSE_SECONDS = 2.0

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output4")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def create_tracker(tracker_type):
    """
    Buat tracker berdasarkan tipe yang dipilih.
    
    Parameters:
        tracker_type: Tipe tracker
    
    Returns:
        tracker: OpenCV tracker object
    """
    # Fungsi nested untuk mencari tracker factory dengan fallback
    # Tracker API bisa di cv2 atau cv2.legacy tergantung versi OpenCV
    def get_tracker_factory(name):
        # Coba CSRT: accurate tapi lebih lambat
        if name == 'CSRT':
            if hasattr(cv2, 'TrackerCSRT_create'):  # OpenCV >= 4.5.1
                return cv2.TrackerCSRT_create
            if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerCSRT_create'):  # OpenCV 4.5.4+
                return cv2.legacy.TrackerCSRT_create
        # Coba KCF: balance speed dan accuracy
        if name == 'KCF':
            if hasattr(cv2, 'TrackerKCF_create'):
                return cv2.TrackerKCF_create
            if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerKCF_create'):
                return cv2.legacy.TrackerKCF_create
        # Coba MOSSE: sangat cepat tapi kurang akurat
        if name == 'MOSSE':
            if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerMOSSE_create'):
                return cv2.legacy.TrackerMOSSE_create
        # Coba MIL: Multiple Instance Learning
        if name == 'MIL':
            if hasattr(cv2, 'TrackerMIL_create'):
                return cv2.TrackerMIL_create
            if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerMIL_create'):
                return cv2.legacy.TrackerMIL_create
        return None  # Tracker tidak ditemukan

    # Coba buat tracker sesuai type yang diminta
    create_func = get_tracker_factory(tracker_type)

    # Jika tracker tidak tersedia, coba fallback ke tracker lain
    if create_func is None:
        for fallback in ['KCF', 'MIL', 'CSRT', 'MOSSE']:
            create_func = get_tracker_factory(fallback)
            if create_func is not None:
                print(f"Tracker {tracker_type} tidak tersedia, menggunakan {fallback}")
                return create_func(), fallback  # Return tracker dan nama fallback
        # Jika semua gagal, raise error
        raise RuntimeError("Tidak ada tracker OpenCV yang tersedia.")

    # Sukses: return tracker dan nama asli
    return create_func(), tracker_type

def select_roi_auto(frame):
    """
    Otomatis pilih ROI berdasarkan motion detection.
    
    Parameters:
        frame: Frame untuk analisis
    
    Returns:
        bbox: Bounding box (x, y, w, h) atau None
    """
    # Deteksi otomatis objek berdasarkan edge detection
    # Konversi ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.GaussianBlur: Smooth image untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # cv2.Canny: Deteksi edge dengan threshold 50-150
    edges = cv2.Canny(blurred, 50, 150)
    
    # Cari kontur dari edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Ambil kontur terbesar (kemungkinan objek utama)
        largest = max(contours, key=cv2.contourArea)
        # Filter: hanya jika area > 500 pixel (buang noise)
        if cv2.contourArea(largest) > 500:
            # Dapatkan bounding box dari kontur
            x, y, w, h = cv2.boundingRect(largest)
            return (x, y, w, h)
    
    return None  # Tidak ada objek terdeteksi

def draw_trajectory(frame, trajectory, color=(0, 255, 0)):
    """
    Gambar trajectory dari posisi sebelumnya.
    
    Parameters:
        frame: Frame untuk digambar
        trajectory: Deque dari posisi (x, y)
        color: Warna trajectory
    """
    # Konversi deque ke list untuk iterasi
    points = list(trajectory)
    
    # Gambar garis menghubungkan titik-titik dalam trajectory
    for i in range(1, len(points)):
        # Skip jika ada None value
        if points[i-1] is None or points[i] is None:
            continue
        
        # Fade effect: garis lama lebih tipis/transparan
        # np.sqrt: buat efek non-linear fade
        thickness = int(np.sqrt(TRAIL_LENGTH / float(i + 1)) * 2.5)
        alpha = float(i) / len(points)  # Alpha untuk transparency (not used here)
        
        # Konversi koordinat float ke integer tuple
        pt1 = tuple(map(int, points[i-1]))  # Titik sebelumnya
        pt2 = tuple(map(int, points[i]))    # Titik sekarang
        
        # cv2.line: Gambar garis dengan thickness dinamis (fade effect)
        cv2.line(frame, pt1, pt2, color, max(1, thickness))

def main():
    """
    Fungsi utama untuk object tracking demo.
    """
    print("=" * 60)
    print("OBJECT TRACKING")
    print("=" * 60)
    print(f"Tracker: {TRACKER_TYPE}")
    
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
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "04_object_tracking_output.avi"),
        fourcc, fps, (width, height)
    )
    
    # Read first frame
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame!")
        return
    
    # Select ROI
    print("\nPilih objek untuk di-track dengan mouse, lalu tekan ENTER")
    print("Atau tekan 'c' untuk auto-detect, 's' untuk skip")
    
    bbox = None
    
    # Auto-detect for video
    if not using_webcam:
        bbox = select_roi_auto(frame)
        if bbox:
            print(f"Auto-detected object at: {bbox}")
    
    if bbox is None:
        cv2.putText(frame, "Draw box around object to track", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press SPACE/ENTER when done", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Object")
    
    if bbox == (0, 0, 0, 0) or bbox is None:
        print("Tidak ada objek dipilih!")
        # Use center as default
        bbox = (width//4, height//4, width//2, height//2)
    
    # Initialize tracker
    tracker, current_tracker_type = create_tracker(TRACKER_TYPE)
    tracker.init(frame, bbox)
    
    # Trajectory
    trajectory = deque(maxlen=TRAIL_LENGTH)
    
    # Stats
    frame_count = 0
    tracking_success = 0
    start_time = time.time()
    
    print("\nTracking...")
    print("Tekan 'q' untuk keluar, 'r' untuk re-select")
    print("Tekan '1' untuk CSRT, '2' untuk KCF, '3' untuk MOSSE")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if not using_webcam:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                # Reinitialize tracker
                ret, frame = cap.read()
                tracker, current_tracker_type = create_tracker(current_tracker_type)
                if bbox:
                    tracker.init(frame, bbox)
                trajectory.clear()
                continue
            break
        
        # Update tracker
        success, box = tracker.update(frame)
        
        vis_frame = frame.copy()
        
        if success:
            tracking_success += 1
            
            # Get center point
            x, y, w, h = [int(v) for v in box]
            center = (x + w // 2, y + h // 2)
            trajectory.append(center)
            
            # Draw bounding box
            cv2.rectangle(vis_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(vis_frame, center, 5, (0, 0, 255), -1)
            
            # Draw trajectory
            draw_trajectory(vis_frame, trajectory)
            
            status = "Tracking"
            status_color = (0, 255, 0)
        else:
            trajectory.append(None)
            status = "Lost"
            status_color = (0, 0, 255)
        
        # Add info
        cv2.putText(vis_frame, f"Tracker: {current_tracker_type}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(vis_frame, f"Status: {status}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(vis_frame, f"Frame: {frame_count}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        success_rate = (tracking_success / max(1, frame_count)) * 100
        cv2.putText(vis_frame, f"Success: {success_rate:.1f}%", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(vis_frame, "q:quit r:reselect 1:CSRT 2:KCF 3:MOSSE", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Write
        out.write(vis_frame)
        
        # Display
        cv2.imshow("Object Tracking", vis_frame)
        
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Re-select object
            bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Select Object")
            if bbox != (0, 0, 0, 0):
                tracker, current_tracker_type = create_tracker(current_tracker_type)
                tracker.init(frame, bbox)
                trajectory.clear()
                print("Re-initialized tracker")
        elif key == ord('s'):
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"04_tracking_{frame_count}.png"), vis_frame)
            print(f"Saved frame {frame_count}")
        elif key == ord('1'):
            if bbox:
                tracker, current_tracker_type = create_tracker('CSRT')
                tracker.init(frame, bbox)
            print(f"Switched to {current_tracker_type}")
        elif key == ord('2'):
            if bbox:
                tracker, current_tracker_type = create_tracker('KCF')
                tracker.init(frame, bbox)
            print(f"Switched to {current_tracker_type}")
        elif key == ord('3'):
            if bbox:
                tracker, current_tracker_type = create_tracker('MOSSE')
                tracker.init(frame, bbox)
            print(f"Switched to {current_tracker_type}")
        
        frame_count += 1

        if AUTO_CLOSE_SECONDS > 0 and not using_webcam:
            if (time.time() - start_time) >= AUTO_CLOSE_SECONDS:
                print("Auto-close: waktu uji selesai.")
                break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Stats
    print("\n" + "=" * 60)
    print("TRACKING STATISTICS")
    print("=" * 60)
    print(f"Total frames: {frame_count}")
    print(f"Successful tracking: {tracking_success}")
    print(f"Success rate: {(tracking_success/max(1,frame_count))*100:.1f}%")
    print(f"Tracker used: {current_tracker_type}")

if __name__ == "__main__":
    main()
