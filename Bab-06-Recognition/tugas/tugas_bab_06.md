# Tugas Bab 6: Recognition (Pengenalan)

## Informasi Tugas
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 6 - Recognition
- **Topik**: Image Classification, Object Detection, Segmentation
- **Waktu Pengerjaan**: 2-3 minggu

---

## Bagian A: Pertanyaan Teori (30 poin)

### A1. Instance Recognition dan BoVW (10 poin)

1. **Jelaskan langkah-langkah dalam Bag of Visual Words (BoVW):**
   - Feature extraction
   - Visual vocabulary construction
   - Histogram quantization
   - TF-IDF weighting

2. **Apa kelemahan dari BoVW? Bagaimana Spatial Pyramid Matching (SPM) memperbaikinya?**

3. **Bandingkan pendekatan instance recognition berbasis:**
   - Hand-crafted features (SIFT + BoVW)
   - Deep learning embeddings

### A2. Object Detection (10 poin)

4. **Jelaskan perbedaan antara:**
   - Two-stage detectors (R-CNN family)
   - One-stage detectors (YOLO, SSD)
   - Transformer-based detectors (DETR)

5. **Apa yang dimaksud dengan:**
   - IoU (Intersection over Union)
   - mAP (mean Average Precision)
   - Non-Maximum Suppression (NMS)

6. **Dalam Faster R-CNN, jelaskan peran dari:**
   - Region Proposal Network (RPN)
   - Anchor boxes
   - RoI Pooling vs RoI Align

### A3. Semantic dan Instance Segmentation (10 poin)

7. **Bandingkan:**
   - Semantic Segmentation
   - Instance Segmentation
   - Panoptic Segmentation

8. **Jelaskan arsitektur U-Net:**
   - Encoder-decoder structure
   - Skip connections
   - Mengapa efektif untuk medical imaging?

9. **Apa yang dimaksud dengan Atrous (Dilated) Convolution di DeepLab? Apa keuntungannya?**

---

## Bagian B: Implementasi Coding (40 poin)

### B1. Bag of Visual Words dari Scratch (15 poin)

Implementasikan sistem BoVW lengkap untuk image classification:

```python
class BagOfVisualWordsClassifier:
    """
    Complete BoVW pipeline untuk image classification
    """
    
    def __init__(self, n_clusters=500, feature_type='sift'):
        """
        Args:
            n_clusters: Vocabulary size
            feature_type: 'sift' atau 'orb'
        """
        self.n_clusters = n_clusters
        self.feature_type = feature_type
        # TODO: Initialize feature detector dan descriptor
    
    def extract_features(self, images):
        """
        Extract local features dari semua images
        
        Args:
            images: List of images
            
        Returns:
            all_descriptors: Semua descriptors digabung
            image_indices: Index image untuk setiap descriptor
        """
        # TODO: Implementasi
        pass
    
    def build_vocabulary(self, images):
        """
        Build visual vocabulary dengan K-Means
        
        Args:
            images: Training images
        """
        # TODO: Implementasi
        pass
    
    def compute_tf_idf_histogram(self, image):
        """
        Compute TF-IDF weighted histogram untuk single image
        
        Formula:
        - TF = n_ij / n_j (term frequency)
        - IDF = log(N / n_i) (inverse document frequency)
        - TF-IDF = TF * IDF
        """
        # TODO: Implementasi
        pass
    
    def fit(self, images, labels):
        """
        Training: build vocabulary dan train classifier (SVM)
        """
        # TODO: Build vocabulary
        # TODO: Compute histograms untuk semua training images
        # TODO: Train SVM classifier
        pass
    
    def predict(self, images):
        """
        Predict class labels untuk images
        """
        # TODO: Implementasi
        pass
    
    def evaluate(self, images, labels):
        """
        Evaluate dengan confusion matrix dan per-class accuracy
        """
        # TODO: Implementasi
        pass


# Testing pada Caltech-101 atau dataset custom
# TODO: Download subset of Caltech-101 (5 classes, ~50 images/class)
# TODO: Train dan evaluate BoVW classifier
# TODO: Compare dengan CNN (transfer learning)
```

