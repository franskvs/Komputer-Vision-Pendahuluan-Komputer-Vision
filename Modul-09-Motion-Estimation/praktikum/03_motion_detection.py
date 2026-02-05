"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 3: Motion Detection

Deskripsi:
    Program ini mendemonstrasikan deteksi gerakan menggunakan
    background subtraction. Metode ini membandingkan frame saat ini
    dengan model background untuk menemukan objek yang bergerak.

Metode yang Diimplementasi:
    1. Frame Differencing: Simpel, bandingkan frame berturut-turut
    2. MOG2 (Mixture of Gaussians): Adaptive, handle shadows
    3. KNN (K-Nearest Neighbors): Robust untuk berbagai kondisi

Teori:
    Background subtraction membangun model statistik dari background
    scene, kemudian mengidentifikasi piksel foreground (bergerak)
    berdasarkan perbedaan dengan model tersebut.

Parameter yang dapat dimodifikasi:
    - METHOD: Metode yang digunakan ('MOG2', 'KNN', 'DIFF')
    - LEARNING_RATE: Kecepatan adaptasi background
    - MIN_AREA: Area minimum untuk deteksi valid

Output:
    - Foreground mask
    - Bounding boxes pada objek bergerak
    - Motion detection statistics

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

# Metode background subtraction: 'MOG2', 'KNN', 'DIFF'
METHOD = 'MOG2'

# Learning rate untuk adaptive methods (0 = tidak update, 1 = update penuh)
LEARNING_RATE = 0.01

# Minimum area untuk dianggap sebagai deteksi valid (filter noise)
MIN_AREA = 500

# Threshold untuk frame differencing
DIFF_THRESHOLD = 30

# Morphological kernel size
KERNEL_SIZE = 5

# Auto close window (detik) untuk testing cepat
AUTO_CLOSE_SECONDS = 2.0

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output3")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def create_background_subtractor(method):
    """
    Buat background subtractor berdasarkan metode yang dipilih.
    
    Parameters:
        method: 'MOG2', 'KNN', atau 'DIFF'
    
    Returns:
        bg_subtractor: Object background subtractor
    """
    if method == 'MOG2':
        # cv2.createBackgroundSubtractorMOG2: Mixture of Gaussians adaptive method
        # Parameter:
        # - history: jumlah frame untuk membangun model background
        # - varThreshold: threshold untuk mahalanobis distance (deteksi foreground)
        # - detectShadows: True = deteksi dan tandai shadow (nilai 127 di mask)
        return cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )
    elif method == 'KNN':
        # cv2.createBackgroundSubtractorKNN: K-Nearest Neighbors method
        # Parameter:
        # - history: jumlah frame untuk membangun model
        # - dist2Threshold: threshold squared distance untuk deteksi foreground
        # - detectShadows: deteksi shadow
        return cv2.createBackgroundSubtractorKNN(
            history=500,
            dist2Threshold=400.0,
            detectShadows=True
        )
    else:  # DIFF - frame differencing manual (tidak ada object subtractor)
        return None

def apply_morphology(mask):
    """
    Aplikasikan operasi morphological untuk membersihkan mask.
    
    Parameters:
        mask: Binary mask
    
    Returns:
        cleaned: Cleaned mask
    """
    # cv2.getStructuringElement: Buat kernel ellipse untuk morphological operations
    # MORPH_ELLIPSE: bentuk elips, lebih smooth dibanding rectangle
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KERNEL_SIZE, KERNEL_SIZE))
    
    # cv2.morphologyEx MORPH_OPEN: erosi kemudian dilasi
    # Menghilangkan noise kecil (white dots) di foreground
    cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # cv2.morphologyEx MORPH_CLOSE: dilasi kemudian erosi
    # Mengisi lubang kecil (black holes) di dalam objek foreground
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    
    # cv2.dilate: Perlebar region foreground sedikit
    # iterations=2: lakukan dilasi 2 kali untuk memperbesar deteksi
    cleaned = cv2.dilate(cleaned, kernel, iterations=2)
    
    return cleaned

def find_moving_objects(mask):
    """
    Temukan objek bergerak dari mask.
    
    Parameters:
        mask: Binary mask
    
    Returns:
        objects: List of (x, y, w, h, area) untuk setiap objek
    """
    # cv2.findContours: Temukan kontur (outline) dari objek di mask
    # Parameter:
    # - mask: binary image (255=foreground, 0=background)
    # - RETR_EXTERNAL: hanya ambil kontur terluar (ignore holes)
    # - CHAIN_APPROX_SIMPLE: compress kontur (hanya simpan endpoint)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    objects = []  # List untuk menyimpan objek yang terdeteksi
    for contour in contours:
        # cv2.contourArea: Hitung luas area kontur
        area = cv2.contourArea(contour)
        # Filter: hanya ambil objek dengan area >= MIN_AREA (buang noise kecil)
        if area >= MIN_AREA:
            # cv2.boundingRect: Dapatkan bounding box (x,y,w,h) dari kontur
            x, y, w, h = cv2.boundingRect(contour)
            objects.append((x, y, w, h, area))  # Simpan info objek
    
    return objects

