# Praktikum 1: Pengenalan Computer Vision dengan Python

## 🎯 Tujuan Praktikum
1. Menginstall dan mengkonfigurasi environment untuk computer vision
2. Memahami cara membaca, menampilkan, dan menyimpan citra
3. Mengenal operasi dasar pada citra
4. Memahami representasi citra digital

---

## Bagian 1: Setup Environment

### 1.1 Install Library yang Dibutuhkan

```python
# Jalankan di terminal:
# pip install numpy opencv-python matplotlib scikit-image

# Atau menggunakan conda:
# conda install numpy opencv matplotlib scikit-image
```

### 1.2 Import Library

```python
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import io, data

# Cek versi
print(f"NumPy version: {np.__version__}")
print(f"OpenCV version: {cv2.__version__}")
```

---

## Bagian 2: Memahami Citra Digital

### 2.1 Apa Itu Citra Digital?

```python
"""
Citra digital adalah representasi numerik dari gambar visual.
Citra tersusun dari elemen-elemen kecil yang disebut PIXEL (Picture Element).

Setiap pixel memiliki:
- Posisi (koordinat x, y)
- Nilai intensitas (brightness)
"""

# Mari buat citra sederhana secara manual
# Citra grayscale 5x5 pixel
citra_sederhana = np.array([
    [0,   50,  100, 150, 200],
    [50,  100, 150, 200, 255],
    [100, 150, 200, 255, 200],
    [150, 200, 255, 200, 150],
    [200, 255, 200, 150, 100]
], dtype=np.uint8)

print("Citra sederhana (5x5):")
print(citra_sederhana)
print(f"\nUkuran: {citra_sederhana.shape}")
print(f"Tipe data: {citra_sederhana.dtype}")
print(f"Nilai min: {citra_sederhana.min()}, max: {citra_sederhana.max()}")
```

### 2.2 Visualisasi Citra

```python
# Tampilkan citra
plt.figure(figsize=(10, 4))

# Subplot 1: Citra grayscale
plt.subplot(1, 2, 1)
plt.imshow(citra_sederhana, cmap='gray', vmin=0, vmax=255)
plt.title('Citra Grayscale')
plt.colorbar(label='Intensitas')

# Subplot 2: Representasi 3D dari intensitas
from mpl_toolkits.mplot3d import Axes3D
ax = plt.subplot(1, 2, 2, projection='3d')
x = np.arange(5)
y = np.arange(5)
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, citra_sederhana, cmap='viridis')
ax.set_title('Representasi 3D Intensitas')

plt.tight_layout()
plt.show()
```

---

## Bagian 3: Membaca dan Menulis Citra

### 3.1 Membaca Citra dengan OpenCV

```python
# Membaca citra berwarna
# cv2.imread() membaca dalam format BGR (bukan RGB!)
img_bgr = cv2.imread('contoh_gambar.jpg')

# Konversi ke RGB untuk ditampilkan dengan matplotlib
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# Membaca sebagai grayscale
img_gray = cv2.imread('contoh_gambar.jpg', cv2.IMREAD_GRAYSCALE)

# Tampilkan informasi
print(f"Ukuran citra BGR: {img_bgr.shape}")  # (height, width, channels)
print(f"Ukuran citra Gray: {img_gray.shape}")  # (height, width)
```

### 3.2 Menggunakan Sample Image

```python
# Gunakan gambar sample dari skimage jika tidak ada file
from skimage import data

# Load sample images
astronaut = data.astronaut()  # Citra RGB
camera = data.camera()        # Citra grayscale
coins = data.coins()          # Citra grayscale

# Tampilkan
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(astronaut)
axes[0].set_title(f'Astronaut\n{astronaut.shape}')
axes[0].axis('off')

axes[1].imshow(camera, cmap='gray')
axes[1].set_title(f'Camera\n{camera.shape}')
axes[1].axis('off')

axes[2].imshow(coins, cmap='gray')
axes[2].set_title(f'Coins\n{coins.shape}')
axes[2].axis('off')

plt.tight_layout()
plt.show()
```

### 3.3 Menyimpan Citra

```python
# Simpan citra dengan OpenCV
# Ingat: OpenCV menggunakan BGR
cv2.imwrite('output_image.jpg', img_bgr)
cv2.imwrite('output_gray.png', img_gray)

# Simpan dengan skimage
from skimage import io
io.imsave('output_skimage.png', img_rgb)

print("Citra berhasil disimpan!")
```

