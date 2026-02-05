# JOBSHEET BAB 5: DEEP LEARNING UNTUK COMPUTER VISION
## Praktikum Sistem Klasifikasi dan Deteksi Berbasis Deep Learning

---

## INFORMASI UMUM PRAKTIKUM

### Identitas
- **Mata Kuliah**: Praktikum Computer Vision
- **Topik**: Deep Learning untuk Computer Vision - Dari Teori hingga Deployment
- **SKS**: 3 SKS (3 × 50 menit per minggu)
- **Total Praktikum**: 6 pertemuan (900 menit)
- **Level**: Menengah-Lanjut

### Prasyarat
- Pemahaman dasar CNN dan neural networks
- Python programming intermediate
- NumPy dan OpenCV basics
- GPU computing (optional, CPU juga OK)

### Tools dan Perangkat
- **Hardware**: PC/Laptop dengan minimum 8GB RAM, GPU optional
- **OS**: Linux/Windows/MacOS
- **Python**: 3.8+
- **Framework**: PyTorch 2.0+ atau TensorFlow 2.8+
- **Library Utama**:
  - `opencv-python >= 4.8.0` (untuk DNN dan image processing)
  - `torch / tensorflow` (deep learning framework)
  - `numpy` (numerical computing)
  - `matplotlib / opencv` (visualization)
  - `ultralytics` (untuk YOLO)
  - `scikit-learn` (untuk metrics dan evaluation)

### Tujuan Pembelajaran Umum
Setelah menyelesaikan praktikum ini, mahasiswa mampu:
1. ✅ Memahami arsitektur CNN dan aplikasinya
2. ✅ Menggunakan pre-trained models untuk inference
3. ✅ Melakukan transfer learning pada dataset custom
4. ✅ Mengimplementasikan object detection real-time
5. ✅ Melakukan optimisasi model untuk deployment
6. ✅ Membuat sistem end-to-end image classification & detection
7. ✅ Melakukan evaluasi dan debugging deep learning models

---

## PERTEMUAN 1: DASAR-DASAR NEURAL NETWORK DAN OPENCV DNN

### Tujuan Pertemuan
- Memahami konsep dasar neural networks untuk vision
- Menjalankan pre-trained models dengan OpenCV DNN
- Memahami preprocessing untuk inference
- Mengoptimalkan inference speed vs accuracy

### Durasi
- Teori & Demo: 60 menit
- Praktikum Terstruktur: 60 menit
- Eksplorasi & Tugas: 30 menit

### Konsep Kunci

#### A. Neural Network Basics
```
Feedforward Neural Network untuk Image Classification:

Input Layer        Hidden Layers                Output Layer
(224×224×3)  →   [Conv] → [ReLU]   →    [FC] → [Softmax]
                    ↓         ↓            ↓
                  [Conv] → [Pool] → [Flatten]
                    ↓         ↓
                 Features  Reduced
                          Spatial Size
```

**Konsep Penting:**
- **Convolution**: Ekstraksi features lokal dengan learnable kernels
- **Pooling**: Dimensionality reduction & shift invariance
- **Activation**: Non-linearity untuk learning complex patterns
- **Softmax**: Konversi logits ke probability distribution

#### B. OpenCV DNN Module
OpenCV DNN memungkinkan inference **TANPA** PyTorch/TensorFlow runtime (sangat penting untuk deployment).

**Supported Model Formats:**
- Caffe (.caffemodel + .prototxt)
- TensorFlow (.pb)
- ONNX (.onnx) ← Recommended untuk portability
- Darknet/YOLO (.weights + .cfg)
- OpenVINO (.xml + .bin) ← Untuk Intel hardware

**Keuntungan OpenCV DNN:**
- Lightweight, no heavy dependencies
- Cross-platform compatibility
- Hardware acceleration support (CUDA, OpenCL, etc.)
- Direct inference without framework installation

