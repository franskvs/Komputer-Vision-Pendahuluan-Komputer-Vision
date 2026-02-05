# JOBSHEET BAB 5: DEEP LEARNING UNTUK COMPUTER VISION

## Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Topik**: Deep Learning untuk Computer Vision
- **Durasi Modul**: 6 × 150 menit (6 pertemuan @ 2.5 jam)
- **Total Waktu**: 900 menit (15 jam)
- **Tools**: Python 3.8+, PyTorch/TensorFlow, OpenCV 4.5+, Ultralytics YOLO
- **Hardware**: CPU (minimal), GPU CUDA-capable (recommended untuk training)
- **RAM**: Minimal 8GB (16GB recommended untuk training)

---

## Pertemuan 1: Dasar-dasar Neural Network dengan OpenCV DNN

### Tujuan
1. Memahami OpenCV DNN module
2. Menjalankan pre-trained model untuk image classification
3. Memahami blob preprocessing

### Alat dan Bahan
- PC dengan Python 3.8+
- Library: opencv-python, numpy, matplotlib
- Pre-trained models: MobileNet, ResNet

### Teori Singkat

OpenCV DNN module memungkinkan inference menggunakan model dari berbagai frameworks tanpa dependency tambahan.

**Supported Frameworks:**
```
├── Caffe (.caffemodel, .prototxt)        # Berkeley framework
├── TensorFlow (.pb, .pbtxt)              # Google framework
├── PyTorch/Torch (.t7, .pth)             # Meta/Facebook framework
├── Darknet/YOLO (.weights, .cfg)         # YOLO original
├── ONNX (.onnx)                          # Open Neural Network Exchange
└── OpenVINO (.xml, .bin)                 # Intel optimization
```

**Keunggulan OpenCV DNN:**
- No framework dependency (pure OpenCV)
- Lightweight dan portable
- CPU-optimized dengan Intel optimizations
- Support multiple backends (OpenVINO, Vulkan, CUDA)
- Cocok untuk deployment production

**Blob Preprocessing:**
```python
blob = cv2.dnn.blobFromImage(
    image,           # Input image (BGR format dari OpenCV)
    scalefactor,     # Scale (1/255.0 untuk [0,1], 1.0 untuk [0,255])
    size,            # Network input size (224, 224) atau (300, 300)
    mean,            # Mean subtraction (103.939, 116.779, 123.68) untuk ImageNet
    swapRB,          # BGR to RGB (True jika model trained dengan RGB)
    crop,            # Center crop (True) atau resize (False)
    ddepth           # Output depth (cv2.CV_32F default)
)
```

**Penjelasan Detail:**
- **scalefactor**: Mengubah range nilai pixel
  - 1/255.0 → normalize ke [0, 1]
  - 0.00392 → sama dengan 1/255.0
  - 1.0 → tetap di [0, 255]
- **mean**: Mean subtraction untuk normalisasi
  - ImageNet mean: (103.939, 116.779, 123.68) BGR
  - Atau (0.485, 0.456, 0.406) RGB normalized
- **swapRB**: OpenCV default BGR, model biasanya RGB
- **crop**: True = crop center, False = resize/warp

**Output Blob Format:**
`[batch, channels, height, width]` atau `[N, C, H, W]`
Contoh: `[1, 3, 224, 224]` untuk 1 gambar RGB 224x224

### Langkah Praktikum

#### Praktikum 1.1: Image Classification dengan MobileNet
```
File: praktikum/01_opencv_dnn_classification.py
```

**Langkah Eksperimen:**
1. **Setup dan Load Model**
   - Download MobileNet model dari OpenCV model zoo
   - Load model dengan `cv2.dnn.readNetFromCaffe()`
   - Load ImageNet class labels (1000 classes)

2. **Inference pada Single Image**
   - Load test image (gunakan gambar kucing/anjing/mobil)
   - Create blob dengan parameter yang tepat
   - Forward pass melalui network
   - Parse output dan ambil top-5 predictions

3. **Visualisasi Hasil**
   - Tampilkan gambar dengan predicted class
   - Show confidence scores untuk top-5 classes
   - Bandingkan dengan ground truth

**Expected Output:**
```
Image: cat.jpg
Predictions:
1. tabby cat (82.3%)
2. tiger cat (12.1%)
3. Egyptian cat (3.4%)
4. lynx (1.2%)
5. Persian cat (0.8%)
Inference time: 23.5 ms
```

**Troubleshooting:**
- Jika akurasi rendah, cek parameter mean dan swapRB
- Jika inference lambat, pastikan menggunakan CPU backend
- Jika error "cannot find model", verify path model

