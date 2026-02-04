#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download Sample Data untuk Bab 11: Structure from Motion
=========================================================

Script ini mendownload gambar dan video sampel yang diperlukan
untuk praktikum Structure from Motion dan SLAM.

Data yang didownload:
1. Gambar stereo building/scene
2. Sekuens gambar untuk SfM
3. Video untuk Visual Odometry

Author: Praktikum Computer Vision
"""

import os
import sys
import urllib.request
import ssl
from pathlib import Path
import shutil

# Disable SSL verification untuk menghindari error sertifikat
ssl._create_default_https_context = ssl._create_unverified_context

def download_file(url, filepath):
    """Download file dari URL."""
    print(f"  Downloading: {filepath.name}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"    Warning: Gagal download {url}: {e}")
        return False


def create_sample_stereo_images(output_dir):
    """
    Membuat gambar sampel untuk demo stereo/SfM jika download gagal.
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("OpenCV tidak tersedia untuk membuat gambar dummy")
        return
    
    print("  Membuat gambar sampel...")
    
    # Gambar 1 - scene dengan objek
    img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    img1[:] = (40, 40, 40)  # Background abu-abu gelap
    
    # Tambahkan "building" shapes
    cv2.rectangle(img1, (100, 150), (200, 400), (180, 180, 180), -1)
    cv2.rectangle(img1, (250, 180), (380, 400), (160, 160, 160), -1)
    cv2.rectangle(img1, (420, 120), (550, 400), (140, 140, 140), -1)
    
    # Tambahkan windows
    for x_base in [100, 250, 420]:
        for y in range(180, 380, 50):
            for x in range(x_base + 20, x_base + 80, 30):
                cv2.rectangle(img1, (x, y), (x+20, y+30), (220, 220, 220), -1)
    
    # Tambahkan texture/features untuk matching
    np.random.seed(42)
    for _ in range(100):
        x = np.random.randint(0, 640)
        y = np.random.randint(0, 150)
        cv2.circle(img1, (x, y), 2, (255, 255, 255), -1)
    
    # Ground
    cv2.rectangle(img1, (0, 400), (640, 480), (60, 60, 60), -1)
    
    # Gambar 2 - sedikit berbeda (simulasi kamera bergerak)
    img2 = np.zeros((480, 640, 3), dtype=np.uint8)
    img2[:] = (40, 40, 40)
    
    # Objek dengan offset (parallax)
    cv2.rectangle(img2, (80, 150), (180, 400), (180, 180, 180), -1)
    cv2.rectangle(img2, (225, 180), (355, 400), (160, 160, 160), -1)
    cv2.rectangle(img2, (390, 120), (520, 400), (140, 140, 140), -1)
    
    # Windows dengan offset
    for x_base in [80, 225, 390]:
        for y in range(180, 380, 50):
            for x in range(x_base + 20, x_base + 80, 30):
                cv2.rectangle(img2, (x, y), (x+20, y+30), (220, 220, 220), -1)
    
    # Same sky features
    np.random.seed(42)
    for _ in range(100):
        x = np.random.randint(0, 640) - 5  # Slight offset
        y = np.random.randint(0, 150)
        if 0 <= x < 640:
            cv2.circle(img2, (x, y), 2, (255, 255, 255), -1)
    
    cv2.rectangle(img2, (0, 400), (640, 480), (60, 60, 60), -1)
    
    cv2.imwrite(str(output_dir / "building1.jpg"), img1)
    cv2.imwrite(str(output_dir / "building2.jpg"), img2)
    print("    Created: building1.jpg, building2.jpg")
    
    # Buat sekuens gambar untuk multi-view
    print("  Membuat sekuens multi-view...")
    for i in range(5):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[:] = (40, 40, 40)
        
        offset = i * 15
        cv2.rectangle(img, (100-offset, 150), (200-offset, 400), (180, 180, 180), -1)
        cv2.rectangle(img, (250-offset, 180), (380-offset, 400), (160, 160, 160), -1)
        cv2.rectangle(img, (420-offset, 120), (550-offset, 400), (140, 140, 140), -1)
        
        cv2.imwrite(str(output_dir / f"multiview_{i+1:02d}.jpg"), img)
    print("    Created: multiview_01.jpg to multiview_05.jpg")


def main():
    """Main function."""
    print("="*60)
    print("DOWNLOAD SAMPLE DATA - BAB 11: STRUCTURE FROM MOTION")
    print("="*60)
    
    # Setup directories
    script_dir = Path(__file__).parent.resolve()
    images_dir = script_dir / "praktikum/data" / "images"
    videos_dir = script_dir / "praktikum/data" / "videos"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput directory: {script_dir / 'praktikum/data'}")
    
    # URLs untuk sample images (dari public domain sources)
    image_urls = {
        # Middlebury Stereo Dataset (public)
        "stereo_left.png": "https://vision.middlebury.edu/stereo/data/scenes2014/png/Adirondack/im0.png",
        "stereo_right.png": "https://vision.middlebury.edu/stereo/data/scenes2014/png/Adirondack/im1.png",
    }
    
    print("\n[1] Downloading stereo images...")
    download_success = False
    
    for filename, url in image_urls.items():
        filepath = images_dir / filename
        if download_file(url, filepath):
            download_success = True
    
    # Jika download gagal, buat gambar dummy
    if not download_success:
        print("\n[2] Creating sample images (fallback)...")
        create_sample_stereo_images(images_dir)
    else:
        # Juga buat gambar tambahan
        print("\n[2] Creating additional sample images...")
        create_sample_stereo_images(images_dir)
    
    print("\n[3] Creating output directory...")
    output_dir = script_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"    Created: {output_dir}")
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    
    print("\nFile yang tersedia:")
    for f in sorted(images_dir.glob("*")):
        print(f"  - {f.name}")
    
    print(f"\nTotal: {len(list(images_dir.glob('*')))} files")
    print("\nAnda dapat menjalankan program praktikum sekarang!")


if __name__ == "__main__":
    main()
