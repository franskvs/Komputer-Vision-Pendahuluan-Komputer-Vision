# Bab 06: Recognition

## Tujuan Pembelajaran

Setelah menyelesaikan bab ini, mahasiswa diharapkan mampu:
1. Memahami konsep dan aplikasi face recognition
2. Mengimplementasikan face detection dengan berbagai metode
3. Menerapkan face recognition menggunakan deep learning
4. Memahami teknik feature extraction untuk recognition
5. Mengimplementasikan similarity matching dan verification
6. Membangun sistem recognition end-to-end

---

## 1. Pendahuluan Recognition

### 1.1 Definisi dan Ruang Lingkup

Recognition dalam computer vision adalah kemampuan sistem untuk mengidentifikasi atau memverifikasi objek, wajah, atau pola dalam gambar atau video. Recognition berbeda dari detection karena tidak hanya menemukan "apa" yang ada di gambar, tetapi juga "siapa" atau "yang mana" dari kategori tertentu.

#### Jenis-jenis Recognition:

1. **Face Recognition**: Mengidentifikasi atau memverifikasi identitas seseorang
2. **Object Recognition**: Mengenali objek spesifik (bukan hanya kategori)
3. **Text Recognition (OCR)**: Membaca dan mengenali teks dalam gambar
4. **Action Recognition**: Mengenali aktivitas atau gerakan
5. **Scene Recognition**: Mengidentifikasi jenis lokasi atau pemandangan

### 1.2 Verification vs Identification

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VERIFICATION (1:1)                               │
├─────────────────────────────────────────────────────────────────────┤
│  Input: Probe image + Claimed identity                              │
│  Question: "Apakah ini orang yang diklaim?"                         │
│  Output: Yes/No (dengan confidence score)                           │
│                                                                     │
│  Use Cases:                                                         │
│  - Face unlock smartphone                                           │
│  - Access control                                                   │
│  - Payment verification                                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   IDENTIFICATION (1:N)                              │
├─────────────────────────────────────────────────────────────────────┤
│  Input: Probe image + Database of N identities                      │
│  Question: "Siapa orang ini?"                                       │
│  Output: Most similar identity (atau unknown)                       │
│                                                                     │
│  Use Cases:                                                         │
│  - Surveillance                                                     │
│  - Missing person search                                            │
│  - Photo organization                                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 Recognition Pipeline

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│  Input  │───►│ Detection│───►│Alignment │───►│ Feature  │───►│ Matching│
│  Image  │    │          │    │          │    │Extraction│    │         │
└─────────┘    └──────────┘    └──────────┘    └──────────┘    └─────────┘
                    │               │               │               │
                    ▼               ▼               ▼               ▼
              Find faces/     Normalize       Extract          Compare
              objects         pose/scale      embedding        with DB
```

---

## 2. Face Detection

### 2.1 Metode Tradisional

#### Viola-Jones (Haar Cascades)
- Menggunakan Haar-like features
- Integral image untuk efisiensi
- Cascade classifier untuk kecepatan
- Tersedia di OpenCV (`cv2.CascadeClassifier`)

```python
# Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
```

#### HOG + SVM
- Histogram of Oriented Gradients sebagai feature
- SVM untuk classification
- Lebih robust terhadap variasi pencahayaan
- Digunakan oleh dlib

### 2.2 Deep Learning Face Detection

#### MTCNN (Multi-task Cascaded CNN)
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  P-Net  │───►│  R-Net  │───►│  O-Net  │
│(Proposal)│   │(Refine) │    │(Output) │
└─────────┘    └─────────┘    └─────────┘
     │              │              │
Candidate      Refine box      Final box +
boxes          positions       landmarks
```

- Stage 1 (P-Net): Proposal network, generates candidate windows
- Stage 2 (R-Net): Refine network, filters false positives
- Stage 3 (O-Net): Output network, final bounding box + landmarks

#### RetinaFace
- Single-stage detector
- Feature Pyramid Network backbone
- Predicts face box + 5 landmarks
- State-of-the-art accuracy

#### BlazeFace
- Designed for mobile devices
- Extremely fast (<1ms on mobile GPU)
- Used in MediaPipe

### 2.3 Face Landmarks

```
       ●  ●          Alis (eyebrows)
       
    ●      ●         Mata (eyes)
    
       ●             Hidung (nose)
       
   ●      ●          Mulut (mouth corners)
      ●              
      ●              Bibir (lips)
      ●
```

Landmarks digunakan untuk:
1. **Face Alignment**: Rotasi dan scaling agar wajah lurus
2. **Expression Analysis**: Deteksi emosi
3. **Gaze Estimation**: Arah pandangan
4. **Face Mesh**: 3D face reconstruction

---

## 3. Face Recognition

### 3.1 Feature Extraction

