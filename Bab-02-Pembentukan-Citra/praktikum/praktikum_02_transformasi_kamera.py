# Praktikum 2: Transformasi Geometri dan Model Kamera

## 🎯 Tujuan Praktikum
1. Mengimplementasikan transformasi geometri 2D
2. Memahami koordinat homogen
3. Mengimplementasikan model kamera pinhole
4. Melakukan kalibrasi kamera sederhana

---

## Bagian 1: Transformasi 2D

### 1.1 Import Library

```python
import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set random seed untuk reprodusibilitas
np.random.seed(42)
```

### 1.2 Fungsi Transformasi Dasar

```python
def translation_matrix(tx, ty):
    """Matriks translasi 2D (3x3 homogen)"""
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=np.float32)

def rotation_matrix(theta):
    """Matriks rotasi 2D (3x3 homogen)
    theta dalam radian
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=np.float32)

def scaling_matrix(sx, sy):
    """Matriks scaling 2D (3x3 homogen)"""
    return np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=np.float32)

def shear_matrix(shx, shy):
    """Matriks shear 2D (3x3 homogen)"""
    return np.array([
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ], dtype=np.float32)
```

### 1.3 Transformasi Titik

```python
def transform_points(points, T):
    """
    Transformasi sekumpulan titik dengan matriks T
    
    Parameters:
        points: numpy array (N, 2) - koordinat titik
        T: numpy array (3, 3) - matriks transformasi homogen
    
    Returns:
        numpy array (N, 2) - titik hasil transformasi
    """
    # Konversi ke homogen
    N = points.shape[0]
    points_h = np.hstack([points, np.ones((N, 1))])
    
    # Transformasi
    transformed = (T @ points_h.T).T
    
    # Konversi kembali ke kartesian
    return transformed[:, :2] / transformed[:, 2:3]

# Contoh: Buat segitiga
triangle = np.array([
    [0, 0],
    [1, 0],
    [0.5, 1]
], dtype=np.float32)

# Terapkan berbagai transformasi
T_translate = translation_matrix(2, 1)
T_rotate = rotation_matrix(np.pi/4)  # 45 derajat
T_scale = scaling_matrix(1.5, 1.5)

triangle_translated = transform_points(triangle, T_translate)
triangle_rotated = transform_points(triangle, T_rotate)
triangle_scaled = transform_points(triangle, T_scale)

# Komposisi transformasi
T_combined = T_translate @ T_rotate @ T_scale
triangle_combined = transform_points(triangle, T_combined)

# Visualisasi
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

def plot_triangle(ax, tri, title, color='blue'):
    tri_closed = np.vstack([tri, tri[0]])
    ax.plot(tri_closed[:, 0], tri_closed[:, 1], 'o-', color=color)
    ax.fill(tri[:, 0], tri[:, 1], alpha=0.3, color=color)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

plot_triangle(axes[0], triangle, 'Original', 'blue')
plot_triangle(axes[0], triangle_translated, 'Translated', 'red')

plot_triangle(axes[1], triangle, 'Original', 'blue')
plot_triangle(axes[1], triangle_rotated, 'Rotated 45°', 'green')

plot_triangle(axes[2], triangle, 'Original', 'blue')
plot_triangle(axes[2], triangle_scaled, 'Scaled 1.5x', 'orange')

plot_triangle(axes[3], triangle, 'Original', 'blue')
plot_triangle(axes[3], triangle_combined, 'Combined', 'purple')

plt.tight_layout()
plt.show()
```

### 1.4 Transformasi Citra dengan OpenCV

