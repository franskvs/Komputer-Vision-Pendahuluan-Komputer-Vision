"""
=============================================================================
PRAKTIKUM BONUS: APLIKASI REAL-WORLD - DOCUMENT SCANNER
=============================================================================
Deskripsi:
    Program ini mendemonstrasikan aplikasi nyata dari feature detection
    dan homography untuk membuat Document Scanner sederhana. Program akan:
    1. Mendeteksi dokumen dalam gambar
    2. Menemukan sudut-sudut dokumen
    3. Melakukan perspective transform untuk "flatten" dokumen
    
Konsep yang Digunakan:
    - Corner detection untuk menemukan sudut dokumen
    - Contour detection untuk menemukan boundary dokumen
    - Homography untuk perspective correction
    
Aplikasi Dunia Nyata:
    - Mobile document scanner apps (CamScanner, Adobe Scan)
    - Receipt scanning untuk expense tracking
    - ID card/passport scanning
    - Whiteboard capture untuk meeting notes

=============================================================================
"""

import cv2
import numpy as np
import os
import time

def get_script_dir():
    """Get script directory"""
    return os.path.dirname(os.path.abspath(__file__))

def order_points(pts):
    """
    Mengurutkan 4 titik corner dalam urutan: top-left, top-right, bottom-right, bottom-left
    """
    # Inisialisasi array untuk koordinat terurut
    rect = np.zeros((4, 2), dtype="float32")
    
    # Top-left memiliki sum terkecil, bottom-right memiliki sum terbesar
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Top-right memiliki diff terkecil, bottom-left memiliki diff terbesar
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

def four_point_transform(image, pts):
    """
    Melakukan perspective transform dengan 4 titik
    """
    # Urutkan points
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Hitung lebar maksimum
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    # Hitung tinggi maksimum
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Koordinat destinasi
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # Hitung perspective transform matrix dan apply
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

def find_document(image):
    """
    Menemukan dokumen dalam gambar menggunakan contour detection
    """
    # Konversi ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection
    edged = cv2.Canny(blurred, 75, 200)
    
    # Dilate untuk menutup gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(edged, kernel, iterations=2)
    
    # Temukan contours
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    # Loop contours untuk menemukan yang berbentuk rectangle
    screenCnt = None
    for c in contours:
        # Approximate contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # Jika 4 points, kemungkinan ini adalah dokumen
        if len(approx) == 4:
            screenCnt = approx
            break
    
    return screenCnt, edged

def scan_document(image_path):
    """
    Main function untuk scan dokumen
    """
    # Load gambar
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    # Resize untuk processing lebih cepat
    orig = image.copy()
    ratio = 800.0 / image.shape[0]
    image = cv2.resize(image, None, fx=ratio, fy=ratio)
    
    # Temukan dokumen
    screenCnt, edged = find_document(image)
    
    if screenCnt is None:
        print("  ⚠ Dokumen tidak terdeteksi!")
        return None, None, None
    
    # Gambar contour pada hasil
    result = image.copy()
    cv2.drawContours(result, [screenCnt], -1, (0, 255, 0), 2)
    
    # Apply perspective transform
    warped = four_point_transform(image, screenCnt.reshape(4, 2))
    
    # Convert ke grayscale dan threshold untuk hasil scan yang lebih bersih
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped_thresh = cv2.adaptiveThreshold(
        warped_gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 4
    )
    
    return result, warped, warped_thresh, edged

def create_demo_document():
    """
    Membuat gambar demo dokumen untuk testing
    """
    # Buat canvas putih
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Tambah teks
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Penjelasan parameter cv2.putText:
    # cv2.putText(image, text, org, fontFace, fontScale, color, thickness, lineType)
    # - image: gambar target
    # - text: teks yang akan ditulis
    # - org: posisi (x, y) kiri-bawah teks
    # - fontFace: jenis font
    # - fontScale: skala ukuran font
    # - color: warna (BGR)
    # - thickness: ketebalan teks
    # - lineType: tipe garis (opsional)
    cv2.putText(canvas, "DEMO DOCUMENT", (150, 100), font, 2, (0, 0, 0), 3)
    cv2.putText(canvas, "Document Scanner Test", (200, 200), font, 1, (0, 0, 0), 2)
    cv2.putText(canvas, "This is a sample document", (150, 300), font, 0.8, (100, 100, 100), 2)
    cv2.putText(canvas, "for testing perspective", (150, 350), font, 0.8, (100, 100, 100), 2)
    cv2.putText(canvas, "correction and scanning.", (150, 400), font, 0.8, (100, 100, 100), 2)
    
    # Tambah border
    cv2.rectangle(canvas, (50, 50), (750, 550), (0, 0, 0), 3)
    
    # Apply perspective transform (simulasi foto dokumen dari sudut)
    h, w = canvas.shape[:2]
    
    # Source points (rectangle)
    src_pts = np.float32([[50, 50], [750, 50], [750, 550], [50, 550]])
    
    # Destination points (trapezoid - simulasi perspective)
    dst_pts = np.float32([[100, 100], [700, 80], [720, 500], [80, 520]])
    
    # Warp
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(canvas, M, (w, h))
    
    # Tambah background
    background = np.ones((700, 900, 3), dtype=np.uint8) * 200
    background[50:650, 50:850] = warped
    
    return background

