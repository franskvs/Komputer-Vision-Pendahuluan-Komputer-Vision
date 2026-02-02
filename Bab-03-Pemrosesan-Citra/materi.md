# Bab 3: Pemrosesan Citra (Image Processing)

## 📚 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami berbagai operasi point processing pada citra
2. Menerapkan filtering linear dan non-linear
3. Melakukan transformasi Fourier dan analisis frekuensi
4. Memahami piramida citra dan representasi multi-skala
5. Mengimplementasikan operasi geometrik pada citra
6. Melakukan interpolasi dan resampling citra

---

## 1. Point Operators

### 1.1 Definisi Point Operator
**Point operator** adalah operasi yang mengubah nilai pixel berdasarkan nilai pixel itu sendiri, tanpa memperhatikan tetangga:

$$g(x,y) = h(f(x,y))$$

di mana $f$ adalah citra input dan $h$ adalah fungsi transfer.

### 1.2 Transformasi Intensitas

#### Transformasi Linear (Brightness dan Contrast)
```python
g(x) = α * f(x) + β
```
- **α** (gain): mengontrol contrast
  - α > 1: meningkatkan contrast
  - α < 1: menurunkan contrast
- **β** (bias): mengontrol brightness
  - β > 0: lebih terang
  - β < 0: lebih gelap

#### Gamma Correction
```python
g = c * f^γ
```
- γ < 1: mencerahkan bayangan (shadows)
- γ > 1: menggelapkan highlights
- Digunakan untuk koreksi display dan menyesuaikan dynamic range

#### Histogram Equalization
Tujuan: menyebarkan distribusi intensitas secara merata

**Algoritma:**
1. Hitung histogram $h(i)$
2. Hitung CDF: $c(i) = \sum_{j=0}^{i} h(j)$
3. Normalisasi: $T(i) = \frac{c(i) - c_{min}}{N - c_{min}} \times 255$

### 1.3 Operasi Aritmatika Citra

| Operasi | Formula | Aplikasi |
|---------|---------|----------|
| Addition | g = f₁ + f₂ | Image blending, menambah brightness |
| Subtraction | g = f₁ - f₂ | Change detection, background removal |
| Multiplication | g = f₁ × f₂ | Masking, shading correction |
| Division | g = f₁ / f₂ | Ratio imaging, flat-field correction |

### 1.4 Color Transformations

#### Color Space Conversions
- **RGB ↔ HSV**: Untuk manipulasi warna intuitif
- **RGB ↔ Lab**: Untuk operasi yang perceptually uniform
- **RGB ↔ YCbCr**: Untuk kompresi video

#### White Balance
Koreksi warna untuk pencahayaan berbeda:
```python
# Gray world assumption
R_avg, G_avg, B_avg = mean(R), mean(G), mean(B)
avg_gray = (R_avg + G_avg + B_avg) / 3
R_corrected = R * (avg_gray / R_avg)
```

---

## 2. Filtering Linear (Convolution)

### 2.1 Konsep Konvolusi

Konvolusi 2D discrete:
$$g(x,y) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} f(x+i, y+j) \cdot h(i,j)$$

di mana $h$ adalah **kernel** atau **filter**.

### 2.2 Jenis-jenis Filter

#### Smoothing Filters (Low-pass)

**Box Filter (Mean Filter)**
```
     | 1 1 1 |
1/9  | 1 1 1 |
     | 1 1 1 |
```
- Sederhana, cepat
- Menyebabkan blurring yang tidak natural

**Gaussian Filter**
$$G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$

- Smoothing yang lebih natural
- Separable: dapat didekomposisi menjadi 2 filter 1D
- Properti: rotationally symmetric

**Contoh Kernel Gaussian 3×3 (σ ≈ 1)**
```
       | 1 2 1 |
1/16   | 2 4 2 |
       | 1 2 1 |
```

#### Sharpening Filters (High-pass)

**Unsharp Masking**
```python
sharpened = original + α * (original - blurred)
```

**Laplacian**
```
     | 0  1  0 |        | 1  1  1 |
     | 1 -4  1 |   atau | 1 -8  1 |
     | 0  1  0 |        | 1  1  1 |
```

