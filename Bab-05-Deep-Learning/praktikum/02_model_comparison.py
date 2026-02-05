"""
=============================================================================
PRAKTIKUM 02 - PERBANDINGAN MODEL CNN
=============================================================================
Program ini membandingkan performa berbagai arsitektur CNN untuk image
classification dalam hal kecepatan inference dan ukuran model.

Konsep yang dipelajari:
1. Karakteristik berbagai arsitektur CNN
2. Trade-off antara accuracy dan speed
3. Benchmarking inference time
4. Memory footprint analysis

Arsitektur yang dibandingkan:
- MobileNet: Ringan, cocok untuk mobile
- ResNet: Deeper network dengan skip connections
- EfficientNet: Compound scaling
- VGG: Classic deep architecture

Kebutuhan:
- opencv-python >= 4.8.0
- numpy
- matplotlib (untuk visualisasi)

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import time
import os
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions



def get_model_info():
    """
    Informasi tentang berbagai arsitektur CNN.
    
    Returns:
        dict: Informasi detail setiap model
    """
    models = {
        "MobileNetV2": {
            "params": "3.5M",
            "size_mb": 14,
            "top1_accuracy": 72.0,
            "top5_accuracy": 90.9,
            "input_size": (224, 224),
            "year": 2018,
            "description": "Efficient architecture dengan depthwise separable convolutions",
            "use_case": "Mobile devices, edge deployment, real-time applications",
            "flops": "0.3B"
        },
        "ResNet50": {
            "params": "25.6M",
            "size_mb": 98,
            "top1_accuracy": 76.1,
            "top5_accuracy": 92.9,
            "input_size": (224, 224),
            "year": 2015,
            "description": "Deep residual learning dengan skip connections",
            "use_case": "General purpose, transfer learning backbone",
            "flops": "4.1B"
        },
        "VGG16": {
            "params": "138M",
            "size_mb": 528,
            "top1_accuracy": 71.5,
            "top5_accuracy": 90.4,
            "input_size": (224, 224),
            "year": 2014,
            "description": "Very deep network dengan 3x3 convolutions konsisten",
            "use_case": "Feature extraction, style transfer",
            "flops": "15.5B"
        },
        "EfficientNet-B0": {
            "params": "5.3M",
            "size_mb": 20,
            "top1_accuracy": 77.1,
            "top5_accuracy": 93.3,
            "input_size": (224, 224),
            "year": 2019,
            "description": "Compound scaling untuk balance depth/width/resolution",
            "use_case": "Best accuracy/efficiency trade-off",
            "flops": "0.4B"
        },
        "DenseNet121": {
            "params": "8M",
            "size_mb": 32,
            "top1_accuracy": 74.4,
            "top5_accuracy": 91.9,
            "input_size": (224, 224),
            "year": 2017,
            "description": "Dense connections untuk feature reuse",
            "use_case": "Medical imaging, feature extraction",
            "flops": "2.9B"
        },
        "InceptionV3": {
            "params": "23.8M",
            "size_mb": 92,
            "top1_accuracy": 77.9,
            "top5_accuracy": 93.7,
            "input_size": (299, 299),
            "year": 2015,
            "description": "Multi-scale feature extraction dengan inception modules",
            "use_case": "High accuracy applications",
            "flops": "5.7B"
        }
    }
    return models


def display_model_comparison():
    """
    Menampilkan perbandingan komprehensif berbagai model CNN.
    """
    print("\n" + "="*80)
    print("PERBANDINGAN ARSITEKTUR CNN")
    print("="*80)
    
    models = get_model_info()
    
    # Header
    print(f"\n{'Model':<18} {'Params':>10} {'Size':>8} {'Top-1':>8} {'Top-5':>8} {'FLOPs':>10}")
    print("-"*80)
    
    for name, info in models.items():
        print(f"{name:<18} {info['params']:>10} {info['size_mb']:>6}MB "
              f"{info['top1_accuracy']:>7.1f}% {info['top5_accuracy']:>7.1f}% "
              f"{info['flops']:>10}")
    
    print("-"*80)
    print("\n[INFO] Keterangan:")
    print("  - Params: Jumlah trainable parameters")
    print("  - Size: Ukuran model file")
    print("  - Top-1: Accuracy prediksi pertama benar")
    print("  - Top-5: Accuracy dalam 5 prediksi teratas")
    print("  - FLOPs: Floating-point operations per inference")


def simulate_inference_benchmark():
    """
    Simulasi benchmark inference time untuk berbagai model.
    
    Karena model sebenarnya tidak di-load, kita simulasikan
    berdasarkan karakteristik teoretis model.
    """
    print("\n" + "="*80)
    print("BENCHMARK INFERENCE TIME (SIMULATED)")
    print("="*80)
    
    # Simulated inference times (ms) berdasarkan FLOPs relatif
    benchmark_results = {
        "MobileNetV2": {"cpu_time": 25, "gpu_time": 3},
        "ResNet50": {"cpu_time": 120, "gpu_time": 12},
        "VGG16": {"cpu_time": 350, "gpu_time": 25},
        "EfficientNet-B0": {"cpu_time": 35, "gpu_time": 4},
        "DenseNet121": {"cpu_time": 95, "gpu_time": 10},
        "InceptionV3": {"cpu_time": 150, "gpu_time": 15}
    }
    
    print(f"\n{'Model':<18} {'CPU (ms)':>12} {'GPU (ms)':>12} {'CPU FPS':>10} {'GPU FPS':>10}")
    print("-"*70)
    
    for name, times in benchmark_results.items():
        cpu_fps = 1000 / times["cpu_time"]
        gpu_fps = 1000 / times["gpu_time"]
        print(f"{name:<18} {times['cpu_time']:>10} ms {times['gpu_time']:>10} ms "
              f"{cpu_fps:>10.1f} {gpu_fps:>10.1f}")
    
    print("-"*70)
    print("\n[INFO] Benchmark pada Intel Core i7 CPU / NVIDIA GTX 1080 GPU (simulated)")
    print("[INFO] Untuk real benchmark, gunakan model sebenarnya dengan timer")


def visualize_accuracy_vs_speed():
    """
    Visualisasi trade-off antara accuracy dan speed.
    """
    print("\n" + "="*80)
    print("VISUALISASI: ACCURACY VS SPEED TRADE-OFF")
    print("="*80)
    
    models = get_model_info()
    
    # Data untuk plotting (diurutkan berdasarkan accuracy)
    sorted_models = sorted(models.items(), key=lambda x: x[1]['top1_accuracy'])
    
    print("\n[ASCII PLOT] Accuracy vs Model Size")
    print("-"*60)
    
    max_width = 50
    for name, info in sorted_models:
        # Normalize accuracy untuk visualisasi
        acc_bar = int(info['top1_accuracy'] / 100 * max_width)
        size_indicator = "●" * min(5, info['size_mb'] // 100 + 1)
        
        acc_visual = "█" * acc_bar
        print(f"{name:>16}: {acc_visual} {info['top1_accuracy']:.1f}%  Size: {size_indicator}")
    
    print("-"*60)
    print("●: ~100MB model size")
    
    # Trade-off analysis
    print("\n[ANALYSIS] Trade-off Summary:")
    print("-"*60)
    
    print("\n1. BEST ACCURACY (jika speed tidak penting):")
    best_acc = max(models.items(), key=lambda x: x[1]['top1_accuracy'])
    print(f"   → {best_acc[0]}: {best_acc[1]['top1_accuracy']:.1f}% accuracy")
    
    print("\n2. BEST SPEED (jika accuracy bisa dikompromikan):")
    # Simulated speed ranking
    print(f"   → MobileNetV2: ~25ms pada CPU")
    
    print("\n3. BEST BALANCE (efficiency ratio):")
    # Efficiency = accuracy / (size * time)
    print(f"   → EfficientNet-B0: 77.1% accuracy, hanya 20MB, 35ms inference")
    
    print("\n4. BEST FOR MOBILE:")
    print(f"   → MobileNetV2: Dirancang khusus untuk mobile deployment")


def demo_preprocessing_comparison():
    """
    Membandingkan preprocessing requirements berbagai model.
    """
    print("\n" + "="*80)
    print("PREPROCESSING REQUIREMENTS PER MODEL")
    print("="*80)
    
    preprocessing_configs = {
        "MobileNetV2": {
            "input_size": (224, 224),
            "mean": (127.5, 127.5, 127.5),
            "scale": 1/127.5,
            "color_space": "RGB"
        },
        "ResNet50": {
            "input_size": (224, 224),
            "mean": (103.939, 116.779, 123.68),  # ImageNet mean (BGR)
            "scale": 1.0,
            "color_space": "BGR"
        },
        "VGG16": {
            "input_size": (224, 224),
            "mean": (103.939, 116.779, 123.68),
            "scale": 1.0,
            "color_space": "BGR"
        },
        "EfficientNet-B0": {
            "input_size": (224, 224),
            "mean": (123.675, 116.28, 103.53),
            "scale": 1/58.395,  # std normalization
            "color_space": "RGB"
        },
        "InceptionV3": {
            "input_size": (299, 299),
            "mean": (127.5, 127.5, 127.5),
            "scale": 1/127.5,
            "color_space": "RGB"
        }
    }
    
    print(f"\n{'Model':<16} {'Input Size':>12} {'Mean (approx)':>20} {'Scale':>12} {'Color':<6}")
    print("-"*75)
    
    for name, config in preprocessing_configs.items():
        mean_str = f"({config['mean'][0]:.0f},{config['mean'][1]:.0f},{config['mean'][2]:.0f})"
        print(f"{name:<16} {str(config['input_size']):>12} {mean_str:>20} "
              f"{config['scale']:>12.6f} {config['color_space']:<6}")
    
    print("-"*75)
    
    # Demo blob creation dengan berbagai config
    print("\n[CODE EXAMPLE] Blob creation per model:")
    
    print("""
