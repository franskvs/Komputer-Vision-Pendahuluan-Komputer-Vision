"""
===============================================================================
PRAKTIKUM COMPUTER VISION
Bab 06: Recognition - Program 02: Deep Learning Face Detection
===============================================================================

Deskripsi:
    Program ini mendemonstrasikan face detection menggunakan deep learning
    methods: MTCNN, RetinaFace, dan OpenCV DNN.

Konsep yang dipelajari:
    1. MTCNN (Multi-task Cascaded Convolutional Networks)
    2. RetinaFace detector
    3. OpenCV DNN face detector
    4. Perbandingan dengan metode tradisional

Dependencies:
    pip install opencv-python numpy matplotlib
    pip install mtcnn (opsional)
    pip install retinaface (opsional)

Kompatibilitas:
    - Windows/Linux/MacOS
    - Python 3.7+
    
Author: Praktikum Computer Vision
===============================================================================
"""

import cv2
import numpy as np
import os
import urllib.request
from pathlib import Path
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# =====================================================================
# BAGIAN 1: SETUP DAN UTILITIES
# =====================================================================

def create_output_directory():
    """Membuat direktori untuk menyimpan hasil output."""
    output_dir = Path("output_deep_face_detection")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def download_dnn_models():
    """
    Download model untuk OpenCV DNN face detector.
    OpenCV DNN menggunakan model dari Caffe atau TensorFlow.
    """
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # OpenCV DNN Face Detector (Caffe model)
    model_files = {
        'prototxt': (
            'deploy.prototxt',
            'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
        ),
        'caffemodel': (
            'res10_300x300_ssd_iter_140000.caffemodel',
            'https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel'
        )
    }
    
    for key, (filename, url) in model_files.items():
        filepath = models_dir / filename
        if not filepath.exists():
            print(f"⬇ Downloading {filename}...")
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"  ✓ Downloaded {filename}")
            except Exception as e:
                print(f"  ✗ Failed to download: {e}")
                print(f"    Manual download: {url}")
        else:
            print(f"✓ {filename} already exists")
    
    return models_dir

