# Bab 4: Model Fitting dan Optimisasi

## 📚 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami konsep fitting model ke data
2. Menerapkan berbagai metode optimisasi
3. Mengimplementasikan RANSAC untuk robust estimation
4. Memahami Hough Transform untuk deteksi bentuk
5. Menerapkan regularisasi dan model selection

---

## 1. Pengantar Model Fitting

### 1.1 Apa itu Model Fitting?

**Model fitting** adalah proses menemukan parameter model matematika yang paling sesuai dengan data observasi.

**Contoh dalam Computer Vision:**
- Fitting garis ke edge points
- Fitting homography ke point correspondences
- Fitting pose kamera ke 2D-3D correspondences

### 1.2 Formulasi Matematis

Diberikan:
- Data observasi: $\{(x_i, y_i)\}_{i=1}^{N}$
- Model dengan parameter $\theta$: $y = f(x; \theta)$

Tujuan: Temukan $\theta^*$ yang meminimalkan error:
$$\theta^* = \arg\min_\theta \sum_{i=1}^{N} \rho(y_i - f(x_i; \theta))$$

di mana $\rho$ adalah fungsi loss.

### 1.3 Jenis Error Metrics

| Metric | Formula | Karakteristik |
|--------|---------|---------------|
| Squared Error (L2) | $\rho(e) = e^2$ | Sensitif terhadap outlier |
| Absolute Error (L1) | $\rho(e) = \|e\|$ | Lebih robust |
| Huber Loss | $\rho(e) = \begin{cases} e^2/2 & \|e\| \leq \delta \\ \delta(\|e\|-\delta/2) & \text{otherwise} \end{cases}$ | Kombinasi L1 dan L2 |
| Tukey Biweight | Redescending | Sangat robust |

---

## 2. Least Squares

### 2.1 Linear Least Squares

**Problem:** Selesaikan sistem overdetermined $Ax = b$

**Solusi Normal Equation:**
$$A^T A x = A^T b$$
$$x = (A^T A)^{-1} A^T b$$

**Solusi dengan Pseudoinverse:**
$$x = A^+ b = (A^T A)^{-1} A^T b$$

**Contoh: Fitting Garis**
```python
# Data points: (x_i, y_i)
# Model: y = mx + c
# Rewrite: [x_i, 1] @ [m, c]^T = y_i

A = np.column_stack([x, np.ones(len(x))])
b = y
params = np.linalg.lstsq(A, b, rcond=None)[0]
m, c = params
```

### 2.2 Weighted Least Squares

Ketika observasi memiliki kepastian berbeda:
$$x = (A^T W A)^{-1} A^T W b$$

di mana $W$ adalah diagonal matrix dengan weight $w_i$.

### 2.3 Total Least Squares

