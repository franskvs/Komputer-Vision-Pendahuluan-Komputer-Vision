# BAB 2: PEMBENTUKAN CITRA (IMAGE FORMATION)

## 🎯 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami primitif geometri dan transformasi dalam computer vision
2. Menjelaskan proses pembentukan citra secara fotometrik
3. Memahami cara kerja kamera digital
4. Mengimplementasikan transformasi geometri dasar

---

## 2.1 Primitif Geometri dan Transformasi

### 2.1.1 Representasi Titik dan Garis

#### Koordinat Kartesian
```
Titik 2D: p = (x, y)
Titik 3D: P = (X, Y, Z)
```

#### Koordinat Homogen
Koordinat homogen menambahkan satu dimensi ekstra untuk memudahkan operasi transformasi.

```
2D: p = (x, y) → p̃ = (x, y, 1) atau (wx, wy, w)
3D: P = (X, Y, Z) → P̃ = (X, Y, Z, 1) atau (wX, wY, wZ, w)
```

**Keuntungan koordinat homogen:**
- Translasi menjadi operasi matriks
- Titik di infinity dapat direpresentasikan
- Transformasi dapat di-chain dengan perkalian matriks

#### Representasi Garis
Garis 2D dapat direpresentasikan sebagai:
```
ax + by + c = 0
Atau dalam bentuk vektor: l = (a, b, c)ᵀ
```

Titik p terletak pada garis l jika: **lᵀp = 0**

### 2.1.2 Transformasi 2D

#### Hierarki Transformasi 2D

```
┌─────────────────────────────────────────────────────────────┐
│                    HIERARKI TRANSFORMASI                     │
├─────────────────────────────────────────────────────────────┤
│  Transformasi      │  DOF  │  Properti Invariant            │
├────────────────────┼───────┼─────────────────────────────────┤
│  Translation       │   2   │  Orientation, Length, Angles    │
│  Euclidean         │   3   │  Length, Angles                 │
│  Similarity        │   4   │  Angles, Ratios                 │
│  Affine            │   6   │  Parallelism, Ratios pada garis │
│  Projective        │   8   │  Cross-ratio                    │
└─────────────────────────────────────────────────────────────┘
DOF = Degrees of Freedom
```

#### Matriks Transformasi

**1. Translasi (2 DOF)**
```
┌ 1  0  tₓ ┐   ┌ x ┐   ┌ x + tₓ ┐
│ 0  1  tᵧ │ × │ y │ = │ y + tᵧ │
└ 0  0  1  ┘   └ 1 ┘   └   1    ┘
```

**2. Rotasi (1 DOF)**
```
┌ cos θ  -sin θ  0 ┐
│ sin θ   cos θ  0 │
└   0       0    1 ┘
```

**3. Euclidean/Rigid (3 DOF)** - Rotasi + Translasi
```
┌ cos θ  -sin θ  tₓ ┐
│ sin θ   cos θ  tᵧ │
└   0       0    1  ┘
```

**4. Similarity (4 DOF)** - Euclidean + Uniform Scale
```
┌ s·cos θ  -s·sin θ  tₓ ┐
│ s·sin θ   s·cos θ  tᵧ │
└    0         0      1 ┘
```

**5. Affine (6 DOF)**
```
┌ a₁₁  a₁₂  tₓ ┐
│ a₂₁  a₂₂  tᵧ │
└  0    0   1  ┘
```

**6. Projective/Homography (8 DOF)**
```
┌ h₁₁  h₁₂  h₁₃ ┐
│ h₂₁  h₂₂  h₂₃ │
└ h₃₁  h₃₂  h₃₃ ┘
```

### 2.1.3 Transformasi 3D

#### Rotasi 3D

**1. Rotasi sekitar sumbu X**
```
Rₓ(θ) = ┌ 1    0       0    ┐
        │ 0  cos θ  -sin θ  │
        └ 0  sin θ   cos θ  ┘
```

**2. Rotasi sekitar sumbu Y**
```
Rᵧ(θ) = ┌  cos θ  0  sin θ ┐
        │    0    1    0   │
        └ -sin θ  0  cos θ ┘
```