# MobileNetV2 / InceptionV3 (normalized to [-1, 1])
blob = cv2.dnn.blobFromImage(image, 1/127.5, (224, 224), 
                              (127.5, 127.5, 127.5), swapRB=True)

# ResNet / VGG (ImageNet mean subtraction)
blob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), 
                              (103.939, 116.779, 123.68), swapRB=False)

# EfficientNet (normalized with std)
blob = cv2.dnn.blobFromImage(image, 1/58.395, (224, 224), 
                              (123.675, 116.28, 103.53), swapRB=True)
""")


def demo_architecture_visualization():
    """
    Visualisasi arsitektur berbagai model menggunakan ASCII art.
    """
    print("\n" + "="*80)
    print("VISUALISASI ARSITEKTUR CNN")
    print("="*80)
    
    # MobileNetV2 Architecture
    print("\n[MobileNetV2] - Depthwise Separable Convolutions")
    print("-"*60)
    print("""
    Input (224×224×3)
         │
    ┌────▼────┐
    │ Conv 3×3│ stride=2, 32 filters
    │  BN+ReLU│
    └────┬────┘
         │
    ┌────▼────────────────┐
    │ Inverted Residual   │ ← MobileNetV2 Innovation
    │ ┌─────────────────┐ │
    │ │ 1×1 Conv (expand)│ │
    │ │ 3×3 DWConv      │ │ Depthwise Separable
    │ │ 1×1 Conv (proj) │ │
    │ └─────────────────┘ │
    │   + Residual        │
    └─────────┬───────────┘
              │
         [×17 blocks]
              │
    ┌─────────▼─────────┐
    │ Global Avg Pool   │
    │ FC → 1000 classes │
    └───────────────────┘
    """)
    
    # ResNet Architecture  
    print("\n[ResNet] - Skip Connections")
    print("-"*60)
    print("""
    Input (224×224×3)
         │
    ┌────▼────┐
    │Conv 7×7 │ stride=2, 64 filters
    │ MaxPool │ 
    └────┬────┘
         │
    ┌────▼────────────────┐
    │   Residual Block    │ ← Skip Connection Innovation
    │                     │
    │  x ──┬─────────┐    │
    │      │  Conv   │    │
    │      │  BN     │    │
    │      │  ReLU   │    │
    │      │  Conv   │    │
    │      │  BN     │    │
    │      └────┬────┘    │
    │           │         │
    │     x + F(x)  ◄─────┤ Identity shortcut
    │           │         │
    │         ReLU        │
    └─────────┬───────────┘
              │
     [3,4,6,3 blocks per stage]
              │
    ┌─────────▼─────────┐
    │ Global Avg Pool   │
    │ FC → 1000 classes │
    └───────────────────┘
    """)
    
    # EfficientNet Architecture
    print("\n[EfficientNet] - Compound Scaling")
    print("-"*60)
    print("""
    Scaling Formula:
    ├── depth:  d = α^φ
    ├── width:  w = β^φ  
    ├── resolution: r = γ^φ
    └── constraint: α × β² × γ² ≈ 2
    
    EfficientNet-B0 → B7:
    ┌───────────────────────────────────────────────────────────────┐
    │  B0   │  B1   │  B2   │  B3   │  B4   │  B5   │  B6   │  B7  │
    │ 224×224│256×256│260×260│300×300│380×380│456×456│528×528│600×600│
    │ 5.3M  │ 7.8M  │ 9.2M  │ 12M   │ 19M   │ 30M   │ 43M   │ 66M  │
    │ 77.1% │ 79.1% │ 80.1% │ 81.6% │ 82.9% │ 83.6% │ 84.0% │ 84.3%│
    └───────────────────────────────────────────────────────────────┘
    
    MBConv Block (Mobile Inverted Bottleneck):
    ┌─────────────────────┐
    │ 1×1 Conv (expand)   │
    │ Depthwise 3×3/5×5   │
    │ Squeeze-Excitation  │ ← Channel attention
    │ 1×1 Conv (project)  │
    │ + Skip connection   │
    └─────────────────────┘
    """)


def demo_practical_selection():
    """
    Panduan praktis memilih model berdasarkan use case.
    """
    print("\n" + "="*80)
    print("PANDUAN PEMILIHAN MODEL")
    print("="*80)
    
    use_cases = [
        {
            "scenario": "Mobile App (Android/iOS)",
            "constraints": "Limited memory, battery, CPU-only",
            "recommendation": "MobileNetV2 atau MobileNetV3-Small",
            "reason": "Didesain untuk mobile, efisien, <4MB model size"
        },
        {
            "scenario": "Edge Device (Raspberry Pi)",
            "constraints": "Very limited compute, real-time needed",
            "recommendation": "MobileNetV2 + quantization",
            "reason": "INT8 quantization bisa 4x lebih cepat"
        },
        {
            "scenario": "Server-side Inference",
            "constraints": "Accuracy priority, GPU available",
            "recommendation": "EfficientNet-B4/B5 atau ResNet152",
            "reason": "Best accuracy, GPU memory cukup"
        },
        {
            "scenario": "Transfer Learning (small dataset)",
            "constraints": "<1000 images, fine-tuning",
            "recommendation": "ResNet50 atau EfficientNet-B0",
            "reason": "Good features, moderate capacity"
        },
        {
            "scenario": "Real-time Video Classification",
            "constraints": "30+ FPS required, accuracy secondary",
            "recommendation": "MobileNetV2 atau ShuffleNet",
            "reason": "<30ms inference pada mid-range GPU"
        },
        {
            "scenario": "Medical Imaging",
            "constraints": "High accuracy critical, GPU available",
            "recommendation": "DenseNet121 atau EfficientNet-B4",
            "reason": "Dense connections preserve fine details"
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"\n[CASE {i}] {case['scenario']}")
        print(f"  Constraints: {case['constraints']}")
        print(f"  ✓ Recommendation: {case['recommendation']}")
        print(f"  Why: {case['reason']}")
    
    print("\n" + "-"*60)
    print("[TIPS] Decision Tree:")
    print("""
                    ┌─ Accuracy penting?
                    │
            ┌───────┼───────┐
            Yes     │       No
            │       │       │
            ▼       │       ▼
    GPU available?  │    MobileNetV2
            │       │
        ┌───┴───┐   │
        Yes    No   │
        │       │   │
        ▼       ▼   │
    EfficientNet  ResNet50
       B4/B5    (reduced)
    """)


def simulate_batch_inference():
    """
    Simulasi inference dengan batch processing.
    """
    print("\n" + "="*80)
    print("BATCH INFERENCE SIMULATION")
    print("="*80)
    
    # Generate sample images
    num_images = 8
    batch_size = 4
    
    print(f"\n[INFO] Processing {num_images} images with batch_size={batch_size}")
    
    # Simulate batch creation
    sample_images = [
        np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        for _ in range(num_images)
    ]
    
    # Simulate single inference timing
    print("\n[BENCHMARK] Single vs Batch Processing:")
    print("-"*50)
    
    # Single processing simulation
    single_start = time.time()
    for img in sample_images:
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (224, 224), (0, 0, 0), swapRB=True)
        # Simulate inference time
        time.sleep(0.02)  # 20ms per image
    single_time = time.time() - single_start
    
    # Batch processing simulation
    batch_start = time.time()
    for i in range(0, num_images, batch_size):
        batch_imgs = sample_images[i:i+batch_size]
        
        # Create batch blob
        blobs = [cv2.dnn.blobFromImage(img, 1/255.0, (224, 224), (0, 0, 0), swapRB=True)
                 for img in batch_imgs]
        batch_blob = np.vstack(blobs)
        
        # Simulate batch inference (more efficient on GPU)
        time.sleep(0.05)  # 50ms per batch (vs 80ms for 4 singles)
    batch_time = time.time() - batch_start
    
    print(f"Single processing: {single_time:.3f}s ({single_time/num_images*1000:.1f}ms/image)")
    print(f"Batch processing:  {batch_time:.3f}s ({batch_time/num_images*1000:.1f}ms/image)")
    print(f"Speedup: {single_time/batch_time:.2f}x")
    
    print("""
