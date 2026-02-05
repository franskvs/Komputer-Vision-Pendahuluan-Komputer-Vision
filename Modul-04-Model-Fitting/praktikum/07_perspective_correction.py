# ============================================================
# PROGRAM: 07_perspective_correction.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Program untuk koreksi perspektif dokumen/whiteboard
# 
# Tujuan Pembelajaran:
#   1. Aplikasi praktis homography untuk document scanning
#   2. Deteksi kontur dan corner
#   3. Perspective correction dengan 4-point transform
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

# 1. File gambar
NAMA_FILE_GAMBAR = "document.jpg"

# 2. Mode deteksi
# Opsi: 'auto' (automatic), 'manual' (hardcoded points)
DETECTION_MODE = 'auto'

# 3. Parameter preprocessing
BLUR_KERNEL = 5
CANNY_LOW = 50
CANNY_HIGH = 150

# 4. Parameter contour detection
MIN_AREA_RATIO = 0.1      # Minimum area ratio terhadap image
EPSILON_RATIO = 0.02       # Untuk polygon approximation

# 5. Output size
OUTPUT_WIDTH = 800
OUTPUT_HEIGHT = 1000

# 6. Manual corner points (jika DETECTION_MODE = 'manual')
# Format: [top-left, top-right, bottom-right, bottom-left]
MANUAL_CORNERS = [
    [100, 50],    # Top-left
    [400, 30],    # Top-right
    [420, 350],   # Bottom-right
    [80, 320]     # Bottom-left
]

# 7. Auto-close plot (detik)
AUTO_CLOSE_SECONDS = 2.0

# ============================================================
# FUNGSI HELPER
# ============================================================

def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    lokasi_potensial = [
        os.path.join(direktori_script, "data", "images", nama_file),
        os.path.join(direktori_script, "..", "..", "Bab-01-Pendahuluan", 
                     "data", "images", nama_file),
        os.path.join(direktori_script, nama_file),
    ]
    
    for path in lokasi_potensial:
        if os.path.exists(path):
            return path
    
    return lokasi_potensial[0]


def buat_gambar_sample():
    """Membuat gambar sample dokumen dengan perspektif miring"""
    gambar = np.zeros((500, 600, 3), dtype=np.uint8)
    
    # Background dengan gradient
    for i in range(500):
        for j in range(600):
            gambar[i, j] = [40 + j//10, 40, 40]
    
    # Dokumen miring (trapezoid)
    doc_pts = np.array([[100, 50], [450, 30], [480, 420], [70, 380]])
    cv2.fillPoly(gambar, [doc_pts], (240, 240, 240))
    
    # Border dokumen
    cv2.polylines(gambar, [doc_pts], True, (100, 100, 100), 2)
    
    # Text content (dengan perspektif)
    # cv2.putText(a,b,c,d,e,f,g): a=img, b=teks, c=posisi(x,y), d=font, e=skala, f=warna, g=ketebalan
    cv2.putText(gambar, "DOCUMENT", (150, 120), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (30, 30, 30), 2)
    # cv2.putText(a,b,c,d,e,f,g): a=img, b=teks, c=posisi(x,y), d=font, e=skala, f=warna, g=ketebalan
    cv2.putText(gambar, "SCANNING", (170, 170), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (50, 50, 50), 2)
    
    # Beberapa garis sebagai text
    for i in range(8):
        y1 = 200 + i * 25
        x1 = 120 + i * 3
        x2 = 430 - i * 3
        cv2.line(gambar, (x1, y1), (x2, y1 + 5), (80, 80, 80), 2)
    
    # Marker corners (untuk debugging)
    for pt in doc_pts:
        cv2.circle(gambar, tuple(pt), 5, (0, 255, 0), -1)
    
    return gambar, doc_pts


def tampilkan_plot():
    """Tampilkan plot sebentar lalu tutup otomatis."""
    plt.show(block=False)
    plt.pause(AUTO_CLOSE_SECONDS)
    plt.close()


# ============================================================
# FUNGSI PERSPECTIVE CORRECTION
# ============================================================

def order_points(pts):
    """
    Order points dalam urutan: top-left, top-right, bottom-right, bottom-left
    
    Penting untuk homography agar mapping konsisten.
    """
    rect = np.zeros((4, 2), dtype=np.float32)
    
    # Sum untuk TL (minimum) dan BR (maximum)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left
    rect[2] = pts[np.argmax(s)]  # Bottom-right
    
    # Diff untuk TR (minimum) dan BL (maximum)
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-right
    rect[3] = pts[np.argmax(diff)]  # Bottom-left
    
    return rect


def detect_document_corners(gambar):
    """
    Deteksi corners dokumen secara otomatis
    
    Algoritma:
    1. Convert ke grayscale
    2. Blur untuk noise reduction
    3. Edge detection
    4. Find contours
    5. Approximate polygon dengan 4 vertices
    
    Return:
    - corners: 4 corner points atau None jika gagal
    """
    # Convert ke grayscale
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    # Blur
    blurred = cv2.GaussianBlur(gray, (BLUR_KERNEL, BLUR_KERNEL), 0)
    
    # Edge detection
    edges = cv2.Canny(blurred, CANNY_LOW, CANNY_HIGH)
    
    # Dilate untuk menghubungkan edges
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Sort by area (largest first)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    img_area = gambar.shape[0] * gambar.shape[1]
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Check minimum area
        if area < MIN_AREA_RATIO * img_area:
            continue
        
        # Approximate polygon
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, EPSILON_RATIO * peri, True)
        
        # Check if it's a quadrilateral
        if len(approx) == 4:
            return approx.reshape(4, 2)
    
    return None


