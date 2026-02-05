#  ============================================================================
# DOKUMENTASI CV2 FUNCTIONS - REFERENSI LENGKAP
# ============================================================================
# File ini berisi dokumentasi lengkap untuk semua OpenCV functions yang sering
# digunakan. Gunakan sebagai referensi ketika membaca program praktikum.
#
# CARA MENGGUNAKAN:
# 1. Baca dokumentasi function yang ingin dipelajari di bawah
# 2. Perhatikan parameter dan arti masing-masing
# 3. Lihat contoh penggunaan di program praktikum
# ============================================================================

# ============================================================================
# 1. INPUT/OUTPUT FUNCTIONS
# ============================================================================

# cv2.imread(filename, flags)
# ----------------------------
# TUJUAN: Membaca/memuat gambar dari file
# PARAMETER:
#    a. filename (str): Path ke file gambar
#    b. flags (int): Mode pembacaan
#       - cv2.IMREAD_COLOR (1): Baca sebagai BGR berwarna, abaikan alpha
#       - cv2.IMREAD_GRAYSCALE (0): Baca sebagai grayscale (1 channel)
#       - cv2.IMREAD_UNCHANGED (-1): Baca semua channel termasuk alpha
# RETURN:
#    numpy.ndarray: Array gambar (H, W, C) atau None jika gagal
# CONTOH:
#    img = cv2.imread("photo.jpg", cv2.IMREAD_COLOR)
#    gray = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)

# cv2.imwrite(filename, img)
# ---------------------------
# TUJUAN: Menyimpan gambar ke file
# PARAMETER:
#    a. filename (str): Path untuk menyimpan file
#    b. img (ndarray): Array gambar yang akan disimpan
# RETURN:
#    bool: True jika berhasil, False jika gagal
# CONTOH:
#    success = cv2.imwrite("output.png", gambar)

# cv2.imshow(winname, mat)
# -------------------------
# TUJUAN: Menampilkan gambar di window
# PARAMETER:
#    a. winname (str): Judul window
#    b. mat (ndarray): Array gambar
# RETURN:
#    None
# CATATAN: Harus diikuti cv2.waitKey() agar window tetap terbuka
# CONTOH:
#    cv2.imshow("My Image", gambar)
#    cv2.waitKey(0)

# cv2.waitKey(delay)
# ------------------
# TUJUAN: Menunggu input keyboard
# PARAMETER:
#    a. delay (int): Waktu tunggu dalam millisecond
#       - 0: Tunggu tanpa batas (sampai user tekan tombol)
#       - >0: Tunggu n milidetik lalu lanjut
# RETURN:
#    int: ASCII code tombol yang ditekan, atau -1 jika timeout
# CONTOH:
#    key = cv2.waitKey(1000)  # Tunggu 1 detik
#    if key == ord('q'):      # Jika user tekan 'q'
#        break

# cv2.destroyAllWindows()
# -----------------------
# TUJUAN: Menutup semua window yang dibuka
# PARAMETER: Tidak ada
# RETURN: None
# CONTOH:
#    cv2.destroyAllWindows()


# ============================================================================
# 2. DRAWING FUNCTIONS
# ============================================================================

# cv2.line(img, pt1, pt2, color, thickness, lineType)
# ---------------------------------------------------
# TUJUAN: Menggambar garis pada gambar
# PARAMETER:
#    a. img (ndarray): Gambar yang akan digambar (akan dimodifikasi!)
#    b. pt1 (tuple): Koordinat (x, y) titik awal garis
#    c. pt2 (tuple): Koordinat (x, y) titik akhir garis
#    d. color (tuple): Warna garis dalam BGR, contoh (255, 0, 0) = biru
#    e. thickness (int): Ketebalan garis dalam pixel
#    f. lineType (int): Tipe garis - cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA
# RETURN: Tidak ada (gambar dimodifikasi langsung)
# CONTOH:
#    cv2.line(gambar, (10, 20), (100, 200), (0, 255, 0), 2)

