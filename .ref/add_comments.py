#!/usr/bin/env python3
"""
Comprehensive inline comment addition for all praktikum files.
This script adds detailed Indonesian comments before every significant code line.
"""

import os
import re
from pathlib import Path

# Comment template dictionary for common operations
COMMENT_TEMPLATES = {
    'print': '# Cetak informasi ke console',
    'cv2.imread': '# Baca gambar dari file',
    'cv2.cvtColor': '# Konversi gambar dari format BGR ke RGB untuk matplotlib',
    'plt.subplots': '# Siapkan kanvas plot untuk menampilkan hasil',
    'plt.suptitle': '# Set judul keseluruhan figure',
    'plt.tight_layout': '# Atur spacing antar subplot',
    'plt.savefig': '# Simpan figure ke file',
    'plt.close': '# Tutup figure untuk menghemat memory',
    'os.path.join': '# Bentuk path lengkap file',
    'os.makedirs': '# Buat folder jika belum ada',
    'cv2.circle': '# Gambar lingkaran pada gambar',
    'cv2.rectangle': '# Gambar persegi panjang pada gambar',
    'cv2.putText': '# Tambahkan teks pada gambar',
    'cv2.warpAffine': '# Terapkan transformasi affine pada gambar',
    'cv2.getRotationMatrix2D': '# Hitung matriks rotasi',
    'cv2.warpPerspective': '# Terapkan transformasi perspektif pada gambar',
    'np.zeros': '# Inisialisasi array numpy dengan nilai nol',
    'np.array': '# Buat array numpy',
    'np.dot': '# Hitung perkalian matriks',
    'np.float32': '# Konversi ke tipe data float32',
    'for i in range': '# Iterasi melalui range',
    'if gambar is None': '# Cek apakah gambar berhasil dimuat',
    'return': '# Kembalikan hasil fungsi',
}

def get_comment_for_line(line_stripped):
    """Get a generic comment for a line based on its content."""
    for keyword, template in COMMENT_TEMPLATES.items():
        if keyword in line_stripped:
            return template
    
    # Generic fallback
    if '=' in line_stripped and 'for' not in line_stripped:
        var_name = line_stripped.split('=')[0].strip()
        return f'# Tentukan nilai untuk {var_name}'
    
    return None

def add_inline_comments_to_file(file_path):
    """Add inline comments to a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        stripped = current_line.strip()
        indent = len(current_line) - len(current_line.lstrip())
        indent_str = ' ' * indent
        
        # Skip empty lines, docstrings, and existing comments
        if not stripped or stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
            new_lines.append(current_line)
            i += 1
            continue
        
        # Skip lines that are just brackets
        if stripped in ['(', ')', '[', ']', '{', '}', ',', ';', 'else:', 'elif ', 'try:', 'except:', 'finally:']:
            new_lines.append(current_line)
            i += 1
            continue
        
        # For lines that look like significant code
        if not current_line.strip().startswith('"') and not current_line.strip().startswith("'"):
            # Check if previous line is a comment
            if not (new_lines and new_lines[-1].strip().startswith('#')):
                comment = get_comment_for_line(stripped)
                if comment:
                    new_lines.append(f"{indent_str}{comment}\n")
        
        new_lines.append(current_line)
        i += 1
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Main execution
if __name__ == "__main__":
    files_dir = Path("/home/sirobo/Documents/Praktikum Komputer Vision/Bab-02-Pembentukan-Citra/praktikum")
    
    # Get all numbered Python files (except 01 which is already done)
    files = sorted([f for f in files_dir.glob("0[2-9]_*.py")] + 
                   [f for f in files_dir.glob("1[0-5]_*.py")])
    
    print(f"Processing {len(files)} files...")
    for file_path in files:
        print(f"  Processing: {file_path.name}")
        # Uncomment to actually process
        # add_inline_comments_to_file(file_path)
    
    print("Done!")
