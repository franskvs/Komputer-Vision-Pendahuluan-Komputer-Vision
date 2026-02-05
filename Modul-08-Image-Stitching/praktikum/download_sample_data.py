"""
Download Sample Data untuk Praktikum Bab 8: Image Stitching
===========================================================

Script ini mendownload gambar-gambar sampel yang diperlukan untuk
praktikum image stitching dan pembuatan panorama.

Penggunaan:
    python download_sample_data.py

Data yang didownload:
    - Set panorama untuk stitching
    - Gambar dengan overlap untuk testing
    - Multiple gambar untuk multi-image panorama
"""

import urllib.request
import os
import sys

def download_file(url, filepath):
    """
    Download file dari URL ke filepath yang ditentukan.
    
    Parameters:
        url: URL sumber file
        filepath: Path tujuan untuk menyimpan file
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        print(f"  Downloading {os.path.basename(filepath)}...", end=" ")
        urllib.request.urlretrieve(url, filepath)
        print("✓")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """
    Fungsi utama untuk mendownload semua data sampel.
    """
    print("=" * 60)
    print("DOWNLOAD SAMPLE DATA - BAB 8: IMAGE STITCHING")
    print("=" * 60)
    
    # Buat folder data/images jika belum ada
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data", "images")
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"\nFolder tujuan: {data_dir}\n")
    
    # Daftar file yang akan didownload
    # Menggunakan gambar dari berbagai sumber untuk stitching
    files_to_download = {
        # Gambar untuk stitching dasar
        "left01.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/left01.jpg",
        "right01.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/right01.jpg",
        
        # Gambar untuk testing
        "graf1.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/graf1.png",
        "graf3.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/graf3.png",
        
        # Gambar building untuk panorama
        "building.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/building.jpg",
        
        # Gambar lain untuk variasi
        "home.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/home.jpg",
        "box.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/box.png",
        "box_in_scene.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/box_in_scene.png",
        
        # Gambar untuk cylindrical projection
        "lena.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg",
        
        # Gambar tambahan
        "messi5.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg",
        "opencv-logo.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/opencv-logo.png",
    }
    
    # Download semua file
    print("Memulai download...\n")
    success_count = 0
    fail_count = 0
    
    for filename, url in files_to_download.items():
        filepath = os.path.join(data_dir, filename)
        
        # Skip jika file sudah ada
        if os.path.exists(filepath):
            print(f"  {filename} sudah ada, skip.")
            success_count += 1
            continue
        
        if download_file(url, filepath):
            success_count += 1
        else:
            fail_count += 1
    
    # Buat juga folder output untuk praktikum
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nFolder output dibuat: {output_dir}")
    
    # Buat folder untuk panorama sets
    pano_dir = os.path.join(data_dir, "panorama_set")
    os.makedirs(pano_dir, exist_ok=True)
    print(f"Folder panorama set dibuat: {pano_dir}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Berhasil: {success_count}")
    print(f"  Gagal: {fail_count}")
    print(f"  Total: {success_count + fail_count}")
    
    if fail_count > 0:
        print("\n⚠️  Beberapa file gagal didownload.")
        print("   Periksa koneksi internet dan coba lagi.")
    else:
        print("\n✅ Semua file berhasil didownload!")
        
    print("\n" + "=" * 60)
    print("INSTRUKSI TAMBAHAN")
    print("=" * 60)
    print("""
Untuk hasil terbaik, disarankan menggunakan foto sendiri:

1. Ambil 3-5 foto dengan smartphone
2. Overlap sekitar 30-50% antar foto
3. Putar badan (bukan kamera) saat mengambil foto
4. Hindari objek bergerak di area overlap
5. Simpan foto di folder: data/images/panorama_set/

Contoh penamaan:
   - panorama_set/pano_01.jpg
   - panorama_set/pano_02.jpg
   - panorama_set/pano_03.jpg
   - dll.
""")
    
    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
