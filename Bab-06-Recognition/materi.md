# Bab 6: Recognition (Pengenalan)

## Daftar Isi
1. [Pendahuluan](#1-pendahuluan)
2. [Instance Recognition](#2-instance-recognition)
3. [Image Classification](#3-image-classification)
4. [Object Detection](#4-object-detection)
5. [Semantic Segmentation](#5-semantic-segmentation)
6. [Instance Segmentation](#6-instance-segmentation)
7. [Video Understanding](#7-video-understanding)
8. [Vision-Language Models](#8-vision-language-models)

---

## 1. Pendahuluan

### 1.1 Apa itu Recognition?

**Recognition** (pengenalan) adalah kemampuan sistem komputer untuk mengidentifikasi dan mengkategorikan objek, scene, atau aktivitas dalam gambar atau video. Ini merupakan salah satu task fundamental dalam computer vision.

### 1.2 Jenis-jenis Task Recognition

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIERARKI RECOGNITION TASKS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Image-level:                                                    │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Image Classification: "Gambar ini adalah kucing" │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  Object-level:                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Object Detection: "Kucing di posisi (x,y,w,h)"   │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  Pixel-level:                                                    │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Semantic Segmentation: "Pixel ini adalah kucing" │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  Instance-level:                                                 │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Instance Segmentation: "Pixel ini adalah         │           │
│  │                         kucing ke-2"             │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Evolusi Pendekatan Recognition

| Era | Pendekatan | Karakteristik |
|-----|------------|---------------|
| 1960-1990 | Rule-based | Template matching, geometric models |
| 1990-2012 | Hand-crafted features | SIFT, HOG + SVM/Random Forest |
| 2012-sekarang | Deep Learning | CNN, Transformers, end-to-end |

---

## 2. Instance Recognition

### 2.1 Definisi

**Instance Recognition** adalah task mengenali objek spesifik yang sama (bukan hanya kategori yang sama). Contoh: mengenali Menara Eiffel, bukan hanya "menara".

### 2.2 Pendekatan Berbasis Fitur

```
┌─────────────────────────────────────────────────────────────────┐
│               PIPELINE INSTANCE RECOGNITION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query Image      Database Images                                │
│       │                │                                         │
│       ▼                ▼                                         │
│  ┌─────────┐     ┌─────────┐                                    │
│  │ Feature │     │ Feature │                                    │
│  │ Extract │     │ Extract │                                    │
│  └────┬────┘     └────┬────┘                                    │
│       │               │                                          │
│       ▼               ▼                                          │
│  ┌─────────┐     ┌─────────┐                                    │
│  │ Describe│     │ Describe│                                    │
│  │ (SIFT)  │     │ (SIFT)  │                                    │
│  └────┬────┘     └────┬────┘                                    │
│       │               │                                          │
│       └───────┬───────┘                                          │
│               ▼                                                  │
│        ┌──────────────┐                                         │
│        │   Matching   │                                         │
│        └──────┬───────┘                                         │
│               ▼                                                  │
│        ┌──────────────┐                                         │
│        │ Verification │                                         │
│        │  (RANSAC)    │                                         │
│        └──────┬───────┘                                         │
│               ▼                                                  │
│          Best Match                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Bag of Visual Words (BoVW)

**Bag of Visual Words** adalah representasi gambar yang terinspirasi dari text retrieval.

**Langkah-langkah:**

1. **Extract Local Features**: Deteksi keypoints dan compute descriptors (SIFT)
2. **Build Visual Vocabulary**: Clustering descriptors menjadi "visual words"
3. **Quantization**: Assign setiap descriptor ke visual word terdekat
4. **Histogram**: Hitung histogram frekuensi visual words

```
Gambar → [Feature Extraction] → [Descriptors]
                                      │
                                      ▼
                              [K-Means Clustering]
                                      │
                                      ▼
                              [Visual Vocabulary]
                              (k visual words)
                                      │
                                      ▼
         Gambar Baru → [Quantize] → [Histogram]
                                      │
                                      ▼
                              [Image Retrieval]
```

**TF-IDF Weighting:**

$$w_{i,j} = \frac{n_{i,j}}{n_j} \times \log\frac{N}{n_i}$$

Di mana:
- $n_{i,j}$: jumlah kemunculan word $i$ di gambar $j$
- $n_j$: total words di gambar $j$
- $N$: total gambar dalam database
- $n_i$: jumlah gambar yang mengandung word $i$

### 2.4 Deep Learning untuk Instance Recognition

Modern approaches menggunakan **deep embeddings**:

```python
# Contoh dengan pretrained CNN
import torch
from torchvision import models, transforms

# Load pretrained model
model = models.resnet50(pretrained=True)
# Remove final classification layer
model = torch.nn.Sequential(*list(model.children())[:-1])

# Extract embedding
def get_embedding(image):
    with torch.no_grad():
        embedding = model(image)
        embedding = embedding.flatten()
        # L2 normalize
        embedding = embedding / embedding.norm()
    return embedding

# Similarity via cosine distance
similarity = torch.dot(emb1, emb2)
```

---

## 3. Image Classification

### 3.1 Problem Formulation

**Input**: Gambar $I \in \mathbb{R}^{H \times W \times C}$

**Output**: Label kelas $y \in \{1, 2, ..., K\}$ atau distribusi probabilitas $P(y|I)$

### 3.2 Traditional Approaches

#### Bag of Visual Words + SVM

```
┌────────────────────────────────────────────────────────────────┐
│                    BOVW + SVM PIPELINE                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Training:                                                      │
│  ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐   │
│  │ Images  │───▶│  SIFT   │───▶│ K-Means  │───▶│ Histogram│   │
│  └─────────┘    │ Extract │    │ Vocab    │    │ Features │   │
│                 └─────────┘    └──────────┘    └────┬─────┘   │
│                                                      │         │
│                                                      ▼         │
│                                               ┌──────────┐     │
│                                               │ Train SVM│     │
│                                               └──────────┘     │
│                                                                 │
│  Testing:                                                       │
│  ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐   │
│  │  Image  │───▶│  SIFT   │───▶│ Quantize │───▶│ Classify │   │
│  └─────────┘    │ Extract │    │ Histogram│    │   SVM    │   │
│                 └─────────┘    └──────────┘    └──────────┘   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

#### Spatial Pyramid Matching (SPM)

SPM menambahkan informasi spatial ke BoVW:

```
Level 0: 1×1 grid  → 1 histogram
Level 1: 2×2 grid  → 4 histograms
Level 2: 4×4 grid  → 16 histograms
                      ↓
Concatenate → Final Feature Vector
```

### 3.3 CNN-based Classification

#### Classic Architectures

| Model | Year | Top-5 Error (ImageNet) | Parameters |
|-------|------|------------------------|------------|
| AlexNet | 2012 | 15.3% | 60M |
| VGG-16 | 2014 | 7.3% | 138M |
| GoogLeNet | 2014 | 6.7% | 4M |
| ResNet-152 | 2015 | 3.6% | 60M |
| EfficientNet-B7 | 2019 | 2.9% | 66M |

#### Training Pipeline Modern

```python
# Modern training dengan PyTorch
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms, datasets, models

# Data Augmentation
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225]),
    transforms.RandomErasing(p=0.5)  # Cutout-like
])

# Mixup Augmentation
def mixup_data(x, y, alpha=1.0):
    lam = np.random.beta(alpha, alpha)
    batch_size = x.size(0)
    index = torch.randperm(batch_size)
    mixed_x = lam * x + (1 - lam) * x[index]
    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam

# Label Smoothing
class LabelSmoothingCrossEntropy(nn.Module):
    def __init__(self, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing
    
    def forward(self, pred, target):
        n_classes = pred.size(-1)
        confidence = 1.0 - self.smoothing
        smooth_value = self.smoothing / (n_classes - 1)
        one_hot = torch.full_like(pred, smooth_value)
        one_hot.scatter_(1, target.unsqueeze(1), confidence)
        return torch.mean(torch.sum(-one_hot * F.log_softmax(pred, dim=1), dim=1))
```

### 3.4 Vision Transformers (ViT)

**Vision Transformer** menerapkan arsitektur Transformer untuk image classification:

```
┌─────────────────────────────────────────────────────────────────┐
│                    VISION TRANSFORMER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input Image (224×224)                                          │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Patch Embed  │  → (224/16)² = 196 patches                    │
│  │  16×16       │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  [CLS] + 196 patch tokens + Position Embeddings                 │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────┐                                            │
│  │ Transformer     │  ×L layers                                 │
│  │ Encoder Block   │                                            │
│  │ ┌─────────────┐ │                                            │
│  │ │ Multi-Head  │ │                                            │
│  │ │ Attention   │ │                                            │
│  │ └─────────────┘ │                                            │
│  │ ┌─────────────┐ │                                            │
│  │ │     MLP     │ │                                            │
│  │ └─────────────┘ │                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  [CLS] token → MLP Head → Class Probabilities                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Object Detection

### 4.1 Problem Formulation

**Input**: Gambar $I$

**Output**: Set bounding boxes $\{(x, y, w, h, c, p)\}$ di mana:
- $(x, y)$: koordinat center atau corner
- $(w, h)$: width dan height
- $c$: class label
- $p$: confidence score

### 4.2 Evaluasi: Intersection over Union (IoU)

$$IoU = \frac{Area_{intersection}}{Area_{union}}$$

```
    ┌─────────────┐
    │   Box A     │
    │   ┌─────┼───┼───┐
    │   │/////│   │   │
    └───┼─────┘   │   │
        │ Intersection│
        │         │   │
        └─────────┴───┘
              Box B

IoU = Area(∩) / Area(∪)
```

### 4.3 Two-Stage Detectors

#### R-CNN Family

```
┌─────────────────────────────────────────────────────────────────┐
│                     R-CNN EVOLUTION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  R-CNN (2014):                                                  │
│  Image → [Selective Search] → 2000 proposals                    │
│          → [CNN per proposal] → [SVM] → Boxes                   │
│  🐌 Sangat lambat (47s per image)                               │
│                                                                  │
│  Fast R-CNN (2015):                                             │
│  Image → [CNN] → Feature Map → [RoI Pooling] → [FC] → Boxes    │
│          ↑                                                       │
│     Selective Search proposals                                   │
│  ⚡ Lebih cepat (2s per image)                                  │
│                                                                  │
│  Faster R-CNN (2015):                                           │
│  Image → [CNN] → Feature Map → [RPN] → Proposals                │
│                        ↓                                         │
│                  [RoI Pooling] → [FC] → Boxes                   │
│  🚀 Real-time capable (0.2s per image)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Region Proposal Network (RPN)

```python
class RPN(nn.Module):
    def __init__(self, in_channels, num_anchors):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, 512, 3, padding=1)
        self.cls_layer = nn.Conv2d(512, num_anchors * 2, 1)  # obj/bg
        self.reg_layer = nn.Conv2d(512, num_anchors * 4, 1)  # dx,dy,dw,dh
    
    def forward(self, feature_map):
        x = F.relu(self.conv(feature_map))
        objectness = self.cls_layer(x)
        box_regression = self.reg_layer(x)
        return objectness, box_regression
```

### 4.4 One-Stage Detectors

#### YOLO (You Only Look Once)

```
┌─────────────────────────────────────────────────────────────────┐
│                      YOLO ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input Image (448×448)                                          │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ CNN Backbone │                                               │
│  │  (Darknet)   │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  S×S Grid (7×7)                                                 │
│  Setiap cell prediksi:                                          │
│  - B bounding boxes (x, y, w, h, confidence) × B                │
│  - C class probabilities                                        │
│                                                                  │
│  Output: S × S × (B×5 + C)                                      │
│          7 × 7 × (2×5 + 20) = 7 × 7 × 30                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**YOLO Loss Function:**

$$L = \lambda_{coord} L_{coord} + L_{obj} + \lambda_{noobj} L_{noobj} + L_{class}$$

#### SSD (Single Shot Detector)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SSD MULTI-SCALE DETECTION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VGG-16 Base                                                    │
│       │                                                          │
│       ├──────────────────────────────────────────────────────┐  │
│       │              Feature Maps at Multiple Scales          │  │
│       ▼                                                       │  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │ 38×38   │  │ 19×19   │  │ 10×10   │  │  5×5    │  ...    │  │
│  │ (small) │  │         │  │         │  │ (large) │         │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘         │  │
│       │            │            │            │               │  │
│       ▼            ▼            ▼            ▼               │  │
│     Conv         Conv         Conv         Conv              │  │
│   predictions  predictions  predictions  predictions         │  │
│       │            │            │            │               │  │
│       └────────────┴────────────┴────────────┘               │  │
│                         │                                     │  │
│                         ▼                                     │  │
│                      NMS → Final Detections                   │  │
│                                                               │  │
└───────────────────────────────────────────────────────────────┘
```

### 4.5 Modern Detectors

#### YOLO v4/v5/v8

Improvements:
- **CSPDarknet** backbone
- **PANet** neck untuk feature aggregation
- **Mosaic** augmentation
- **Self-adversarial training**

#### DETR (Detection Transformer)

```
Image → CNN Backbone → Transformer Encoder/Decoder → Set Predictions
                                    ↓
                        Object Queries (learnable)
                                    ↓
                        Bipartite Matching Loss
```

---

## 5. Semantic Segmentation

### 5.1 Problem Formulation

**Input**: Gambar $I \in \mathbb{R}^{H \times W \times 3}$

**Output**: Label map $L \in \{0, 1, ..., K\}^{H \times W}$

Setiap pixel diberi label kelas.

### 5.2 Fully Convolutional Networks (FCN)

```
┌─────────────────────────────────────────────────────────────────┐
│                           FCN                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input Image                                                     │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────────────────────────────┐                     │
│  │         CNN Encoder (VGG)              │                     │
│  │  Conv → Pool → Conv → Pool → Conv      │                     │
│  │  (resolusi menurun)                    │                     │
│  └────────────────┬───────────────────────┘                     │
│                   │                                              │
│                   ▼                                              │
│  ┌────────────────────────────────────────┐                     │
│  │         1×1 Conv (classifier)          │                     │
│  └────────────────┬───────────────────────┘                     │
│                   │                                              │
│                   ▼                                              │
│  ┌────────────────────────────────────────┐                     │
│  │      Upsampling (Deconv/Bilinear)      │                     │
│  └────────────────┬───────────────────────┘                     │
│                   │                                              │
│                   ▼                                              │
│           Segmentation Map                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 U-Net

**U-Net** menggunakan encoder-decoder dengan skip connections:

```
┌─────────────────────────────────────────────────────────────────┐
│                         U-NET                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│     Encoder                              Decoder                 │
│                                                                  │
│  ┌──────────┐                          ┌──────────┐             │
│  │ 64×64×64 │─────────────────────────▶│ 64×64×64 │             │
│  └────┬─────┘        Skip              └────▲─────┘             │
│       │ Pool                                │ UpConv            │
│       ▼                                     │                    │
│  ┌──────────┐                          ┌──────────┐             │
│  │32×32×128 │─────────────────────────▶│32×32×128 │             │
│  └────┬─────┘        Skip              └────▲─────┘             │
│       │ Pool                                │ UpConv            │
│       ▼                                     │                    │
│  ┌──────────┐                          ┌──────────┐             │
│  │16×16×256 │─────────────────────────▶│16×16×256 │             │
│  └────┬─────┘        Skip              └────▲─────┘             │
│       │ Pool                                │ UpConv            │
│       ▼                                     │                    │
│  ┌──────────┐                          ┌──────────┐             │
│  │ 8×8×512  │─────────────────────────▶│ 8×8×512  │             │
│  └────┬─────┘                          └────▲─────┘             │
│       │                                     │                    │
│       └──────────┐  Bottleneck  ┌──────────┘                    │
│                  ▼              │                                │
│              ┌──────────┐      │                                │
│              │ 4×4×1024 │──────┘                                │
│              └──────────┘                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.4 DeepLab Series

**Key Innovations:**

1. **Atrous (Dilated) Convolution**: Memperbesar receptive field tanpa mengurangi resolusi

```
Standard 3×3 conv (dilation=1):
■ ■ ■
■ ■ ■
■ ■ ■

Dilated 3×3 conv (dilation=2):
■ □ ■ □ ■
□ □ □ □ □
■ □ ■ □ ■
□ □ □ □ □
■ □ ■ □ ■
```

2. **ASPP (Atrous Spatial Pyramid Pooling)**:

```
Feature Map
     │
     ├─→ [1×1 Conv] ─────────────────┐
     ├─→ [Atrous 3×3, rate=6] ───────┤
     ├─→ [Atrous 3×3, rate=12] ──────┼─→ Concat → 1×1 Conv
     ├─→ [Atrous 3×3, rate=18] ──────┤
     └─→ [Global Avg Pool] ──────────┘
```

### 5.5 Loss Functions untuk Segmentation

**Cross-Entropy Loss:**
$$L_{CE} = -\frac{1}{N}\sum_{i=1}^{N} \sum_{c=1}^{C} y_{i,c} \log(p_{i,c})$$

**Dice Loss:**
$$L_{Dice} = 1 - \frac{2|A \cap B|}{|A| + |B|} = 1 - \frac{2\sum_i p_i g_i}{\sum_i p_i + \sum_i g_i}$$

**Focal Loss** (untuk class imbalance):
$$L_{Focal} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$

---

## 6. Instance Segmentation

### 6.1 Problem Formulation

Kombinasi object detection dan semantic segmentation:
- Detect individual objects
- Segment setiap instance secara terpisah

### 6.2 Mask R-CNN

```
┌─────────────────────────────────────────────────────────────────┐
│                       MASK R-CNN                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Image → Backbone (ResNet + FPN) → Feature Maps                 │
│                         │                                        │
│                         ▼                                        │
│                  Region Proposal Network                         │
│                         │                                        │
│                         ▼                                        │
│                  RoI Proposals                                   │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                            │
│              │     RoIAlign        │  (preserve spatial info)   │
│              └──────────┬──────────┘                            │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         │               │               │                        │
│         ▼               ▼               ▼                        │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│    │  Class  │    │  BBox   │    │  Mask   │                   │
│    │  Head   │    │  Head   │    │  Head   │                   │
│    └────┬────┘    └────┬────┘    └────┬────┘                   │
│         │              │              │                          │
│         ▼              ▼              ▼                          │
│      Classes        Boxes         Masks                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**RoIAlign vs RoIPool:**
- RoIPool: Quantization menyebabkan misalignment
- RoIAlign: Bilinear interpolation, preserves spatial accuracy

### 6.3 Panoptic Segmentation

Menggabungkan semantic dan instance segmentation:
- **Things**: Countable objects (cars, people) → instance segmentation
- **Stuff**: Uncountable regions (sky, road) → semantic segmentation

---

## 7. Video Understanding

### 7.1 Action Recognition

**Approaches:**
1. **Two-Stream Networks**: Spatial (RGB) + Temporal (Optical Flow)
2. **3D Convolutions**: C3D, I3D
3. **Transformers**: Video Transformers, TimeSformer

### 7.2 Video Object Segmentation

Track dan segment objects across frames.

### 7.3 Action Detection

Localize actions in space and time.

---

## 8. Vision-Language Models

### 8.1 CLIP (Contrastive Language-Image Pre-training)

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIP                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Image Encoder          Text Encoder                           │
│   (Vision Transformer)   (Transformer)                          │
│        │                      │                                  │
│        ▼                      ▼                                  │
│   Image Embedding        Text Embedding                         │
│        │                      │                                  │
│        └──────────┬───────────┘                                 │
│                   │                                              │
│                   ▼                                              │
│          Contrastive Loss                                        │
│    (match images with descriptions)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Zero-shot Classification:**
```python
# CLIP zero-shot classification
import clip

model, preprocess = clip.load("ViT-B/32")

# Create text prompts for classes
class_names = ["cat", "dog", "bird"]
text_inputs = torch.cat([
    clip.tokenize(f"a photo of a {c}") for c in class_names
])

# Compute features
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_inputs)

# Compute similarity
similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
```

---

## Ringkasan

| Task | Input | Output | Aplikasi |
|------|-------|--------|----------|
| Instance Recognition | Query + DB | Matching | Image retrieval |
| Image Classification | Image | Class label | Photo tagging |
| Object Detection | Image | Bounding boxes | Autonomous driving |
| Semantic Segmentation | Image | Pixel labels | Medical imaging |
| Instance Segmentation | Image | Instance masks | Robotics |
| Panoptic Segmentation | Image | All pixels labeled | Scene understanding |

---

## Latihan Mandiri

1. Implementasikan Bag of Visual Words untuk image retrieval
2. Train CNN classifier pada CIFAR-10 hingga >90% accuracy
3. Implementasikan YOLO atau SSD dari paper
4. Fine-tune Mask R-CNN pada custom dataset
5. Gunakan CLIP untuk zero-shot classification

---

*Referensi: Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Edition. Chapter 6.*
