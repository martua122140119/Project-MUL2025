import cv2
import pyaudio
import numpy as np
import time

# Pengaturan Audio untuk PyAudio
FORMAT = pyaudio.paInt16      # Format audio 16-bit integer
CHANNELS = 1                  # Mono channel
RATE = 44100                  # Sample rate 44.1 KHz (CD quality)
CHUNK = 1024                  # Jumlah sample per buffer
RECORD_SECONDS = 3            # Durasi rekam audio dan video

# Rentang frekuensi untuk klasifikasi suara hewan
FREQ_ANJING_MAX = 300        # Batas maksimum frekuensi anjing (Hz)
FREQ_KAMBING_MAX = 1000      # Batas maksimum frekuensi kambing (Hz)
MIN_RMS_THRESHOLD = 500      # Batas minimum volume suara yang diterima

def calculate_rms(data):
    """
    Menghitung Root Mean Square (RMS) untuk mengukur volume suara.
    RMS tinggi = suara keras, RMS rendah = suara pelan
    """
    data_float = data.astype(np.float32)
    return np.sqrt(np.mean(data_float**2))

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
        cv2.imshow("Tirukan Suara Hewan ini!!", tampilan)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            return "start"
        elif key == ord('q'):
            return "exit"

def streaming_kamera_dengan_overlay(cap, gambar_hewan, hewan_terdeteksi, ukuran_overlay=(200,200)): 
    """Streaming kamera dengan overlay gambar hewan."""
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

        cv2.imshow("Suara Hewan Terdeteksi", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def rekam_dan_analisis(cap):
    # Inisialisasi PyAudio dan buka stream untuk rekaman
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
        print("⚠ Tidak ada data audio.")
        return

    audio_np = np.frombuffer(b''.join(frames_audio), dtype=np.int16)
    
    # Tambahkan pengecekan RMS
    rms_value = calculate_rms(audio_np)
    print(f"📊 RMS suara yang direkam: {rms_value:.2f}")

    if rms_value < MIN_RMS_THRESHOLD:
        print(f"⚠ Suara terlalu pelan (RMS: {rms_value:.2f}). Coba lebih keras!")
        return

    print("✅ Suara cukup keras, melanjutkan analisis frekuensi...")
    
    # Analisis Frekuensi menggunakan FFT
    fft_data = np.fft.fft(audio_np)                    # Transformasi Fourier
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)    # Konversi ke Hz
    idx = np.where(freqs > 0)                          # Ambil frekuensi positif
    fft_positive = np.abs(fft_data[idx])               # Magnitude frekuensi
    freqs_positive = freqs[idx]

    # Deteksi jenis hewan berdasarkan frekuensi dominan
    dominant_freq = freqs_positive[np.argmax(fft_positive)]
    if dominant_freq < FREQ_ANJING_MAX:           # Frek < 300 Hz = Anjing
        hewan_terdeteksi = "Anjing 🐕"
        gambar = cv2.imread("Hewan/gambar/anjing.png")
    elif dominant_freq < FREQ_KAMBING_MAX:        # Frek < 1000 Hz = Kambing
        hewan_terdeteksi = "Kambing 🐐"
        gambar = cv2.imread("Hewan/gambar/kambing.png")
    else:                                         # Frek >= 1000 Hz = Kucing
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
