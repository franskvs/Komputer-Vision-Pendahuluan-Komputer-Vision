# TUGAS BAB 2: PEMBENTUKAN CITRA

## 📋 Informasi Tugas

| Aspek | Detail |
|-------|--------|
| **Deadline** | 1 minggu setelah praktikum |
| **Format** | Jupyter Notebook (.ipynb) atau Python (.py) + Laporan PDF |
| **Pengumpulan** | Melalui platform e-learning |

---

## Tugas 1: Teori - Transformasi dan Proyeksi (25 poin)

### Soal 1.1 (10 poin)
Diberikan matriks transformasi 2D:

```
H = ┌ 0.866  -0.5   100 ┐
    │ 0.5    0.866   50 │
    └ 0      0       1  ┘
```

a) Identifikasi jenis transformasi ini (translation/rotation/scaling/affine/projective)
b) Tentukan parameter-parameter transformasi (sudut rotasi, translasi, dll)
c) Hitung koordinat titik P' jika P = (200, 150)
d) Apakah transformasi ini mempertahankan sudut? Jelaskan!

### Soal 1.2 (10 poin)
Sebuah kamera memiliki parameter intrinsik:
- Focal length: fx = 800 pixel, fy = 800 pixel
- Principal point: (cx, cy) = (320, 240)
- Tidak ada distorsi

a) Tuliskan matriks intrinsik K
b) Jika ada titik 3D P = (2, 1, 10) dalam koordinat kamera, hitung proyeksi 2D-nya
c) Berapa field of view horizontal dan vertikal kamera (dalam derajat)?

### Soal 1.3 (5 poin)
Jelaskan perbedaan antara:
a) Distorsi radial vs distorsi tangensial
b) Barrel distortion vs pincushion distortion

Sertakan sketsa ilustrasi untuk masing-masing!

---

## Tugas 2: Coding - Transformasi Geometri (35 poin)

### 2.1 Transformasi Sequence (15 poin)

```python
"""
Implementasikan kelas TransformationManager yang dapat:
1. Menyimpan sequence transformasi
2. Menggabungkan (compose) semua transformasi
3. Menghitung inverse dari sequence transformasi
4. Menerapkan transformasi pada titik dan gambar
"""

class TransformationManager:
    def __init__(self):
        self.transforms = []  # List of (name, matrix) tuples
    
    def add_translation(self, tx, ty):
        """Tambahkan translasi ke sequence"""
        # Implementasi Anda
        pass
    
    def add_rotation(self, angle_degrees, center=(0, 0)):
        """Tambahkan rotasi (dalam derajat) ke sequence"""
        # Implementasi Anda
        pass
    
    def add_scaling(self, sx, sy, center=(0, 0)):
        """Tambahkan scaling ke sequence"""
        # Implementasi Anda
        pass
    
    def add_custom(self, name, matrix):
        """Tambahkan transformasi custom"""
        # Implementasi Anda
        pass
    
    def get_composed_matrix(self):
        """
        Gabungkan semua transformasi menjadi satu matriks
        Urutan: T_n @ T_{n-1} @ ... @ T_1
        """
        # Implementasi Anda
        pass
    
    def get_inverse(self):
        """Hitung inverse dari composed matrix"""
        # Implementasi Anda
        pass
    
    def transform_points(self, points):
        """
        Transformasi array of points (N, 2)
        Return: transformed points (N, 2)
        """
        # Implementasi Anda
        pass
    
    def transform_image(self, image, output_size=None):
        """
        Transformasi gambar menggunakan composed matrix
        """
        # Implementasi Anda
        pass
    
    def visualize_sequence(self, points):
        """
        Visualisasi efek setiap transformasi secara berurutan
        """
        # Implementasi Anda
        pass
    
    def print_summary(self):
        """Print ringkasan semua transformasi"""
        # Implementasi Anda
        pass


# Contoh penggunaan yang harus berfungsi:
if __name__ == "__main__":
    tm = TransformationManager()
    
    # Tambahkan transformasi
    tm.add_translation(100, 50)
    tm.add_rotation(45, center=(320, 240))
    tm.add_scaling(0.8, 0.8, center=(320, 240))
    
    # Print summary
    tm.print_summary()
    
    # Test pada titik
    points = np.array([[100, 100], [200, 100], [150, 200]])
    transformed = tm.transform_points(points)
    print(f"Original: {points}")
    print(f"Transformed: {transformed}")
    
    # Test pada gambar
    # img = cv2.imread('test.jpg')
    # img_transformed = tm.transform_image(img)
```