#### C. Image Preprocessing Pipeline
```
Raw Image → Resize → Normalize → Mean Subtract → Blob
(H×W×3)   (224×224)  ([0,1])    (ImageNet)   (1×3×H×W)
```

### Praktikum Terstruktur

#### **PRAKTIKUM 1.1: OpenCV DNN Image Classification Basics**

**File**: `praktikum/01_opencv_dnn_classification.py`

**Langkah-langkah:**

```bash
# 1. Jalankan program
python praktikum/01_opencv_dnn_classification.py

# 2. Pilih menu demo 1 - Basic Classification
# Output yang diharapkan:
# [INFO] Image loaded: shape=(480, 640, 3)
# [INFO] Blob created: shape=(1, 3, 224, 224)
# [Classification Result]
# Top 5 predictions with confidence scores
```

**Apa yang dipelajari:**
- Membaca dan resize gambar
- Membuat blob dengan `cv2.dnn.blobFromImage()`
- Preprocessing untuk network input
- Memahami blob shape: (batch, channels, height, width)

**Real-World Application: Smart Retail Inventory**
```
Use Case: Automatic Product Classification in Retail
Challenge: 1000+ product SKUs, manual counting is time-consuming
Solution: 
  - Deploy image classification model on edge device (PI/Jetson)
  - Use OpenCV DNN for lightweight inference
  - Process shelf images in real-time
Result:
  - Reduce inventory check time from 4 hours → 15 minutes
  - 95%+ accuracy on known products
  - Works on CPU without GPU
```

#### **PRAKTIKUM 1.2: Exploring Blob Parameters**

**File**: `praktikum/01_opencv_dnn_classification.py` → Menu 2

**Parameter yang Diexplore:**

```python
# Blob creation parameters
blob = cv2.dnn.blobFromImage(
    image,                          # Input image (BGR)
    scalefactor=1/255.0,           # Normalization factor
    size=(224, 224),               # Network input size
    mean=(104, 117, 123),          # Mean subtraction (BGR)
    swapRB=False,                  # BGR to RGB conversion
    crop=False                     # Center crop if True
)

# Impact analysis:
# - scalefactor: [1.0, 1/255, 1/127.5] → different normalization ranges
# - size: [224, 256, 300] → receptive field changes
# - mean: ImageNet mean values vs zero mean → network expects
# - swapRB: BGR vs RGB → important for color correctness
```

**Latihan:**
1. Coba berbagai scale factor dan amati impact ke output
2. Test dengan input size berbeda (224, 256, 416)
3. Compare swapRB=True vs False pada colored images

#### **PRAKTIKUM 1.3: Complete Classification Workflow**

**File**: `praktikum/01_opencv_dnn_classification.py` → Menu 3

**Workflow:**
```
Read Image → Preprocess → Create Blob → Forward Pass → Top-K → Visualize
     ↓            ↓           ↓             ↓           ↓
  OpenCV      Normalize    blobFromImage  Network    argmax+sort
```

**Output:**
```
[Classification Result]
Predicted Class: dog (index 207)
Top 5 Predictions:
  1. dog         - 0.8954 ████████████████
  2. puppy       - 0.0812 ███
  3. animal      - 0.0234 ▌
```

### Tugas Praktikum 1

**Tugas 1.1: Model Analysis**
- Run `01_opencv_dnn_classification.py` dengan 5 gambar berbeda
- Catat predictions untuk setiap gambar
- Analisis Top-1 vs Top-5 accuracy
- **Output**: File `tugas1_results.txt` dengan results

**Tugas 1.2: Preprocessing Impact Study**
- Jalankan same image dengan berbagai preprocessing parameter
- Observe changes in predictions
- Document which parameters affect confidence scores most
- **Output**: File `tugas1_preprocessing_study.py` dengan analisis

**Tugas 1.3: Real-World Scenario**
- **Skenario**: Food delivery app wants to verify restaurant photos
- Classify 3-5 food images menggunakan model trained on ImageNet
- Evaluate realistic use cases (poor lighting, occlusion, etc.)
- **Output**: Demo video atau screenshots dengan hasil klasifikasi

