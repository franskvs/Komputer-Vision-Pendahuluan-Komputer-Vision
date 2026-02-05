"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 1: HDR Imaging

Deskripsi:
    Program ini mendemonstrasikan pembuatan High Dynamic Range (HDR)
    image dari multiple exposure photographs dan berbagai teknik
    tone mapping untuk mengkonversi HDR ke displayable LDR.

Teori:
    HDR imaging menggabungkan multiple exposures untuk capture
    extended dynamic range yang melebihi sensor capability.
    
    Pipeline:
    1. Capture bracket exposures
    2. Align images (jika handheld)
    3. Merge ke HDR radiance map
    4. Tone map ke LDR untuk display

Tone Mapping Operators:
    - Drago: Logarithmic, mimics eye adaptation
    - Reinhard: Photographic reproduction
    - Mantiuk: Perceptually uniform

Parameter yang dapat dimodifikasi:
    - GAMMA: Gamma correction
    - SATURATION: Color saturation
    - CONTRAST: Contrast adjustment

Output:
    - HDR merged image (EXR format)
    - Tone mapped results dengan berbagai operators

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Gamma untuk tone mapping
GAMMA = 2.2

# Saturation adjustment
SATURATION = 1.0

# Exposure times (dalam detik)
# Sesuaikan dengan exposure bracket Anda
EXPOSURE_TIMES = np.array([1/30, 1/4, 1.0], dtype=np.float32)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output1")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_exposure_bracket(image_dir, pattern="scene_exp"):
    """
    Load exposure bracket images dari directory.
    
    Parameters:
        image_dir: Directory containing bracket images
        pattern: Filename pattern
    
    Returns:
        images: List of images
        times: Exposure times array
    """
    images = []
    
    # Try to find exposure bracket files
    for i in range(1, 10):
        filepath = os.path.join(image_dir, f"{pattern}{i}.jpg")
        if os.path.exists(filepath):
            img = cv2.imread(filepath)
            if img is not None:
                images.append(img)
                print(f"  Loaded: {pattern}{i}.jpg")
    
    if len(images) == 0:
        print("  No bracket images found!")
        return None, None
    
    # Adjust exposure times array to match
    times = EXPOSURE_TIMES[:len(images)]
    
    return images, times

def align_images(images):
    """
    Align exposure bracket images menggunakan MTB (Median Threshold Bitmap).
    
    Parameters:
        images: List of images to align
    
    Returns:
        aligned: List of aligned images
    """
    print("  Aligning images...")
    
    alignMTB = cv2.createAlignMTB()
    aligned = images.copy()
    alignMTB.process(images, aligned)
    
    return aligned

def create_hdr_debevec(images, times):
    """
    Buat HDR image menggunakan Debevec method.
    
    Parameters:
        images: Exposure bracket images
        times: Exposure times
    
    Returns:
        hdr: HDR radiance map
        response: Camera response function
    """
    print("  Creating HDR with Debevec method...")
    
    # Calibrate camera response
    calibrate = cv2.createCalibrateDebevec()
    response = calibrate.process(images, times)
    
    # Merge to HDR
    merge = cv2.createMergeDebevec()
    hdr = merge.process(images, times, response)
    
    return hdr, response

def create_hdr_robertson(images, times):
    """
    Buat HDR image menggunakan Robertson method.
    """
    print("  Creating HDR with Robertson method...")
    
    calibrate = cv2.createCalibrateRobertson()
    response = calibrate.process(images, times)
    
    merge = cv2.createMergeRobertson()
    hdr = merge.process(images, times, response)
    
    return hdr, response

def tonemap_drago(hdr, gamma=GAMMA, saturation=SATURATION):
    """
    Tone mapping dengan Drago operator (logarithmic).
    """
    tonemap = cv2.createTonemapDrago(gamma=gamma, saturation=saturation)
    ldr = tonemap.process(hdr)
    return np.clip(ldr * 255, 0, 255).astype(np.uint8)

def tonemap_reinhard(hdr, gamma=GAMMA, intensity=0.0, light_adapt=0.8, color_adapt=0.0):
    """
    Tone mapping dengan Reinhard operator (photographic).
    """
    tonemap = cv2.createTonemapReinhard(
        gamma=gamma, 
        intensity=intensity,
        light_adapt=light_adapt,
        color_adapt=color_adapt
    )
    ldr = tonemap.process(hdr)
    return np.clip(ldr * 255, 0, 255).astype(np.uint8)

def tonemap_mantiuk(hdr, gamma=GAMMA, scale=0.7, saturation=SATURATION):
    """
    Tone mapping dengan Mantiuk operator (perceptually uniform).
    """
    tonemap = cv2.createTonemapMantiuk(gamma=gamma, scale=scale, saturation=saturation)
    ldr = tonemap.process(hdr)
    return np.clip(ldr * 255, 0, 255).astype(np.uint8)

def tonemap_simple(hdr, gamma=GAMMA):
    """
    Simple gamma tone mapping.
    """
    tonemap = cv2.createTonemap(gamma=gamma)
    ldr = tonemap.process(hdr)
    return np.clip(ldr * 255, 0, 255).astype(np.uint8)

def plot_response_curve(response, output_path):
    """
    Plot camera response function.
    """
    plt.figure(figsize=(10, 6))
    
    colors = ['b', 'g', 'r']
    labels = ['Blue', 'Green', 'Red']
    
    for i, (color, label) in enumerate(zip(colors, labels)):
        plt.plot(response[:, 0, i], range(256), color=color, label=label)
    
    plt.xlabel('Log Exposure')
    plt.ylabel('Pixel Value')
    plt.title('Camera Response Function')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    print(f"  Response curve saved to: {output_path}")

