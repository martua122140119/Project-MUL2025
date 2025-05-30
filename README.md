# Animal Sound Detection & AR 🎤🐾

> Proyek Multimedia 2025: Sistem Deteksi Suara Hewan dengan Augmented Reality

Sistem interaktif yang memungkinkan pengguna untuk menirukan suara hewan dan mendapatkan feedback visual melalui Augmented Reality. Program menggunakan analisis frekuensi FFT untuk mengklasifikasikan suara dan menampilkan gambar hewan yang sesuai dalam tampilan AR real-time.

Video Demo : [Video Demo](https://drive.google.com/file/d/15ly4UvXe3HkUlfBYv3_hNZ6Eii_Z3cIk/view?usp=sharing)
## Tim Pengembang

| Nama | NIM | GitHub |
|------|-----|--------|
| Martua Kevin A.M.H.Lubis | 122140119 | [@martua122140119](http://github.com/martua122140119) |
| Dyo Dwi Carol Bukit | 122140145 | [@DyoBukit](https://github.com/DyoBukit) |
| Rafelina Octa Ladelavia| 122140082 | [@Rafelinaoctaa](https://github.com/Rafelinaoctaa) |

## Progress Mingguan

### Week 1 (5 - 10 Mei 2025)
-  Membuat repositoty pada Github dan mengundang anggota tim dan dosen.

### Week 2 (12 -17 Mei 2025)
-  Membuat struktur folder untuk aset dan kode pertama (Dyo)
-  Implementasi analisis fft untuk deteksi frekuensi audio hewan

### Week 3 (19 - 24 Mei 2025)
-  Menambahkan kode kedua menggunakan mfcc (Kevin)
-  Implementasi menggunakan mfcc untuk deteksi suara hewan
-  Pengujian: Akurasi analisis frekuensi dengan menggunakan dataset suara hewan

### Week 4 (22-30 Mei 2025)
-  Membuat kode 3 menggunakan fft (Rafelina)
-  Mengganti fitur yang digunakan dari mfcc ke fft
-  Bug fixing dan optimasi performa
-  Dokumentasi dan finalisasi

## Fitur Utama

* Deteksi suara hewan menggunakan analisis frekuensi (FFT)
* Klasifikasi 3 jenis hewan berdasarkan rentang frekuensi:
  * Anjing: < 300 Hz
  * Kambing: 300-1000 Hz 
  * Kucing: > 1000 Hz
* Deteksi volume suara menggunakan RMS
* Tampilan AR dengan overlay gambar hewan pada feed kamera
* Antarmuka interaktif dengan preview gambar hewan

## Struktur Folder

```
Proyek Tubes/
├── codefinal.py         # Program utama
└── Hewan/
    └── gambar/         # File gambar (.png)
        ├── anjing.png
        ├── kucing.png
        └── kambing.png
```

## Dependencies

Program membutuhkan library Python berikut:
```bash
pip install opencv-python numpy pyaudio
```

## Installation

Install all required dependencies using:
```bash
pip install -r requirements.txt
```

## Cara Penggunaan

1. Jalankan program:
   ```bash
   python codefinal.py
   ```

2. Tampilan awal akan menunjukkan:
   * Preview ketiga gambar hewan di bagian atas
   * Feed kamera di bagian bawah
   
3. Kontrol program:
   * Tekan `s` untuk mulai merekam suara (3 detik)
   * Tekan `q` untuk keluar dari tampilan aktif
   * Program akan mendeteksi volume dan frekuensi suara

## Parameter Teknis

* Format Audio:
  * Sample rate: 44100 Hz (CD quality)
  * Channels: 1 (mono)
  * Format: 16-bit integer
  * Chunk size: 1024 samples
  * Durasi rekam: 3 detik

* Deteksi Suara:
  * Volume minimum (RMS threshold): 500
  * Threshold frekuensi anjing: < 300 Hz
  * Threshold frekuensi kambing: 300-1000 Hz
  * Threshold frekuensi kucing: > 1000 Hz

## Catatan Penggunaan

* Pastikan mikrofon terhubung dan berfungsi
* Suara harus cukup keras (di atas threshold RMS)
* Volume terlalu rendah akan meminta pengulangan
* Posisikan wajah dalam frame kamera untuk hasil terbaik
* Program menampilkan nilai RMS dan hasil deteksi hewan

## Troubleshooting

* Jika kamera tidak terdeteksi: Periksa koneksi webcam
* Jika audio terlalu pelan: Tingkatkan volume input mikrofon
* Jika gambar tidak muncul: Pastikan file .png ada di folder Hewan/gambar/
* Jika deteksi tidak akurat: Coba suara yang lebih keras dan jelas