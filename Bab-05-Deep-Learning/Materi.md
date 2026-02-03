# BAB 5: DEEP LEARNING UNTUK COMPUTER VISION

## Tujuan Pembelajaran

Setelah menyelesaikan bab ini, mahasiswa diharapkan mampu:
1. Memahami arsitektur Convolutional Neural Network (CNN)
2. Menggunakan pre-trained models untuk image classification
3. Menerapkan Transfer Learning untuk custom dataset
4. Memahami Object Detection dengan YOLO
5. Melakukan Image Segmentation

---

## 5.1 Pendahuluan Deep Learning

### 5.1.1 Mengapa Deep Learning?

Traditional computer vision menggunakan hand-crafted features (SIFT, HOG, etc.) yang memerlukan domain expertise untuk design. Deep Learning secara otomatis mempelajari features dari data.

```
Traditional CV Pipeline:
Input → Hand-crafted Features → Classifier → Output
        (SIFT, HOG, etc.)      (SVM, RF)

Deep Learning Pipeline:
Input → Neural Network (learns features + classifier) → Output
```

### 5.1.2 Perkembangan Deep Learning untuk CV

| Tahun | Milestone | Dampak |
|-------|-----------|--------|
| 2012 | AlexNet wins ImageNet | CNN revolution begins |
| 2014 | VGGNet, GoogLeNet | Deeper networks |
| 2015 | ResNet (152 layers) | Skip connections |
| 2016 | YOLO real-time detection | Object detection |
| 2017 | Transformer attention | Foundation for ViT |
| 2020 | Vision Transformer (ViT) | Attention-based CV |

---

## 5.2 Convolutional Neural Networks (CNN)

### 5.2.1 Arsitektur Dasar CNN

```
┌─────────────────────────────────────────────────────────────┐
│                    CNN Architecture                          │
├─────────────────────────────────────────────────────────────┤
│  Input   →  Conv  →  ReLU  →  Pool  →  Conv  →  ...  →  FC │
│ (Image)    Layer    Activ.   Layer    Layer        Layers   │
│                                                              │
│  [H×W×C]  [H×W×F]  [H×W×F]  [H/2×W/2×F]              [N]   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2.2 Convolutional Layer

Convolution melakukan operasi sliding window dengan learnable filters:

```
Input Feature Map      Filter (Kernel)       Output Feature Map
┌───┬───┬───┬───┐      ┌───┬───┬───┐        ┌───┬───┐
│ 1 │ 2 │ 3 │ 0 │      │ 1 │ 0 │ 1 │        │ 8 │ 6 │
├───┼───┼───┼───┤  ∗   ├───┼───┼───┤   =    ├───┼───┤
│ 4 │ 5 │ 6 │ 1 │      │ 0 │ 1 │ 0 │        │ 4 │ 7 │
├───┼───┼───┼───┤      ├───┼───┼───┤        └───┴───┘
│ 7 │ 8 │ 9 │ 2 │      │ 1 │ 0 │ 1 │
├───┼───┼───┼───┤      └───┴───┘
│ 0 │ 1 │ 2 │ 3 │
└───┴───┴───┴───┘
```

**Parameter:**
- **Kernel Size**: ukuran filter (biasanya 3×3, 5×5)
- **Stride**: langkah pergeseran (biasanya 1 atau 2)
- **Padding**: penambahan border (same atau valid)
- **Filters**: jumlah output channels

**Formula Output Size:**
$$O = \frac{I - K + 2P}{S} + 1$$

Dimana:
- $O$ = Output size
- $I$ = Input size
- $K$ = Kernel size
- $P$ = Padding
- $S$ = Stride

### 5.2.3 Pooling Layer

Pooling mengurangi spatial dimensions untuk:
- Mengurangi parameters
- Control overfitting
- Achieve translation invariance

```
Max Pooling (2×2, stride 2):
┌───┬───┬───┬───┐        ┌───┬───┐
│ 1 │ 3 │ 2 │ 4 │        │ 5 │ 6 │
├───┼───┼───┼───┤   →    ├───┼───┤
│ 5 │ 2 │ 6 │ 1 │        │ 8 │ 7 │
├───┼───┼───┼───┤        └───┴───┘
│ 7 │ 8 │ 3 │ 2 │
├───┼───┼───┼───┤
│ 4 │ 1 │ 5 │ 7 │
└───┴───┴───┴───┘
```

### 5.2.4 Activation Functions

| Function | Formula | Karakteristik |
|----------|---------|---------------|
| ReLU | $f(x) = max(0, x)$ | Simple, efficient, standard |
| Leaky ReLU | $f(x) = max(0.01x, x)$ | Prevents dying neurons |
| Sigmoid | $f(x) = \frac{1}{1+e^{-x}}$ | Output [0,1], vanishing gradient |
| Softmax | $f(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$ | Multi-class probability |

---

## 5.3 Arsitektur CNN Populer

### 5.3.1 LeNet-5 (1998)

Arsitektur pertama yang sukses untuk digit recognition:

```
Input (32×32×1)
    ↓