---

## Bagian 4: Operasi Dasar pada Citra

### 4.1 Mengakses Pixel

```python
# Gunakan sample image
img = data.astronaut()

# Akses pixel tunggal (y, x) atau (row, col)
pixel = img[100, 200]  # Di koordinat (200, 100)
print(f"Nilai pixel di (200, 100): {pixel}")  # [R, G, B]

# Modifikasi pixel
img_copy = img.copy()
img_copy[100, 200] = [255, 0, 0]  # Set ke merah

# Akses region of interest (ROI)
roi = img[100:200, 150:300]  # [y1:y2, x1:x2]
print(f"Ukuran ROI: {roi.shape}")
```

### 4.2 Memisahkan Channel Warna

```python
# Pisahkan channel RGB
R = img[:, :, 0]
G = img[:, :, 1]
B = img[:, :, 2]

# Visualisasi setiap channel
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(img)
axes[0, 0].set_title('Original RGB')

axes[0, 1].imshow(R, cmap='Reds')
axes[0, 1].set_title('Red Channel')

axes[1, 0].imshow(G, cmap='Greens')
axes[1, 0].set_title('Green Channel')

axes[1, 1].imshow(B, cmap='Blues')
axes[1, 1].set_title('Blue Channel')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### 4.3 Operasi Aritmatika pada Citra

```python
# Brightness adjustment
def adjust_brightness(img, value):
    """Menambah/mengurangi brightness"""
    # Konversi ke float untuk menghindari overflow
    img_float = img.astype(np.float32)
    img_adjusted = img_float + value
    # Clip ke range valid [0, 255]
    img_adjusted = np.clip(img_adjusted, 0, 255)
    return img_adjusted.astype(np.uint8)

# Contrast adjustment
def adjust_contrast(img, factor):
    """Mengubah contrast dengan faktor tertentu"""
    img_float = img.astype(np.float32)
    # Formula: output = factor * (input - 128) + 128
    img_adjusted = factor * (img_float - 128) + 128
    img_adjusted = np.clip(img_adjusted, 0, 255)
    return img_adjusted.astype(np.uint8)

# Demonstrasi
img = data.camera()

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

axes[0, 0].imshow(img, cmap='gray')
axes[0, 0].set_title('Original')

axes[0, 1].imshow(adjust_brightness(img, 50), cmap='gray')
axes[0, 1].set_title('Brighter (+50)')

axes[0, 2].imshow(adjust_brightness(img, -50), cmap='gray')
axes[0, 2].set_title('Darker (-50)')

axes[1, 0].imshow(img, cmap='gray')
axes[1, 0].set_title('Original')

axes[1, 1].imshow(adjust_contrast(img, 1.5), cmap='gray')
axes[1, 1].set_title('High Contrast (1.5x)')

axes[1, 2].imshow(adjust_contrast(img, 0.5), cmap='gray')
axes[1, 2].set_title('Low Contrast (0.5x)')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## Bagian 5: Histogram Citra

### 5.1 Menghitung dan Menampilkan Histogram

```python
def plot_histogram(img, title="Histogram"):
    """
    Menampilkan citra dan histogramnya
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    if len(img.shape) == 2:  # Grayscale
        axes[0].imshow(img, cmap='gray')
        axes[1].hist(img.ravel(), bins=256, range=(0, 256), color='gray')
    else:  # Color
        axes[0].imshow(img)
        colors = ('red', 'green', 'blue')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            axes[1].plot(hist, color=color, label=f'{color.upper()} channel')
        axes[1].legend()
    
    axes[0].set_title(title)
    axes[0].axis('off')
    axes[1].set_title('Histogram')
    axes[1].set_xlabel('Pixel Value')
    axes[1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()

# Demonstrasi
img_gray = data.camera()
img_color = data.astronaut()

plot_histogram(img_gray, "Grayscale Image")
plot_histogram(img_color, "Color Image")
```

### 5.2 Analisis Histogram