### Deliverables Pertemuan 1

```
Bab-05-Deep-Learning/
├── praktikum/
│   ├── 01_opencv_dnn_classification.py     [UPDATED dengan Q-key closing]
│   └── sample_results_01/
│       ├── classification_output.png
│       ├── blob_visualization.png
│       └── results_summary.txt
├── tugas_1/
│   ├── tugas1_results.txt
│   ├── tugas1_preprocessing_study.py
│   └── tugas1_scenarios.md
└── dokumentasi_1.md
```

### Evaluasi Kriteria
- **Fungsionalitas**: Program berjalan tanpa error ✓
- **Output**: Predictions dan confidence scores visible ✓
- **Dokumentasi**: Penjelasan parameter dan hasil ✓
- **Real-world thinking**: Ada aplikasi praktis ✓

---

## PERTEMUAN 2: CONVOLUTIONAL NEURAL NETWORKS - ARCHITECTURE & TRAINING

### Tujuan Pertemuan
- Membangun CNN dari scratch
- Memahami training loop dan optimization
- Praktik dengan MNIST/CIFAR-10 datasets
- Debugging common training issues

### Durasi
- Teori: 50 menit
- Praktikum Coding: 70 menit
- Debugging & Optimization: 30 menit

### Konsep Kunci - CNN Architecture

#### A. Convolutional Layer Mechanics
```
Input: (H, W, C_in)  →  Convolution  →  Output: (H', W', C_out)

Parameters:
- Kernel size K (3×3, 5×5, 7×7)
- Number of filters F = C_out
- Stride S (1, 2)
- Padding P (0, 1, same)

Output size formula:
H' = floor((H + 2P - K) / S) + 1
W' = floor((W + 2P - K) / S) + 1
```

**Contoh CNN Architecture Sederhana:**
```
Input (28×28×1)
  ↓
Conv2D(32, 3×3) + ReLU → (28×28×32)
  ↓
MaxPool2D(2×2) → (14×14×32)
  ↓
Conv2D(64, 3×3) + ReLU → (14×14×64)
  ↓
MaxPool2D(2×2) → (7×7×64)
  ↓
Flatten() → (3136,)
  ↓
Dense(128) + ReLU → (128,)
  ↓
Dense(10) + Softmax → (10,) [class probabilities]
```

#### B. Training Loop Components

**1. Forward Pass:**
```python
# Compute predictions
predictions = model(input_batch)  # shape: (batch_size, num_classes)

# Compute loss
loss = criterion(predictions, labels)  # single scalar value
```

**2. Backward Pass:**
```python
# Compute gradients
loss.backward()  # backward propagation through network

# Update weights
optimizer.step()  # W = W - lr * dL/dW
optimizer.zero_grad()  # reset gradients for next iteration
```

**3. Evaluation:**
```python
with torch.no_grad():
    predictions = model(test_batch)
    accuracy = (predictions.argmax(1) == labels).float().mean()
```

### Praktikum Terstruktur

#### **PRAKTIKUM 2.1: CNN from Scratch dengan PyTorch**

**File**: `praktikum/03_cnn_pytorch.py`

**Langkah-langkah:**

```bash
# 1. Download MNIST dataset (otomatis)
python praktikum/03_cnn_pytorch.py

# 2. Select menu: "1. Train CNN"
# Output:
# Loading MNIST dataset...
# Epoch 1/10 - Loss: 0.4521, Accuracy: 94.23%
# Epoch 2/10 - Loss: 0.1234, Accuracy: 97.56%
# ...
# Final Test Accuracy: 98.45%
```

**Network Architecture yang Dibangun:**
```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64*7*7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.pool = nn.MaxPool2d(2, 2)
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

**Real-World Application: Handwritten Digit Recognition**
```
Use Case: Bank check processing, postal code recognition
Challenge: Real-world images have noise, rotation, variation
Solution:
  - Train CNN on MNIST dataset
  - Add data augmentation (rotation, blur, noise)
  - Deploy on mobile/edge device
