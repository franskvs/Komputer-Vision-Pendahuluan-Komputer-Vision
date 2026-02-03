# PROJECT BAB 5: DeepVision - Sistem Klasifikasi Produk Otomatis

## Latar Belakang Cerita

**PT. SmartRetail Indonesia** adalah perusahaan retail modern yang mengoperasikan 50+ toko di seluruh Indonesia. Mereka menghadapi tantangan dalam proses inventaris produk yang masih dilakukan secara manual, memakan waktu lama dan rentan kesalahan.

**Tantangan yang Dihadapi:**
1. **Inventory Check**: Staf harus mengecek ribuan produk secara manual
2. **Misplaced Products**: Produk sering tertukar posisi di rak
3. **Stock Counting**: Menghitung stok memakan waktu berjam-jam
4. **Quality Control**: Produk rusak/kadaluarsa sulit terdeteksi

**Solusi yang Dibutuhkan:**
Sistem AI berbasis Deep Learning yang dapat:
- Mengklasifikasikan produk secara otomatis dari foto
- Mendeteksi produk pada rak toko (object detection)
- Menghitung jumlah produk tertentu
- Berjalan real-time pada perangkat edge (efficient inference)

---

## Deskripsi Project

Mahasiswa diminta mengembangkan **DeepVision** - sistem klasifikasi dan deteksi produk otomatis yang terdiri dari 3 modul utama:

### Modul 1: Product Classifier (Transfer Learning)
Sistem klasifikasi produk menggunakan transfer learning untuk mengkategorikan produk ke dalam minimal 5 kategori.

### Modul 2: Shelf Detector (Object Detection)
Sistem deteksi produk pada rak menggunakan YOLO untuk mendeteksi dan menghitung produk.

### Modul 3: Deployment Pipeline (ONNX Export)
Pipeline deployment yang mengexport model ke ONNX dan menjalankan inference dengan OpenCV DNN.

---

## Spesifikasi Teknis

### Modul 1: Product Classifier

**Dataset Requirements:**
- Minimal 5 kategori produk (contoh: Minuman, Snack, Sabun, Mie Instan, Tissue)
- Minimal 50 gambar per kategori
- Split: 80% training, 20% validation

**Model Specifications:**
```
Input: 224×224×3 RGB image
Output: Probability distribution over N classes

Architecture Options:
├── MobileNetV2 (recommended untuk edge)
├── ResNet18/34
├── EfficientNet-B0
└── Custom architecture (bonus)
```

**Training Requirements:**
- Transfer learning dari ImageNet weights
- Data augmentation (minimal: flip, rotation, color jitter)
- Early stopping untuk prevent overfitting
- Save best model checkpoint

**Evaluation Metrics:**
- Accuracy ≥ 85% pada validation set
- Confusion matrix analysis
- Per-class precision dan recall

**Deliverables:**
```
modul1_classifier/
├── data/
│   ├── train/
│   │   ├── kategori1/
│   │   ├── kategori2/
│   │   └── ...
│   └── val/
├── train_classifier.py      # Training script
├── evaluate_classifier.py   # Evaluation script
├── classifier_demo.py       # Demo inference
├── best_model.pth          # Trained model weights
└── training_log.txt        # Training history
```

---

### Modul 2: Shelf Detector

**Dataset Requirements:**
- Gambar rak toko dengan berbagai produk
- Minimal 100 gambar untuk training
- Annotations dalam format YOLO (txt per image)
- Minimal 3 classes untuk deteksi

**Model Specifications:**
```
Input: 640×640 RGB image
Output: List of detections (class, confidence, bbox, [mask])

Model Options:
├── YOLOv8n (nano - fastest)
├── YOLOv8s (small - balanced)
└── YOLOv8n-seg (dengan segmentation)
```

**Training Requirements:**
- Fine-tune dari COCO pretrained weights
- Training minimal 50 epochs
- Augmentation: mosaic, mixup, hsv augment
- Validation setiap epoch

