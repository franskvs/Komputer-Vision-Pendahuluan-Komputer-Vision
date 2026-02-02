# Tugas Bab 5: Deep Learning untuk Computer Vision

## Informasi Tugas
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 5 - Deep Learning
- **Topik**: Neural Networks, CNN, dan Transfer Learning
- **Waktu Pengerjaan**: 2-3 minggu

---

## Bagian A: Pertanyaan Teori (30 poin)

### A1. Neural Networks Dasar (10 poin)

1. **Jelaskan perbedaan antara fungsi aktivasi berikut beserta kelebihan dan kekurangannya:**
   - Sigmoid
   - Tanh
   - ReLU
   - Leaky ReLU
   - Softmax

2. **Dalam backpropagation, jelaskan:**
   - Apa yang dimaksud dengan chain rule?
   - Mengapa gradien perlu di-propagate dari output ke input?
   - Apa yang terjadi jika learning rate terlalu besar atau terlalu kecil?

3. **Apa yang dimaksud dengan vanishing gradient problem? Bagaimana arsitektur modern seperti ResNet mengatasi masalah ini?**

### A2. Convolutional Neural Networks (10 poin)

4. **Jelaskan operasi konvolusi pada CNN:**
   - Bagaimana filter/kernel bekerja?
   - Apa pengaruh stride dan padding?
   - Hitung output size dari konvolusi dengan input 32x32, kernel 3x3, stride 1, padding 1

5. **Bandingkan Max Pooling dan Average Pooling:**
   - Kapan sebaiknya menggunakan masing-masing?
   - Apa dampaknya terhadap fitur yang dipelajari?

6. **Jelaskan peran dari komponen-komponen berikut dalam CNN:**
   - Batch Normalization
   - Dropout
   - Global Average Pooling

### A3. Arsitektur dan Training (10 poin)

7. **Bandingkan arsitektur VGG, ResNet, dan EfficientNet:**
   - Apa ide utama dari masing-masing arsitektur?
   - Bagaimana parameter count dibandingkan dengan akurasi?

8. **Jelaskan teknik-teknik regularisasi dalam deep learning:**
   - Data augmentation
   - L2 regularization (weight decay)
   - Early stopping
   - Dropout

9. **Apa yang dimaksud dengan transfer learning? Jelaskan kapan menggunakan:**
   - Feature extraction (freeze backbone)
   - Fine-tuning (unfreeze some layers)
   - Training from scratch

---

## Bagian B: Implementasi Coding (40 poin)

### B1. Custom Neural Network Layer (15 poin)

Implementasikan kelas `ConvolutionalLayer` menggunakan NumPy only (tanpa framework deep learning):

```python
class ConvolutionalLayer:
    """
    Implementasi layer konvolusi dari scratch
    
    Attributes:
        in_channels: Jumlah channel input
        out_channels: Jumlah filter (output channels)
        kernel_size: Ukuran filter (assume square)
        stride: Stride konvolusi
        padding: Zero padding
    """
    
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        """
        Initialize filters dengan Xavier initialization
        Shape weights: (out_channels, in_channels, kernel_size, kernel_size)
        """
        # TODO: Implementasi
        pass
    
    def forward(self, x):
        """
        Forward pass konvolusi
        
        Args:
            x: Input tensor shape (batch_size, in_channels, H, W)
            
        Returns:
            output: Shape (batch_size, out_channels, H_out, W_out)
        """
        # TODO: Implementasi dengan loop atau im2col
        pass
    
    def backward(self, grad_output):
        """
        Backward pass untuk menghitung gradient
        
        Args:
            grad_output: Gradient dari layer berikutnya
            
        Returns:
            grad_input: Gradient untuk layer sebelumnya
            grad_weights: Gradient untuk update weights
        """
        # TODO: Implementasi
        pass


# Testing
conv = ConvolutionalLayer(3, 16, kernel_size=3, stride=1, padding=1)
x = np.random.randn(2, 3, 32, 32)  # batch=2, channels=3, 32x32
output = conv.forward(x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")  # Expected: (2, 16, 32, 32)
```

**Kriteria Penilaian:**
- Forward pass benar (8 poin)
- Backward pass benar (5 poin)
- Testing dan verifikasi (2 poin)

### B2. CNN Classifier dengan PyTorch (15 poin)

Bangun dan train CNN classifier untuk dataset Fashion-MNIST:

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

class FashionCNN(nn.Module):
    """
    CNN untuk klasifikasi Fashion-MNIST (10 kelas)
    
    Requirements:
    - Minimal 3 convolutional blocks
    - Gunakan BatchNorm dan Dropout
    - Global Average Pooling sebelum FC layer
    - Target: >90% test accuracy
    """
    
    def __init__(self, num_classes=10):
        super().__init__()
        # TODO: Implementasi arsitektur
        pass
    
    def forward(self, x):
        # TODO: Implementasi forward pass
        pass