Result:
  - 99%+ accuracy on clean digits
  - ~95% on real-world checks with preprocessing
  - Fast inference (<10ms per digit)
```

#### **PRAKTIKUM 2.2: Data Augmentation untuk Better Generalization**

**File**: `praktikum/06_data_augmentation.py`

**Augmentation Techniques:**

```python
# Geometric transforms
- Random rotation (±15 degrees)
- Random flip (horizontal, vertical)
- Random affine transforms
- Random perspective

# Color augmentations
- Brightness/contrast adjustment
- Color jittering (Hue, Saturation, Value)
- Grayscale conversion
- Equalization

# Advanced
- Mixup: Blend two images linearly
- CutOut: Randomly mask regions
- CutMix: Mix images at pixel level
```

**Langkah Praktikum:**
```bash
python praktikum/06_data_augmentation.py

# Menu options:
# 1. Geometric Augmentations
# 2. Color Augmentations
# 3. Noise & Blur
# 4. Advanced (Mixup, CutOut, CutMix)
# 5. Complete Pipeline

# Visual output:
# Original image vs 5 augmented variants untuk setiap technique
```

**Impact Analysis:**
```
Training WITHOUT augmentation:
- Train accuracy: 99.5%
- Test accuracy: 95.2%
- Overfitting gap: 4.3%

Training WITH augmentation:
- Train accuracy: 97.8%
- Test accuracy: 97.1%
- Overfitting gap: 0.7% ← Much better!
```

### Common Training Issues & Debugging

#### **Issue 1: Loss Not Decreasing**
```
❌ Problem: Loss stays constant atau increases
✓ Solutions:
  - Reduce learning rate (lr too high causes instability)
  - Check data loading (verify images are normalized 0-1)
  - Initialize weights properly (Xavier/He initialization)
  - Verify labels are correct
```

#### **Issue 2: Overfitting**
```
❌ Symptoms: Train acc 99% but Test acc 60%
✓ Solutions:
  - Add L2 regularization (weight decay)
  - Use dropout layers (0.2-0.5)
  - Increase data augmentation
  - Use early stopping with validation set
  - Reduce model capacity (fewer layers/parameters)
```

#### **Issue 3: GPU Out of Memory**
```
❌ Error: CUDA out of memory
✓ Solutions:
  - Reduce batch size (32 → 16 → 8)
  - Reduce image resolution (224 → 128)
  - Use mixed precision (torch.autocast)
  - Gradient accumulation for larger effective batch
```

### Tugas Praktikum 2

**Tugas 2.1: Custom Architecture Design**
- Design CNN architecture untuk CIFAR-10 (32×32 images, 10 classes)
- Target: ≥ 85% test accuracy
- Document architecture dengan layer configurations
- **Deliverable**: `tugas2_custom_cnn.py`

**Tugas 2.2: Augmentation Experiment**
- Train same CNN dengan dan tanpa data augmentation
- Compare train/test accuracy curves
- Analyze overfitting with/without augmentation
- **Deliverable**: `tugas2_augmentation_analysis.md` + plot

**Tugas 2.3: Hyperparameter Tuning**
- Experiment dengan learning rate: [1e-3, 1e-4, 1e-5]
- Experiment dengan batch size: [16, 32, 64, 128]
- Measure training time dan final accuracy
- **Deliverable**: `tugas2_hyperparameter_grid.py` + results table

### Deliverables Pertemuan 2

```
Bab-05-Deep-Learning/
├── praktikum/
│   ├── 03_cnn_pytorch.py           [UPDATED]
│   ├── 04_cnn_keras.py             [UPDATED]
│   ├── 06_data_augmentation.py      [UPDATED - auto Q-key]
│   └── training_results_02/
│       ├── training_loss_curve.png
│       ├── accuracy_curve.png
│       ├── confusion_matrix.png
│       └── model_checkpoint.pth
├── tugas_2/
│   ├── tugas2_custom_cnn.py
│   ├── tugas2_augmentation_analysis.md
│   └── tugas2_hyperparameter_grid.py
└── dokumentasi_2.md
```

---

## PERTEMUAN 3: TRANSFER LEARNING & FINE-TUNING

### Tujuan Pertemuan
- Memahami transfer learning konsep
- Praktik fine-tuning pre-trained models
- Handling small datasets dengan TL
- Evaluasi & optimization

### Durasi
- Teori: 40 menit
- Praktikum: 80 menit
- Case Study: 40 menit

### Konsep Kunci

#### A. Transfer Learning Strategies

**Strategy 1: Feature Extraction (Freeze All)**
```
Pre-trained Model (ImageNet)
   ↓