```python
"""
Histogram memberi informasi tentang:
1. Distribusi intensitas pixel
2. Kontras citra (lebar histogram)
3. Brightness rata-rata (posisi puncak)
4. Potensi masalah (over/under exposure)
"""

# Buat citra dengan karakteristik berbeda
img = data.camera()

# Citra gelap
img_dark = (img * 0.3).astype(np.uint8)

# Citra terang
img_bright = np.clip(img * 1.5 + 50, 0, 255).astype(np.uint8)

# Citra kontras rendah
img_low_contrast = ((img - img.min()) / (img.max() - img.min()) * 100 + 78).astype(np.uint8)

# Tampilkan perbandingan
fig, axes = plt.subplots(4, 2, figsize=(12, 16))

images = [img, img_dark, img_bright, img_low_contrast]
titles = ['Normal', 'Dark', 'Bright', 'Low Contrast']

for i, (im, title) in enumerate(zip(images, titles)):
    axes[i, 0].imshow(im, cmap='gray')
    axes[i, 0].set_title(title)
    axes[i, 0].axis('off')
    
    axes[i, 1].hist(im.ravel(), bins=256, range=(0, 256), color='gray')
    axes[i, 1].set_xlim(0, 255)
    axes[i, 1].set_title(f'Histogram - {title}')

plt.tight_layout()
plt.show()
```

---

## Bagian 6: Konversi Color Space

### 6.1 RGB ke Grayscale

```python
def rgb_to_grayscale(img_rgb):
    """
    Konversi RGB ke Grayscale menggunakan formula:
    Gray = 0.299*R + 0.587*G + 0.114*B
    
    Formula ini berdasarkan sensitivitas mata manusia
    terhadap warna yang berbeda
    """
    R = img_rgb[:, :, 0].astype(np.float32)
    G = img_rgb[:, :, 1].astype(np.float32)
    B = img_rgb[:, :, 2].astype(np.float32)
    
    gray = 0.299 * R + 0.587 * G + 0.114 * B
    return gray.astype(np.uint8)

# Demonstrasi
img_color = data.astronaut()

# Metode manual
gray_manual = rgb_to_grayscale(img_color)

# Metode OpenCV
gray_cv2 = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)

# Bandingkan
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(img_color)
axes[0].set_title('Original RGB')
axes[1].imshow(gray_manual, cmap='gray')
axes[1].set_title('Grayscale (Manual)')
axes[2].imshow(gray_cv2, cmap='gray')
axes[2].set_title('Grayscale (OpenCV)')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### 6.2 RGB ke HSV

```python
"""
HSV (Hue, Saturation, Value):
- Hue: Warna (0-180 di OpenCV)
- Saturation: Kejenuhan warna (0-255)
- Value: Kecerahan (0-255)

HSV lebih intuitif untuk manipulasi warna
"""

img_rgb = data.astronaut()
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

# Pisahkan channel
H, S, V = img_hsv[:,:,0], img_hsv[:,:,1], img_hsv[:,:,2]

# Visualisasi
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(img_rgb)
axes[0, 0].set_title('Original RGB')

axes[0, 1].imshow(H, cmap='hsv')
axes[0, 1].set_title('Hue')

axes[1, 0].imshow(S, cmap='gray')
axes[1, 0].set_title('Saturation')

axes[1, 1].imshow(V, cmap='gray')
axes[1, 1].set_title('Value')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## 📝 Latihan Praktikum

### Latihan 1: Informasi Citra
Buat fungsi `image_info(img)` yang menampilkan:
- Dimensi citra
- Tipe data
- Nilai minimum, maksimum, dan rata-rata
- Jumlah channel

### Latihan 2: Negative Image
Buat fungsi untuk menghasilkan citra negatif:
- Grayscale: `negative = 255 - original`
- Color: Terapkan pada setiap channel

### Latihan 3: Thresholding Manual
Buat fungsi `threshold(img, thresh_value)` yang menghasilkan citra biner:
- Pixel > threshold → 255 (putih)
- Pixel ≤ threshold → 0 (hitam)

### Latihan 4: Crop dan Resize
Buat program yang:
1. Membaca citra
2. Melakukan crop pada region tertentu
3. Melakukan resize ke ukuran yang ditentukan
4. Menyimpan hasilnya

---

## 📚 Referensi Tambahan

1. OpenCV Documentation: https://docs.opencv.org/
2. scikit-image Documentation: https://scikit-image.org/docs/
3. NumPy for Image Processing: https://numpy.org/doc/