#### Praktikum 1.2: Model Comparison
```
File: praktikum/02_model_comparison.py
```

**Objective:** Membandingkan trade-off antara accuracy dan speed

**Models untuk Comparison:**
| Model | Size | Params | Expected Accuracy |
|-------|------|--------|-------------------|
| MobileNet-V2 | 14 MB | 3.5M | 72% Top-1 |
| ResNet-50 | 102 MB | 25M | 76% Top-1 |
| EfficientNet-B0 | 21 MB | 5.3M | 77% Top-1 |

**Metrics yang Diukur:**
1. **Inference Time**
   - Average over 100 runs
   - Exclude first run (warm-up)
   - Report in milliseconds

2. **Accuracy**
   - Test pada ImageNet validation subset (50 images)
   - Calculate Top-1 dan Top-5 accuracy

3. **Memory Usage**
   - Model file size
   - Runtime memory (measure dengan psutil)

**Analisis Expected:**
- MobileNet: fastest, reasonable accuracy
- ResNet: slower, higher accuracy
- Trade-off: 2-3x slower untuk ~4% accuracy gain

**Buat Tabel Hasil:**
```
| Model | Size | Time (ms) | Top-1 | Top-5 | FPS |
|-------|------|-----------|-------|-------|-----|
| ...   | ...  | ...       | ...   | ...   | ... |
```

### Latihan
1. Download dan test model ONNX lain
2. Buat wrapper function untuk berbagai model
3. Test dengan batch processing

### Tugas Mandiri (Dikumpulkan Pertemuan 2)

**Tugas 1.1: Model Benchmark Report**

Benchmark minimal 3 model berbeda dengan requirements:

**Models yang Disarankan:**
- MobileNet-V2 (lightweight)
- ResNet-50 (balanced)
- EfficientNet-B0 (efficient)

**Dataset Test:**
- Minimal 100 images dari ImageNet validation
- Balanced across 10 different classes
- Include challenging cases (occlusion, blur, small object)

**Metrics yang Harus Dilaporkan:**
1. Model size (MB)
2. Inference time (mean ± std)
3. Top-1 accuracy (%)
4. Top-5 accuracy (%)
5. Memory footprint (MB)
6. FPS throughput

**Format Laporan:**
```markdown
# Model Benchmark Report

## Executive Summary
- Best model untuk accuracy: ...
- Best model untuk speed: ...
- Recommended untuk production: ...

## Detailed Results
### MobileNet-V2
- Accuracy: XX%
- Speed: YY ms
- Analysis: ...

[Include graphs: accuracy vs speed plot]

## Conclusion
- Trade-off analysis
- Use case recommendations
```

**Deliverables:**
- `benchmark_report.pdf` (3-5 halaman)
- `benchmark_results.csv` (raw data)
- `comparison_plots.png` (visualization)

**Grading Criteria:**
- Completeness: 40%
- Analysis depth: 30%
- Visualization: 20%
- Writing quality: 10%

---

## Pertemuan 2: Convolutional Neural Network dari Scratch

### Tujuan
1. Memahami arsitektur CNN
2. Membangun CNN sederhana dengan PyTorch/Keras
3. Training pada MNIST/CIFAR-10

### Alat dan Bahan
- Library: torch, torchvision atau tensorflow, keras
- Dataset: MNIST, CIFAR-10

### Teori Singkat

**CNN Architecture Components:**
```
Input (28×28×1 untuk MNIST)
    ↓
Conv2D(32, 3×3) + ReLU    # 32 filters, 3×3 kernel
    ↓
MaxPool2D(2×2)             # Reduce spatial size
    ↓
Conv2D(64, 3×3) + ReLU
    ↓
MaxPool2D(2×2)
    ↓
Flatten()                  # 2D → 1D
    ↓
Dense(128) + ReLU         # Fully connected
    ↓
Dense(10) + Softmax       # 10 classes
```

