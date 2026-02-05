# BAB 5: DEEP LEARNING - PRAKTIKUM
## Computer Vision - Deep Learning for Image Analysis

### 📋 RINGKASAN

Praktikum ini mencakup **12 program** yang mendemonstrasikan penggunaan deep learning untuk computer vision, mulai dari klasifikasi gambar hingga deteksi objek dan segmentasi.

**Status:** ✅ **PROGRAM TERVERIFIKASI**
- **12 programs** untuk pembelajaran deep learning
- Output tersimpan di folder `output/`

---

### 🎯 STRUKTUR PRAKTIKUM

#### 1. **Image Classification** (Programs 01-02)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 01 | OpenCV DNN Classification | DNN module, inference | Image classification |
| 02 | Model Comparison | Multi-model benchmark | Model selection |

#### 2. **CNN Training** (Programs 03-04)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 03 | CNN PyTorch | PyTorch CNN training | Custom classification |
| 04 | CNN Keras | Keras/TensorFlow CNN | Deep learning pipeline |

#### 3. **Transfer Learning & Augmentation** (Programs 05-06)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 05 | Transfer Learning | Pre-trained models | Fine-tuning |
| 06 | Data Augmentation | Image augmentation | Dataset expansion |

#### 4. **Object Detection** (Programs 07-08)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 07 | YOLO Detection | YOLOv8 inference | Object detection |
| 08 | YOLO Realtime | Realtime detection | Video analytics |

#### 5. **Segmentation** (Programs 09-10)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 09 | Semantic Segmentation | Pixel classification | Scene parsing |
| 10 | Instance Segmentation | Object instances | Self-driving |

#### 6. **Deployment** (Programs 11-12)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 11 | ONNX Export | Model conversion | Cross-platform |
| 12 | OpenCV Deployment | Production inference | Edge deployment |

---

### 🚀 CARA MENJALANKAN

#### Setup Awal (Hanya Sekali)
```bash
# 1. Install dependencies
pip install torch torchvision tensorflow keras ultralytics onnx

# 2. Generate gambar untuk praktikum
python3 setup_images.py

# Output: Gambar di folder data/images/
```

#### Menjalankan Program Individual
```bash
# Contoh: Jalankan OpenCV DNN classification
python3 01_opencv_dnn_classification.py

# Output akan tersimpan di: output/output1/
```

#### Automated Testing (Semua Program Sekaligus)
```bash
# Test semua program secara otomatis
python3 run_all_tests.py

# Output: 
# - Verification report
# - Execution statistics
```

---

### 📁 STRUKTUR DIREKTORI

```
Bab-05-Deep-Learning/praktikum/
│
├── data/
│   ├── images/               # Gambar praktikum
│   │   ├── dog.jpg           # Classification sample
│   │   ├── cat.jpg           # Classification sample
│   │   └── ...
│   └── models/               # Pre-trained models
│       ├── mobilenet.onnx
│       └── ...
│
├── output/
│   ├── output1/             # Hasil DNN classification
│   ├── output2/             # Hasil model comparison
│   └── ... (12 folders)
│
├── 01_opencv_dnn_classification.py
├── 02_model_comparison.py
├── ... (12 programs)
│
├── CV2_FUNCTIONS_REFERENCE.py  # Referensi fungsi OpenCV
├── setup_images.py             # Setup gambar
├── run_all_tests.py            # Test runner
├── README.md                   # Dokumentasi ini
└── QUICKSTART.md               # Panduan cepat
```

---

### 📚 KONSEP YANG DIPELAJARI

1. **DNN Module** - OpenCV deep learning inference
2. **CNN Architecture** - Convolutional Neural Networks
3. **Transfer Learning** - Pre-trained model fine-tuning
4. **Data Augmentation** - Training data expansion
5. **Object Detection** - YOLO, SSD, Faster R-CNN
6. **Semantic Segmentation** - Pixel-wise classification
7. **Instance Segmentation** - Object-level segmentation
8. **ONNX** - Open Neural Network Exchange
9. **Model Deployment** - Production inference

---

### 🔧 TROUBLESHOOTING

**Q: Gambar tidak ditemukan?**
```bash
python3 setup_images.py
```

**Q: Error "No module named torch"?**
```bash
pip install torch torchvision
```

**Q: Error "No module named tensorflow"?**
```bash
pip install tensorflow keras
```

**Q: YOLO tidak tersedia?**
```bash
pip install ultralytics
```

---

### 📖 REFERENSI

- [OpenCV DNN Tutorial](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [TensorFlow/Keras Documentation](https://www.tensorflow.org/guide)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- File: `CV2_FUNCTIONS_REFERENCE.py` - Dokumentasi fungsi lengkap