#### Edge Detection Filters

**Sobel Operator**
```
         | -1 0 1 |            | -1 -2 -1 |
Gx = 1/4 | -2 0 2 |   Gy = 1/4 |  0  0  0 |
         | -1 0 1 |            |  1  2  1 |
```

Gradient magnitude: $G = \sqrt{G_x^2 + G_y^2}$
Gradient direction: $\theta = \arctan(G_y / G_x)$

**Prewitt Operator**
```
         | -1 0 1 |            | -1 -1 -1 |
Gx = 1/3 | -1 0 1 |   Gy = 1/3 |  0  0  0 |
         | -1 0 1 |            |  1  1  1 |
```

**Scharr Operator** (lebih akurat untuk sudut)
```
           | -3  0  3 |            | -3 -10 -3 |
Gx = 1/16  | -10 0 10 |   Gy = 1/16|  0   0  0 |
           | -3  0  3 |            |  3  10  3 |
```

### 2.3 Border Handling

| Metode | Deskripsi |
|--------|-----------|
| Zero padding | Pixel luar = 0 |
| Replicate | Pixel tepi diulang |
| Reflect | Mirror dari tepi |
| Wrap | Circular wrap-around |

### 2.4 Separable Filters

Filter separable dapat ditulis sebagai outer product:
$$h = \mathbf{v} \cdot \mathbf{u}^T$$

**Keuntungan:**
- Kompleksitas dari O(k²n²) menjadi O(2kn²)
- Gaussian filter adalah separable

---

## 3. Non-linear Filtering

### 3.1 Mengapa Non-linear?

Linear filter memiliki keterbatasan:
- Tidak dapat menghilangkan noise sambil mempertahankan edge
- Gaussian blur memudarkan tepi

### 3.2 Median Filter

**Konsep:** Ganti pixel dengan median dari tetangganya

**Kelebihan:**
- Sangat efektif untuk salt-and-pepper noise
- Mempertahankan edge
- Robust terhadap outlier

**Kekurangan:**
- Lebih lambat dari linear filter
- Dapat menghilangkan detail kecil

### 3.3 Bilateral Filter

Kombinasi spatial proximity dan intensity similarity:

$$g(x,y) = \frac{1}{W} \sum_{i,j} f(i,j) \cdot G_s(||p-q||) \cdot G_r(|f(p)-f(q)|)$$

di mana:
- $G_s$: Gaussian spatial (jarak posisi)
- $G_r$: Gaussian range (jarak intensitas)
- $W$: faktor normalisasi

**Kelebihan:**
- Edge-preserving smoothing
- Mengurangi noise tanpa blur edge

### 3.4 Morphological Operations

Operasi pada citra biner menggunakan structuring element.

#### Operasi Dasar

**Dilation (Dilasi)**
$$A \oplus B = \{z | (B_z \cap A) \neq \emptyset\}$$
- Memperbesar objek
- Mengisi lubang kecil

**Erosion (Erosi)**
$$A \ominus B = \{z | B_z \subseteq A\}$$
- Mengecilkan objek
- Menghilangkan noise kecil

#### Operasi Turunan

**Opening** (Erosion → Dilation)
$$A \circ B = (A \ominus B) \oplus B$$
- Menghilangkan protrusi kecil
- Smoothing kontur

**Closing** (Dilation → Erosion)
$$A \bullet B = (A \oplus B) \ominus B$$
- Mengisi lubang kecil
- Menyambung gap

**Morphological Gradient**
$$grad(A) = (A \oplus B) - (A \ominus B)$$
- Deteksi tepi pada citra biner

### 3.5 Distance Transform

Menghitung jarak setiap pixel ke pixel background terdekat:

$$D(x,y) = \min_{(x',y') \in B} ||{(x,y) - (x',y')}||$$

**Metrik jarak:**
- Euclidean: $\sqrt{(x-x')^2 + (y-y')^2}$
- Manhattan (City block): $|x-x'| + |y-y'|$
- Chessboard: $\max(|x-x'|, |y-y'|)$

---

## 4. Fourier Transform

### 4.1 Transformasi Fourier 2D

**Continuous:**
$$F(u,v) = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f(x,y) e^{-j2\pi(ux+vy)} dx\,dy$$

