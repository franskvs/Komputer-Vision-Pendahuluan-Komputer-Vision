# Bab 5: Deep Learning untuk Computer Vision

## 📚 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami dasar-dasar neural networks dan backpropagation
2. Menguasai arsitektur Convolutional Neural Networks (CNN)
3. Mengenal arsitektur populer (ResNet, VGG, etc.)
4. Memahami teknik training dan regularisasi
5. Mengimplementasikan CNN untuk klasifikasi gambar

---

## 1. Pengantar Neural Networks

### 1.1 Dari Machine Learning ke Deep Learning

**Machine Learning Tradisional:**
```
Input → Feature Engineering → Classifier → Output
         (manual)
```

**Deep Learning:**
```
Input → Feature Learning + Classification → Output
         (automatic, end-to-end)
```

### 1.2 Perceptron

Unit dasar neural network:
$$y = \sigma\left(\sum_{i=1}^{n} w_i x_i + b\right) = \sigma(\mathbf{w}^T \mathbf{x} + b)$$

di mana $\sigma$ adalah **activation function**.

### 1.3 Activation Functions

| Fungsi | Formula | Kegunaan |
|--------|---------|----------|
| Sigmoid | $\sigma(x) = \frac{1}{1+e^{-x}}$ | Output layer (binary) |
| Tanh | $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$ | Hidden layers (jarang) |
| ReLU | $\text{ReLU}(x) = \max(0, x)$ | Hidden layers (paling populer) |
| Leaky ReLU | $\text{LReLU}(x) = \max(\alpha x, x)$ | Menghindari dying ReLU |
| Softmax | $\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$ | Output layer (multiclass) |
| GELU | $x \cdot \Phi(x)$ | Transformers |

### 1.4 Multi-Layer Perceptron (MLP)

```
Input Layer → Hidden Layer(s) → Output Layer
```

**Forward Pass:**
$$\mathbf{h}_1 = \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$$
$$\mathbf{h}_2 = \sigma(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2)$$
$$\mathbf{y} = \text{softmax}(\mathbf{W}_3 \mathbf{h}_2 + \mathbf{b}_3)$$

---

## 2. Backpropagation

### 2.1 Konsep Dasar

**Tujuan:** Hitung gradient $\frac{\partial L}{\partial \theta}$ untuk semua parameter $\theta$.

**Metode:** Chain rule dari kalkulus

### 2.2 Algoritma Backpropagation

1. **Forward Pass:** Hitung output dan simpan intermediate values
2. **Compute Loss:** $L = \text{Loss}(\hat{y}, y)$
3. **Backward Pass:** Hitung gradient dari output ke input

**Contoh untuk 1 hidden layer:**
$$\frac{\partial L}{\partial \mathbf{W}_2} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial \mathbf{W}_2}$$

$$\frac{\partial L}{\partial \mathbf{W}_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial \mathbf{h}} \cdot \frac{\partial \mathbf{h}}{\partial \mathbf{W}_1}$$

### 2.3 Loss Functions

**Cross-Entropy (Classification):**
$$L = -\sum_{i} y_i \log(\hat{y}_i)$$

**Mean Squared Error (Regression):**
$$L = \frac{1}{n}\sum_{i}(y_i - \hat{y}_i)^2$$

---

## 3. Convolutional Neural Networks (CNN)

### 3.1 Motivasi

**Masalah MLP untuk Gambar:**
- Jumlah parameter sangat besar (1000×1000×3 = 3M input)
- Tidak memanfaatkan struktur spatial
- Tidak translation invariant

**Solusi CNN:**
- Parameter sharing (filter yang sama untuk seluruh gambar)
- Local connectivity (hanya melihat region kecil)
- Translation equivariance

### 3.2 Convolutional Layer

**Operasi:**
$$(I * K)(x, y) = \sum_{i}\sum_{j} I(x+i, y+j) \cdot K(i, j)$$

**Parameter:**
- **Kernel size:** Ukuran filter (3×3, 5×5, etc.)
- **Stride:** Langkah pergeseran filter
- **Padding:** Penambahan pixel di border
- **Number of filters:** Jumlah feature maps output

**Output Size:**
$$O = \frac{W - K + 2P}{S} + 1$$

