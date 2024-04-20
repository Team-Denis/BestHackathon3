import matplotlib.pyplot as plt
import numpy as np

ts = np.linspace(0, 100, 100 * 44100)
signal = np.sin(2 * np.pi * 440 * ts)
signal += np.sin(2 * np.pi * 880 * ts)
signal += np.sin(2 * np.pi * 1320 * ts)
signal += np.sin(2 * np.pi * 1760 * ts)
signal += np.sin(2 * np.pi * 2200 * ts)
fs = 44100  # assumed sample frequency in Hz

# Split the signal into chunks
chunk_size = 44100  # 1 second chunks
num_chunks = len(signal) // chunk_size
chunks = np.split(signal[:num_chunks * chunk_size], num_chunks)

# Compute the FFT for each chunk
fft_chunks = [np.fft.fft(chunk) for chunk in chunks]

# Compute the frequencies for the x-axis
frequencies = np.fft.fftfreq(chunk_size, 1 / fs)

# Plot each FFT result on a separate line in a 2D plot, offset vertically by the chunk number
plt.figure(figsize=(10, 10))
for i, fft_chunk in enumerate(fft_chunks):
    # Transform the complex numbers in the frequency spectrum to their magnitudes
    fft_mag = np.abs(fft_chunk)
    fft_mag = fft_mag[:len(fft_chunk) // 2]
    frequencies_chunk = frequencies[:len(frequencies) // 2]

    plt.plot(frequencies_chunk, fft_mag + i * 10)  # Offset each line vertically by the chunk number times 10

plt.xlabel('Frequency (Hz)')
plt.ylabel('Chunk number')
plt.title('Waterfall plot of FFT for each time chunk')
plt.show()