├── Layer 1-5: Frozen (generic features)
├── Layer 6-7: Frozen
└── Custom Head:
    ├── GlobalAveragePool
    ├── Dense(512) + ReLU
    ├── Dropout(0.5)
    └── Dense(num_classes) + Softmax ← Train ONLY this

Benefits:
- Fast training (only last layer)
- Works with small datasets (100-1000 images)
- Low computational cost

Use Cases:
- Few samples per class
- Similar domain to ImageNet
```

**Strategy 2: Fine-Tuning (Unfreeze Later Layers)**
```
Pre-trained Backbone:
   ↓
├── Layer 1-4: Frozen (lr = 0)
├── Layer 5-7: Unfrozen (lr = 1e-5)  ← Lower learning rate
└── Custom Head: (lr = 1e-4)         ← Higher learning rate
    └── ...layers...

Rationale:
- Early layers learn generic features (edges, textures)
- Later layers learn task-specific patterns
- Need lower lr to not destroy pre-trained weights

Use Cases:
- Moderate dataset (1000-10000 images)
- Different domain but related to ImageNet
```

**Strategy 3: Full Training (Unfreeze All)**
```
Pre-trained Model (as initialization):
   ↓
├── All layers unfrozen
├── All layers trained with appropriate learning rates
├── Typically: Early layers (lower lr), Later layers (higher lr)
└── Discriminative learning rates (per-layer tuning)

Benefits:
- Maximum flexibility
- Best possible performance
- Handle domain shift

Requirements:
- Large dataset (10000+ images)
- Significant domain difference from ImageNet
- More computational resources
- Risk of overfitting if data is limited
```

#### B. Learning Rates for Transfer Learning

```
Best Practice - Discriminative Learning Rates:

Layer Type              Recommended LR
─────────────────────────────────────
Early Conv (Block 1-2)  1e-5 to 5e-5
Mid Conv (Block 3-4)    5e-5 to 1e-4
Late Conv (Block 5)     1e-4 to 5e-4
Custom Head             1e-3 to 1e-2

Ratio: Head/Early ≈ 100:1

Example for ResNet50:
├── layer1: lr = 1e-5
├── layer2: lr = 2e-5
├── layer3: lr = 5e-5
├── layer4: lr = 1e-4
├── fc: lr = 1e-3
```

### Praktikum Terstruktur

#### **PRAKTIKUM 3.1: Transfer Learning Basic - ResNet50**

**File**: `praktikum/05_transfer_learning.py`

```bash
python praktikum/05_transfer_learning.py

# Menu:
# 1. Feature Extraction Mode
# 2. Fine-Tuning Mode
# 3. Full Training Mode
# 4. Compare All Strategies
```

**Real-World Application: Medical Image Classification**
```
Use Case: Chest X-ray classification (Normal vs Pneumonia)
Dataset: 500 images per class (small!)
Challenge: Deep networks need thousands of images

Solution using Transfer Learning:
1. Load ResNet50 pre-trained on ImageNet
2. Strategy: Feature Extraction
   - Freeze all layers
   - Replace last layer: 1000 → 2 classes
   - Train only last layer on medical data