#### Traditional Methods
1. **Eigenfaces (PCA)**: Reduksi dimensi dengan Principal Component Analysis
2. **Fisherfaces (LDA)**: Linear Discriminant Analysis untuk maximizing class separation
3. **LBPH**: Local Binary Pattern Histograms

#### Deep Learning Methods
1. **DeepFace** (Facebook/Meta): Pertama mencapai human-level performance
2. **FaceNet** (Google): Triplet loss, 128-D embedding
3. **ArcFace**: Additive angular margin loss
4. **CosFace**: Large margin cosine loss

### 3.2 FaceNet Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FaceNet                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Input Image (160×160×3)                                            │
│        │                                                            │
│        ▼                                                            │
│  ┌───────────────────┐                                              │
│  │    Inception      │                                              │
│  │    Network        │                                              │
│  │  (or ResNet)      │                                              │
│  └─────────┬─────────┘                                              │
│            │                                                        │
│            ▼                                                        │
│  ┌───────────────────┐                                              │
│  │  L2 Normalization │                                              │
│  └─────────┬─────────┘                                              │
│            │                                                        │
│            ▼                                                        │
│       Embedding                                                     │
│      (128-D vector)                                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 Loss Functions

#### Triplet Loss
```
L = max(0, ||f(A) - f(P)||² - ||f(A) - f(N)||² + margin)

Dimana:
- A = Anchor image
- P = Positive (same person)
- N = Negative (different person)
- margin = minimum distance gap

Tujuan: distance(A,P) + margin < distance(A,N)
```

#### ArcFace (Additive Angular Margin Loss)
```
L = -log(e^(s·cos(θ_y + m)) / (e^(s·cos(θ_y + m)) + Σ e^(s·cos(θ_j))))

Dimana:
- θ = angle between feature and weight
- m = angular margin
- s = scale factor

Keunggulan: Better discriminative power
```

### 3.4 Face Embedding

Face embedding adalah representasi vektor dari wajah dalam high-dimensional space di mana:
- Wajah orang yang sama → vektor berdekatan
- Wajah orang berbeda → vektor berjauhan

```
Embedding Space:

        Person A ●  ● Person A
                 ●
                    ●
                    
        Person B ■
                 ■  ■ Person B
                 
             Person C ▲
                      ▲
                      
Distance metrics:
- Euclidean: √(Σ(x_i - y_i)²)
- Cosine similarity: (x·y)/(||x||||y||)
```

---

## 4. Similarity Matching

### 4.1 Distance Metrics

```python
import numpy as np

def euclidean_distance(v1, v2):
    """Euclidean (L2) distance."""
    return np.sqrt(np.sum((v1 - v2) ** 2))

def cosine_similarity(v1, v2):
    """Cosine similarity (1 = identical, 0 = orthogonal)."""
    dot = np.dot(v1, v2)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot / norm

def cosine_distance(v1, v2):
    """Cosine distance (0 = identical, 1 = orthogonal)."""
    return 1 - cosine_similarity(v1, v2)
```

### 4.2 Threshold Selection

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Threshold Trade-off                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Threshold rendah:                                                  │
│  - Lebih banyak matches                                             │
│  - False Accept Rate (FAR) tinggi                                   │
│  - Cocok untuk convenience (face unlock casual)                     │
│                                                                     │
│  Threshold tinggi:                                                  │
│  - Lebih sedikit matches                                            │
│  - False Reject Rate (FRR) tinggi                                   │
│  - Cocok untuk security (banking, access control)                   │
│                                                                     │
│  Equal Error Rate (EER):                                            │
│  - Titik dimana FAR = FRR                                           │
│  - Sering digunakan sebagai benchmark                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 Efficient Search

Untuk database besar, perlu efficient nearest neighbor search:

1. **Brute Force**: O(N) - cocok untuk database kecil
2. **KD-Tree**: O(log N) - buruk untuk high dimensions
3. **Ball Tree**: O(log N) - better for high dimensions
4. **LSH** (Locality Sensitive Hashing): Approximate, sub-linear
5. **FAISS** (Facebook AI Similarity Search): State-of-the-art
6. **Annoy** (Spotify): Memory-efficient approximate NN

---

## 5. Optical Character Recognition (OCR)

### 5.1 OCR Pipeline

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Input  │───►│ Text     │───►│Character │───►│  Post-   │
│  Image  │    │ Detection│    │Recognition│   │Processing│
└─────────┘    └──────────┘    └──────────┘    └──────────┘
                    │               │               │
                    ▼               ▼               ▼
              Find text        Recognize        Spell check,
              regions          characters       formatting
