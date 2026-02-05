"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 12 - OPENCV DNN DEPLOYMENT
# Assignment - set nilai ke variabel
=============================================================================
Program ini mendemonstrasikan deployment model deep learning menggunakan
OpenCV DNN module tanpa memerlukan PyTorch atau TensorFlow.

Konsep yang dipelajari:
1. OpenCV DNN module overview
2. Loading berbagai format model
3. Inference untuk classification
4. Inference untuk object detection
5. Inference untuk segmentation
6. Performance optimization

Kebutuhan:
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy

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
import time
# Import library/module untuk digunakan
import os
# Import library/module untuk digunakan
import urllib.request


# Definisi function dengan nama dan parameter
def check_opencv_dnn():
    """
    Check OpenCV DNN support.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("OPENCV DNN MODULE CHECK")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print(f"\n[INFO] OpenCV version: {cv2.__version__}")
    
    # Check available backends
    print("\n[INFO] Available DNN backends:")
    # Assignment - set nilai ke variabel
    backends = {
        cv2.dnn.DNN_BACKEND_DEFAULT: "Default",
        cv2.dnn.DNN_BACKEND_OPENCV: "OpenCV",
    }
    
    # Check optional backends
    try:
        # Assignment - set nilai ke variabel
        backends[cv2.dnn.DNN_BACKEND_CUDA] = "CUDA"
    # Tangkap exception jika ada error di blok try
    except:
        pass
    
    # Blok try-except untuk error handling
    try:
        # Assignment - set nilai ke variabel
        backends[cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE] = "OpenVINO"
    # Tangkap exception jika ada error di blok try
    except:
        pass
    
    # Iterasi/loop melalui elemen dalam koleksi
    for backend_id, name in backends.items():
        print(f"  - {name} (ID: {backend_id})")
    
    # Check available targets
    print("\n[INFO] Available DNN targets:")
    # Assignment - set nilai ke variabel
    targets = {
        cv2.dnn.DNN_TARGET_CPU: "CPU",
    }
    
    # Blok try-except untuk error handling
    try:
        # Assignment - set nilai ke variabel
        targets[cv2.dnn.DNN_TARGET_CUDA] = "CUDA"
    # Tangkap exception jika ada error di blok try
    except:
        pass
    
    # Blok try-except untuk error handling
    try:
        # Assignment - set nilai ke variabel
        targets[cv2.dnn.DNN_TARGET_CUDA_FP16] = "CUDA FP16"
    # Tangkap exception jika ada error di blok try
    except:
        pass
    
    # Blok try-except untuk error handling
    try:
        # Assignment - set nilai ke variabel
        targets[cv2.dnn.DNN_TARGET_OPENCL] = "OpenCL"
    # Tangkap exception jika ada error di blok try
    except:
        pass
    
    # Iterasi/loop melalui elemen dalam koleksi
    for target_id, name in targets.items():
        print(f"  - {name} (ID: {target_id})")


# Definisi function dengan nama dan parameter
def demo_dnn_overview():
    """
    Overview tentang OpenCV DNN module.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("OPENCV DNN MODULE OVERVIEW")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [APA ITU OPENCV DNN?]
    ─────────────────────────────────────────────────────────────────────
    OpenCV DNN adalah modul inference untuk deep learning yang:
    
    - TIDAK memerlukan training (inference only)
    - TIDAK memerlukan PyTorch atau TensorFlow runtime
    - Mendukung berbagai format model
    - Cross-platform dan lightweight
    
    
    [SUPPORTED MODEL FORMATS]
    ─────────────────────────────────────────────────────────────────────
    
    ┌────────────────┬────────────────────────────────────────────────┐
    │ Format         │ Loading Function                               │
    ├────────────────┼────────────────────────────────────────────────┤
    # Baca model Caffe dari file .prototxt dan .caffemodel
    │ Caffe          │ cv2.dnn.readNetFromCaffe(prototxt, caffemodel) │
    # Baca model TensorFlow dari file .pb
    │ TensorFlow     │ cv2.dnn.readNetFromTensorflow(pb, pbtxt)       │
    # Baca model YOLO dari file .cfg dan .weights
    │ Darknet (YOLO) │ cv2.dnn.readNetFromDarknet(cfg, weights)       │
    │ ONNX           │ cv2.dnn.readNetFromONNX(model.onnx)            │
    │ Torch          │ cv2.dnn.readNetFromTorch(model.t7)             │
    │ TFLite         │ cv2.dnn.readNetFromTFLite(model.tflite)        │
    └────────────────┴────────────────────────────────────────────────┘
    
    
    [BASIC WORKFLOW]
    ─────────────────────────────────────────────────────────────────────
    
    1. Load model
       # Assignment - set nilai ke variabel
       net = cv2.dnn.readNetFromONNX('model.onnx')
    
    2. Set backend and target
       net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
       net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    3. Preprocess input
       # Konversi gambar ke blob untuk neural network
       blob = cv2.dnn.blobFromImage(image, scalefactor, size, mean, swapRB)
    
    4. Set input
       net.setInput(blob)
    
    5. Forward pass
       # Assignment - set nilai ke variabel
       output = net.forward()
    
    
    [BLOB FROM IMAGE]
    ─────────────────────────────────────────────────────────────────────
    
    # Konversi gambar ke blob untuk neural network
    cv2.dnn.blobFromImage(image, scalefactor, size, mean, swapRB, crop)
    
    Parameters:
    - image: Input image (BGR by default)
    - scalefactor: Multiply values by this (usually 1/255 or 1/127.5)
    - size: Output blob size (width, height)
    - mean: Mean subtraction values (B, G, R)
    - swapRB: Swap Red and Blue channels (BGR→RGB)
    - crop: Whether to crop or resize
    
    Output shape: (N, C, H, W)
    - N: Batch size
    - C: Number of channels
    - H: Height
    - W: Width
    
    
    [COMMON PREPROCESSING]
    ─────────────────────────────────────────────────────────────────────
    
    ImageNet models:
    # Konversi gambar ke blob untuk neural network
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (224, 224),
                                  (0.485*255, 0.456*255, 0.406*255),
                                  # Assignment - set nilai ke variabel
                                  swapRB=True, crop=False)
    
    # Load YOLOv8 model untuk object detection
    YOLO models:
    # Konversi gambar ke blob untuk neural network
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416),
                                  # Assignment - set nilai ke variabel
                                  (0, 0, 0), swapRB=True, crop=False)
    
    MobileNet-SSD:
    # Konversi gambar ke blob untuk neural network
    blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300),
                                  # Assignment - set nilai ke variabel
                                  (127.5, 127.5, 127.5), swapRB=True)
    """)


# Definisi function dengan nama dan parameter
def demo_classification_inference():
    """
    Demonstrasi inference untuk image classification.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("CLASSIFICATION INFERENCE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Try to use existing ONNX model or create synthetic demo
    onnx_path = "simple_classifier.onnx"
    
    # Conditional statement - eksekusi jika kondisi True
    if os.path.exists(onnx_path):
        print(f"\n[INFO] Loading model from {onnx_path}...")
        
        # Blok try-except untuk error handling
        try:
            # Assignment - set nilai ke variabel
            net = cv2.dnn.readNetFromONNX(onnx_path)
            
            # Set backend
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            print("[INFO] Model loaded successfully!")
            
            # Get layer info
            layer_names = net.getLayerNames()
            print(f"[INFO] Number of layers: {len(layer_names)}")
            
            # Create test image
            test_img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
            
            # Preprocess
            blob = cv2.dnn.blobFromImage(test_img, 1/255.0, (64, 64),
                                         # Assignment - set nilai ke variabel
                                         (0, 0, 0), swapRB=True, crop=False)
            
            print(f"\n[INFO] Input blob shape: {blob.shape}")
            
            # Inference
            net.setInput(blob)
            
            # Assignment - set nilai ke variabel
            start = time.time()
            # Assignment - set nilai ke variabel
            output = net.forward()
            # Assignment - set nilai ke variabel
            inference_time = (time.time() - start) * 1000
            
            print(f"[INFO] Output shape: {output.shape}")
            print(f"[INFO] Inference time: {inference_time:.2f} ms")
            
            # Get prediction
            class_id = np.argmax(output[0])
            # Assignment - set nilai ke variabel
            confidence = output[0][class_id]
            
            print(f"\n[PREDICTION]")
            print(f"  Class ID: {class_id}")
            print(f"  Confidence: {confidence:.4f}")
            
            # Benchmark
            print("\n[BENCHMARK]")
            # Assignment - set nilai ke variabel
            times = []
            # Iterasi/loop melalui elemen dalam koleksi
            for _ in range(50):
                # Assignment - set nilai ke variabel
                start = time.time()
                net.forward()
                times.append(time.time() - start)
            
            # Hitung rata-rata dari array
            print(f"  Average: {np.mean(times)*1000:.2f} ms")
            # Hitung standard deviation dari array
            print(f"  Std Dev: {np.std(times)*1000:.2f} ms")
            # Hitung rata-rata dari array
            print(f"  FPS: {1/np.mean(times):.1f}")
            
        # Tangkap exception jika ada error di blok try
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
    
    else:
        print(f"\n[WARNING] {onnx_path} not found")
        print("[INFO] Showing classification workflow example...")
    
    # Show example code
    print("""
    [CLASSIFICATION EXAMPLE CODE]
    ─────────────────────────────────────────────────────────────────────
    
    # Load model
    net = cv2.dnn.readNetFromONNX('mobilenet_v2.onnx')
    
    # Read image
    image = cv2.imread('image.jpg')
    
    # Preprocess
    blob = cv2.dnn.blobFromImage(
        image,
        # Assignment - set nilai ke variabel
        scalefactor=1/255.0,
        # Assignment - set nilai ke variabel
        size=(224, 224),
        # Assignment - set nilai ke variabel
        mean=(0.485*255, 0.456*255, 0.406*255),  # ImageNet mean
        # Assignment - set nilai ke variabel
        swapRB=True,
        # Assignment - set nilai ke variabel
        crop=False
    )
    
    # Inference
    net.setInput(blob)
    # Assignment - set nilai ke variabel
    output = net.forward()
    
    # Get top-5 predictions
    indices = np.argsort(output[0])[::-1][:5]
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i, idx in enumerate(indices):
        print(f"{i+1}. Class {idx}: {output[0][idx]:.4f}")
    """)


# Definisi function dengan nama dan parameter
def demo_detection_inference():
    """
    Demonstrasi inference untuk object detection dengan OpenCV DNN.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("OBJECT DETECTION INFERENCE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [SUPPORTED DETECTION MODELS]
    ─────────────────────────────────────────────────────────────────────
    
    # Load YOLOv8 model untuk object detection
    1. YOLO (Darknet)
       ───────────────
       # Assignment - set nilai ke variabel
       cfg = 'yolov4.cfg'
       # Assignment - set nilai ke variabel
       weights = 'yolov4.weights'
       # Baca model YOLO dari file .cfg dan .weights
       net = cv2.dnn.readNetFromDarknet(cfg, weights)
    
    # Load YOLOv8 model untuk object detection
    2. YOLO (ONNX)
       ────────────
       # Assignment - set nilai ke variabel
       net = cv2.dnn.readNetFromONNX('yolov8n.onnx')
    
    3. SSD (Caffe/TensorFlow)
       ────────────────────────
       # Baca model Caffe dari file .prototxt dan .caffemodel
       net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_ssd.caffemodel')
       # Baca model TensorFlow dari file .pb
       net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'config.pbtxt')
    
    4. Faster R-CNN (TensorFlow)
       ─────────────────────────
       # Baca model TensorFlow dari file .pb
       net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb')
    """)
    
    # Simulated detection demo
    print("\n[INFO] Running simulated detection demo...")
    
    # Create test image
    test_img = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Draw some objects
    cv2.rectangle(test_img, (100, 100), (200, 300), (150, 100, 100), -1)  # Person
    # Gambar persegi panjang pada gambar
    cv2.rectangle(test_img, (400, 150), (580, 280), (100, 100, 150), -1)  # Car
    
    # Simulated detections
    detections = [
        {'class': 'person', 'confidence': 0.92, 'box': [100, 100, 200, 300]},
        {'class': 'car', 'confidence': 0.88, 'box': [400, 150, 580, 280]},
    ]
    
    # Draw detections
    for det in detections:
        # Assignment - set nilai ke variabel
        x1, y1, x2, y2 = det['box']
        # Gambar persegi panjang pada gambar
        cv2.rectangle(test_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Assignment - set nilai ke variabel
        label = f"{det['class']}: {det['confidence']:.2f}"
        # cv2.putText(a, b, c, d, e, f, g): a=test_img, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(test_img, label, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Tampilkan gambar di window
    cv2.imshow("Detection Demo", test_img)
    # Tunggu input keyboard (1ms per iterasi)
    cv2.waitKey(2000)
    # Tutup semua window
    cv2.destroyAllWindows()
    
    # Show example code
    print("""
    # Load YOLOv8 model untuk object detection
    [YOLO DETECTION WITH OPENCV DNN]
    ─────────────────────────────────────────────────────────────────────
    
    # Load YOLO model
    net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    # Get output layer names
    layer_names = net.getLayerNames()
    # Iterasi/loop melalui elemen dalam koleksi
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    
    # Read image
    image = cv2.imread('image.jpg')
    # Assignment - set nilai ke variabel
    height, width = image.shape[:2]
    
    # Preprocess
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416),
                                  # Assignment - set nilai ke variabel
                                  swapRB=True, crop=False)
    
    # Inference
    net.setInput(blob)
    # Assignment - set nilai ke variabel
    outputs = net.forward(output_layers)
    
    # Process outputs
    boxes = []
    # Assignment - set nilai ke variabel
    confidences = []
    # Assignment - set nilai ke variabel
    class_ids = []
    
    # Iterasi/loop melalui elemen dalam koleksi
    for output in outputs:
        # Iterasi/loop melalui elemen dalam koleksi
        for detection in output:
            # Assignment - set nilai ke variabel
            scores = detection[5:]
            # Cari index dari nilai maksimum
            class_id = np.argmax(scores)
            # Assignment - set nilai ke variabel
            confidence = scores[class_id]
            
            # Conditional statement - eksekusi jika kondisi True
            if confidence > 0.5:
                # Scale box back to image size
                center_x = int(detection[0] * width)
                # Assignment - set nilai ke variabel
                center_y = int(detection[1] * height)
                # Assignment - set nilai ke variabel
                w = int(detection[2] * width)
                # Assignment - set nilai ke variabel
                h = int(detection[3] * height)
                
                # Assignment - set nilai ke variabel
                x = int(center_x - w / 2)
                # Assignment - set nilai ke variabel
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Draw results
    for i in indices.flatten():
        # Assignment - set nilai ke variabel
        x, y, w, h = boxes[i]
        # Gambar persegi panjang pada gambar
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    """)


# Definisi function dengan nama dan parameter
def demo_segmentation_inference():
    """
    Demonstrasi inference untuk semantic segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("SEGMENTATION INFERENCE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [SEGMENTATION WITH OPENCV DNN]
    ─────────────────────────────────────────────────────────────────────
    
    # Load segmentation model (DeepLab, FCN, etc.)
    net = cv2.dnn.readNetFromONNX('deeplabv3.onnx')
    
    # Or from TensorFlow
    # net = cv2.dnn.readNetFromTensorflow('deeplabv3_frozen.pb')
    
    # Read image
    image = cv2.imread('image.jpg')
    
    # Preprocess
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (513, 513),
                                  (0.485*255, 0.456*255, 0.406*255),
                                  # Assignment - set nilai ke variabel
                                  swapRB=True, crop=False)
    
    # Inference
    net.setInput(blob)
    # Assignment - set nilai ke variabel
    output = net.forward()  # Shape: (1, num_classes, H, W)
    
    # Get segmentation map
    seg_map = np.argmax(output[0], axis=0)  # Shape: (H, W)
    
    # Resize to original size
    seg_map = cv2.resize(seg_map.astype(np.uint8), (image.shape[1], image.shape[0]),
                         # Assignment - set nilai ke variabel
                         interpolation=cv2.INTER_NEAREST)
    
    # Apply colormap
    colormap = create_colormap(21)  # 21 classes for Pascal VOC
    # Assignment - set nilai ke variabel
    colored_seg = colormap[seg_map]
    
    # Overlay
    overlay = cv2.addWeighted(image, 0.6, colored_seg.astype(np.uint8), 0.4, 0)
    """)
    
    # Simulated segmentation demo
    print("\n[INFO] Running simulated segmentation demo...")
    
    # Create test image and mask
    test_img = np.ones((300, 400, 3), dtype=np.uint8) * 135  # Sky
    # Assignment - set nilai ke variabel
    test_img[200:, :] = [34, 139, 34]  # Ground
    # Gambar persegi panjang pada gambar
    cv2.rectangle(test_img, (100, 80), (180, 220), [100, 100, 200], -1)  # Person
    # Gambar persegi panjang pada gambar
    cv2.rectangle(test_img, (250, 120), (380, 200), [128, 128, 128], -1)  # Car
    
    # Simulated segmentation output
    seg_map = np.zeros((300, 400), dtype=np.uint8)
    # Definisi class untuk membuat object
    seg_map[:, :] = 0  # Sky as class 0
    # Definisi class untuk membuat object
    seg_map[200:, :] = 1  # Ground as class 1
    # Definisi class untuk membuat object
    seg_map[80:220, 100:180] = 15  # Person as class 15
    # Definisi class untuk membuat object
    seg_map[120:200, 250:380] = 7  # Car as class 7
    
    # Create colormap
    colormap = np.zeros((256, 3), dtype=np.uint8)
    # Assignment - set nilai ke variabel
    colormap[0] = [135, 206, 235]  # Sky
    # Assignment - set nilai ke variabel
    colormap[1] = [34, 139, 34]    # Ground
    # Assignment - set nilai ke variabel
    colormap[7] = [128, 128, 128]  # Car
    # Assignment - set nilai ke variabel
    colormap[15] = [192, 128, 128] # Person
    
    # Assignment - set nilai ke variabel
    colored_seg = colormap[seg_map]
    
    # Overlay
    overlay = cv2.addWeighted(test_img, 0.5, colored_seg, 0.5, 0)
    
    # Display
    combined = np.hstack([test_img, colored_seg, overlay])
    # Tampilkan gambar di window
    cv2.imshow("Segmentation Demo (Input | Mask | Overlay)", combined)
    # Tunggu input keyboard (1ms per iterasi)
    cv2.waitKey(2000)
    # Tutup semua window
    cv2.destroyAllWindows()
    
    print("[INFO] Segmentation demo completed")


