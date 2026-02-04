#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 6: MONOCULAR DEPTH ESTIMATION (MiDaS)
=============================================================================
Deskripsi:
    Program untuk melakukan estimasi kedalaman dari gambar single view
    menggunakan deep learning model MiDaS (Mixed Data Sampling).

Konsep Monocular Depth Estimation:
    - Mengestimasi depth dari satu gambar saja (tanpa stereo)
    - Menggunakan visual cues: texture gradient, perspective, occlusion
    - Deep learning mempelajari depth patterns dari training data
    - Output adalah relative depth (tidak absolute)

MiDaS:
    - Dikembangkan oleh Intel ISL
    - Ditraining pada campuran banyak dataset
    - Zero-shot generalization yang baik
    - Tersedia dalam berbagai ukuran model

Model Options:
    - MiDaS Small (midas_v21_small): Cepat, cocok untuk real-time
    - MiDaS Large (midas_v21_large): Lebih akurat, lebih lambat
    - DPT Hybrid: Transformer-based, state-of-the-art

Limitasi:
    - Output adalah relative depth (tidak dalam meter)
    - Tidak ada informasi scale absolut
    - Akurasi lebih rendah dari stereo pada beberapa kasus

Output:
    - Relative depth map
    - Visualisasi dengan colormap
    - Perbandingan dengan stereo (jika tersedia)

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
Dependensi: torch, torchvision, timm, opencv-python
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time

# =============================================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# =============================================================================

# Path ke gambar input
DATA_DIR = Path(__file__).parent / "data"
INPUT_IMAGE = DATA_DIR / "images" / "street_scene.png"
INPUT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_left.png"

# Path output
OUTPUT_DIR = Path(__file__).parent / "output" / "output6" / "depth_mono"

# Model MiDaS yang digunakan
# Options: "MiDaS_small", "DPT_Large", "DPT_Hybrid"
# "MiDaS_small" - cepat, untuk real-time
# "DPT_Large" - akurat tapi lambat
# "DPT_Hybrid" - balance antara speed dan akurasi
MIDAS_MODEL = "MiDaS_small"

# Device untuk inference
# "cuda" untuk GPU, "cpu" untuk CPU
DEVICE = "cpu"  # Akan di-override jika CUDA tersedia

# Colormap untuk visualisasi
COLORMAP = cv2.COLORMAP_INFERNO

# Enable comparison dengan stereo depth (jika tersedia)
COMPARE_WITH_STEREO = True
STEREO_DEPTH_FILE = DATA_DIR / "depth" / "depth_meters.npy"

# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def check_torch_availability():
    """
    Memeriksa ketersediaan PyTorch dan CUDA.
    
    Returns:
        Tuple (torch_available, device)
    """
    try:
        import torch
        
        # Check CUDA
        if torch.cuda.is_available():
            device = "cuda"
            print(f"[OK] PyTorch {torch.__version__} with CUDA support")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            print(f"[OK] PyTorch {torch.__version__} (CPU only)")
        
        return True, device
    
    except ImportError:
        print("[ERROR] PyTorch tidak tersedia")
        print("  Install dengan: pip install torch torchvision")
        return False, "cpu"


def load_midas_model(model_type="MiDaS_small", device="cpu"):
    """
    Memuat model MiDaS menggunakan torch hub.
    
    Args:
        model_type: Tipe model ("MiDaS_small", "DPT_Large", "DPT_Hybrid")
        device: "cuda" atau "cpu"
        
    Returns:
        Tuple (model, transform) atau (None, None) jika gagal
    """
    try:
        import torch
        
        print(f"\n[INFO] Loading MiDaS model: {model_type}")
        print("  (Download otomatis jika belum ada)")
        
        # Load model dari torch hub
        model = torch.hub.load("intel-isl/MiDaS", model_type, trust_repo=True)
        
        # Load transform yang sesuai
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
        
        if model_type in ["DPT_Large", "DPT_Hybrid"]:
            transform = midas_transforms.dpt_transform
        else:
            transform = midas_transforms.small_transform
        
        # Move to device
        model.to(device)
        model.eval()
        
        print(f"[OK] Model loaded successfully")
        
        return model, transform
    
    except Exception as e:
        print(f"[ERROR] Gagal memuat model: {e}")
        return None, None