```

### 5.2 Text Detection Methods

1. **EAST** (Efficient and Accurate Scene Text Detector)
2. **CRAFT** (Character Region Awareness For Text)
3. **DBNet** (Differentiable Binarization)

### 5.3 Text Recognition Methods

1. **Tesseract**: Open source, traditional + LSTM
2. **CRNN**: CNN + RNN + CTC loss
3. **TrOCR**: Transformer-based OCR

### 5.4 End-to-End Solutions

1. **EasyOCR**: Multi-language, easy to use
2. **PaddleOCR**: High accuracy, multilingual
3. **Google Cloud Vision API**: Commercial, accurate
4. **Amazon Textract**: Document understanding

---

## 6. Praktikum

### 6.1 Struktur Folder

```
Bab-06-Recognition/
├── Materi.md
├── Jobsheet.md
├── Project.md
├── Referensi.md
├── Rubrik_Penilaian_Project.md
├── Rubrik_Penilaian_Tugas_Video.md
└── praktikum/
    ├── 01_face_detection_opencv.py
    ├── 02_face_detection_deep.py
    ├── 03_face_landmarks.py
    ├── 04_face_recognition.py
    ├── 05_face_verification.py
    ├── 06_face_database.py
    ├── 07_similarity_matching.py
    ├── 08_ocr_basic.py
    ├── 09_ocr_advanced.py
    └── 10_realtime_recognition.py
```

### 6.2 Alur Praktikum

| Pertemuan | Topik | Program |
|-----------|-------|---------|
| 1 | Face Detection Methods | 01, 02 |
| 2 | Face Landmarks & Alignment | 03 |
| 3 | Face Recognition Basics | 04, 05 |
| 4 | Database & Matching | 06, 07 |
| 5 | OCR Implementation | 08, 09 |
| 6 | Real-time System | 10 |

---

## 7. Project: FaceGuard - Smart Attendance System

### 7.1 Deskripsi

Membangun sistem absensi berbasis face recognition yang dapat:
- Registrasi wajah karyawan
- Verifikasi identitas real-time
- Log attendance dengan timestamp
- Dashboard monitoring
- Anti-spoofing detection

### 7.2 Fitur Utama

1. **Face Registration Module**
   - Capture multiple angles
   - Extract and store embeddings
   - Quality check

2. **Attendance Module**
   - Real-time face detection
   - Identity verification
   - Clock in/out logging

3. **Admin Dashboard**
   - Employee management
   - Attendance reports
   - System configuration

---

## 8. Evaluasi Metrics

### 8.1 Face Recognition Metrics

| Metric | Formula | Deskripsi |
|--------|---------|-----------|
| **FAR** (False Accept Rate) | FP / (FP + TN) | Proporsi orang salah yang diterima |
| **FRR** (False Reject Rate) | FN / (FN + TP) | Proporsi orang benar yang ditolak |
| **EER** (Equal Error Rate) | FAR = FRR | Error rate saat FAR = FRR |
| **Accuracy** | (TP + TN) / Total | Overall correctness |
| **TAR@FAR** | TP rate at specific FAR | Common benchmark |

### 8.2 OCR Metrics

| Metric | Deskripsi |
|--------|-----------|
| **CER** (Character Error Rate) | Edit distance / total chars |
| **WER** (Word Error Rate) | Edit distance / total words |
| **Accuracy** | Correct / Total |

---

## 9. Best Practices

### 9.1 Face Recognition

1. **Data Collection**
   - Multiple poses dan pencahayaan
   - Minimal 5-10 gambar per orang
   - Update secara berkala

2. **Anti-Spoofing**
   - Liveness detection
   - Depth sensing jika tersedia
   - Motion analysis

3. **Privacy**
   - Encrypt stored embeddings
   - Data retention policy
   - User consent

### 9.2 OCR

1. **Image Quality**
   - Resolusi cukup (minimal 300 DPI untuk dokumen)
   - Pencahayaan merata
   - Hindari blur dan skew

2. **Preprocessing**
   - Deskewing
   - Noise removal
   - Binarization

3. **Post-processing**
   - Spell checking
   - Format validation
   - Confidence filtering

---

## 10. Kesimpulan

Recognition adalah salah satu area terpenting dalam computer vision dengan aplikasi luas dari keamanan hingga otomatisasi bisnis. Kombinasi deep learning dengan efficient search algorithms telah membuat recognition systems menjadi praktis untuk deployment real-world.

Key takeaways:
1. Face detection adalah prerequisite untuk face recognition
2. Deep learning embeddings far outperform traditional methods
3. Threshold selection sangat penting untuk balance FAR/FRR
4. Privacy dan security harus menjadi prioritas
5. OCR memerlukan preprocessing yang baik untuk hasil optimal

---

## Referensi

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Ed. - Chapter 6
2. Schroff, F., et al. (2015). "FaceNet: A Unified Embedding for Face Recognition"
3. Deng, J., et al. (2019). "ArcFace: Additive Angular Margin Loss"
4. Zhang, K., et al. (2016). "Joint Face Detection and Alignment using MTCNN"
5. Shi, B., et al. (2017). "An End-to-End Trainable Neural Network for Image-based Sequence Recognition"
