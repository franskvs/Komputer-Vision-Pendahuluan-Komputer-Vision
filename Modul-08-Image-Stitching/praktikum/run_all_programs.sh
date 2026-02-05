#!/bin/bash
# Script untuk menjalankan semua program praktikum Bab 08
# Auto-close enabled - semua program akan close otomatis setelah 2 detik

echo "============================================================"
echo "MENJALANKAN SEMUA PROGRAM BAB 08: IMAGE STITCHING"
echo "============================================================"
echo ""

# Pindah ke direktori praktikum
cd "$(dirname "$0")"

# Pastikan data sudah ada
if [ ! -d "data/images" ]; then
    echo "📥 Download sample data dulu..."
    python download_sample_data.py
    echo ""
fi

# Jalankan semua program
echo "🔄 Menjalankan semua program dengan auto-close (2 detik)..."
echo ""

echo "▶️  Program 01: Simple Stitching"
python 01_simple_stitching.py
echo ""

echo "▶️  Program 02: OpenCV Stitcher Class"
python 02_opencv_stitcher.py
echo ""

echo "▶️  Program 03: Blending Comparison"
python 03_blending_comparison.py
echo ""

echo "▶️  Program 04: Multi-Image Panorama"
python 04_multi_image_panorama.py
echo ""

echo "▶️  Program 05: Cylindrical Projection"
python 05_cylindrical_projection.py
echo ""

echo "▶️  Program 06: Realtime Stitching (AUTO MODE)"
python 06_realtime_stitching.py
echo ""

echo "============================================================"
echo "✅ SEMUA PROGRAM SELESAI"
echo "============================================================"
echo ""
echo "📂 Output disimpan di folder: output/"
echo ""
echo "Output yang dihasilkan:"
find output -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | sort
echo ""
echo "Untuk melihat hasil, buka file-file di folder output/"
echo ""