Meminimalkan error pada semua variabel (x dan y):
$$\min \sum_i (x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2$$

dengan constraint bahwa $(\hat{x}_i, \hat{y}_i)$ berada pada garis.

**Solusi:** Gunakan SVD dari $[A | b]$.

### 2.4 Non-linear Least Squares

Untuk model non-linear $y = f(x; \theta)$:

**Gauss-Newton:**
$$\theta_{k+1} = \theta_k - (J^T J)^{-1} J^T r(\theta_k)$$

di mana:
- $J$ = Jacobian matrix $\frac{\partial r}{\partial \theta}$
- $r(\theta)$ = residual vector

**Levenberg-Marquardt:**
$$\theta_{k+1} = \theta_k - (J^T J + \lambda I)^{-1} J^T r(\theta_k)$$

- Kombinasi Gauss-Newton dan gradient descent
- $\lambda$ mengontrol trade-off

---

## 3. RANSAC (Random Sample Consensus)

### 3.1 Mengapa RANSAC?

Least squares sensitif terhadap **outliers**. RANSAC adalah metode robust yang dapat menangani data dengan banyak outlier.

### 3.2 Algoritma RANSAC

```
Input: Data D, model M, threshold t, iterations N
Output: Best model parameters, inlier set

1. For i = 1 to N:
   a. Randomly sample minimal set S from D
   b. Fit model M to S
   c. Count inliers: points with error < t
   d. If inliers > best_count:
      - Update best_model
      - Update best_inliers
      - Update best_count

2. Refit model using all inliers
3. Return best_model, best_inliers
```

### 3.3 Parameter RANSAC

**Jumlah iterasi (N):**
$$N = \frac{\log(1-p)}{\log(1-w^n)}$$

di mana:
- $p$ = probabilitas sukses yang diinginkan (biasanya 0.99)
- $w$ = rasio inlier dalam data
- $n$ = minimal sample size

**Contoh:**
- Jika 50% inlier ($w=0.5$), fitting garis ($n=2$), $p=0.99$:
- $N = \frac{\log(0.01)}{\log(1-0.25)} \approx 16$ iterasi

### 3.4 Variasi RANSAC

| Variasi | Deskripsi |
|---------|-----------|
| MSAC | Mengganti counting dengan scoring inlier |
| MLESAC | Maximum Likelihood estimation |
| LO-RANSAC | Local optimization setelah menemukan model bagus |
| PROSAC | Progressive sampling (prioritaskan fitur yang lebih baik) |

### 3.5 Aplikasi RANSAC

1. **Homography Estimation** - 4 point correspondences
2. **Fundamental Matrix** - 7 atau 8 points
3. **Essential Matrix** - 5 points
4. **3D Plane Fitting** - 3 points
5. **Pose Estimation (PnP)** - Minimal 4 points

---

## 4. Hough Transform

### 4.1 Konsep Dasar

Hough Transform mengubah deteksi bentuk menjadi **voting problem** dalam parameter space.

### 4.2 Hough Transform untuk Garis

**Representasi Garis:**
- Slope-intercept: $y = mx + c$ (tidak bisa vertikal)
- Normal form: $x\cos\theta + y\sin\theta = \rho$

**Algoritma:**
1. Buat accumulator array $H(\rho, \theta)$
2. Untuk setiap edge point $(x_i, y_i)$:
   - Untuk setiap $\theta$:
     - Hitung $\rho = x_i\cos\theta + y_i\sin\theta$
     - Increment $H(\rho, \theta)$
3. Temukan peaks dalam $H$ → parameter garis

### 4.3 Hough Transform untuk Lingkaran

**Representasi Lingkaran:**
$(x-a)^2 + (y-b)^2 = r^2$

**Accumulator:** 3D space $(a, b, r)$

**Optimisasi:** Jika radius diketahui, hanya 2D accumulator.

### 4.4 Generalized Hough Transform

Untuk bentuk arbitrary yang didefinisikan oleh R-table (lookup table dari edge direction ke displacement).

### 4.5 Probabilistic Hough Transform

- Sampling subset dari edge points
- Lebih cepat untuk gambar besar
- OpenCV: `cv2.HoughLinesP()`

---

## 5. Metode Optimisasi

### 5.1 Gradient Descent

**Batch Gradient Descent:**
$$\theta_{t+1} = \theta_t - \alpha \nabla_\theta L(\theta_t)$$

di mana $\alpha$ adalah learning rate.

**Stochastic Gradient Descent (SGD):**
Update menggunakan satu sample pada setiap iterasi.

**Mini-batch Gradient Descent:**
Kompromi antara batch dan stochastic.

### 5.2 Momentum Methods

**Momentum:**
$$v_t = \gamma v_{t-1} + \alpha \nabla_\theta L(\theta_t)$$
$$\theta_{t+1} = \theta_t - v_t$$

**Nesterov Accelerated Gradient:**
$$v_t = \gamma v_{t-1} + \alpha \nabla_\theta L(\theta_t - \gamma v_{t-1})$$

### 5.3 Adaptive Learning Rate

**AdaGrad:**
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{G_t + \epsilon}} g_t$$

