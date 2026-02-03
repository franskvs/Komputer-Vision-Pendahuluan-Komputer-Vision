# ============================================================
# PROGRAM: 08_optical_flow.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk Optical Flow (Lucas-Kanade dan Farneback)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep optical flow
#   2. Perbandingan sparse vs dense optical flow
#   3. Aplikasi motion detection dan tracking
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. Sumber video
# Opsi: 0 (webcam), 'video.mp4' (file), 'synthetic' (synthetic motion)
VIDEO_SOURCE = 'synthetic'

# 2. Jenis Optical Flow
# Opsi: 'sparse' (Lucas-Kanade), 'dense' (Farneback), 'both'
FLOW_TYPE = 'both'

# 3. Parameter Shi-Tomasi corner detection (untuk sparse)
MAX_CORNERS = 100
QUALITY_LEVEL = 0.3
MIN_DISTANCE = 7
BLOCK_SIZE = 7

# 4. Parameter Lucas-Kanade (sparse flow)
LK_WIN_SIZE = (15, 15)
LK_MAX_LEVEL = 2
LK_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

# 5. Parameter Farneback (dense flow)
FB_PYR_SCALE = 0.5
FB_LEVELS = 3
FB_WIN_SIZE = 15
FB_ITERATIONS = 3
FB_POLY_N = 5
FB_POLY_SIGMA = 1.2

# 6. Visualisasi
TRACK_LENGTH = 10          # Panjang track history
FLOW_SCALE = 5             # Scale untuk visualisasi dense flow
MIN_FLOW_MAGNITUDE = 1.0   # Minimum magnitude untuk display

# ============================================================
# FUNGSI HELPER
# ============================================================

def create_synthetic_video():
    """
    Membuat synthetic video dengan objek bergerak
    
    Return:
    - frames: list of frames
    """
    frames = []
    h, w = 400, 600
    
    for t in range(60):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        frame[:, :] = [30, 30, 30]
        
        # Moving circle
        x1 = int(100 + t * 3)
        y1 = int(100 + np.sin(t * 0.1) * 50)
        cv2.circle(frame, (x1, y1), 30, (0, 0, 255), -1)
        
        # Moving rectangle
        x2 = int(500 - t * 2)
        y2 = int(200 + np.cos(t * 0.15) * 30)
        cv2.rectangle(frame, (x2-30, y2-30), (x2+30, y2+30), (0, 255, 0), -1)
        
        # Rotating line
        cx, cy = 300, 300
        angle = t * 0.1
        x3 = int(cx + 80 * np.cos(angle))
        y3 = int(cy + 80 * np.sin(angle))
        cv2.line(frame, (cx, cy), (x3, y3), (255, 255, 0), 3)
        
        # Text
        cv2.putText(frame, f"Frame {t}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        frames.append(frame)
    
    return frames


def draw_flow_vectors(img, flow, step=16, scale=1.0):
    """
    Draw optical flow vectors sebagai arrows
    
    Parameter:
    - img: input image
    - flow: dense flow field
    - step: sampling step
    - scale: scale for visualization
    """
    h, w = img.shape[:2]
    y, x = np.mgrid[step//2:h:step, step//2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    
    # Filter by magnitude
    mag = np.sqrt(fx**2 + fy**2)
    mask = mag > MIN_FLOW_MAGNITUDE
    
    output = img.copy()
    
    # Draw arrows
    for i in range(len(x)):
        if mask[i]:
            pt1 = (x[i], y[i])
            pt2 = (int(x[i] + fx[i] * scale), int(y[i] + fy[i] * scale))
            cv2.arrowedLine(output, pt1, pt2, (0, 255, 0), 1, tipLength=0.3)
    
    return output


def flow_to_hsv(flow):
    """
    Convert optical flow ke HSV visualization
    
    - Hue: direction of flow
    - Saturation: 255 (full)
    - Value: magnitude of flow
    """
    h, w = flow.shape[:2]
    hsv = np.zeros((h, w, 3), dtype=np.uint8)
    hsv[..., 1] = 255  # Saturation
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    hsv[..., 0] = ang * 180 / np.pi / 2  # Hue (0-180)
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)  # Value
    
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return rgb


# ============================================================
# FUNGSI OPTICAL FLOW
# ============================================================

def lucas_kanade_flow(prev_gray, curr_gray, prev_pts):
    """
    Sparse Optical Flow menggunakan Lucas-Kanade method
    
    Asumsi:
    1. Brightness Constancy: pixel intensity tidak berubah
    2. Small Motion: gerakan kecil antar frame
    3. Spatial Coherence: neighboring pixels move together
    
    Parameter:
    - prev_gray: previous frame (grayscale)
    - curr_gray: current frame (grayscale)
    - prev_pts: points to track
    
    Return:
    - next_pts: tracked points di frame baru
    - status: 1 jika tracking berhasil, 0 jika gagal
    - error: tracking error
    """
    if prev_pts is None or len(prev_pts) == 0:
        return None, None, None
    
    next_pts, status, error = cv2.calcOpticalFlowPyrLK(
        prev_gray, curr_gray, prev_pts, None,
        winSize=LK_WIN_SIZE,
        maxLevel=LK_MAX_LEVEL,
        criteria=LK_CRITERIA
    )
    
    return next_pts, status, error


def farneback_flow(prev_gray, curr_gray):
    """
    Dense Optical Flow menggunakan Farneback method
    
    Menghitung flow untuk setiap pixel dalam image.
    Lebih comprehensive tapi lebih lambat dari sparse.
    
    Parameter:
    - prev_gray: previous frame (grayscale)
    - curr_gray: current frame (grayscale)
    
    Return:
    - flow: dense flow field (h, w, 2) - dx, dy untuk setiap pixel
    """
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        pyr_scale=FB_PYR_SCALE,
        levels=FB_LEVELS,
        winsize=FB_WIN_SIZE,
        iterations=FB_ITERATIONS,
        poly_n=FB_POLY_N,
        poly_sigma=FB_POLY_SIGMA,
        flags=0
    )
    
    return flow