Conv1 (5×5, 6 filters) → 28×28×6
    ↓
AvgPool (2×2) → 14×14×6
    ↓
Conv2 (5×5, 16 filters) → 10×10×16
    ↓
AvgPool (2×2) → 5×5×16
    ↓
FC (120) → FC (84) → Output (10)
```

### 5.3.2 VGGNet (2014)

Menggunakan 3×3 convolutions secara konsisten:

```
VGG-16 Configuration:
├── Block 1: 2× Conv(64, 3×3) + MaxPool
├── Block 2: 2× Conv(128, 3×3) + MaxPool  
├── Block 3: 3× Conv(256, 3×3) + MaxPool
├── Block 4: 3× Conv(512, 3×3) + MaxPool
├── Block 5: 3× Conv(512, 3×3) + MaxPool
├── FC (4096) → FC (4096) → FC (1000)
└── Total: ~138M parameters
```

### 5.3.3 ResNet (2015)

Memperkenalkan skip connections untuk train deep networks:

```
Residual Block:
         ┌────────────────┐
    x ───┤                ├───→ x + F(x)
         │    F(x)        │
         │  ┌─────────┐   │
         └──│ Conv    │───┘
            │ BN+ReLU │
            │ Conv    │
            │ BN      │
            └─────────┘

Identity Mapping: H(x) = F(x) + x
```

**Variants:**
- ResNet-18: 18 layers
- ResNet-34: 34 layers
- ResNet-50: 50 layers (bottleneck)
- ResNet-101, ResNet-152

### 5.3.4 EfficientNet (2019)

Compound scaling untuk balance depth, width, dan resolution:

```
Scaling Factors:
├── Depth: d = α^φ
├── Width: w = β^φ  
├── Resolution: r = γ^φ
└── Constraint: α × β² × γ² ≈ 2

EfficientNet-B0 to B7: increasing φ
```

---

## 5.4 Transfer Learning

### 5.4.1 Konsep Transfer Learning

Transfer learning menggunakan knowledge dari pre-trained model (biasanya ImageNet) untuk task baru.

```
ImageNet Pre-trained Model:
┌──────────────────────────────────────────┐
│ Feature Extractor │ Classifier           │
│ (Conv Layers)     │ (FC Layers)          │
│ [Freeze/Fine-tune]│ [Replace]            │
└──────────────────────────────────────────┘
                    ↓
Custom Task:
┌──────────────────────────────────────────┐
│ Feature Extractor │ New Classifier       │
│ (Pre-trained)     │ (Custom classes)     │
└──────────────────────────────────────────┘
```

### 5.4.2 Strategi Transfer Learning

| Strategy | When to Use | How |
|----------|------------|-----|
| Feature Extraction | Small dataset, similar domain | Freeze all, train new classifier |
| Fine-tuning | Medium dataset | Unfreeze top layers, low learning rate |
| Full Training | Large dataset, different domain | Train from scratch or unfreeze all |

### 5.4.3 Best Practices

1. **Start with Feature Extraction**: Freeze pre-trained weights
2. **Use Lower Learning Rate**: 10x-100x smaller untuk fine-tuning
3. **Unfreeze Gradually**: From top to bottom layers
4. **Data Augmentation**: Essential untuk small datasets
5. **Early Stopping**: Monitor validation loss

---

## 5.5 Object Detection

### 5.5.1 Paradigma Object Detection

```
Image Classification: "What is in the image?"
→ Output: Class label

Object Detection: "What and where?"
→ Output: Class + Bounding Box (x, y, w, h)

Instance Segmentation: "What, where, and exact shape?"
→ Output: Class + Pixel-level mask
```

### 5.5.2 Two-Stage Detectors

**R-CNN Family:**
```
R-CNN (2014):
Image → Selective Search (2000 proposals) → CNN → SVM → BBox Regression

Fast R-CNN (2015):
Image → CNN → RoI Pooling → FC → Class + BBox

Faster R-CNN (2016):
Image → CNN → RPN (Region Proposal Network) → RoI Pooling → Class + BBox
```

### 5.5.3 One-Stage Detectors (YOLO)

YOLO (You Only Look Once) - real-time detection:

```
YOLO Architecture:
Image (448×448)
    ↓
Backbone CNN (feature extraction)
    ↓
Grid (S×S) - divide image into cells
    ↓
Each cell predicts:
├── B bounding boxes (x, y, w, h, confidence)
└── C class probabilities
    ↓
Non-Maximum Suppression (NMS)
    ↓
Final detections
```

**YOLO Versions:**
- YOLOv1 (2016): Original paper
- YOLOv3 (2018): Multi-scale detection
- YOLOv5 (2020): PyTorch implementation
- YOLOv8 (2023): State-of-the-art, ultralytics

### 5.5.4 Metrics untuk Object Detection

**IoU (Intersection over Union):**
$$IoU = \frac{Area_{intersection}}{Area_{union}}$$

**mAP (mean Average Precision):**
- AP per class pada berbagai IoU thresholds
- mAP@0.5: IoU threshold 0.5
- mAP@0.5:0.95: average over IoU 0.5 to 0.95

---

## 5.6 Image Segmentation

### 5.6.1 Types of Segmentation

```
Semantic Segmentation:
├── Classify each pixel into a class
├── No distinction between instances
└── Output: H×W class labels

