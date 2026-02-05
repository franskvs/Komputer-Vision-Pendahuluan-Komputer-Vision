#!/usr/bin/env python3
"""
Enhanced inline comment addition for all practical files.
This version adds more comprehensive comments to code blocks.
"""

import os
import re
from pathlib import Path

# Extended dictionary with more specific patterns
COMMENT_RULES = [
    # Control flow
    (r'^\s*if\s+.*\s+is\s+None\s*:', 'Cek apakah variabel kosong/None'),
    (r'^\s*if\s+not\s+.*:\s*$', 'Cek kondisi logis'),
    (r'^\s*if\s+.*\.shape', 'Cek dimensi array/gambar'),
    (r'^\s*for\s+\w+\s+in\s+range\(', 'Iterasi melalui range'),
    (r'^\s*while\s+', 'Loop while untuk proses berulang'),
    
    # Array/Matrix operations
    (r'^\s*\w+\s*=\s*np\.zeros', 'Inisialisasi array numpy dengan nilai nol'),
    (r'^\s*\w+\s*=\s*np\.eye', 'Buat matriks identitas'),
    (r'^\s*\w+\s*=\s*np\.array', 'Buat array numpy dari data'),
    (r'^\s*\w+\s*=\s*np\.dot\(', 'Hitung perkalian matriks/dot product'),
    (r'^\s*\w+\s*=.*np\.linalg\.norm', 'Hitung norma/magnitude vektor'),
    (r'^\s*\w+\s*=.*np\.radians', 'Konversi derajat ke radian'),
    (r'^\s*\w+\s*=.*np\.degrees', 'Konversi radian ke derajat'),
    
    # Image operations
    (r'^\s*\w+\s*=\s*cv2\.imread', 'Baca gambar dari file'),
    (r'^\s*\w+\s*=\s*cv2\.resize', 'Resize gambar ke ukuran baru'),
    (r'^\s*\w+\s*=\s*cv2\.cvtColor', 'Konversi gambar ke format warna berbeda'),
    (r'^\s*cv2\.rectangle', 'Gambar persegi panjang pada gambar'),
    (r'^\s*cv2\.circle', 'Gambar lingkaran pada gambar'),
    (r'^\s*cv2\.line', 'Gambar garis pada gambar'),
    (r'^\s*cv2\.putText', 'Tambahkan teks pada gambar'),
    (r'^\s*cv2\.drawContours', 'Gambar kontur pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.warpAffine', 'Terapkan transformasi affine pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.warpPerspective', 'Terapkan transformasi perspektif pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.getRotationMatrix2D', 'Hitung matriks rotasi 2D'),
    (r'^\s*\w+\s*=\s*cv2\.getPerspectiveTransform', 'Hitung matriks transformasi perspektif'),
    (r'^\s*\w+\s*=\s*cv2\.adaptiveThreshold', 'Terapkan adaptive thresholding pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.threshold', 'Terapkan thresholding pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.filter2D', 'Terapkan filter konvolusi pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.Canny', 'Deteksi edge menggunakan algoritma Canny'),
    (r'^\s*\w+\s*=\s*cv2\.findContours', 'Temukan kontur pada gambar'),
    (r'^\s*\w+\s*=\s*cv2\.createCLAHE', 'Buat objek CLAHE untuk enhancement'),
    
    # Matrix/Matrix operations
    (r'^\s*\w+\s*=\s*np\.linalg\.inv', 'Hitung invers matriks'),
    (r'^\s*\w+\s*=\s*np\.linalg\.eig', 'Hitung eigenvalue dan eigenvector'),
    (r'^\s*\w+\s*\+=', 'Tambahkan nilai ke variabel'),
    (r'^\s*\w+\s*\*=', 'Kalikan variabel dengan nilai'),
    (r'^\s*\w+\s*=\s*\w+\.copy', 'Buat salinan dari array/gambar'),
    
    # Plotting
    (r'^\s*fig,\s*axes\s*=\s*plt\.subplots', 'Siapkan kanvas plot untuk menampilkan hasil'),
    (r'^\s*plt\.imshow\(', 'Tampilkan gambar pada plot'),
    (r'^\s*plt\.savefig', 'Simpan figure ke file dengan kualitas DPI tertentu'),
    (r'^\s*plt\.close\(', 'Tutup figure untuk menghemat memory'),
    (r'^\s*plt\.title\(', 'Set judul pada subplot'),
    (r'^\s*plt\.suptitle', 'Set judul keseluruhan figure'),
    (r'^\s*plt\.tight_layout', 'Atur spacing antar subplot'),
    (r'^\s*axes\[.*\]\.imshow', 'Tampilkan gambar pada subplot tertentu'),
    (r'^\s*axes\[.*\]\.set_title', 'Set judul untuk subplot'),
    (r'^\s*axes\[.*\]\.axis\(', 'Nonaktifkan atau atur axis pada subplot'),
    
    # File operations
    (r'^\s*path.*=\s*os\.path\.join', 'Bentuk path lengkap file'),
    (r'^\s*os\.makedirs', 'Buat folder jika belum ada'),
    
    # Output
    (r'^\s*print\(', 'Cetak informasi ke console'),
    (r'^\s*return\s+', 'Kembalikan hasil dari fungsi'),
]

def get_indent(line):
    """Get indentation of a line."""
    return len(line) - len(line.lstrip())

def should_add_comment_before(line, prev_line):
    """Check if a comment should be added before this line."""
    stripped = line.strip()
    
    # Skip empty lines and lines that are just brackets
    if not stripped or stripped in ['(', ')', '[', ']', '{', '}', ',', ';']:
        return False
    
    # Skip if it's already a comment
    if stripped.startswith('#'):
        return False
    
    # Skip docstring markers
    if stripped.startswith('"""') or stripped.startswith("'''"):
        return False
    
    # Skip if previous line is already a comment
    if prev_line and prev_line.strip().startswith('#'):
        return False
    
    # Don't comment lines that are part of multi-line statements
    if '\\' in line:
        return False
    
    return True

def get_comment_for_line(line):
    """Generate a comment for a line based on patterns."""
    for pattern, comment in COMMENT_RULES:
        if re.match(pattern, line):
            return comment
    return None

def add_comments_to_file(file_path):
    """Add inline comments to a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    prev_line = None
    
    for i, line in enumerate(lines):
        # Check if we should add a comment before this line
        if should_add_comment_before(line, prev_line):
            indent = get_indent(line)
            indent_str = ' ' * indent
            
            comment = get_comment_for_line(line.lstrip())
            if comment:
                new_lines.append(f"{indent_str}# {comment}\n")
        
        new_lines.append(line)
        prev_line = line
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return len(new_lines)

# Main
if __name__ == "__main__":
    base_dir = Path("/home/sirobo/Documents/Praktikum Komputer Vision/Bab-02-Pembentukan-Citra/praktikum")
    
    # Process all files
    files_to_process = sorted([
        f for f in base_dir.glob("0[1-9]_*.py")
    ] + [
        f for f in base_dir.glob("1[0-5]_*.py")
    ])
    
    print(f"Processing {len(files_to_process)} files...")
    for file_path in files_to_process:
        try:
            lines_count = add_comments_to_file(file_path)
            print(f"✓ {file_path.name:30} - {lines_count} lines processed")
        except Exception as e:
            print(f"✗ {file_path.name:30} - Error: {e}")
    
    print("\nAll files processed successfully!")
