#!/usr/bin/env python3
"""
Add inline comments to all remaining practical files (03-15).
This script reads each file and adds descriptive comments before significant code lines.
"""

import os
import re
from pathlib import Path

# Dictionary of patterns to add comments for common operations
PATTERNS_TO_COMMENT = {
    r'^\s*gambar\s*=\s*np\.zeros': 'Inisialisasi kanvas gambar kosong (hitam) dengan dimensi tertentu',
    r'^\s*for\s+i\s+in\s+range': 'Iterasi melalui range untuk pemrosesan',
    r'^\s*cv2\.rectangle': 'Gambar persegi panjang pada gambar',
    r'^\s*cv2\.circle': 'Gambar lingkaran pada gambar',
    r'^\s*cv2\.putText': 'Tambahkan teks pada gambar',
    r'^\s*cv2\.line': 'Gambar garis pada gambar',
    r'^\s*cv2\.imread': 'Baca gambar dari file',
    r'^\s*cv2\.resize': 'Resize gambar ke ukuran baru dengan metode interpolasi tertentu',
    r'^\s*cv2\.warpAffine': 'Terapkan transformasi affine pada gambar',
    r'^\s*cv2\.warpPerspective': 'Terapkan transformasi perspektif pada gambar',
    r'^\s*cv2\.getRotationMatrix2D': 'Hitung matriks rotasi 2D',
    r'^\s*cv2\.getPerspectiveTransform': 'Hitung matriks transformasi perspektif',
    r'^\s*cv2\.cvtColor': 'Konversi gambar dari format BGR ke RGB untuk matplotlib',
    r'^\s*plt\.subplots': 'Siapkan kanvas plot untuk menampilkan hasil',
    r'^\s*plt\.savefig': 'Simpan figure ke file dengan kualitas DPI tertentu',
    r'^\s*plt\.close': 'Tutup figure untuk menghemat memory',
    r'^\s*print': 'Cetak informasi ke console',
    r'^\s*if\s+.*\s+is\s+None': 'Cek apakah variabel kosong/None',
    r'^\s*return': 'Kembalikan hasil dari fungsi',
}

def get_indent(line):
    """Get indentation of a line."""
    return len(line) - len(line.lstrip())

def should_add_comment_before(line, prev_line):
    """Check if a comment should be added before this line."""
    stripped = line.strip()
    
    # Skip empty lines and lines that are just brackets
    if not stripped or stripped in ['(', ')', '[', ']', '{', '}']:
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
    
    return True

def get_comment_for_line(line):
    """Generate a comment for a line based on patterns."""
    for pattern, comment in PATTERNS_TO_COMMENT.items():
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
    
    # Get all files from 03 to 15
    files_to_process = sorted([
        f for f in base_dir.glob("0[3-9]_*.py")
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
