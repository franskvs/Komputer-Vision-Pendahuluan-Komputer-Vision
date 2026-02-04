# ============================================================
# PROGRAM: generate_data.py
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi:
#   Membuat data sample untuk praktikum Bab 2
#   (gambar sintetis) agar semua script dapat dijalankan
# ============================================================

import os
from pathlib import Path

import cv2
import numpy as np


# ============================================================
# KONFIGURASI OUTPUT
# ============================================================
ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
VIDEOS_DIR = DATA_DIR / "videos"


# ============================================================
# HELPER
# ============================================================

def ensure_dirs():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def save_image(name, img):
    out_path = IMAGES_DIR / name
    cv2.imwrite(str(out_path), img)
    print(f"[OK] {out_path}")


# ============================================================
# GENERATOR GAMBAR
# ============================================================

def make_portrait():
    """Gambar portret sederhana untuk uji transformasi."""
    h, w = 600, 450
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Background gradient
    for y in range(h):
        img[y, :] = [50 + y // 4, 80 + y // 6, 120 + y // 8]

    # Face circle
    center = (w // 2, h // 2 - 20)
    cv2.circle(img, center, 150, (210, 190, 170), -1)

    # Eyes
    cv2.circle(img, (center[0] - 50, center[1] - 30), 18, (20, 20, 20), -1)
    cv2.circle(img, (center[0] + 50, center[1] - 30), 18, (20, 20, 20), -1)

    # Mouth
    cv2.ellipse(img, (center[0], center[1] + 50), (50, 25), 0, 0, 180, (30, 30, 30), 4)

    # Shirt
    cv2.rectangle(img, (0, h - 180), (w, h), (30, 60, 140), -1)
    cv2.putText(img, "PORTRAIT", (20, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    return img


def make_checkerboard(cols=9, rows=6, square=40):
    """Checkerboard untuk kalibrasi kamera."""
    height = rows * square
    width = cols * square
    img = np.zeros((height, width), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                y1, y2 = i * square, (i + 1) * square
                x1, x2 = j * square, (j + 1) * square
                img[y1:y2, x1:x2] = 255

    img = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=200)
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def make_perspective_document():
    """Dokumen perspektif untuk homography/document scanner."""
    h, w = 700, 900
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Background kayu
    for y in range(h):
        base = 60 + (y // 12)
        img[y, :] = [base + 10, base, base - 10]
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Dokumen (trapesium)
    pts = np.array([
        [180, 80],
        [700, 120],
        [760, 600],
        [140, 640],
    ], dtype=np.int32)

    cv2.fillPoly(img, [pts], (245, 245, 245))
    cv2.polylines(img, [pts], True, (60, 60, 60), 3)

    # Isi dokumen
    for i in range(8):
        y = 180 + i * 45
        x1 = 220 + int((y - 120) * 0.05)
        x2 = 660 + int((y - 120) * 0.08)
        cv2.line(img, (x1, y), (x2, y), (120, 120, 120), 2)

    cv2.putText(img, "DOKUMEN", (300, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (60, 60, 60), 2)

    return img


def make_grid_scene():
    """Grid + shapes untuk uji affine/rotasi."""
    h, w = 500, 700
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Grid
    for x in range(0, w, 50):
        cv2.line(img, (x, 0), (x, h), (40, 40, 40), 1)
    for y in range(0, h, 50):
        cv2.line(img, (0, y), (w, y), (40, 40, 40), 1)

    # Shapes
    cv2.rectangle(img, (120, 120), (320, 320), (255, 255, 255), 2)
    cv2.circle(img, (500, 250), 70, (0, 255, 255), 2)
    cv2.line(img, (120, 320), (320, 120), (255, 0, 0), 2)
    cv2.putText(img, "GRID", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)

    return img


def make_aliasing_pattern():
    """Pola frekuensi tinggi untuk uji aliasing/interpolasi."""
    h, w = 256, 256
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Checker kecil
    for i in range(h):
        for j in range(w):
            if ((i // 4) + (j // 4)) % 2 == 0:
                img[i, j] = [220, 220, 220]
            else:
                img[i, j] = [30, 30, 30]

    cv2.putText(img, "ALIAS", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    return img


# ============================================================
# MAIN
# ============================================================

def main():
    ensure_dirs()

    save_image("portrait.jpg", make_portrait())
    save_image("document.jpg", make_perspective_document())
    save_image("checkerboard.png", make_checkerboard())
    save_image("grid_scene.jpg", make_grid_scene())
    save_image("aliasing_pattern.png", make_aliasing_pattern())

    print("\nSelesai. Data sample untuk Bab 2 sudah dibuat.")


if __name__ == "__main__":
    main()
