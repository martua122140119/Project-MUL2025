import cv2
import pyaudio
import numpy as np
import time

# Pengaturan Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3  # Durasi rekam audio dan video

# Rentang frekuensi (perkirakan)
FREQ_ANJING_MAX = 200
FREQ_KAMBING_MAX = 700

def tampil_awal_dengan_gambar(cap):
    """Tampilkan gambar hewan dan kamera. Tekan 's'=start, 'q'=keluar."""
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
        cv2.imshow("Tekan 's'=mulai, 'q'=keluar", tampilan)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            return "start"
        elif key == ord('q'):
            return "exit"

def streaming_kamera_dengan_overlay(cap, gambar_hewan, hewan_terdeteksi, ukuran_overlay=(200,200)):
    overlay_resized = cv2.resize(gambar_hewan, ukuran_overlay)

    print(f"📹 Streaming kamera dengan overlay: {hewan_terdeteksi}. Tekan 'q' untuk keluar.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca kamera.")
            break

        # Tempel overlay di pojok kiri atas
        h, w, _ = overlay_resized.shape
        frame[0:h, 0:w] = overlay_resized

        cv2.imshow("Kamera dengan Overlay Hewan", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def rekam_dan_analisis(cap):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("🎥 Merekam selama 3 detik...")
    frames_audio = []
    start_time = time.time()

    while (time.time() - start_time) < RECORD_SECONDS:
        ret, frame = cap.read()
        if ret:
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
    cv2.destroyAllWindows()

    if not frames_audio:
        print("⚠️ Tidak ada data audio.")
        return

    audio_np = np.frombuffer(b''.join(frames_audio), dtype=np.int16)
    fft_data = np.fft.fft(audio_np)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.where(freqs > 0)
    fft_positive = np.abs(fft_data[idx])
    freqs_positive = freqs[idx]

    if len(fft_positive) == 0:
        print("⚠️ Data frekuensi kosong.")
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
        streaming_kamera_dengan_overlay(cap, gambar, hewan_terdeteksi, ukuran_overlay=(200, 200))

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

if __name__ == '__main__':
    main()