"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 10 - INSTANCE SEGMENTATION
# Assignment - set nilai ke variabel
=============================================================================
Program ini mendemonstrasikan konsep dan implementasi instance segmentation
# Definisi class untuk membuat object
yang dapat membedakan instance berbeda dari class yang sama.

Konsep yang dipelajari:
1. Perbedaan semantic vs instance segmentation
2. Mask R-CNN architecture
# Load YOLOv8 model untuk object detection
3. YOLOv8-seg untuk instance segmentation
4. Panoptic segmentation overview
5. Visualisasi dan post-processing

Kebutuhan:
- ultralytics (pip install ultralytics)
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy
- matplotlib

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
import matplotlib.pyplot as plt
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

# Check PyTorch
TORCH_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import torch
    # Import library/module untuk digunakan
    import torchvision
    # Assignment - set nilai ke variabel
    TORCH_AVAILABLE = True
    print("[INFO] PyTorch tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] PyTorch tidak tersedia")


# Definisi function dengan nama dan parameter
def generate_random_color():
    """Generate random bright color untuk visualisasi."""
    # Generate random integer dalam range tertentu
    return tuple(np.random.randint(50, 255, 3).tolist())


# Definisi function dengan nama dan parameter
def demo_segmentation_types():
    """
    Demonstrasi perbedaan jenis segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("JENIS-JENIS SEGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [PERBANDINGAN SEGMENTATION TASKS]
    ─────────────────────────────────────────────────────────────────────
    
    1. SEMANTIC SEGMENTATION
       ─────────────────────
       - Klasifikasi setiap pixel ke dalam class
       - TIDAK membedakan instance berbeda
       # Definisi class untuk membuat object
       - Output: Single mask dengan class labels
       
       Contoh: Semua orang di gambar dilabel sebagai "person"
    
    2. INSTANCE SEGMENTATION
       ──────────────────────
       - Mendeteksi dan segmentasi setiap object instance
       # Definisi class untuk membuat object
       - MEMBEDAKAN instance berbeda dari class yang sama
       - Output: Multiple masks, satu per instance
       
       Contoh: Person 1, Person 2, Person 3 memiliki mask terpisah
    
    3. PANOPTIC SEGMENTATION
       ──────────────────────
       - Kombinasi semantic + instance segmentation
       - "Things" (countable objects): instance segmentation
       - "Stuff" (uncountable): semantic segmentation
       
       Contoh: Person 1, Person 2 (instance) + Sky, Road (semantic)
    
    
    [VISUAL COMPARISON]
    ─────────────────────────────────────────────────────────────────────
    
    Original Image:           [Person A] [Person B] [Car] [Tree] [Sky]
    
    Semantic Segmentation:    [PERSON  ] [PERSON  ] [CAR] [TREE] [SKY]
                              # Iterasi/loop melalui elemen dalam koleksi
                              (same color for all persons)
    
    Instance Segmentation:    [Person 1] [Person 2] [Car 1] [ignore stuff]
                              (different color per instance)
    
    Panoptic Segmentation:    [Person 1] [Person 2] [Car 1] [TREE] [SKY]
                              (instances + stuff classes)
    """)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Original image (simulated)
    img = np.ones((300, 400, 3), dtype=np.uint8) * 135  # Sky
    # Assignment - set nilai ke variabel
    img[200:, :] = [34, 139, 34]  # Ground (green)
    
    # Two persons
    cv2.rectangle(img, (50, 100), (120, 220), [100, 100, 200], -1)  # Person 1
    # Gambar persegi panjang pada gambar
    cv2.rectangle(img, (150, 110), (210, 210), [100, 100, 200], -1)  # Person 2
    # Car
    cv2.rectangle(img, (280, 150), (380, 210), [128, 128, 128], -1)  # Car
    
    # Konversi format warna (BGR ke RGB, dll)
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    # Semantic Segmentation
    semantic = np.zeros((300, 400, 3), dtype=np.uint8)
    # Assignment - set nilai ke variabel
    semantic[:, :] = [135, 206, 235]  # Sky (light blue)
    # Assignment - set nilai ke variabel
    semantic[200:, :] = [34, 139, 34]  # Ground
    # Assignment - set nilai ke variabel
    semantic[100:220, 50:120] = [192, 128, 128]  # Person class
    # Definisi class untuk membuat object
    semantic[110:210, 150:210] = [192, 128, 128]  # Person class (same color!)
    # Assignment - set nilai ke variabel
    semantic[150:210, 280:380] = [128, 128, 128]  # Car
    
    axes[0, 1].imshow(semantic)
    # Iterasi/loop melalui elemen dalam koleksi
    axes[0, 1].set_title('Semantic Segmentation\n(Same color for all persons)')
    axes[0, 1].axis('off')
    
    # Instance Segmentation
    instance = np.zeros((300, 400, 3), dtype=np.uint8)
    # Assignment - set nilai ke variabel
    instance[100:220, 50:120] = [255, 100, 100]  # Person 1 (red)
    # Assignment - set nilai ke variabel
    instance[110:210, 150:210] = [100, 255, 100]  # Person 2 (green - different!)
    # Assignment - set nilai ke variabel
    instance[150:210, 280:380] = [100, 100, 255]  # Car (blue)
    
    axes[1, 0].imshow(instance)
    axes[1, 0].set_title('Instance Segmentation\n(Different color per instance)')
    axes[1, 0].axis('off')
    
    # Panoptic Segmentation
    panoptic = np.zeros((300, 400, 3), dtype=np.uint8)
    # Assignment - set nilai ke variabel
    panoptic[:, :] = [135, 206, 235]  # Sky (stuff)
    # Assignment - set nilai ke variabel
    panoptic[200:, :] = [34, 139, 34]  # Ground (stuff)
    # Assignment - set nilai ke variabel
    panoptic[100:220, 50:120] = [255, 100, 100]  # Person 1 (thing)
    # Assignment - set nilai ke variabel
    panoptic[110:210, 150:210] = [100, 255, 100]  # Person 2 (thing)
    # Assignment - set nilai ke variabel
    panoptic[150:210, 280:380] = [100, 100, 255]  # Car (thing)
    
    axes[1, 1].imshow(panoptic)
    axes[1, 1].set_title('Panoptic Segmentation\n(Things + Stuff)')
    axes[1, 1].axis('off')
    
    # Atur spacing otomatis antar subplot
    plt.tight_layout()
    # Simpan figure ke file gambar
    plt.savefig('segmentation_types.png', dpi=150, bbox_inches='tight')
    # Tampilkan semua figure yang telah dibuat
    plt.show()
    
    print("\n[INFO] Visualisasi disimpan: segmentation_types.png")


