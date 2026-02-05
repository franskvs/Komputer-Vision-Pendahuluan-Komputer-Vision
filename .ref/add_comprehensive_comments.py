#!/usr/bin/env python3
"""
Script untuk menambahkan komentar comprehensive ke setiap baris signifikan
di semua file praktikum. Fokus pada penjelasan parameter dan operasi.
"""

import re
import os
from pathlib import Path

# Dictionary berisi penjelasan untuk setiap operasi penting
EXPLANATION_MAP = {
    # OpenCV functions
    'cv2.imread': '# Baca gambar dari file, return BGR image array',
    'cv2.imshow': '# Tampilkan gambar di window',
    'cv2.waitKey': '# Tunggu input keyboard (1ms per iterasi)',
    'cv2.destroyAllWindows': '# Tutup semua window',
    'cv2.cvtColor': '# Konversi format warna (BGR ke RGB, dll)',
    'cv2.resize': '# Ubah ukuran gambar ke resolusi baru',
    'cv2.rectangle': '# Gambar persegi panjang pada gambar',
    'cv2.circle': '# Gambar lingkaran pada gambar',
    'cv2.putText': '# Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)',
    'cv2.line': '# Gambar garis pada gambar',
    'cv2.drawContours': '# Gambar outline kontur pada gambar',
    'cv2.warpAffine': '# Terapkan transformasi affine (rotasi, translasi, skew)',
    'cv2.warpPerspective': '# Terapkan transformasi perspektif',
    'cv2.getRotationMatrix2D': '# Hitung matriks rotasi 2D',
    'cv2.getPerspectiveTransform': '# Hitung matriks transformasi perspektif',
    'cv2.threshold': '# Binerisasi gambar berdasarkan threshold nilai pixel',
    'cv2.Canny': '# Deteksi tepi menggunakan metode Canny',
    'cv2.findContours': '# Cari semua kontur/outline objek di gambar',
    'cv2.HoughLines': '# Deteksi garis lurus menggunakan Hough Transform',
    'cv2.HoughCircles': '# Deteksi lingkaran menggunakan Hough Circle Detection',
    'cv2.GaussianBlur': '# Blur gambar untuk mengurangi noise',
    'cv2.medianBlur': '# Median blur untuk menghilangkan salt-and-pepper noise',
    'cv2.morphologyEx': '# Operasi morfologi (erosi, dilasi, opening, closing)',
    'cv2.dnn.readNetFromDarknet': '# Baca model YOLO dari file .cfg dan .weights',
    'cv2.dnn.readNetFromCaffe': '# Baca model Caffe dari file .prototxt dan .caffemodel',
    'cv2.dnn.readNetFromTensorflow': '# Baca model TensorFlow dari file .pb',
    'cv2.dnn.blobFromImage': '# Konversi gambar ke blob untuk neural network',
    
    # Numpy operations
    'np.array': '# Buat array numpy dari list/data',
    'np.zeros': '# Buat array numpy penuh dengan nilai 0',
    'np.ones': '# Buat array numpy penuh dengan nilai 1',
    'np.random.randint': '# Generate random integer dalam range tertentu',
    'np.dot': '# Hitung dot product / matrix multiplication',
    'np.linalg.inv': '# Hitung inverse matriks',
    'np.linalg.solve': '# Selesaikan sistem persamaan linear',
    'np.mean': '# Hitung rata-rata dari array',
    'np.std': '# Hitung standard deviation dari array',
    'np.reshape': '# Ubah shape array tanpa mengubah data',
    'np.concatenate': '# Gabung beberapa array menjadi satu',
    'np.transpose': '# Transpose matriks/array',
    'np.clip': '# Batasi nilai array antara min dan max',
    'np.argmax': '# Cari index dari nilai maksimum',
    'np.where': '# Cari index dimana kondisi bernilai True',
    
    # Matplotlib operations
    'plt.subplot': '# Buat subplot di grid figure',
    'plt.imshow': '# Tampilkan gambar di subplot',
    'plt.plot': '# Plot kurva/garis di subplot',
    'plt.scatter': '# Plot scatter plot di subplot',
    'plt.histogram': '# Plot histogram di subplot',
    'plt.title': '# Set judul untuk subplot',
    'plt.xlabel': '# Set label untuk sumbu X',
    'plt.ylabel': '# Set label untuk sumbu Y',
    'plt.legend': '# Tampilkan legend untuk plot',
    'plt.tight_layout': '# Atur spacing otomatis antar subplot',
    'plt.savefig': '# Simpan figure ke file gambar',
    'plt.show': '# Tampilkan semua figure yang telah dibuat',
    'plt.close': '# Tutup figure untuk menghemat memory',
    
    # Deep Learning operations
    'torch.tensor': '# Buat tensor PyTorch dari data',
    'tf.keras.models.load_model': '# Load model TensorFlow/Keras dari file',
    'model.predict': '# Lakukan inference pada input data',
    'model.fit': '# Train model dengan data training dan validation',
    'YOLO': '# Load YOLOv8 model untuk object detection',
    'model.predict': '# Jalankan inference YOLOv8 pada gambar',
    
    # Common patterns
    'for ': '# Iterasi/loop melalui elemen dalam koleksi',
    'if ': '# Conditional statement - eksekusi jika kondisi True',
    'while ': '# Loop berulang selama kondisi bernilai True',
    'try:': '# Blok try-except untuk error handling',
    'except': '# Tangkap exception jika ada error di blok try',
    'with open': '# Buka file dengan context manager (otomatis close)',
    'import ': '# Import library/module untuk digunakan',
    'def ': '# Definisi function dengan nama dan parameter',
    'class ': '# Definisi class untuk membuat object',
    'return ': '# Return value dari function',
    '=': '# Assignment - set nilai ke variabel',
}