**RMSprop:**
$$E[g^2]_t = \gamma E[g^2]_{t-1} + (1-\gamma) g_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{E[g^2]_t + \epsilon}} g_t$$

**Adam (Adaptive Moment Estimation):**
Kombinasi momentum dan RMSprop - paling populer untuk deep learning.

### 5.4 Second-order Methods

**Newton's Method:**
$$\theta_{t+1} = \theta_t - H^{-1} \nabla_\theta L$$

di mana $H$ adalah Hessian matrix.

**Quasi-Newton (BFGS, L-BFGS):**
Approximasi Hessian tanpa menghitung penuh.

---

## 6. Regularisasi

### 6.1 Mengapa Regularisasi?

Mencegah **overfitting** dengan menambahkan constraint pada parameter.

### 6.2 Jenis Regularisasi

**L2 Regularization (Ridge):**
$$L_{reg} = L + \lambda ||\theta||_2^2$$

- Membuat parameter kecil
- Tidak menghasilkan sparsity

**L1 Regularization (Lasso):**
$$L_{reg} = L + \lambda ||\theta||_1$$

- Menghasilkan sparse solution
- Feature selection

**Elastic Net:**
$$L_{reg} = L + \lambda_1 ||\theta||_1 + \lambda_2 ||\theta||_2^2$$

### 6.3 Regularisasi dalam CV

- **Smoothness prior:** Constrain solusi agar smooth
- **Total Variation:** Preserve edges dalam denoising
- **Sparsity:** Untuk compressed sensing dan sparse reconstruction

---

## 7. Model Selection

### 7.1 Kriteria Model Selection

**Akaike Information Criterion (AIC):**
$$AIC = 2k - 2\ln(L)$$

**Bayesian Information Criterion (BIC):**
$$BIC = k\ln(n) - 2\ln(L)$$

di mana:
- $k$ = jumlah parameter
- $n$ = jumlah data points
- $L$ = maximum likelihood

### 7.2 Cross-Validation

**k-Fold Cross-Validation:**
1. Bagi data menjadi k fold
2. Untuk setiap fold:
   - Train pada k-1 fold
   - Test pada 1 fold
3. Average error

**Leave-One-Out Cross-Validation:**
Special case dengan k = n.

### 7.3 Bias-Variance Tradeoff

$$Error = Bias^2 + Variance + Irreducible\ Error$$

- **High Bias:** Model terlalu simple (underfitting)
- **High Variance:** Model terlalu complex (overfitting)

---

## 8. Aplikasi: Line Fitting

### 8.1 Least Squares Line Fitting

```python
def fit_line_least_squares(points):
    """
    Fit line y = mx + c using least squares
    
    Parameters:
        points: (N, 2) array of (x, y) points
    
    Returns:
        m, c: slope and intercept
    """
    x = points[:, 0]
    y = points[:, 1]
    
    A = np.column_stack([x, np.ones(len(x))])
    params = np.linalg.lstsq(A, y, rcond=None)[0]
    
    return params[0], params[1]
```

### 8.2 RANSAC Line Fitting

```python
def fit_line_ransac(points, threshold=5, iterations=100):
    """
    RANSAC line fitting
    
    Parameters:
        points: (N, 2) array
        threshold: inlier threshold
        iterations: max iterations
    
    Returns:
        best_line: (m, c)
        inliers: boolean mask
    """
    best_inliers = None
    best_count = 0
    
    for _ in range(iterations):
        # Sample 2 points
        idx = np.random.choice(len(points), 2, replace=False)
        p1, p2 = points[idx]
        
        # Fit line through 2 points
        if p2[0] - p1[0] == 0:  # Vertical line
            continue
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        c = p1[1] - m * p1[0]
        
        # Count inliers
        distances = np.abs(m * points[:, 0] - points[:, 1] + c) / np.sqrt(m**2 + 1)
        inliers = distances < threshold
        count = np.sum(inliers)
        
        if count > best_count:
            best_count = count
            best_inliers = inliers
    
    # Refit with all inliers
    inlier_points = points[best_inliers]
    m, c = fit_line_least_squares(inlier_points)
    
    return (m, c), best_inliers
```

