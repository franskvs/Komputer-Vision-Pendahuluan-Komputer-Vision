"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 01: Face Detection dengan OpenCV (Haar + HOG dlib)

Tujuan:
1) Menjalankan face detection klasik (Haar Cascade).
2) Menjalankan face detection berbasis HOG+SVM (dlib) jika tersedia.
3) Menyimpan dan menampilkan hasil dengan auto-close 2 detik.
"""

# Import library OpenCV untuk operasi pengolahan citra.
import cv2
# Import NumPy untuk manipulasi array dan pembuatan citra sintetis.
import numpy as np
# Import Path untuk penanganan path file/folder.
from pathlib import Path
# Import time untuk pencatatan waktu proses.
import time

# Coba import dlib untuk HOG+SVM face detector (opsional).
try:
    # Import dlib jika tersedia di lingkungan.
    import dlib
    # Tandai bahwa dlib tersedia.
    DLIB_AVAILABLE = True
except Exception:
    # Tandai bahwa dlib tidak tersedia.
    DLIB_AVAILABLE = False


def create_output_dir():
    """Membuat folder output untuk hasil deteksi."""
    # Tentukan nama folder output.
    output_dir = Path("output_face_detection")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path folder output.
    return output_dir


def load_sample_image():
    """Muat gambar sampel dari folder data, atau buat gambar sintetis."""
    # Tentukan kandidat gambar dari folder data.
    candidates = list(Path("data").glob("*.jpg")) + list(Path("data").glob("*.png"))
    # Periksa apakah ada gambar yang tersedia.
    if candidates:
        # Baca gambar pertama yang ditemukan.
        return cv2.imread(str(candidates[0]))
    # Buat kanvas putih untuk gambar sintetis.
    image = np.ones((480, 640, 3), dtype=np.uint8) * 230
    # Tentukan posisi wajah sintetis.
    faces = [(160, 200, 70), (360, 210, 60), (480, 300, 65)]
    # Gambar wajah sintetis satu per satu.
    for x, y, r in faces:
        # Gambar oval wajah.
        cv2.ellipse(image, (x, y), (r, int(r * 1.2)), 0, 0, 360, (200, 170, 140), -1)
        # Gambar outline wajah.
        cv2.ellipse(image, (x, y), (r, int(r * 1.2)), 0, 0, 360, (80, 60, 40), 2)
        # Gambar mata kiri.
        cv2.circle(image, (x - r // 3, y - r // 5), r // 8, (255, 255, 255), -1)
        # Gambar mata kanan.
        cv2.circle(image, (x + r // 3, y - r // 5), r // 8, (255, 255, 255), -1)
        # Gambar pupil kiri.
        cv2.circle(image, (x - r // 3, y - r // 5), r // 16, (40, 40, 40), -1)
        # Gambar pupil kanan.
        cv2.circle(image, (x + r // 3, y - r // 5), r // 16, (40, 40, 40), -1)
        # Gambar mulut sederhana.
        cv2.ellipse(image, (x, y + r // 3), (r // 3, r // 6), 0, 0, 180, (120, 80, 80), 2)
    # Tambahkan label pada gambar sintetis.
    cv2.putText(image, "Synthetic Face Image", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
    # Kembalikan gambar sintetis.
    return image


def detect_faces_haar(image):
    """Deteksi wajah menggunakan Haar Cascade."""
    # Siapkan path cascade frontal face bawaan OpenCV.
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    # Inisialisasi cascade classifier.
    cascade = cv2.CascadeClassifier(cascade_path)
    # Konversi gambar ke grayscale untuk deteksi.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Tingkatkan kontras menggunakan histogram equalization.
    gray = cv2.equalizeHist(gray)
    # Catat waktu mulai deteksi.
    start = time.time()
    # Jalankan deteksi multi-scale.
    boxes = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    # Hitung waktu deteksi.
    elapsed = time.time() - start
    # Kembalikan bounding box dan waktu.
    return boxes, elapsed


def detect_faces_dlib(image):
    """Deteksi wajah menggunakan dlib HOG+SVM jika tersedia."""
    # Jika dlib tidak tersedia, kembalikan kosong.
    if not DLIB_AVAILABLE:
        # Kembalikan hasil kosong.
        return [], 0.0
    # Inisialisasi detector HOG+SVM.
    detector = dlib.get_frontal_face_detector()
    # Konversi gambar ke grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Catat waktu mulai deteksi.
    start = time.time()
    # Jalankan deteksi wajah.
    detections = detector(gray, 1)
    # Hitung waktu deteksi.
    elapsed = time.time() - start
    # Ubah hasil dlib ke format (x, y, w, h).
    boxes = [(d.left(), d.top(), d.width(), d.height()) for d in detections]
    # Kembalikan bounding box dan waktu.
    return boxes, elapsed


def draw_boxes(image, boxes, color, label):
    """Gambar bounding box dan label ke gambar."""
    # Salin gambar agar original tetap aman.
    output = image.copy()
    # Loop untuk setiap bounding box.
    for i, (x, y, w, h) in enumerate(boxes):
        # Gambar kotak deteksi.
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        # Susun teks label untuk setiap wajah.
        text = f"{label} {i + 1}"
        # Tulis teks label di atas kotak.
        cv2.putText(output, text, (x, max(0, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    # Kembalikan gambar dengan anotasi.
    return output


def show_image(title, image, delay_ms=2000):
    """Tampilkan gambar dengan auto-close setelah delay tertentu."""
    # Coba tampilkan jendela jika GUI tersedia.
    try:
        # Tampilkan gambar ke jendela.
        cv2.imshow(title, image)
        # Tunggu beberapa milidetik (auto-close).
        cv2.waitKey(delay_ms)
        # Tutup semua jendela OpenCV.
        cv2.destroyAllWindows()
    except Exception:
        # Abaikan jika display tidak tersedia.
        pass


def main():
    """Fungsi utama untuk menjalankan demo deteksi wajah."""
    # Muat gambar sampel.
    image = load_sample_image()
    # Jalankan deteksi Haar Cascade.
    haar_boxes, haar_time = detect_faces_haar(image)
    # Jalankan deteksi dlib jika tersedia.
    dlib_boxes, dlib_time = detect_faces_dlib(image)
    # Gambar hasil deteksi Haar pada gambar.
    haar_vis = draw_boxes(image, haar_boxes, (0, 255, 0), "Haar")
    # Gambar hasil deteksi dlib pada gambar.
    dlib_vis = draw_boxes(image, dlib_boxes, (255, 0, 0), "HOG")
    # Buat folder output.
    output_dir = create_output_dir()
    # Simpan hasil deteksi Haar.
    cv2.imwrite(str(output_dir / "01_haar_faces.jpg"), haar_vis)
    # Simpan hasil deteksi dlib.
    cv2.imwrite(str(output_dir / "01_hog_faces.jpg"), dlib_vis)
    # Cetak ringkasan hasil ke terminal.
    print(f"Haar: {len(haar_boxes)} faces, {haar_time*1000:.2f} ms")
    # Cetak ringkasan hasil dlib.
    print(f"HOG(dlib): {len(dlib_boxes)} faces, {dlib_time*1000:.2f} ms")
    # Tampilkan hasil Haar dengan auto-close.
    show_image("Haar Face Detection", haar_vis)
    # Tampilkan hasil HOG dengan auto-close.
    show_image("HOG Face Detection", dlib_vis)


# Jalankan program jika file dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