```python
from skimage import data

# Load sample image
img = data.astronaut()
h, w = img.shape[:2]

# Definisikan transformasi
angle = 30  # derajat
scale = 0.8
tx, ty = 50, 30

# Rotasi menggunakan OpenCV
center = (w // 2, h // 2)
M_rotate = cv2.getRotationMatrix2D(center, angle, scale)
img_rotated = cv2.warpAffine(img, M_rotate, (w, h))

# Translasi
M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
img_translated = cv2.warpAffine(img, M_translate, (w, h))

# Affine transformation
# Definisikan 3 pasang titik
pts_src = np.float32([[50, 50], [200, 50], [50, 200]])
pts_dst = np.float32([[10, 100], [200, 50], [100, 250]])
M_affine = cv2.getAffineTransform(pts_src, pts_dst)
img_affine = cv2.warpAffine(img, M_affine, (w, h))

# Perspective transformation
# Definisikan 4 pasang titik
pts_src_persp = np.float32([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]])
pts_dst_persp = np.float32([[50, 50], [w-100, 20], [20, h-50], [w-50, h-20]])
M_persp = cv2.getPerspectiveTransform(pts_src_persp, pts_dst_persp)
img_perspective = cv2.warpPerspective(img, M_persp, (w, h))

# Visualisasi
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].imshow(img)
axes[0, 0].set_title('Original')

axes[0, 1].imshow(img_rotated)
axes[0, 1].set_title(f'Rotated {angle}°, Scale {scale}')

axes[0, 2].imshow(img_translated)
axes[0, 2].set_title(f'Translated ({tx}, {ty})')

axes[1, 0].imshow(img)
axes[1, 0].set_title('Original')

axes[1, 1].imshow(img_affine)
axes[1, 1].set_title('Affine Transform')

axes[1, 2].imshow(img_perspective)
axes[1, 2].set_title('Perspective Transform')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## Bagian 2: Model Kamera Pinhole

### 2.1 Proyeksi 3D ke 2D

```python
def create_camera_matrix(fx, fy, cx, cy, skew=0):
    """
    Membuat matriks intrinsik kamera K
    """
    K = np.array([
        [fx, skew, cx],
        [0,  fy,   cy],
        [0,  0,    1]
    ], dtype=np.float64)
    return K

def project_points(points_3d, K, R, t):
    """
    Proyeksi titik 3D ke 2D menggunakan model pinhole
    
    Parameters:
        points_3d: (N, 3) - titik dalam koordinat world
        K: (3, 3) - matriks intrinsik
        R: (3, 3) - matriks rotasi
        t: (3, 1) - vektor translasi
    
    Returns:
        points_2d: (N, 2) - titik pada image plane
    """
    N = points_3d.shape[0]
    
    # Bentuk matriks [R|t]
    Rt = np.hstack([R, t])
    
    # Matriks proyeksi
    P = K @ Rt
    
    # Konversi ke homogen
    points_h = np.hstack([points_3d, np.ones((N, 1))])
    
    # Proyeksi
    projected = (P @ points_h.T).T
    
    # Normalisasi
    points_2d = projected[:, :2] / projected[:, 2:3]
    
    return points_2d

# Contoh: Proyeksi kubus 3D
# Definisikan vertices kubus
cube_vertices = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Bottom face
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # Top face
], dtype=np.float64)

# Edges kubus
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom
    (4, 5), (5, 6), (6, 7), (7, 4),  # Top
    (0, 4), (1, 5), (2, 6), (3, 7)   # Sides
]

# Parameter kamera
fx, fy = 500, 500
cx, cy = 320, 240
K = create_camera_matrix(fx, fy, cx, cy)

# Posisi kamera (rotasi dan translasi)
# Kamera melihat ke arah kubus
angle_x = np.radians(20)
angle_y = np.radians(30)
Rx = np.array([
    [1, 0, 0],
    [0, np.cos(angle_x), -np.sin(angle_x)],
    [0, np.sin(angle_x), np.cos(angle_x)]
])
Ry = np.array([
    [np.cos(angle_y), 0, np.sin(angle_y)],
    [0, 1, 0],
    [-np.sin(angle_y), 0, np.cos(angle_y)]
])
R = Ry @ Rx
t = np.array([[0], [0], [5]])  # Kamera di depan kubus

# Proyeksi
cube_2d = project_points(cube_vertices, K, R, t)

# Visualisasi
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 3D view
ax3d = fig.add_subplot(121, projection='3d')
for e in edges:
    ax3d.plot3D(*zip(cube_vertices[e[0]], cube_vertices[e[1]]), 'b-')
ax3d.scatter3D(*cube_vertices.T, c='red', s=50)
ax3d.set_xlabel('X')
ax3d.set_ylabel('Y')
ax3d.set_zlabel('Z')
ax3d.set_title('3D Cube')

# 2D projection
axes[1].set_xlim(0, 640)
axes[1].set_ylim(480, 0)  # Flip y-axis
for e in edges:
    axes[1].plot(*zip(cube_2d[e[0]], cube_2d[e[1]]), 'b-')
axes[1].scatter(*cube_2d.T, c='red', s=50)
axes[1].set_xlabel('u (pixels)')
axes[1].set_ylabel('v (pixels)')
axes[1].set_title('2D Projection')
axes[1].set_aspect('equal')
axes[1].grid(True)