**3. Rotasi sekitar sumbu Z**
```
R_z(θ) = ┌ cos θ  -sin θ  0 ┐
         │ sin θ   cos θ  0 │
         └   0       0    1 ┘
```

#### Representasi Rotasi

| Representasi | Parameter | Kelebihan | Kekurangan |
|--------------|-----------|-----------|------------|
| Euler Angles | 3 | Intuitif | Gimbal lock |
| Axis-Angle | 4 (3+1) | Efisien | Tidak unik untuk θ=0 |
| Quaternion | 4 | Interpolasi smooth | Kurang intuitif |
| Rotation Matrix | 9 | Komposisi mudah | Redundan |

#### Quaternion
```
q = (w, x, y, z) = w + xi + yj + zk
dimana: i² = j² = k² = ijk = -1

Unit quaternion: |q| = √(w² + x² + y² + z²) = 1
```

### 2.1.4 Proyeksi 3D ke 2D

#### Model Kamera Pinhole

```
                    Image Plane
                         │
    3D Point  ─────────○─┼──────────── Optical Axis
       P              ╲  │
                       ╲ │f (focal length)
                        ╲│
                     ────●──── Camera Center
                         C
```

**Persamaan Proyeksi:**
```
x = f · X/Z
y = f · Y/Z
```

Dalam bentuk matriks (koordinat homogen):
```
┌ x̃ ┐   ┌ f  0  0  0 ┐   ┌ X ┐
│ ỹ │ = │ 0  f  0  0 │ × │ Y │
└ z̃ ┘   └ 0  0  1  0 ┘   │ Z │
                         └ 1 ┘
```

#### Matriks Intrinsik Kamera (K)

```
K = ┌ fₓ  s   cₓ ┐
    │ 0   fᵧ  cᵧ │
    └ 0   0   1  ┘

dimana:
- fₓ, fᵧ = focal length dalam pixel
- (cₓ, cᵧ) = principal point
- s = skew parameter (biasanya 0)
```

#### Matriks Proyeksi Lengkap

```
P = K [R | t]

dimana:
- K = matriks intrinsik (3×3)
- R = matriks rotasi (3×3)
- t = vektor translasi (3×1)
```

### 2.1.5 Distorsi Lensa

#### Distorsi Radial
```
x_distorted = x(1 + k₁r² + k₂r⁴ + k₃r⁶)
y_distorted = y(1 + k₁r² + k₂r⁴ + k₃r⁶)

dimana r² = x² + y²
```

**Jenis distorsi:**
- k > 0: Barrel distortion (pinggir membengkak)
- k < 0: Pincushion distortion (pinggir menciut)

#### Distorsi Tangensial
```
x_distorted = x + [2p₁xy + p₂(r² + 2x²)]
y_distorted = y + [p₁(r² + 2y²) + 2p₂xy]
```

---

## 2.2 Pembentukan Citra Fotometrik

### 2.2.1 Pencahayaan (Lighting)

#### Sumber Cahaya

**1. Point Light (Titik)**
- Intensitas menurun dengan jarak kuadrat
- L ∝ 1/r²

**2. Directional Light (Arah)**
- Sinar paralel (seperti matahari)
- Intensitas konstan

**3. Area Light (Area)**
- Sumber cahaya dengan luas
- Menghasilkan soft shadow

#### Ambient vs Direct Illumination
```
I_total = I_ambient + I_direct
```

### 2.2.2 Reflectance dan Shading

#### BRDF (Bidirectional Reflectance Distribution Function)
```
f_r(ωᵢ, ωᵣ) = dL_r(ωᵣ) / dE_i(ωᵢ)
```

#### Model Refleksi

**1. Lambertian (Diffuse)**
- Cahaya dipantulkan merata ke semua arah
- Intensitas bergantung pada sudut datang
```
I = I_light × k_d × cos(θ)
  = I_light × k_d × (N · L)
```

**2. Specular (Phong Model)**
```
I = k_s × (R · V)^n

dimana:
- R = reflect direction
- V = view direction
- n = shininess
```

**3. Model Phong Lengkap**
```
I = I_a × k_a + I_d × k_d × (N·L) + I_s × k_s × (R·V)^n
    ─────────   ─────────────────   ───────────────────
     Ambient        Diffuse              Specular
```