def create_sample_image():
    """
    Membuat sample image dengan ilustrasi wajah.
    Dalam praktik nyata, gunakan gambar asli.
    """
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Gambar beberapa wajah dengan variasi pose
    faces = [
        (160, 200, 80, 0),      # (x, y, radius, rotation)
        (350, 180, 75, -15),
        (500, 200, 65, 20),
        (250, 380, 70, 0),
    ]
    
    for x, y, r, rot in faces:
        # Wajah oval dengan sedikit skin tone
        skin_color = (190, 170, 155)
        cv2.ellipse(img, (x, y), (r, int(r*1.25)), rot, 0, 360, skin_color, -1)
        cv2.ellipse(img, (x, y), (r, int(r*1.25)), rot, 0, 360, (100, 80, 60), 2)
        
        # Mata
        eye_y = y - r//4
        eye_offset = r//3
        
        # Transformasi sederhana untuk rotasi (approximate)
        rad = np.radians(rot)
        cos_r, sin_r = np.cos(rad), np.sin(rad)
        
        # Mata kiri
        ex1 = int(x - eye_offset * cos_r)
        ey1 = int(eye_y - eye_offset * sin_r)
        cv2.circle(img, (ex1, ey1), r//8, (255, 255, 255), -1)
        cv2.circle(img, (ex1, ey1), r//15, (50, 50, 50), -1)
        
        # Mata kanan
        ex2 = int(x + eye_offset * cos_r)
        ey2 = int(eye_y + eye_offset * sin_r)
        cv2.circle(img, (ex2, ey2), r//8, (255, 255, 255), -1)
        cv2.circle(img, (ex2, ey2), r//15, (50, 50, 50), -1)
        
        # Hidung
        nose_y = y + r//8
        cv2.line(img, (x, y), (x, nose_y), (150, 130, 110), 2)
        
        # Mulut
        mouth_y = y + r//2
        cv2.ellipse(img, (x, mouth_y), (r//4, r//8), rot, 20, 160, (150, 100, 100), 2)
    
    cv2.putText(img, "Sample Image for Deep Face Detection", 
                (100, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    
    return img

# =====================================================================
# BAGIAN 2: OPENCV DNN FACE DETECTOR
# =====================================================================

def demo_opencv_dnn_detector():
    """
    Demo OpenCV DNN Face Detector.
    
    OpenCV DNN module mendukung berbagai framework:
    - Caffe
    - TensorFlow
    - Torch
    - ONNX
    - Darknet (YOLO)
    
    Face detector yang digunakan adalah SSD (Single Shot Detector)
    dengan ResNet-10 backbone, ditraining pada WIDER FACE dataset.
    
    Kelebihan:
    - Cukup akurat
    - Tidak perlu library tambahan (built-in OpenCV)
    - Mendukung GPU acceleration
    
    Kekurangan:
    - Tidak seakurat MTCNN/RetinaFace
    - Tidak menyediakan landmarks
    """
    print("\n" + "="*60)
    print("DEMO: OpenCV DNN Face Detector")
    print("="*60)
    
    # Download models jika belum ada
    models_dir = download_dnn_models()
    
    prototxt = models_dir / "deploy.prototxt"
    caffemodel = models_dir / "res10_300x300_ssd_iter_140000.caffemodel"
    
    if not prototxt.exists() or not caffemodel.exists():
        print("\n⚠ Model files tidak tersedia!")
        print("   Menjalankan mode simulasi...")
        demo_dnn_simulation()
        return
    
    # Load model
    print("\n📍 Loading DNN model...")
    net = cv2.dnn.readNetFromCaffe(str(prototxt), str(caffemodel))
    
    # Set backend dan target (CPU atau GPU)
    # Backend options: DNN_BACKEND_DEFAULT, DNN_BACKEND_OPENCV, DNN_BACKEND_CUDA
    # Target options: DNN_TARGET_CPU, DNN_TARGET_CUDA, DNN_TARGET_OPENCL
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    print("✓ Model loaded successfully")
    
    # Load atau buat sample image
    img = create_sample_image()
    h, w = img.shape[:2]
    
    # Prepare input blob
    # Parameter: image, scalefactor, size, mean, swapRB
    # Model ditraining dengan ukuran 300x300
    print("\n📍 Preparing input blob...")
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)),  # Resize ke ukuran model
        1.0,                           # Scale factor
        (300, 300),                    # Size
        (104.0, 177.0, 123.0),        # Mean subtraction
        swapRB=False                   # BGR karena pakai Caffe
    )
    
    # Inference
    print("📍 Running inference...")
    start_time = time.time()
    
    net.setInput(blob)
    detections = net.forward()
    
    inference_time = (time.time() - start_time) * 1000
    print(f"✓ Inference time: {inference_time:.2f} ms")
    
    # Process detections
    # Output shape: [1, 1, N, 7]
    # Setiap detection: [batch_id, class_id, confidence, x1, y1, x2, y2]
    confidence_threshold = 0.5
    
    img_result = img.copy()
    face_count = 0
    
    print(f"\n📊 Hasil Deteksi (threshold={confidence_threshold}):")
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > confidence_threshold:
            face_count += 1
            
            # Get coordinates (normalized 0-1)
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)
            
            # Clip ke boundary image
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            
            # Gambar box
            cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Label dengan confidence
            label = f"Face: {confidence:.2f}"
            cv2.putText(img_result, label, (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            print(f"   Face {face_count}: conf={confidence:.2f}, box=({x1},{y1})-({x2},{y2})")
    
    print(f"\n   Total faces: {face_count}")
    
    # Simpan hasil
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_opencv_dnn.jpg"), img_result)
    print(f"\n✓ Hasil disimpan: {output_dir}/02_opencv_dnn.jpg")
    
    # Tampilkan
    try:
        cv2.imshow("OpenCV DNN Face Detection", img_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        pass

def demo_dnn_simulation():
    """
    Simulasi OpenCV DNN detection untuk kasus model tidak tersedia.
    """
    print("\n📍 Demonstrasi konsep OpenCV DNN...")
    
    print("""
    OpenCV DNN Face Detection Pipeline:
    
    1. Model Loading:
       net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
       atau
       net = cv2.dnn.readNetFromTensorflow(pb_file)
    
    2. Blob Creation:
       blob = cv2.dnn.blobFromImage(
           image,              # Input image
           scalefactor=1.0,    # Pixel value scaling
           size=(300, 300),    # Model input size
           mean=(104, 177, 123), # Mean subtraction
           swapRB=False        # BGR/RGB swap
       )
    
    3. Inference:
       net.setInput(blob)
       detections = net.forward()
    
    4. Post-processing:
       - Filter by confidence threshold
       - Convert normalized coords to image coords
       - Apply NMS (Non-Maximum Suppression) if needed
    """)
    
    # Buat ilustrasi pipeline
    img = create_sample_image()
    
    # Simulasi "deteksi" dengan lokasi approximate
    h, w = img.shape[:2]
    fake_detections = [
        (100, 120, 220, 280, 0.95),
        (280, 100, 420, 260, 0.92),
        (430, 130, 570, 280, 0.88),
        (180, 300, 320, 450, 0.90),
    ]
    
    for x1, y1, x2, y2, conf in fake_detections:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{conf:.2f}", (x1, y1-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    cv2.putText(img, "Simulated DNN Detection", (200, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_dnn_simulated.jpg"), img)
    print(f"\n✓ Simulasi disimpan: {output_dir}/02_dnn_simulated.jpg")

# =====================================================================
# BAGIAN 3: MTCNN (Multi-task Cascaded Convolutional Networks)
# =====================================================================

def demo_mtcnn_detector():
    """
    Demo MTCNN Face Detector.
    
    MTCNN (Multi-task Cascaded Convolutional Networks):
    - Paper: "Joint Face Detection and Alignment using Multi-task Cascaded 
             Convolutional Networks" (Zhang et al., 2016)
    
    Arsitektur 3-stage cascade:
    1. P-Net (Proposal Network): 
       - Input: Image pyramid
       - Output: Candidate face regions
       - Fast, low resolution
    
    2. R-Net (Refine Network):
       - Input: Candidates dari P-Net
       - Output: Refined bounding boxes
       - Medium resolution
    
    3. O-Net (Output Network):
       - Input: Refined candidates
       - Output: Final boxes + 5 landmarks
       - High resolution, accurate
    
    Kelebihan:
    - Akurat
    - Menyediakan landmarks (mata, hidung, mulut)
    - Real-time capable
    
    Kekurangan:
    - Lebih lambat dari single-stage detector
    - Kurang akurat untuk wajah sangat kecil
    """
    print("\n" + "="*60)
    print("DEMO: MTCNN Face Detector")
    print("="*60)
    
    # Cek apakah mtcnn tersedia
    try:
        from mtcnn import MTCNN
        HAS_MTCNN = True
        print("\n✓ MTCNN library tersedia")
    except ImportError:
        HAS_MTCNN = False
        print("\n⚠ MTCNN library tidak tersedia")
        print("   Install dengan: pip install mtcnn")
    
    if HAS_MTCNN:
        run_mtcnn_detection()
    else:
        demo_mtcnn_concept()

def run_mtcnn_detection():
    """Jalankan MTCNN detection."""
    from mtcnn import MTCNN
    
    # Initialize detector
    print("\n📍 Initializing MTCNN detector...")
    detector = MTCNN()
    print("✓ Detector initialized")
    
    # Load image
    img = create_sample_image()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # MTCNN expects RGB
    
    # Detect faces
    print("\n📍 Detecting faces...")
    start_time = time.time()
    results = detector.detect_faces(img_rgb)
    detection_time = (time.time() - start_time) * 1000
    
    print(f"\n📊 Hasil Deteksi:")
    print(f"   Waktu: {detection_time:.2f} ms")
    print(f"   Faces: {len(results)}")
    
    # Process results
    img_result = img.copy()
    
    for i, face in enumerate(results):
        # Bounding box
        x, y, w, h = face['box']
        confidence = face['confidence']
        
        # Gambar box
        cv2.rectangle(img_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Landmarks (5 points: left_eye, right_eye, nose, mouth_left, mouth_right)
        keypoints = face['keypoints']
        
        # Gambar landmarks
        colors = {
            'left_eye': (255, 0, 0),
            'right_eye': (0, 0, 255),
            'nose': (0, 255, 0),
            'mouth_left': (255, 255, 0),
            'mouth_right': (0, 255, 255)
        }
        
        for name, point in keypoints.items():
            color = colors.get(name, (255, 255, 255))
            cv2.circle(img_result, point, 3, color, -1)
        
        # Label
        cv2.putText(img_result, f"Face {i+1}: {confidence:.2f}", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        print(f"\n   Face {i+1}:")
        print(f"      Confidence: {confidence:.2f}")
        print(f"      Box: ({x}, {y}, {w}, {h})")
        print(f"      Landmarks: {len(keypoints)} points")
    
    # Simpan hasil
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_mtcnn.jpg"), img_result)
    print(f"\n✓ Hasil disimpan: {output_dir}/02_mtcnn.jpg")
    
    # Tampilkan
    try:
        cv2.imshow("MTCNN Face Detection", img_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        pass

def demo_mtcnn_concept():
    """Demo konsep MTCNN tanpa library."""
    print("\n📍 Demonstrasi konsep MTCNN...")
    
    print("""
    MTCNN Architecture:
    ==================
    
    Image Pyramid
         │
         ▼
    ┌─────────┐
    │  P-Net  │  Proposal Network (12x12 conv)
    │         │  → Coarse face candidates
    │ 12x12   │  → NMS to reduce candidates
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  R-Net  │  Refine Network (24x24 conv)
    │         │  → Better bbox regression
    │ 24x24   │  → Filter false positives
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  O-Net  │  Output Network (48x48 conv)
    │         │  → Final bbox + 5 landmarks
    │ 48x48   │  → High quality results
    └─────────┘
    
    5-Point Landmarks:
    • Left eye center
    • Right eye center
    • Nose tip
    • Left mouth corner
    • Right mouth corner
    """)
    
    # Buat ilustrasi
    img = create_sample_image()
    h, w = img.shape[:2]
    
    # Simulasi deteksi dengan landmarks
    fake_faces = [
        # (x, y, w, h, landmarks)
        (100, 120, 120, 160, [(130, 160), (190, 160), (160, 190), (140, 230), (180, 230)]),
        (280, 100, 140, 180, [(320, 140), (380, 140), (350, 180), (330, 220), (370, 220)]),
    ]
    
    for x, y, bw, bh, landmarks in fake_faces:
        # Box
        cv2.rectangle(img, (x, y), (x+bw, y+bh), (0, 255, 0), 2)
        
        # Landmarks
        landmark_names = ['left_eye', 'right_eye', 'nose', 'mouth_left', 'mouth_right']
        colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255)]
        
        for (lx, ly), name, color in zip(landmarks, landmark_names, colors):
            cv2.circle(img, (lx, ly), 4, color, -1)
    
    # Legend
    legend_y = h - 80
    cv2.putText(img, "Landmarks:", (10, legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    legend_items = [("L Eye", (255, 0, 0)), ("R Eye", (0, 0, 255)), 
                    ("Nose", (0, 255, 0)), ("Mouth", (255, 255, 0))]
    for i, (name, color) in enumerate(legend_items):
        x = 10 + i * 100
        cv2.circle(img, (x, legend_y + 20), 5, color, -1)
        cv2.putText(img, name, (x + 10, legend_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    cv2.putText(img, "MTCNN Concept (Simulated)", (200, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_mtcnn_concept.jpg"), img)
    print(f"\n✓ Ilustrasi disimpan: {output_dir}/02_mtcnn_concept.jpg")

# =====================================================================
# BAGIAN 4: RETINAFACE
# =====================================================================

def demo_retinaface_detector():
    """
    Demo RetinaFace Detector.
    
    RetinaFace:
    - Paper: "RetinaFace: Single-shot Multi-level Face Localisation in the Wild"
             (Deng et al., 2019)
    
    Fitur utama:
    - Single-stage detector (lebih cepat dari MTCNN)
    - Multi-task learning: detection + landmarks + 3D face
    - Feature Pyramid Network (FPN) untuk multi-scale
    - Context modules untuk small faces
    
    Output:
    - Bounding box
    - 5 landmarks
    - Quality score
    - (Optional) 3D face reconstruction
    """
    print("\n" + "="*60)
    print("DEMO: RetinaFace Detector")
    print("="*60)
    
    # Cek library
    try:
        from retinaface import RetinaFace
        HAS_RETINAFACE = True
        print("\n✓ RetinaFace library tersedia")
    except ImportError:
        HAS_RETINAFACE = False
        print("\n⚠ RetinaFace library tidak tersedia")
        print("   Install dengan: pip install retinaface")
    
    if HAS_RETINAFACE:
        run_retinaface_detection()
    else:
        demo_retinaface_concept()

def run_retinaface_detection():
    """Jalankan RetinaFace detection."""
    from retinaface import RetinaFace
    
    # Buat/load image
    img = create_sample_image()
    
    # Simpan sementara (RetinaFace butuh path atau numpy)
    temp_path = "temp_face_image.jpg"
    cv2.imwrite(temp_path, img)
    
    print("\n📍 Running RetinaFace detection...")
    start_time = time.time()
    
    # Detect
    faces = RetinaFace.detect_faces(temp_path)
    
    detection_time = (time.time() - start_time) * 1000
    print(f"✓ Detection time: {detection_time:.2f} ms")
    
    # Process results
    img_result = img.copy()
    
    if isinstance(faces, dict):
        print(f"\n📊 Detected {len(faces)} face(s)")
        
        for face_id, face_data in faces.items():
            # Bounding box
            x1, y1, x2, y2 = face_data['facial_area']
            confidence = face_data['score']
            
            cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Landmarks
            landmarks = face_data['landmarks']
            
            for name, (lx, ly) in landmarks.items():
                cv2.circle(img_result, (int(lx), int(ly)), 3, (0, 0, 255), -1)
            
            # Label
            cv2.putText(img_result, f"{face_id}: {confidence:.2f}", (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            print(f"\n   {face_id}:")
            print(f"      Score: {confidence:.2f}")
            print(f"      Area: ({x1}, {y1}) - ({x2}, {y2})")
    else:
        print("   No faces detected")
    
    # Cleanup
    os.remove(temp_path)
    
    # Simpan hasil
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_retinaface.jpg"), img_result)
    print(f"\n✓ Hasil disimpan: {output_dir}/02_retinaface.jpg")

def demo_retinaface_concept():
    """Demo konsep RetinaFace tanpa library."""
    print("\n📍 Demonstrasi konsep RetinaFace...")
    
    print("""
    RetinaFace Architecture:
    =======================
    
    Input Image
         │
         ▼
    ┌──────────────┐
    │   Backbone   │  ResNet-50/MobileNet
    │   (Feature   │
    │  Extraction) │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │     FPN      │  Feature Pyramid Network
    │  (Multi-     │  C2, C3, C4, C5 features
    │   Scale)     │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Context    │  SSH-like context module
    │   Module     │  For small face detection
    └──────┬───────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
    ┌───────┐  ┌──────┐  ┌──────────┐
    │ Class │  │ Box  │  │ Landmark │
    │ Head  │  │ Head │  │   Head   │
    └───────┘  └──────┘  └──────────┘
    
    Multi-task Outputs:
    • Face/Non-face classification
    • Bounding box regression
    • 5-point landmark localization
    • (Optional) 3D face reconstruction
    """)
    
    # Buat ilustrasi
    img = create_sample_image()
    
    # Simulasi deteksi
    fake_faces = [
        (100, 120, 220, 280, 0.99, [(135, 165), (185, 165), (160, 195), (140, 240), (180, 240)]),
        (280, 100, 420, 280, 0.97, [(325, 150), (385, 150), (355, 190), (335, 230), (375, 230)]),
    ]
    
    for x1, y1, x2, y2, conf, landmarks in fake_faces:
        # Box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{conf:.2f}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Landmarks
        colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255)]
        for (lx, ly), color in zip(landmarks, colors):
            cv2.circle(img, (lx, ly), 4, color, -1)
    
    cv2.putText(img, "RetinaFace Concept (Simulated)", (180, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_retinaface_concept.jpg"), img)
    print(f"\n✓ Ilustrasi disimpan: {output_dir}/02_retinaface_concept.jpg")

# =====================================================================
# BAGIAN 5: PERBANDINGAN METODE DEEP LEARNING
# =====================================================================

def demo_deep_comparison():
    """
    Perbandingan berbagai deep learning face detectors.
    """
    print("\n" + "="*60)
    print("DEMO: Perbandingan Deep Learning Face Detectors")
    print("="*60)
    
    img = create_sample_image()
    results = []
    
    # Test OpenCV DNN
    print("\n📍 Testing OpenCV DNN...")
    models_dir = Path("models")
    prototxt = models_dir / "deploy.prototxt"
    caffemodel = models_dir / "res10_300x300_ssd_iter_140000.caffemodel"
    
    if prototxt.exists() and caffemodel.exists():
        net = cv2.dnn.readNetFromCaffe(str(prototxt), str(caffemodel))
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, 
                                     (300, 300), (104.0, 177.0, 123.0))
        
        start = time.time()
        net.setInput(blob)
        detections = net.forward()
        dnn_time = (time.time() - start) * 1000
        
        # Count faces
        dnn_faces = sum(1 for i in range(detections.shape[2]) 
                       if detections[0, 0, i, 2] > 0.5)
        
        results.append({
            'method': 'OpenCV DNN',
            'faces': dnn_faces,
            'time_ms': dnn_time,
            'landmarks': False
        })
    else:
        print("   ⚠ Model not available")
    
    # Test MTCNN
    print("📍 Testing MTCNN...")
    try:
        from mtcnn import MTCNN
        detector = MTCNN()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        start = time.time()
        mtcnn_results = detector.detect_faces(img_rgb)
        mtcnn_time = (time.time() - start) * 1000
        
        results.append({
            'method': 'MTCNN',
            'faces': len(mtcnn_results),
            'time_ms': mtcnn_time,
            'landmarks': True
        })
    except ImportError:
        print("   ⚠ MTCNN not installed")
    
    # Test RetinaFace
    print("📍 Testing RetinaFace...")
    try:
        from retinaface import RetinaFace
        temp_path = "temp_comparison.jpg"
        cv2.imwrite(temp_path, img)
        
        start = time.time()
        rf_results = RetinaFace.detect_faces(temp_path)
        rf_time = (time.time() - start) * 1000
        
        rf_faces = len(rf_results) if isinstance(rf_results, dict) else 0
        
        results.append({
            'method': 'RetinaFace',
            'faces': rf_faces,
            'time_ms': rf_time,
            'landmarks': True
        })
        
        os.remove(temp_path)
    except ImportError:
        print("   ⚠ RetinaFace not installed")
    
    # Tampilkan perbandingan
    if results:
        print("\n" + "="*60)
        print("📊 HASIL PERBANDINGAN:")
        print("="*60)
        print(f"{'Method':<20} {'Faces':<10} {'Time (ms)':<15} {'Landmarks':<10}")
        print("-"*55)
        
        for r in results:
            landmarks = "Yes" if r['landmarks'] else "No"
            print(f"{r['method']:<20} {r['faces']:<10} {r['time_ms']:<15.2f} {landmarks:<10}")
        
        # Analisis
        print("\n📝 Analisis:")
        if len(results) > 1:
            fastest = min(results, key=lambda x: x['time_ms'])
            most_faces = max(results, key=lambda x: x['faces'])
            print(f"   • Tercepat: {fastest['method']} ({fastest['time_ms']:.2f} ms)")
            print(f"   • Paling banyak deteksi: {most_faces['method']} ({most_faces['faces']} faces)")
        
        # Buat visualisasi
        create_deep_comparison_image(img, results)
    else:
        print("\n⚠ Tidak ada detector yang tersedia untuk perbandingan")
        demo_comparison_concept()

def create_deep_comparison_image(img, results):
    """Buat visualisasi perbandingan."""
    # Placeholder - buat chart sederhana
    chart_width = 600
    chart_height = 400
    chart = np.ones((chart_height, chart_width, 3), dtype=np.uint8) * 255
    
    # Title
    cv2.putText(chart, "Deep Learning Face Detectors Comparison", (80, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Bar chart
    bar_width = 100
    max_time = max(r['time_ms'] for r in results) if results else 1
    
    for i, r in enumerate(results):
        x = 80 + i * 180
        
        # Time bar
        bar_height = int(200 * (r['time_ms'] / max_time))
        cv2.rectangle(chart, (x, 300 - bar_height), (x + bar_width, 300), (0, 150, 0), -1)
        
        # Labels
        cv2.putText(chart, r['method'], (x, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(chart, f"{r['time_ms']:.1f}ms", (x + 20, 290 - bar_height),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 100, 0), 1)
        cv2.putText(chart, f"{r['faces']} faces", (x + 20, 350),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 0, 0), 1)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_deep_comparison.jpg"), chart)
    print(f"\n✓ Comparison chart disimpan: {output_dir}/02_deep_comparison.jpg")

def demo_comparison_concept():
    """Demo perbandingan konsep saja."""
    print("""
    
    Perbandingan Deep Learning Face Detectors:
    ==========================================
    
    | Method      | Speed    | Accuracy | Landmarks | Notes              |
    |-------------|----------|----------|-----------|---------------------|
    | OpenCV DNN  | Fast     | Good     | No        | Built-in OpenCV     |
    | MTCNN       | Medium   | Very Good| Yes (5)   | 3-stage cascade     |
    | RetinaFace  | Medium   | Excellent| Yes (5)   | State-of-the-art    |
    | BlazeFace   | Very Fast| Good     | Yes (6)   | Mobile-optimized    |
    
    Recommendations:
    ================
    • Real-time mobile: BlazeFace
    • General use: OpenCV DNN (no extra dependencies)
    • High accuracy: RetinaFace
    • Balance speed/accuracy: MTCNN
    """)

# =====================================================================
# BAGIAN 6: CONFIDENCE THRESHOLD & NMS
# =====================================================================

def demo_confidence_threshold():
    """
    Demo pengaruh confidence threshold pada detection.
    
    Confidence threshold adalah batas minimum kepercayaan
    detector bahwa suatu region mengandung wajah.
    
    - Threshold tinggi: Lebih strict, miss beberapa wajah
    - Threshold rendah: Lebih sensitif, lebih banyak false positives
    """
    print("\n" + "="*60)
    print("DEMO: Pengaruh Confidence Threshold")
    print("="*60)
    
    # Load OpenCV DNN model
    models_dir = Path("models")
    prototxt = models_dir / "deploy.prototxt"
    caffemodel = models_dir / "res10_300x300_ssd_iter_140000.caffemodel"
    
    if not prototxt.exists() or not caffemodel.exists():
        print("\n⚠ Model tidak tersedia, menjalankan demo konsep...")
        demo_threshold_concept()
        return
    
    net = cv2.dnn.readNetFromCaffe(str(prototxt), str(caffemodel))
    
    img = create_sample_image()
    h, w = img.shape[:2]
    
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    
    # Test berbagai threshold
    thresholds = [0.3, 0.5, 0.7, 0.9]
    
    print("\n📊 Pengaruh Confidence Threshold:")
    print("-"*40)
    print(f"{'Threshold':<15} {'Faces Detected':<15}")
    print("-"*40)
    
    # Buat comparison image
    comparison = np.ones((500, len(thresholds) * 200, 3), dtype=np.uint8) * 255
    
    for idx, thresh in enumerate(thresholds):
        img_copy = img.copy()
        face_count = 0
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > thresh:
                face_count += 1
                
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                
                cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        print(f"{thresh:<15} {face_count:<15}")
        
        # Add to comparison
        img_small = cv2.resize(img_copy, (180, 150))
        x_offset = idx * 200 + 10
        comparison[80:230, x_offset:x_offset+180] = img_small
        
        cv2.putText(comparison, f"Threshold: {thresh}", (x_offset + 30, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(comparison, f"Faces: {face_count}", (x_offset + 50, 260),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 1)
    
    # Title
    cv2.putText(comparison, "Confidence Threshold Comparison", (comparison.shape[1]//2 - 150, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    output_dir = create_output_directory()
    cv2.imwrite(str(output_dir / "02_threshold_comparison.jpg"), comparison)
    print(f"\n✓ Comparison disimpan: {output_dir}/02_threshold_comparison.jpg")
    
    print("\n💡 Rekomendasi Threshold:")
    print("   • General: 0.5 (balanced)")
    print("   • Security (minimize false positives): 0.7-0.9")
    print("   • Search (minimize misses): 0.3-0.5")

def demo_threshold_concept():
    """Demo konsep threshold tanpa model."""
    print("""
    
    Confidence Threshold Effect:
    ===========================
    
    High Threshold (0.9):
    • Hanya wajah dengan confidence sangat tinggi
    • Lebih sedikit false positives
    • Mungkin miss wajah dengan pose/lighting challenging
    
    Medium Threshold (0.5):
    • Balance antara sensitivity dan specificity
    • Recommended untuk general use
    
    Low Threshold (0.2):
    • Detect lebih banyak wajah
    • Risk lebih banyak false positives
    • Berguna jika di-combine dengan verification step
    """)

# =====================================================================
# MENU UTAMA
# =====================================================================

def main():
    """Menu utama program deep learning face detection."""
    print("="*60)
    print("PRAKTIKUM COMPUTER VISION")
    print("Bab 06: Deep Learning Face Detection")
    print("="*60)
    
    while True:
        print("\n" + "-"*40)
        print("MENU:")
        print("-"*40)
        print("1. OpenCV DNN Face Detector")
        print("2. MTCNN Face Detector")
        print("3. RetinaFace Detector")
        print("4. Deep Learning Comparison")
        print("5. Confidence Threshold Demo")
        print("0. Exit")
        print("-"*40)
        
        try:
            choice = input("\nPilih menu [0-5]: ").strip()
        except EOFError:
            choice = "0"
        
        if choice == "1":
            demo_opencv_dnn_detector()
        elif choice == "2":
            demo_mtcnn_detector()
        elif choice == "3":
            demo_retinaface_detector()
        elif choice == "4":
            demo_deep_comparison()
        elif choice == "5":
            demo_confidence_threshold()
        elif choice == "0":
            print("\n👋 Terima kasih!")
            break
        else:
            print("⚠ Pilihan tidak valid!")

if __name__ == "__main__":
    main()
