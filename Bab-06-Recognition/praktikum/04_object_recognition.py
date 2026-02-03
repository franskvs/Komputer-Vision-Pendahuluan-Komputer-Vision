"""
=============================================================================
PRAKTIKUM 04 - OBJECT RECOGNITION DAN CLASSIFICATION
=============================================================================
Program ini mendemonstrasikan Object Recognition dan Image Classification
menggunakan pre-trained CNN models.

Konsep yang dipelajari:
1. Image Classification dengan CNN
2. Multi-label classification
3. Top-K predictions
4. Class Activation Maps (CAM) untuk interpretasi

Object Recognition vs Object Detection:
- Recognition: Mengidentifikasi APA yang ada di gambar (whole image)
- Detection: Mengidentifikasi APA dan DI MANA (bounding boxes)

Kebutuhan:
- opencv-python >= 4.8.0
- numpy
- Pre-trained models (MobileNet, ResNet)

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import os
import urllib.request


def download_imagenet_labels():
    """
    Download ImageNet class labels.
    """
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    labels_path = "imagenet_classes.txt"
    
    if not os.path.exists(labels_path):
        try:
            print("[INFO] Downloading ImageNet labels...")
            urllib.request.urlretrieve(labels_url, labels_path)
            print("[INFO] Download complete!")
        except Exception as e:
            print(f"[WARNING] Failed to download labels: {e}")
            return None
    
    # Load labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    
    return labels


def create_imagenet_labels():
    """
    Membuat subset ImageNet labels untuk demonstrasi.
    """
    # Common ImageNet classes subset
    labels = [
        "tench", "goldfish", "great white shark", "tiger shark", "hammerhead",
        "electric ray", "stingray", "cock", "hen", "ostrich",
        "brambling", "goldfinch", "house finch", "junco", "indigo bunting",
        "robin", "bulbul", "jay", "magpie", "chickadee",
        "water ouzel", "kite", "bald eagle", "vulture", "great grey owl",
        "European fire salamander", "common newt", "eft", "spotted salamander", "axolotl",
        "bullfrog", "tree frog", "tailed frog", "loggerhead", "leatherback turtle",
        "mud turtle", "terrapin", "box turtle", "banded gecko", "common iguana",
        "American chameleon", "whiptail", "agama", "frilled lizard", "alligator lizard",
        "Gila monster", "green lizard", "African chameleon", "Komodo dragon", "African crocodile",
        # ... more classes
        "tabby cat", "tiger cat", "Persian cat", "Siamese cat", "Egyptian cat",
        "cougar", "lynx", "leopard", "snow leopard", "jaguar",
        "lion", "tiger", "cheetah", "brown bear", "American black bear",
        "ice bear", "sloth bear", "mongoose", "meerkat", "tiger beetle",
        # Objects
        "iPod", "laptop", "mouse", "remote control", "keyboard",
        "cellular telephone", "refrigerator", "microwave", "oven", "toaster",
        "washing machine", "vacuum", "electric fan", "coffee maker", "iron",
        "hair dryer", "toilet seat", "desk", "dining table", "wardrobe",
        "bookcase", "china cabinet", "screen", "television", "monitor",
        # Vehicles
        "sports car", "taxi", "jeep", "pickup", "minivan",
        "ambulance", "fire engine", "school bus", "trolleybus", "trailer truck",
        "moving van", "police van", "recreational vehicle", "streetcar", "snowplow",
        "garbage truck", "tractor", "racing car", "limousine", "convertible"
    ]
    
    # Pad to 1000 classes
    while len(labels) < 1000:
        labels.append(f"class_{len(labels)}")
    
    return labels


def softmax(x):
    """
    Compute softmax probabilities.
    """
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()


def demo_image_classification_concept():
    """
    Menampilkan konsep Image Classification.
    """
    print("\n" + "="*70)
    print("KONSEP IMAGE CLASSIFICATION")
    print("="*70)
    
    print("""
    [DEFINISI]
    ─────────────────────────────────────────────────────────────────────
    
    Image Classification: Memprediksi SATU atau LEBIH labels untuk 
    keseluruhan gambar.
    
    Input: Gambar (H × W × C)
    Output: Probability distribution over classes
    
    
    [TYPES OF CLASSIFICATION]
    ─────────────────────────────────────────────────────────────────────
    
    1. Single-label Classification
       - Satu gambar = satu class
       - Output: Softmax probabilities
       - Contoh: "Ini adalah gambar kucing"
    
    2. Multi-label Classification
       - Satu gambar bisa punya multiple labels
       - Output: Sigmoid per class (independent)
       - Contoh: "Gambar ini mengandung: kucing, sofa, jendela"
    
    
    [PIPELINE]
    ─────────────────────────────────────────────────────────────────────
    
    ┌─────────────┐     ┌────────────────┐     ┌───────────────┐
    │   Input     │────→│ Preprocessing  │────→│   CNN Model   │
    │   Image     │     │ (resize, norm) │     │ (backbone +   │
    │ 224×224×3   │     │                │     │  classifier)  │
    └─────────────┘     └────────────────┘     └───────┬───────┘
                                                       │
                                                       ▼
    ┌─────────────┐     ┌────────────────┐     ┌───────────────┐
    │  Top-K      │←────│   Softmax/     │←────│   Logits      │
    │ Predictions │     │   Sigmoid      │     │ (raw scores)  │
    └─────────────┘     └────────────────┘     └───────────────┘
    
    
    [PREPROCESSING FOR CNN]
    ─────────────────────────────────────────────────────────────────────
    
    1. Resize ke input size model (224×224 atau 299×299)
    2. Normalize pixel values:
       - [0, 255] → [0, 1] atau
       - [0, 255] → [-1, 1] atau
       - ImageNet normalization (mean subtraction + std division)
    3. Convert BGR (OpenCV) to RGB (if needed)
    4. Channel first format: (H, W, C) → (C, H, W)
    
    
    [IMAGENET DATASET]
    ─────────────────────────────────────────────────────────────────────
    
    - 1,000 classes
    - ~1.2 million training images
    - Categories: animals, objects, vehicles, food, etc.
    - Benchmark untuk image classification
    
    Examples:
    - n01440764: tench (fish)
    - n02102040: English springer
    - n02979186: cassette player
    """)


def demo_classification_opencv():
    """
    Demonstrasi image classification dengan OpenCV DNN.
    """
    print("\n" + "="*70)
    print("IMAGE CLASSIFICATION DENGAN OPENCV DNN")
    print("="*70)
    
    # Get labels
    labels = download_imagenet_labels()
    if labels is None:
        labels = create_imagenet_labels()
    
    print(f"\n[INFO] Loaded {len(labels)} class labels")
    
    # Create sample image
    print("\n[INFO] Creating sample image for classification...")
    sample_image = create_sample_object_image()
    
    print("\n[STEP 1] Preprocessing")
    print("-"*50)
    
    # Preprocessing parameters for different models
    preprocess_configs = {
        "MobileNet": {
            "size": (224, 224),
            "scale": 1/127.5,
            "mean": (127.5, 127.5, 127.5),
            "swapRB": True
        },
        "ResNet": {
            "size": (224, 224),
            "scale": 1.0,
            "mean": (103.939, 116.779, 123.68),
            "swapRB": False
        },
        "EfficientNet": {
            "size": (224, 224),
            "scale": 1/255.0,
            "mean": (0, 0, 0),
            "swapRB": True
        }
    }
    
    # Demo preprocessing
    config = preprocess_configs["MobileNet"]
    blob = cv2.dnn.blobFromImage(
        sample_image,
        config["scale"],
        config["size"],
        config["mean"],
        config["swapRB"]
    )
    
    print(f"Input image shape: {sample_image.shape}")
    print(f"Blob shape: {blob.shape}")
    print(f"Blob value range: [{blob.min():.3f}, {blob.max():.3f}]")
    
    print("\n[STEP 2] Simulated Inference")
    print("-"*50)
    
    # Simulate network output
    np.random.seed(42)
    logits = np.random.randn(1000)
    
    # Make some classes more likely
    logits[281] += 3  # tabby cat
    logits[285] += 2  # Egyptian cat
    logits[282] += 1.5  # tiger cat
    
    probabilities = softmax(logits)
    
    print("\n[STEP 3] Top-5 Predictions")
    print("-"*50)
    
    top5_idx = np.argsort(probabilities)[::-1][:5]
    
    print("\nPredicted classes:")
    for i, idx in enumerate(top5_idx):
        bar_length = int(probabilities[idx] * 50)
        bar = "█" * bar_length
        print(f"  {i+1}. {labels[idx]:30s} {probabilities[idx]:.4f} {bar}")
    
    # Visualize
    display = sample_image.copy()
    
    y_offset = 30
    cv2.putText(display, "Classification Results:", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    for i, idx in enumerate(top5_idx[:3]):
        y_offset += 30
        text = f"{i+1}. {labels[idx]}: {probabilities[idx]:.2%}"
        cv2.putText(display, text, (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow("Image Classification", display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_sample_object_image():
    """
    Membuat sample image yang menyerupai objek untuk klasifikasi.
    """
    image = np.ones((300, 300, 3), dtype=np.uint8) * 200
    
    # Background gradient
    for y in range(300):
        for x in range(300):
            image[y, x] = [180 + y//5, 200 - x//10, 220 - y//10]
    
    # Draw cat-like shape
    # Body
    cv2.ellipse(image, (150, 180), (60, 50), 0, 0, 360, (150, 130, 100), -1)
    
    # Head
    cv2.ellipse(image, (150, 100), (50, 45), 0, 0, 360, (160, 140, 110), -1)
    
    # Ears
    pts_ear1 = np.array([[100, 70], [115, 40], [130, 70]], np.int32)
    pts_ear2 = np.array([[170, 70], [185, 40], [200, 70]], np.int32)
    cv2.fillPoly(image, [pts_ear1], (160, 140, 110))
    cv2.fillPoly(image, [pts_ear2], (160, 140, 110))
    
    # Inner ears
    pts_inner1 = np.array([[108, 68], [115, 50], [122, 68]], np.int32)
    pts_inner2 = np.array([[178, 68], [185, 50], [192, 68]], np.int32)
    cv2.fillPoly(image, [pts_inner1], (200, 150, 150))
    cv2.fillPoly(image, [pts_inner2], (200, 150, 150))
    
    # Eyes
    cv2.ellipse(image, (130, 95), (12, 15), 0, 0, 360, (80, 180, 80), -1)
    cv2.ellipse(image, (170, 95), (12, 15), 0, 0, 360, (80, 180, 80), -1)
    cv2.ellipse(image, (130, 95), (5, 10), 0, 0, 360, (0, 0, 0), -1)
    cv2.ellipse(image, (170, 95), (5, 10), 0, 0, 360, (0, 0, 0), -1)
    
    # Nose
    pts_nose = np.array([[150, 110], [143, 120], [157, 120]], np.int32)
    cv2.fillPoly(image, [pts_nose], (200, 150, 150))
    
    # Whiskers
    cv2.line(image, (100, 115), (135, 110), (80, 80, 80), 1)
    cv2.line(image, (100, 125), (135, 120), (80, 80, 80), 1)
    cv2.line(image, (200, 115), (165, 110), (80, 80, 80), 1)
    cv2.line(image, (200, 125), (165, 120), (80, 80, 80), 1)
    
    # Tail
    pts_tail = np.array([[200, 200], [250, 180], [260, 150], [255, 170], [210, 195]], np.int32)
    cv2.polylines(image, [pts_tail], False, (150, 130, 100), 15)
    
    return image


def demo_topk_analysis():
    """
    Demonstrasi analisis Top-K predictions.
    """
    print("\n" + "="*70)
    print("TOP-K PREDICTION ANALYSIS")
    print("="*70)
    
    print("""
    [TOP-K PREDICTIONS]
    ─────────────────────────────────────────────────────────────────────
    
    K=1 (Top-1): Apakah prediksi pertama benar?
        → Metrics: Top-1 Accuracy
    
    K=5 (Top-5): Apakah label benar ada di 5 prediksi teratas?
        → Metrics: Top-5 Accuracy
        → Standard untuk ImageNet benchmark
    
    K=10: Untuk analisis lebih lanjut atau multi-label hints
    
    
    [CONFIDENCE ANALYSIS]
    ─────────────────────────────────────────────────────────────────────
    """)
    
    # Simulate different confidence scenarios
    scenarios = [
        {
            "name": "High Confidence",
            "probs": [0.95, 0.02, 0.01, 0.01, 0.01],
            "labels": ["cat", "dog", "tiger", "lion", "leopard"]
        },
        {
            "name": "Medium Confidence",
            "probs": [0.45, 0.30, 0.15, 0.07, 0.03],
            "labels": ["cat", "tiger cat", "tabby", "Persian cat", "dog"]
        },
        {
            "name": "Low Confidence (Ambiguous)",
            "probs": [0.25, 0.22, 0.20, 0.18, 0.15],
            "labels": ["cat", "dog", "rabbit", "hamster", "guinea pig"]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print("-"*50)
        
        for label, prob in zip(scenario['labels'], scenario['probs']):
            bar = "█" * int(prob * 40)
            print(f"  {label:15s} {prob:.2%} {bar}")
        
        # Analysis
        top1_conf = scenario['probs'][0]
        if top1_conf > 0.8:
            analysis = "✓ Very confident - trust the prediction"
        elif top1_conf > 0.5:
            analysis = "~ Moderately confident - consider alternatives"
        else:
            analysis = "✗ Low confidence - multiple possibilities"
        
        print(f"\n  Analysis: {analysis}")


def demo_class_activation_map():
    """
    Demonstrasi Class Activation Map (CAM) untuk interpretasi.
    """
    print("\n" + "="*70)
    print("CLASS ACTIVATION MAP (CAM)")
    print("="*70)
    
    print("""
    [KONSEP CAM]
    ─────────────────────────────────────────────────────────────────────
    
    CAM menunjukkan REGION mana dalam gambar yang "responsible" untuk 
    prediksi tertentu.
    
    Workflow:
    1. Extract feature maps dari layer konvolusi terakhir
    2. Global Average Pooling → menghasilkan weights per channel
    3. Weighted sum of feature maps → activation map
    4. Overlay pada gambar original
    
    
    [FORMULA]
    ─────────────────────────────────────────────────────────────────────
    
    CAM = Σ(wk × fk)
    
    dimana:
    - wk: weight untuk class c pada channel k
    - fk: feature map channel k
    
    
    [VARIASI CAM]
    ─────────────────────────────────────────────────────────────────────
    
    1. CAM (original)
       - Memerlukan Global Average Pooling layer
       - Simple weighted sum
    
    2. Grad-CAM
       - Works dengan any CNN architecture
       - Menggunakan gradients sebagai weights
       - Gradient of class score w.r.t. feature maps
    
    3. Grad-CAM++
       - Improved version
       - Better untuk multiple instances
    
    4. Score-CAM
       - Gradient-free
       - More stable
    """)
    
    # Simulate CAM visualization
    print("\n[SIMULASI] CAM Visualization")
    print("-"*50)
    
    # Create sample image
    image = create_sample_object_image()
    
    # Simulate CAM (highlight center where "object" is)
    h, w = image.shape[:2]
    cam = np.zeros((h, w), dtype=np.float32)
    
    # Create Gaussian-like activation centered on object
    y_indices, x_indices = np.ogrid[:h, :w]
    center_y, center_x = 130, 150  # Center of the "cat"
    
    # Distance from center
    dist = np.sqrt((y_indices - center_y)**2 + (x_indices - center_x)**2)
    cam = np.exp(-dist**2 / (2 * 60**2))  # Gaussian
    
    # Normalize to [0, 255]
    cam_normalized = ((cam - cam.min()) / (cam.max() - cam.min()) * 255).astype(np.uint8)
    
    # Apply colormap
    cam_colored = cv2.applyColorMap(cam_normalized, cv2.COLORMAP_JET)
    
    # Overlay on original image
    alpha = 0.5
    overlay = cv2.addWeighted(image, 1-alpha, cam_colored, alpha, 0)
    
    # Add labels
    cv2.putText(overlay, "Class Activation Map (CAM)", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(overlay, "Predicted: Cat (95%)", (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Create display
    display = np.hstack([image, cam_colored, overlay])
    
    # Add labels at top
    label_bar = np.zeros((40, display.shape[1], 3), dtype=np.uint8)
    cv2.putText(label_bar, "Original", (50, 28), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(label_bar, "CAM Heatmap", (350, 28), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(label_bar, "Overlay", (680, 28), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    final_display = np.vstack([label_bar, display])
    
    cv2.imshow("Class Activation Map Demo", final_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n[INFO] CAM menunjukkan bahwa model fokus pada area wajah kucing")
    print("[INFO] Region merah = high activation = paling berpengaruh pada prediksi")


def demo_multilabel_classification():
    """
    Demonstrasi multi-label classification.
    """
    print("\n" + "="*70)
    print("MULTI-LABEL CLASSIFICATION")
    print("="*70)
    
    print("""
    [PERBEDAAN SINGLE vs MULTI-LABEL]
    ─────────────────────────────────────────────────────────────────────
    
    Single-Label:
    - Output: Softmax → satu label dengan probabilitas tertinggi
    - Sum of probabilities = 1
    - Contoh: "Ini adalah kucing"
    
    Multi-Label:
    - Output: Sigmoid per class → multiple labels bisa aktif
    - Each class independent (0-1)
    - Contoh: "Gambar mengandung: kucing, sofa, televisi"
    
    
    [CONTOH OUTPUT]
    ─────────────────────────────────────────────────────────────────────
    
    Single-Label (Softmax):
    ┌────────────┬─────────┐
    │ Class      │ Prob    │
    ├────────────┼─────────┤
    │ Cat        │ 0.75    │
    │ Dog        │ 0.15    │
    │ Sofa       │ 0.05    │
    │ TV         │ 0.05    │
    └────────────┴─────────┘
    Sum = 1.0
    Prediction: Cat
    
    Multi-Label (Sigmoid):
    ┌────────────┬─────────┬───────────┐
    │ Class      │ Prob    │ Active?   │
    ├────────────┼─────────┼───────────┤
    │ Cat        │ 0.92    │ YES (>0.5)│
    │ Dog        │ 0.08    │ NO        │
    │ Sofa       │ 0.87    │ YES (>0.5)│
    │ TV         │ 0.73    │ YES (>0.5)│
    └────────────┴─────────┴───────────┘
    Predictions: Cat, Sofa, TV
    """)
    
    # Demo multi-label scenario
    print("\n[SIMULASI] Multi-label classification")
    print("-"*50)
    
    # Simulated scene dengan multiple objects
    labels = ["person", "cat", "dog", "sofa", "chair", "tv", "laptop", 
              "book", "plant", "window"]
    
    # Sigmoid probabilities (independent)
    np.random.seed(123)
    probs = np.array([0.95, 0.88, 0.12, 0.92, 0.35, 0.78, 0.45, 
                      0.15, 0.67, 0.55])
    
    threshold = 0.5
    
    print(f"\nPredictions (threshold={threshold}):")
    print("-"*40)
    
    detected = []
    for label, prob in zip(labels, probs):
        status = "✓" if prob >= threshold else " "
        bar = "█" * int(prob * 30)
        print(f"  [{status}] {label:10s} {prob:.2f} {bar}")
        if prob >= threshold:
            detected.append(label)
    
    print(f"\nDetected objects: {', '.join(detected)}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM OBJECT RECOGNITION & CLASSIFICATION")
    print("="*70)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Konsep Image Classification")
        print("2. Classification dengan OpenCV DNN")
        print("3. Top-K Prediction Analysis")
        print("4. Class Activation Map (CAM)")
        print("5. Multi-label Classification")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-6): ").strip()
        
        if choice == '1':
            demo_image_classification_concept()
        elif choice == '2':
            demo_classification_opencv()
        elif choice == '3':
            demo_topk_analysis()
        elif choice == '4':
            demo_class_activation_map()
        elif choice == '5':
            demo_multilabel_classification()
        elif choice == '6':
            demo_image_classification_concept()
            demo_classification_opencv()
            demo_topk_analysis()
            demo_class_activation_map()
            demo_multilabel_classification()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
