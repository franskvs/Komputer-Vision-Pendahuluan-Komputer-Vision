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
        return cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )
    elif method == 'KNN':
        return cv2.createBackgroundSubtractorKNN(
            history=500,
            dist2Threshold=400.0,
            detectShadows=True
        )
    else:  # DIFF - akan ditangani secara manual
        return None

def apply_morphology(mask):
    """
    Aplikasikan operasi morphological untuk membersihkan mask.
    
    Parameters:
        mask: Binary mask
    
    Returns:
        cleaned: Cleaned mask
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KERNEL_SIZE, KERNEL_SIZE))
    
    # Opening untuk menghilangkan noise kecil
    cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Closing untuk mengisi lubang
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    
    # Dilate sedikit untuk memperbesar region
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
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= MIN_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            objects.append((x, y, w, h, area))
    
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
    output = frame.copy()
    
    # Draw bounding boxes
    for (x, y, w, h, area) in objects:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(output, f"Area: {area}", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Create colored mask overlay
    mask_colored = np.zeros_like(frame)
    mask_colored[:, :, 1] = mask  # Green channel
    
    # Blend with original
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
    diff = cv2.absdiff(prev_frame, curr_frame)
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
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply background subtraction
        if current_method == 'DIFF':
            if prev_gray is not None:
                fg_mask = frame_differencing(prev_gray, gray)
            else:
                fg_mask = np.zeros_like(gray)
            prev_gray = gray.copy()
        else:
            fg_mask = bg_subtractor.apply(frame, learningRate=LEARNING_RATE)
            
            # Remove shadow pixels (127 in MOG2/KNN)
            fg_mask[fg_mask == 127] = 0
        
        # Clean mask
        clean_mask = apply_morphology(fg_mask)
        
        # Find objects
        objects = find_moving_objects(clean_mask)
        total_detections += len(objects)
        
        # Calculate motion percentage
        motion_pixels = np.sum(clean_mask > 0)
        total_pixels = clean_mask.shape[0] * clean_mask.shape[1]
        motion_percentage = (motion_pixels / total_pixels) * 100
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
