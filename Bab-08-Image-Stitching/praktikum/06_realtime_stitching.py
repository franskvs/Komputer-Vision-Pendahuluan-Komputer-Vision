"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 6: Real-time Stitching (Capture dan Stitch)

Deskripsi:
    Program ini mendemonstrasikan pembuatan panorama secara interaktif.
    User dapat mengambil beberapa foto dari webcam atau file, kemudian
    melihat hasil stitching secara real-time.

Mode Operasi:
    1. Capture Mode: Ambil foto dari webcam
    2. Load Mode: Load foto dari folder

Instruksi:
    - Tekan 'c' untuk capture frame (mode webcam)
    - Tekan 's' untuk stitch gambar yang sudah di-capture
    - Tekan 'r' untuk reset (hapus semua capture)
    - Tekan 'q' untuk quit

Parameter yang dapat dimodifikasi:
    - MODE: 'webcam' atau 'folder'
    - MIN_CAPTURES: Minimum jumlah capture sebelum bisa stitch
    - MAX_CAPTURES: Maximum jumlah capture

Output:
    - Live preview dari webcam
    - Hasil stitching

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import glob
import time

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Mode operasi: 'webcam' atau 'folder'
MODE = 'folder'  # Gunakan folder karena tidak semua komputer punya webcam

# Minimum capture sebelum bisa stitch
MIN_CAPTURES = 2

# Maximum captures
MAX_CAPTURES = 10

# Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_sample_images():
    """
    Load sample images untuk mode folder.
    """
    images = []
    names = []
    
    # Coba panorama_set dulu
    pano_folder = os.path.join(DATA_DIR, "panorama_set")
    if os.path.exists(pano_folder):
        files = sorted(glob.glob(os.path.join(pano_folder, "*.[jp][pn][g]*")))
        if len(files) >= 2:
            for f in files[:MAX_CAPTURES]:
                img = cv2.imread(f)
                if img is not None:
                    images.append(img)
                    names.append(os.path.basename(f))
            return images, names
    
    # Fallback ke gambar default
    default_files = ["left01.jpg", "right01.jpg", "graf1.png", "graf3.png"]
    for f in default_files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path) and len(images) < MAX_CAPTURES:
            img = cv2.imread(path)
            if img is not None:
                images.append(img)
                names.append(f)
    
    return images, names

def stitch_images(images):
    """
    Stitch gambar menggunakan OpenCV Stitcher.
    """
    if len(images) < 2:
        return None, "Butuh minimal 2 gambar"
    
    # Resize untuk kecepatan
    resized = []
    for img in images:
        h, w = img.shape[:2]
        if max(h, w) > 600:
            scale = 600 / max(h, w)
            img = cv2.resize(img, None, fx=scale, fy=scale)
        resized.append(img)
    
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    status, result = stitcher.stitch(resized)
    
    status_msg = {
        cv2.Stitcher_OK: "Success",
        cv2.Stitcher_ERR_NEED_MORE_IMGS: "Butuh lebih banyak gambar dengan overlap",
        cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Estimasi homography gagal - overlap kurang?",
        cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Penyesuaian kamera gagal"
    }
    
    if status == cv2.Stitcher_OK:
        return result, status_msg[status]
    else:
        return None, status_msg.get(status, f"Error: {status}")