di mana W = input width, K = kernel size, P = padding, S = stride.

### 3.3 Pooling Layer

**Tujuan:**
- Reduce spatial dimensions
- Provide translation invariance
- Reduce computation

**Jenis:**
- **Max Pooling:** Ambil nilai maksimum
- **Average Pooling:** Ambil rata-rata
- **Global Average Pooling:** Rata-rata seluruh feature map

### 3.4 Batch Normalization

Normalisasi aktivasi untuk setiap mini-batch:

$$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$$
$$y = \gamma \hat{x} + \beta$$

**Manfaat:**
- Training lebih stabil
- Memungkinkan learning rate lebih besar
- Regularization effect

### 3.5 Dropout

Randomly "drop" neurons selama training dengan probabilitas p.

$$\tilde{h} = h \odot m, \quad m \sim \text{Bernoulli}(1-p)$$

**Saat inference:** Scale output dengan (1-p) atau tidak drop sama sekali.

---

## 4. Arsitektur CNN Populer

### 4.1 LeNet-5 (1998)

```
Input → Conv → Pool → Conv → Pool → FC → FC → Output
(32×32)                              (10 classes)
```

**Karakteristik:**
- Arsitektur pertama yang sukses untuk digit recognition
- ~60K parameters

### 4.2 AlexNet (2012)

**Breakthrough** yang memulai era deep learning:
- 8 layers (5 conv + 3 FC)
- ~60M parameters
- ReLU activation
- Dropout
- GPU training

### 4.3 VGGNet (2014)

**Filosofi:** Gunakan filter 3×3 saja, sangat dalam

```
VGG-16: 13 Conv + 3 FC = 16 layers
VGG-19: 16 Conv + 3 FC = 19 layers
```

**Insight:** Dua 3×3 conv = satu 5×5 conv (lebih sedikit parameter)

### 4.4 GoogLeNet/Inception (2014)

**Inception Module:** Multiple filter sizes secara parallel

```
       1×1 Conv
      /   |   \
3×3 Conv 5×5 Conv Pool
      \   |   /
       Concat
```

**Keunggulan:**
- Multi-scale feature extraction
- Efficient computation dengan 1×1 conv

### 4.5 ResNet (2015)

**Problem:** Very deep networks sulit ditraining (vanishing gradient)

**Solution:** Skip connections (residual learning)

$$y = F(x) + x$$

di mana F(x) adalah residual yang dipelajari.

**Variants:**
- ResNet-18, 34, 50, 101, 152
- ResNet-50 adalah baseline yang sangat populer

### 4.6 DenseNet (2017)

**Idea:** Connect setiap layer ke semua layer sebelumnya

$$x_l = H_l([x_0, x_1, ..., x_{l-1}])$$

**Keuntungan:**
- Feature reuse
- Gradient flow lebih baik
- Lebih sedikit parameters

### 4.7 EfficientNet (2019)

**Compound Scaling:** Scale depth, width, dan resolution secara bersamaan

$$depth: d = \alpha^\phi$$
$$width: w = \beta^\phi$$
$$resolution: r = \gamma^\phi$$

dengan constraint $\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2$

---

## 5. Training Neural Networks

### 5.1 Data Augmentation

Teknik untuk meningkatkan variasi data training:

| Augmentation | Deskripsi |
|--------------|-----------|
| Random Crop | Crop random region |
| Random Flip | Flip horizontal/vertical |
| Color Jitter | Ubah brightness, contrast, saturation |
| Random Rotation | Rotasi dengan sudut random |
| Cutout | Hapus region random |
| Mixup | Campurkan dua gambar |
| CutMix | Potong dan paste dari gambar lain |

### 5.2 Optimization Algorithms

**SGD with Momentum:**
$$v_t = \gamma v_{t-1} + \eta \nabla L$$
$$\theta_t = \theta_{t-1} - v_t$$

**Adam:**
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) \nabla L$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) (\nabla L)^2$$
$$\theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

### 5.3 Learning Rate Schedule

| Schedule | Deskripsi |
|----------|-----------|
| Step Decay | Kurangi LR setiap N epoch |
| Cosine Annealing | LR mengikuti kurva cosine |
| Warmup | Mulai dari LR kecil, naikkan perlahan |
| One Cycle | Naik lalu turun dalam satu cycle |

