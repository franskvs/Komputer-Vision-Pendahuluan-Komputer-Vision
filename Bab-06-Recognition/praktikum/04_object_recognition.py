"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 04: Object Recognition (MobileNet-SSD via OpenCV DNN)

Tujuan:
1) Melakukan pengenalan objek (recognition) dengan bounding box.
2) Menyimpan hasil dan menampilkan output auto-close 2 detik.
"""

# Import OpenCV untuk operasi DNN.
import cv2
# Import NumPy untuk pembuatan citra sintetis.
import numpy as np
# Import Path untuk penanganan path file.
from pathlib import Path
# Import urllib untuk mengunduh model.
import urllib.request
# Import time untuk pengukuran waktu.
import time


def create_output_dir():
    """Buat folder output hasil object recognition."""
    # Tentukan folder output.
    output_dir = Path("output_object_recognition")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path output.
    return output_dir


def download_mobilenet_ssd():
    """Unduh model MobileNet-SSD Caffe jika belum tersedia."""
    # Tentukan folder model.
    models_dir = Path("models")
    # Buat folder jika belum ada.
    models_dir.mkdir(parents=True, exist_ok=True)
    # Tentukan file prototxt.
    prototxt = models_dir / "MobileNetSSD_deploy.prototxt"
    # Tentukan file caffemodel.
    caffemodel = models_dir / "MobileNetSSD_deploy.caffemodel"
    # Unduh prototxt jika belum ada.
    if not prototxt.exists():
        # Unduh prototxt dari repository OpenCV.
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt",
            prototxt,
        )
    # Unduh caffemodel jika belum ada.
    if not caffemodel.exists():
        # Unduh caffemodel dari repository OpenCV.
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.caffemodel",
            caffemodel,
        )
    # Kembalikan path model.
    return prototxt, caffemodel


def get_labels():
    """Daftar label COCO kecil untuk MobileNet-SSD."""
    # Daftar label bawaan MobileNet-SSD (21 kelas).
    return [
        "background",
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "pottedplant",
        "sheep",
        "sofa",
        "train",
        "tvmonitor",
    ]


def load_sample_image():
    """Muat gambar dari folder data atau buat gambar sintetis."""
    # Cari file pada folder data.
    candidates = list(Path("data").glob("*.jpg")) + list(Path("data").glob("*.png"))
    # Jika ada gambar, gunakan gambar pertama.
    if candidates:
        # Baca gambar dari disk.
        return cv2.imread(str(candidates[0]))
    # Buat kanvas putih.
    image = np.ones((420, 640, 3), dtype=np.uint8) * 230
    # Gambar objek sintetis (orang dan mobil sederhana).
    cv2.rectangle(image, (70, 180), (140, 360), (80, 120, 200), -1)
    # Gambar kepala orang sintetis.
    cv2.circle(image, (105, 150), 30, (200, 170, 140), -1)
    # Gambar mobil sintetis.
    cv2.rectangle(image, (260, 250), (520, 330), (50, 50, 180), -1)
    # Gambar roda mobil.
    cv2.circle(image, (300, 335), 20, (20, 20, 20), -1)
    # Gambar roda mobil.
    cv2.circle(image, (480, 335), 20, (20, 20, 20), -1)
    # Tambahkan label.
    cv2.putText(image, "Synthetic Objects", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
    # Kembalikan gambar sintetis.
    return image


def detect_objects(image, prototxt, caffemodel, conf_threshold=0.4):
    """Deteksi objek dengan MobileNet-SSD."""
    # Muat model DNN.
    net = cv2.dnn.readNetFromCaffe(str(prototxt), str(caffemodel))
    # Ambil ukuran gambar.
    h, w = image.shape[:2]
    # Buat blob dari gambar.
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    # Set input ke jaringan.
    net.setInput(blob)
    # Catat waktu sebelum inferensi.
    start = time.time()
    # Jalankan forward pass.
    detections = net.forward()
    # Hitung waktu inferensi.
    elapsed = time.time() - start
    # Siapkan list hasil.
    results = []
    # Loop hasil deteksi.
    for i in range(detections.shape[2]):
        # Ambil confidence.
        confidence = float(detections[0, 0, i, 2])
        # Filter berdasarkan threshold.
        if confidence >= conf_threshold:
            # Ambil class id.
            class_id = int(detections[0, 0, i, 1])
            # Ambil koordinat bounding box.
            x1 = int(detections[0, 0, i, 3] * w)
            # Ambil y1.
            y1 = int(detections[0, 0, i, 4] * h)
            # Ambil x2.
            x2 = int(detections[0, 0, i, 5] * w)
            # Ambil y2.
            y2 = int(detections[0, 0, i, 6] * h)
            # Simpan hasil.
            results.append((class_id, confidence, x1, y1, x2, y2))
    # Kembalikan hasil dan waktu.
    return results, elapsed


def draw_results(image, results, labels):
    """Gambar bounding box dan label pada gambar."""
    # Salin gambar agar original aman.
    output = image.copy()
    # Loop setiap hasil deteksi.
    for class_id, confidence, x1, y1, x2, y2 in results:
        # Tentukan label kelas.
        label = labels[class_id] if class_id < len(labels) else "object"
        # Gambar bounding box.
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Buat teks label.
        text = f"{label}: {confidence:.2f}"
        # Tulis teks label.
        cv2.putText(output, text, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    # Kembalikan gambar hasil.
    return output


def show_image(title, image, delay_ms=2000):
    """Tampilkan gambar dengan auto-close."""
    # Coba tampilkan jendela jika GUI tersedia.
    try:
        # Tampilkan gambar.
        cv2.imshow(title, image)
        # Tunggu beberapa milidetik.
        cv2.waitKey(delay_ms)
        # Tutup jendela.
        cv2.destroyAllWindows()
    except Exception:
        # Abaikan jika display tidak tersedia.
        pass


def main():
    """Fungsi utama untuk demo object recognition."""
    # Unduh model jika belum ada.
    prototxt, caffemodel = download_mobilenet_ssd()
    # Muat gambar sampel.
    image = load_sample_image()
    # Ambil label kelas.
    labels = get_labels()
    # Jalankan deteksi objek.
    results, elapsed = detect_objects(image, prototxt, caffemodel)
    # Gambar hasil deteksi.
    output = draw_results(image, results, labels)
    # Buat folder output.
    output_dir = create_output_dir()
    # Simpan hasil ke file.
    cv2.imwrite(str(output_dir / "04_object_recognition.jpg"), output)
    # Cetak ringkasan hasil.
    print(f"Detected objects: {len(results)} | Time: {elapsed*1000:.2f} ms")
    # Tampilkan hasil dengan auto-close.
    show_image("Object Recognition", output)


# Jalankan program saat dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
    
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