def create_thumbnail_grid(images, max_cols=5, thumb_size=120):
    """
    Buat grid thumbnail dari list gambar.
    """
    if not images:
        return np.zeros((thumb_size, thumb_size * 2, 3), dtype=np.uint8)
    
    n = len(images)
    cols = min(n, max_cols)
    rows = (n + cols - 1) // cols
    
    grid = np.zeros((rows * thumb_size, cols * thumb_size, 3), dtype=np.uint8)
    
    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        
        # Resize ke thumbnail
        h, w = img.shape[:2]
        scale = min(thumb_size / h, thumb_size / w)
        new_h, new_w = int(h * scale), int(w * scale)
        thumb = cv2.resize(img, (new_w, new_h))
        
        # Center dalam cell
        y_offset = (thumb_size - new_h) // 2
        x_offset = (thumb_size - new_w) // 2
        
        y_start = row * thumb_size + y_offset
        x_start = col * thumb_size + x_offset
        
        grid[y_start:y_start + new_h, x_start:x_start + new_w] = thumb
        
        # Tambah nomor
        cv2.putText(grid, str(i + 1), 
                   (col * thumb_size + 5, row * thumb_size + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return grid

def run_webcam_mode():
    """
    Mode webcam - capture dari kamera.
    """
    print("=" * 60)
    print("WEBCAM MODE")
    print("=" * 60)
    print("Instruksi:")
    print("  'c' - Capture frame")
    print("  's' - Stitch captured images")
    print("  'r' - Reset captures")
    print("  'q' - Quit")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Tidak dapat membuka webcam!")
        print("Menggunakan mode folder sebagai gantinya...")
        return run_folder_mode()
    
    captured_images = []
    panorama = None
    message = ""
    message_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Tampilkan info
        display = frame.copy()
        cv2.putText(display, f"Captures: {len(captured_images)}/{MAX_CAPTURES}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, "c:capture s:stitch r:reset q:quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Tampilkan message sementara
        if time.time() - message_time < 2:
            cv2.putText(display, message, (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("Webcam", display)
        
        # Tampilkan thumbnails
        if captured_images:
            thumb_grid = create_thumbnail_grid(captured_images)
            cv2.imshow("Captured Images", thumb_grid)
        
        # Tampilkan panorama jika ada
        if panorama is not None:
            h, w = panorama.shape[:2]
            if max(h, w) > 800:
                scale = 800 / max(h, w)
                display_pano = cv2.resize(panorama, None, fx=scale, fy=scale)
            else:
                display_pano = panorama
            cv2.imshow("Panorama", display_pano)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c') and len(captured_images) < MAX_CAPTURES:
            captured_images.append(frame.copy())
            message = f"Captured! ({len(captured_images)} total)"
            message_time = time.time()
            print(f"Captured image {len(captured_images)}")
        
        elif key == ord('s'):
            if len(captured_images) >= MIN_CAPTURES:
                print("Stitching...")
                panorama, msg = stitch_images(captured_images)
                message = msg
                message_time = time.time()
                
                if panorama is not None:
                    # Simpan
                    output_path = os.path.join(OUTPUT_DIR, "06_realtime_panorama.jpg")
                    cv2.imwrite(output_path, panorama)
                    print(f"Panorama disimpan: {output_path}")
            else:
                message = f"Butuh minimal {MIN_CAPTURES} captures"
                message_time = time.time()
        
        elif key == ord('r'):
            captured_images = []
            panorama = None
            message = "Reset!"
            message_time = time.time()
            cv2.destroyWindow("Captured Images")
            cv2.destroyWindow("Panorama")
        
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def run_folder_mode():
    """
    Mode folder - load gambar dari folder dan stitch.
    """
    print("=" * 60)
    print("FOLDER MODE")
    print("=" * 60)
    
    # Load gambar
    images, names = load_sample_images()
    
    if len(images) < 2:
        print("ERROR: Tidak cukup gambar!")
        print("Letakkan gambar di folder data/images/panorama_set/")
        return
    
    print(f"\nDitemukan {len(images)} gambar:")
    for i, name in enumerate(names):
        print(f"  {i + 1}. {name}")
    
    # Tampilkan gambar
    print("\nMenampilkan gambar...")
    print("Instruksi:")
    print("  's' - Stitch semua gambar")
    print("  '1-9' - Toggle gambar on/off")
    print("  'q' - Quit")
    
    selected = [True] * len(images)
    panorama = None
    
    while True:
        # Buat display
        display_images = [img for img, sel in zip(images, selected) if sel]
        thumb_grid = create_thumbnail_grid(display_images)
        
        # Tambah info
        info_h = 60
        info_panel = np.zeros((info_h, thumb_grid.shape[1], 3), dtype=np.uint8)
        cv2.putText(info_panel, f"Selected: {sum(selected)}/{len(images)}", 
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(info_panel, "s:stitch  1-9:toggle  q:quit", 
                   (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        display = np.vstack([info_panel, thumb_grid])
        cv2.imshow("Images", display)
        
        if panorama is not None:
            h, w = panorama.shape[:2]
            if max(h, w) > 800:
                scale = 800 / max(h, w)
                pano_display = cv2.resize(panorama, None, fx=scale, fy=scale)
            else:
                pano_display = panorama
            cv2.imshow("Panorama", pano_display)
        
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('s'):
            if sum(selected) >= MIN_CAPTURES:
                print("\nStitching...")
                selected_images = [img for img, sel in zip(images, selected) if sel]
                panorama, msg = stitch_images(selected_images)
                print(f"Status: {msg}")
                
                if panorama is not None:
                    output_path = os.path.join(OUTPUT_DIR, "06_realtime_panorama.jpg")
                    cv2.imwrite(output_path, panorama)
                    print(f"Panorama disimpan: {output_path}")
            else:
                print(f"Butuh minimal {MIN_CAPTURES} gambar!")
        
        elif ord('1') <= key <= ord('9'):
            idx = key - ord('1')
            if idx < len(selected):
                selected[idx] = not selected[idx]
                print(f"Image {idx + 1}: {'selected' if selected[idx] else 'deselected'}")
        
        elif key == ord('q'):
            break
    
    cv2.destroyAllWindows()

def main():
    """
    Fungsi utama.
    """
    print("=" * 60)
    print("REAL-TIME / INTERACTIVE STITCHING")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if MODE == 'webcam':
        run_webcam_mode()
    else:
        run_folder_mode()
    
    print("\nSelesai!")

if __name__ == "__main__":
    main()