# Definisi function dengan nama dan parameter
def demo_performance_optimization():
    """
    Tips untuk mengoptimasi performa OpenCV DNN.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [OPTIMIZATION STRATEGIES]
    ─────────────────────────────────────────────────────────────────────
    
    1. BACKEND SELECTION
       ──────────────────
       
       # CPU (Default)
       net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
       net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
       
       # CUDA (NVIDIA GPU)
       net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
       net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
       
       # CUDA with FP16 (faster, slightly less accurate)
       net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
       net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
       
       # Intel OpenVINO
       net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
       net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # or MYRIAD, GPU
    
    2. INPUT SIZE REDUCTION
       ─────────────────────
       # Assignment - set nilai ke variabel
       - Smaller input = faster inference
       - Trade-off with accuracy
       
       # Instead of 640x640
       blob = cv2.dnn.blobFromImage(img, 1/255.0, (320, 320), ...)
    
    3. BATCH PROCESSING
       ──────────────────
       - Process multiple images at once
       
       # Konversi gambar ke blob untuk neural network
       blobs = cv2.dnn.blobFromImages(images, 1/255.0, (416, 416), ...)
       net.setInput(blobs)
       # Assignment - set nilai ke variabel
       outputs = net.forward()
    
    4. ASYNC INFERENCE
       ─────────────────
       # Start async inference
       net.setInput(blob)
       net.forwardAsync()
       
       # Do other work...
       
       # Wait for result
       outputs = net.forward()
    
    5. MODEL OPTIMIZATION
       ──────────────────
       - Use quantized models (INT8)
       - Use efficient architectures (MobileNet, EfficientNet)
       - Prune unnecessary layers
    
    
    [BENCHMARK COMPARISON]
    ─────────────────────────────────────────────────────────────────────
    
    # Load YOLOv8 model untuk object detection
    Model: YOLOv4-tiny (416x416)
    
    ┌─────────────────────────────┬────────────┬──────────┐
    │ Configuration               │ Time (ms)  │ FPS      │
    ├─────────────────────────────┼────────────┼──────────┤
    │ OpenCV CPU                  │ ~50        │ ~20      │
    │ OpenCV CUDA                 │ ~10        │ ~100     │
    │ OpenCV CUDA FP16            │ ~7         │ ~140     │
    │ OpenVINO (Intel i7)         │ ~15        │ ~65      │
    │ TensorRT (direct)           │ ~5         │ ~200     │
    └─────────────────────────────┴────────────┴──────────┘
    
    * Results vary based on hardware and OpenCV build
    """)
    
    # Check current capabilities
    print("\n[INFO] Checking current system capabilities...")
    check_opencv_dnn()
    
    # Benchmark if model available
    onnx_path = "simple_classifier.onnx"
    
    # Conditional statement - eksekusi jika kondisi True
    if os.path.exists(onnx_path):
        print(f"\n[INFO] Benchmarking with {onnx_path}...")
        
        # Blok try-except untuk error handling
        try:
            # Assignment - set nilai ke variabel
            net = cv2.dnn.readNetFromONNX(onnx_path)
            
            # Create test input
            test_blob = np.random.randn(1, 3, 64, 64).astype(np.float32)
            
            # Assignment - set nilai ke variabel
            backends = [
                (cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU, "OpenCV CPU"),
            ]
            
            # Try CUDA if available
            try:
                backends.append((cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA, "CUDA"))
            # Tangkap exception jika ada error di blok try
            except:
                pass
            
            # Iterasi/loop melalui elemen dalam koleksi
            for backend, target, name in backends:
                # Blok try-except untuk error handling
                try:
                    net.setPreferableBackend(backend)
                    net.setPreferableTarget(target)
                    net.setInput(test_blob)
                    
                    # Warmup
                    for _ in range(5):
                        net.forward()
                    
                    # Benchmark
                    times = []
                    # Iterasi/loop melalui elemen dalam koleksi
                    for _ in range(50):
                        # Assignment - set nilai ke variabel
                        start = time.time()
                        net.forward()
                        times.append(time.time() - start)
                    
                    # Hitung rata-rata dari array
                    avg_time = np.mean(times) * 1000
                    # Assignment - set nilai ke variabel
                    fps = 1000 / avg_time
                    
                    print(f"  {name}: {avg_time:.2f} ms ({fps:.1f} FPS)")
                    
                # Tangkap exception jika ada error di blok try
                except Exception as e:
                    print(f"  {name}: Not available - {e}")
                    
        # Tangkap exception jika ada error di blok try
        except Exception as e:
            print(f"[ERROR] Benchmark failed: {e}")


