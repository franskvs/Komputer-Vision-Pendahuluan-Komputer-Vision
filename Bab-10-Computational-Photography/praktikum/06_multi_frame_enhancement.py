"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 6: Multi-Frame Enhancement

Deskripsi:
    Program ini mendemonstrasikan enhancement dengan multiple frames:
    - Temporal averaging untuk noise reduction
    - Frame alignment (registration)
    - Best frame selection

Teori:
    Multi-frame processing memanfaatkan informasi temporal:
    
    1. Noise Reduction:
       - Noise bersifat random dan independent antar frames
       - Averaging N frames mengurangi noise by factor √N
       - SNR improvement: SNR_new = SNR_old × √N
    
    2. Alignment:
       - Handheld capture menghasilkan slight movement
       - Registration diperlukan sebelum averaging
       - ECC atau feature-based alignment
    
    3. Moving Object Handling:
       - Detect motion regions
       - Use single frame untuk regions dengan motion

Parameter yang dapat dimodifikasi:
    - NUM_FRAMES: Jumlah frames untuk averaging
    - ALIGNMENT_METHOD: 'ecc' atau 'feature'
    - MOTION_THRESHOLD: Threshold untuk motion detection

Output:
    - Multi-frame averaged result
    - SNR improvement metrics

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Number of frames to simulate/use
NUM_FRAMES = 8

# Alignment method: 'ecc' atau 'feature'
ALIGNMENT_METHOD = 'ecc'

# Motion detection threshold
MOTION_THRESHOLD = 30

# Simulated noise level
NOISE_SIGMA = 25

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output6")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def simulate_burst(image, num_frames=NUM_FRAMES, noise_sigma=NOISE_SIGMA, 
                   max_shift=3):
    """
    Simulasi burst capture dengan noise dan slight shifts.
    """
    frames = []
    shifts = []
    
    h, w = image.shape[:2]
    
    for i in range(num_frames):
        # Add random noise
        noisy = image.astype(np.float64)
        noise = np.random.normal(0, noise_sigma, image.shape)
        noisy = np.clip(noisy + noise, 0, 255).astype(np.uint8)
        
        # Add random shift (simulating camera shake)
        dx = np.random.randint(-max_shift, max_shift + 1)
        dy = np.random.randint(-max_shift, max_shift + 1)
        
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted = cv2.warpAffine(noisy, M, (w, h))
        
        frames.append(shifted)
        shifts.append((dx, dy))
        
    return frames, shifts