### 2.2 Homography Estimator (20 poin)

```python
"""
Implementasikan estimasi homography dari titik korespondensi
menggunakan Direct Linear Transform (DLT)
"""

def estimate_homography(src_points, dst_points):
    """
    Estimasi matriks homography H sehingga dst = H @ src
    
    Parameters:
        src_points: numpy array (N, 2) - titik sumber (minimal 4)
        dst_points: numpy array (N, 2) - titik tujuan
    
    Returns:
        H: numpy array (3, 3) - matriks homography
    
    Algoritma DLT:
    1. Untuk setiap pasangan titik (x,y) -> (x',y')
       Buat 2 persamaan linear
    2. Susun menjadi sistem Ah = 0
    3. Selesaikan dengan SVD
    4. Reshape solusi menjadi matriks 3x3
    """
    # Implementasi Anda
    pass


def normalize_points(points):
    """
    Normalisasi titik untuk stabilitas numerik
    
    Returns:
        normalized_points: titik yang dinormalisasi
        T: matriks normalisasi
    """
    # Implementasi Anda
    pass


def estimate_homography_normalized(src_points, dst_points):
    """
    Estimasi homography dengan normalisasi (lebih stabil)
    """
    # Implementasi Anda
    pass


def decompose_homography(H):
    """
    Dekomposisi homography menjadi rotasi, translasi, dan normal plane
    (untuk kasus kamera terkalibrasi)
    """
    # Implementasi Anda (bonus)
    pass


# Test
if __name__ == "__main__":
    # Definisikan titik korespondensi
    src = np.array([
        [0, 0],
        [100, 0],
        [100, 100],
        [0, 100]
    ], dtype=np.float64)
    
    dst = np.array([
        [10, 20],
        [110, 10],
        [120, 100],
        [20, 110]
    ], dtype=np.float64)
    
    # Estimasi homography
    H = estimate_homography(src, dst)
    print(f"Estimated Homography:\n{H}")
    
    # Verifikasi
    H_cv2 = cv2.findHomography(src, dst)[0]
    print(f"\nOpenCV Homography:\n{H_cv2}")
    
    # Hitung error
    src_h = np.hstack([src, np.ones((4, 1))])
    projected = (H @ src_h.T).T
    projected = projected[:, :2] / projected[:, 2:3]
    error = np.sqrt(np.sum((projected - dst)**2, axis=1))
    print(f"\nReprojection errors: {error}")
```

---

## Tugas 3: Mini Project - Virtual Camera (40 poin)

### Deskripsi
Buat aplikasi simulasi kamera virtual yang dapat:
1. Menampilkan objek 3D (kubus atau objek lain)
2. Mengontrol posisi dan orientasi kamera
3. Mengubah parameter intrinsik kamera
4. Menerapkan dan mengoreksi distorsi lensa

### Requirements