**Training Loop:**
```python
for epoch in range(epochs):
    for batch in dataloader:
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### Langkah Praktikum

#### Praktikum 2.1: CNN dengan PyTorch
```
File: praktikum/03_cnn_pytorch.py
```
1. Definisikan arsitektur CNN
2. Training pada MNIST
3. Evaluasi dengan test set

#### Praktikum 2.2: CNN dengan Keras
```
File: praktikum/04_cnn_keras.py
```
1. Build model dengan Sequential API
2. Training dengan callbacks
3. Visualisasi training history

### Latihan
1. Modifikasi arsitektur (tambah layer, ubah filter)
2. Experiment dengan hyperparameters
3. Coba pada CIFAR-10

### Tugas Mandiri
1. Implementasi LeNet-5 architecture
2. Bandingkan dengan custom architecture
3. Plot confusion matrix untuk analisis error

---

## Pertemuan 3: Transfer Learning

### Tujuan
1. Memahami konsep Transfer Learning
2. Fine-tuning pre-trained models
3. Aplikasi pada custom dataset

### Alat dan Bahan
- Pre-trained models: ResNet, VGG, EfficientNet
- Custom dataset (minimal 2 classes, 100 images/class)

### Teori Singkat

**Transfer Learning Strategies:**
```
Strategy 1: Feature Extraction
├── Freeze all pre-trained layers
├── Replace classifier head
└── Train only new layers

Strategy 2: Fine-tuning
├── Freeze early layers (generic features)
├── Unfreeze later layers (task-specific)
└── Train with low learning rate

Strategy 3: Full Training
├── Use pre-trained as initialization
├── Unfreeze all layers
└── Train entire network
```

**Learning Rate untuk Fine-tuning:**
```
Pre-trained layers: lr = 1e-5 to 1e-4
New layers: lr = 1e-3 to 1e-2
Ratio: 10-100x difference
```

### Langkah Praktikum

#### Praktikum 3.1: Transfer Learning PyTorch
```
File: praktikum/05_transfer_learning.py
```
1. Load pre-trained ResNet
2. Modify classifier untuk custom classes
3. Training dengan freezing strategy

#### Praktikum 3.2: Data Augmentation
```
File: praktikum/06_data_augmentation.py
```
1. Implementasi augmentation pipeline
2. Visualisasi augmented images
3. Impact terhadap training

### Latihan
1. Coba berbagai pre-trained backbones
2. Experiment dengan unfreezing strategies
3. Compare performance pada small dataset

### Tugas Mandiri
1. Buat classifier untuk dataset custom (minimal 3 classes)
2. Bandingkan training from scratch vs transfer learning
3. Dokumentasi augmentation yang digunakan

---

## Pertemuan 4: Object Detection dengan YOLO

### Tujuan
1. Memahami arsitektur YOLO
2. Menggunakan YOLOv8 untuk detection
3. Training YOLO pada custom dataset

### Alat dan Bahan
- Library: ultralytics
- Pre-trained: yolov8n, yolov8s, yolov8m
- COCO dataset annotations

### Teori Singkat

**YOLO Detection Process:**
```
1. Input Image (640×640)
2. Backbone extracts features
3. Neck aggregates multi-scale features
4. Head predicts:
   - Bounding boxes (x, y, w, h)
   - Objectness score
   - Class probabilities
5. NMS filters overlapping detections
```

**YOLOv8 Variants:**
| Model | Size | mAP@0.5 | Speed |
|-------|------|---------|-------|
| YOLOv8n | 3.2M | 37.3 | Fast |
| YOLOv8s | 11.2M | 44.9 | Medium |
| YOLOv8m | 25.9M | 50.2 | Medium |
| YOLOv8l | 43.7M | 52.9 | Slow |

### Langkah Praktikum

#### Praktikum 4.1: YOLO Inference
```
File: praktikum/07_yolo_detection.py
```
1. Load YOLOv8 model
2. Detection pada image dan video
3. Visualisasi hasil

#### Praktikum 4.2: YOLO dengan Webcam
```
File: praktikum/08_yolo_realtime.py
```
1. Real-time detection dari webcam
2. Measure FPS
3. Filter specific classes

### Latihan
1. Bandingkan yolov8n vs yolov8s vs yolov8m
2. Experiment dengan confidence threshold
3. Custom post-processing (counting, tracking)

### Tugas Mandiri
1. Buat vehicle counter menggunakan YOLO
2. Implementasi line crossing detection
3. Export hasil ke video file

---

## Pertemuan 5: Image Segmentation

### Tujuan
1. Memahami semantic segmentation
2. Menggunakan model segmentation
3. Instance segmentation dengan YOLO

### Alat dan Bahan
- Library: ultralytics, segmentation-models-pytorch
- Pre-trained segmentation models

### Teori Singkat

**Segmentation Output:**
```
Semantic Segmentation:
Input: H×W×3 image
Output: H×W class map (each pixel = class ID)

Instance Segmentation:
Input: H×W×3 image
Output: List of (mask, class, confidence) per instance
```

**Segmentation Metrics:**
```
IoU (Intersection over Union):
IoU = (Predicted ∩ Ground Truth) / (Predicted ∪ Ground Truth)

Dice Coefficient:
Dice = 2 × |Predicted ∩ Ground Truth| / (|Predicted| + |Ground Truth|)

