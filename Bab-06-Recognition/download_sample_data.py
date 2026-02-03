"""
=============================================================================
DOWNLOAD SAMPLE DATA - BAB 06 RECOGNITION
=============================================================================
Script untuk mengunduh dan menyiapkan sample data untuk praktikum Recognition.

Data yang diunduh:
1. Sample images untuk face detection/recognition
2. Pre-trained models untuk face detection
3. Sample images untuk scene recognition
4. Sample images untuk OCR

Author: [Nama Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import os
import urllib.request
import ssl

# Disable SSL verification untuk menghindari error sertifikat
ssl._create_default_https_context = ssl._create_unverified_context


def create_directories():
    """Membuat struktur folder untuk data."""
    dirs = [
        "data",
        "data/faces",
        "data/faces/train",
        "data/faces/test",
        "data/objects",
        "data/scenes",
        "data/ocr",
        "data/models"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"[OK] Folder dibuat: {d}")


def download_face_detection_models():
    """
    Mengunduh model Haar Cascade dan DNN untuk face detection.
    """
    print("\n[1/4] Mengunduh Face Detection Models...")
    print("-" * 50)
    
    # Haar Cascade models (biasanya sudah ada di OpenCV)
    models = {
        "haarcascade_frontalface_default.xml": 
            "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
        "haarcascade_frontalface_alt.xml":
            "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml",
        "haarcascade_eye.xml":
            "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml",
    }
    
    for name, url in models.items():
        filepath = os.path.join("data/models", name)
        if not os.path.exists(filepath):
            try:
                print(f"  Mengunduh {name}...")
                urllib.request.urlretrieve(url, filepath)
                print(f"  [OK] {name} berhasil diunduh")
            except Exception as e:
                print(f"  [ERROR] Gagal mengunduh {name}: {e}")
        else:
            print(f"  [SKIP] {name} sudah ada")
    
    # Info tentang DNN model
    print("\n  [INFO] Untuk DNN face detector, unduh manual:")
    print("  - deploy.prototxt dari:")
    print("    https://github.com/opencv/opencv/blob/master/samples/dnn/face_detector/deploy.prototxt")
    print("  - res10_300x300_ssd_iter_140000.caffemodel dari:")
    print("    https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel")


def download_sample_images():
    """
    Mengunduh sample images dari sumber public domain.
    """
    print("\n[2/4] Mengunduh Sample Images...")
    print("-" * 50)
    
    # Sample face images (dari Unsplash - free to use)
    face_urls = [
        ("face_sample_1.jpg", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("face_sample_2.jpg", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400"),
        ("face_sample_3.jpg", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"),
    ]
    
    for name, url in face_urls:
        filepath = os.path.join("data/faces/test", name)
        if not os.path.exists(filepath):
            try:
                print(f"  Mengunduh {name}...")
                urllib.request.urlretrieve(url, filepath)
                print(f"  [OK] {name}")
            except Exception as e:
                print(f"  [ERROR] {name}: {e}")
        else:
            print(f"  [SKIP] {name} sudah ada")
    
    # Sample scene images
    scene_urls = [
        ("beach.jpg", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("office.jpg", "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"),
        ("street.jpg", "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400"),
        ("forest.jpg", "https://images.unsplash.com/photo-1448375240586-882707db888b?w=400"),
        ("kitchen.jpg", "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"),
    ]
    
    for name, url in scene_urls:
        filepath = os.path.join("data/scenes", name)
        if not os.path.exists(filepath):
            try:
                print(f"  Mengunduh {name}...")
                urllib.request.urlretrieve(url, filepath)
                print(f"  [OK] {name}")
            except Exception as e:
                print(f"  [ERROR] {name}: {e}")
        else:
            print(f"  [SKIP] {name} sudah ada")


def create_synthetic_ocr_images():
    """
    Membuat synthetic images untuk OCR testing.
    """
    print("\n[3/4] Membuat Synthetic OCR Images...")
    print("-" * 50)
    
    try:
        import cv2
        import numpy as np
        
        # Simple text image
        img1 = np.ones((100, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img1, "Hello World", (50, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        cv2.imwrite("data/ocr/text_sample_1.jpg", img1)
        print("  [OK] text_sample_1.jpg")
        
        # Numbers
        img2 = np.ones((100, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img2, "12345-67890", (30, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        cv2.imwrite("data/ocr/text_sample_2.jpg", img2)
        print("  [OK] text_sample_2.jpg")
        
        # License plate style
        img3 = np.ones((80, 250, 3), dtype=np.uint8) * 255
        cv2.rectangle(img3, (5, 5), (245, 75), (0, 0, 0), 2)
        cv2.putText(img3, "B 1234 ABC", (20, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.imwrite("data/ocr/license_plate.jpg", img3)
        print("  [OK] license_plate.jpg")
        
        # Document style
        img4 = np.ones((300, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img4, "INVOICE #001", (100, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.line(img4, (50, 55), (350, 55), (0, 0, 0), 1)
        cv2.putText(img4, "Item: Product A", (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(img4, "Qty: 5", (50, 130), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(img4, "Price: $100.00", (50, 160), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(img4, "Total: $500.00", (50, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.imwrite("data/ocr/invoice.jpg", img4)
        print("  [OK] invoice.jpg")
        
    except ImportError:
        print("  [WARNING] OpenCV tidak tersedia - skip pembuatan synthetic images")


def create_face_database_template():
    """
    Membuat template struktur untuk face database.
    """
    print("\n[4/4] Membuat Face Database Template...")
    print("-" * 50)
    
    # Buat folder untuk beberapa orang
    persons = ["person_01", "person_02", "person_03"]
    
    for person in persons:
        person_dir = os.path.join("data/faces/train", person)
        os.makedirs(person_dir, exist_ok=True)
        
        # Buat README di setiap folder
        readme = os.path.join(person_dir, "README.txt")
        with open(readme, 'w') as f:
            f.write(f"Folder untuk foto {person}\n")
            f.write("Masukkan 5-10 foto wajah orang ini.\n")
            f.write("Pastikan foto dari berbagai sudut dan pencahayaan.\n")
        
        print(f"  [OK] Template untuk {person}")
    
    print("\n  [INFO] Untuk menggunakan face recognition:")
    print("  1. Isi folder data/faces/train/person_XX dengan foto wajah")
    print("  2. Gunakan nama folder sebagai label/nama orang")
    print("  3. Minimal 5 foto per orang disarankan")


def print_summary():
    """
    Menampilkan ringkasan data yang tersedia.
    """
    print("\n" + "=" * 60)
    print("RINGKASAN DATA")
    print("=" * 60)
    
    # Count files in each directory
    directories = [
        ("data/faces/train", "Face Training"),
        ("data/faces/test", "Face Testing"),
        ("data/objects", "Objects"),
        ("data/scenes", "Scenes"),
        ("data/ocr", "OCR Samples"),
        ("data/models", "Models")
    ]
    
    for path, name in directories:
        if os.path.exists(path):
            files = [f for f in os.listdir(path) 
                    if os.path.isfile(os.path.join(path, f)) 
                    and not f.startswith('.')]
            dirs = [d for d in os.listdir(path) 
                   if os.path.isdir(os.path.join(path, d))]
            print(f"  {name:20s}: {len(files)} files, {len(dirs)} folders")
        else:
            print(f"  {name:20s}: Not found")
    
    print("\n" + "-" * 60)
    print("LANGKAH SELANJUTNYA:")
    print("-" * 60)
    print("1. Tambahkan foto wajah ke data/faces/train/person_XX")
    print("2. Jika menggunakan DNN face detector, unduh model manual")
    print("3. Jalankan program praktikum sesuai kebutuhan")
    print("=" * 60)


def main():
    """
    Fungsi utama untuk mengunduh semua sample data.
    """
    print("=" * 60)
    print("DOWNLOAD SAMPLE DATA - BAB 06 RECOGNITION")
    print("=" * 60)
    print("\nScript ini akan mengunduh sample data untuk praktikum.\n")
    
    # Konfirmasi user
    response = input("Lanjutkan download? (y/n): ").strip().lower()
    if response != 'y':
        print("Download dibatalkan.")
        return
    
    # Jalankan proses download
    create_directories()
    download_face_detection_models()
    download_sample_images()
    create_synthetic_ocr_images()
    create_face_database_template()
    print_summary()
    
    print("\n[SELESAI] Download sample data selesai!")


if __name__ == "__main__":
    main()
