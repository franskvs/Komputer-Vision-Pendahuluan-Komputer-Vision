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
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


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

# Auto close window (detik) untuk testing cepat
AUTO_CLOSE_SECONDS = 2.0

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
    # cv2.goodFeaturesToTrack: Deteksi corner menggunakan Shi-Tomasi
    # Parameter: gray = input grayscale, maxCorners = jumlah max corner,
    # qualityLevel = kualitas min (0-1), minDistance = jarak min antar corner (pixel),
    # blockSize = ukuran neighborhood untuk perhitungan derivative
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
    # Siapkan parameter untuk Lucas-Kanade optical flow
    # winSize: ukuran window pencarian (lebar, tinggi)
    # maxLevel: jumlah level pyramid (0=tidak pakai pyramid, >0=multi-scale)
    # criteria: kriteria terminasi iterasi (EPS=epsilon, COUNT=max iterasi)
    lk_params = dict(
        winSize=WIN_SIZE,
        maxLevel=MAX_LEVEL,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )
    
    # cv2.calcOpticalFlowPyrLK: Hitung optical flow dengan Lucas-Kanade pyramidal
    # Parameter: prev_gray=frame sebelumnya, curr_gray=frame sekarang,
    # prev_pts=titik yang akan di-track, None=output akan dibuat otomatis
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
    # Buat mask kosong dengan ukuran sama seperti frame untuk menggambar trails
    mask = np.zeros_like(frame)
    
    # Loop setiap track yang tersimpan dalam history
    for i, track in enumerate(tracks):
        if len(track) > 1:  # Hanya gambar jika ada minimal 2 titik
            # Ambil warna untuk track ini (modulo untuk cycling colors)
            color = colors[i % len(colors)].tolist()
            
            # Gambar garis untuk menghubungkan titik-titik dalam track history
            for j in range(1, len(track)):
                # Konversi koordinat float ke integer untuk cv2.line
                pt1 = tuple(map(int, track[j-1]))  # Titik sebelumnya
                pt2 = tuple(map(int, track[j]))    # Titik sekarang
                # cv2.line: Gambar garis dari pt1 ke pt2 dengan ketebalan 2
                cv2.line(mask, pt1, pt2, color, 2)
            
            # cv2.circle: Gambar lingkaran pada posisi terakhir (current position)
            # Parameter: frame, center, radius, color, thickness (-1=filled)
            cv2.circle(frame, tuple(map(int, track[-1])), 5, color, -1)
    
    # cv2.add: Gabungkan frame asli dengan mask trails
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
    # Validasi: pastikan ada points untuk digambar
    if prev_pts is None or next_pts is None:
        return frame
    
    # Loop setiap pasang titik (prev, next) dan status tracking-nya
    for i, (prev, next_, st) in enumerate(zip(prev_pts, next_pts, status)):
        if st[0] == 1:  # Hanya gambar jika tracking berhasil (status=1)
            # Konversi koordinat dari array ke integer
            x1, y1 = map(int, prev.ravel())  # Posisi sebelumnya
            x2, y2 = map(int, next_.ravel()) # Posisi sekarang
            
            # cv2.arrowedLine: Gambar panah dari posisi lama ke baru
            # Parameter: frame, start_point, end_point, color (BGR), thickness
            cv2.arrowedLine(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.circle: Gambar titik merah di posisi awal untuk referensi
            cv2.circle(frame, (x1, y1), 3, (0, 0, 255), -1)
    
    return frame

def main():
    """
    Fungsi utama untuk Lucas-Kanade optical flow demo.
    """
    # Tampilkan header program
    print("=" * 60)
    print("LUCAS-KANADE OPTICAL FLOW")
    print("=" * 60)
    
    # os.makedirs: Buat direktori output jika belum ada (exist_ok=True agar tidak error jika sudah ada)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Cari file video di direktori data
    video_path = os.path.join(DATA_DIR, "moving_object.avi")
    
    # Cek apakah file video ada
    if not os.path.exists(video_path):
        # Jika tidak ada, gunakan webcam sebagai alternatif
        print("Video tidak ditemukan, menggunakan webcam...")
        cap = cv2.VideoCapture(0)  # 0 = webcam default
        using_webcam = True
    else:
        # Buka file video
        cap = cv2.VideoCapture(video_path)
        using_webcam = False
        print(f"Menggunakan video: {video_path}")
    
    if not cap.isOpened():
        print("ERROR: Tidak dapat membuka video/webcam!")
        return
    
    # Ambil properti video dari capture object
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # FPS, default 30 jika tidak terdeteksi
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Lebar frame dalam pixel
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Tinggi frame dalam pixel
    
    print(f"Video properties: {width}x{height} @ {fps} FPS")
    
    # Setup video writer untuk menyimpan output
    # cv2.VideoWriter_fourcc: Buat fourcc code untuk codec XVID (kompatibel)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # cv2.VideoWriter: Buat object writer untuk menyimpan video
    # Parameter: output_path, codec, fps, frame_size (width, height)
    out = cv2.VideoWriter(
        os.path.join(OUTPUT_DIR, "01_lucas_kanade_output.avi"),
        fourcc, fps, (width, height)
    )
    
    # Baca frame pertama untuk inisialisasi
    ret, frame = cap.read()  # ret=True jika berhasil, frame=data gambar
    if not ret:
        print("Tidak dapat membaca frame!")
        return
    
    # cv2.cvtColor: Konversi frame BGR ke grayscale (optical flow butuh grayscale)
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Deteksi features awal pada frame pertama
    prev_pts = detect_features(prev_gray)
    
    # Generate warna random untuk setiap track (RGB 0-255)
    # np.random.randint: Buat array random integer shape (MAX_CORNERS, 3)
    colors = np.random.randint(0, 255, (MAX_CORNERS, 3))
    
    # Buat list kosong untuk menyimpan history tracking setiap feature
    tracks = [[] for _ in range(MAX_CORNERS)]
    
    # Inisialisasi track histories dengan posisi awal
    if prev_pts is not None:
        for i, pt in enumerate(prev_pts):
            # pt.ravel(): Ubah shape (1,2) menjadi (2,) untuk lebih mudah
            tracks[i].append(pt.ravel())
    
    frame_count = 0
    start_time = time.time()
    
    print("\nMulai tracking...")
    print("Tekan 'q' untuk keluar, 'r' untuk reset features")
    print("Tekan 's' untuk save screenshot")
    
    # Loop utama: proses setiap frame dalam video
    while True:
        # Baca frame berikutnya
        ret, frame = cap.read()
        if not ret:  # Jika gagal membaca (video habis)
            if not using_webcam:
                # Untuk file video: reset ke awal (loop terus)
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                # Untuk webcam: stop jika tidak ada frame
                break
        
        # Konversi frame saat ini ke grayscale untuk optical flow
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Proses hanya jika ada points untuk di-track
        if prev_pts is not None and len(prev_pts) > 0:
            # Hitung optical flow: cari posisi baru dari prev_pts di frame saat ini
            next_pts, status, error = calculate_optical_flow(
                prev_gray, curr_gray, prev_pts
            )
            
            # Filter hanya points yang berhasil di-track (status=1)
            if next_pts is not None:
                # status.flatten(): Ubah shape (N,1) jadi (N,) untuk indexing
                # good_new: posisi baru yang berhasil di-track
                good_new = next_pts[status.flatten() == 1]
                # good_old: posisi lama yang berhasil di-track
                good_old = prev_pts[status.flatten() == 1]
                
                # Update track histories: tambahkan posisi baru ke history
                track_idx = 0  # Index untuk good points
                for i, st in enumerate(status.flatten()):
                    if st == 1 and track_idx < len(good_new):  # Jika tracking berhasil
                        # Tambahkan posisi baru ke track history
                        tracks[i].append(good_new[track_idx].ravel())
                        # Batasi panjang track agar tidak terlalu panjang (hemat memori)
                        if len(tracks[i]) > TRACK_LENGTH:
                            # Ambil hanya TRACK_LENGTH terakhir
                            tracks[i] = tracks[i][-TRACK_LENGTH:]
                        track_idx += 1
                
                # Gambar visualisasi pada frame
                vis_frame = frame.copy()  # Copy frame agar aslinya tidak berubah
                # Gambar track trails (garis mengikuti gerakan)
                vis_frame = draw_tracks(vis_frame, tracks, colors)
                # Gambar flow vectors (panah dari posisi lama ke baru)
                # Reshape ke (N,1,2) karena fungsi draw butuh format tersebut
                vis_frame = draw_flow_vectors(vis_frame, good_old.reshape(-1, 1, 2), 
                                             good_new.reshape(-1, 1, 2), 
                                             status[status.flatten() == 1].reshape(-1, 1))
                
                # Update prev_pts dengan posisi baru untuk frame selanjutnya
                prev_pts = good_new.reshape(-1, 1, 2)
            else:
                # Jika optical flow gagal (next_pts=None), gunakan frame asli
                vis_frame = frame.copy()
        else:
            # Jika tidak ada points atau jumlah points habis, re-detect features
            vis_frame = frame.copy()
            # Deteksi ulang good features pada frame saat ini
            prev_pts = detect_features(curr_gray)
            # Reset track histories (mulai dari awal)
            tracks = [[] for _ in range(MAX_CORNERS)]
            # Inisialisasi tracks dengan posisi features baru
            if prev_pts is not None:
                for i, pt in enumerate(prev_pts):
                    if i < len(tracks):  # Pastikan tidak melebihi ukuran list
                        tracks[i].append(pt.ravel())
        
        # Tambahkan informasi teks pada frame visualisasi
        # cv2.putText(image, text, position, font, scale, color, thickness)
        # Parameter: vis_frame=canvas, f"Frame: {frame_count}"=teks, (10,30)=posisi (x,y),
        # cv2.FONT_HERSHEY_SIMPLEX=jenis font, 0.7=ukuran font, (0,255,0)=warna hijau BGR, 2=ketebalan
        cv2.putText(vis_frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # Tampilkan jumlah points yang sedang di-track
        cv2.putText(vis_frame, f"Points: {len(prev_pts) if prev_pts is not None else 0}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # Tampilkan instruksi keyboard
        cv2.putText(vis_frame, "q:quit r:reset s:save", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # cv2.VideoWriter.write: Simpan frame ke file video output
        out.write(vis_frame)
        
        # cv2.imshow: Tampilkan frame di window
        cv2.imshow("Lucas-Kanade Optical Flow", vis_frame)
        
        # cv2.waitKey: Tunggu keyboard input (1ms untuk webcam, 30ms untuk video file)
        # & 0xFF: Ambil 8 bit terakhir untuk kompatibilitas cross-platform
        key = cv2.waitKey(1 if using_webcam else 30) & 0xFF
        
        # Handle keyboard input
        # Handle keyboard input
        if key == ord('q'):  # Tekan 'q' untuk quit
            break
        elif key == ord('r'):  # Tekan 'r' untuk reset (deteksi ulang features)
            # Deteksi ulang features pada frame saat ini
            prev_pts = detect_features(curr_gray)
            # Reset semua track histories
            tracks = [[] for _ in range(MAX_CORNERS)]
            # Inisialisasi tracks dengan features baru
            if prev_pts is not None:
                for i, pt in enumerate(prev_pts):
                    if i < len(tracks):
                        tracks[i].append(pt.ravel())
            print(f"Reset: detected {len(prev_pts) if prev_pts is not None else 0} features")
        elif key == ord('s'):  # Tekan 's' untuk save screenshot
            # Buat nama file dengan nomor frame
            screenshot_path = os.path.join(OUTPUT_DIR, f"01_screenshot_{frame_count}.png")
            # cv2.imwrite: Simpan frame ke file image
            cv2.imwrite(screenshot_path, vis_frame)
            print(f"Saved: {screenshot_path}")
        
        # Update prev_gray untuk iterasi berikutnya
        # copy(): Buat salinan agar tidak terpengaruh modifikasi di iterasi berikutnya
        prev_gray = curr_gray.copy()
        frame_count += 1  # Increment counter frame

        # Auto-close untuk testing: keluar setelah waktu tertentu
        if AUTO_CLOSE_SECONDS > 0 and not using_webcam:
            # time.time(): Waktu saat ini dalam detik
            if (time.time() - start_time) >= AUTO_CLOSE_SECONDS:
                print("Auto-close: waktu uji selesai.")
                break
    
    # Cleanup: lepaskan resources
    cap.release()  # Tutup video capture
    out.release()  # Tutup video writer
    cv2.destroyAllWindows()  # Tutup semua window OpenCV
    
    print(f"\nSelesai! Total frames: {frame_count}")
    print(f"Output saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