def draw_detections(frame, objects, mask):
    """
    Gambar deteksi pada frame.
    
    Parameters:
        frame: Frame untuk digambar
        objects: List objek terdeteksi
        mask: Foreground mask
    
    Returns:
        output: Frame dengan visualisasi
    """
    output = frame.copy()  # Copy frame agar asli tidak berubah
    
    # Gambar bounding box untuk setiap objek terdeteksi
    for (x, y, w, h, area) in objects:
        # cv2.rectangle: Gambar kotak hijau di sekitar objek
        # (x,y) = pojok kiri atas, (x+w, y+h) = pojok kanan bawah
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Tampilkan area objek di atas bounding box
        cv2.putText(output, f"Area: {area}", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Buat colored mask overlay untuk visualisasi foreground
    mask_colored = np.zeros_like(frame)  # Array kosong seperti frame
    mask_colored[:, :, 1] = mask  # Set green channel dengan mask (hijau = foreground)
    
    # cv2.addWeighted: Blend frame asli dengan mask colored (transparency)
    # Formula: output = frame*1.0 + mask_colored*0.3 + 0
    # 0.3 = alpha transparency (30% mask, 70% frame)
    output = cv2.addWeighted(output, 1.0, mask_colored, 0.3, 0)
    
    return output

def frame_differencing(prev_frame, curr_frame, threshold=DIFF_THRESHOLD):
    """
    Deteksi motion dengan frame differencing sederhana.
    
    Parameters:
        prev_frame: Frame sebelumnya (grayscale)
        curr_frame: Frame saat ini (grayscale)
        threshold: Threshold untuk binarisasi
    
    Returns:
        mask: Binary motion mask
    """
    # cv2.absdiff: Hitung absolute difference antara dua frame
    # |prev_frame - curr_frame| = deteksi pixel yang berubah
    diff = cv2.absdiff(prev_frame, curr_frame)
    # cv2.threshold: Binarisasi difference image
    # Pixel > threshold = 255 (motion), sisanya = 0 (static)
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return mask

def main():
    """
    Fungsi utama untuk motion detection demo.
    """
    print("=" * 60)
    print("MOTION DETECTION")
    print("=" * 60)
    print(f"Metode: {METHOD}")
    
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
    
    # Create background subtractor
    bg_subtractor = create_background_subtractor(METHOD)
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "03_motion_detection_output.avi"),
        fourcc, fps, (width * 2, height)
    )
    
    # For frame differencing
    prev_gray = None
    
    # Statistics
    motion_history = deque(maxlen=100)
    frame_count = 0
    total_detections = 0
    start_time = time.time()
    
    print("\nProcessing...")
    print("Tekan 'q' untuk keluar, 's' untuk save")
    print("Tekan '1' untuk MOG2, '2' untuk KNN, '3' untuk DIFF")
    
    current_method = METHOD
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if not using_webcam:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            break
        
        # Konversi ke grayscale untuk frame differencing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplikasikan metode background subtraction sesuai pilihan
        if current_method == 'DIFF':
            # Frame differencing: bandingkan frame sekarang dengan sebelumnya
            if prev_gray is not None:
                fg_mask = frame_differencing(prev_gray, gray)
            else:
                # Frame pertama: mask kosong
                fg_mask = np.zeros_like(gray)
            prev_gray = gray.copy()  # Simpan untuk iterasi berikutnya
        else:
            # MOG2/KNN: apply adaptive background subtractor
            # learningRate: rate adaptasi background model (0=static, 1=full update)
            fg_mask = bg_subtractor.apply(frame, learningRate=LEARNING_RATE)
            
            # Hapus shadow pixels (nilai 127 di MOG2/KNN)
            # Shadow bukan foreground sebenarnya, set ke 0 (background)
            fg_mask[fg_mask == 127] = 0
        
        # Clean mask
        clean_mask = apply_morphology(fg_mask)
        
        # Temukan objek bergerak dari mask yang sudah dibersihkan
        objects = find_moving_objects(clean_mask)
        total_detections += len(objects)  # Akumulasi jumlah deteksi
        
        # Hitung persentase motion di frame (untuk statistik)
        motion_pixels = np.sum(clean_mask > 0)  # Jumlah pixel foreground
        total_pixels = clean_mask.shape[0] * clean_mask.shape[1]  # Total pixel
        motion_percentage = (motion_pixels / total_pixels) * 100
        # Simpan ke deque (circular buffer, max 100 entry)
        motion_history.append(motion_percentage)
        
        # Draw
        vis_frame = draw_detections(frame, objects, clean_mask)
        
        # Add info
        cv2.putText(vis_frame, f"Method: {current_method}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(vis_frame, f"Objects: {len(objects)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(vis_frame, f"Motion: {motion_percentage:.1f}%", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Create mask visualization
        mask_vis = cv2.cvtColor(clean_mask, cv2.COLOR_GRAY2BGR)
        cv2.putText(mask_vis, "Foreground Mask", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Combine
        combined = np.hstack([vis_frame, mask_vis])
        
        # Write
        out.write(combined)
        
        # Display
        cv2.imshow("Motion Detection", combined)
        
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"03_motion_{frame_count}.png"), combined)
            print(f"Saved frame {frame_count}")
        elif key == ord('1'):
            current_method = 'MOG2'
            bg_subtractor = create_background_subtractor('MOG2')
            print("Switched to MOG2")
        elif key == ord('2'):
            current_method = 'KNN'
            bg_subtractor = create_background_subtractor('KNN')
            print("Switched to KNN")
        elif key == ord('3'):
            current_method = 'DIFF'
            prev_gray = None
            print("Switched to Frame Differencing")
        
        frame_count += 1

        if AUTO_CLOSE_SECONDS > 0 and not using_webcam:
            if (time.time() - start_time) >= AUTO_CLOSE_SECONDS:
                print("Auto-close: waktu uji selesai.")
                break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Print statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(f"Total frames processed: {frame_count}")
    print(f"Total detections: {total_detections}")
    print(f"Average detections per frame: {total_detections/max(1,frame_count):.2f}")
    print(f"Average motion percentage: {np.mean(motion_history):.2f}%")
    print(f"Max motion percentage: {np.max(motion_history):.2f}%")

if __name__ == "__main__":
    main()