# Definisi function dengan nama dan parameter
def demo_realworld_pipeline():
    """
    Demonstrasi pipeline deployment real-world.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("REAL-WORLD DEPLOYMENT PIPELINE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [PRODUCTION DEPLOYMENT PIPELINE]
    ─────────────────────────────────────────────────────────────────────
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                    DEPLOYMENT ARCHITECTURE                      │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    │
    │  │ Input   │───►│ Preprocess│───►│ Inference│───►│ Post-   │    │
    │  │ Source  │    │           │    │ (OpenCV  │    │ process │    │
    │  │         │    │           │    │  DNN)    │    │         │    │
    │  └─────────┘    └──────────┘    └──────────┘    └─────────┘    │
    │       │                              │                │         │
    │       ▼                              ▼                ▼         │
    │  - Webcam                     - ONNX model     - NMS           │
    │  - Video file                 - TensorFlow     - Thresholding  │
    │  - Image stream               - Caffe          - Visualization │
    │  - Network stream             - Darknet                        │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
    
    
    [COMPLETE INFERENCE CLASS]
    ─────────────────────────────────────────────────────────────────────
    """)
    
    # Define inference class
    class OpenCVInference:
        """
        # Definisi class untuk membuat object
        Production-ready inference class using OpenCV DNN.
        """
        # Definisi function dengan nama dan parameter
        def __init__(self, model_path, input_size=(224, 224), 
                     # Assignment - set nilai ke variabel
                     mean=(0, 0, 0), scale=1/255.0, swap_rb=True):
            """
            Initialize the inference engine.
            
            Args:
                model_path: Path to ONNX/Caffe/TensorFlow model
                input_size: Input size (width, height)
                # Iterasi/loop melalui elemen dalam koleksi
                mean: Mean values for preprocessing
                # Iterasi/loop melalui elemen dalam koleksi
                scale: Scale factor for preprocessing
                swap_rb: Whether to swap R and B channels
            """
            # Assignment - set nilai ke variabel
            self.input_size = input_size
            # Assignment - set nilai ke variabel
            self.mean = mean
            # Assignment - set nilai ke variabel
            self.scale = scale
            # Assignment - set nilai ke variabel
            self.swap_rb = swap_rb
            
            # Load model
            if model_path.endswith('.onnx'):
                # Assignment - set nilai ke variabel
                self.net = cv2.dnn.readNetFromONNX(model_path)
            # Conditional statement - eksekusi jika kondisi True
            elif model_path.endswith('.caffemodel'):
                # Assignment - set nilai ke variabel
                prototxt = model_path.replace('.caffemodel', '.prototxt')
                # Baca model Caffe dari file .prototxt dan .caffemodel
                self.net = cv2.dnn.readNetFromCaffe(prototxt, model_path)
            else:
                raise ValueError(f"Unsupported model format: {model_path}")
            
            # Set backend
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            # Warmup
            dummy = np.zeros((input_size[1], input_size[0], 3), dtype=np.uint8)
            self.predict(dummy)
        
        # Definisi function dengan nama dan parameter
        def preprocess(self, image):
            """Preprocess image for inference."""
            # Konversi gambar ke blob untuk neural network
            blob = cv2.dnn.blobFromImage(
                image, 
                self.scale, 
                self.input_size,
                self.mean, 
                # Assignment - set nilai ke variabel
                swapRB=self.swap_rb, 
                # Assignment - set nilai ke variabel
                crop=False
            )
            # Return value dari function
            return blob
        
        # Definisi function dengan nama dan parameter
        def predict(self, image):
            """Run inference on image."""
            # Assignment - set nilai ke variabel
            blob = self.preprocess(image)
            self.net.setInput(blob)
            # Assignment - set nilai ke variabel
            output = self.net.forward()
            # Return value dari function
            return output
        
        # Definisi function dengan nama dan parameter
        def predict_batch(self, images):
            """Run inference on batch of images."""
            # Konversi gambar ke blob untuk neural network
            blobs = cv2.dnn.blobFromImages(
                images,
                self.scale,
                self.input_size,
                self.mean,
                # Assignment - set nilai ke variabel
                swapRB=self.swap_rb,
                # Assignment - set nilai ke variabel
                crop=False
            )
            self.net.setInput(blobs)
            # Assignment - set nilai ke variabel
            outputs = self.net.forward()
            # Return value dari function
            return outputs
        
        # Definisi function dengan nama dan parameter
        def benchmark(self, num_iterations=100):
            """Benchmark inference speed."""
            # Generate random integer dalam range tertentu
            dummy = np.random.randint(0, 255, 
                # Assignment - set nilai ke variabel
                (self.input_size[1], self.input_size[0], 3), dtype=np.uint8)
            
            # Warmup
            for _ in range(10):
                self.predict(dummy)
            
            # Benchmark
            times = []
            # Iterasi/loop melalui elemen dalam koleksi
            for _ in range(num_iterations):
                # Assignment - set nilai ke variabel
                start = time.time()
                self.predict(dummy)
                times.append(time.time() - start)
            
            # Return value dari function
            return {
                # Hitung rata-rata dari array
                'avg_ms': np.mean(times) * 1000,
                # Hitung standard deviation dari array
                'std_ms': np.std(times) * 1000,
                # Hitung rata-rata dari array
                'fps': 1 / np.mean(times)
            }
    
    print("""
    [USAGE EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    
    # Initialize
    inference = OpenCVInference(
        # Assignment - set nilai ke variabel
        model_path='model.onnx',
        # Assignment - set nilai ke variabel
        input_size=(224, 224),
        # Assignment - set nilai ke variabel
        mean=(0.485*255, 0.456*255, 0.406*255),
        # Assignment - set nilai ke variabel
        scale=1/255.0,
        # Assignment - set nilai ke variabel
        swap_rb=True
    )
    
    # Single image
    image = cv2.imread('test.jpg')
    # Assignment - set nilai ke variabel
    output = inference.predict(image)
    
    # Batch inference
    images = [cv2.imread(f'image_{i}.jpg') for i in range(4)]
    # Assignment - set nilai ke variabel
    outputs = inference.predict_batch(images)
    
    # Benchmark
    results = inference.benchmark(num_iterations=100)
    print(f"Average: {results['avg_ms']:.2f} ms")
    print(f"FPS: {results['fps']:.1f}")
    
    
    [VIDEO PROCESSING EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    cap = cv2.VideoCapture('video.mp4')
    
    # Loop berulang selama kondisi bernilai True
    while cap.isOpened():
        # Assignment - set nilai ke variabel
        ret, frame = cap.read()
        # Conditional statement - eksekusi jika kondisi True
        if not ret:
            break
        
        # Inference
        output = inference.predict(frame)
        
        # Post-process and visualize
        result = postprocess(output)
        visualize(frame, result)
        
        # Tampilkan gambar di window
        cv2.imshow('Detection', frame)
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:
            break
    
    cap.release()
    # Tutup semua window
    cv2.destroyAllWindows()
    """)
    
    # Demo if model available
    onnx_path = "simple_classifier.onnx"
    
    # Conditional statement - eksekusi jika kondisi True
    if os.path.exists(onnx_path):
        # Definisi class untuk membuat object
        print(f"\n[INFO] Testing OpenCVInference class with {onnx_path}...")
        
        # Blok try-except untuk error handling
        try:
            # Assignment - set nilai ke variabel
            inference = OpenCVInference(
                # Assignment - set nilai ke variabel
                model_path=onnx_path,
                # Assignment - set nilai ke variabel
                input_size=(64, 64),
                # Assignment - set nilai ke variabel
                mean=(0, 0, 0),
                # Assignment - set nilai ke variabel
                scale=1/255.0,
                # Assignment - set nilai ke variabel
                swap_rb=True
            )
            
            # Test single inference
            test_img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
            # Assignment - set nilai ke variabel
            output = inference.predict(test_img)
            print(f"[INFO] Output shape: {output.shape}")
            
            # Benchmark
            results = inference.benchmark(50)
            print(f"\n[BENCHMARK RESULTS]")
            print(f"  Average: {results['avg_ms']:.2f} ms")
            print(f"  Std Dev: {results['std_ms']:.2f} ms")
            print(f"  FPS: {results['fps']:.1f}")
            
        # Tangkap exception jika ada error di blok try
        except Exception as e:
            print(f"[ERROR] {e}")


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM OPENCV DNN DEPLOYMENT")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. OpenCV DNN Overview")
        print("2. Classification Inference")
        print("3. Object Detection Inference")
        print("4. Segmentation Inference")
        print("5. Performance Optimization")
        print("6. Real-World Pipeline")
        print("7. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-7): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_dnn_overview()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_classification_inference()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_detection_inference()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_segmentation_inference()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_performance_optimization()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_realworld_pipeline()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '7':
            demo_dnn_overview()
            demo_classification_inference()
            demo_detection_inference()
            demo_segmentation_inference()
            demo_performance_optimization()
            demo_realworld_pipeline()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
