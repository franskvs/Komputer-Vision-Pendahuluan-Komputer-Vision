"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 01 - OPENCV DNN: IMAGE CLASSIFICATION
# Assignment - set nilai ke variabel
=============================================================================
Program ini mendemonstrasikan penggunaan OpenCV DNN module untuk melakukan
image classification menggunakan pre-trained models dari berbagai frameworks.

OpenCV DNN memungkinkan inferencing tanpa dependency ke PyTorch/TensorFlow,
sangat berguna untuk deployment di environment yang terbatas.

Konsep yang dipelajari:
1. Memuat model dari berbagai formats (ONNX, Caffe, TensorFlow)
2. Preprocessing dengan blobFromImage()
3. Forward pass dan interpretasi output
4. ImageNet classification dengan 1000 classes

Kebutuhan:
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy
- Koneksi internet untuk download model pertama kali

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import cv2
# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import os
# Import library/module untuk digunakan
import urllib.request
# Import library/module untuk digunakan
from pathlib import Path
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions



# Definisi function dengan nama dan parameter
def download_file(url, filepath):
    """
    Download file dari URL jika belum ada.
    
    Args:
        url: URL file yang akan didownload
        filepath: Path tujuan penyimpanan file
    """
    # Conditional statement - eksekusi jika kondisi True
    if not os.path.exists(filepath):
        print(f"Downloading {os.path.basename(filepath)}...")
        print(f"URL: {url}")
        # Blok try-except untuk error handling
        try:
            # Buat direktori jika belum ada
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Download dengan progress indicator
            def show_progress(block_num, block_size, total_size):
                # Conditional statement - eksekusi jika kondisi True
                if total_size > 0:
                    # Assignment - set nilai ke variabel
                    percent = min(100, block_num * block_size * 100 / total_size)
                    # Assignment - set nilai ke variabel
                    print(f"\rProgress: {percent:.1f}%", end="")
            
            urllib.request.urlretrieve(url, filepath, show_progress)
            print("\nDownload complete!")
        # Tangkap exception jika ada error di blok try
        except Exception as e:
            print(f"\nError downloading: {e}")
            # Return value dari function
            return False
    else:
        print(f"File already exists: {filepath}")
    # Return value dari function
    return True


# Definisi function dengan nama dan parameter
def load_imagenet_labels(labels_path):
    """
    Memuat daftar label ImageNet.
    
    ImageNet memiliki 1000 classes dari berbagai kategori
    seperti hewan, kendaraan, objek sehari-hari, dll.
    
    Args:
        labels_path: Path ke file labels
        
    Returns:
        list: Daftar nama class
    """
    # Conditional statement - eksekusi jika kondisi True
    if os.path.exists(labels_path):
        # Buka file dengan context manager (otomatis close)
        with open(labels_path, 'r') as f:
            # Iterasi/loop melalui elemen dalam koleksi
            labels = [line.strip() for line in f.readlines()]
        # Return value dari function
        return labels
    else:
        # Generate dummy labels jika file tidak ada
        print("Warning: Labels file not found, using dummy labels")
        # Iterasi/loop melalui elemen dalam koleksi
        return [f"Class_{i}" for i in range(1000)]