Results:
- Train time: 30 minutes (vs 12 hours from scratch)
- Accuracy: 94% (vs 65% from scratch with 500 images)
- Overfitting: Minimal due to frozen layers

Production:
- Model size: 100MB (manageable)
- Inference: 50ms per image (fast enough)
- Deployment: CPU or GPU
```

**Step-by-Step Praktikum:**

```bash
# 1. Prepare custom dataset
mkdir -p data/custom_dataset/{train,val}/{class1,class2}
# Copy images to respective directories

# 2. Run transfer learning script
python praktikum/05_transfer_learning.py
# Select: "1. Feature Extraction Mode"

# 3. Monitor training
# Expected output:
# Epoch 1/10
# ├── Loss: 0.523 | Accuracy: 75.2% | Val: 74.8%
# ├── Loss: 0.234 | Accuracy: 91.2% | Val: 90.1%
# └── Saved best model: best_model.pth (Top-1 val)

# 4. Evaluate on test set
# Accuracy: 92.3%
# Per-class metrics:
# ├── Class 1: Precision 0.89 | Recall 0.95
# └── Class 2: Precision 0.95 | Recall 0.89
```

#### **PRAKTIKUM 3.2: Strategy Comparison**

**Comparing all three strategies on same dataset:**

```python
# Setup
dataset: 1000 images, 2 classes
val_split: 20% (200 images)
architecture: ResNet50
metrics: accuracy, training_time, overfitting_gap
```

**Expected Results:**

```
Strategy              Train Time  Val Accuracy  Overfit Gap
────────────────────────────────────────────────────────
1. Feature Extr       15 min      91.2%         4.3%
2. Fine-tuning        45 min      94.5%         2.1%
3. Full Training      120 min     95.8%         1.5%

Analysis:
- Feature extraction: Fast, good baseline
- Fine-tuning: Best practical choice
- Full training: Best accuracy, but risk with small data
```

### Tugas Praktikum 3

**Tugas 3.1: Custom Dataset Collection & Labeling**
- Kumpulkan minimal 3 class, 100 images/class (dari google images, smartphone, dll)
- Organize dalam folder structure:
  ```
  dataset/
  ├── train/
  │   ├── class1/ (80 images)
  │   ├── class2/ (80 images)
  │   └── class3/ (80 images)
  └── val/
      ├── class1/ (20 images)
      ├── class2/ (20 images)
      └── class3/ (20 images)
  ```
- **Deliverable**: `datasets/custom_dataset/` folder + metadata.txt

**Tugas 3.2: Transfer Learning Implementation**
- Implement feature extraction (freeze all but last layer)
- Train on your custom dataset
- Achieve ≥ 85% validation accuracy
- Document training process & results
- **Deliverable**: `tugas3_transfer_learning.py` + `training_log.txt`

**Tugas 3.3: Strategy Analysis**
- Train same dataset dengan 2 different strategies
- Compare: accuracy, training time, memory usage
- Analyze learning curves (training vs validation)
- Document which strategy is best for your dataset
- **Deliverable**: `tugas3_strategy_analysis.md` + plots

### Deliverables Pertemuan 3

```
Bab-05-Deep-Learning/
├── praktikum/
│   ├── 05_transfer_learning.py    [UPDATED]
│   └── transfer_learning_results/
│       ├── feature_extraction_model.pth
│       ├── fine_tuning_model.pth
│       ├── training_curves.png
│       └── comparison_table.txt
├── datasets/
│   └── custom_dataset/           ← YOUR COLLECTED DATA
│       ├── train/
│       ├── val/
│       └── metadata.txt
├── tugas_3/
│   ├── tugas3_transfer_learning.py
│   ├── tugas3_strategy_analysis.md
│   ├── training_log.txt
│   └── results/
│       ├── model_checkpoint.pth
│       ├── confusion_matrix.png
│       └── classification_report.txt
└── dokumentasi_3.md
```

---

## PERTEMUAN 4: OBJECT DETECTION DENGAN YOLO

### Tujuan Pertemuan
- Memahami object detection architecture (YOLO)
- Menggunakan YOLOv8 untuk real-time detection
- Training YOLO pada custom dataset
- Deployment & optimization

### Durasi
- Teori: 50 menit
- Praktikum: 70 menit
- Case Study: 40 menit

### Konsep Kunci

#### A. YOLO Detection Pipeline

**YOLO (You Only Look Once) Approach:**
```
Single Image
    ↓
