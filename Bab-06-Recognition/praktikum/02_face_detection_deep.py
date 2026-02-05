"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 02: Deep Learning Face Detection (OpenCV DNN)

Tujuan:
1) Menggunakan model DNN bawaan OpenCV untuk deteksi wajah.
2) Menyimpan hasil dan menampilkan output dengan auto-close 2 detik.
"""

# Import OpenCV untuk DNN dan operasi citra.
import cv2
# Import NumPy untuk pembuatan gambar sintetis.
import numpy as np
# Import Path untuk penanganan path file.
from pathlib import Path
# Import urllib untuk mengunduh model.
import urllib.request
# Import time untuk pengukuran waktu inferensi.
import time


def create_output_dir():
    """Buat folder output hasil deteksi."""
    # Tentukan folder output.
    output_dir = Path("output_deep_face_detection")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path folder.
    return output_dir


def download_dnn_model():
    """Unduh model OpenCV DNN (Res10 SSD) jika belum tersedia."""
    # Tentukan folder model.
    models_dir = Path("models")
    # Buat folder model jika belum ada.
    models_dir.mkdir(parents=True, exist_ok=True)
    # Tentukan file prototxt.
    prototxt = models_dir / "deploy.prototxt"
    # Tentukan file caffemodel.
    caffemodel = models_dir / "res10_300x300_ssd_iter_140000.caffemodel"
    # Unduh prototxt jika belum ada.
    if not prototxt.exists():
        # Unduh prototxt dari repository OpenCV.
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
            prototxt,
        )
    # Unduh caffemodel jika belum ada.
    if not caffemodel.exists():
        # Unduh caffemodel dari repository OpenCV.
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel",
            caffemodel,
        )
    # Kembalikan path model.
    return prototxt, caffemodel


def load_sample_image():
    """Muat gambar dari folder data atau buat gambar sintetis."""
    # Cari kandidat gambar pada folder data.
    candidates = list(Path("data").glob("*.jpg")) + list(Path("data").glob("*.png"))
    # Jika ada file, gunakan gambar pertama.
    if candidates:
        # Baca gambar dari disk.
        return cv2.imread(str(candidates[0]))
    # Buat kanvas putih.
    image = np.ones((480, 640, 3), dtype=np.uint8) * 220
    # Tambahkan dua wajah sintetis.
    for x, y, r in [(200, 220, 80), (420, 240, 70)]:
        # Gambar oval wajah.
        cv2.ellipse(image, (x, y), (r, int(r * 1.2)), 0, 0, 360, (200, 170, 140), -1)
        # Gambar outline wajah.
        cv2.ellipse(image, (x, y), (r, int(r * 1.2)), 0, 0, 360, (90, 70, 50), 2)
        # Gambar mata kiri.
        cv2.circle(image, (x - r // 3, y - r // 5), r // 8, (255, 255, 255), -1)
        # Gambar mata kanan.
        cv2.circle(image, (x + r // 3, y - r // 5), r // 8, (255, 255, 255), -1)
        # Gambar pupil kiri.
        cv2.circle(image, (x - r // 3, y - r // 5), r // 16, (40, 40, 40), -1)
        # Gambar pupil kanan.
        cv2.circle(image, (x + r // 3, y - r // 5), r // 16, (40, 40, 40), -1)
        # Gambar mulut.
        cv2.ellipse(image, (x, y + r // 3), (r // 3, r // 6), 0, 0, 180, (120, 80, 80), 2)
    # Tambahkan teks label.
    cv2.putText(image, "Sample Face Image", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
    # Kembalikan gambar sintetis.
    return image


def detect_faces_dnn(image, prototxt, caffemodel, conf_threshold=0.5):
    """Deteksi wajah dengan OpenCV DNN."""
    # Muat model DNN.
    net = cv2.dnn.readNetFromCaffe(str(prototxt), str(caffemodel))
    # Tentukan ukuran input model.
    input_size = (300, 300)
    # Buat blob dari gambar input.
    blob = cv2.dnn.blobFromImage(cv2.resize(image, input_size), 1.0, input_size, (104.0, 177.0, 123.0))
    # Set input ke jaringan.
    net.setInput(blob)
    # Catat waktu sebelum inferensi.
    start = time.time()
    # Jalankan forward pass.
    detections = net.forward()
    # Hitung waktu inferensi.
    elapsed = time.time() - start
    # Ambil ukuran gambar.
    h, w = image.shape[:2]
    # Siapkan daftar kotak hasil.
    boxes = []
    # Loop hasil deteksi.
    for i in range(detections.shape[2]):
        # Ambil confidence deteksi.
        confidence = float(detections[0, 0, i, 2])
        # Filter berdasarkan threshold.
        if confidence >= conf_threshold:
            # Ambil koordinat bounding box ter-normalisasi.
            x1 = int(detections[0, 0, i, 3] * w)
            # Ambil koordinat y1.
            y1 = int(detections[0, 0, i, 4] * h)
            # Ambil koordinat x2.
            x2 = int(detections[0, 0, i, 5] * w)
            # Ambil koordinat y2.
            y2 = int(detections[0, 0, i, 6] * h)
            # Hitung lebar dan tinggi box.
            boxes.append((x1, y1, x2 - x1, y2 - y1, confidence))
    # Kembalikan box dan waktu.
    return boxes, elapsed


def draw_boxes(image, boxes):
    """Gambar bounding box hasil deteksi ke gambar."""
    # Salin gambar agar original tetap aman.
    output = image.copy()
    # Loop setiap box.
    for i, (x, y, w, h, conf) in enumerate(boxes):
        # Gambar kotak deteksi.
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Susun label confidence.
        label = f"Face {i + 1}: {conf:.2f}"
        # Tulis label ke gambar.
        cv2.putText(output, label, (x, max(0, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    # Kembalikan gambar hasil.
    return output


def show_image(title, image, delay_ms=2000):
    """Tampilkan gambar dan auto-close setelah delay tertentu."""
    # Coba tampilkan jendela jika GUI tersedia.
    try:
        # Tampilkan gambar.
        cv2.imshow(title, image)
        # Tunggu beberapa milidetik.
        cv2.waitKey(delay_ms)
        # Tutup semua jendela.
        cv2.destroyAllWindows()
    except Exception:
        # Abaikan jika display tidak tersedia.
        pass


def main():
    """Fungsi utama untuk menjalankan demo deteksi DNN."""
    # Unduh model jika belum ada.
    prototxt, caffemodel = download_dnn_model()
    # Muat gambar sampel.
    image = load_sample_image()
    # Jalankan deteksi DNN.
    boxes, elapsed = detect_faces_dnn(image, prototxt, caffemodel)
    # Gambar hasil deteksi.
    result = draw_boxes(image, boxes)
    # Buat folder output.
    output_dir = create_output_dir()
    # Simpan hasil ke file.
    cv2.imwrite(str(output_dir / "02_dnn_faces.jpg"), result)
    # Cetak ringkasan ke terminal.
    print(f"DNN: {len(boxes)} faces, {elapsed*1000:.2f} ms")
    # Tampilkan hasil dengan auto-close.
    show_image("DNN Face Detection", result)


# Jalankan program saat file dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