**Discrete (DFT):**
$$F(u,v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x,y) e^{-j2\pi(\frac{ux}{M}+\frac{vy}{N})}$$

### 4.2 Sifat-sifat Penting

| Sifat | Domain Spasial | Domain Frekuensi |
|-------|----------------|------------------|
| Linearity | af₁ + bf₂ | aF₁ + bF₂ |
| Translation | f(x-a, y-b) | F(u,v)e^{-j2π(ua/M+vb/N)} |
| Rotation | f(r, θ+θ₀) | F(ρ, φ+θ₀) |
| Scaling | f(ax, by) | F(u/a, v/b)/|ab| |
| Convolution | f * g | F · G |

### 4.3 Spektrum Frekuensi

**Magnitude Spectrum:**
$$|F(u,v)| = \sqrt{R^2(u,v) + I^2(u,v)}$$

**Phase Spectrum:**
$$\phi(u,v) = \arctan\left(\frac{I(u,v)}{R(u,v)}\right)$$

**Interpretasi:**
- Frekuensi rendah (center): informasi global, brightness
- Frekuensi tinggi (edge): detail, edge, noise

### 4.4 Filtering di Domain Frekuensi

**Proses:**
1. Hitung DFT: $F = \mathcal{F}\{f\}$
2. Kalikan dengan filter: $G = H \cdot F$
3. Inverse DFT: $g = \mathcal{F}^{-1}\{G\}$

**Jenis Filter:**

**Ideal Low-pass:**
$$H(u,v) = \begin{cases} 1 & D(u,v) \leq D_0 \\ 0 & D(u,v) > D_0 \end{cases}$$

**Butterworth Low-pass:**
$$H(u,v) = \frac{1}{1 + [D(u,v)/D_0]^{2n}}$$

**Gaussian Low-pass:**
$$H(u,v) = e^{-D^2(u,v)/2D_0^2}$$

---

## 5. Piramida Citra dan Multi-Scale

### 5.1 Gaussian Pyramid

**Konstruksi:**
1. Mulai dari level 0 (gambar asli)
2. Blur dengan Gaussian
3. Downsample 2x
4. Ulangi untuk level berikutnya

**Reduksi:**
$$G_l = \text{downsample}(G_{l-1} * g)$$

di mana $g$ adalah kernel Gaussian.

### 5.2 Laplacian Pyramid

**Konsep:** Menyimpan perbedaan antar level

$$L_l = G_l - \text{upsample}(G_{l+1})$$

**Kegunaan:**
- Kompresi citra
- Image blending
- Texture synthesis

### 5.3 Scale Space

Representasi citra pada berbagai skala:

$$L(x,y,\sigma) = G(x,y,\sigma) * f(x,y)$$

di mana σ adalah parameter skala.

**Difference of Gaussians (DoG):**
$$D(x,y,\sigma) = L(x,y,k\sigma) - L(x,y,\sigma)$$

Digunakan untuk deteksi blob dan fitur pada SIFT.

### 5.4 Applications

1. **Image Blending:** Laplacian pyramid blending untuk seamless composite
2. **Feature Detection:** Multi-scale detection (SIFT, ORB)
3. **Object Detection:** Sliding window pada berbagai skala
4. **Super-resolution:** Merekonstruksi detail dari piramida

---

## 6. Operasi Geometrik

### 6.1 Transformasi Dasar

#### Flipping
```python
horizontal_flip: f(x, y) → f(W-1-x, y)
vertical_flip: f(x, y) → f(x, H-1-y)
```

#### Rotation
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$

#### Scaling
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$

### 6.2 Warping dan Interpolasi

**Proses Warping:**
1. Definisikan transformasi T
2. Untuk setiap pixel output (x', y')
3. Hitung koordinat sumber (x, y) = T⁻¹(x', y')
4. Interpolasi nilai dari citra sumber

### 6.3 Metode Interpolasi

#### Nearest Neighbor
- Ambil nilai pixel terdekat
- Cepat tapi menghasilkan artifact

#### Bilinear Interpolation
Interpolasi linear di kedua arah:
$$f(x,y) = (1-a)(1-b)f_{00} + a(1-b)f_{10} + (1-a)b f_{01} + ab f_{11}$$

