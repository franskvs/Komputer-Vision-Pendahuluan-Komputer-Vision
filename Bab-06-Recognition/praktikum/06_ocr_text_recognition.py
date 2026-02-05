"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 06: OCR dan Text Recognition (Tesseract jika tersedia)

Tujuan:
1) Melakukan preprocessing OCR.
2) Membaca teks dengan pytesseract jika tersedia.
3) Menampilkan hasil dengan auto-close 2 detik.
"""

# Import OpenCV untuk operasi citra.
import cv2
# Import NumPy untuk manipulasi numerik.
import numpy as np
# Import Path untuk akses file.
from pathlib import Path

# Coba import pytesseract (opsional).
try:
    # Import pytesseract jika tersedia.
    import pytesseract
    # Tandai bahwa tesseract tersedia.
    TESSERACT_AVAILABLE = True
except Exception:
    # Tandai bahwa tesseract tidak tersedia.
    TESSERACT_AVAILABLE = False


def create_output_dir():
    """Buat folder output hasil OCR."""
    # Tentukan folder output.
    output_dir = Path("output_ocr")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path output.
    return output_dir


def create_text_image(text="Praktikum OCR", font_scale=1.5, add_noise=False, rotate_angle=0):
    """Buat gambar teks sintetis untuk demo OCR."""
    # Tentukan ukuran gambar.
    width, height = 600, 150
    # Buat background putih.
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    # Tentukan font dan skala.
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Hitung ukuran teks.
    text_size = cv2.getTextSize(text, font, font_scale, 3)[0]
    # Hitung posisi teks agar tengah.
    text_x = (width - text_size[0]) // 2
    # Hitung posisi y teks.
    text_y = (height + text_size[1]) // 2
    # Gambar teks pada canvas.
    cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), 3)
    # Jika diminta noise, tambahkan.
    if add_noise:
        # Tambahkan Gaussian noise.
        noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
        # Gabungkan dengan image.
        image = cv2.add(image, noise)
    # Jika diminta rotasi, lakukan rotasi.
    if rotate_angle != 0:
        # Tentukan titik tengah.
        center = (width // 2, height // 2)
        # Buat matriks rotasi.
        matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
        # Terapkan rotasi.
        image = cv2.warpAffine(image, matrix, (width, height), borderValue=(255, 255, 255))
    # Kembalikan gambar teks.
    return image


def preprocess_for_ocr(image):
    """Preprocessing sederhana untuk OCR."""
    # Konversi ke grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Terapkan Gaussian blur untuk mengurangi noise.
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # Terapkan threshold Otsu untuk binarisasi.
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Kembalikan hasil preprocessing.
    return binary


def run_ocr(image):
    """Jalankan OCR jika pytesseract tersedia, jika tidak kembalikan dummy."""
    # Jika tesseract tidak tersedia, kembalikan placeholder.
    if not TESSERACT_AVAILABLE:
        # Kembalikan hasil dummy.
        return "(pytesseract tidak tersedia)"
    # Jalankan OCR pada gambar.
    text = pytesseract.image_to_string(image)
    # Kembalikan teks hasil OCR.
    return text.strip()


def show_image(title, image, delay_ms=2000):
    """Tampilkan gambar dengan auto-close."""
    # Coba tampilkan jendela jika GUI tersedia.
    try:
        # Tampilkan gambar.
        cv2.imshow(title, image)
        # Tunggu beberapa milidetik.
        cv2.waitKey(delay_ms)
        # Tutup jendela.
        cv2.destroyAllWindows()
    except Exception:
        # Abaikan jika display tidak tersedia.
        pass


def main():
    """
    Fungsi utama program OCR dan Text Recognition.
    """
    # Buat folder output.
    output_dir = create_output_dir()
    
    # Buat image text sintetis.
    text_img = create_text_image("OCR Demo")
    
    # Pre-process image untuk OCR.
    processed = preprocess_for_ocr(text_img)
    
    # Jalankan OCR.
    ocr_result = run_ocr(processed)
    
    # Simpan hasil.
    cv2.imwrite(str(output_dir / "06_ocr_demo.jpg"), text_img)
    cv2.imwrite(str(output_dir / "06_ocr_processed.jpg"), processed)
    
    # Cetak hasil.
    print("="*70)
    print("PRAKTIKUM OCR DAN TEXT RECOGNITION")
    print("="*70)
    print(f"\n[INFO] OCR Result: {ocr_result}")
    print(f"[INFO] Output files saved to: {output_dir}/")
    
    # Tampilkan dengan auto-close.
    show_image("OCR Demo - Original", text_img, delay_ms=2000)
    show_image("OCR Demo - Processed", processed, delay_ms=2000)


if __name__ == "__main__":
    main()