def predict_depth(model, transform, image, device="cpu"):
    """
    Memprediksi depth dari gambar menggunakan MiDaS.
    
    Args:
        model: MiDaS model
        transform: Transform untuk preprocessing
        image: Input image (BGR, numpy array)
        device: "cuda" atau "cpu"
        
    Returns:
        Tuple (depth_map, inference_time)
    """
    import torch
    
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Apply transform
    input_batch = transform(img_rgb).to(device)
    
    # Inference
    start_time = time.time()
    with torch.no_grad():
        prediction = model(input_batch)
        
        # Interpolate to original size
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()
    
    inference_time = (time.time() - start_time) * 1000
    
    # Convert to numpy
    depth = prediction.cpu().numpy()
    
    return depth, inference_time


def normalize_depth(depth, method="minmax"):
    """
    Normalisasi depth map untuk visualisasi.
    
    Args:
        depth: Raw depth prediction
        method: "minmax" atau "robust"
        
    Returns:
        Normalized depth (0-1)
    """
    if method == "minmax":
        depth_min = depth.min()
        depth_max = depth.max()
        normalized = (depth - depth_min) / (depth_max - depth_min + 1e-8)
    elif method == "robust":
        # Use percentile for robustness to outliers
        p2 = np.percentile(depth, 2)
        p98 = np.percentile(depth, 98)
        normalized = (depth - p2) / (p98 - p2 + 1e-8)
        normalized = np.clip(normalized, 0, 1)
    else:
        normalized = depth
    
    return normalized


def visualize_depth(depth, colormap=cv2.COLORMAP_INFERNO, invert=True):
    """
    Membuat visualisasi depth dengan colormap.
    
    Args:
        depth: Normalized depth map (0-1)
        colormap: OpenCV colormap
        invert: Invert sehingga dekat = terang, jauh = gelap
        
    Returns:
        Colored depth image (BGR)
    """
    # Convert to 8-bit
    depth_8bit = (depth * 255).astype(np.uint8)
    
    if invert:
        depth_8bit = 255 - depth_8bit
    
    # Apply colormap
    depth_colored = cv2.applyColorMap(depth_8bit, colormap)
    
    return depth_colored


def compare_mono_stereo(mono_depth, stereo_depth):
    """
    Membandingkan monocular dan stereo depth.
    
    Args:
        mono_depth: Monocular depth (normalized 0-1)
        stereo_depth: Stereo depth (dalam meter)
        
    Returns:
        Dictionary dengan comparison metrics
    """
    # Normalize stereo depth untuk perbandingan
    valid_stereo = stereo_depth > 0
    
    if np.sum(valid_stereo) == 0:
        return {'correlation': float('nan')}
    
    stereo_norm = normalize_depth(stereo_depth[valid_stereo])
    mono_norm = normalize_depth(mono_depth[valid_stereo])
    
    # Correlation
    correlation = np.corrcoef(mono_norm.flatten(), stereo_norm.flatten())[0, 1]
    
    return {
        'correlation': correlation,
        'valid_pixels': np.sum(valid_stereo)
    }


