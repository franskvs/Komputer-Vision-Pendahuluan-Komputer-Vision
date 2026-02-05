#!/usr/bin/env python3
"""
Script untuk menambahkan inline comments ke semua file praktikum.
Ini akan menambahkan keterangan (comments) di atas setiap baris kode yang signifikan.
"""

import os
import re
from pathlib import Path

def should_add_comment(line):
    """Cek apakah baris perlu mendapat comment."""
    stripped = line.strip()
    # Skip empty lines, comments, dan def/class statements
    if not stripped or stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        return False
    # Skip lines yang hanya kurung atau operator
    if stripped in ['(', ')', '[', ']', '{', '}', ',', ';']:
        return False
    return True

def get_indent(line):
    """Ambil indentasi dari baris."""
    return len(line) - len(line.lstrip())

def add_inline_comments(file_path):
    """Tambahkan inline comments ke file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        indent = get_indent(line)
        indent_str = ' ' * indent
        
        # Jika baris saat ini adalah def statement, cek apakah sudah ada keterangan
        if line.strip().startswith('def '):
            # Cek apakah baris sebelumnya adalah keterangan
            if new_lines and '# Keterangan:' not in new_lines[-1]:
                # Tambahkan keterangan default
                func_name = line.strip().split('(')[0].replace('def ', '').replace('_', ' ').title()
                new_lines.append(f"{indent_str}# Keterangan: {func_name}.\n")
            new_lines.append(line)
        elif should_add_comment(line):
            # Cek apakah baris sebelumnya sudah comment
            if new_lines and not new_lines[-1].strip().startswith('#'):
                # Buat comment berdasarkan konten
                comment = generate_comment(line.strip(), indent_str)
                if comment:
                    new_lines.append(comment)
            new_lines.append(line)
        else:
            new_lines.append(line)
        
        i += 1
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Processed: {file_path}")

def generate_comment(code_line, indent_str):
    """Generate sebuah comment yang relevan untuk kode."""
    # Ini adalah placeholder - dalam praktiknya, kita perlu comment manual yang relevan
    # Untuk sekarang, kita skip auto-generation
    return None

# Main
if __name__ == "__main__":
    files_dir = Path("/home/sirobo/Documents/Praktikum Komputer Vision/Bab-02-Pembentukan-Citra/praktikum")
    
    files = sorted(files_dir.glob("0*_*.py"))
    
    for file_path in files:
        if file_path.name not in ['01_translasi.py']:  # Skip already processed
            print(f"Processing: {file_path.name}")
            # add_inline_comments(file_path)
    
    print("\nDone!")