def create_comparison_figure(images_dict, output_path):
    """
    Buat figure perbandingan hasil tone mapping.
    """
    n = len(images_dict)
    fig, axes = plt.subplots(2, (n+1)//2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (name, img) in enumerate(images_dict.items()):
        if i < len(axes):
            axes[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[i].set_title(name)
            axes[i].axis('off')
    
    # Hide unused axes
    for i in range(len(images_dict), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Comparison figure saved to: {output_path}")

def main():
    """
    Fungsi utama untuk HDR imaging demo.
    """
    # Cetak header awal program
    print("=" * 60)
    # Cetak judul praktikum
    print("HDR IMAGING")
    # Cetak garis pemisah
    print("=" * 60)
    
    # Pastikan folder output tersedia
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Tentukan folder exposure bracket
    hdr_dir = os.path.join(DATA_DIR, "hdr_bracket")
    
    # Informasi proses loading
    print("\nLoading exposure bracket...")
    # Muat images dan exposure times
    images, times = load_exposure_bracket(hdr_dir)
    
    # Validasi ketersediaan exposure
    if images is None or len(images) < 2:
        # Informasi error jika data kurang
        print("\nTidak cukup exposure bracket images!")
        # Instruksi untuk download data
        print("Jalankan download_sample_data.py terlebih dahulu.")
        # Hentikan program
        return
    
    # Tampilkan jumlah exposure
    print(f"\nLoaded {len(images)} exposures")
    # Tampilkan exposure times
    print(f"Exposure times: {times}")
    
    # Lakukan alignment antar exposure
    aligned = align_images(images)
    
    # Cetak garis pemisah proses HDR
    print("\n" + "-" * 40)
    # Buat HDR dengan metode Debevec
    hdr_debevec, response = create_hdr_debevec(aligned, times)
    
    # Plot kurva response camera
    plot_response_curve(response, os.path.join(OUTPUT_DIR, "01_response_curve.png"))
    
    # Bentuk path file HDR
    hdr_path = os.path.join(OUTPUT_DIR, "01_hdr_image.hdr")
    # Simpan HDR ke disk
    cv2.imwrite(hdr_path, hdr_debevec)
    # Konfirmasi lokasi HDR
    print(f"  HDR saved to: {hdr_path}")
    
    # Cetak garis pemisah tone mapping
    print("\n" + "-" * 40)
    # Informasi proses tone mapping
    print("Applying tone mapping operators...")
    
    # Siapkan container hasil
    results = {}
    
    # Terapkan tone mapping sederhana
    results['Simple Gamma'] = tonemap_simple(hdr_debevec)
    # Simpan hasil tone mapping sederhana
    cv2.imwrite(os.path.join(OUTPUT_DIR, "01_tonemap_simple.jpg"), results['Simple Gamma'])
    
    # Terapkan tone mapping Drago
    results['Drago'] = tonemap_drago(hdr_debevec)
    # Simpan hasil Drago
    cv2.imwrite(os.path.join(OUTPUT_DIR, "01_tonemap_drago.jpg"), results['Drago'])
    
    # Terapkan tone mapping Reinhard
    results['Reinhard'] = tonemap_reinhard(hdr_debevec)
    # Simpan hasil Reinhard
    cv2.imwrite(os.path.join(OUTPUT_DIR, "01_tonemap_reinhard.jpg"), results['Reinhard'])
    
    # Terapkan tone mapping Mantiuk
    results['Mantiuk'] = tonemap_mantiuk(hdr_debevec)
    # Simpan hasil Mantiuk
    cv2.imwrite(os.path.join(OUTPUT_DIR, "01_tonemap_mantiuk.jpg"), results['Mantiuk'])
    
    # Tambahkan exposure awal untuk perbandingan
    results['Under-exposed'] = aligned[0]
    # Tambahkan exposure akhir untuk perbandingan
    results['Over-exposed'] = aligned[-1]
    
    # Buat figure perbandingan
    create_comparison_figure(results, os.path.join(OUTPUT_DIR, "01_hdr_comparison.png"))
    
    # Cetak ringkasan
    print("\n" + "=" * 60)
    # Judul ringkasan
    print("SUMMARY")
    # Garis pemisah ringkasan
    print("=" * 60)
    # Tampilkan daftar file output
    print(f"""
HDR processing complete!

Files generated:
  - 01_response_curve.png: Camera response function
  - 01_hdr_image.hdr: HDR radiance map
  - 01_tonemap_simple.jpg: Simple gamma mapping
  - 01_tonemap_drago.jpg: Drago operator
  - 01_tonemap_reinhard.jpg: Reinhard operator
  - 01_tonemap_mantiuk.jpg: Mantiuk operator
  - 01_hdr_comparison.png: Side-by-side comparison

Tips:
  - Drago: Best for natural scenes
  - Reinhard: Best for high contrast
  - Mantiuk: Best for details
""")
    
    # Tampilkan hasil Drago
    cv2.imshow("HDR - Drago", results['Drago'])
    # Tampilkan hasil Reinhard
    cv2.imshow("HDR - Reinhard", results['Reinhard'])
    # Informasi auto-close
    print("\nMenampilkan hasil (akan otomatis tertutup dalam 2 detik)...")
    # Tunggu 2 detik
    cv2.waitKey(2000)
    # Tutup semua window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