Pixel Accuracy:
Accuracy = Correct Pixels / Total Pixels
```

### Langkah Praktikum

#### Praktikum 5.1: Semantic Segmentation
```
File: praktikum/09_semantic_segmentation.py
```
1. Load DeepLabV3 model
2. Segmentasi pada images
3. Visualisasi dengan colormap

#### Praktikum 5.2: Instance Segmentation dengan YOLO
```
File: praktikum/10_instance_segmentation.py
```
1. YOLOv8-seg model
2. Extract per-instance masks
3. Post-processing masks

### Latihan
1. Bandingkan semantic vs instance segmentation
2. Experiment dengan berbagai backbones
3. Hitung IoU untuk setiap class

### Tugas Mandiri
1. Background removal menggunakan segmentation
2. Implementasi portrait mode effect
3. Analisis performance per class

---

## Pertemuan 6: Model Deployment dan Optimization

### Tujuan
1. Export model ke ONNX
2. Optimasi model (quantization)
3. Deployment dengan OpenCV

### Alat dan Bahan
- ONNX runtime
- OpenCV DNN module
- Pre-trained models

### Teori Singkat

**Model Export Workflow:**
```
Training Framework (PyTorch/TF)
         ↓
    Export to ONNX
         ↓
    Optimize/Quantize
         ↓
    Deploy with Runtime
    (OpenCV, ONNX Runtime, TensorRT)
```

**Quantization Types:**
```
FP32 → FP16: 2x smaller, minimal accuracy loss
FP32 → INT8: 4x smaller, requires calibration
```

### Langkah Praktikum

#### Praktikum 6.1: ONNX Export dan Inference
```
File: praktikum/11_onnx_export.py
```
1. Export PyTorch model ke ONNX
2. Verify dengan ONNX runtime
3. Compare dengan original model

#### Praktikum 6.2: OpenCV DNN Deployment
```
File: praktikum/12_opencv_deployment.py
```
1. Load ONNX dengan OpenCV
2. Inference tanpa PyTorch
3. Benchmark performance

### Latihan
1. Export model sendiri ke ONNX
2. Bandingkan inference time antar backend
3. Test cross-platform deployment

### Tugas Mandiri
1. Buat end-to-end application dengan ONNX
2. Dokumentasi deployment process
3. Performance comparison report

---

## Tugas Video Praktikum

### Deskripsi
Buat video demonstrasi yang menunjukkan pemahaman deep learning untuk computer vision.

### Persyaratan Video
- **Durasi**: 8-12 menit
- **Format**: MP4, minimal 720p
- **Konten yang harus ada**:
  1. CNN architecture explanation (2 menit)
  2. Transfer learning demo (3 menit)
  3. Object detection demo (3 menit)
  4. Custom application showcase (2-4 menit)

### Checklist Penilaian
- [ ] Penjelasan arsitektur CNN (convolution, pooling, FC)
- [ ] Demo image classification dengan pre-trained model
- [ ] Demo transfer learning dengan custom dataset
- [ ] Demo YOLO object detection
- [ ] Perbandingan model (accuracy, speed)
- [ ] Visualisasi yang jelas dan informatif
- [ ] Kualitas audio dan video baik

---

## Referensi Praktikum

### Library Documentation
1. [PyTorch Tutorials](https://pytorch.org/tutorials/)
2. [TorchVision Models](https://pytorch.org/vision/stable/models.html)
3. [Ultralytics YOLOv8](https://docs.ultralytics.com/)
4. [OpenCV DNN](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)

### Datasets
1. [MNIST](http://yann.lecun.com/exdb/mnist/)
2. [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)
3. [ImageNet](https://www.image-net.org/)
4. [COCO](https://cocodataset.org/)

### Papers
1. AlexNet: "ImageNet Classification with Deep CNNs" (2012)
2. VGGNet: "Very Deep Convolutional Networks" (2014)
3. ResNet: "Deep Residual Learning" (2015)
4. YOLO: "You Only Look Once" (2016)

---

## Catatan Penting

### Requirement Hardware
- GPU recommended untuk training (CUDA-capable)
- Minimum 8GB RAM
- SSD untuk faster data loading

### Tips Training
1. Start dengan small model (MobileNet, YOLOv8n)
2. Monitor training dengan TensorBoard
3. Save checkpoint regularly
4. Use mixed precision jika GPU support

### Troubleshooting
1. CUDA out of memory → Reduce batch size
2. Training tidak converge → Check learning rate
3. Overfitting → Add augmentation, dropout
4. Slow training → Use pretrained, reduce image size
