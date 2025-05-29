# Animal Sound Detection & AR 🎤🐾

Program untuk mendeteksi suara hewan berdasarkan frekuensi suara yang ditirukan pengguna, kemudian menampilkan gambar hewan yang terdeteksi menggunakan Augmented Reality (AR) sederhana.

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
  * Volume minimum (RMS threshold): 700
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