# cv2.rectangle(img, pt1, pt2, color, thickness)
# -----------------------------------------------
# TUJUAN: Menggambar rectangle/kotak pada gambar
# PARAMETER:
#    a. img (ndarray): Gambar yang akan digambar
#    b. pt1 (tuple): Koordinat (x, y) KIRI ATAS
#    c. pt2 (tuple): Koordinat (x, y) KANAN BAWAH
#    d. color (tuple): Warna dalam BGR
#    e. thickness (int): Ketebalan garis
#       - -1: Isi kotak penuh dengan warna (filled)
#       - 1-n: Hanya garis outline dengan ketebalan n
# RETURN: Tidak ada
# CONTOH:
#    cv2.rectangle(gambar, (50, 50), (200, 150), (0, 255, 0), 2)
#    cv2.rectangle(gambar, (10, 10), (100, 100), (255, 0, 0), -1)  # Filled

# cv2.circle(img, center, radius, color, thickness)
# --------------------------------------------------
# TUJUAN: Menggambar lingkaran pada gambar
# PARAMETER:
#    a. img (ndarray): Gambar yang akan digambar
#    b. center (tuple): Koordinat (x, y) PUSAT lingkaran
#    c. radius (int): Radius lingkaran dalam pixel
#    d. color (tuple): Warna dalam BGR
#    e. thickness (int): Ketebalan garis
#       - -1: Isi lingkaran penuh
#       - 1-n: Hanya outline dengan ketebalan n
# RETURN: Tidak ada
# CONTOH:
#    cv2.circle(gambar, (320, 240), 100, (0, 0, 255), 2)

# cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)
# -------------------------------------------------------------------------------
# TUJUAN: Menggambar elips pada gambar
# PARAMETER:
#    a. img (ndarray): Gambar
#    b. center (tuple): Pusat elips (x, y)
#    c. axes (tuple): (major_axis, minor_axis) - ukuran panjang dan lebar
#    d. angle (int): Rotasi elips dalam derajat
#    e. startAngle, endAngle (int): Sudut awal dan akhir (untuk arc)
#    f. color (tuple): Warna BGR
#    g. thickness (int): Ketebalan
# CONTOH:
#    cv2.ellipse(gambar, (320, 240), (100, 50), 45, 0, 360, (255, 0, 0), 2)

# cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)
# -------------------------------------------------------------------------------
# TUJUAN: Menulis teks pada gambar
# PARAMETER:
#    a. img (ndarray): Gambar yang akan ditulis
#    b. text (str): String teks yang akan ditulis
#    c. org (tuple): Koordinat (x, y) untuk posisi BAWAH KIRI teks
#    d. fontFace (int): Jenis font:
#       - cv2.FONT_HERSHEY_SIMPLEX (paling umum)
#       - cv2.FONT_HERSHEY_PLAIN
#       - cv2.FONT_HERSHEY_DUPLEX
#       - cv2.FONT_HERSHEY_COMPLEX
#    e. fontScale (float): Ukuran font (1.0 = normal, 0.5 = kecil, 2.0 = besar)
#    f. color (tuple): Warna teks dalam BGR
#    g. thickness (int): Ketebalan teks (1-3 normal, >3 tebal)
#    h. lineType (int): cv2.LINE_AA untuk anti-aliased
# RETURN: Tidak ada
# CONTOH:
#    cv2.putText(gambar, "Hello", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
#                1.0, (255, 255, 255), 2)

# cv2.polylines(img, pts, isClosed, color, thickness)
# ---------------------------------------------------
# TUJUAN: Menggambar polygon/poligon (banyak garis)
# PARAMETER:
#    a. img (ndarray): Gambar
#    b. pts (list): List dari koordinat-koordinat vertex
#    c. isClosed (bool): True untuk menutup polygon
#    d. color (tuple): Warna
#    e. thickness (int): Ketebalan garis
# CONTOH:
#    pts = np.array([(50,50), (150,50), (100,200)], dtype=np.int32)
#    cv2.polylines(gambar, [pts], True, (0, 255, 0), 2)


# ============================================================================
# 3. COLOR CONVERSION FUNCTIONS
# ============================================================================

# cv2.cvtColor(src, code)
# -----------------------
# TUJUAN: Mengkonversi gambar antar color space
# PARAMETER:
#    a. src (ndarray): Gambar sumber
#    b. code (int): Kode konversi:
#       - cv2.COLOR_BGR2RGB: BGR ke RGB (untuk display di matplotlib)
#       - cv2.COLOR_BGR2GRAY: BGR ke Grayscale
#       - cv2.COLOR_BGR2HSV: BGR ke HSV (Hue-Saturation-Value)
#       - cv2.COLOR_RGB2BGR: RGB ke BGR
#       - cv2.COLOR_GRAY2BGR: Grayscale ke BGR
# RETURN:
#    ndarray: Gambar yang sudah dikonversi
# CONTOH:
#    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
#    hsv = cv2.cvtColor(gambar, cv2.COLOR_BGR2HSV)