Backbone (CSPDarknet):
  Extract multi-scale features
  Output: Features at 3 scales
    ↓
Neck (PANeck):
  Aggregate features
  Build feature pyramid
    ↓
Head (Detect):
  Predict for each scale:
  - Bounding box (x, y, w, h)
  - Objectness score (object or not)
  - Class probabilities (which class)
    ↓
Post-processing:
  - Confidence filtering (0.5)
  - NMS (remove duplicates)
    ↓
Final Detections:
  List of: [class, confidence, bbox]
```

**YOLOv8 Variants:**
```
Model    Size(MB)  Speed(ms)  mAP50(%)  Use Case
──────────────────────────────────────────────
YOLOv8n   6.3      ~80        37.3     Edge/Mobile
YOLOv8s   22.5     ~140       44.9     Lightweight
YOLOv8m   49.7     ~233       50.2     Balanced
YOLOv8l   83.7     ~375       52.3     Accuracy
YOLOv8x   161.0    ~526       53.9     Best (slow)

Selection criteria:
- Edge device (Raspberry Pi) → YOLOv8n
- Laptop/Desktop → YOLOv8s/m
- GPU Server → YOLOv8l/x
- Real-time requirement → smaller model
- Accuracy requirement → larger model
```

#### B. Training YOLO on Custom Dataset

**Dataset Format (YOLO):**
```
dataset/
├── images/
│   ├── train/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── val/
│       └── ...
├── labels/
│   ├── train/
│   │   ├── img1.txt  (format: class x_center y_center width height)
│   │   └── img2.txt
│   └── val/
│       └── ...
└── data.yaml          (metadata: path, nc, names)
```

**data.yaml Example:**
```yaml
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

nc: 3  # number of classes
names: ['car', 'person', 'dog']  # class names
```

### Praktikum Terstruktur

#### **PRAKTIKUM 4.1: YOLOv8 Inference pada Real-time Video**

**File**: `praktikum/07_yolo_detection.py`, `praktikum/08_yolo_realtime.py`

```bash
# 1. Basic inference on image
python praktikum/07_yolo_detection.py

# 2. Real-time detection on webcam
python praktikum/08_yolo_realtime.py

# Output:
# ├── Detected objects with bounding boxes
# ├── Class labels dengan confidence scores
# ├── FPS (frames per second)
# └── Inference time per frame
```

**Expected Output:**
```
[YOLO Detection Results]
Detected 5 objects in image
├── person at (234, 123, 345, 567) - confidence: 0.98
├── car at (456, 234, 789, 456) - confidence: 0.95
├── dog at (567, 345, 645, 500) - confidence: 0.92
├── person at (700, 200, 850, 600) - confidence: 0.87
└── bicycle at (100, 400, 250, 650) - confidence: 0.78

Processing time: 45ms/frame
Average FPS: 22.2
```

**Real-World Application: Traffic Monitoring**
```
Use Case: Traffic camera detects cars, motorcycles, pedestrians
Challenge: 24/7 operation, detect violations (speeding, wrong lane)
Solution:
  1. Deploy YOLOv8s on edge device
  2. Detect vehicles + pedestrians
  3. Track objects between frames
  4. Identify rule violations
  
Results:
- Detection accuracy: 94%
- Real-time FPS: 25 on GPU, 8 on CPU
- Memory: 50MB (small enough for edge)
```

#### **PRAKTIKUM 4.2: Training YOLO on Custom Dataset (Optional - Advanced)**

**File**: `praktikum/yolo_train_custom.py` (provide template)

```bash
python praktikum/yolo_train_custom.py --dataset path/to/dataset

