import pyaudio
import wave

def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    # Setting parameters for the audio file
    FORMAT = pyaudio.paInt16    # Format of wave
    CHANNELS = 1                # Number of audio channels (use 1 for mono)
    RATE = 16000                # Frame rate (16000 Hz is common for speech recognition)
    CHUNK = 1024                # Frames per audio sample
    
    try:
        # Creating PyAudio object
        audio = pyaudio.PyAudio()
        print("PyAudio object created")

        # Open a new stream for the microphone
        print("Listening...")
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        # List to save all audio frames
        frames = []

        # Start recording
        for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # Finished recording
        print("Finished recording.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Saving the recorded audio as a .wav file
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")

    except Exception as e:
        print(f"Error in record_audio function: {e}")

def read_audio(WAVE_FILENAME):
    try:
        # Function to read audio (wav) file
        with open(WAVE_FILENAME, 'rb') as f:
            audio = f.read()
        return audio
    except Exception as e:
        print(f"Error in read_audio function: {e}")
        return None

if __name__ == "__main__":
    print("Starting audio recording...")
    record_audio(4, "myspeech.wav")  # Example: 4 seconds recording