def four_point_transform(gambar, pts, output_width=None, output_height=None):
    """
    Perspective transform menggunakan 4 point correspondences
    
    Parameter:
    - gambar: input image
    - pts: 4 corner points
    - output_width/height: desired output size
    
    Return:
    - warped: corrected image
    """
    # Order the points
    rect = order_points(pts)
    tl, tr, br, bl = rect
    
    # Calculate output dimensions
    if output_width is None or output_height is None:
        # Calculate based on max width/height of input quadrilateral
        width_top = np.linalg.norm(tr - tl)
        width_bottom = np.linalg.norm(br - bl)
        output_width = int(max(width_top, width_bottom))
        
        height_left = np.linalg.norm(bl - tl)
        height_right = np.linalg.norm(br - tr)
        output_height = int(max(height_left, height_right))
    
    # Destination points (rectangle)
    dst = np.array([
        [0, 0],
        [output_width - 1, 0],
        [output_width - 1, output_height - 1],
        [0, output_height - 1]
    ], dtype=np.float32)
    
    # Compute homography matrix
    H = cv2.getPerspectiveTransform(rect, dst)
    
    # Warp the image
    warped = cv2.warpPerspective(gambar, H, (output_width, output_height))
    
    return warped, H


def enhance_document(gambar):
    """
    Enhance dokumen hasil scanning
    
    - Increase contrast
    - Convert to grayscale (optional)
    - Thresholding (optional)
    """
    # Convert ke grayscale
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding untuk black-white
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 21, 10
    )
    
    # CLAHE untuk contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    return gray, thresh, enhanced


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_detection_stages():
    """Demonstrasi tahapan deteksi dokumen"""
    print("\n" + "=" * 60)
    print("TAHAPAN DETEKSI DOKUMEN")
    print("=" * 60)
    
    print("""
PIPELINE:

1. Grayscale conversion
2. Gaussian blur (noise reduction)
3. Canny edge detection
4. Find contours
5. Filter by area
6. Polygon approximation
7. Select quadrilateral
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
        doc_pts = None
    else:
        gambar, doc_pts = buat_gambar_sample()
    
    # Step by step
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (BLUR_KERNEL, BLUR_KERNEL), 0)
    edges = cv2.Canny(blurred, CANNY_LOW, CANNY_HIGH)
    
    # Dilate
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw all contours
    img_contours = gambar.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    
    # Find document contour
    corners = detect_document_corners(gambar)
    
    img_corners = gambar.copy()
    if corners is not None:
        cv2.drawContours(img_corners, [corners.astype(int)], -1, (0, 255, 0), 3)
        for i, pt in enumerate(corners):
            cv2.circle(img_corners, tuple(pt.astype(int)), 8, (255, 0, 0), -1)
            # cv2.putText(a,b,c,d,e,f,g): a=img, b=teks, c=posisi(x,y), d=font, e=skala, f=warna, g=ketebalan
            cv2.putText(img_corners, str(i), tuple(pt.astype(int) + [10, 10]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("1. Original Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title("2. Grayscale")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(blurred, cmap='gray')
    axes[0, 2].set_title("3. Blurred")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(edges, cmap='gray')
    axes[1, 0].set_title("4. Canny Edges")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"5. Contours ({len(contours)} found)")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(img_corners, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title("6. Detected Corners")
    axes[1, 2].axis('off')
    
    plt.suptitle("Document Detection Pipeline", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_enhancement():
    """Demonstrasi enhancement dokumen"""
    print("\n" + "=" * 60)
    print("DOCUMENT ENHANCEMENT")
    print("=" * 60)
    
    print("""
ENHANCEMENT OPTIONS:

1. Grayscale: Untuk dokumen text
2. Adaptive Threshold: Black-white (good for OCR)
3. CLAHE: Contrast enhancement
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar, _ = buat_gambar_sample()
    
    # Detect dan correct
    corners = detect_document_corners(gambar)
    
    if corners is not None:
        warped, _ = four_point_transform(gambar, corners, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    else:
        print("   Using manual corners...")
        corners = np.array(MANUAL_CORNERS, dtype=np.float32)
        warped, _ = four_point_transform(gambar, corners, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    # Enhancement
    gray, thresh, enhanced = enhance_document(warped)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    axes[0, 0].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Corrected (Color)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title("Grayscale")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(thresh, cmap='gray')
    axes[1, 0].set_title("Adaptive Threshold\n(Good for OCR)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(enhanced, cmap='gray')
    axes[1, 1].set_title("CLAHE Enhanced")
    axes[1, 1].axis('off')
    
    plt.suptitle("Document Enhancement Options", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


def demo_aspect_ratio():
    """Demonstrasi berbagai aspect ratio output"""
    print("\n" + "=" * 60)
    print("OUTPUT ASPECT RATIOS")
    print("=" * 60)
    
    print("""
COMMON DOCUMENT SIZES:

A4: 210 × 297 mm (aspect ratio 1:1.414)
Letter: 8.5 × 11 inch (aspect ratio 1:1.294)
ID Card: 85.6 × 54 mm (aspect ratio 1.585:1)
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar, _ = buat_gambar_sample()
    
    corners = detect_document_corners(gambar)
    if corners is None:
        corners = np.array(MANUAL_CORNERS, dtype=np.float32)
    
    aspect_ratios = [
        (600, 800, "Auto"),
        (595, 842, "A4 (595×842)"),
        (612, 792, "Letter (612×792)"),
        (324, 204, "ID Card (324×204)")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    for i, (w, h, name) in enumerate(aspect_ratios):
        if name == "Auto":
            warped, _ = four_point_transform(gambar, corners)
        else:
            warped, _ = four_point_transform(gambar, corners, w, h)
        
        axes[i].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"{name}\n{warped.shape[1]}×{warped.shape[0]} pixels")
        axes[i].axis('off')
    
    plt.suptitle("Different Output Aspect Ratios", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: PERSPECTIVE CORRECTION")
    print("Bab 4 - Model Fitting dan Feature Matching")
    print("=" * 60)
    
    print("""
PERSPECTIVE CORRECTION (Document Scanner)

Aplikasi praktis homography untuk mengoreksi perspektif
gambar dokumen yang difoto dari sudut miring.

PIPELINE:
1. Detect document corners (automatic/manual)
2. Order corners (TL, TR, BR, BL)
3. Define destination rectangle
4. Compute homography matrix
5. Warp image
6. (Optional) Enhance for OCR

USE CASES:
├── Mobile document scanner
├── Whiteboard capture
├── Receipt scanning
├── Business card reader
└── Book digitization
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
        doc_pts_true = None
    else:
        print("[INFO] Membuat gambar sample...")
        gambar, doc_pts_true = buat_gambar_sample()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Mode: {DETECTION_MODE}")
    
    # Step 1: Detect corners
    print("\n[STEP 1] Detecting Document Corners...")
    
    if DETECTION_MODE == 'auto':
        corners = detect_document_corners(gambar)
        
        if corners is not None:
            print("   [SUCCESS] Auto detection berhasil!")
            print(f"   Detected corners:")
            for i, pt in enumerate(corners):
                print(f"      {i}: ({pt[0]:.1f}, {pt[1]:.1f})")
        else:
            print("   [WARNING] Auto detection gagal, menggunakan manual corners")
            corners = np.array(MANUAL_CORNERS, dtype=np.float32)
    else:
        print("   Using manual corners...")
        corners = np.array(MANUAL_CORNERS, dtype=np.float32)
    
    # Order corners
    ordered = order_points(corners)
    print(f"\n[STEP 2] Ordered corners (TL, TR, BR, BL):")
    labels = ['Top-Left', 'Top-Right', 'Bottom-Right', 'Bottom-Left']
    for i, (label, pt) in enumerate(zip(labels, ordered)):
        print(f"   {label}: ({pt[0]:.1f}, {pt[1]:.1f})")
    
    # Step 3: Perspective transform
    print(f"\n[STEP 3] Perspective Transform...")
    print(f"   Output size: {OUTPUT_WIDTH} × {OUTPUT_HEIGHT}")
    
    warped, H = four_point_transform(gambar, corners, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    print(f"\n[HOMOGRAPHY MATRIX]")
    print(f"   {H[0,0]:10.4f} {H[0,1]:10.4f} {H[0,2]:10.4f}")
    print(f"   {H[1,0]:10.4f} {H[1,1]:10.4f} {H[1,2]:10.4f}")
    print(f"   {H[2,0]:10.4f} {H[2,1]:10.4f} {H[2,2]:10.4f}")
    
    # Step 4: Enhancement
    print(f"\n[STEP 4] Document Enhancement...")
    gray, thresh, enhanced = enhance_document(warped)
    
    # Visualisasi
    print("\n[STEP 5] Visualisasi...")
    
    # Draw corners on original
    img_corners = gambar.copy()
    cv2.drawContours(img_corners, [corners.astype(int)], -1, (0, 255, 0), 3)
    for i, pt in enumerate(ordered):
        cv2.circle(img_corners, tuple(pt.astype(int)), 8, (255, 0, 0), -1)
        # cv2.putText(a,b,c,d,e,f,g): a=img, b=teks, c=posisi(x,y), d=font, e=skala, f=warna, g=ketebalan
        cv2.putText(img_corners, labels[i][:2], 
                    tuple(pt.astype(int) + [10, -10]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img_corners, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Detected Corners")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f"Corrected ({OUTPUT_WIDTH}×{OUTPUT_HEIGHT})")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(gray, cmap='gray')
    axes[1, 0].set_title("Grayscale")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(thresh, cmap='gray')
    axes[1, 1].set_title("Adaptive Threshold")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(enhanced, cmap='gray')
    axes[1, 2].set_title("CLAHE Enhanced")
    axes[1, 2].axis('off')
    
    plt.suptitle("Perspective Correction (Document Scanner)", fontsize=14)
    plt.tight_layout()
    tampilkan_plot()
    
    # Demo tambahan
    demo_detection_stages()
    demo_enhancement()
    demo_aspect_ratio()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN PERSPECTIVE CORRECTION")
    print("=" * 60)
    print("""
FUNGSI OPENCV:

# Edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

# Polygon approximation
peri = cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

# Perspective transform (4 points)
H = cv2.getPerspectiveTransform(src_pts, dst_pts)
warped = cv2.warpPerspective(img, H, (width, height))

# Enhancement
thresh = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

TIPS:
1. Blur sebelum edge detection untuk mengurangi noise
2. Dilate edges untuk menghubungkan yang terputus
3. Filter contours by area untuk menghindari false detection
4. Order points dengan konsisten (TL, TR, BR, BL)
5. Gunakan adaptive threshold untuk OCR
6. CLAHE bagus untuk contrast enhancement

COMMON ISSUES:
├── No document detected: adjust Canny thresholds
├── Wrong corners: adjust epsilon ratio
├── Warped result blurry: check input resolution
└── Text not readable: try different enhancement
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