**Kriteria Penilaian:**
- Feature extraction benar (3 poin)
- K-Means vocabulary (3 poin)
- TF-IDF weighting (4 poin)
- SVM training dan testing (3 poin)
- Evaluation metrics (2 poin)

### B2. Custom Object Detector (15 poin)

Implementasikan simple object detector menggunakan sliding window dan CNN classifier:

```python
class SlidingWindowDetector:
    """
    Simple object detector menggunakan sliding window
    """
    
    def __init__(self, classifier_model, class_names, image_size=(224, 224)):
        """
        Args:
            classifier_model: Trained CNN classifier
            class_names: List of class names
            image_size: Input size untuk classifier
        """
        self.model = classifier_model
        self.class_names = class_names
        self.image_size = image_size
    
    def generate_windows(self, image, scales=[1.0, 0.75, 0.5], 
                        window_size=(128, 128), stride=32):
        """
        Generate sliding windows at multiple scales
        
        Args:
            image: Input image
            scales: List of scale factors
            window_size: Base window size
            stride: Stride between windows
            
        Yields:
            window: Window image
            (x, y, w, h): Window coordinates di original image
        """
        # TODO: Implementasi multi-scale sliding window
        pass
    
    def detect(self, image, confidence_threshold=0.5, nms_threshold=0.3):
        """
        Detect objects dalam image
        
        Returns:
            boxes: Detected bounding boxes
            labels: Class labels
            scores: Confidence scores
        """
        # TODO: Implementasi
        # 1. Generate sliding windows
        # 2. Classify each window
        # 3. Filter by confidence
        # 4. Apply NMS
        pass
    
    def apply_nms(self, boxes, scores, threshold):
        """
        Non-Maximum Suppression
        """
        # TODO: Implementasi NMS dari scratch
        pass
    
    def visualize(self, image, boxes, labels, scores):
        """Visualize detections"""
        # TODO: Implementasi
        pass


# Bonus: Implementasi Selective Search untuk region proposals
class SelectiveSearchRegionProposal:
    """
    Selective Search untuk region proposals
    """
    
    def __init__(self):
        pass
    
    def generate_proposals(self, image, n_proposals=2000):
        """
        Generate region proposals menggunakan selective search
        
        Gunakan cv2.ximgproc.segmentation.createSelectiveSearchSegmentation
        """
        # TODO: Implementasi
        pass


# Testing
# TODO: Train classifier untuk 2-3 object classes
# TODO: Run sliding window detector pada test images
# TODO: Evaluate dengan mAP
```

**Kriteria Penilaian:**
- Multi-scale sliding window (5 poin)
- Classification integration (3 poin)
- NMS dari scratch (4 poin)
- Visualization (3 poin)

### B3. U-Net untuk Segmentation (10 poin)

Implementasikan U-Net dari scratch dan train pada dataset sederhana:

```python
import torch
import torch.nn as nn

class DoubleConv(nn.Module):
    """Double convolution block: Conv -> BN -> ReLU -> Conv -> BN -> ReLU"""
    
    def __init__(self, in_channels, out_channels):
        super().__init__()
        # TODO: Implementasi
        pass
    
    def forward(self, x):
        # TODO: Implementasi
        pass


class UNet(nn.Module):
    """
    U-Net architecture untuk semantic segmentation
    
    Architecture:
    - Encoder: 4 downsampling blocks
    - Bottleneck
    - Decoder: 4 upsampling blocks dengan skip connections
    - Output: 1x1 conv untuk classification
    """
    
    def __init__(self, in_channels=3, num_classes=2, features=[64, 128, 256, 512]):
        super().__init__()
        self.encoder = nn.ModuleList()
        self.decoder = nn.ModuleList()
        self.pool = nn.MaxPool2d(2, 2)
        
        # TODO: Build encoder
        # TODO: Build bottleneck
        # TODO: Build decoder
        # TODO: Final conv
    
    def forward(self, x):
        """
        Forward pass dengan skip connections
        
        Returns:
            output: Segmentation map [B, num_classes, H, W]
        """
        # TODO: Encoder pass (save skip connections)
        # TODO: Bottleneck
        # TODO: Decoder pass (concat skip connections)
        # TODO: Final classification
        pass


def dice_loss(pred, target, smooth=1e-6):
    """
    Dice Loss untuk segmentation
    
    L = 1 - (2 * |A ∩ B| + smooth) / (|A| + |B| + smooth)
    """
    # TODO: Implementasi
    pass


def train_unet(model, train_loader, val_loader, epochs=50):
    """
    Training loop untuk U-Net
    
    Features:
    - Combined loss: BCE + Dice
    - Learning rate scheduling
    - Best model checkpointing
    """
    # TODO: Implementasi
    pass


# Testing pada dataset sederhana (e.g., cell segmentation)
# TODO: Create atau download simple segmentation dataset
# TODO: Train U-Net
# TODO: Evaluate dengan IoU dan Dice score
```

