# ============================================================
# PROGRAM: 06_document_scanner.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: Program document scanner lengkap dengan deteksi
#            otomatis sudut dokumen menggunakan edge detection
# 
# Tujuan Pembelajaran:
#   1. Mengintegrasikan berbagai teknik CV untuk aplikasi nyata
#   2. Deteksi kontur dan seleksi kontur 4 sisi
#   3. Koreksi perspektif otomatis
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "sample.jpg"

# 2. Ukuran resize untuk pemrosesan (lebih kecil = lebih cepat)
RESIZE_WIDTH = 500

# 3. Parameter Canny edge detection
CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 200

# 4. Parameter Gaussian blur
BLUR_KERNEL_SIZE = 5

# 5. Ukuran output dokumen (inch × DPI)
# Contoh: A4 = 8.27" x 11.69" pada 100 DPI
OUTPUT_WIDTH = 827
OUTPUT_HEIGHT = 1169

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(direktori_script, "..", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, "..", "..", 
                                  "Bab-01-Pendahuluan", "data", "images", nama_file)
    
    if not os.path.exists(path_data):
        path_data = os.path.join(direktori_script, nama_file)
    
    return path_data


def buat_gambar_dokumen():
    """
    Membuat gambar simulasi dokumen dengan background
    untuk demonstrasi document scanner
    """
    # Background meja kayu
    gambar = np.zeros((700, 900, 3), dtype=np.uint8)
    
    # Tekstur meja
    for i in range(700):
        for j in range(900):
            noise = np.random.randint(-10, 10)
            gambar[i, j] = [80 + noise, 60 + noise, 45 + noise]
    
    # Blur untuk tekstur natural
    gambar = cv2.GaussianBlur(gambar, (5, 5), 0)
    
    # Dokumen putih dengan perspektif
    # Titik-titik sudut dokumen (dalam perspektif)
    pts_dokumen = np.array([
        [180, 80],    # top-left
        [700, 120],   # top-right
        [750, 580],   # bottom-right
        [130, 620]    # bottom-left
    ], np.int32)
    
    # Isi dokumen dengan warna putih
    cv2.fillPoly(gambar, [pts_dokumen], (250, 250, 250))
    
    # Bayangan dokumen
    shadow_pts = pts_dokumen + np.array([[10, 10]])
    mask = np.zeros_like(gambar)
    cv2.fillPoly(mask, [shadow_pts.astype(np.int32)], (50, 50, 50))
    gambar = cv2.addWeighted(gambar, 1, mask, 0.3, 0)
    
    # Konten dalam dokumen (simulasi teks)
    # Kita perlu menghitung posisi teks yang mengikuti perspektif
    
    # Header
    header_y = 150
    cv2.putText(gambar, "SURAT KETERANGAN", (280, header_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (30, 30, 30), 2)
    
    # Garis teks
    for i in range(8):
        y_pos = 220 + i * 45
        x_start = 200 + int((y_pos - 80) * 0.05)  # Menyesuaikan perspektif
        x_end = 680 + int((y_pos - 80) * 0.1)
        line_length = np.random.randint(int((x_end - x_start) * 0.6), 
                                        int((x_end - x_start) * 0.95))
        cv2.line(gambar, (x_start, y_pos), (x_start + line_length, y_pos), 
                (100, 100, 100), 2)
    
    # Tanda tangan area
    cv2.rectangle(gambar, (500, 500), (700, 570), (150, 150, 150), 2)
    cv2.putText(gambar, "TTD", (570, 545), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    
    return gambar, pts_dokumen.astype(np.float32)


# ============================================================
# FUNGSI DOCUMENT SCANNER
# ============================================================

def order_points(pts):
    """
    Mengurutkan 4 titik dalam urutan konsisten:
    top-left, top-right, bottom-right, bottom-left
    """
    rect = np.zeros((4, 2), dtype=np.float32)
    
    # Top-left: koordinat dengan sum minimum
    # Bottom-right: koordinat dengan sum maksimum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Top-right: koordinat dengan diff minimum (y - x kecil)
    # Bottom-left: koordinat dengan diff maksimum (y - x besar)
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect


def deteksi_dokumen(gambar, show_steps=True):
    """
    Mendeteksi sudut dokumen dalam gambar
    
    Parameter:
    - gambar: input image (BGR)
    - show_steps: apakah menampilkan langkah-langkah
    
    Return:
    - corners: 4 titik sudut dokumen, atau None jika tidak ditemukan
    """
    # Simpan original untuk skala
    tinggi_orig, lebar_orig = gambar.shape[:2]
    
    # Resize untuk pemrosesan lebih cepat
    rasio = RESIZE_WIDTH / lebar_orig
    gambar_kecil = cv2.resize(gambar, (RESIZE_WIDTH, int(tinggi_orig * rasio)))
    
    # Step 1: Konversi ke grayscale
    gray = cv2.cvtColor(gambar_kecil, cv2.COLOR_BGR2GRAY)
    
    # Step 2: Blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)
    
    # Step 3: Edge detection
    edges = cv2.Canny(blurred, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
    
    # Step 4: Dilasi untuk menghubungkan edge yang terputus
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Step 5: Temukan kontur
    contours, _ = cv2.findContours(edges_dilated, cv2.RETR_LIST, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    # Step 6: Urutkan kontur berdasarkan area (terbesar dulu)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    # Step 7: Cari kontur dengan 4 titik (dokumen)
    doc_contour = None
    for contour in contours:
        # Aproksimasi kontur
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        
        # Jika kontur memiliki 4 titik, kemungkinan itu dokumen
        if len(approx) == 4:
            doc_contour = approx
            break
    
    # Tampilkan langkah-langkah jika diminta
    if show_steps:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        axes[0, 0].imshow(cv2.cvtColor(gambar_kecil, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title("1. Original (Resized)")
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(gray, cmap='gray')
        axes[0, 1].set_title("2. Grayscale")
        axes[0, 1].axis('off')
        
        axes[0, 2].imshow(blurred, cmap='gray')
        axes[0, 2].set_title("3. Gaussian Blur")
        axes[0, 2].axis('off')
        
        axes[1, 0].imshow(edges, cmap='gray')
        axes[1, 0].set_title("4. Canny Edges")
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(edges_dilated, cmap='gray')
        axes[1, 1].set_title("5. Dilated Edges")
        axes[1, 1].axis('off')
        
        # Tampilkan kontur yang ditemukan
        gambar_kontur = gambar_kecil.copy()
        if doc_contour is not None:
            cv2.drawContours(gambar_kontur, [doc_contour], -1, (0, 255, 0), 3)
            for pt in doc_contour.reshape(-1, 2):
                cv2.circle(gambar_kontur, tuple(pt), 8, (0, 0, 255), -1)
        
        axes[1, 2].imshow(cv2.cvtColor(gambar_kontur, cv2.COLOR_BGR2RGB))
        axes[1, 2].set_title("6. Detected Document")
        axes[1, 2].axis('off')
        
        plt.suptitle("Langkah-langkah Deteksi Dokumen", fontsize=14)
        plt.tight_layout()
        plt.show()
    
    # Return corners scaled back ke ukuran original
    if doc_contour is not None:
        corners = doc_contour.reshape(4, 2) / rasio
        return corners.astype(np.float32)
    
    return None


def koreksi_perspektif(gambar, corners, output_size=None):
    """
    Melakukan koreksi perspektif pada dokumen
    
    Parameter:
    - gambar: input image
    - corners: 4 titik sudut dokumen
    - output_size: tuple (width, height) atau None untuk auto
    
    Return:
    - gambar hasil koreksi
    """
    # Urutkan titik
    rect = order_points(corners)
    (tl, tr, br, bl) = rect
    
    # Hitung dimensi output
    if output_size is None:
        # Gunakan jarak terbesar sebagai dimensi
        lebar_top = np.linalg.norm(tr - tl)
        lebar_bottom = np.linalg.norm(br - bl)
        lebar = int(max(lebar_top, lebar_bottom))
        
        tinggi_left = np.linalg.norm(bl - tl)
        tinggi_right = np.linalg.norm(br - tr)
        tinggi = int(max(tinggi_left, tinggi_right))
    else:
        lebar, tinggi = output_size
    
    # Titik tujuan
    dst = np.array([
        [0, 0],
        [lebar - 1, 0],
        [lebar - 1, tinggi - 1],
        [0, tinggi - 1]
    ], dtype=np.float32)
    
    # Hitung transformation matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    
    # Terapkan transformasi
    hasil = cv2.warpPerspective(gambar, M, (lebar, tinggi))
    
    return hasil


def enhance_dokumen(gambar):
    """
    Meningkatkan kualitas hasil scan
    
    Parameter:
    - gambar: hasil scan (BGR)
    
    Return:
    - gambar yang sudah di-enhance
    """
    # Konversi ke grayscale
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding untuk hasil seperti scan
    # Metode 1: Adaptive threshold
    thresh_adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Metode 2: CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_clahe = clahe.apply(gray)
    
    # Metode 3: Sharpening
    kernel_sharp = np.array([[-1, -1, -1],
                             [-1,  9, -1],
                             [-1, -1, -1]])
    sharpened = cv2.filter2D(gray, -1, kernel_sharp)
    
    return gray, thresh_adaptive, enhanced_clahe, sharpened


def scan_dokumen_lengkap(gambar, output_size=None):
    """
    Pipeline lengkap document scanner
    
    Parameter:
    - gambar: input image (BGR)
    - output_size: ukuran output (width, height) atau None
    
    Return:
    - hasil scan
    - corners yang terdeteksi
    """
    print("\n" + "=" * 60)
    print("DOCUMENT SCANNER - PIPELINE LENGKAP")
    print("=" * 60)
    
    # Step 1: Deteksi dokumen
    print("[Step 1] Mendeteksi sudut dokumen...")
    corners = deteksi_dokumen(gambar, show_steps=True)
    
    if corners is None:
        print("[ERROR] Tidak dapat mendeteksi dokumen!")
        return None, None
    
    print(f"[INFO] Sudut terdeteksi: {corners.tolist()}")
    
    # Step 2: Koreksi perspektif
    print("\n[Step 2] Melakukan koreksi perspektif...")
    if output_size is None:
        output_size = (OUTPUT_WIDTH, OUTPUT_HEIGHT)
    scanned = koreksi_perspektif(gambar, corners, output_size)
    print(f"[INFO] Ukuran output: {scanned.shape}")
    
    # Step 3: Enhancement
    print("\n[Step 3] Meningkatkan kualitas hasil scan...")
    gray, thresh, clahe, sharp = enhance_dokumen(scanned)
    
    # Tampilkan hasil enhancement
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(scanned, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Perspective Corrected")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(gray, cmap='gray')
    axes[0, 2].set_title("Grayscale")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(thresh, cmap='gray')
    axes[1, 0].set_title("Adaptive Threshold\n(seperti hasil scan)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(clahe, cmap='gray')
    axes[1, 1].set_title("CLAHE Enhanced")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(sharp, cmap='gray')
    axes[1, 2].set_title("Sharpened")
    axes[1, 2].axis('off')
    
    plt.suptitle("Document Scanner - Hasil Enhancement", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    return scanned, corners


def demo_manual_selection():
    """
    Demonstrasi pemilihan titik manual dengan GUI interaktif
    """
    print("\n" + "=" * 60)
    print("DEMO PEMILIHAN TITIK MANUAL")
    print("=" * 60)
    
    print("""
Dalam aplikasi nyata, sering diperlukan pemilihan titik manual
ketika deteksi otomatis gagal.

Berikut contoh implementasi dengan mouse callback:
    """)
    
    code_example = '''
# Contoh implementasi pemilihan titik dengan mouse
points = []

def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")

# Setup window
cv2.namedWindow("Select 4 Corners")
cv2.setMouseCallback("Select 4 Corners", mouse_callback)

while len(points) < 4:
    temp_img = gambar.copy()
    for pt in points:
        cv2.circle(temp_img, pt, 5, (0, 255, 0), -1)
    cv2.imshow("Select 4 Corners", temp_img)
    if cv2.waitKey(1) == 27:  # ESC
        break

cv2.destroyAllWindows()
'''
    print(code_example)


def demo_batch_processing():
    """
    Demonstrasi pemrosesan batch dokumen
    """
    print("\n" + "=" * 60)
    print("DEMO BATCH PROCESSING")
    print("=" * 60)
    
    print("""
Untuk memproses banyak dokumen sekaligus:

def process_batch(input_folder, output_folder):
    import glob
    
    images = glob.glob(os.path.join(input_folder, "*.jpg"))
    
    for i, img_path in enumerate(images):
        print(f"Processing {i+1}/{len(images)}: {img_path}")
        
        # Baca gambar
        img = cv2.imread(img_path)
        
        # Deteksi dan koreksi
        corners = deteksi_dokumen(img, show_steps=False)
        if corners is not None:
            scanned = koreksi_perspektif(img, corners)
            
            # Simpan hasil
            filename = os.path.basename(img_path)
            output_path = os.path.join(output_folder, f"scanned_{filename}")
            cv2.imwrite(output_path, scanned)
            print(f"  Saved: {output_path}")
        else:
            print(f"  Warning: Could not detect document")
    """)


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: DOCUMENT SCANNER")
    print("Bab 2 - Pembentukan Citra")
    print("=" * 60)
    
    print("""
DOCUMENT SCANNER menggabungkan beberapa teknik:
├── Edge Detection (Canny)
├── Contour Detection
├── Polygon Approximation
├── Perspective Transform
└── Image Enhancement

Pipeline:
  Input → Grayscale → Blur → Edge → Contours → 
  4-Point Detection → Perspective Correction → Enhancement → Output
    """)
    
    # Buat atau muat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Membuat gambar simulasi dokumen...")
        gambar, pts_true = buat_gambar_dokumen()
        print(f"[INFO] Ground truth corners: {pts_true.tolist()}")
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    
    # Tampilkan gambar asli
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    plt.title("Input Image")
    plt.axis('off')
    plt.show()
    
    # Jalankan document scanner
    hasil, corners = scan_dokumen_lengkap(gambar)
    
    if hasil is not None:
        # Demo pemilihan manual
        demo_manual_selection()
        
        # Demo batch processing
        demo_batch_processing()
        
        # Simpan hasil
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "hasil_scan.jpg")
        cv2.imwrite(output_path, hasil)
        print(f"\n[INFO] Hasil disimpan: {output_path}")
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN DOCUMENT SCANNER")
    print("=" * 60)
    print("""
FUNGSI-FUNGSI YANG DIGUNAKAN:
├── cv2.Canny(img, t1, t2)           : Edge detection
├── cv2.findContours(...)            : Menemukan kontur
├── cv2.approxPolyDP(contour, eps)   : Aproksimasi polygon
├── cv2.getPerspectiveTransform(...) : Hitung matrix
├── cv2.warpPerspective(...)         : Terapkan transformasi
├── cv2.adaptiveThreshold(...)       : Enhancement
└── cv2.createCLAHE(...)             : Contrast enhancement

PARAMETER PENTING:
├── Canny thresholds: mengontrol sensitivitas edge
├── approxPolyDP epsilon: toleransi aproksimasi (0.02 * perimeter)
├── Gaussian blur kernel: mengurangi noise

TIPS DETEKSI YANG BAIK:
├── Background kontras dengan dokumen
├── Pencahayaan merata tanpa bayangan
├── Dokumen tidak terlalu miring
└── Edge dokumen terlihat jelas

APLIKASI NYATA:
├── CamScanner, Adobe Scan
├── Sistem OCR preprocessing
├── Digitalisasi arsip
└── KTP/SIM scanner
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