**Evaluation Metrics:**
- mAP@0.5 ≥ 0.6
- mAP@0.5:0.95 reported
- Per-class AP analysis

**Deliverables:**
```
modul2_detector/
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
├── data.yaml              # Dataset config
├── train_detector.py      # Training script
├── detect_products.py     # Detection script
├── count_products.py      # Product counting
├── best.pt               # Trained YOLO weights
└── results/              # Training metrics
```

---

### Modul 3: Deployment Pipeline

**Export Requirements:**
- Export classifier ke ONNX format
- Export YOLO ke ONNX format
- Verify exported models

**Inference Requirements:**
- Load models dengan OpenCV DNN
- Inference tanpa PyTorch dependency
- Support untuk image dan video input

**Performance Requirements:**
- Inference time < 100ms per frame pada CPU
- FPS ≥ 15 untuk real-time video

**Deliverables:**
```
modul3_deployment/
├── export_classifier_onnx.py    # Export classifier
├── export_yolo_onnx.py          # Export YOLO
├── inference_opencv.py          # OpenCV inference
├── benchmark.py                 # Performance benchmark
├── classifier.onnx             # Exported classifier
├── yolo.onnx                   # Exported YOLO
└── benchmark_results.txt       # Benchmark report
```

---

## Integrated Demo Application

**Buat aplikasi terintegrasi yang menggabungkan semua modul:**

```
integrated_app/
├── app.py                      # Main application
├── modules/
│   ├── classifier.py          # Classifier wrapper
│   ├── detector.py            # Detector wrapper
│   └── utils.py               # Helper functions
├── config.yaml                # Configuration
└── README.md                  # Usage instructions
```

**Features:**
1. **Single Image Mode**: Upload gambar → classify + detect
2. **Video/Webcam Mode**: Real-time processing
3. **Counting Mode**: Hitung produk tertentu
4. **Report Generation**: Export hasil ke JSON/CSV

---

## Timeline Pengerjaan

| Minggu | Deliverable | Poin |
|--------|-------------|------|
| 1 | Dataset collection & preparation | - |
| 2 | Modul 1: Classifier training & evaluation | 30% |
| 3 | Modul 2: Detector training & evaluation | 30% |
| 4 | Modul 3: ONNX export & deployment | 20% |
| 5 | Integrated application & documentation | 20% |

---

## Rubrik Penilaian

### Modul 1: Product Classifier (30 poin)

| Aspek | Poin | Kriteria |
|-------|------|----------|
| Dataset | 5 | ≥5 classes, ≥50 images/class, proper split |
| Training | 10 | Transfer learning, augmentation, proper training loop |
| Accuracy | 10 | ≥85% validation accuracy |
| Documentation | 5 | Training logs, confusion matrix, analysis |

### Modul 2: Shelf Detector (30 poin)

| Aspek | Poin | Kriteria |
|-------|------|----------|
| Dataset | 5 | ≥100 images, proper annotations, YOLO format |
| Training | 10 | Fine-tuning, proper augmentation, validation |
| mAP | 10 | mAP@0.5 ≥ 0.6 |
| Demo | 5 | Working detection demo, counting feature |

### Modul 3: Deployment (20 poin)

| Aspek | Poin | Kriteria |
|-------|------|----------|
| ONNX Export | 5 | Both models exported successfully |
| OpenCV Inference | 10 | Working inference tanpa PyTorch |
| Performance | 5 | < 100ms inference, benchmark report |

### Integrated Application (20 poin)

| Aspek | Poin | Kriteria |
|-------|------|----------|
| Functionality | 10 | All features working |
| Code Quality | 5 | Clean, modular, documented |
| Documentation | 5 | Complete README, usage guide |

---

## Bonus Points (maksimal +20)

| Bonus | Poin | Kriteria |
|-------|------|----------|
| Custom CNN Architecture | +5 | Design dan train from scratch |
| Instance Segmentation | +5 | Gunakan YOLOv8-seg |
| Real-time Optimization | +5 | FPS ≥ 30 dengan optimization |
| Web/Mobile Demo | +5 | Deploy ke web (Gradio/Streamlit) |

