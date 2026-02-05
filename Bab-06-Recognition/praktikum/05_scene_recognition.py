"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 05: Scene Recognition (Indoor vs Outdoor)

Tujuan:
1) Mengklasifikasikan scene menggunakan fitur warna sederhana.
2) Menampilkan hasil dengan auto-close 2 detik.
"""

# Import OpenCV untuk operasi citra.
import cv2
# Import NumPy untuk manipulasi numerik.
import numpy as np
# Import Path untuk akses data.
from pathlib import Path


def create_output_dir():
    """Buat folder output hasil scene recognition."""
    # Tentukan folder output.
    output_dir = Path("output_scene_recognition")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path output.
    return output_dir


def load_scene_image():
    """Muat gambar dari folder data atau buat scene sintetis."""
    # Cari file gambar pada folder data.
    candidates = list(Path("data").glob("*.jpg")) + list(Path("data").glob("*.png"))
    # Jika ada gambar, gunakan gambar pertama.
    if candidates:
        # Baca gambar dari disk.
        return cv2.imread(str(candidates[0]))
    # Buat kanvas kosong untuk scene sintetis outdoor.
    image = np.ones((360, 640, 3), dtype=np.uint8) * 220
    # Buat langit biru.
    image[:160, :] = (255, 210, 120)
    # Buat area hijau sebagai vegetasi.
    image[160:300, :] = (80, 160, 80)
    # Buat area jalan abu-abu.
    image[300:, :] = (120, 120, 120)
    # Tambahkan matahari.
    cv2.circle(image, (540, 60), 30, (0, 255, 255), -1)
    # Tambahkan teks label.
    cv2.putText(image, "Synthetic Outdoor Scene", (20, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    # Kembalikan scene sintetis.
    return image


def extract_color_features(image):
    """Ekstrak fitur warna sederhana (mean BGR)."""
    # Hitung rata-rata setiap channel.
    mean_bgr = image.mean(axis=(0, 1))
    # Kembalikan vektor fitur.
    return mean_bgr


def classify_scene_simple(features):
    """Klasifikasi scene sederhana berdasarkan dominasi warna."""
    # Ambil channel biru, hijau, merah.
    blue, green, red = features
    # Jika biru tinggi, prediksi outdoor (sky dominan).
    if blue > green and blue > red:
        # Kembalikan label outdoor.
        return "Outdoor"
    # Jika hijau tinggi, prediksi outdoor (vegetasi).
    if green > blue and green > red:
        # Kembalikan label outdoor.
        return "Outdoor"
    # Selain itu, prediksi indoor.
    return "Indoor"


def annotate_scene(image, label):
    """Tambahkan label prediksi pada gambar."""
    # Salin gambar agar aman.
    output = image.copy()
    # Susun teks label.
    text = f"Scene: {label}"
    # Tulis teks label ke gambar.
    cv2.putText(output, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    # Kembalikan gambar hasil.
    return output


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
    """Fungsi utama untuk demo scene recognition."""
    # Muat gambar scene.
    image = load_scene_image()
    # Ekstrak fitur warna.
    features = extract_color_features(image)
    # Prediksi label scene.
    label = classify_scene_simple(features)
    # Anotasi hasil prediksi.
    output = annotate_scene(image, label)
    # Buat folder output.
    output_dir = create_output_dir()
    # Simpan hasil ke file.
    cv2.imwrite(str(output_dir / "05_scene_recognition.jpg"), output)
    # Cetak hasil prediksi.
    print("="*70)
    print("PRAKTIKUM SCENE RECOGNITION")
    print("="*70)
    print(f"\nPrediksi scene: {label}")
    print(f"Output files saved to: {output_dir}/")
    # Tampilkan hasil dengan auto-close.
    show_image("Scene Recognition", output)


if __name__ == "__main__":
    main()