**Kriteria Penilaian:**
- U-Net architecture benar (5 poin)
- Skip connections benar (2 poin)
- Dice loss (1 poin)
- Training dan evaluation (2 poin)

---

## Bagian C: Proyek Mini - Complete Recognition Pipeline (30 poin)

### Deskripsi Proyek

Bangun sistem recognition lengkap yang mencakup classification, detection, dan segmentation:

### C1. Multi-Task Recognition System (15 poin)

```python
class MultiTaskRecognitionSystem:
    """
    Unified system untuk multiple recognition tasks
    """
    
    def __init__(self, config):
        """
        Config example:
        {
            'classification': {
                'model': 'resnet50',
                'num_classes': 10,
                'pretrained': True
            },
            'detection': {
                'model': 'fasterrcnn',
                'confidence_threshold': 0.5
            },
            'segmentation': {
                'model': 'deeplabv3',
                'num_classes': 21
            }
        }
        """
        self.config = config
        # TODO: Initialize all models
    
    def classify(self, image, top_k=5):
        """
        Image classification
        
        Returns:
            predictions: List of (class_name, confidence)
        """
        # TODO: Implementasi
        pass
    
    def detect(self, image, classes_of_interest=None):
        """
        Object detection
        
        Args:
            classes_of_interest: Filter untuk specific classes
            
        Returns:
            detections: List of {box, class, score}
        """
        # TODO: Implementasi
        pass
    
    def segment(self, image, mode='semantic'):
        """
        Image segmentation
        
        Args:
            mode: 'semantic' atau 'instance'
            
        Returns:
            mask: Segmentation mask
            class_info: Per-class information
        """
        # TODO: Implementasi
        pass
    
    def analyze(self, image):
        """
        Complete analysis: classification + detection + segmentation
        
        Returns:
            {
                'classification': {...},
                'detection': {...},
                'segmentation': {...},
                'summary': 'Text description of image content'
            }
        """
        # TODO: Implementasi
        pass
    
    def visualize_all(self, image, results, save_path=None):
        """
        Comprehensive visualization
        """
        # TODO: Create multi-panel visualization
        pass
```

### C2. Custom Dataset Pipeline (10 poin)

```python
class CustomDatasetPipeline:
    """
    Pipeline untuk training pada custom dataset
    """
    
    def __init__(self, data_dir, task='classification'):
        """
        Args:
            data_dir: Directory dengan data
            task: 'classification', 'detection', atau 'segmentation'
        """
        self.data_dir = data_dir
        self.task = task
    
    def prepare_classification_data(self):
        """
        Prepare data untuk classification
        Expected structure:
        data_dir/
            train/
                class1/
                class2/
            val/
                class1/
                class2/
        """
        # TODO: Implementasi
        pass
    
    def prepare_detection_data(self, annotation_format='coco'):
        """
        Prepare data untuk detection
        Support formats: COCO, Pascal VOC, YOLO
        """
        # TODO: Implementasi
        pass
    
    def prepare_segmentation_data(self):
        """
        Prepare data untuk segmentation
        Expected: images dan corresponding masks
        """
        # TODO: Implementasi
        pass
    
    def get_dataloaders(self, batch_size=32, augmentation=True):
        """
        Create train/val/test dataloaders
        """
        # TODO: Implementasi
        pass
    
    def analyze_dataset(self):
        """
        Analisis statistik dataset:
        - Class distribution
        - Image sizes
        - Object sizes (untuk detection)
        """
        # TODO: Implementasi
        pass


class DataAugmentor:
    """
    Advanced data augmentation untuk berbagai tasks
    """
    
    def __init__(self, task='classification'):
        self.task = task
    
    def get_train_transforms(self):
        """Get training transforms"""
        # TODO: Implementasi berbagai augmentations
        pass
    
    def get_val_transforms(self):
        """Get validation transforms (minimal augmentation)"""
        # TODO: Implementasi
        pass
    
    def mixup(self, images, labels, alpha=0.2):
        """Mixup augmentation"""
        # TODO: Implementasi
        pass
    
    def cutout(self, images, n_holes=1, length=16):
        """Cutout augmentation"""
        # TODO: Implementasi
        pass
    
    def mosaic(self, images, labels):
        """Mosaic augmentation (untuk detection)"""
        # TODO: Implementasi
        pass
```

