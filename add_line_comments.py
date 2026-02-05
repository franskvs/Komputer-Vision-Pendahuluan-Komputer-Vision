#!/usr/bin/env python3
"""
Tambahkan keterangan (komentar) di atas setiap baris kode.
Fokus pada file praktikum Bab-03.
"""

from pathlib import Path
import re

SPECIAL_COMMENT_MAP = {
    "cv2.putText": "# Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).",
    "cv2.imread": "# Keterangan: Baca gambar dari file ke array.",
    "cv2.cvtColor": "# Keterangan: Konversi ruang warna gambar.",
    "cv2.resize": "# Keterangan: Ubah ukuran gambar.",
    "cv2.imwrite": "# Keterangan: Simpan gambar ke file.",
    "cv2.GaussianBlur": "# Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.",
    "cv2.Sobel": "# Keterangan: Hitung gradien Sobel untuk deteksi tepi.",
    "cv2.Laplacian": "# Keterangan: Hitung Laplacian untuk deteksi tepi.",
    "cv2.warpAffine": "# Keterangan: Terapkan transformasi affine pada gambar.",
    "cv2.warpPerspective": "# Keterangan: Terapkan transformasi perspektif pada gambar.",
    "cv2.pyrDown": "# Keterangan: Downsample gambar untuk membangun pyramid.",
    "cv2.pyrUp": "# Keterangan: Upsample gambar untuk membangun pyramid.",
    "cv2.remap": "# Keterangan: Remap koordinat piksel untuk warping.",
    "np.zeros": "# Keterangan: Inisialisasi array bernilai nol.",
    "np.ones": "# Keterangan: Inisialisasi array bernilai satu.",
    "np.arange": "# Keterangan: Buat range angka berjarak tetap.",
    "np.linspace": "# Keterangan: Buat range angka berjarak linier.",
    "np.meshgrid": "# Keterangan: Buat grid koordinat 2D.",
    "plt.figure": "# Keterangan: Buat kanvas figure untuk plotting.",
    "plt.subplot": "# Keterangan: Pilih area subplot untuk menampilkan hasil.",
    "plt.imshow": "# Keterangan: Tampilkan gambar pada kanvas.",
    "plt.title": "# Keterangan: Set judul subplot.",
    "plt.axis": "# Keterangan: Atur tampilan sumbu.",
    "plt.tight_layout": "# Keterangan: Rapikan jarak antar subplot.",
    "plt.savefig": "# Keterangan: Simpan hasil visualisasi ke file.",
    "plt.close": "# Keterangan: Tutup figure untuk menghemat memori.",
}


def is_code_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    return True


def is_triple_quote_line(line):
    return "'''" in line or '"""' in line


def generate_comment(line):
    stripped = line.strip()

    for key, comment in SPECIAL_COMMENT_MAP.items():
        if key in stripped:
            return comment

    if stripped.startswith("import "):
        module = stripped.replace("import ", "", 1)
        return f"# Keterangan: Impor modul {module}."

    if stripped.startswith("from ") and " import " in stripped:
        module = stripped.split(" import ")[0].replace("from ", "")
        return f"# Keterangan: Impor komponen dari modul {module}."

    if stripped.startswith("def "):
        name = stripped.split("(")[0].replace("def ", "")
        return f"# Keterangan: Definisikan fungsi {name}."

    if stripped.startswith("class "):
        name = stripped.split(":")[0].replace("class ", "")
        return f"# Keterangan: Definisikan kelas {name}."

    if stripped.startswith("for "):
        header = stripped.replace(":", "")
        return f"# Keterangan: Mulai loop dengan {header}."

    if stripped.startswith("while "):
        header = stripped.replace(":", "")
        return f"# Keterangan: Mulai loop while dengan kondisi {header[6:]}."

    if stripped.startswith("if "):
        header = stripped.replace(":", "")
        return f"# Keterangan: Cek kondisi {header[3:]}."

    if stripped.startswith("elif "):
        header = stripped.replace(":", "")
        return f"# Keterangan: Cek kondisi alternatif {header[5:]}."

    if stripped.startswith("else:"):
        return "# Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi."

    if stripped.startswith("try:"):
        return "# Keterangan: Mulai blok try untuk menangani error."

    if stripped.startswith("except"):
        return "# Keterangan: Tangani error pada blok except."

    if stripped.startswith("finally:"):
        return "# Keterangan: Jalankan blok finally setelah try/except."

    if stripped.startswith("return"):
        return "# Keterangan: Kembalikan hasil dari fungsi."

    if "=" in stripped and "==" not in stripped and "!=" not in stripped:
        left = stripped.split("=")[0].strip()
        left = re.sub(r"\s+", " ", left)
        if "," in left:
            return f"# Keterangan: Inisialisasi beberapa variabel ({left})."
        return f"# Keterangan: Inisialisasi atau perbarui variabel {left}."

    if stripped.endswith(":"):
        return "# Keterangan: Mulai blok kode baru."

    return "# Keterangan: Jalankan perintah berikut."


def add_comments_to_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_triple = False

    for line in lines:
        if is_triple_quote_line(line):
            # Toggle state ketika ada triple quote
            in_triple = not in_triple
            new_lines.append(line)
            continue

        if in_triple:
            new_lines.append(line)
            continue

        if not is_code_line(line):
            new_lines.append(line)
            continue

        # Jika baris sebelumnya sudah ada keterangan, jangan tambahkan lagi
        if new_lines and new_lines[-1].lstrip().startswith("# Keterangan:"):
            new_lines.append(line)
            continue

        indent = " " * (len(line) - len(line.lstrip()))
        comment = generate_comment(line)
        new_lines.append(f"{indent}{comment}\n")
        new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    base_dir = Path("/home/sirobo/Documents/Praktikum Komputer Vision/Bab-03-Pemrosesan-Citra/praktikum")
    files = sorted(list(base_dir.glob("0*_*.py")) + list(base_dir.glob("1*_*.py")))

    for file_path in files:
        add_comments_to_file(file_path)
        print(f"✓ Updated comments: {file_path.name}")