```python
"""
Virtual Camera Simulator
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class VirtualCamera:
    def __init__(self, image_size=(640, 480)):
        """
        Initialize virtual camera
        
        Parameters:
            image_size: (width, height)
        """
        self.width, self.height = image_size
        
        # Intrinsic parameters (default)
        self.fx = 500
        self.fy = 500
        self.cx = image_size[0] / 2
        self.cy = image_size[1] / 2
        self.skew = 0
        
        # Distortion coefficients (k1, k2, p1, p2, k3)
        self.dist_coeffs = np.zeros(5)
        
        # Extrinsic parameters
        self.position = np.array([0, 0, 0], dtype=np.float64)  # Camera position in world
        self.rotation = np.eye(3)  # Camera rotation matrix
        
        # Scene objects
        self.objects = []
    
    @property
    def K(self):
        """Camera intrinsic matrix"""
        # Implementasi Anda
        pass
    
    def set_intrinsics(self, fx=None, fy=None, cx=None, cy=None, skew=None):
        """Set camera intrinsic parameters"""
        # Implementasi Anda
        pass
    
    def set_distortion(self, k1=0, k2=0, p1=0, p2=0, k3=0):
        """Set lens distortion coefficients"""
        # Implementasi Anda
        pass
    
    def set_position(self, x, y, z):
        """Set camera position in world coordinates"""
        # Implementasi Anda
        pass
    
    def look_at(self, target, up=np.array([0, 1, 0])):
        """Orient camera to look at target point"""
        # Implementasi Anda
        pass
    
    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        """Rotate camera by Euler angles (in degrees)"""
        # Implementasi Anda
        pass
    
    def move_forward(self, distance):
        """Move camera forward along its view direction"""
        # Implementasi Anda
        pass
    
    def add_object(self, vertices, edges, color='blue'):
        """Add 3D object to scene"""
        # Implementasi Anda
        pass
    
    def add_cube(self, center=(0, 0, 0), size=1, color='blue'):
        """Add cube to scene"""
        # Implementasi Anda
        pass
    
    def add_grid(self, size=10, spacing=1):
        """Add ground grid to scene"""
        # Implementasi Anda
        pass
    
    def project(self, points_3d, apply_distortion=True):
        """
        Project 3D points to 2D image plane
        
        Parameters:
            points_3d: (N, 3) world coordinates
            apply_distortion: whether to apply lens distortion
        
        Returns:
            points_2d: (N, 2) image coordinates
            visible: boolean array indicating which points are visible
        """
        # Implementasi Anda
        pass
    
    def render(self, show_axes=True, show_info=True):
        """
        Render the scene
        
        Returns:
            image: numpy array of rendered image
        """
        # Implementasi Anda
        pass
    
    def visualize_3d(self):
        """Visualize camera and scene in 3D"""
        # Implementasi Anda
        pass
    
    def interactive_demo(self):
        """
        Interactive demo with keyboard controls:
        - W/S: Move forward/backward
        - A/D: Rotate left/right
        - Q/E: Rotate up/down
        - +/-: Zoom in/out (change focal length)
        - 1/2: Increase/decrease distortion
        - R: Reset camera
        - ESC: Exit
        """
        # Implementasi Anda (bonus)
        pass


class SceneObject:
    """Class to represent 3D objects"""
    def __init__(self, vertices, edges, color='blue'):
        self.vertices = np.array(vertices, dtype=np.float64)
        self.edges = edges
        self.color = color


# Demo
if __name__ == "__main__":
    # Create camera
    cam = VirtualCamera(image_size=(800, 600))
    
    # Set camera parameters
    cam.set_intrinsics(fx=600, fy=600)
    cam.set_position(5, 3, 5)
    cam.look_at(np.array([0, 0, 0]))
    
    # Add objects
    cam.add_cube(center=(0, 0, 0), size=2, color='red')
    cam.add_cube(center=(3, 0, 0), size=1, color='blue')
    cam.add_grid(size=10, spacing=1)
    
    # Render
    image = cam.render(show_axes=True, show_info=True)
    
    # Visualize
    plt.figure(figsize=(12, 5))
    
    plt.subplot(121)
    plt.imshow(image)
    plt.title('Camera View')
    plt.axis('off')
    
    plt.subplot(122, projection='3d')
    cam.visualize_3d()
    plt.title('3D Scene')
    
    plt.tight_layout()
    plt.show()
    
    # Interactive demo (bonus)
    # cam.interactive_demo()
```

### Kriteria Penilaian Mini Project

| Kriteria | Poin |
|----------|------|
| Proyeksi 3D ke 2D benar | 10 |
| Kontrol kamera berfungsi | 10 |
| Distorsi lensa berfungsi | 10 |
| Visualisasi baik | 5 |
| Kode rapi dan terdokumentasi | 5 |
| Fitur bonus (interaktif) | +10 |

---

## Rubrik Penilaian Total

| Komponen | Poin |
|----------|------|
| Tugas 1: Teori | 25 |
| Tugas 2: Coding | 35 |
| Tugas 3: Mini Project | 40 |
| **Total** | **100** |
| Bonus | +10 |

---

## Ketentuan Pengumpulan

1. **Nama file**: `Tugas2_NIM_Nama.zip`
2. **Isi ZIP**:
   - `tugas1_teori.pdf` - Jawaban tugas teori
   - `tugas2_coding/` - Folder berisi kode tugas 2
   - `mini_project/` - Folder berisi mini project
   - `README.md` - Penjelasan cara menjalankan kode
3. **Keterlambatan**: -10 poin per hari

---

## Tips

1. Gunakan koordinat homogen untuk semua transformasi
2. Perhatikan urutan perkalian matriks
3. Test dengan kasus sederhana dulu (identitas, rotasi kecil)
4. Verifikasi hasil dengan OpenCV sebagai ground truth
5. Perhatikan konvensi koordinat (y-axis bisa terbalik di image vs world)

---

**Selamat mengerjakan!** 🎉