### 2.2.3 Optik

#### Thin Lens Equation
```
1/f = 1/d_o + 1/d_i

dimana:
- f = focal length
- d_o = jarak objek
- d_i = jarak image
```

#### Depth of Field
```
DoF ∝ (f-number)² × d²

Aperture besar (f kecil) → DoF sempit
Aperture kecil (f besar) → DoF lebar
```

---

## 2.3 Kamera Digital

### 2.3.1 Sensor

#### CCD vs CMOS
| Fitur | CCD | CMOS |
|-------|-----|------|
| Konsumsi daya | Tinggi | Rendah |
| Kecepatan | Lambat | Cepat |
| Noise | Rendah | Lebih tinggi |
| Biaya | Mahal | Murah |
| Aplikasi | Kamera pro | Smartphone |

#### Bayer Pattern
```
┌───┬───┬───┬───┐
│ R │ G │ R │ G │
├───┼───┼───┼───┤
│ G │ B │ G │ B │
├───┼───┼───┼───┤
│ R │ G │ R │ G │
├───┼───┼───┼───┤
│ G │ B │ G │ B │
└───┴───┴───┴───┘
```

### 2.3.2 Sampling dan Aliasing

#### Nyquist Theorem
```
f_sampling ≥ 2 × f_max

Jika tidak dipenuhi → Aliasing!
```

**Anti-aliasing:**
- Optical low-pass filter
- Oversampling + downsampling

### 2.3.3 Color

#### Color Spaces
- **RGB**: Red, Green, Blue (additive)
- **CMY/CMYK**: Cyan, Magenta, Yellow, Black (subtractive)
- **HSV**: Hue, Saturation, Value
- **YUV/YCbCr**: Luminance, Chrominance
- **Lab**: Perceptually uniform

#### White Balance
```
R_corrected = R × gain_R
G_corrected = G × gain_G
B_corrected = B × gain_B
```

### 2.3.4 Kompresi

#### JPEG
1. Konversi RGB → YCbCr
2. Downsampling chrominance (4:2:0)
3. Block 8×8 DCT
4. Quantization
5. Entropy coding (Huffman)

---

## 2.4 Diagram Ringkasan

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMAGE FORMATION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  3D World          Camera Model         2D Image                │
│  ════════         ═════════════        ══════════               │
│                                                                  │
│  Objek 3D    →    Proyeksi        →    Sensor       → Citra     │
│  (X,Y,Z)          Perspektif           Digital         Digital  │
│                   P = K[R|t]                                     │
│                                                                  │
│  Lighting   →     BRDF/           →    Sampling     → Pixel     │
│  (Sumber)         Shading              & Aliasing     Values    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Rumus-Rumus Penting

### Transformasi
```
Homogeneous 2D: p' = H × p  (H: 3×3)
Homogeneous 3D: P' = T × P  (T: 4×4)
```

### Proyeksi
```
p = K × [R|t] × P

┌ u ┐     ┌ fx  0  cx ┐   ┌ r11 r12 r13 tx ┐   ┌ X ┐
│ v │ = s │ 0  fy  cy │ × │ r21 r22 r23 ty │ × │ Y │
└ 1 ┘     └ 0   0   1 ┘   └ r31 r32 r33 tz ┘   │ Z │
                                               └ 1 ┘
```

### Refleksi
```
Lambertian: I = ρ × max(0, N·L) × I_light
Phong:      I = I_a × k_a + I_d × k_d × (N·L) + I_s × k_s × (R·V)^n
```

---

## Pertanyaan Diskusi

1. Mengapa koordinat homogen penting dalam computer vision?
2. Apa perbedaan fundamental antara transformasi affine dan projective?
3. Bagaimana distorsi lensa mempengaruhi rekonstruksi 3D?
4. Mengapa model Lambertian sering digunakan meskipun tidak akurat untuk semua permukaan?

---

## Referensi Bab Ini

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, Chapter 2
2. Hartley, R., & Zisserman, A. (2004). Multiple View Geometry in Computer Vision
3. Forsyth, D. A., & Ponce, J. (2012). Computer Vision: A Modern Approach, Ch. 1-5