def add_detailed_comment(code_line):
    """
    Tambahkan komentar detail berdasarkan operasi di kode.
    """
    stripped = code_line.strip()
    
    # Skip empty lines dan comments yang sudah ada
    if not stripped or stripped.startswith('#'):
        return None
    
    # Check setiap pattern di EXPLANATION_MAP
    for pattern, explanation in EXPLANATION_MAP.items():
        if pattern in stripped:
            return explanation
    
    # Untuk cv2.putText khusus, berikan penjelasan parameter
    if 'cv2.putText' in stripped:
        return '# cv2.putText(image, text, position, font, fontScale, color, thickness)'
    
    return None

def get_indentation(line):
    """Get indentation level dari baris."""
    return len(line) - len(line.lstrip())

def add_comments_to_file(file_path):
    """Add comprehensive comments ke file Python."""
    print(f"Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        print(f"  ERROR: Tidak bisa baca file")
        return False
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        stripped = current_line.strip()
        indent = get_indentation(current_line)
        indent_str = ' ' * indent
        
        # Always keep current line
        add_comment = False
        
        # Skip docstrings, comments, dan empty lines
        if not stripped or stripped.startswith('#') or \
           stripped.startswith('"""') or stripped.startswith("'''"):
            new_lines.append(current_line)
            i += 1
            continue
        
        # Check if previous line is a comment (to avoid duplication)
        has_previous_comment = False
        if new_lines:
            prev_line = new_lines[-1].strip()
            if prev_line.startswith('#'):
                has_previous_comment = True
        
        # Add comment if needed
        if not has_previous_comment and stripped not in ['(', ')', '[', ']', '{', '}']:
            comment = add_detailed_comment(stripped)
            if comment:
                new_lines.append(f"{indent_str}{comment}\n")
                add_comment = True
        
        new_lines.append(current_line)
        i += 1
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"  ✓ Added comments successfully")
    return True

def main():
    """Process semua file praktikum di Bab-05-Deep-Learning."""
    base_dir = Path("/home/sirobo/Documents/Praktikum Komputer Vision/Bab-05-Deep-Learning/praktikum")
    
    if not base_dir.exists():
        print(f"Directory tidak ditemukan: {base_dir}")
        return
    
    # Get semua Python files
    python_files = sorted(base_dir.glob("*.py"))
    
    print(f"Found {len(python_files)} Python files")
    print("=" * 70)
    
    success_count = 0
    for file_path in python_files:
        if add_comments_to_file(file_path):
            success_count += 1
    
    print("=" * 70)
    print(f"✓ Successfully processed {success_count}/{len(python_files)} files")

if __name__ == "__main__":
    main()