def detect_good_features(gray):
    """
    Detect good features to track (Shi-Tomasi corners)
    """
    pts = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=MAX_CORNERS,
        qualityLevel=QUALITY_LEVEL,
        minDistance=MIN_DISTANCE,
        blockSize=BLOCK_SIZE
    )
    
    return pts


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_sparse_flow():
    """Demonstrasi sparse optical flow (Lucas-Kanade)"""
    print("\n" + "=" * 60)
    print("SPARSE OPTICAL FLOW (LUCAS-KANADE)")
    print("=" * 60)
    
    print("""
LUCAS-KANADE METHOD:

Assumptions:
1. Brightness Constancy: I(x,y,t) = I(x+dx, y+dy, t+dt)
2. Small Motion: Taylor expansion valid
3. Spatial Coherence: neighboring pixels sama

Equation:
    Ix*Vx + Iy*Vy + It = 0

Dimana:
├── Ix, Iy: spatial gradients
├── It: temporal gradient
└── Vx, Vy: velocities to solve

Karena underdetermined (1 eq, 2 unknowns),
gunakan local window → least squares solution.
    """)
    
    # Create synthetic video
    frames = create_synthetic_video()
    
    # Initialize
    prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    pts = detect_good_features(prev_gray)
    
    # Tracking history
    tracks = []
    
    # Colors for visualization
    colors = np.random.randint(0, 255, (MAX_CORNERS, 3))
    
    # Create mask for drawing
    mask = np.zeros_like(frames[0])
    
    # Process frames
    results = []
    
    for i, frame in enumerate(frames[1:30]):
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if pts is not None and len(pts) > 0:
            next_pts, status, error = lucas_kanade_flow(prev_gray, curr_gray, pts)
            
            if next_pts is not None:
                # Select good points
                good_new = next_pts[status == 1]
                good_old = pts[status == 1]
                
                # Draw tracks
                output = frame.copy()
                for j, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel().astype(int)
                    c, d = old.ravel().astype(int)
                    mask = cv2.line(mask, (a, b), (c, d), colors[j].tolist(), 2)
                    output = cv2.circle(output, (a, b), 5, colors[j].tolist(), -1)
                
                output = cv2.add(output, mask)
                results.append(output)
                
                # Update
                pts = good_new.reshape(-1, 1, 2)
        
        prev_gray = curr_gray.copy()
        
        # Re-detect if too few points
        if pts is None or len(pts) < 10:
            pts = detect_good_features(curr_gray)
            mask = np.zeros_like(frame)
    
    # Show some results
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    indices = [0, 5, 10, 15, 20, 25]
    for i, idx in enumerate(indices):
        if idx < len(results):
            axes[i].imshow(cv2.cvtColor(results[idx], cv2.COLOR_BGR2RGB))
            axes[i].set_title(f"Frame {idx + 1}")
            axes[i].axis('off')
    
    plt.suptitle("Sparse Optical Flow (Lucas-Kanade)", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_dense_flow():
    """Demonstrasi dense optical flow (Farneback)"""
    print("\n" + "=" * 60)
    print("DENSE OPTICAL FLOW (FARNEBACK)")
    print("=" * 60)
    
    print("""
FARNEBACK METHOD:

Menghitung flow untuk SETIAP pixel.
Menggunakan polynomial expansion untuk approximate
neighborhood of each pixel.

Keuntungan:
├── Complete motion field
├── Good for understanding overall motion
└── Can detect moving regions

Kekurangan:
├── Computationally expensive
└── May not be accurate at object boundaries

Visualisasi:
├── HSV: Hue = direction, Value = magnitude
└── Arrows: sampled flow vectors
    """)
    
    # Create synthetic video
    frames = create_synthetic_video()
    
    prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    
    results_hsv = []
    results_arrow = []
    
    for i, frame in enumerate(frames[1:30]):
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate dense flow
        flow = farneback_flow(prev_gray, curr_gray)
        
        # HSV visualization
        hsv_vis = flow_to_hsv(flow)
        results_hsv.append(hsv_vis)
        
        # Arrow visualization
        arrow_vis = draw_flow_vectors(frame, flow, step=20, scale=FLOW_SCALE)
        results_arrow.append(arrow_vis)
        
        prev_gray = curr_gray.copy()
    
    # Show results
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    indices = [0, 10, 20, 28]
    
    for i, idx in enumerate(indices):
        if idx < len(frames) - 1:
            axes[0, i].imshow(cv2.cvtColor(frames[idx], cv2.COLOR_BGR2RGB))
            axes[0, i].set_title(f"Frame {idx}")
            axes[0, i].axis('off')
            
            if idx < len(results_hsv):
                axes[1, i].imshow(cv2.cvtColor(results_hsv[idx], cv2.COLOR_BGR2RGB))
                axes[1, i].set_title(f"HSV Flow")
                axes[1, i].axis('off')
                
                axes[2, i].imshow(cv2.cvtColor(results_arrow[idx], cv2.COLOR_BGR2RGB))
                axes[2, i].set_title(f"Arrow Flow")
                axes[2, i].axis('off')
    
    axes[0, 0].set_ylabel("Original", fontsize=12)
    axes[1, 0].set_ylabel("HSV Vis", fontsize=12)
    axes[2, 0].set_ylabel("Arrow Vis", fontsize=12)
    
    plt.suptitle("Dense Optical Flow (Farneback)", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_comparison():
    """Perbandingan sparse vs dense optical flow"""
    print("\n" + "=" * 60)
    print("COMPARISON: SPARSE vs DENSE")
    print("=" * 60)
    
    print("""
COMPARISON:

| Aspect        | Sparse (LK)     | Dense (Farneback) |
|---------------|-----------------|-------------------|
| Coverage      | Selected points | All pixels        |
| Speed         | Fast            | Slow              |
| Memory        | Low             | High              |
| Accuracy      | High at points  | Good overall      |
| Use Case      | Object tracking | Motion analysis   |

WHEN TO USE:

Sparse (Lucas-Kanade):
├── Object tracking
├── Feature tracking
├── Real-time applications
└── When you know what to track

Dense (Farneback):
├── Motion segmentation
├── Action recognition
├── Video compression
└── Complete motion analysis
    """)
    
    # Create synthetic video
    frames = create_synthetic_video()
    
    # Select a pair of frames
    frame1 = frames[10]
    frame2 = frames[15]
    
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Sparse flow
    start = time.time()
    pts = detect_good_features(gray1)
    next_pts, status, _ = lucas_kanade_flow(gray1, gray2, pts)
    sparse_time = (time.time() - start) * 1000
    
    sparse_vis = frame1.copy()
    if next_pts is not None and status is not None:
        for i, (new, old) in enumerate(zip(next_pts[status == 1], pts[status == 1])):
            a, b = new.ravel().astype(int)
            c, d = old.ravel().astype(int)
            sparse_vis = cv2.line(sparse_vis, (a, b), (c, d), (0, 255, 0), 2)
            sparse_vis = cv2.circle(sparse_vis, (a, b), 5, (0, 0, 255), -1)
    
    # Dense flow
    start = time.time()
    dense_flow = farneback_flow(gray1, gray2)
    dense_time = (time.time() - start) * 1000
    
    dense_hsv = flow_to_hsv(dense_flow)
    dense_arrow = draw_flow_vectors(frame1, dense_flow, step=20, scale=FLOW_SCALE)
    
    print(f"\nTiming:")
    print(f"Sparse (LK):      {sparse_time:.2f} ms")
    print(f"Dense (Farneback): {dense_time:.2f} ms")
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Frame 1")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Frame 2")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(sparse_vis, cv2.COLOR_BGR2RGB))
    n_tracked = np.sum(status == 1) if status is not None else 0
    axes[0, 2].set_title(f"Sparse Flow\n{n_tracked} points, {sparse_time:.1f}ms")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(dense_hsv, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"Dense Flow (HSV)\n{dense_time:.1f}ms")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(dense_arrow, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title("Dense Flow (Arrows)")
    axes[1, 1].axis('off')
    
    # Flow magnitude histogram
    mag, _ = cv2.cartToPolar(dense_flow[..., 0], dense_flow[..., 1])
    axes[1, 2].hist(mag.flatten(), bins=50, color='blue', alpha=0.7)
    axes[1, 2].set_xlabel("Flow Magnitude")
    axes[1, 2].set_ylabel("Pixel Count")
    axes[1, 2].set_title("Flow Magnitude Distribution")
    
    plt.suptitle("Sparse vs Dense Optical Flow Comparison", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: OPTICAL FLOW")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
OPTICAL FLOW adalah pattern of apparent motion dari objects,
surfaces, atau edges dalam visual scene yang disebabkan oleh
relative motion antara observer dan scene.

OPTICAL FLOW EQUATION:

    Ix*Vx + Iy*Vy + It = 0

Dimana:
├── Ix = ∂I/∂x (spatial gradient x)
├── Iy = ∂I/∂y (spatial gradient y)
├── It = ∂I/∂t (temporal gradient)
├── Vx = dx/dt (velocity x)
└── Vy = dy/dt (velocity y)

ASSUMPTIONS:
1. Brightness Constancy
2. Small Motion (untuk Taylor expansion)
3. Spatial Coherence

DUA PENDEKATAN:

1. SPARSE FLOW (Lucas-Kanade):
   ├── Hitung flow hanya di selected points
   ├── Fast dan efficient
   └── Good untuk tracking

2. DENSE FLOW (Farneback, FlowNet, etc.):
   ├── Hitung flow untuk semua pixels
   ├── Complete motion field
   └── Good untuk motion segmentation

APLIKASI:
├── Object tracking
├── Motion detection
├── Video stabilization
├── Action recognition
├── Autonomous driving
└── Video compression
    """)
    
    print(f"[INFO] Video Source: {VIDEO_SOURCE}")
    print(f"[INFO] Flow Type: {FLOW_TYPE}")
    
    # Demo sparse flow
    if FLOW_TYPE in ['sparse', 'both']:
        demo_sparse_flow()
    
    # Demo dense flow
    if FLOW_TYPE in ['dense', 'both']:
        demo_dense_flow()
    
    # Comparison
    demo_comparison()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN OPTICAL FLOW")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Detect good features to track
pts = cv2.goodFeaturesToTrack(gray, maxCorners=100,
    qualityLevel=0.3, minDistance=7)

# Sparse Flow (Lucas-Kanade)
next_pts, status, error = cv2.calcOpticalFlowPyrLK(
    prev_gray, curr_gray, prev_pts, None,
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# Dense Flow (Farneback)
flow = cv2.calcOpticalFlowFarneback(
    prev_gray, curr_gray, None,
    pyr_scale=0.5,
    levels=3,
    winsize=15,
    iterations=3,
    poly_n=5,
    poly_sigma=1.2,
    flags=0
)

# Convert flow to HSV visualization
mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
hsv[..., 0] = ang * 180 / np.pi / 2
hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

TIPS:
1. Gunakan pyramid untuk handle large motion
2. Re-detect features jika tracking point hilang
3. Dense flow untuk motion segmentation
4. Sparse flow untuk real-time tracking
5. Combine dengan Kalman filter untuk smoother tracking

MODERN ALTERNATIVES:
├── DeepFlow: CNN-based dense flow
├── FlowNet: End-to-end learned flow
├── RAFT: State-of-the-art accuracy
└── PWC-Net: Good speed-accuracy tradeoff
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
