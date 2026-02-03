"""
=============================================================================
DOWNLOAD SAMPLE DATA - BAB 7: DETEKSI FITUR DAN PENCOCOKAN
=============================================================================
Script ini akan mendownload gambar-gambar contoh yang diperlukan untuk
praktikum deteksi fitur dan pencocokan.

Gambar yang didownload:
1. Checkerboard - untuk deteksi corner
2. Building/Architecture - objek dengan banyak fitur
3. Object pairs - untuk feature matching
4. Book/Document - untuk homography testing
=============================================================================
"""

import urllib.request
import os
import sys

def download_file(url, filepath):
    """Download file dari URL ke filepath yang ditentukan"""
    try:
        print(f"Downloading: {os.path.basename(filepath)}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"  ✓ Berhasil: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Gagal download {url}: {e}")
        return False

def create_directories():
    """Buat struktur folder yang diperlukan"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    directories = [
        os.path.join(script_dir, "data", "images"),
        os.path.join(script_dir, "data", "videos"),
        os.path.join(script_dir, "praktikum", "output"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Folder dibuat/ada: {directory}")
    
    return script_dir

def main():
    print("=" * 60)
    print("DOWNLOAD SAMPLE DATA - BAB 7: DETEKSI FITUR")
    print("=" * 60)
    print()
    
    # Buat direktori
    script_dir = create_directories()
    images_dir = os.path.join(script_dir, "data", "images")
    
    print()
    print("Mengunduh gambar sampel...")
    print("-" * 40)
    
    # Daftar gambar untuk didownload
    # Menggunakan gambar dari berbagai sumber public domain
    images = {
        # Checkerboard untuk corner detection
        "checkerboard.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/chessboard.png",
        
        # Building dengan banyak fitur
        "building.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/building.jpg",
        
        # Box untuk feature matching (template)
        "box.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/box.png",
        
        # Box in scene (untuk matching)
        "box_in_scene.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/box_in_scene.png",
        
        # Sudoku untuk perspective transform
        "sudoku.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/sudoku.png",
        
        # Gambar untuk homography
        "home.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/home.jpg",
        
        # Left dan right image untuk stereo/matching
        "left01.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/left01.jpg",
        "right01.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/right01.jpg",
        
        # Gambar dengan rotasi untuk testing invariance
        "graf1.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/graf1.png",
        "graf3.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/graf3.png",
        
        # Butterfly untuk blob detection
        "butterfly.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/butterfly.jpg",
    }
    
    # Download semua gambar
    success_count = 0
    fail_count = 0
    
    for filename, url in images.items():
        filepath = os.path.join(images_dir, filename)
        if download_file(url, filepath):
            success_count += 1
        else:
            fail_count += 1
    
    print()
    print("=" * 60)
    print(f"HASIL DOWNLOAD:")
    print(f"  Berhasil: {success_count} file")
    print(f"  Gagal: {fail_count} file")
    print("=" * 60)
    
    # Buat file README di folder data
    readme_content = """# Data Sampel - Bab 7: Deteksi Fitur dan Pencocokan

## Daftar Gambar

| File | Kegunaan |
|------|----------|
| checkerboard.png | Deteksi corner dengan pola teratur |
| building.jpg | Objek dengan banyak fitur natural |
| box.png | Template untuk feature matching |
| box_in_scene.png | Scene dengan objek box untuk matching |
| sudoku.png | Testing perspective transform |
| home.jpg | Homography dan transformasi perspektif |
| left01.jpg, right01.jpg | Stereo matching |
| graf1.png, graf3.png | Testing rotation invariance |
| butterfly.jpg | Blob detection dan fitur natural |

## Sumber
Gambar-gambar ini berasal dari OpenCV samples yang tersedia secara publik.
https://github.com/opencv/opencv/tree/master/samples/data

## Penggunaan
Gambar-gambar ini digunakan untuk praktikum deteksi fitur dan pencocokan.
Silakan gunakan gambar sendiri untuk eksplorasi lebih lanjut.
"""
    
    readme_path = os.path.join(script_dir, "data", "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ README dibuat: {readme_path}")
    
    print()
    print("Selesai! Silakan jalankan program praktikum.")
    
    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
