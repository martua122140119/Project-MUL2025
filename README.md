# Animal Sound Detection & AR 🎤🐾

Program untuk mendeteksi suara hewan berdasarkan frekuensi suara yang ditirukan pengguna, kemudian menampilkan gambar hewan yang terdeteksi menggunakan Augmented Reality (AR) sederhana.

## Fitur Utama

* Deteksi suara hewan menggunakan analisis frekuensi (FFT)
* Klasifikasi 3 jenis hewan berdasarkan rentang frekuensi:
  * Anjing: < 200 Hz
  * Kambing: 200-700 Hz 
  * Kucing: > 700 Hz
* Tampilan AR dengan overlay gambar hewan pada feed kamera
* Antarmuka interaktif dengan preview gambar hewan

## Struktur Folder

```
Proyek Tubes/
├── codefinal.py         # Program utama
└── Hewan/
    ├── suara/          # File suara (.wav)
    │   ├── anjing.wav
    │   ├── kucing.wav
    │   └── kambing.wav  
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
   * Preview gambar hewan di bagian atas
   * Feed kamera di bagian bawah
   
3. Kontrol program:
   * Tekan `s` untuk mulai merekam suara (3 detik)
   * Tekan `q` untuk keluar dari tampilan aktif
   * Program akan otomatis mendeteksi dan menampilkan gambar hewan yang sesuai

## Parameter Teknis

* Format Audio:
  * Sample rate: 44100 Hz
  * Channels: 1 (mono)
  * Format: 16-bit integer
  * Chunk size: 1024 samples
  * Durasi rekam: 5 detik

* Deteksi Frekuensi:
  * Menggunakan Fast Fourier Transform (FFT)
  * Threshold frekuensi anjing: < 200 Hz
  * Threshold frekuensi kambing: 200-700 Hz
  * Threshold frekuensi kucing: > 700 Hz

## Catatan Penggunaan

* Pastikan mikrofon terhubung dan berfungsi
* Suara tiruan harus cukup jelas dan stabil
* Hindari noise/suara latar yang mengganggu
* Posisikan wajah dalam frame kamera untuk hasil terbaik
* Program akan menampilkan frekuensi dominan yang terdeteksi

## Troubleshooting

* Jika kamera tidak terdeteksi: Periksa koneksi webcam
* Jika audio tidak terekam: Periksa pengaturan mikrofon
* Jika gambar tidak muncul: Pastikan file .png ada di folder yang benar
* Jika deteksi tidak akurat: Coba suara yang lebih jelas/stabil