di mana a dan b adalah jarak fraksional.

#### Bicubic Interpolation
- Menggunakan 16 tetangga terdekat
- Hasil lebih smooth
- Lebih lambat dari bilinear

### 6.4 Resampling

**Downsampling:**
- Harus di-blur dulu (anti-aliasing)
- Mencegah aliasing artifact

**Upsampling:**
- Interpolasi untuk mengisi pixel baru
- Tidak dapat menambah informasi baru

---

## 7. Canny Edge Detection

### 7.1 Langkah-langkah Algoritma

1. **Gaussian Smoothing**
   - Reduksi noise
   - Pilih σ berdasarkan skala edge yang diinginkan

2. **Gradient Computation**
   - Hitung magnitude dan direction
   - Biasanya dengan Sobel operator

3. **Non-maximum Suppression (NMS)**
   - Thin edges ke 1 pixel
   - Pertahankan hanya local maxima dalam arah gradient

4. **Double Thresholding**
   - High threshold: edge kuat
   - Low threshold: edge kandidat

5. **Edge Tracking by Hysteresis**
   - Edge kuat selalu diterima
   - Edge lemah diterima jika terhubung ke edge kuat

### 7.2 Parameter Tuning

| Parameter | Efek Jika Tinggi | Efek Jika Rendah |
|-----------|------------------|------------------|
| σ (Gaussian) | Edge lebih smooth | Detail lebih banyak |
| High threshold | Lebih sedikit edge | Lebih banyak edge |
| Low threshold | Edge lebih banyak terhubung | Edge terputus |

---

## 8. Segmentasi Dasar

### 8.1 Thresholding

**Global Thresholding:**
$$g(x,y) = \begin{cases} 1 & f(x,y) > T \\ 0 & f(x,y) \leq T \end{cases}$$

**Otsu's Method:**
- Threshold optimal yang memaksimalkan between-class variance
- Automatic threshold selection

### 8.2 Adaptive Thresholding

Threshold berbeda untuk setiap region:
$$T(x,y) = \text{mean}(N(x,y)) - C$$

di mana N(x,y) adalah neighborhood dan C adalah konstanta.

### 8.3 Connected Components

**Algoritma:**
1. Scan gambar
2. Assign label ke pixel foreground
3. Merge label yang terhubung
4. Relabel secara sequential

**Konektivitas:**
- 4-connected: atas, bawah, kiri, kanan
- 8-connected: termasuk diagonal

---

## 🔑 Konsep Kunci

| Konsep | Deskripsi |
|--------|-----------|
| Point operators | Operasi pixel-wise tanpa tetangga |
| Convolution | Operasi linear dengan kernel |
| Gaussian filter | Smoothing yang rotationally symmetric |
| Bilateral filter | Edge-preserving smoothing |
| Morphology | Operasi shape-based pada biner |
| Fourier Transform | Representasi frekuensi |
| Pyramid | Multi-scale representation |
| Canny | Gold standard edge detection |

---

## 📐 Formula Penting

### Konvolusi 2D
$$g(x,y) = \sum_{i,j} f(x+i, y+j) \cdot h(i,j)$$

### Gaussian Kernel
$$G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$

### Sobel Gradient Magnitude
$$G = \sqrt{G_x^2 + G_y^2}$$

### DFT 2D
$$F(u,v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x,y) e^{-j2\pi(ux/M+vy/N)}$$

---

## 🎯 Ringkasan

1. **Point operators** mengubah intensitas tanpa memperhatikan spasial
2. **Linear filtering** menggunakan konvolusi untuk smoothing, sharpening, edge detection
3. **Non-linear filtering** (median, bilateral) lebih baik untuk preserving edges
4. **Fourier transform** memungkinkan analisis dan filtering di domain frekuensi
5. **Image pyramids** menyediakan representasi multi-scale
6. **Geometric operations** memerlukan interpolasi yang tepat
7. **Canny detector** adalah algoritma edge detection yang robust

---

## 📖 Referensi

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Ed. Bab 3.
2. Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing.
3. OpenCV Documentation: Image Processing Tutorials