---

## Format Pengumpulan

### Struktur Folder
```
NIM_Nama_DeepVision/
├── modul1_classifier/
│   └── (seperti di atas)
├── modul2_detector/
│   └── (seperti di atas)
├── modul3_deployment/
│   └── (seperti di atas)
├── integrated_app/
│   └── (seperti di atas)
├── docs/
│   ├── report.pdf            # Laporan lengkap
│   ├── dataset_description.md
│   └── model_architecture.md
├── requirements.txt
└── README.md                  # Project overview
```

### Laporan (docs/report.pdf)

**Format:** PDF, maksimal 20 halaman

**Struktur:**
1. **Pendahuluan** (1 halaman)
   - Latar belakang
   - Tujuan project

2. **Dataset** (2 halaman)
   - Deskripsi dataset
   - Data collection process
   - Preprocessing & augmentation

3. **Metodologi** (4 halaman)
   - Arsitektur model per modul
   - Training strategy
   - Hyperparameters

4. **Hasil dan Analisis** (5 halaman)
   - Training curves
   - Evaluation metrics
   - Confusion matrix & error analysis
   - Performance benchmark

5. **Deployment** (2 halaman)
   - ONNX export process
   - OpenCV integration
   - Performance comparison

6. **Kesimpulan** (1 halaman)
   - Summary hasil
   - Lessons learned
   - Future improvements

---

## Dataset Suggestions

### Opsi 1: Collect Your Own
- Foto produk dari minimarket/supermarket
- Gunakan smartphone dengan pencahayaan baik
- Variasi angle dan background

### Opsi 2: Public Datasets
- [Freiburg Groceries Dataset](https://github.com/PhilJd/freiburg_groceries_dataset)
- [MVTec Anomaly Detection](https://www.mvtec.com/company/research/datasets/mvtec-ad)
- [GroZi-120](https://github.com/felixblack/GroZi-120)
- [SKU-110K](https://github.com/eg4000/SKU110K_CVPR19)

### Opsi 3: Synthetic Data
- Generate dengan image composition
- Augment existing images
- Use DALL-E/Midjourney untuk generate (limited)

---

## Tools dan Resources

### Training
```python
# Classifier
import torch
import torchvision
from torchvision import models, transforms

# Detector
from ultralytics import YOLO
```

### Export
```python
# ONNX Export
import torch.onnx
model = YOLO('best.pt')
model.export(format='onnx')
```

### Deployment
```python
# OpenCV DNN
net = cv2.dnn.readNetFromONNX('model.onnx')
blob = cv2.dnn.blobFromImage(image, ...)
net.setInput(blob)
output = net.forward()
```

### Visualization
```python
# TensorBoard
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter('runs/experiment')

# Weights & Biases (optional)
import wandb
wandb.init(project='deepvision')
```

---

## FAQ

**Q: Bolehkah menggunakan dataset yang sudah ada?**
A: Ya, boleh menggunakan public dataset. Namun perlu preprocessing dan dokumentasi proper.

**Q: Apakah harus training dari awal atau boleh fine-tune?**
A: Wajib menggunakan transfer learning/fine-tuning untuk efficiency.

**Q: Minimum spec komputer untuk training?**
A: CPU-only bisa untuk classifier dengan batch kecil. Untuk YOLO, recommended GPU dengan minimal 4GB VRAM.

**Q: Bolehkah menggunakan cloud training?**
A: Ya, boleh menggunakan Google Colab, Kaggle, atau cloud lainnya.

**Q: Bagaimana jika tidak punya GPU?**
A: Gunakan Google Colab (free GPU), reduce image size, atau gunakan smaller models (MobileNet, YOLOv8n).

---

## Contact dan Support

- Konsultasi project: Saat jam praktikum
- Deadline questions: Minimal 3 hari sebelum deadline
- Technical issues: Buat issue di repository atau forum