---

## 9. Aplikasi: Homography Estimation

### 9.1 Direct Linear Transform (DLT)

Untuk setiap pasangan titik $(x, y) \leftrightarrow (x', y')$:

$$\begin{bmatrix} 
-x & -y & -1 & 0 & 0 & 0 & x'x & x'y & x' \\
0 & 0 & 0 & -x & -y & -1 & y'x & y'y & y'
\end{bmatrix} h = 0$$

Selesaikan dengan SVD untuk h, kemudian reshape ke matriks 3×3.

### 9.2 RANSAC Homography

```python
def estimate_homography_ransac(src_pts, dst_pts, threshold=5, iterations=1000):
    """
    Estimate homography with RANSAC
    
    Parameters:
        src_pts: (N, 2) source points
        dst_pts: (N, 2) destination points
        threshold: inlier threshold
        iterations: max iterations
    
    Returns:
        H: (3, 3) homography matrix
        inliers: boolean mask
    """
    best_H = None
    best_inliers = None
    best_count = 0
    
    N = len(src_pts)
    
    for _ in range(iterations):
        # Sample 4 correspondences
        idx = np.random.choice(N, 4, replace=False)
        
        # Compute homography from 4 points
        H = compute_homography_dlt(src_pts[idx], dst_pts[idx])
        
        # Transform all source points
        src_h = np.column_stack([src_pts, np.ones(N)])
        projected = (H @ src_h.T).T
        projected = projected[:, :2] / projected[:, 2:3]
        
        # Count inliers
        errors = np.linalg.norm(projected - dst_pts, axis=1)
        inliers = errors < threshold
        count = np.sum(inliers)
        
        if count > best_count:
            best_count = count
            best_inliers = inliers
            best_H = H
    
    # Refit with all inliers
    if best_inliers is not None and np.sum(best_inliers) >= 4:
        H = compute_homography_dlt(
            src_pts[best_inliers], 
            dst_pts[best_inliers]
        )
        return H, best_inliers
    
    return best_H, best_inliers
```

---

## 🔑 Konsep Kunci

| Konsep | Deskripsi |
|--------|-----------|
| Model fitting | Menemukan parameter terbaik untuk data |
| Least squares | Minimize sum of squared errors |
| RANSAC | Robust estimation dengan random sampling |
| Hough Transform | Voting dalam parameter space |
| Regularization | Mencegah overfitting |
| Cross-validation | Evaluasi generalization |

---

## 📐 Formula Penting

### Linear Least Squares
$$x = (A^T A)^{-1} A^T b$$

### RANSAC Iterations
$$N = \frac{\log(1-p)}{\log(1-w^n)}$$

### Hough Transform (Line)
$$\rho = x\cos\theta + y\sin\theta$$

### L2 Regularization
$$L_{reg} = L + \lambda ||\theta||_2^2$$

### Gradient Descent
$$\theta_{t+1} = \theta_t - \alpha \nabla L$$

---

## 🎯 Ringkasan

1. **Model fitting** adalah masalah optimisasi untuk menemukan parameter terbaik
2. **Least squares** adalah metode dasar tetapi sensitif terhadap outlier
3. **RANSAC** adalah metode robust yang efektif untuk data dengan outlier
4. **Hough Transform** mengubah detection menjadi voting problem
5. **Regularisasi** mencegah overfitting dengan menambah constraints
6. **Gradient-based optimization** adalah dasar untuk neural networks

---

## 📖 Referensi

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Ed. Bab 4.
2. Hartley, R. & Zisserman, A. (2004). Multiple View Geometry. Bab 3-4.
3. Fischler, M. A. & Bolles, R. C. (1981). Random Sample Consensus.
