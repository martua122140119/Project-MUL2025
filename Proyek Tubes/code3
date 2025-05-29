import cv2
import pyaudio
import numpy as np
import time

# Pengaturan Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3

# Rentang frekuensi (perkirakan)
FREQ_ANJING_MAX = 200
FREQ_KAMBING_MAX = 700

def tampil_awal_dengan_gambar(cap):
    """Tampilkan gambar hewan dan kamera. Tekan 's'=start, 'm'=ulang, 'q'=keluar."""
    ukuran_gambar = (150, 150)
    anjing = cv2.resize(cv2.imread("Hewan/gambar/anjing.png"), ukuran_gambar)
    kambing = cv2.resize(cv2.imread("Hewan/gambar/kambing.png"), ukuran_gambar)
    kucing = cv2.resize(cv2.imread("Hewan/gambar/kucing.png"), ukuran_gambar)
    barisan_gambar = np.hstack((anjing, kambing, kucing))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca kamera.")
            return "exit"

        frame_resized = cv2.resize(frame, (barisan_gambar.shape[1], 300))
        tampilan = np.vstack((barisan_gambar, frame_resized))
        cv2.imshow("Tekan 's'=mulai, 'm'=ulang, 'q'=keluar", tampilan)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            return "start"
        elif key == ord('m'):
            return "restart"
        elif key == ord('q'):
            return "exit"

def rekam_dan_analisis(cap):
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
    out_video = cv2.VideoWriter('output_video.avi',
                                cv2.VideoWriter_fourcc(*'XVID'),
                                fps, (frame_width, frame_height))

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("🎥 Merekam selama 5 detik...")
    frames_audio = []
    start_time = time.time()

    while (time.time() - start_time) < RECORD_SECONDS:
        ret, frame = cap.read()
        if ret:
            out_video.write(frame)
            cv2.imshow('Merekam... Tekan Q untuk stop', frame)
        try:
            data_audio = stream.read(CHUNK, exception_on_overflow=False)
            frames_audio.append(data_audio)
        except:
            print("Overflow audio.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("❌ Rekaman dihentikan.")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()
    out_video.release()
    cv2.destroyAllWindows()

    if not frames_audio:
        print("⚠ Tidak ada data audio.")
        return

    audio_np = np.frombuffer(b''.join(frames_audio), dtype=np.int16)
    fft_data = np.fft.fft(audio_np)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.where(freqs > 0)
    fft_positive = np.abs(fft_data[idx])
    freqs_positive = freqs[idx]

    if len(fft_positive) == 0:
        print("⚠ Data frekuensi kosong.")
        return

    dominant_freq = freqs_positive[np.argmax(fft_positive)]
    print(f"🎵 Frekuensi dominan: {dominant_freq:.2f} Hz")

    # Deteksi jenis hewan
    if dominant_freq < FREQ_ANJING_MAX:
        hewan_terdeteksi = "Anjing 🐕"
        gambar = cv2.imread("Hewan/gambar/anjing.png")
    elif dominant_freq < FREQ_KAMBING_MAX:
        hewan_terdeteksi = "Kambing 🐐"
        gambar = cv2.imread("Hewan/gambar/kambing.png")
    else:
        hewan_terdeteksi = "Kucing 🐈"
        gambar = cv2.imread("Hewan/gambar/kucing.png")

    print(f"✅ Hewan yang ditiru: {hewan_terdeteksi}")

    if gambar is not None:
        cv2.imshow(f"Hasil Deteksi: {hewan_terdeteksi}", gambar)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Tidak bisa membuka kamera.")
        return

    while True:
        aksi = tampil_awal_dengan_gambar(cap)
        if aksi == "start":
            rekam_dan_analisis(cap)
        elif aksi == "restart":
            print("🔄 Tampilan awal dimuat ulang.")
            continue
        elif aksi == "exit":
            break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan program
if _name_ == '_main_':
    main()