plt.tight_layout()
plt.show()
```

### 2.2 Efek Parameter Kamera

```python
def visualize_camera_parameters():
    """
    Visualisasi efek perubahan parameter kamera
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Kubus untuk diproyeksikan
    R = np.eye(3)
    t = np.array([[0], [0], [5]])
    
    # Parameter default
    default_fx, default_fy = 500, 500
    default_cx, default_cy = 320, 240
    
    # Variasi focal length
    focal_lengths = [200, 500, 1000]
    for i, fl in enumerate(focal_lengths):
        K = create_camera_matrix(fl, fl, default_cx, default_cy)
        cube_2d = project_points(cube_vertices, K, R, t)
        
        ax = axes[0, i]
        for e in edges:
            ax.plot(*zip(cube_2d[e[0]], cube_2d[e[1]]), 'b-')
        ax.set_xlim(0, 640)
        ax.set_ylim(480, 0)
        ax.set_title(f'Focal Length = {fl}')
        ax.set_aspect('equal')
        ax.grid(True)
    
    # Variasi principal point
    principal_points = [(160, 120), (320, 240), (480, 360)]
    for i, (cx, cy) in enumerate(principal_points):
        K = create_camera_matrix(default_fx, default_fy, cx, cy)
        cube_2d = project_points(cube_vertices, K, R, t)
        
        ax = axes[1, i]
        for e in edges:
            ax.plot(*zip(cube_2d[e[0]], cube_2d[e[1]]), 'b-')
        ax.plot(cx, cy, 'r+', markersize=15, markeredgewidth=3)  # Principal point
        ax.set_xlim(0, 640)
        ax.set_ylim(480, 0)
        ax.set_title(f'Principal Point = ({cx}, {cy})')
        ax.set_aspect('equal')
        ax.grid(True)
    
    plt.suptitle('Effect of Camera Parameters', fontsize=14)
    plt.tight_layout()
    plt.show()

visualize_camera_parameters()
```

---

## Bagian 3: Distorsi Lensa

### 3.1 Simulasi Distorsi Radial

```python
def apply_radial_distortion(points, k1, k2=0, k3=0, center=(0, 0)):
    """
    Terapkan distorsi radial pada titik
    
    x_d = x(1 + k1*r² + k2*r⁴ + k3*r⁶)
    y_d = y(1 + k1*r² + k2*r⁴ + k3*r⁶)
    """
    x = points[:, 0] - center[0]
    y = points[:, 1] - center[1]
    
    r2 = x**2 + y**2
    r4 = r2**2
    r6 = r2**3
    
    factor = 1 + k1*r2 + k2*r4 + k3*r6
    
    x_distorted = x * factor + center[0]
    y_distorted = y * factor + center[1]
    
    return np.column_stack([x_distorted, y_distorted])

def visualize_distortion():
    """
    Visualisasi efek distorsi radial
    """
    # Buat grid titik
    x = np.linspace(-1, 1, 20)
    y = np.linspace(-1, 1, 20)
    xx, yy = np.meshgrid(x, y)
    points = np.column_stack([xx.ravel(), yy.ravel()])
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original
    axes[0].scatter(points[:, 0], points[:, 1], s=10)
    axes[0].set_title('Original Grid')
    axes[0].set_aspect('equal')
    axes[0].grid(True)
    
    # Barrel distortion (k1 < 0)
    distorted_barrel = apply_radial_distortion(points, k1=-0.3)
    axes[1].scatter(distorted_barrel[:, 0], distorted_barrel[:, 1], s=10, c='red')
    axes[1].set_title('Barrel Distortion (k1 = -0.3)')
    axes[1].set_aspect('equal')
    axes[1].grid(True)
    
    # Pincushion distortion (k1 > 0)
    distorted_pincushion = apply_radial_distortion(points, k1=0.3)
    axes[2].scatter(distorted_pincushion[:, 0], distorted_pincushion[:, 1], s=10, c='green')
    axes[2].set_title('Pincushion Distortion (k1 = 0.3)')
    axes[2].set_aspect('equal')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()

visualize_distortion()
```

### 3.2 Undistortion dengan OpenCV

```python
def demonstrate_undistortion():
    """
    Demonstrasi koreksi distorsi menggunakan OpenCV
    """
    # Simulasi citra terdistorsi dengan membuat checker pattern
    rows, cols = 8, 12
    square_size = 50
    pattern = np.zeros(((rows+1)*square_size, (cols+1)*square_size), dtype=np.uint8)
    
    for i in range(rows+1):
        for j in range(cols+1):
            if (i + j) % 2 == 0:
                y1, y2 = i*square_size, (i+1)*square_size
                x1, x2 = j*square_size, (j+1)*square_size
                pattern[y1:y2, x1:x2] = 255
    
    h, w = pattern.shape
    
    # Parameter kamera (simulasi)
    K = np.array([
        [w/2, 0, w/2],
        [0, h/2, h/2],
        [0, 0, 1]
    ], dtype=np.float64)
    
    # Koefisien distorsi (simulasi barrel distortion)
    dist_coeffs = np.array([-0.3, 0.1, 0, 0, 0], dtype=np.float64)
    
    # Terapkan distorsi
    map_x, map_y = cv2.initUndistortRectifyMap(K, dist_coeffs, None, K, (w, h), cv2.CV_32FC1)
    
    # Untuk simulasi, kita perlu inverse mapping
    # Gunakan cv2.undistort untuk koreksi
    distorted = cv2.remap(pattern, map_x, map_y, cv2.INTER_LINEAR)
    
    # Koreksi distorsi
    undistorted = cv2.undistort(distorted, K, dist_coeffs)
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(pattern, cmap='gray')
    axes[0].set_title('Original Pattern')
    
    axes[1].imshow(distorted, cmap='gray')
    axes[1].set_title('Distorted')
    
    axes[2].imshow(undistorted, cmap='gray')
    axes[2].set_title('Undistorted (Corrected)')
    
    for ax in axes:
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

demonstrate_undistortion()
```

---

## Bagian 4: Kalibrasi Kamera (Sederhana)

### 4.1 Menggunakan Checkerboard Pattern

```python
def simple_camera_calibration():
    """
    Demonstrasi kalibrasi kamera menggunakan checkerboard
    (Dalam praktik nyata, Anda memerlukan multiple images)
    """
    # Parameter checkerboard
    CHECKERBOARD = (7, 5)  # Inner corners
    
    # Kriteria terminasi
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Siapkan titik objek 3D
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    
    # List untuk menyimpan titik objek dan titik gambar
    objpoints = []  # 3D points in world coordinate
    imgpoints = []  # 2D points in image plane
    
    print("Untuk kalibrasi kamera yang sebenarnya:")
    print("1. Cetak checkerboard pattern")
    print("2. Ambil 10-20 foto dari berbagai sudut")
    print("3. Deteksi corners di setiap foto")
    print("4. Jalankan cv2.calibrateCamera()")
    
    # Contoh output kalibrasi (nilai dummy untuk demonstrasi)
    sample_K = np.array([
        [800, 0, 320],
        [0, 800, 240],
        [0, 0, 1]
    ], dtype=np.float64)
    
    sample_dist = np.array([0.1, -0.25, 0, 0, 0], dtype=np.float64)
    
    print("\nContoh hasil kalibrasi:")
    print(f"Camera Matrix K:\n{sample_K}")
    print(f"\nDistortion Coefficients:\n{sample_dist}")
    print(f"\nFocal length: fx={sample_K[0,0]:.1f}, fy={sample_K[1,1]:.1f}")
    print(f"Principal point: ({sample_K[0,2]:.1f}, {sample_K[1,2]:.1f})")

simple_camera_calibration()
```

---

## 📝 Latihan Praktikum

### Latihan 1: Transformasi Komposit
Implementasikan fungsi yang menggabungkan:
- Rotasi sebesar θ di sekitar titik (cx, cy)
- Scaling sebesar s di sekitar titik yang sama
- Translasi sebesar (tx, ty)

### Latihan 2: Homography Estimation
Implementasikan estimasi matriks homography dari 4 pasang titik korespondensi menggunakan DLT (Direct Linear Transform).

### Latihan 3: Virtual Camera
Buat program yang mensimulasikan kamera virtual yang dapat:
- Bergerak maju/mundur (mengubah jarak)
- Berputar sekitar sumbu Y
- Mengubah focal length (zoom)

### Latihan 4: Panorama Sederhana
Gunakan homography untuk menggabungkan 2 gambar menjadi panorama sederhana.

---

## 📚 Referensi Praktikum

1. OpenCV Camera Calibration Tutorial: https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html
2. Hartley & Zisserman, Chapter 2-4
3. Multiple View Geometry Tutorials: http://www.robots.ox.ac.uk/~vgg/hzbook/