### C3. Evaluation dan Benchmarking (5 poin)

```python
class RecognitionEvaluator:
    """
    Comprehensive evaluation untuk recognition tasks
    """
    
    def __init__(self):
        pass
    
    def evaluate_classification(self, predictions, targets, class_names):
        """
        Classification metrics:
        - Accuracy (top-1, top-5)
        - Precision, Recall, F1 per class
        - Confusion matrix
        - ROC curves
        """
        # TODO: Implementasi
        pass
    
    def evaluate_detection(self, predictions, ground_truths, iou_thresholds=[0.5]):
        """
        Detection metrics:
        - mAP@IoU
        - AP per class
        - Precision-Recall curves
        """
        # TODO: Implementasi
        pass
    
    def evaluate_segmentation(self, predictions, ground_truths, num_classes):
        """
        Segmentation metrics:
        - Pixel accuracy
        - Mean IoU (mIoU)
        - Per-class IoU
        - Dice score
        """
        # TODO: Implementasi
        pass
    
    def generate_report(self, task, results, save_path='report.html'):
        """
        Generate comprehensive HTML report dengan visualizations
        """
        # TODO: Implementasi
        pass
```

---

## Format Pengumpulan

### File yang Dikumpulkan:
```
tugas_bab_06/
├── laporan.pdf
├── teori/
│   └── jawaban_teori.md
├── implementasi/
│   ├── bovw_classifier.py         # B1
│   ├── sliding_window_detector.py # B2
│   └── unet_segmentation.py       # B3
├── project/
│   ├── multi_task_system.py       # C1
│   ├── dataset_pipeline.py        # C2
│   ├── evaluator.py               # C3
│   ├── models/
│   └── outputs/
├── notebooks/
│   └── experiments.ipynb
└── README.md
```

---

## Rubrik Penilaian

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| Teori (A) | 30% | Pemahaman konsep recognition tasks |
| BoVW (B1) | 15% | Implementasi lengkap dan benar |
| Detector (B2) | 15% | Sliding window + NMS benar |
| U-Net (B3) | 10% | Architecture dan training benar |
| Multi-Task (C1) | 15% | Pipeline terintegrasi |
| Dataset (C2) | 10% | Data preparation lengkap |
| Evaluation (C3) | 5% | Metrics comprehensive |

---

## Dataset yang Disarankan

### Untuk Classification
- **CIFAR-10/100**: https://www.cs.toronto.edu/~kriz/cifar.html
- **Caltech-101**: http://www.vision.caltech.edu/Image_Datasets/Caltech101/
- **Flowers-102**: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/

### Untuk Detection
- **Pascal VOC**: http://host.robots.ox.ac.uk/pascal/VOC/
- **COCO (subset)**: https://cocodataset.org/

### Untuk Segmentation
- **Pascal VOC Segmentation**
- **Cityscapes**: https://www.cityscapes-dataset.com/
- **DRIVE (retinal vessels)**: https://drive.grand-challenge.org/

---

## Tips dan Catatan

1. ⚠️ **Mulai dengan model pretrained** - Jangan train dari scratch
2. 📊 **Analisis dataset dulu** - Pahami distribusi dan karakteristik
3. 🔄 **Augmentation penting** - Terutama untuk dataset kecil
4. 📈 **Track experiments** - Gunakan wandb atau tensorboard
5. 💾 **Checkpoint models** - Simpan best model berdasarkan validation

**Selamat mengerjakan! 🚀**
