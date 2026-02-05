# QUICK START GUIDE - BAB-05-DEEP-LEARNING

## 🚀 Cara Cepat Mulai

### Jalankan Program
```bash
cd Bab-05-Deep-Learning/praktikum

# Jalankan salah satu:
python3 01_opencv_dnn_classification.py     # Image classification
python3 07_yolo_detection.py               # Object detection  
python3 08_yolo_realtime.py                # Real-time video
python3 06_data_augmentation.py            # Data augmentation
python3 05_transfer_learning.py            # Transfer learning
```

### Tutup Program
- **Tekan 'q'** atau **ESC** untuk menutup window image/video
- **Ctrl+C** untuk stop program

### Baca Dokumentasi
- **JOBSHEET_UPDATED.md** - Panduan lengkap 6 pertemuan
- **LAPORAN_LENGKAP_PENINGKATAN.md** - Dokumentasi detail setiap file
- **FINAL_STATUS.md** - Status keseluruhan & checklist

---

## 📂 File Organization

| File | Topik | Status |
|------|-------|--------|
| 01_opencv_dnn_classification.py | Image Classification | ✅ Ready |
| 02_model_comparison.py | Model Comparison | ✅ Ready |
| 03_cnn_pytorch.py | CNN from Scratch (PyTorch) | ✅ Ready |
| 04_cnn_keras.py | CNN from Scratch (Keras) | ✅ Ready |
| 05_transfer_learning.py | Transfer Learning | ✅ Ready |
| 06_data_augmentation.py | Data Augmentation | ✅ Ready |
| 07_yolo_detection.py | Object Detection (Image) | ✅ Ready |
| 08_yolo_realtime.py | Object Detection (Video) | ✅ Ready |
| 09_semantic_segmentation.py | Semantic Segmentation | ✅ Ready |
| 10_instance_segmentation.py | Instance Segmentation | ✅ Ready |
| 11_onnx_export.py | ONNX Export | ✅ Ready |
| 12_opencv_deployment.py | Production Deployment | ✅ Ready |

---

## 💡 Key Improvements

✅ **Auto-Close GUI**: Press 'q' atau ESC (tidak perlu manual close window)  
✅ **Inline Comments**: Setiap baris code ada penjelasan  
✅ **Parameter Docs**: cv2.putText parameters dijelaskan (a, b, c, d, e, f, g)  
✅ **Real-world Examples**: Smart Retail, Medical Imaging, Traffic Monitoring  
✅ **Comprehensive Jobsheet**: 6 pertemuan dengan tugas terukur  
✅ **Automated Testing**: Run `verify_programs.py` untuk check semua file  

---

## 🎯 Per-File Quick Reference

### File 01: Image Classification
```
Topic: OpenCV DNN untuk image classification
Demo: Classify gambar, visualize confidence scores
Time: 2-3 menit per run
Real-world: Smart retail inventory checking
```

### File 06: Data Augmentation
```
Topic: Teknik augmentasi untuk generalisasi
Demo: Geometric, color, noise augmentations
Time: 1-2 menit per run
Real-world: Synthetic data generation untuk training
```

### File 07: YOLO Detection
```
Topic: Real-time object detection
Demo: Image detection, NMS, confidence threshold
Time: 2-3 menit per run
Real-world: Traffic monitoring, security systems
```

### File 08: YOLO Real-time
```
Topic: Live detection dari video/webcam
Demo: FPS calculation, object counting, zones
Time: 3-5 menit per run
Real-world: Live surveillance, counting systems
```

---

## 🔧 Understanding Code Comments

### Contoh 1: Simple Function
```python
# Baca gambar dari file, return BGR image array
img = cv2.imread("image.jpg")
```

### Contoh 2: cv2.putText Parameters
```python
# cv2.putText(a, b, c, d, e, f, g):
# a=image, b=teks, c=posisi(x,y), d=font, e=skala, f=warna(B,G,R), g=ketebalan
cv2.putText(img, "Label", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
```

### Contoh 3: Complex Operation
```python
# Gambar persegi panjang pada gambar
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
```

---

## ✅ Verification

```bash
# Check semua file OK
python3 verify_programs.py

# Expected output:
# ✓ Syntax valid: 13/13 (100%)
# ✓ Imports OK: 13/13 (100%)
# ✓ Q-key implemented: 5/5
```

---

## 📚 Learning Path

### Minggu 1: Fundamentals
1. Read JOBSHEET_UPDATED.md - Pertemuan 1
2. Run 01_opencv_dnn_classification.py
3. Understand CNN basics

### Minggu 2: Architecture
1. Read JOBSHEET_UPDATED.md - Pertemuan 2
2. Run 03_cnn_pytorch.py or 04_cnn_keras.py
3. Build simple CNN

### Minggu 3: Transfer Learning
1. Read JOBSHEET_UPDATED.md - Pertemuan 3
2. Run 05_transfer_learning.py
3. Fine-tune pre-trained model

### Minggu 4: Detection
1. Read JOBSHEET_UPDATED.md - Pertemuan 4
2. Run 07_yolo_detection.py
3. Run 08_yolo_realtime.py
4. Understand YOLO

### Minggu 5-6: Advanced
1. Read JOBSHEET_UPDATED.md - Pertemuan 5-6
2. Run segmentation programs
3. Final project integration

---

## 🎓 Tips untuk Pembelajaran

1. **Baca komentar dulu** sebelum jalankan program
2. **Modifikasi parameter** untuk eksperimen
3. **Lihat output** untuk understand apa yang terjadi
4. **Dokumentasi lengkap** ada di LAPORAN_LENGKAP_PENINGKATAN.md
5. **Verify semua file** dengan verify_programs.py

---

## 📞 Troubleshooting

**Q: Gambar tidak tutup?**
```
A: Tekan 'q' atau ESC, bukan klik window
```

**Q: Module tidak ditemukan?**
```
A: Install dependencies: pip install -r requirements.txt
```

**Q: Ingin tahu detail lebih?**
```
A: Baca LAPORAN_LENGKAP_PENINGKATAN.md
```

---

**Status**: ✅ READY TO USE  
**Last Updated**: 5 Februari 2026  
**All Files Tested**: YES