[INFO] Batch processing benefits:
  1. Reduced overhead per image
  2. Better GPU utilization
  3. Memory bandwidth efficiency
  4. Parallelism in matrix operations
    """)


def main():
    """
    Fungsi utama untuk menjalankan semua demonstrasi.
    """
    print("="*80)
    print("PRAKTIKUM PERBANDINGAN MODEL CNN")
    print("="*80)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Perbandingan Model (Tabel)")
        print("2. Benchmark Inference Time")
        print("3. Accuracy vs Speed Trade-off")
        print("4. Preprocessing Requirements")
        print("5. Visualisasi Arsitektur")
        print("6. Panduan Pemilihan Model")
        print("7. Batch Inference Simulation")
        print("8. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-8): ").strip()
        
        if choice == '1':
            display_model_comparison()
        elif choice == '2':
            simulate_inference_benchmark()
        elif choice == '3':
            visualize_accuracy_vs_speed()
        elif choice == '4':
            demo_preprocessing_comparison()
        elif choice == '5':
            demo_architecture_visualization()
        elif choice == '6':
            demo_practical_selection()
        elif choice == '7':
            simulate_batch_inference()
        elif choice == '8':
            display_model_comparison()
            simulate_inference_benchmark()
            visualize_accuracy_vs_speed()
            demo_preprocessing_comparison()
            demo_architecture_visualization()
            demo_practical_selection()
            simulate_batch_inference()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