def process_video_realtime(model, transform, device, video_source=0):
    """
    Proses video secara real-time dengan MiDaS.
    
    Args:
        model: MiDaS model
        transform: Transform untuk preprocessing
        device: "cuda" atau "cpu"
        video_source: 0 untuk webcam atau path ke video
    """
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("[ERROR] Tidak bisa membuka video source")
        return
    
    print("\n[INFO] Real-time depth estimation")
    print("  Press 'q' to quit")
    
    fps_list = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize untuk speed
        frame_small = cv2.resize(frame, (384, 288))
        
        # Predict depth
        depth, inf_time = predict_depth(model, transform, frame_small, device)
        
        # Normalize dan visualize
        depth_norm = normalize_depth(depth)
        depth_vis = visualize_depth(depth_norm)
        
        # Resize back
        depth_vis = cv2.resize(depth_vis, (frame.shape[1], frame.shape[0]))
        
        # Calculate FPS
        fps = 1000 / inf_time
        fps_list.append(fps)
        avg_fps = np.mean(fps_list[-30:])  # Average of last 30 frames
        
        # Combine
        combined = np.hstack([frame, depth_vis])
        
        # Add info
        cv2.putText(combined, f"FPS: {avg_fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(combined, "RGB", (frame.shape[1]//2 - 30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(combined, "Depth", (frame.shape[1] + frame.shape[1]//2 - 40, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.imshow("MiDaS Real-time Depth", combined)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def create_synthetic_scene():
    """
    Membuat scene sintetis dengan depth cues yang jelas.
    """
    height, width = 480, 640
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Sky gradient (distance cue)
    for y in range(height // 3):
        blue_val = 200 - int(y * 0.5)
        img[y, :] = [blue_val, 150, 100]
    
    # Ground with perspective
    for y in range(height // 3, height):
        ratio = (y - height // 3) / (2 * height // 3)
        green = int(100 + 50 * (1 - ratio))
        brown = int(80 + 40 * ratio)
        img[y, :] = [60, green, brown]
    
    # Add road with perspective
    vanishing_point = (width // 2, height // 3)
    road_bottom_left = (width // 4, height)
    road_bottom_right = (3 * width // 4, height)
    
    pts = np.array([
        vanishing_point,
        road_bottom_left,
        road_bottom_right
    ], np.int32)
    cv2.fillPoly(img, [pts], (100, 100, 100))
    
    # Add trees with size gradient (closer = bigger)
    tree_positions = [
        (100, 320, 80),   # x, base_y, height - big tree (close)
        (550, 300, 50),   # medium tree
        (450, 200, 20),   # small tree (far)
        (200, 220, 25),   # small tree (far)
    ]
    
    for x, base_y, h in tree_positions:
        # Tree trunk
        cv2.rectangle(img, (x-h//10, base_y), (x+h//10, base_y-h//2), 
                     (30, 60, 80), -1)
        # Tree crown
        cv2.circle(img, (x, base_y-h//2-h//4), h//3, (50, 150, 50), -1)
    
    # Add car with size cue
    car_y = height - 80
    car_width = 100
    cv2.rectangle(img, (width//2-car_width//2, car_y),
                 (width//2+car_width//2, car_y+40), (0, 0, 180), -1)
    cv2.rectangle(img, (width//2-car_width//3, car_y-25),
                 (width//2+car_width//3, car_y), (0, 0, 150), -1)
    
    # Add sun
    cv2.circle(img, (550, 50), 40, (0, 200, 255), -1)
    
    return img


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("MONOCULAR DEPTH ESTIMATION (MiDaS)")
    print("="*60)
    print(f"Model: {MIDAS_MODEL}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check PyTorch
    print("\n[STEP 1] Memeriksa PyTorch...")
    torch_available, device = check_torch_availability()
    
    if not torch_available:
        print("\n[ERROR] PyTorch diperlukan untuk MiDaS")
        print("Install dengan: pip install torch torchvision timm")
        
        # Demo dengan fallback
        print("\n[INFO] Menampilkan gambar sintetis sebagai demo...")
        img = create_synthetic_scene()
        cv2.imshow("Synthetic Scene (PyTorch needed for depth)", img)
        cv2.waitKey(0)
        return
    
    # Override device dari config
    if DEVICE == "cuda" and device != "cuda":
        print(f"[WARNING] CUDA requested but not available, using CPU")
        device = "cpu"
    else:
        device = DEVICE if DEVICE == "cpu" else device
    
    # Load model
    print("\n[STEP 2] Memuat model MiDaS...")
    model, transform = load_midas_model(MIDAS_MODEL, device)
    
    if model is None:
        print("[ERROR] Gagal memuat model")
        return
    
    # Load input image
    print("\n[STEP 3] Memuat gambar input...")
    
    img = cv2.imread(str(INPUT_IMAGE))
    if img is None:
        img = cv2.imread(str(INPUT_IMAGE_FALLBACK))
    if img is None:
        print("[INFO] Gambar tidak ditemukan. Membuat gambar sintetis...")
        img = create_synthetic_scene()
    
    print(f"  Image size: {img.shape[1]}x{img.shape[0]}")
    
    # Predict depth
    print("\n[STEP 4] Memprediksi depth...")
    depth_raw, inference_time = predict_depth(model, transform, img, device)
    
    print(f"  Inference time: {inference_time:.2f} ms ({1000/inference_time:.1f} fps)")
    
    # Normalize
    print("\n[STEP 5] Normalisasi dan visualisasi...")
    depth_norm = normalize_depth(depth_raw, method="robust")
    depth_vis = visualize_depth(depth_norm, COLORMAP)
    
    # Save results
    cv2.imwrite(str(OUTPUT_DIR / "depth_mono.png"), depth_vis)
    np.save(str(OUTPUT_DIR / "depth_mono_raw.npy"), depth_raw)
    print(f"  Saved: {OUTPUT_DIR / 'depth_mono.png'}")
    
    # Compare with stereo if available
    if COMPARE_WITH_STEREO and STEREO_DEPTH_FILE.exists():
        print("\n[STEP 6] Membandingkan dengan stereo depth...")
        stereo_depth = np.load(str(STEREO_DEPTH_FILE))
        
        # Resize if needed
        if stereo_depth.shape != depth_norm.shape:
            stereo_depth = cv2.resize(stereo_depth, (depth_norm.shape[1], depth_norm.shape[0]))
        
        comparison = compare_mono_stereo(depth_norm, stereo_depth)
        print(f"  Correlation with stereo: {comparison['correlation']:.3f}")
    
    # Display results
    print("\n[STEP 7] Menampilkan hasil...")
    
    # Create matplotlib figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Original image
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Input Image")
    axes[0, 0].axis('off')
    
    # Raw depth
    im1 = axes[0, 1].imshow(depth_raw, cmap='inferno')
    axes[0, 1].set_title("MiDaS Raw Output (Relative Depth)")
    axes[0, 1].axis('off')
    plt.colorbar(im1, ax=axes[0, 1])
    
    # Depth histogram
    axes[1, 0].hist(depth_norm.flatten(), bins=50, color='blue', alpha=0.7)
    axes[1, 0].set_xlabel("Normalized Depth")
    axes[1, 0].set_ylabel("Frequency")
    axes[1, 0].set_title("Depth Distribution")
    
    # Visualized depth
    axes[1, 1].imshow(cv2.cvtColor(depth_vis, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"Depth Visualization\n({MIDAS_MODEL}, {inference_time:.0f}ms)")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "midas_analysis.png"), dpi=150, bbox_inches='tight')
    
    # OpenCV display
    combined = np.hstack([img, depth_vis])
    cv2.putText(combined, "Input", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(combined, f"MiDaS Depth ({inference_time:.0f}ms)", (img.shape[1] + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    cv2.imshow("Monocular Depth Estimation", combined)
    
    plt.show()
    
    # Ask for real-time demo
    print("\n" + "="*60)
    print("Tekan 'r' untuk real-time webcam demo")
    print("Tekan sembarang tombol lain untuk keluar")
    print("="*60)
    
    key = cv2.waitKey(0)
    
    if key == ord('r'):
        cv2.destroyAllWindows()
        process_video_realtime(model, transform, device)
    
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] Monocular depth estimation selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")
    
    # Print notes
    print("\n" + "="*60)
    print("CATATAN PENTING")
    print("="*60)
    print("1. Output MiDaS adalah RELATIVE depth, bukan absolute")
    print("2. Tidak ada informasi scale (tidak dalam meter)")
    print("3. Untuk absolute depth, perlu kalibrasi dengan ground truth")
    print("4. Monocular depth berguna untuk:")
    print("   - Bokeh effect")
    print("   - Depth-based compositing")
    print("   - Scene understanding")
    print("   - Augmented reality")


if __name__ == "__main__":
    main()