def train_model(model, train_loader, val_loader, epochs=20):
    """
    Training loop dengan:
    - Learning rate scheduling
    - Early stopping berdasarkan validation accuracy
    - Best model checkpoint
    
    Returns:
        history: Dictionary berisi train/val loss dan accuracy per epoch
    """
    # TODO: Implementasi
    pass


def evaluate_model(model, test_loader):
    """
    Evaluasi model pada test set
    
    Returns:
        accuracy: Overall accuracy
        class_accuracy: Per-class accuracy
        confusion_matrix: Confusion matrix
    """
    # TODO: Implementasi
    pass


# Main
if __name__ == "__main__":
    # Load Fashion-MNIST
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    train_dataset = torchvision.datasets.FashionMNIST(
        './data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.FashionMNIST(
        './data', train=False, download=True, transform=transform)
    
    # Split train -> train/val
    # TODO: Implement train/val split
    
    # Create dataloaders
    # TODO: Create dataloaders
    
    # Create and train model
    model = FashionCNN()
    history = train_model(model, train_loader, val_loader)
    
    # Evaluate
    results = evaluate_model(model, test_loader)
    print(f"Test Accuracy: {results['accuracy']:.2%}")
    
    # Plot training history
    # TODO: Plot loss and accuracy curves
    
    # Plot confusion matrix
    # TODO: Plot confusion matrix
```

**Kriteria Penilaian:**
- Arsitektur CNN yang baik (5 poin)
- Training loop lengkap dengan LR scheduling dan early stopping (5 poin)
- Evaluasi dan visualisasi (3 poin)
- Mencapai >90% accuracy (2 poin)

### B3. Transfer Learning untuk Custom Dataset (10 poin)

Implementasikan transfer learning untuk klasifikasi gambar custom:

```python
class TransferLearningClassifier:
    """
    Transfer learning classifier menggunakan pretrained model
    
    Features:
    - Support multiple backbones (ResNet18, ResNet50, VGG16, EfficientNet)
    - Feature extraction mode dan fine-tuning mode
    - Data augmentation untuk small datasets
    """
    
    def __init__(self, backbone='resnet18', num_classes=5, pretrained=True):
        """
        Initialize dengan pretrained backbone
        
        Args:
            backbone: Nama backbone ('resnet18', 'resnet50', 'vgg16', 'efficientnet_b0')
            num_classes: Jumlah kelas output
            pretrained: Gunakan pretrained weights
        """
        # TODO: Implementasi
        pass
    
    def freeze_backbone(self):
        """Freeze semua layer kecuali classifier"""
        pass
    
    def unfreeze_backbone(self, num_layers=None):
        """
        Unfreeze backbone layers untuk fine-tuning
        
        Args:
            num_layers: Jumlah layer terakhir yang di-unfreeze (None = semua)
        """
        pass
    
    def get_transforms(self, mode='train'):
        """
        Get data transforms
        
        Args:
            mode: 'train' atau 'val'/'test'
        """
        # TODO: Implementasi dengan augmentation untuk train
        pass
    
    def train_feature_extraction(self, train_loader, val_loader, epochs=10):
        """Train dengan backbone frozen"""
        pass
    
    def train_fine_tuning(self, train_loader, val_loader, epochs=10, lr=1e-4):
        """Fine-tune dengan backbone unfrozen"""
        pass


# Demo dengan flowers dataset atau custom dataset
# TODO: Implementasi training pipeline
```

**Kriteria Penilaian:**
- Multiple backbone support (3 poin)
- Feature extraction dan fine-tuning (4 poin)
- Data augmentation yang tepat (3 poin)

---

## Bagian C: Proyek Mini - Image Classification System (30 poin)

### Deskripsi Proyek

Bangun sistem klasifikasi gambar lengkap dengan fitur-fitur berikut:

### C1. Arsitektur dan Training (15 poin)

```python
class ImageClassificationSystem:
    """
    Sistem klasifikasi gambar end-to-end
    """
    
    def __init__(self, config):
        """
        Initialize system dengan konfigurasi
        
        Config example:
        config = {
            'model_name': 'resnet18',
            'num_classes': 10,
            'image_size': 224,
            'batch_size': 32,
            'learning_rate': 0.001,
            'epochs': 50,
            'data_augmentation': True,
            'pretrained': True,
            'use_mixup': False,
            'use_cutout': False
        }
        """
        self.config = config
        # TODO: Implementasi
    
    def prepare_data(self, data_dir, val_split=0.2):
        """
        Prepare dataset dari directory structure:
        data_dir/
            class1/
                img1.jpg
                img2.jpg
            class2/
                ...
        """
        # TODO: Implementasi dengan ImageFolder dan transforms
        pass
    
    def build_model(self):
        """Build model berdasarkan config"""
        pass
    
    def train(self, train_loader, val_loader):
        """
        Full training pipeline dengan:
        - Mixed precision training (optional)
        - Learning rate finder
        - Cosine annealing LR schedule
        - Mixup/Cutout augmentation (optional)
        - Tensorboard logging
        - Model checkpointing
        """
        pass
    
    def evaluate(self, test_loader):
        """
        Comprehensive evaluation dengan:
        - Overall metrics (accuracy, precision, recall, F1)
        - Per-class metrics
        - Confusion matrix
        - ROC curves (untuk binary atau one-vs-rest)
        - Grad-CAM visualizations
        """
        pass
    
    def predict(self, image_path):
        """
        Single image prediction dengan confidence scores
        """
        pass
    
    def export_model(self, format='onnx'):
        """Export model untuk deployment (ONNX, TorchScript)"""
        pass