def main():
    print("=" * 70)
    print("PRAKTIKUM BONUS: DOCUMENT SCANNER")
    print("=" * 70)
    print()
    
    print("Aplikasi Real-World:")
    print("  - Mobile document scanner")
    print("  - Receipt scanning")
    print("  - ID card digitization")
    print("  - Whiteboard capture")
    print()
    
    # Setup paths
    script_dir = get_script_dir()
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Buat demo document
    print("Membuat demo document...")
    demo_doc = create_demo_document()
    demo_path = os.path.join(output_dir, "demo_document.jpg")
    cv2.imwrite(demo_path, demo_doc)
    print(f"  ✓ Demo document dibuat: {demo_path}")
    print()
    
    # Process demo document
    print("Memproses demo document...")
    print("-" * 40)
    
    result, warped, warped_thresh, edged = scan_document(demo_path)
    
    if result is not None:
        print("  ✓ Dokumen terdeteksi!")
        print("  ✓ Perspective correction applied")
        
        # Resize untuk visualisasi
        max_width = 400
        h, w = result.shape[:2]
        if w > max_width:
            scale = max_width / w
            result = cv2.resize(result, None, fx=scale, fy=scale)
            edged = cv2.resize(edged, None, fx=scale, fy=scale)
            warped = cv2.resize(warped, None, fx=scale, fy=scale)
            warped_thresh = cv2.resize(warped_thresh, None, fx=scale, fy=scale)
        
        # Tambah label
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(result, "1. Detected", (10, 30), font, 0.7, (0, 255, 0), 2)
        
        edged_color = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR)
        cv2.putText(edged_color, "2. Edges", (10, 30), font, 0.7, (255, 255, 255), 2)
        
        cv2.putText(warped, "3. Corrected", (10, 30), font, 0.7, (0, 255, 0), 2)
        
        warped_thresh_color = cv2.cvtColor(warped_thresh, cv2.COLOR_GRAY2BGR)
        cv2.putText(warped_thresh_color, "4. Scanned", (10, 30), font, 0.7, (255, 255, 255), 2)
        
        # Resize semua ke ukuran yang sama untuk stacking
        target_h, target_w = result.shape[:2]
        edged_color = cv2.resize(edged_color, (target_w, target_h))
        warped = cv2.resize(warped, (target_w, target_h))
        warped_thresh_color = cv2.resize(warped_thresh_color, (target_w, target_h))
        
        # Gabungkan
        row1 = np.hstack([result, edged_color])
        row2 = np.hstack([warped, warped_thresh_color])
        visualization = np.vstack([row1, row2])
        
        # Simpan
        output_path = os.path.join(output_dir, "document_scanner_demo.jpg")
        cv2.imwrite(output_path, visualization)
        print(f"  Output disimpan: {output_path}")
    
    print()
    print("=" * 70)
    print("CARA MENGGUNAKAN DENGAN GAMBAR SENDIRI:")
    print("=" * 70)
    print("""
1. Foto dokumen Anda dengan background kontras
   - Pastikan 4 sudut dokumen terlihat jelas
   - Pencahayaan merata
   - Background berbeda warna dengan dokumen
   
2. Simpan gambar di folder data/images/
   
3. Modifikasi kode untuk load gambar Anda:
   image_path = "data/images/your_document.jpg"
   
4. Run program dan lihat hasil!

Tips untuk hasil terbaik:
  - Dokumen harus berbentuk rectangle (tidak kusut)
  - Background simple dan kontras
  - Pencahayaan cukup
  - Fokus kamera tajam
""")
    
    print()
    print("=" * 70)
    print("KONSEP YANG DIPELAJARI:")
    print("=" * 70)
    print("""
✓ Contour detection untuk menemukan shape
✓ Polygon approximation untuk simplifikasi shape
✓ Four-point perspective transform
✓ Adaptive thresholding untuk hasil scan bersih
✓ Integration multiple CV techniques untuk solve real problem

Ini adalah contoh bagaimana teknik-teknik yang dipelajari
di praktikum sebelumnya diintegrasikan untuk membuat aplikasi nyata!
""")
    
    print("Selesai! Cek folder output untuk hasil.")

if __name__ == "__main__":
    main()
