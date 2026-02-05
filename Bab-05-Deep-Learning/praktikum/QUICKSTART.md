# QUICK START GUIDE - BAB 5 DEEP LEARNING

## ⚡ LANGKAH CEPAT (10 MENIT)

### 1️⃣ Install Dependencies
```bash
# PyTorch (pilih salah satu sesuai sistem)
pip install torch torchvision

# TensorFlow/Keras
pip install tensorflow keras

# YOLO
pip install ultralytics

# ONNX
pip install onnx onnxruntime
```

### 2️⃣ Setup Images (Pertama Kali Saja)
```bash
cd "Bab-05-Deep-Learning/praktikum"
python3 setup_images.py
```
✅ Output: Gambar di `data/images/` dan models di `data/models/`

---

### 3️⃣ Test Semua Program (Opsional - Verifikasi)
```bash
python3 run_all_tests.py
```
✅ Output: Verification report + output files

---

### 4️⃣ Jalankan Program Individual
```bash
# Program populer:

# OpenCV DNN Classification
python3 01_opencv_dnn_classification.py

# YOLO Object Detection (paling menarik!)
python3 07_yolo_detection.py

# Transfer Learning
python3 05_transfer_learning.py

# Semantic Segmentation
python3 09_semantic_segmentation.py
```

---

## 📂 LIHAT HASIL

Semua output tersimpan di:
```
output/
├── output1/   ← OpenCV DNN Classification
├── output2/   ← Model Comparison
├── output3/   ← CNN PyTorch
├── output4/   ← CNN Keras
├── output5/   ← Transfer Learning
├── output6/   ← Data Augmentation
├── output7/   ← YOLO Detection (MUST SEE!)
├── output8/   ← YOLO Realtime
├── output9/   ← Semantic Segmentation
├── output10/  ← Instance Segmentation
├── output11/  ← ONNX Export
└── output12/  ← OpenCV Deployment
```

---

## 🎯 PROGRAM FAVORIT (MUST TRY)

| Program | File | Wow Factor | Real App |
|---------|------|------------|----------|
| **YOLO Detection** | `07_yolo_detection.py` | ⭐⭐⭐⭐⭐ | Object Detection |
| **Semantic Segmentation** | `09_semantic_segmentation.py` | ⭐⭐⭐⭐⭐ | Self-driving |
| **Transfer Learning** | `05_transfer_learning.py` | ⭐⭐⭐⭐⭐ | Fine-tuning |
| **Data Augmentation** | `06_data_augmentation.py` | ⭐⭐⭐⭐ | Dataset Expansion |
| **OpenCV DNN** | `01_opencv_dnn_classification.py` | ⭐⭐⭐⭐ | Production |

---

## 🔥 DEMO UNTUK PRESENTASI

### Demo 1: Object Detection dengan YOLO
```bash
python3 07_yolo_detection.py
```
**Output:** Gambar dengan bounding boxes objek terdeteksi

### Demo 2: Semantic Segmentation
```bash
python3 09_semantic_segmentation.py
```
**Output:** Pixel-wise segmentation masks

### Demo 3: Transfer Learning
```bash
python3 05_transfer_learning.py
```
**Output:** Fine-tuned model untuk custom dataset

### Demo 4: Data Augmentation
```bash
python3 06_data_augmentation.py
```
**Output:** Various augmented images

---

## 🎨 GAMBAR YANG TERSEDIA

| Image | Ukuran | Best For | Deskripsi |
|-------|--------|----------|-----------|
| `dog.jpg` | 512×512 | Programs 1-6 | Classification |
| `cat.jpg` | 512×512 | Programs 1-6 | Classification |
| `street.jpg` | 640×480 | Programs 7-10 | Detection/Segmentation |
| `car.jpg` | 640×480 | Programs 7-8 | YOLO detection |

---

## ⚠️ TROUBLESHOOTING

### Error "No module named torch"
```bash
pip install torch torchvision
```

### Error "No module named tensorflow"
```bash
pip install tensorflow keras
```

### YOLO tidak tersedia
```bash
pip install ultralytics
```

### CUDA out of memory
Gunakan CPU atau reduce batch size:
```python
device = "cpu"  # instead of "cuda"
```

### Model download lambat
Model akan didownload saat pertama kali dijalankan. Pastikan koneksi internet stabil.