# Definisi function dengan nama dan parameter
def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocessing gambar untuk neural network.
    
    Langkah-langkah:
    1. Resize ke ukuran yang diharapkan network
    2. Konversi ke blob dengan normalization
    3. Mean subtraction (ImageNet mean values)
    
    Args:
        image: Input image (BGR format dari OpenCV)
        target_size: Ukuran input yang diharapkan network
        
    Returns:
        blob: 4D tensor siap untuk network (1, C, H, W)
    """
    # Mean values ImageNet (RGB order) - digunakan untuk normalization
    # Nilai ini adalah rata-rata pixel dari dataset ImageNet
    imagenet_mean = (104.0, 117.0, 123.0)  # BGR order untuk OpenCV
    
    # Buat blob dari gambar
    # blobFromImage melakukan:
    # 1. Resize gambar ke target_size
    # 2. Mean subtraction
    # 3. Optional scaling
    # 4. Swap channels jika diperlukan (BGR to RGB)
    # 5. Reshape ke 4D tensor (batch, channels, height, width)
    blob = cv2.dnn.blobFromImage(
        image,
        # Assignment - set nilai ke variabel
        scalefactor=1.0,        # Scale factor untuk pixel values
        # Assignment - set nilai ke variabel
        size=target_size,        # Target size (width, height)
        # Assignment - set nilai ke variabel
        mean=imagenet_mean,      # Mean subtraction values
        # Assignment - set nilai ke variabel
        swapRB=False,           # Tidak swap karena model expects BGR
        # Assignment - set nilai ke variabel
        crop=False              # Resize tanpa crop
    )
    
    # Return value dari function
    return blob


# Definisi function dengan nama dan parameter
def demo_classification_basic():
    """
    Demonstrasi klasifikasi gambar dasar menggunakan MobileNet.
    
    MobileNet adalah arsitektur CNN yang efisien dan ringan,
    cocok untuk deployment pada perangkat dengan resources terbatas.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEMO: Basic Image Classification dengan MobileNet")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Paths untuk model dan labels
    models_dir = "models"
    # Assignment - set nilai ke variabel
    os.makedirs(models_dir, exist_ok=True)
    
    # MobileNet V2 dari OpenCV model zoo
    # URL bisa berubah, cek OpenCV documentation untuk update
    model_config = os.path.join(models_dir, "mobilenet_v2.pbtxt")
    # Assignment - set nilai ke variabel
    model_weights = os.path.join(models_dir, "mobilenet_v2.pb")
    # Assignment - set nilai ke variabel
    labels_path = os.path.join(models_dir, "imagenet_labels.txt")
    
    # Buat dummy model info jika tidak tersedia
    print("\n[INFO] Untuk menjalankan demo ini, Anda perlu:")
    print("1. Download MobileNet V2 model (.pb format)")
    print("2. Download config file (.pbtxt)")  
    print("3. Download ImageNet labels")
    print("\nAlternatively, gunakan demo_classification_with_caffe() yang lebih mudah")
    
    # Demo dengan synthetic data
    print("\n[DEMO MODE] Menggunakan synthetic inference simulation...")
    
    # Buat gambar test
    test_image = create_sample_image()
    
    print(f"\n[INFO] Input image shape: {test_image.shape}")
    print("[INFO] Preprocessing image...")
    
    # Demo preprocessing
    blob = preprocess_image(test_image)
    print(f"[INFO] Blob shape: {blob.shape}")
    print(f"       - Batch size: {blob.shape[0]}")
    print(f"       - Channels: {blob.shape[1]}")
    print(f"       - Height: {blob.shape[2]}")
    print(f"       - Width: {blob.shape[3]}")
    
    # Simulate classification output
    print("\n[SIMULATED] Top 5 predictions:")
    # Assignment - set nilai ke variabel
    dummy_predictions = [
        ("daisy", 0.892),
        ("sunflower", 0.051),
        ("rose", 0.023),
        ("tulip", 0.018),
        ("dandelion", 0.009)
    ]
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i, (label, prob) in enumerate(dummy_predictions, 1):
        # Assignment - set nilai ke variabel
        bar = "█" * int(prob * 40)
        print(f"  {i}. {label:20s} {prob:.3f} {bar}")
    
    # Tampilkan gambar
    display = test_image.copy()
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(display, f"Predicted: {dummy_predictions[0][0]}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(display, f"Confidence: {dummy_predictions[0][1]:.2%}", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
    
    # Tampilkan gambar di window
    cv2.imshow("Classification Result (Simulated)", display)
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_blob_creation():
    """
    Demonstrasi pembuatan blob dan parameter-parameternya.
    
    Blob adalah representasi 4D tensor dari gambar yang siap
    dimasukkan ke neural network.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEMO: Blob Creation dan Parameter Effects")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Buat gambar test
    image = create_sample_image()
    # Assignment - set nilai ke variabel
    h, w = image.shape[:2]
    print(f"\n[INFO] Original image: {w}x{h}")
    
    # Demo berbagai parameter blob
    configs = [
        {
            "name": "Standard (224x224, normalized)",
            "params": {"scalefactor": 1/255.0, "size": (224, 224), 
                      "mean": (0, 0, 0), "swapRB": True, "crop": False}
        },
        {
            "name": "ImageNet preprocessing",
            "params": {"scalefactor": 1.0, "size": (224, 224), 
                      "mean": (104, 117, 123), "swapRB": False, "crop": False}
        },
        {
            "name": "With center crop",
            "params": {"scalefactor": 1/255.0, "size": (224, 224), 
                      "mean": (0, 0, 0), "swapRB": True, "crop": True}
        },
        {
            "name": "Different input size (300x300)",
            "params": {"scalefactor": 1.0, "size": (300, 300), 
                      "mean": (127.5, 127.5, 127.5), "swapRB": True, "crop": False}
        }
    ]
    
    print("\n[INFO] Berbagai konfigurasi blob:")
    print("-" * 60)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for config in configs:
        # Konversi gambar ke blob untuk neural network
        blob = cv2.dnn.blobFromImage(image, **config["params"])
        
        print(f"\n{config['name']}:")
        print(f"  Shape: {blob.shape}")
        # Assignment - set nilai ke variabel
        print(f"  Params: scalefactor={config['params']['scalefactor']}, "
              # Assignment - set nilai ke variabel
              f"size={config['params']['size']}")
        print(f"  Mean subtraction: {config['params']['mean']}")
        print(f"  Value range: [{blob.min():.3f}, {blob.max():.3f}]")
    
    # Visualisasi blob
    print("\n[INFO] Menampilkan visualisasi blob channels...")
    
    # Konversi gambar ke blob untuk neural network
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (224, 224), 
                                  # Assignment - set nilai ke variabel
                                  (0, 0, 0), swapRB=True, crop=False)
    
    # Extract channels
    r_channel = blob[0, 0, :, :]  # Red (karena swapRB=True)
    # Assignment - set nilai ke variabel
    g_channel = blob[0, 1, :, :]  # Green
    # Assignment - set nilai ke variabel
    b_channel = blob[0, 2, :, :]  # Blue
    
    # Normalize untuk display
    r_display = (r_channel * 255).astype(np.uint8)
    # Assignment - set nilai ke variabel
    g_display = (g_channel * 255).astype(np.uint8)
    # Assignment - set nilai ke variabel
    b_display = (b_channel * 255).astype(np.uint8)
    
    # Gabungkan untuk display
    channels_vis = np.hstack([r_display, g_display, b_display])
    # Ubah ukuran gambar ke resolusi baru
    channels_vis = cv2.resize(channels_vis, (672, 224))
    
    # Tambah labels
    labels_img = np.zeros((40, 672), dtype=np.uint8)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(labels_img, "Red Channel", (50, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 1)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(labels_img, "Green Channel", (274, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 1)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(labels_img, "Blue Channel", (498, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 1)
    
    # Assignment - set nilai ke variabel
    combined = np.vstack([labels_img, channels_vis])
    
    # Tampilkan gambar di window
    cv2.imshow("Blob Channels (after RGB swap)", combined)
    # Tampilkan gambar di window
    cv2.imshow("Original Image", image)
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_classification_workflow():
    """
    Demonstrasi workflow lengkap image classification.
    
    Workflow:
    1. Load image
    2. Preprocess (blob creation)
    3. Forward pass
    4. Post-process (softmax, top-k)
    5. Display results
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEMO: Complete Classification Workflow")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Buat beberapa gambar test dengan variasi
    images = []
    # Assignment - set nilai ke variabel
    labels = ["Landscape", "Portrait", "Object", "Pattern"]
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(4):
        # Assignment - set nilai ke variabel
        img = create_sample_image(variation=i)
        images.append((img, labels[i]))
    
    print("\n[INFO] Processing 4 test images...")
    
    # Simulate batch processing
    results = []
    # Iterasi/loop melalui elemen dalam koleksi
    for img, label in images:
        # Assignment - set nilai ke variabel
        blob = preprocess_image(img)
        
        # Simulate network output (random softmax distribution)
        np.random.seed(hash(label) % 2**32)
        # Assignment - set nilai ke variabel
        logits = np.random.randn(1000)
        # Assignment - set nilai ke variabel
        probabilities = softmax(logits)
        
        # Get top 5
        top_indices = np.argsort(probabilities)[::-1][:5]
        # Assignment - set nilai ke variabel
        top_probs = probabilities[top_indices]
        
        results.append({
            'image': img,
            'label': label,
            'top_classes': top_indices,
            'top_probs': top_probs
        })
    
    # Display results
    for i, result in enumerate(results):
        print(f"\n[Image {i+1}: {result['label']}]")
        print(f"  Blob shape: {preprocess_image(result['image']).shape}")
        # Definisi class untuk membuat object
        print(f"  Top prediction class index: {result['top_classes'][0]}")
        print(f"  Top confidence: {result['top_probs'][0]:.4f}")
    
    # Visualisasi grid
    display_grid = []
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(0, 4, 2):
        # Assignment - set nilai ke variabel
        row = np.hstack([
            # Ubah ukuran gambar ke resolusi baru
            cv2.resize(results[i]['image'], (200, 200)),
            # Ubah ukuran gambar ke resolusi baru
            cv2.resize(results[i+1]['image'], (200, 200))
        ])
        display_grid.append(row)
    
    # Assignment - set nilai ke variabel
    grid = np.vstack(display_grid)
    
    # Add text overlay
    cv2.putText(grid, "Image 1", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(grid, "Image 2", (210, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(grid, "Image 3", (10, 230), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(grid, "Image 4", (210, 230), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Tampilkan gambar di window
    cv2.imshow("Classification Workflow Demo", grid)
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def softmax(x):
    """
    Compute softmax values untuk array of scores.
    
    Softmax mengkonversi raw logits menjadi probability distribution.
    # Assignment - set nilai ke variabel
    Formula: softmax(x_i) = exp(x_i) / sum(exp(x_j))
    
    Args:
        x: Array of raw scores (logits)
        
    Returns:
        # Assignment - set nilai ke variabel
        Array of probabilities (sum = 1)
    """
    # Subtract max untuk numerical stability
    exp_x = np.exp(x - np.max(x))
    # Return value dari function
    return exp_x / exp_x.sum()


# Definisi function dengan nama dan parameter
def demo_inference_backends():
    """
    Demonstrasi berbagai inference backends yang didukung OpenCV DNN.
    
    Backends menentukan hardware mana yang digunakan untuk inference.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEMO: Inference Backends")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("\n[INFO] OpenCV DNN Supported Backends:")
    print("-" * 50)
    
    # Assignment - set nilai ke variabel
    backends = [
        ("DNN_BACKEND_DEFAULT", "Default backend (usually CPU)"),
        ("DNN_BACKEND_OPENCV", "OpenCV implementation"),
        ("DNN_BACKEND_INFERENCE_ENGINE", "Intel OpenVINO"),
        ("DNN_BACKEND_CUDA", "NVIDIA CUDA (requires OpenCV built with CUDA)")
    ]
    
    # Assignment - set nilai ke variabel
    targets = [
        ("DNN_TARGET_CPU", "CPU inference"),
        ("DNN_TARGET_OPENCL", "OpenCL (GPU)"),
        ("DNN_TARGET_CUDA", "NVIDIA CUDA"),
        ("DNN_TARGET_CUDA_FP16", "NVIDIA CUDA with FP16")
    ]
    
    print("\nBackends:")
    # Iterasi/loop melalui elemen dalam koleksi
    for name, desc in backends:
        # Assignment - set nilai ke variabel
        value = getattr(cv2.dnn, name, "N/A")
        print(f"  cv2.dnn.{name}: {value} - {desc}")
    
    print("\nTargets:")
    # Iterasi/loop melalui elemen dalam koleksi
    for name, desc in targets:
        # Assignment - set nilai ke variabel
        value = getattr(cv2.dnn, name, "N/A")
        print(f"  cv2.dnn.{name}: {value} - {desc}")
    
    print("\n[INFO] Untuk menggunakan backend/target:")
    print("  net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)")
    print("  net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)")
    
    # Check CUDA availability
    print("\n[INFO] Checking CUDA availability...")
    # Conditional statement - eksekusi jika kondisi True
    cuda_available = cv2.cuda.getCudaEnabledDeviceCount() > 0 if hasattr(cv2, 'cuda') else False
    # Conditional statement - eksekusi jika kondisi True
    if cuda_available:
        print(f"  CUDA devices found: {cv2.cuda.getCudaEnabledDeviceCount()}")
    else:
        print("  CUDA not available (OpenCV not built with CUDA support)")


# Definisi function dengan nama dan parameter
def create_sample_image(variation=0):
    """
    Membuat sample image untuk demonstrasi.
    
    Args:
        variation: Variasi gambar (0-3)
        
    Returns:
        numpy array: BGR image
    """
    # Assignment - set nilai ke variabel
    size = 300
    
    # Conditional statement - eksekusi jika kondisi True
    if variation == 0:
        # Gradient dengan shapes
        image = np.zeros((size, size, 3), dtype=np.uint8)
        # Iterasi/loop melalui elemen dalam koleksi
        for y in range(size):
            # Iterasi/loop melalui elemen dalam koleksi
            for x in range(size):
                # Assignment - set nilai ke variabel
                image[y, x] = [
                    int(255 * x / size),
                    int(255 * y / size),
                    int(128 + 127 * np.sin(x/30 + y/30))
                ]
        # Add circle
        cv2.circle(image, (150, 150), 80, (255, 255, 0), -1)
        
    # Conditional statement - eksekusi jika kondisi True
    elif variation == 1:
        # Concentric circles
        image = np.zeros((size, size, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        center = (size // 2, size // 2)
        # Iterasi/loop melalui elemen dalam koleksi
        for r in range(150, 10, -20):
            # Generate random integer dalam range tertentu
            color = (np.random.randint(50, 255), 
                    # Generate random integer dalam range tertentu
                    np.random.randint(50, 255),
                    # Generate random integer dalam range tertentu
                    np.random.randint(50, 255))
            # Gambar lingkaran pada gambar
            cv2.circle(image, center, r, color, -1)
            
    # Conditional statement - eksekusi jika kondisi True
    elif variation == 2:
        # Rectangle pattern
        image = np.ones((size, size, 3), dtype=np.uint8) * 200
        # Iterasi/loop melalui elemen dalam koleksi
        for i in range(0, size, 40):
            # Iterasi/loop melalui elemen dalam koleksi
            for j in range(0, size, 40):
                # Generate random integer dalam range tertentu
                color = (np.random.randint(0, 200),
                        # Generate random integer dalam range tertentu
                        np.random.randint(0, 200),
                        # Generate random integer dalam range tertentu
                        np.random.randint(0, 200))
                # Gambar persegi panjang pada gambar
                cv2.rectangle(image, (i, j), (i+35, j+35), color, -1)
                
    else:
        # Noise pattern
        image = np.random.randint(0, 256, (size, size, 3), dtype=np.uint8)
        # Blur gambar untuk mengurangi noise
        image = cv2.GaussianBlur(image, (21, 21), 0)
    
    # Return value dari function
    return image


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama untuk menjalankan semua demonstrasi.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM OPENCV DNN - IMAGE CLASSIFICATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("\n[INFO] OpenCV version:", cv2.__version__)
    print("[INFO] DNN backends available:", 
          hasattr(cv2, 'dnn') and hasattr(cv2.dnn, 'blobFromImage'))
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Basic Classification Demo")
        print("2. Blob Creation & Parameters")
        print("3. Complete Classification Workflow")
        print("4. Inference Backends Info")
        print("5. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-5): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_classification_basic()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_blob_creation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_classification_workflow()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_inference_backends()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_classification_basic()
            demo_blob_creation()
            demo_classification_workflow()
            demo_inference_backends()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
