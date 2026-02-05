"""
Download Sample Data untuk Praktikum Bab 9: Motion Estimation
=============================================================

Script ini mendownload video-video sampel yang diperlukan untuk
praktikum motion estimation dan optical flow.

Penggunaan:
    python download_sample_data.py

Data yang didownload:
    - Video untuk optical flow demo
    - Video untuk tracking
    - Video untuk stabilization test
"""

import urllib.request
import os
import sys
import cv2
import numpy as np

def download_file(url, filepath):
    """
    Download file dari URL ke filepath yang ditentukan.
    """
    try:
        print(f"  Downloading {os.path.basename(filepath)}...", end=" ")
        urllib.request.urlretrieve(url, filepath)
        print("✓")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_synthetic_video(output_path, video_type="moving_object"):
    """
    Buat video sintetis untuk testing ketika video real tidak tersedia.
    
    Parameters:
        output_path: Path untuk menyimpan video
        video_type: Tipe video ('moving_object', 'shaky', 'multi_object')
    """
    print(f"  Creating synthetic {video_type} video...", end=" ")
    
    width, height = 640, 480
    fps = 30
    duration = 5  # seconds
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    num_frames = fps * duration
    
    for i in range(num_frames):
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add background gradient
        for y in range(height):
            frame[y, :, 0] = int(50 + 30 * np.sin(y/50 + i/30))  # Blue varying
            frame[y, :, 1] = int(50 + 20 * np.sin(y/40))  # Green
            frame[y, :, 2] = int(40)  # Red
        
        if video_type == "moving_object":
            # Single object moving across screen
            x = int(50 + (width - 100) * i / num_frames)
            y = int(height/2 + 50 * np.sin(i * 0.1))
            cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
            cv2.circle(frame, (x, y), 30, (255, 255, 255), 2)
            
        elif video_type == "shaky":
            # Simulated camera shake
            shake_x = int(10 * np.sin(i * 0.5))
            shake_y = int(8 * np.cos(i * 0.7))
            
            # Draw some fixed objects
            cv2.rectangle(frame, (100 + shake_x, 100 + shake_y), 
                         (200 + shake_x, 200 + shake_y), (255, 0, 0), -1)
            cv2.circle(frame, (400 + shake_x, 300 + shake_y), 40, (0, 0, 255), -1)
            
        elif video_type == "multi_object":
            # Multiple objects moving
            # Object 1 - horizontal
            x1 = int(50 + (width - 100) * i / num_frames)
            cv2.circle(frame, (x1, 150), 25, (255, 0, 0), -1)
            
            # Object 2 - vertical
            y2 = int(50 + (height - 100) * i / num_frames)
            cv2.circle(frame, (width - 100, y2), 25, (0, 255, 0), -1)
            
            # Object 3 - diagonal
            x3 = int(50 + (width - 100) * i / num_frames)
            y3 = int(50 + (height - 100) * i / num_frames)
            cv2.rectangle(frame, (x3 - 20, y3 - 20), (x3 + 20, y3 + 20), (0, 0, 255), -1)
            
            # Object 4 - circular path
            angle = i * 0.1
            x4 = int(width/2 + 100 * np.cos(angle))
            y4 = int(height/2 + 100 * np.sin(angle))
            cv2.circle(frame, (x4, y4), 20, (255, 255, 0), -1)
        
        # Add frame number
        cv2.putText(frame, f"Frame: {i}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print("✓")
    return True

def main():
    """
    Fungsi utama untuk mendownload/membuat semua data sampel.
    """
    print("=" * 60)
    print("DOWNLOAD SAMPLE DATA - BAB 9: MOTION ESTIMATION")
    print("=" * 60)
    
    # Setup directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data", "videos")
    output_dir = os.path.join(script_dir, "output")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nFolder video: {data_dir}")
    print(f"Folder output: {output_dir}\n")
    
    # URLs untuk video sample (dari OpenCV samples dan lainnya)
    # Note: OpenCV tidak menyediakan video sample langsung, jadi kita buat synthetic
    
    success_count = 0
    fail_count = 0
    
    # Create synthetic videos
    print("Membuat video sintetis untuk testing...\n")
    
    videos_to_create = [
        ("moving_object.avi", "moving_object"),
        ("shaky_video.avi", "shaky"),
        ("multi_object.avi", "multi_object"),
    ]
    
    for filename, video_type in videos_to_create:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"  {filename} sudah ada, skip.")
            success_count += 1
        else:
            if create_synthetic_video(filepath, video_type):
                success_count += 1
            else:
                fail_count += 1
    
    # Download gambar untuk optical flow juga
    print("\nDownload gambar tambahan...")
    
    image_urls = {
        "frame1.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/pic1.png",
        "frame2.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/pic2.png",
    }
    
    images_dir = os.path.join(script_dir, "data", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    for filename, url in image_urls.items():
        filepath = os.path.join(images_dir, filename)
        if os.path.exists(filepath):
            print(f"  {filename} sudah ada, skip.")
            success_count += 1
        else:
            if download_file(url, filepath):
                success_count += 1
            else:
                fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Berhasil: {success_count}")
    print(f"  Gagal: {fail_count}")
    
    if fail_count == 0:
        print("\n✅ Semua data berhasil disiapkan!")
    else:
        print("\n⚠️  Beberapa file gagal dibuat/didownload.")
    
    print("\n" + "=" * 60)
    print("INSTRUKSI")
    print("=" * 60)
    print("""
Untuk hasil lebih baik, gunakan video Anda sendiri:

1. Rekam video dengan smartphone
2. Simpan di folder: data/videos/
3. Format yang didukung: .mp4, .avi, .mov

Contoh video untuk praktikum:
- Video orang berjalan (untuk tracking)
- Video dengan gerakan kamera (untuk stabilization)
- Video objek bergerak (untuk optical flow)
""")
    
    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