def align_ecc(reference, target, warp_mode=cv2.MOTION_TRANSLATION):
    """
    Align images using ECC (Enhanced Correlation Coefficient).
    """
    # Convert to grayscale
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    tgt_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    
    # Initialize warp matrix
    if warp_mode == cv2.MOTION_TRANSLATION:
        warp_matrix = np.eye(2, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    
    # Criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-7)
    
    try:
        _, warp_matrix = cv2.findTransformECC(
            ref_gray, tgt_gray, warp_matrix, warp_mode, criteria
        )
        
        # Apply warp
        h, w = target.shape[:2]
        if warp_mode == cv2.MOTION_TRANSLATION:
            aligned = cv2.warpAffine(target, warp_matrix, (w, h),
                                     flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        else:
            aligned = cv2.warpPerspective(target, warp_matrix, (w, h),
                                          flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        return aligned, warp_matrix
        
    except cv2.error:
        # If alignment fails, return original
        return target, np.eye(2, 3, dtype=np.float32)

def align_feature(reference, target):
    """
    Align images using feature matching.
    """
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    tgt_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    
    # Detect features
    orb = cv2.ORB_create(500)
    kp1, des1 = orb.detectAndCompute(ref_gray, None)
    kp2, des2 = orb.detectAndCompute(tgt_gray, None)
    
    if des1 is None or des2 is None:
        return target, None
    
    # Match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    if len(matches) < 4:
        return target, None
    
    # Extract matched points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Find homography
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)
    
    if H is None:
        return target, None
    
    # Warp
    h, w = target.shape[:2]
    aligned = cv2.warpPerspective(target, H, (w, h))
    
    return aligned, H

def multi_frame_average(frames, reference_idx=0, method=ALIGNMENT_METHOD):
    """
    Average multiple frames with alignment.
    """
    reference = frames[reference_idx]
    aligned_frames = [reference]
    
    print(f"    Aligning frames using {method} method...")
    
    for i, frame in enumerate(frames):
        if i == reference_idx:
            continue
        
        if method == 'ecc':
            aligned, _ = align_ecc(reference, frame)
        else:  # feature
            aligned, _ = align_feature(reference, frame)
        
        aligned_frames.append(aligned)
    
    # Average
    average = np.mean(aligned_frames, axis=0).astype(np.uint8)
    
    return average, aligned_frames

def calculate_snr(clean, noisy):
    """
    Calculate Signal-to-Noise Ratio.
    """
    signal_power = np.mean(clean.astype(np.float64) ** 2)
    noise = noisy.astype(np.float64) - clean.astype(np.float64)
    noise_power = np.mean(noise ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    return 10 * np.log10(signal_power / noise_power)

def detect_motion(frame1, frame2, threshold=MOTION_THRESHOLD):
    """
    Detect motion regions between frames.
    """
    diff = cv2.absdiff(frame1, frame2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, motion_mask = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel)
    
    return motion_mask

def main():
    """
    Fungsi utama untuk multi-frame enhancement demo.
    """
    print("=" * 60)
    print("MULTI-FRAME ENHANCEMENT")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load image
    image_path = os.path.join(DATA_DIR, "clean_image.jpg")
    
    if not os.path.exists(image_path):
        image_path = os.path.join(DATA_DIR, "lena.png")
    
    if not os.path.exists(image_path):
        print("Image tidak ditemukan! Jalankan download_sample_data.py")
        return
    
    print(f"\nLoading clean image: {image_path}")
    clean = cv2.imread(image_path)
    
    if clean is None:
        print("Failed to load image!")
        return
    
    print(f"Image size: {clean.shape}")
    
    # Simulate burst capture
    print(f"\nSimulating burst capture ({NUM_FRAMES} frames)...")
    print(f"  Noise sigma: {NOISE_SIGMA}")
    frames, shifts = simulate_burst(clean, NUM_FRAMES, NOISE_SIGMA)
    
    # Save individual frames
    for i, frame in enumerate(frames[:4]):
        cv2.imwrite(os.path.join(OUTPUT_DIR, f"06_frame_{i}.jpg"), frame)
    
    # Calculate SNR of single noisy frame
    single_snr = calculate_snr(clean, frames[0])
    print(f"\nSingle frame SNR: {single_snr:.2f} dB")
    
    # Multi-frame averaging dengan berbagai jumlah frames
    print("\nTesting dengan berbagai jumlah frames...")
    
    results = {}
    snr_values = []
    frame_counts = [1, 2, 4, 8]
    
    for n in frame_counts:
        if n <= len(frames):
            print(f"\n  Processing {n} frames...")
            if n == 1:
                averaged = frames[0]
            else:
                averaged, _ = multi_frame_average(frames[:n])
            
            snr = calculate_snr(clean, averaged)
            snr_values.append(snr)
            results[f"{n} frames"] = averaged
            
            cv2.imwrite(os.path.join(OUTPUT_DIR, f"06_averaged_{n}frames.jpg"), averaged)
            print(f"    SNR: {snr:.2f} dB")
    
    # Calculate theoretical SNR improvement
    print("\n" + "-" * 40)
    print("SNR Improvement Analysis:")
    print(f"  Theoretical: SNR increases by √N")
    print(f"  Single frame SNR: {single_snr:.2f} dB")
    
    for i, n in enumerate(frame_counts[1:], 1):
        theoretical_gain = 10 * np.log10(n)  # dB
        actual_gain = snr_values[i] - snr_values[0]
        print(f"  {n} frames: actual={actual_gain:.2f} dB, theoretical={theoretical_gain:.2f} dB")
    
    # Create comparison figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Clean Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"Single Noisy Frame\nSNR: {snr_values[0]:.1f} dB")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(results.get('2 frames', frames[0]), cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f"2 Frames Averaged\nSNR: {snr_values[1] if len(snr_values)>1 else 0:.1f} dB")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(results.get('4 frames', frames[0]), cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"4 Frames Averaged\nSNR: {snr_values[2] if len(snr_values)>2 else 0:.1f} dB")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(results.get('8 frames', frames[0]), cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"8 Frames Averaged\nSNR: {snr_values[3] if len(snr_values)>3 else 0:.1f} dB")
    axes[1, 1].axis('off')
    
    # SNR plot
    axes[1, 2].plot(frame_counts, snr_values, 'bo-', label='Actual')
    theoretical_snr = [snr_values[0] + 10*np.log10(n) for n in frame_counts]
    axes[1, 2].plot(frame_counts, theoretical_snr, 'r--', label='Theoretical')
    axes[1, 2].set_xlabel('Number of Frames')
    axes[1, 2].set_ylabel('SNR (dB)')
    axes[1, 2].set_title('SNR vs Number of Frames')
    axes[1, 2].legend()
    axes[1, 2].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "06_multiframe_comparison.png"), dpi=150)
    plt.close()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"""
Multi-frame enhancement complete!

Results:
  - Single frame SNR: {snr_values[0]:.2f} dB
  - 8 frames averaged SNR: {snr_values[-1]:.2f} dB
  - SNR improvement: {snr_values[-1] - snr_values[0]:.2f} dB

Files generated:
  - 06_frame_*.jpg: Individual noisy frames
  - 06_averaged_*frames.jpg: Averaged results
  - 06_multiframe_comparison.png: Visual comparison

Key insight:
  - Averaging N frames improves SNR by ~√N
  - Alignment is crucial for proper averaging
  - Motion detection prevents ghosting artifacts
""")
    
    # Display
    cv2.imshow("Clean Original", clean)
    cv2.imshow("Single Noisy Frame", frames[0])
    cv2.imshow("8 Frames Averaged", results.get('8 frames', frames[0]))
    print("\nTekan sembarang tombol untuk menutup...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
