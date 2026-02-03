"""
PRAKTIKUM BAB 9: MOTION ESTIMATION
==================================
Program 6: Video Stabilization

Deskripsi:
    Program ini mendemonstrasikan video stabilization menggunakan
    optical flow untuk mengestimasi camera motion dan mengkompensasi
    gerakan yang tidak diinginkan.

Teori:
    Video stabilization terdiri dari:
    1. Motion Estimation: Estimasi gerakan kamera antar frame
    2. Motion Smoothing: Filter gerakan untuk menghilangkan shake
    3. Image Warping: Warp frame untuk mengkompensasi shake

    Metode yang digunakan:
    - Feature tracking dengan Lucas-Kanade
    - Affine/Homography transformation estimation
    - Moving average smoothing

Parameter yang dapat dimodifikasi:
    - SMOOTHING_RADIUS: Radius untuk moving average (frames)
    - MAX_FEATURES: Jumlah features untuk tracking
    - CROP_RATIO: Ratio crop untuk border artifacts

Output:
    - Side-by-side comparison original vs stabilized
    - Stabilized video file

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

# Radius untuk moving average smoothing (frames)
# Semakin besar = lebih smooth tapi lebih delay
SMOOTHING_RADIUS = 15

# Jumlah features untuk tracking
MAX_FEATURES = 200

# Quality level untuk feature detection
QUALITY_LEVEL = 0.01

# Minimum distance antar features
MIN_DISTANCE = 30

# Crop ratio untuk menghilangkan border artifacts (0.0 - 0.2)
CROP_RATIO = 0.1

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "videos")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def moving_average(curve, radius):
    """
    Apply moving average filter ke curve.
    
    Parameters:
        curve: Input curve (1D array)
        radius: Window radius
    
    Returns:
        smoothed: Smoothed curve
    """
    window_size = 2 * radius + 1
    kernel = np.ones(window_size) / window_size
    
    # Pad curve untuk edge handling
    curve_padded = np.pad(curve, (radius, radius), mode='edge')
    
    # Convolve
    smoothed = np.convolve(curve_padded, kernel, mode='same')
    
    # Remove padding
    smoothed = smoothed[radius:-radius]
    
    return smoothed

def estimate_motion(prev_gray, curr_gray, prev_pts):
    """
    Estimasi motion antar frame menggunakan optical flow.
    
    Parameters:
        prev_gray: Previous frame (grayscale)
        curr_gray: Current frame (grayscale)
        prev_pts: Points untuk tracking
    
    Returns:
        transform: Transformation matrix (2x3 affine)
    """
    # Lucas-Kanade parameters
    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )
    
    # Track features
    curr_pts, status, err = cv2.calcOpticalFlowPyrLK(
        prev_gray, curr_gray, prev_pts, None, **lk_params
    )
    
    # Filter valid points
    idx = np.where(status == 1)[0]
    prev_pts_good = prev_pts[idx]
    curr_pts_good = curr_pts[idx]
    
    # Estimate affine transformation
    if len(prev_pts_good) >= 3:
        transform, _ = cv2.estimateAffinePartial2D(
            prev_pts_good, curr_pts_good
        )
        if transform is None:
            transform = np.eye(2, 3, dtype=np.float32)
    else:
        transform = np.eye(2, 3, dtype=np.float32)
    
    return transform

def get_transform_params(transform):
    """
    Extract translation, rotation, scale dari affine matrix.
    
    Parameters:
        transform: 2x3 affine matrix
    
    Returns:
        dx, dy: Translation
        da: Rotation angle
        ds: Scale
    """
    dx = transform[0, 2]
    dy = transform[1, 2]
    da = np.arctan2(transform[1, 0], transform[0, 0])
    ds = np.sqrt(transform[0, 0]**2 + transform[1, 0]**2)
    
    return dx, dy, da, ds

def create_transform(dx, dy, da, ds):
    """
    Create affine matrix dari parameters.
    """
    transform = np.zeros((2, 3), dtype=np.float32)
    transform[0, 0] = ds * np.cos(da)
    transform[0, 1] = -ds * np.sin(da)
    transform[1, 0] = ds * np.sin(da)
    transform[1, 1] = ds * np.cos(da)
    transform[0, 2] = dx
    transform[1, 2] = dy
    
    return transform

def stabilize_video(input_path, output_path, show_progress=True):
    """
    Stabilize video.
    
    Parameters:
        input_path: Path to input video
        output_path: Path to output video
        show_progress: Show progress
    
    Returns:
        success: Boolean
    """
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("Error: Cannot open video!")
        return False
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video: {width}x{height} @ {fps} FPS, {n_frames} frames")
    
    # First pass: estimate all transforms
    print("\nPass 1: Estimating motion...")
    
    transforms = []
    
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    for i in range(n_frames - 1):
        # Detect features
        prev_pts = cv2.goodFeaturesToTrack(
            prev_gray,
            maxCorners=MAX_FEATURES,
            qualityLevel=QUALITY_LEVEL,
            minDistance=MIN_DISTANCE
        )
        
        ret, curr_frame = cap.read()
        if not ret:
            break
        
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Estimate transform
        if prev_pts is not None:
            transform = estimate_motion(prev_gray, curr_gray, prev_pts)
        else:
            transform = np.eye(2, 3, dtype=np.float32)
        
        transforms.append(transform)
        
        prev_gray = curr_gray.copy()
        
        if show_progress and (i + 1) % 30 == 0:
            print(f"  Frame {i + 1}/{n_frames}")
    
    transforms = np.array(transforms)
    
    # Extract parameters
    print("\nPass 2: Smoothing trajectory...")
    
    trajectory = np.zeros((len(transforms), 4))  # dx, dy, da, ds
    
    cumsum = np.array([0., 0., 0., 1.])  # cumulative sum (ds starts at 1)
    
    for i, transform in enumerate(transforms):
        dx, dy, da, ds = get_transform_params(transform)
        cumsum[0] += dx
        cumsum[1] += dy
        cumsum[2] += da
        cumsum[3] *= ds
        trajectory[i] = cumsum.copy()
    
    # Smooth trajectory
    smoothed_trajectory = np.copy(trajectory)
    for i in range(4):
        smoothed_trajectory[:, i] = moving_average(trajectory[:, i], SMOOTHING_RADIUS)
    
    # Calculate difference
    diff = smoothed_trajectory - trajectory
    
    # Apply correction to transforms
    corrected_transforms = []
    for i, transform in enumerate(transforms):
        dx, dy, da, ds = get_transform_params(transform)
        
        # Add smoothing difference
        dx += diff[i, 0]
        dy += diff[i, 1]
        da += diff[i, 2]
        # ds tidak diubah untuk menghindari zoom
        
        corrected_transforms.append(create_transform(dx, dy, da, ds))
    
    # Second pass: apply transforms
    print("\nPass 3: Applying stabilization...")
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # Calculate crop dimensions
    crop_x = int(width * CROP_RATIO)
    crop_y = int(height * CROP_RATIO)
    out_width = width - 2 * crop_x
    out_height = height - 2 * crop_y
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (out_width * 2, out_height))
    
    for i in range(n_frames - 1):
        ret, frame = cap.read()
        if not ret:
            break
        
        if i < len(corrected_transforms):
            # Apply transformation
            stabilized = cv2.warpAffine(
                frame, corrected_transforms[i], (width, height)
            )
        else:
            stabilized = frame.copy()
        
        # Crop
        original_crop = frame[crop_y:crop_y+out_height, crop_x:crop_x+out_width]
        stabilized_crop = stabilized[crop_y:crop_y+out_height, crop_x:crop_x+out_width]
        
        # Add labels
        cv2.putText(original_crop, "Original", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(stabilized_crop, "Stabilized", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Combine
        combined = np.hstack([original_crop, stabilized_crop])
        
        out.write(combined)
        
        # Display
        cv2.imshow("Video Stabilization", combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if show_progress and (i + 1) % 30 == 0:
            print(f"  Frame {i + 1}/{n_frames}")
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\nStabilized video saved to: {output_path}")
    return True

def main():
    """
    Fungsi utama untuk video stabilization demo.
    """
    print("=" * 60)
    print("VIDEO STABILIZATION")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Cari video shaky
    video_path = os.path.join(DATA_DIR, "shaky_video.avi")
    
    if not os.path.exists(video_path):
        print("Video shaky tidak ditemukan!")
        print("Menggunakan video moving_object sebagai demo...")
        video_path = os.path.join(DATA_DIR, "moving_object.avi")
    
    if not os.path.exists(video_path):
        print("ERROR: Tidak ada video yang tersedia!")
        print("Jalankan download_sample_data.py terlebih dahulu.")
        return
    
    print(f"\nInput: {video_path}")
    print(f"Smoothing radius: {SMOOTHING_RADIUS} frames")
    print(f"Crop ratio: {CROP_RATIO}")
    
    output_path = os.path.join(OUTPUT_DIR, "06_stabilized_output.avi")
    
    # Stabilize
    success = stabilize_video(video_path, output_path)
    
    if success:
        print("\n" + "=" * 60)
        print("STABILIZATION COMPLETE")
        print("=" * 60)
        print(f"Output: {output_path}")
        print("""
Tips untuk hasil lebih baik:
1. Gunakan SMOOTHING_RADIUS lebih besar untuk video yang sangat goyang
2. Kurangi CROP_RATIO jika terlalu banyak area terpotong
3. Untuk video real, gunakan video dari smartphone dengan shake alami
        """)

if __name__ == "__main__":
    main()