Instance Segmentation:
├── Semantic + instance separation
├── Different objects of same class distinguished
└── Output: H×W labels + instance IDs

Panoptic Segmentation:
├── Combines semantic and instance
├── Both "stuff" (sky, road) and "things" (car, person)
└── Output: Complete scene understanding
```

### 5.6.2 FCN (Fully Convolutional Network)

Arsitektur pertama untuk semantic segmentation:

```
Encoder-Decoder Architecture:

Encoder (Downsampling):
Image → Conv → Pool → Conv → Pool → ...
                                    ↓
                               Bottleneck
                                    ↓
Decoder (Upsampling):
... → ConvTranspose → Skip Connection → ConvTranspose → Output
```

### 5.6.3 U-Net Architecture

Popular untuk medical image segmentation:

```
U-Net Structure:
                    Encoder                Decoder
                    
Input ─────────────────────────────────────────────── Output
   │                                                    ↑
   └─Conv─Conv─Pool─┬─────────────────────┬─Up─Conv─Conv─┘
                    │                     │
                    └─Conv─Conv─Pool─┬────┼─Up─Conv─Conv─┘
                                     │    │
                                     └────┴─Bottleneck
                                     
Skip Connections: Concatenate encoder features to decoder
```

### 5.6.4 Mask R-CNN

Extends Faster R-CNN untuk instance segmentation:

```
Mask R-CNN:
Image → Backbone → RPN → RoI Align → 
    ├── Classification Head → Class
    ├── Box Regression Head → BBox
    └── Mask Head (FCN) → Binary Mask
```

---

## 5.7 Frameworks dan Tools

### 5.7.1 Deep Learning Frameworks

| Framework | Keunggulan | Use Case |
|-----------|------------|----------|
| PyTorch | Dynamic graph, research-friendly | Research, prototyping |
| TensorFlow/Keras | Production-ready, TFLite | Deployment |
| ONNX | Interoperability | Model exchange |

### 5.7.2 Libraries untuk CV

```python
# Image Classification & Transfer Learning
import torchvision.models as models
model = models.resnet50(pretrained=True)

# Object Detection
from ultralytics import YOLO
model = YOLO('yolov8n.pt')

# Segmentation
import segmentation_models_pytorch as smp
model = smp.Unet('resnet34', encoder_weights='imagenet')

# OpenCV DNN Module
net = cv2.dnn.readNetFromONNX('model.onnx')
```

---

## 5.8 Praktik Terbaik

### 5.8.1 Data Preparation

```python
# Data Augmentation dengan albumentations
import albumentations as A

transform = A.Compose([
    A.RandomRotate90(),
    A.Flip(),
    A.ColorJitter(brightness=0.2, contrast=0.2),
    A.GaussianBlur(blur_limit=3),
    A.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])
```

### 5.8.2 Training Tips

1. **Learning Rate Schedule**: Cosine annealing, step decay
2. **Batch Size**: Larger = more stable, smaller = better generalization
3. **Regularization**: Dropout, weight decay, data augmentation
4. **Mixed Precision**: FP16 untuk faster training
5. **Gradient Clipping**: Prevent exploding gradients

### 5.8.3 Model Evaluation

```python
# Classification metrics
from sklearn.metrics import classification_report, confusion_matrix

# Detection metrics  
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

# Segmentation metrics
def iou_score(pred, target):
    intersection = (pred & target).sum()
    union = (pred | target).sum()
    return intersection / union
```

---

## 5.9 Deployment

### 5.9.1 Model Optimization

```
Optimization Techniques:
├── Quantization: FP32 → INT8 (4x smaller)
├── Pruning: Remove unnecessary weights
├── Knowledge Distillation: Train smaller model
└── ONNX Export: Framework-agnostic format
```

### 5.9.2 Inference Engines

| Engine | Platform | Use Case |
|--------|----------|----------|
| TensorRT | NVIDIA GPU | High-performance inference |
| OpenVINO | Intel CPU/GPU | Edge deployment |
| TFLite | Mobile | Android/iOS |
| ONNX Runtime | Cross-platform | General purpose |

---

## Kesimpulan

Deep Learning telah merevolusi Computer Vision dengan:
1. **Automatic Feature Learning**: Tidak perlu hand-crafted features
2. **State-of-the-art Performance**: Superhuman di banyak tasks
3. **Transfer Learning**: Leverage large pre-trained models
4. **Real-time Capability**: YOLO, EfficientDet untuk real-time
5. **End-to-end Systems**: Input image → output predictions

### Trend Terkini
- Vision Transformers (ViT)
- Self-supervised learning
- Foundation models (CLIP, SAM)
- Neural Architecture Search (NAS)
- Efficient models untuk edge devices