```

### C2. Visualisasi dan Interpretability (10 poin)

```python
class ModelInterpretability:
    """
    Tools untuk interpretasi model CNN
    """
    
    def __init__(self, model):
        self.model = model
    
    def grad_cam(self, image, target_layer, target_class=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            image: Input image tensor
            target_layer: Layer untuk generate CAM
            target_class: Target class (None = predicted class)
            
        Returns:
            heatmap: Grad-CAM heatmap
            overlay: Heatmap overlaid on image
        """
        # TODO: Implementasi Grad-CAM
        pass
    
    def feature_visualization(self, layer_name, filter_idx):
        """
        Visualize apa yang dipelajari oleh filter tertentu
        menggunakan activation maximization
        """
        pass
    
    def saliency_map(self, image, target_class=None):
        """
        Generate saliency map menggunakan gradient
        """
        pass
    
    def visualize_filters(self, layer_name):
        """Visualize convolutional filters"""
        pass
    
    def plot_feature_maps(self, image, layer_names):
        """Plot feature maps dari multiple layers"""
        pass
```

### C3. Deployment Ready (5 poin)

```python
class ImageClassificationAPI:
    """
    API wrapper untuk deployment
    """
    
    def __init__(self, model_path, class_names):
        """Load trained model"""
        pass
    
    def preprocess(self, image):
        """Preprocess image untuk inference"""
        pass
    
    def predict(self, image, top_k=5):
        """
        Returns:
            predictions: List of (class_name, confidence) tuples
        """
        pass
    
    def predict_batch(self, images):
        """Batch prediction"""
        pass


# Flask/FastAPI endpoint example (optional bonus)
from flask import Flask, request, jsonify

app = Flask(__name__)
classifier = ImageClassificationAPI('model.pth', class_names)

@app.route('/predict', methods=['POST'])
def predict():
    # TODO: Implementasi endpoint
    pass
```

---

## Format Pengumpulan

### File yang Dikumpulkan:
```
tugas_bab_05/
├── laporan.pdf                     # Laporan tugas
├── teori/
│   └── jawaban_teori.md            # Jawaban Bagian A
├── implementasi/
│   ├── conv_layer.py               # Bagian B1
│   ├── fashion_cnn.py              # Bagian B2
│   └── transfer_learning.py        # Bagian B3
├── project/
│   ├── classification_system.py    # Bagian C1
│   ├── interpretability.py         # Bagian C2
│   ├── api.py                      # Bagian C3
│   ├── models/                     # Saved models
│   └── outputs/                    # Visualizations
├── notebooks/
│   └── experiments.ipynb           # Jupyter notebook eksperimen
└── README.md                       # Dokumentasi
```

### Kriteria Laporan:
1. **Pendahuluan**: Latar belakang dan tujuan
2. **Metodologi**: Arsitektur model, hyperparameters, training strategy
3. **Hasil dan Analisis**: 
   - Training curves
   - Test metrics
   - Confusion matrix
   - Grad-CAM visualizations
4. **Diskusi**: 
   - Apa yang berhasil dan tidak
   - Perbandingan berbagai arsitektur/settings
5. **Kesimpulan**: Rangkuman dan future work

---

## Rubrik Penilaian

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| Teori (A) | 30% | Kebenaran konsep, kedalaman pemahaman |
| Conv Layer (B1) | 15% | Implementasi benar, backward pass benar |
| Fashion CNN (B2) | 15% | Arsitektur baik, training proper, >90% acc |
| Transfer Learning (B3) | 10% | Multiple backbones, freeze/unfreeze benar |
| Classification System (C1) | 15% | Pipeline lengkap, training proper |
| Interpretability (C2) | 10% | Grad-CAM benar, visualisasi informatif |
| Deployment (C3) | 5% | API working, preprocessing benar |

---

## Referensi untuk Tugas

1. **PyTorch Tutorials**: https://pytorch.org/tutorials/
2. **Grad-CAM Paper**: https://arxiv.org/abs/1610.02391
3. **Transfer Learning Guide**: https://cs231n.github.io/transfer-learning/
4. **Fashion-MNIST**: https://github.com/zalandoresearch/fashion-mnist

---

## Catatan Penting

1. ⚠️ **Kode harus original** - Plagiarism akan mendapat nilai 0
2. 📊 **Dokumentasi penting** - Jelaskan setiap keputusan desain
3. 🔬 **Eksperimen sistematis** - Coba berbagai hyperparameters
4. 📈 **Visualisasi informatif** - Graphs harus labeled dengan baik
5. 💻 **GPU opsional** - Tugas bisa dikerjakan dengan CPU (lebih lambat)

**Selamat mengerjakan! 🚀**