# Definisi function dengan nama dan parameter
def demo_mask_rcnn_architecture():
    """
    Demonstrasi arsitektur Mask R-CNN.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("MASK R-CNN ARCHITECTURE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [MASK R-CNN OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    Mask R-CNN (He et al., 2017) adalah extension dari Faster R-CNN yang
    menambahkan branch untuk prediksi segmentation mask.
    
    
    [ARSITEKTUR]
    ─────────────────────────────────────────────────────────────────────
    
                          ┌─────────────────────────────────────┐
                          │           Input Image                │
                          └───────────────┬─────────────────────┘
                                          │
                          ┌───────────────▼─────────────────────┐
                          │      Backbone (ResNet + FPN)         │
                          │      → Feature Pyramid Network       │
                          └───────────────┬─────────────────────┘
                                          │
                          ┌───────────────▼─────────────────────┐
                          │    Region Proposal Network (RPN)     │
                          │    → Generate region proposals       │
                          └───────────────┬─────────────────────┘
                                          │
                          ┌───────────────▼─────────────────────┐
                          │       RoI Align (not RoI Pool!)      │
                          │    → Precise feature extraction      │
                          └───────────────┬─────────────────────┘
                                          │
               ┌──────────────────────────┼──────────────────────────┐
               │                          │                          │
    ┌──────────▼──────────┐   ┌──────────▼──────────┐   ┌──────────▼──────────┐
    │   Classification    │   │   Box Regression    │   │   Mask Prediction   │
    │   Branch            │   │   Branch            │   │   Branch            │
    │   → Class labels    │   │   → Bounding boxes  │   │   → Binary masks    │
    └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
    
    
    [KEY INNOVATIONS]
    ─────────────────────────────────────────────────────────────────────
    
    1. ROI ALIGN vs ROI POOLING
       ─────────────────────────
       RoI Pooling (Faster R-CNN):
       - Uses quantization (rounding)
       - Causes misalignment
       
       RoI Align (Mask R-CNN):
       - Uses bilinear interpolation
       - No quantization loss
       # Iterasi/loop melalui elemen dalam koleksi
       - Critical for accurate masks
    
    2. PARALLEL BRANCHES
       ──────────────────
       - Classification and bbox: same as Faster R-CNN
       - Mask branch: runs in parallel (not sequential)
       # Definisi class untuk membuat object
       - Mask untuk setiap class (binary mask per class)
    
    3. DECOUPLED MASK PREDICTION
       ──────────────────────────
       - Mask prediction TIDAK bergantung pada class
       # Definisi class untuk membuat object
       - Per-class binary mask instead of multi-class mask
       - Mengurangi competition antar classes
    
    
    [LOSS FUNCTION]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    L = L_cls + L_box + L_mask
    
    - L_cls: Classification loss (cross-entropy)
    - L_box: Bounding box regression loss (smooth L1)
    - L_mask: Binary cross-entropy untuk mask
    
    Mask loss hanya dihitung untuk ground-truth class.
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TORCH_AVAILABLE:
        # Blok try-except untuk error handling
        try:
            # Import library/module untuk digunakan
            from torchvision.models.detection import maskrcnn_resnet50_fpn
            
            print("\n[INFO] Loading Mask R-CNN ResNet50-FPN...")
            # Assignment - set nilai ke variabel
            model = maskrcnn_resnet50_fpn(pretrained=True)
            model.eval()
            
            # Count parameters
            total_params = sum(p.numel() for p in model.parameters())
            print(f"[INFO] Total parameters: {total_params:,}")
            
            # Test inference
            print("\n[INFO] Testing inference...")
            
            # Create test image
            test_img = np.zeros((480, 640, 3), dtype=np.uint8)
            # Assignment - set nilai ke variabel
            test_img[:, :] = [135, 206, 235]  # Sky
            # Assignment - set nilai ke variabel
            test_img[350:, :] = [34, 139, 34]  # Ground
            
            # Add objects
            cv2.rectangle(test_img, (100, 200), (200, 380), [100, 100, 200], -1)  # Person
            # Gambar persegi panjang pada gambar
            cv2.rectangle(test_img, (400, 250), (580, 370), [128, 128, 128], -1)  # Car
            
            # Convert to tensor
            img_tensor = torch.from_numpy(test_img).permute(2, 0, 1).float() / 255.0
            
            # Inference
            with torch.no_grad():
                # Assignment - set nilai ke variabel
                start = time.time()
                # Assignment - set nilai ke variabel
                predictions = model([img_tensor])
                # Assignment - set nilai ke variabel
                inference_time = time.time() - start
            
            print(f"[INFO] Inference time: {inference_time*1000:.2f} ms")
            
            # Process predictions
            pred = predictions[0]
            print(f"\n[INFO] Detections found: {len(pred['boxes'])}")
            
            # Get COCO class names (partial list)
            COCO_CLASSES = {
                0: 'background', 1: 'person', 2: 'bicycle', 3: 'car',
                4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train'
            }
            
            # Visualize
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            # Konversi format warna (BGR ke RGB, dll)
            axes[0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
            axes[0].set_title('Input Image')
            axes[0].axis('off')
            
            # Draw detections
            output_img = test_img.copy()
            # Buat array numpy penuh dengan nilai 0
            mask_overlay = np.zeros_like(test_img)
            
            # Iterasi/loop melalui elemen dalam koleksi
            for i in range(len(pred['boxes'])):
                # Assignment - set nilai ke variabel
                score = pred['scores'][i].item()
                # Conditional statement - eksekusi jika kondisi True
                if score < 0.5:
                    continue
                
                # Box
                box = pred['boxes'][i].cpu().numpy().astype(int)
                # Assignment - set nilai ke variabel
                label = pred['labels'][i].item()
                # Assignment - set nilai ke variabel
                mask = pred['masks'][i, 0].cpu().numpy()
                
                # Color
                color = generate_random_color()
                
                # Draw box
                cv2.rectangle(output_img, (box[0], box[1]), (box[2], box[3]), color, 2)
                
                # Apply mask
                mask_binary = (mask > 0.5).astype(np.uint8)
                # Assignment - set nilai ke variabel
                mask_overlay[mask_binary == 1] = color
                
                # Assignment - set nilai ke variabel
                class_name = COCO_CLASSES.get(label, f'class_{label}')
                # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
                cv2.putText(output_img, f"{class_name}: {score:.2f}",
                           (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Konversi format warna (BGR ke RGB, dll)
            axes[1].imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
            axes[1].set_title('Detection Boxes')
            axes[1].axis('off')
            
            # Combined mask overlay
            combined = cv2.addWeighted(test_img, 0.6, mask_overlay, 0.4, 0)
            # Konversi format warna (BGR ke RGB, dll)
            axes[2].imshow(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
            axes[2].set_title('Instance Masks')
            axes[2].axis('off')
            
            # Atur spacing otomatis antar subplot
            plt.tight_layout()
            # Simpan figure ke file gambar
            plt.savefig('mask_rcnn_result.png', dpi=150, bbox_inches='tight')
            # Tampilkan semua figure yang telah dibuat
            plt.show()
            
        # Tangkap exception jika ada error di blok try
        except Exception as e:
            print(f"[ERROR] {e}")
            # Assignment - set nilai ke variabel
            print("[INFO] Mask R-CNN demo requires torchvision >= 0.8.0")
    else:
        print("\n[SIMULATION MODE] Mask R-CNN architecture explained.")


# Definisi function dengan nama dan parameter
def demo_yolov8_segmentation():
    """
    # Load YOLOv8 model untuk object detection
    Demonstrasi YOLOv8-seg untuk instance segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    # Load YOLOv8 model untuk object detection
    print("YOLOV8 INSTANCE SEGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    # Load YOLOv8 model untuk object detection
    [YOLOV8-SEG OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    # Load YOLOv8 model untuk object detection
    YOLOv8-seg menambahkan segmentation head ke arsitektur YOLOv8 untuk
    real-time instance segmentation.
    
    
    [ARSITEKTUR]
    ─────────────────────────────────────────────────────────────────────
    
    Input → Backbone (CSPDarknet) → Neck (PANet) → Detection Head
                                                 → Segmentation Head
    
    Detection Head: boxes + classes + confidence
    Segmentation Head: mask coefficients → combined with prototype masks
    
    
    [MODEL VARIANTS]
    ─────────────────────────────────────────────────────────────────────
    
    ┌──────────────┬─────────┬──────────┬─────────────┬──────────────┐
    │ Model        │ Params  │ FLOPs    │ Box mAP50-95│ Mask mAP50-95│
    ├──────────────┼─────────┼──────────┼─────────────┼──────────────┤
    # Load YOLOv8 model untuk object detection
    │ YOLOv8n-seg  │ 3.4M    │ 12.6G    │ 36.7        │ 30.5         │
    # Load YOLOv8 model untuk object detection
    │ YOLOv8s-seg  │ 11.8M   │ 42.6G    │ 44.6        │ 36.8         │
    # Load YOLOv8 model untuk object detection
    │ YOLOv8m-seg  │ 27.3M   │ 110.2G   │ 49.9        │ 40.8         │
    # Load YOLOv8 model untuk object detection
    │ YOLOv8l-seg  │ 46.0M   │ 220.5G   │ 52.3        │ 42.6         │
    # Load YOLOv8 model untuk object detection
    │ YOLOv8x-seg  │ 71.8M   │ 344.1G   │ 53.4        │ 43.4         │
    └──────────────┴─────────┴──────────┴─────────────┴──────────────┘
    
    * Evaluated on COCO val2017
    
    
    [PENGGUNAAN]
    ─────────────────────────────────────────────────────────────────────
    
    # Load YOLOv8 model untuk object detection
    from ultralytics import YOLO
    
    # Load model
    model = YOLO('yolov8n-seg.pt')
    
    # Inference
    results = model(image)
    
    # Access results
    for result in results:
        # Assignment - set nilai ke variabel
        boxes = result.boxes        # Detection boxes
        # Assignment - set nilai ke variabel
        masks = result.masks        # Segmentation masks
        
        # Mask data
        if masks is not None:
            # Assignment - set nilai ke variabel
            mask_data = masks.data  # Tensor of masks
            # Assignment - set nilai ke variabel
            xy = masks.xy           # Polygon coordinates
    """)
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE:
        # Load YOLOv8 model untuk object detection
        print("\n[INFO] Loading YOLOv8n-seg model...")
        
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n-seg.pt')
        
        # Create test image
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        test_img[:, :] = [200, 200, 200]  # Gray background
        # Assignment - set nilai ke variabel
        test_img[350:, :] = [100, 150, 100]  # Ground
        
        # Add objects (simple shapes)
        cv2.rectangle(test_img, (80, 150), (180, 380), [150, 100, 100], -1)  # Person-like
        # Gambar persegi panjang pada gambar
        cv2.rectangle(test_img, (300, 200), (500, 350), [100, 100, 150], -1)  # Car-like
        cv2.ellipse(test_img, (550, 150), (50, 80), 0, 0, 360, [150, 150, 100], -1)  # Ball
        
        # Run inference
        print("[INFO] Running inference...")
        # Assignment - set nilai ke variabel
        results = model(test_img, verbose=False)
        
        # Process results
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Konversi format warna (BGR ke RGB, dll)
        axes[0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        # Draw masks
        mask_overlay = test_img.copy()
        
        # Iterasi/loop melalui elemen dalam koleksi
        for result in results:
            # Conditional statement - eksekusi jika kondisi True
            if result.masks is not None:
                print(f"[INFO] Detected {len(result.masks)} instances")
                
                # Iterasi/loop melalui elemen dalam koleksi
                for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
                    # Get mask
                    mask_np = mask.cpu().numpy()
                    # Ubah ukuran gambar ke resolusi baru
                    mask_resized = cv2.resize(mask_np, (640, 480))
                    
                    # Generate color
                    color = generate_random_color()
                    
                    # Apply mask
                    mask_binary = (mask_resized > 0.5).astype(np.uint8)
                    # Iterasi/loop melalui elemen dalam koleksi
                    for c in range(3):
                        # Cari index dimana kondisi bernilai True
                        mask_overlay[:, :, c] = np.where(
                            # Assignment - set nilai ke variabel
                            mask_binary == 1,
                            mask_overlay[:, :, c] * 0.5 + color[c] * 0.5,
                            mask_overlay[:, :, c]
                        )
                    
                    # Draw box
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    # Assignment - set nilai ke variabel
                    cls = int(box.cls[0])
                    # Assignment - set nilai ke variabel
                    conf = float(box.conf[0])
                    
                    # Gambar persegi panjang pada gambar
                    cv2.rectangle(mask_overlay, (xyxy[0], xyxy[1]), 
                                 (xyxy[2], xyxy[3]), color, 2)
                    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
                    cv2.putText(mask_overlay, f"{model.names[cls]}: {conf:.2f}",
                               (xyxy[0], xyxy[1]-10), cv2.FONT_HERSHEY_SIMPLEX,
                               0.5, color, 2)
            else:
                print("[INFO] No instances detected (may need real image)")
        
        # Konversi format warna (BGR ke RGB, dll)
        axes[1].imshow(cv2.cvtColor(mask_overlay, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Instance Segmentation')
        axes[1].axis('off')
        
        # Plot segmentation result from model
        annotated = results[0].plot()
        # Konversi format warna (BGR ke RGB, dll)
        axes[2].imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        # Load YOLOv8 model untuk object detection
        axes[2].set_title('YOLOv8-seg Output')
        axes[2].axis('off')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('yolov8_seg_result.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()
        
    else:
        # Simulation
        print("\n[SIMULATION MODE]")
        # Load YOLOv8 model untuk object detection
        print("Simulating YOLOv8-seg output...")
        
        # Create simulated results
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        test_img[:, :] = [200, 200, 200]
        
        # Simulated detections
        detections = [
            {'class': 'person', 'box': [80, 150, 180, 380], 'conf': 0.89, 
             # Buat array numpy penuh dengan nilai 0
             'mask': np.zeros((480, 640), dtype=np.uint8)},
            {'class': 'car', 'box': [300, 200, 500, 350], 'conf': 0.92,
             # Buat array numpy penuh dengan nilai 0
             'mask': np.zeros((480, 640), dtype=np.uint8)},
        ]
        
        # Create masks
        detections[0]['mask'][150:380, 80:180] = 1
        # Assignment - set nilai ke variabel
        detections[1]['mask'][200:350, 300:500] = 1
        
        # Visualize
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        axes[0].imshow(test_img)
        axes[0].set_title('Input Image (Synthetic)')
        axes[0].axis('off')
        
        # Draw masks with different colors
        mask_overlay = test_img.copy()
        # Assignment - set nilai ke variabel
        colors = [(255, 100, 100), (100, 255, 100)]
        
        # Iterasi/loop melalui elemen dalam koleksi
        for det, color in zip(detections, colors):
            # Assignment - set nilai ke variabel
            mask = det['mask']
            # Iterasi/loop melalui elemen dalam koleksi
            for c in range(3):
                # Cari index dimana kondisi bernilai True
                mask_overlay[:, :, c] = np.where(
                    # Assignment - set nilai ke variabel
                    mask == 1,
                    mask_overlay[:, :, c] * 0.5 + color[c] * 0.5,
                    mask_overlay[:, :, c]
                ).astype(np.uint8)
            
            # Assignment - set nilai ke variabel
            box = det['box']
            # Gambar persegi panjang pada gambar
            cv2.rectangle(mask_overlay, (box[0], box[1]), (box[2], box[3]), color, 2)
        
        axes[1].imshow(mask_overlay)
        axes[1].set_title('Instance Segmentation (Simulated)')
        axes[1].axis('off')
        
        # All masks
        all_masks = np.zeros((480, 640, 3), dtype=np.uint8)
        # Iterasi/loop melalui elemen dalam koleksi
        for det, color in zip(detections, colors):
            # Assignment - set nilai ke variabel
            mask = det['mask']
            # Assignment - set nilai ke variabel
            all_masks[mask == 1] = color
        
        axes[2].imshow(all_masks)
        axes[2].set_title('Instance Masks')
        axes[2].axis('off')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('yolov8_seg_simulated.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()


# Definisi function dengan nama dan parameter
def demo_mask_post_processing():
    """
    Demonstrasi post-processing untuk instance segmentation masks.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("MASK POST-PROCESSING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [POST-PROCESSING TECHNIQUES]
    ─────────────────────────────────────────────────────────────────────
    
    1. THRESHOLDING
       - Convert soft mask to binary mask
       - Typical threshold: 0.5
       
    2. MORPHOLOGICAL OPERATIONS
       - Erosion: Remove small protrusions
       - Dilation: Fill small holes
       - Opening: Erosion → Dilation
       - Closing: Dilation → Erosion
    
    3. CONNECTED COMPONENT ANALYSIS
       - Remove small disconnected regions
       - Keep largest connected component
    
    4. BOUNDARY REFINEMENT
       - CRF (Conditional Random Field)
       - GrabCut
       - Bilateral filtering
    
    5. POLYGON SIMPLIFICATION
       - Douglas-Peucker algorithm
       - Reduce number of polygon points
    """)
    
    # Create example mask with noise
    np.random.seed(42)
    
    # Create base mask
    mask = np.zeros((300, 400), dtype=np.float32)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(mask, (100, 50), (300, 250), 1.0, -1)
    
    # Add soft edges (simulating network output)
    mask = cv2.GaussianBlur(mask, (21, 21), 5)
    
    # Add noise
    noise = np.random.random((300, 400)).astype(np.float32) * 0.3
    # Batasi nilai array antara min dan max
    noisy_mask = np.clip(mask + noise - 0.15, 0, 1)
    
    # Buat subplot di grid figure
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Original soft mask
    axes[0, 0].imshow(noisy_mask, cmap='gray')
    axes[0, 0].set_title('Soft Mask (Network Output)')
    axes[0, 0].axis('off')
    
    # Thresholding
    thresh_mask = (noisy_mask > 0.5).astype(np.uint8)
    # Assignment - set nilai ke variabel
    axes[0, 1].imshow(thresh_mask, cmap='gray')
    axes[0, 1].set_title('After Thresholding (> 0.5)')
    axes[0, 1].axis('off')
    
    # Opening (remove noise)
    kernel = np.ones((5, 5), np.uint8)
    # Operasi morfologi (erosi, dilasi, opening, closing)
    opened_mask = cv2.morphologyEx(thresh_mask, cv2.MORPH_OPEN, kernel)
    # Assignment - set nilai ke variabel
    axes[0, 2].imshow(opened_mask, cmap='gray')
    axes[0, 2].set_title('After Opening')
    axes[0, 2].axis('off')
    
    # Closing (fill holes)
    closed_mask = cv2.morphologyEx(opened_mask, cv2.MORPH_CLOSE, kernel)
    # Assignment - set nilai ke variabel
    axes[0, 3].imshow(closed_mask, cmap='gray')
    axes[0, 3].set_title('After Closing')
    axes[0, 3].axis('off')
    
    # Connected components - keep largest
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed_mask)
    
    # Conditional statement - eksekusi jika kondisi True
    if num_labels > 1:
        # Find largest component (excluding background)
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        # Assignment - set nilai ke variabel
        largest_mask = (labels == largest_label).astype(np.uint8)
    else:
        # Assignment - set nilai ke variabel
        largest_mask = closed_mask
    
    # Assignment - set nilai ke variabel
    axes[1, 0].imshow(largest_mask, cmap='gray')
    axes[1, 0].set_title('Largest Connected Component')
    axes[1, 0].axis('off')
    
    # Contour extraction
    contours, _ = cv2.findContours(largest_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Buat array numpy penuh dengan nilai 0
    contour_img = np.zeros((300, 400, 3), dtype=np.uint8)
    # Gambar outline kontur pada gambar
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    axes[1, 1].imshow(contour_img)
    axes[1, 1].set_title('Contour Extraction')
    axes[1, 1].axis('off')
    
    # Polygon simplification
    simplified_img = np.zeros((300, 400, 3), dtype=np.uint8)
    # Iterasi/loop melalui elemen dalam koleksi
    for contour in contours:
        # Assignment - set nilai ke variabel
        epsilon = 0.02 * cv2.arcLength(contour, True)
        # Assignment - set nilai ke variabel
        simplified = cv2.approxPolyDP(contour, epsilon, True)
        # Gambar outline kontur pada gambar
        cv2.drawContours(simplified_img, [simplified], -1, (255, 0, 0), 2)
        
        # Show original for comparison
        cv2.drawContours(simplified_img, [contour], -1, (0, 255, 0), 1)
    
    axes[1, 2].imshow(simplified_img)
    axes[1, 2].set_title('Polygon Simplification\n(Green: original, Blue: simplified)')
    axes[1, 2].axis('off')
    
    # Final result
    final_img = np.zeros((300, 400, 3), dtype=np.uint8)
    # Assignment - set nilai ke variabel
    final_img[:, :] = [200, 200, 200]
    # Assignment - set nilai ke variabel
    final_img[largest_mask == 1] = [100, 200, 100]
    # Gambar outline kontur pada gambar
    cv2.drawContours(final_img, contours, -1, (0, 100, 0), 2)
    
    axes[1, 3].imshow(final_img)
    axes[1, 3].set_title('Final Refined Mask')
    axes[1, 3].axis('off')
    
    # Atur spacing otomatis antar subplot
    plt.tight_layout()
    # Simpan figure ke file gambar
    plt.savefig('mask_post_processing.png', dpi=150, bbox_inches='tight')
    # Tampilkan semua figure yang telah dibuat
    plt.show()
    
    # Print statistics
    print("\n[PROCESSING STATISTICS]")
    print(f"Original noisy mask pixels > 0.5: {(noisy_mask > 0.5).sum()}")
    print(f"After thresholding: {thresh_mask.sum()}")
    print(f"After opening: {opened_mask.sum()}")
    print(f"After closing: {closed_mask.sum()}")
    print(f"Largest component: {largest_mask.sum()}")
    # Conditional statement - eksekusi jika kondisi True
    if len(contours) > 0:
        print(f"Contour points: {len(contours[0])}")
        # Assignment - set nilai ke variabel
        epsilon = 0.02 * cv2.arcLength(contours[0], True)
        # Assignment - set nilai ke variabel
        simplified = cv2.approxPolyDP(contours[0], epsilon, True)
        print(f"Simplified polygon points: {len(simplified)}")


# Definisi function dengan nama dan parameter
def demo_instance_segmentation_metrics():
    """
    Demonstrasi metrics untuk evaluasi instance segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("INSTANCE SEGMENTATION METRICS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [EVALUATION METRICS]
    ─────────────────────────────────────────────────────────────────────
    
    1. MASK AP (Average Precision)
       ────────────────────────────
       # Assignment - set nilai ke variabel
       - AP@[IoU=0.50:0.95] - primary metric
       - AP@50 - at 50% IoU threshold
       - AP@75 - at 75% IoU threshold
       
       IoU dihitung untuk MASK, bukan hanya box!
    
    2. AP BY SIZE
       ───────────
       - AP_small: objects < 32×32 pixels
       - AP_medium: 32×32 to 96×96 pixels  
       - AP_large: objects > 96×96 pixels
    
    3. AR (Average Recall)
       ─────────────────────
       - AR@1: max 1 detection per image
       - AR@10: max 10 detections per image
       - AR@100: max 100 detections per image
    
    
    [MASK IOU CALCULATION]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    Mask IoU = (Mask_pred ∩ Mask_gt) / (Mask_pred ∪ Mask_gt)
    
    Dimana ∩ dan ∪ adalah operasi pixel-wise intersection dan union.
    
    
    [COCO EVALUATION]
    ─────────────────────────────────────────────────────────────────────
    
    COCO menggunakan 10 IoU thresholds:
    [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    
    # Assignment - set nilai ke variabel
    Final AP = Average over all thresholds and all classes
    """)
    
    # Definisi function dengan nama dan parameter
    def compute_mask_iou(mask1, mask2):
        """Compute IoU between two binary masks."""
        # Assignment - set nilai ke variabel
        intersection = np.logical_and(mask1, mask2).sum()
        # Assignment - set nilai ke variabel
        union = np.logical_or(mask1, mask2).sum()
        # Conditional statement - eksekusi jika kondisi True
        if union == 0:
            # Return value dari function
            return 0
        # Return value dari function
        return intersection / union
    
    # Create example masks
    gt_mask = np.zeros((200, 200), dtype=np.uint8)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(gt_mask, (50, 50), (150, 150), 1, -1)
    
    # Prediction 1: Good overlap
    pred_mask1 = np.zeros((200, 200), dtype=np.uint8)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(pred_mask1, (55, 55), (155, 155), 1, -1)
    
    # Prediction 2: Medium overlap
    pred_mask2 = np.zeros((200, 200), dtype=np.uint8)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(pred_mask2, (70, 70), (170, 170), 1, -1)
    
    # Prediction 3: Poor overlap
    pred_mask3 = np.zeros((200, 200), dtype=np.uint8)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(pred_mask3, (100, 100), (190, 190), 1, -1)
    
    # Assignment - set nilai ke variabel
    predictions = [
        ('Prediction 1', pred_mask1),
        ('Prediction 2', pred_mask2),
        ('Prediction 3', pred_mask3)
    ]
    
    print("\n[MASK IoU EXAMPLES]")
    
    # Buat subplot di grid figure
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # Ground truth
    axes[0, 0].imshow(gt_mask, cmap='Blues')
    axes[0, 0].set_title('Ground Truth')
    axes[0, 0].axis('off')
    
    # Assignment - set nilai ke variabel
    ious = []
    # Iterasi/loop melalui elemen dalam koleksi
    for i, (name, pred_mask) in enumerate(predictions):
        # Assignment - set nilai ke variabel
        iou = compute_mask_iou(gt_mask, pred_mask)
        ious.append(iou)
        # Assignment - set nilai ke variabel
        print(f"  {name}: IoU = {iou:.4f}")
        
        # Show prediction
        axes[0, i+1].imshow(pred_mask, cmap='Reds')
        axes[0, i+1].set_title(f'{name}')
        axes[0, i+1].axis('off')
        
        # Show overlap
        overlap = np.zeros((200, 200, 3), dtype=np.uint8)
        # Iterasi/loop melalui elemen dalam koleksi
        overlap[gt_mask == 1] = [0, 0, 255]  # Blue for GT
        # Iterasi/loop melalui elemen dalam koleksi
        overlap[pred_mask == 1] = [255, 0, 0]  # Red for pred
        # Iterasi/loop melalui elemen dalam koleksi
        overlap[np.logical_and(gt_mask, pred_mask)] = [0, 255, 0]  # Green for overlap
        
        axes[1, i].imshow(overlap)
        # Assignment - set nilai ke variabel
        axes[1, i].set_title(f'Overlap (IoU={iou:.2f})\nBlue=GT, Red=Pred, Green=Overlap')
        axes[1, i].axis('off')
    
    # IoU bar chart
    axes[1, 3].bar(['Pred 1', 'Pred 2', 'Pred 3'], ious, color=['green', 'orange', 'red'])
    # Assignment - set nilai ke variabel
    axes[1, 3].axhline(y=0.5, color='black', linestyle='--', label='IoU=0.5')
    # Assignment - set nilai ke variabel
    axes[1, 3].axhline(y=0.75, color='gray', linestyle='--', label='IoU=0.75')
    axes[1, 3].set_ylabel('IoU')
    axes[1, 3].set_title('Mask IoU Comparison')
    axes[1, 3].legend()
    axes[1, 3].set_ylim(0, 1)
    
    # Atur spacing otomatis antar subplot
    plt.tight_layout()
    # Simpan figure ke file gambar
    plt.savefig('instance_seg_metrics.png', dpi=150, bbox_inches='tight')
    # Tampilkan semua figure yang telah dibuat
    plt.show()
    
    # AP calculation example
    print("\n[AP CALCULATION EXAMPLE]")
    print("─" * 50)
    
    # Simulated precision-recall values at different IoU thresholds
    iou_thresholds = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    # Assignment - set nilai ke variabel
    ap_per_threshold = [0.85, 0.83, 0.80, 0.76, 0.71, 0.65, 0.55, 0.42, 0.25, 0.10]
    
    print("IoU Threshold | AP")
    print("-" * 25)
    # Iterasi/loop melalui elemen dalam koleksi
    for iou, ap in zip(iou_thresholds, ap_per_threshold):
        print(f"    {iou:.2f}      | {ap:.2f}")
    
    # Hitung rata-rata dari array
    mean_ap = np.mean(ap_per_threshold)
    print("-" * 25)
    print(f"  AP@[.50:.95] | {mean_ap:.2f}")


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM INSTANCE SEGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Jenis-jenis Segmentation")
        print("2. Mask R-CNN Architecture")
        # Load YOLOv8 model untuk object detection
        print("3. YOLOv8 Instance Segmentation")
        print("4. Mask Post-Processing")
        print("5. Instance Segmentation Metrics")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-6): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_segmentation_types()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_mask_rcnn_architecture()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_yolov8_segmentation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_mask_post_processing()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_instance_segmentation_metrics()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_segmentation_types()
            demo_mask_rcnn_architecture()
            demo_yolov8_segmentation()
            demo_mask_post_processing()
            demo_instance_segmentation_metrics()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