### 5.4 Regularization Techniques

1. **L2 Regularization (Weight Decay)**
   $$L_{reg} = L + \lambda \sum_i w_i^2$$

2. **Dropout**
   - Typical: p=0.5 for FC, p=0.1-0.3 for conv

3. **Early Stopping**
   - Stop training ketika validation loss berhenti turun

4. **Label Smoothing**
   - Soft targets bukan hard 0/1

---

## 6. Transfer Learning

### 6.1 Konsep

Gunakan knowledge dari model yang sudah ditraining pada dataset besar (misalnya ImageNet) untuk task baru.

### 6.2 Strategi

**Feature Extraction:**
```
Pretrained CNN → Freeze → New FC Layer → Train
```

**Fine-tuning:**
```
Pretrained CNN → Unfreeze some/all layers → Train with small LR
```

### 6.3 Kapan Menggunakan

| Kondisi | Strategi |
|---------|----------|
| Data kecil, mirip ImageNet | Feature extraction |
| Data kecil, berbeda dari ImageNet | Fine-tune upper layers |
| Data besar, mirip ImageNet | Fine-tune all layers |
| Data besar, berbeda dari ImageNet | Train from scratch / fine-tune |

---

## 7. Object Detection Networks

### 7.1 Two-Stage Detectors

**R-CNN Family:**
- R-CNN (2014): Selective Search + CNN
- Fast R-CNN (2015): ROI Pooling
- Faster R-CNN (2016): Region Proposal Network

### 7.2 One-Stage Detectors

- **YOLO** (You Only Look Once): Grid-based detection
- **SSD** (Single Shot Detector): Multi-scale feature maps
- **RetinaNet**: Focal Loss untuk class imbalance

### 7.3 Modern Architectures

- **DETR**: Transformer-based detection
- **YOLOv5/v8**: SOTA real-time detection

---

## 8. Semantic Segmentation

### 8.1 Encoder-Decoder Architecture

```
Input → Encoder (downsampling) → Decoder (upsampling) → Output
         Conv, Pool                Deconv, Upsample
```

### 8.2 Arsitektur Populer

- **FCN** (Fully Convolutional Networks)
- **U-Net**: Skip connections antara encoder-decoder
- **DeepLab**: Atrous/Dilated convolutions
- **PSPNet**: Pyramid Pooling Module

---

## 9. Modern Trends

### 9.1 Vision Transformers (ViT)

**Idea:** Treat image sebagai sequence of patches

```
Image → Split into patches → Linear embedding → Transformer → Classification
```

### 9.2 Self-Supervised Learning

Belajar representasi tanpa label:
- **Contrastive Learning:** SimCLR, MoCo
- **Masked Image Modeling:** MAE, BEiT

### 9.3 Neural Architecture Search (NAS)

Otomasi desain arsitektur menggunakan search algorithms.

---

## 🔑 Konsep Kunci

| Konsep | Deskripsi |
|--------|-----------|
| Backpropagation | Algoritma untuk compute gradients |
| CNN | Network dengan convolutional layers |
| ReLU | Activation function paling populer |
| Batch Normalization | Normalisasi untuk stable training |
| Dropout | Regularization dengan random dropping |
| Skip Connection | Shortcut untuk gradient flow |
| Transfer Learning | Reuse pretrained weights |

---

## 📐 Formula Penting

### Convolution Output Size
$$O = \frac{W - K + 2P}{S} + 1$$

### Cross-Entropy Loss
$$L = -\sum_{i} y_i \log(\hat{y}_i)$$

### Batch Normalization
$$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

### Adam Update
$$\theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

---

## 🎯 Ringkasan

1. **Deep Learning** memungkinkan feature learning otomatis
2. **CNN** adalah arsitektur dominan untuk computer vision
3. **ResNet** memperkenalkan skip connections untuk very deep networks
4. **Batch Normalization** dan **Dropout** penting untuk regularization
5. **Transfer Learning** sangat efektif untuk dataset kecil
6. **Vision Transformers** adalah trend terbaru yang powerful

---

## 📖 Referensi

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Ed. Bab 5.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.
3. He, K., et al. (2016). Deep Residual Learning for Image Recognition.