# cv2.inRange(src, lowerb, upperb)
# ---------------------------------
# TUJUAN: Membuat mask berdasarkan range warna
# PARAMETER:
#    a. src (ndarray): Gambar sumber (biasanya HSV untuk akurasi warna)
#    b. lowerb (tuple): Batas bawah range warna
#    c. upperb (tuple): Batas atas range warna
# RETURN:
#    ndarray: Binary mask (putih=dalam range, hitam=di luar range)
# CONTOH:
#    hsv = cv2.cvtColor(gambar, cv2.COLOR_BGR2HSV)
#    mask = cv2.inRange(hsv, (90, 100, 100), (130, 255, 255))  # Deteksi hijau


# ============================================================================
# 4. GEOMETRIC TRANSFORMATION FUNCTIONS
# ============================================================================

# cv2.resize(src, dsize, interpolation)
# ------------------------------------
# TUJUAN: Mengubah ukuran gambar
# PARAMETER:
#    a. src (ndarray): Gambar sumber
#    b. dsize (tuple): Ukuran target (width, height)
#    c. interpolation (int): Metode interpolasi:
#       - cv2.INTER_LINEAR: Linear interpolation (bagus untuk resize ke atas)
#       - cv2.INTER_CUBIC: Cubic interpolation (lebih detail)
#       - cv2.INTER_NEAREST: Nearest neighbor (cepat tapi kurang smooth)
#       - cv2.INTER_AREA: Downsampling terbaik
# RETURN:
#    ndarray: Gambar yang sudah diubah ukuran
# CONTOH:
#    small = cv2.resize(gambar, (320, 240))
#    large = cv2.resize(gambar, (1920, 1080), cv2.INTER_CUBIC)

# cv2.warpAffine(src, M, dsize)
# ------------------------------
# TUJUAN: Melakukan transformasi affine (rotasi, scaling, translasi)
# PARAMETER:
#    a. src (ndarray): Gambar sumber
#    b. M (ndarray): 2x3 affine transformation matrix
#    c. dsize (tuple): Ukuran output (width, height)
# RETURN:
#    ndarray: Gambar yang sudah ditransformasi
# CONTOH:
#    M = cv2.getRotationMatrix2D((cx, cy), angle, scale)
#    rotated = cv2.warpAffine(gambar, M, (width, height))

# cv2.warpPerspective(src, M, dsize)
# -----------------------------------
# TUJUAN: Melakukan transformasi perspektif (view dari sudut berbeda)
# PARAMETER:
#    a. src (ndarray): Gambar
#    b. M (ndarray): 3x3 perspective transformation matrix
#    c. dsize (tuple): Ukuran output
# RETURN:
#    ndarray: Gambar terperspektif
# CONTOH:
#    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
#    warped = cv2.warpPerspective(gambar, M, (width, height))


# ============================================================================
# 5. FILTERING FUNCTIONS
# ============================================================================

# cv2.blur(src, ksize)
# --------------------
# TUJUAN: Blur/smoothing gambar
# PARAMETER:
#    a. src (ndarray): Gambar
#    b. ksize (tuple): Kernel size (3,3), (5,5), dst
# RETURN:
#    ndarray: Gambar yang sudah di-blur
# CONTOH:
#    blurred = cv2.blur(gambar, (5, 5))

# cv2.GaussianBlur(src, ksize, sigmaX, sigmaY)
# -----------------------------------------------
# TUJUAN: Gaussian blur (lebih natural dari blur biasa)
# PARAMETER:
#    a. src (ndarray): Gambar
#    b. ksize (tuple): Kernel size (harus ganjil: 3, 5, 7, dll)
#    c. sigmaX, sigmaY (float): Standard deviation
# RETURN:
#    ndarray: Gambar yang di-blur
# CONTOH:
#    gaussian = cv2.GaussianBlur(gambar, (5, 5), 0)