# Configuration
epochs: 100
imgsz: 640
batch: 16  # adjust for GPU memory
lr0: 0.01  # initial learning rate
```

### Tugas Praktikum 4

**Tugas 4.1: Real-time Detection on Video**
- Run YOLOv8 on sample video file
- Detect objects and annotate with boxes + labels
- Save output video with detections
- Measure and report FPS
- **Deliverable**: `tugas4_video_detection.py` + output_video.mp4

**Tugas 4.2: Webcam Live Detection**
- Stream from webcam/USB camera
- Real-time object detection
- Count objects per class (e.g., "3 persons, 2 cars")
- Press 'q' to exit
- **Deliverable**: `tugas4_webcam_detection.py` + screenshot

**Tugas 4.3: Performance Analysis**
- Run YOLOv8n vs YOLOv8m vs YOLOv8l on same video
- Compare: FPS, accuracy, memory usage
- Create comparison table
- **Deliverable**: `tugas4_performance_analysis.py` + results.csv

### Deliverables Pertemuan 4

```
Bab-05-Deep-Learning/
├── praktikum/
│   ├── 07_yolo_detection.py         [UPDATED]
│   ├── 08_yolo_realtime.py          [UPDATED - Q-key exit]
│   └── detection_results/
│       ├── sample_detections.jpg
│       ├── output_video.mp4
│       └── stats.txt
├── tugas_4/
│   ├── tugas4_video_detection.py
│   ├── tugas4_webcam_detection.py
│   ├── tugas4_performance_analysis.py
│   └── results/
│       ├── output_video.mp4
│       ├── performance_comparison.csv
│       └── analysis_report.md
└── dokumentasi_4.md
```

---

## PERTEMUAN 5-6: IMAGE SEGMENTATION & FINAL PROJECT

### Ringkasan Singkat
- Semantic segmentation (FCN, U-Net)
- Instance segmentation (Mask R-CNN)
- Final project: End-to-end system

**Deliverable Final:**
```
Final Project: DeepVision Sistem
├── Code/
│   ├── classifier.py
│   ├── detector.py
│   └── integration.py
├── Models/
│   ├── classifier_model.pth
│   └── detector_model.pt
├── Demo/
│   ├── demo_video.mp4
│   └── demo_results/
└── Documentation/
    ├── README.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

---

## PANDUAN UMUM PRAKTIKUM

### Checklist Setiap Pertemuan
- [ ] Baca materials sebelumnya
- [ ] Jalankan semua praktikum yang disediakan
- [ ] Pahami output dan error messages
- [ ] Modifikasi parameters dan observe impact
- [ ] Selesaikan semua tugas terstruktur
- [ ] Dokumentasikan findings
- [ ] Submit sebelum deadline

### Tips Sukses
1. **Start Early**: Jangan last-minute
2. **Experiment**: Coba berbagai parameter
3. **Debug Systematically**: Print intermediate results
4. **Visualize**: Selalu plot/show hasil
5. **Document**: Catat apa yang Anda pelajari
6. **Ask Questions**: Jangan takut bertanya
7. **Collaborate**: Diskusi dengan teman (tapi kerja sendiri)

### Common Issues & Solutions

**Issue: "ModuleNotFoundError: torch"**
```
Solution: pip install torch torchvision torchaudio -index-url https://download.pytorch.org/whl/cu118
```

**Issue: "CUDA out of memory"**
```
Solution: Reduce batch size, image size, atau use CPU
```

**Issue: "cv2.imshow() hangs"**
```
✓ FIXED in updated files - uses Q-key to close
```

---

## EVALUATION RUBRIK

### Per Pertemuan (25% masing-masing)
- Ketuntasan praktikum
- Kualitas dokumentasi
- Eksperimen & analisis
- Presentasi hasil

### Final Project (25%)
- Functionality
- Code quality
- Documentation
- Presentation

### Minimum Grade: 70% (C)
