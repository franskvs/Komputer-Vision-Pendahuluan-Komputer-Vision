"""
# Assignment - set nilai ke variabel
=============================================================================
# Load YOLOv8 model untuk object detection
PRAKTIKUM 07 - OBJECT DETECTION DENGAN YOLO
# Assignment - set nilai ke variabel
=============================================================================
# Load YOLOv8 model untuk object detection
Program ini mendemonstrasikan penggunaan YOLOv8 untuk object detection.
# Load YOLOv8 model untuk object detection
YOLO (You Only Look Once) adalah algoritma real-time object detection
yang mendeteksi objek dalam satu forward pass melalui network.

Konsep yang dipelajari:
# Load YOLOv8 model untuk object detection
1. Arsitektur YOLO
# Load YOLOv8 model untuk object detection
2. Loading dan inference dengan YOLOv8
3. Detection pada gambar dan video
4. Visualisasi bounding boxes
5. Post-processing (NMS, confidence filtering)

Kebutuhan:
- ultralytics (pip install ultralytics)
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy

Note: Jika ultralytics tidak tersedia, program akan menjalankan simulasi.

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
import time

# Check apakah ultralytics tersedia
YOLO_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Load YOLOv8 model untuk object detection
    from ultralytics import YOLO
    # Load YOLOv8 model untuk object detection
    YOLO_AVAILABLE = True
    # Load YOLOv8 model untuk object detection
    print("[INFO] Ultralytics YOLO tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] Ultralytics tidak tersedia - menggunakan simulasi")


# COCO class names (80 classes)
COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
    'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]


# Definisi function dengan nama dan parameter
def create_sample_scene():
    """
    Membuat sample scene untuk demonstrasi object detection.
    
    Returns:
        numpy array: BGR image dengan beberapa objek
    """
    # Create scene
    scene = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Background gradient
    for y in range(480):
        # Assignment - set nilai ke variabel
        scene[y, :] = scene[y, :] * (1 - y/1000)
    
    # Add "objects" untuk simulasi deteksi
    # Person (rectangle)
    cv2.rectangle(scene, (100, 150), (180, 400), (50, 100, 150), -1)
    # Gambar lingkaran pada gambar
    cv2.circle(scene, (140, 120), 30, (180, 150, 130), -1)  # Head
    
    # Car (rectangle)
    cv2.rectangle(scene, (350, 280), (550, 380), (100, 100, 200), -1)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(scene, (380, 260), (520, 290), (80, 80, 180), -1)  # Top
    # Gambar lingkaran pada gambar
    cv2.circle(scene, (390, 380), 25, (50, 50, 50), -1)  # Wheel
    # Gambar lingkaran pada gambar
    cv2.circle(scene, (510, 380), 25, (50, 50, 50), -1)  # Wheel
    
    # Dog (ellipse)
    cv2.ellipse(scene, (280, 380), (40, 25), 0, 0, 360, (139, 90, 43), -1)
    # Gambar lingkaran pada gambar
    cv2.circle(scene, (310, 370), 15, (139, 90, 43), -1)  # Head
    
    # Add text
    # cv2.putText(a, b, c, d, e, f, g): a=scene, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(scene, "Sample Scene for Detection", (150, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
    
    # Return value dari function
    return scene


# Definisi function dengan nama dan parameter
def generate_random_color(seed):
    """
    Generate warna konsisten untuk setiap class.
    
    Args:
        # Definisi class untuk membuat object
        seed: Seed untuk random (biasanya class ID)
        
    Returns:
        tuple: BGR color
    """
    np.random.seed(seed)
    # Generate random integer dalam range tertentu
    return tuple(map(int, np.random.randint(0, 255, 3)))


# Definisi function dengan nama dan parameter
def draw_detection(image, box, class_id, confidence, class_names=COCO_CLASSES):
    """
    Menggambar bounding box dan label pada gambar.
    
    Args:
        image: BGR image
        box: Bounding box [x1, y1, x2, y2]
        class_id: Class ID
        confidence: Confidence score
        # Definisi class untuk membuat object
        class_names: List of class names
    """
    # Assignment - set nilai ke variabel
    x1, y1, x2, y2 = map(int, box)
    
    # Get color
    color = generate_random_color(class_id)
    
    # Draw box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    
    # Prepare label
    class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
    # Assignment - set nilai ke variabel
    label = f"{class_name}: {confidence:.2f}"
    
    # Draw label background
    (label_w, label_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(image, (x1, y1 - label_h - 10), (x1 + label_w + 10, y1), color, -1)
    
    # Draw label text
    # cv2.putText(a, b, c, d, e, f, g): a=image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(image, label, (x1 + 5, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


# Definisi function dengan nama dan parameter
def non_max_suppression(boxes, scores, iou_threshold=0.5):
    """
    Non-Maximum Suppression untuk menghilangkan overlapping detections.
    
    Args:
        boxes: Array of bounding boxes [[x1,y1,x2,y2], ...]
        scores: Array of confidence scores
        iou_threshold: IoU threshold untuk suppression
        
    Returns:
        list: Indices of kept boxes
    """
    # Conditional statement - eksekusi jika kondisi True
    if len(boxes) == 0:
        # Return value dari function
        return []
    
    # Buat array numpy dari list/data
    boxes = np.array(boxes)
    # Buat array numpy dari list/data
    scores = np.array(scores)
    
    # Sort by score
    indices = np.argsort(scores)[::-1]
    
    # Assignment - set nilai ke variabel
    keep = []
    
    # Loop berulang selama kondisi bernilai True
    while len(indices) > 0:
        # Keep the highest score
        current = indices[0]
        keep.append(current)
        
        # Conditional statement - eksekusi jika kondisi True
        if len(indices) == 1:
            break
        
        # Calculate IoU with remaining boxes
        current_box = boxes[current]
        # Assignment - set nilai ke variabel
        remaining_boxes = boxes[indices[1:]]
        
        # Calculate intersection
        x1 = np.maximum(current_box[0], remaining_boxes[:, 0])
        # Assignment - set nilai ke variabel
        y1 = np.maximum(current_box[1], remaining_boxes[:, 1])
        # Assignment - set nilai ke variabel
        x2 = np.minimum(current_box[2], remaining_boxes[:, 2])
        # Assignment - set nilai ke variabel
        y2 = np.minimum(current_box[3], remaining_boxes[:, 3])
        
        # Assignment - set nilai ke variabel
        intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        
        # Calculate union
        current_area = (current_box[2] - current_box[0]) * (current_box[3] - current_box[1])
        # Assignment - set nilai ke variabel
        remaining_areas = (remaining_boxes[:, 2] - remaining_boxes[:, 0]) * \
                         (remaining_boxes[:, 3] - remaining_boxes[:, 1])
        # Assignment - set nilai ke variabel
        union = current_area + remaining_areas - intersection
        
        # Calculate IoU
        iou = intersection / (union + 1e-6)
        
        # Keep boxes with IoU below threshold
        mask = iou <= iou_threshold
        # Assignment - set nilai ke variabel
        indices = indices[1:][mask]
    
    # Return value dari function
    return keep


# Definisi function dengan nama dan parameter
def demo_yolo_architecture():
    """
    # Load YOLOv8 model untuk object detection
    Menjelaskan arsitektur YOLO.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    # Load YOLOv8 model untuk object detection
    print("ARSITEKTUR YOLO (You Only Look Once)")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    # Load YOLOv8 model untuk object detection
    [YOLO ARCHITECTURE]
    ─────────────────────────────────────────────────────────────────────
    
    Input Image (640×640×3)
           │
           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                         BACKBONE                                 │
    │  (Feature Extraction - CSPDarknet/EfficientNet)                 │
    │                                                                  │
    │  Conv → BatchNorm → SiLU → Conv → ... → Feature Maps           │
    │                                                                  │
    │  Output: Multi-scale feature maps                               │
    │  - P3: 80×80 (small objects)                                    │
    │  - P4: 40×40 (medium objects)                                   │
    │  - P5: 20×20 (large objects)                                    │
    └─────────────────────────────────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                           NECK                                   │
    │  (Feature Pyramid Network + Path Aggregation Network)           │
    │                                                                  │
    │  FPN: Top-down pathway (semantic information)                   │
    │  PAN: Bottom-up pathway (localization information)              │
    │                                                                  │
    │  Aggregates features dari multiple scales                       │
    └─────────────────────────────────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                          HEAD                                    │
    # Load YOLOv8 model untuk object detection
    │  (Detection Head - Anchor-free in YOLOv8)                       │
    │                                                                  │
    │  Per grid cell, prediksi:                                       │
    │  ┌─────────────────────────────────────────────┐                │
    │  │ • Box coordinates (x, y, w, h)              │                │
    │  │ • Objectness score                          │                │
    │  │ • Class probabilities (80 classes COCO)    │                │
    │  └─────────────────────────────────────────────┘                │
    └─────────────────────────────────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                     POST-PROCESSING                              │
    │                                                                  │
    │  1. Filter by confidence threshold (e.g., > 0.5)                │
    │  2. Non-Maximum Suppression (NMS)                               │
    │  3. Output final detections                                      │
    └─────────────────────────────────────────────────────────────────┘
    
    
    # Load YOLOv8 model untuk object detection
    [YOLOv8 VARIANTS]
    ─────────────────────────────────────────────────────────────────────
    
    Model       | Params | Size   | mAP@0.5 | Speed (ms) | Use Case
    ────────────|────────|────────|─────────|────────────|──────────────
    # Load YOLOv8 model untuk object detection
    YOLOv8n     | 3.2M   | 6.3MB  | 37.3%   | 0.99       | Edge/Mobile
    # Load YOLOv8 model untuk object detection
    YOLOv8s     | 11.2M  | 22.5MB | 44.9%   | 1.20       | Balanced
    # Load YOLOv8 model untuk object detection
    YOLOv8m     | 25.9M  | 52.0MB | 50.2%   | 1.83       | Accuracy
    # Load YOLOv8 model untuk object detection
    YOLOv8l     | 43.7M  | 87.7MB | 52.9%   | 2.39       | High accuracy
    # Load YOLOv8 model untuk object detection
    YOLOv8x     | 68.2M  | 137MB  | 53.9%   | 3.53       | Best accuracy
    
    * Speed measured on NVIDIA T4 GPU with TensorRT
    """)


# Definisi function dengan nama dan parameter
def demo_yolo_inference():
    """
    # Load YOLOv8 model untuk object detection
    Demonstrasi inference YOLO pada gambar.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    # Load YOLOv8 model untuk object detection
    print("YOLO INFERENCE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE:
        # Load YOLOv8 model untuk object detection
        print("\n[INFO] Loading YOLOv8n model...")
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n.pt')  # Auto-download jika belum ada
        
        # Create test image
        image = create_sample_scene()
        
        print("[INFO] Running inference...")
        # Assignment - set nilai ke variabel
        results = model(image, verbose=False)
        
        # Process results
        for result in results:
            # Assignment - set nilai ke variabel
            boxes = result.boxes
            
            print(f"\n[INFO] Detected {len(boxes)} objects:")
            
            # Iterasi/loop melalui elemen dalam koleksi
            for box in boxes:
                # Assignment - set nilai ke variabel
                cls = int(box.cls[0])
                # Assignment - set nilai ke variabel
                conf = float(box.conf[0])
                # Assignment - set nilai ke variabel
                xyxy = box.xyxy[0].cpu().numpy()
                
                # Assignment - set nilai ke variabel
                class_name = model.names[cls]
                print(f"  - {class_name}: {conf:.2f} at [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")
                
                # Draw on image
                draw_detection(image, xyxy, cls, conf, list(model.names.values()))
        
        # Tampilkan gambar di window
        cv2.imshow("YOLO Detection Results", image)
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
        
    else:
        # Simulasi deteksi
        print("\n[SIMULATION MODE] Simulating YOLO detection...")
        
        # Assignment - set nilai ke variabel
        image = create_sample_scene()
        
        # Simulated detections
        detections = [
            {'class_id': 0, 'class_name': 'person', 'confidence': 0.92, 
             'box': [90, 90, 190, 410]},
            {'class_id': 2, 'class_name': 'car', 'confidence': 0.87, 
             'box': [340, 250, 560, 390]},
            {'class_id': 16, 'class_name': 'dog', 'confidence': 0.78, 
             'box': [230, 345, 340, 420]},
        ]
        
        print(f"\n[INFO] Detected {len(detections)} objects:")
        
        # Iterasi/loop melalui elemen dalam koleksi
        for det in detections:
            print(f"  - {det['class_name']}: {det['confidence']:.2f} "
                  f"at {det['box']}")
            draw_detection(image, det['box'], det['class_id'], det['confidence'])
        
        # Tampilkan gambar di window
        cv2.imshow("YOLO Detection Results (Simulated)", image)
        print("\n[INFO] Tekan 'q' untuk menutup gambar...")
        # Loop berulang selama kondisi bernilai True
        while True:
            # Tunggu input keyboard (1ms per iterasi)
            key = cv2.waitKey(1) & 0xFF
            # Conditional statement - eksekusi jika kondisi True
            if key == ord('q') or key == 27:
                break
        # Tutup semua window
        cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_yolo_video():
    """
    # Load YOLOv8 model untuk object detection
    Demonstrasi YOLO pada video/webcam.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    # Load YOLOv8 model untuk object detection
    print("YOLO VIDEO DETECTION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    # Conditional statement - eksekusi jika kondisi True
    if not cap.isOpened():
        print("[WARNING] Webcam tidak tersedia, menggunakan synthetic video...")
        # Assignment - set nilai ke variabel
        cap = None
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE and cap is not None:
        # Load YOLOv8 model untuk object detection
        print("\n[INFO] Loading YOLOv8n model...")
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n.pt')
        
        print("[INFO] Starting webcam detection. Press 'q' to quit.")
        
        # Assignment - set nilai ke variabel
        fps_list = []
        
        # Loop berulang selama kondisi bernilai True
        while True:
            # Assignment - set nilai ke variabel
            ret, frame = cap.read()
            # Conditional statement - eksekusi jika kondisi True
            if not ret:
                break
            
            # Assignment - set nilai ke variabel
            start_time = time.time()
            
            # Run inference
            results = model(frame, verbose=False)
            
            # Draw results
            for result in results:
                # Assignment - set nilai ke variabel
                boxes = result.boxes
                # Iterasi/loop melalui elemen dalam koleksi
                for box in boxes:
                    # Assignment - set nilai ke variabel
                    cls = int(box.cls[0])
                    # Assignment - set nilai ke variabel
                    conf = float(box.conf[0])
                    # Assignment - set nilai ke variabel
                    xyxy = box.xyxy[0].cpu().numpy()
                    draw_detection(frame, xyxy, cls, conf, list(model.names.values()))
            
            # Calculate FPS
            inference_time = time.time() - start_time
            # Assignment - set nilai ke variabel
            fps = 1.0 / inference_time
            fps_list.append(fps)
            
            # Display FPS
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Tampilkan gambar di window
            cv2.imshow("YOLO Real-time Detection", frame)
            
            # Tunggu input keyboard (1ms per iterasi)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        # Tutup semua window
        cv2.destroyAllWindows()
        
        # Hitung rata-rata dari array
        avg_fps = np.mean(fps_list) if fps_list else 0
        print(f"\n[INFO] Average FPS: {avg_fps:.1f}")
        
    else:
        # Simulasi dengan synthetic frames
        print("\n[SIMULATION MODE] Generating synthetic video detection...")
        
        # Assignment - set nilai ke variabel
        frame_count = 50
        
        # Iterasi/loop melalui elemen dalam koleksi
        for i in range(frame_count):
            # Generate synthetic frame
            frame = create_sample_scene()
            
            # Add some variation
            noise = np.random.randint(-10, 10, frame.shape, dtype=np.int16)
            # Batasi nilai array antara min dan max
            frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            # Simulated detections (with slight movement)
            offset = int(5 * np.sin(i / 5))
            # Assignment - set nilai ke variabel
            detections = [
                {'box': [90+offset, 90, 190+offset, 410], 'class_id': 0, 'conf': 0.9},
                {'box': [340, 250-offset, 560, 390-offset], 'class_id': 2, 'conf': 0.85},
            ]
            
            # Iterasi/loop melalui elemen dalam koleksi
            for det in detections:
                draw_detection(frame, det['box'], det['class_id'], det['conf'])
            
            # Display FPS (simulated)
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"FPS: 30.0 (simulated)", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"Frame: {i+1}/{frame_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Tampilkan gambar di window
            cv2.imshow("YOLO Video (Simulated)", frame)
            
            # Tunggu input keyboard (1ms per iterasi)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
        
        # Tutup semua window
        cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_nms():
    """
    Demonstrasi Non-Maximum Suppression.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("NON-MAXIMUM SUPPRESSION (NMS)")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [KONSEP NMS]
    ─────────────────────────────────────────────────────────────────────
    
    Masalah: Neural network sering menghasilkan multiple overlapping
             detections untuk objek yang sama.
    
    Solusi:  Non-Maximum Suppression memfilter deteksi berdasarkan
             IoU (Intersection over Union) dan confidence score.
    
    Algoritma:
    1. Sort detections by confidence (descending)
    2. Pilih detection dengan confidence tertinggi
    3. Hapus semua detection dengan IoU > threshold terhadap yang dipilih
    4. Ulangi sampai tidak ada detection tersisa
    """)
    
    # Create visualization
    image = np.ones((400, 600, 3), dtype=np.uint8) * 240
    
    # Draw object
    cv2.rectangle(image, (200, 100), (400, 300), (100, 100, 100), -1)
    # cv2.putText(a, b, c, d, e, f, g): a=image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(image, "Object", (260, 210), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 255, 255), 2)
    
    # Overlapping detections
    detections = [
        ([195, 95, 405, 305], 0.95),   # Best match
        ([190, 90, 400, 300], 0.88),   # Overlapping
        ([200, 100, 410, 310], 0.82),  # Overlapping
        ([205, 105, 395, 295], 0.75),  # Overlapping
    ]
    
    # Draw before NMS
    before_image = image.copy()
    # Iterasi/loop melalui elemen dalam koleksi
    for box, conf in detections:
        # Assignment - set nilai ke variabel
        color = (0, int(255 * conf), 0)
        # Gambar persegi panjang pada gambar
        cv2.rectangle(before_image, (box[0], box[1]), (box[2], box[3]), color, 2)
        # cv2.putText(a, b, c, d, e, f, g): a=before_image, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(before_image, f"{conf:.2f}", (box[0], box[1]-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # cv2.putText(a, b, c, d, e, f, g): a=before_image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(before_image, "Before NMS", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    # cv2.putText(a, b, c, d, e, f, g): a=before_image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(before_image, f"Detections: {len(detections)}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Apply NMS
    boxes = [d[0] for d in detections]
    # Iterasi/loop melalui elemen dalam koleksi
    scores = [d[1] for d in detections]
    # Assignment - set nilai ke variabel
    keep_indices = non_max_suppression(boxes, scores, iou_threshold=0.5)
    
    # Draw after NMS
    after_image = image.copy()
    # Iterasi/loop melalui elemen dalam koleksi
    for idx in keep_indices:
        # Assignment - set nilai ke variabel
        box, conf = detections[idx]
        # Assignment - set nilai ke variabel
        color = (0, int(255 * conf), 0)
        # Gambar persegi panjang pada gambar
        cv2.rectangle(after_image, (box[0], box[1]), (box[2], box[3]), color, 2)
        # cv2.putText(a, b, c, d, e, f, g): a=after_image, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(after_image, f"{conf:.2f}", (box[0], box[1]-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # cv2.putText(a, b, c, d, e, f, g): a=after_image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(after_image, "After NMS", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    # cv2.putText(a, b, c, d, e, f, g): a=after_image, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(after_image, f"Detections: {len(keep_indices)}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Combine
    combined = np.hstack([before_image, after_image])
    
    # Tampilkan gambar di window
    cv2.imshow("Non-Maximum Suppression", combined)
    
    print(f"\n[INFO] Detections before NMS: {len(detections)}")
    print(f"[INFO] Detections after NMS: {len(keep_indices)}")
    print(f"[INFO] IoU threshold: 0.5")
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_confidence_threshold():
    """
    Demonstrasi efek confidence threshold.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("CONFIDENCE THRESHOLD")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Generate detections dengan berbagai confidence
    image = create_sample_scene()
    
    # Assignment - set nilai ke variabel
    all_detections = [
        {'box': [90, 90, 190, 410], 'class_id': 0, 'conf': 0.95, 'name': 'person'},
        {'box': [340, 250, 560, 390], 'class_id': 2, 'conf': 0.72, 'name': 'car'},
        {'box': [230, 345, 340, 420], 'class_id': 16, 'conf': 0.45, 'name': 'dog'},
        {'box': [500, 50, 580, 120], 'class_id': 14, 'conf': 0.35, 'name': 'bird'},
        {'box': [20, 200, 80, 280], 'class_id': 39, 'conf': 0.25, 'name': 'bottle'},
    ]
    
    # Assignment - set nilai ke variabel
    thresholds = [0.25, 0.5, 0.75]
    
    # Assignment - set nilai ke variabel
    images = []
    # Iterasi/loop melalui elemen dalam koleksi
    for thresh in thresholds:
        # Assignment - set nilai ke variabel
        img = image.copy()
        
        # Iterasi/loop melalui elemen dalam koleksi
        filtered = [d for d in all_detections if d['conf'] >= thresh]
        
        # Iterasi/loop melalui elemen dalam koleksi
        for det in filtered:
            draw_detection(img, det['box'], det['class_id'], det['conf'])
        
        # cv2.putText(a, b, c, d, e, f, g): a=img, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(img, f"Threshold: {thresh}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        # cv2.putText(a, b, c, d, e, f, g): a=img, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(img, f"Detections: {len(filtered)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        # Ubah ukuran gambar ke resolusi baru
        images.append(cv2.resize(img, (400, 300)))
    
    # Assignment - set nilai ke variabel
    combined = np.hstack(images)
    
    # Tampilkan gambar di window
    cv2.imshow("Confidence Threshold Effect", combined)
    
    print("\n[INFO] All detections:")
    # Iterasi/loop melalui elemen dalam koleksi
    for det in all_detections:
        print(f"  - {det['name']}: {det['conf']:.2f}")
    
    print("\n[INFO] Effect of threshold:")
    # Iterasi/loop melalui elemen dalam koleksi
    for thresh in thresholds:
        # Iterasi/loop melalui elemen dalam koleksi
        filtered = [d for d in all_detections if d['conf'] >= thresh]
        print(f"  - Threshold {thresh}: {len(filtered)} detections")
    
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    # Load YOLOv8 model untuk object detection
    print("PRAKTIKUM OBJECT DETECTION DENGAN YOLO")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        # Load YOLOv8 model untuk object detection
        print("1. Arsitektur YOLO")
        # Load YOLOv8 model untuk object detection
        print("2. YOLO Inference pada Gambar")
        # Load YOLOv8 model untuk object detection
        print("3. YOLO Video/Webcam Detection")
        print("4. Non-Maximum Suppression (NMS)")
        print("5. Confidence Threshold")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-6): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_yolo_architecture()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_yolo_inference()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_yolo_video()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_nms()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_confidence_threshold()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_yolo_architecture()
            demo_yolo_inference()
            demo_nms()
            demo_confidence_threshold()
            demo_yolo_video()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