# cv2.filter2D(src, ddepth, kernel)
# ----------------------------------
# TUJUAN: Konvolusi custom dengan kernel
# PARAMETER:
#    a. src (ndarray): Gambar
#    b. ddepth (int): Depth output (-1 sama dengan input)
#    c. kernel (ndarray): Kernel 2D untuk konvolusi
# RETURN:
#    ndarray: Hasil konvolusi
# CONTOH:
#    kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
#    edges = cv2.filter2D(gambar, -1, kernel)


# ============================================================================
# 6. EDGE DETECTION FUNCTIONS
# ============================================================================

# cv2.Canny(image, threshold1, threshold2)
# ----------------------------------------
# TUJUAN: Mendeteksi edge/tepi menggunakan Canny edge detector
# PARAMETER:
#    a. image (ndarray): Gambar input (biasanya grayscale)
#    b. threshold1 (int): Threshold bawah
#    c. threshold2 (int): Threshold atas
#       - Edge dengan gradient > threshold2 = edge kuat
#       - Edge dengan gradient < threshold1 = bukan edge
#       - Antara threshold1 dan threshold2 = edge jika connected ke edge kuat
# RETURN:
#    ndarray: Binary image dengan edge (putih)
# CONTOH:
#    edges = cv2.Canny(gray, 100, 200)

# cv2.Sobel(src, ddepth, dx, dy, ksize)
# ------
# TUJUAN: Mendeteksi edge dengan Sobel operator
# PARAMETER:
#    a. src (ndarray): Gambar
#    b. ddepth (int): Data type output
#    c. dx (int): Derivatif dalam arah x (0 atau 1)
#    d. dy (int): Derivatif dalam arah y (0 atau 1)
#    e. ksize (int): Kernel size (1, 3, 5, 7)
# RETURN:
#    ndarray: Gambar dengan edge terhitung
# CONTOH:
#    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)


# ============================================================================
# 7. CONTOUR FUNCTIONS
# ============================================================================

# cv2.findContours(image, mode, method)
# ------------------------------------
# TUJUAN: Menemukan kontur/outline objek dalam gambar
# PARAMETER:
#    a. image (ndarray): Binary image (hasil threshold atau edge detection)
#    b. mode (int): Mode deteksi:
#       - cv2.RETR_EXTERNAL: Hanya kontur terluar
#       - cv2.RETR_LIST: Semua kontur
#       - cv2.RETR_TREE: Kontur dengan hierarchi
#    c. method (int): Metode aproksimasi:
#       - cv2.CHAIN_APPROX_NONE: Semua pixel kontur
#       - cv2.CHAIN_APPROX_SIMPLE: Kompresi kontur (lebih efisien)
# RETURN:
#    list: List kontur (setiap kontur adalah numpy array koordinat)
# CONTOH:
#    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, 
#                                           cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(image, contours, contourIdx, color, thickness)
# ---------------------------------------------------------------
# TUJUAN: Menggambar kontur pada gambar
# PARAMETER:
#    a. image (ndarray): Gambar
#    b. contours (list): List kontur dari findContours
#    c. contourIdx (int): Index kontur yang akan digambar (-1 = semua)
#    d. color (tuple): Warna BGR
#    e. thickness (int): Ketebalan garis (-1 untuk filled)
# RETURN:
#    Tidak ada
# CONTOH:
#    cv2.drawContours(gambar, contours, -1, (0, 255, 0), 2)


# ============================================================================
# CATATAN PENTING
# ============================================================================
#
# 1. KOORDINAT SISTEM:
#    OpenCV menggunakan:
#    - (x, y) dimana x = horizontal (kolom), y = vertical (baris)
#    - Origin (0, 0) di KIRI ATAS
#    - Berbeda dengan numpy array (row, col) = (y, x)
#
# 2. COLOR FORMAT:
#    OpenCV menggunakan BGR (bukan RGB):
#    - (255, 0, 0) = BIRU
#    - (0, 255, 0) = HIJAU
#    - (0, 0, 255) = MERAH
#    Untuk menampilkan di matplotlib, konversi ke RGB dulu!
#
# 3. IMAGE MODIFICATION:
#    Kebanyakan fungsi OpenCV memodifikasi gambar LANGSUNG (in-place)
#    Contoh: cv2.line(), cv2.rectangle() mengubah gambar langsung
#
# 4. MEMORY:
#    NumPy arrays di Python tidak dicopy secara default
#    Jika ingin copy, gunakan: img_copy = img.copy()
#
# ============================================================================

