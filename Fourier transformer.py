import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d


with open('position.txt', 'r') as file:
    positions = [float(line.strip()) for line in file if line.strip()]


with open('intensity.txt', 'r') as file:
    intensity = [float(line.strip()) for line in file if line.strip()]





plt.plot(positions, intensity, linestyle='-', color='blue')
plt.xlabel('Positions')
plt.ylabel("Intensities")
plt.title("Interpherogram")
plt.grid(True)
plt.show()

positions = np.array(positions)
# Consider that light goes back and forward
pos = positions*2*10**6 

# Compute Fourier Transform subtracting the mean value
fft_signal = np.fft.fft(intensity - np.mean(intensity))

#Shift 
np.fft.fftshift(fft_signal)

# Compute frequency axis
freq = np.fft.fftfreq(len(intensity), pos[2]-pos[1])
wavelength = 1/freq

print(type (wavelength))

# positive_x_y = [(xi), (yi) for xi, yi in zip (wavelength, fft_signal) if xi >= 0]

# if positive_x_y:
#     peak_x, peak_y = max(positive_x_y, key=lambda pair: pair[1])
#     print("Peak Y:", peak_y)
#     print("Corresponding X:", peak_x)
# else:
#     print("No positive X values found.")

fft_signal = gaussian_filter1d(fft_signal, sigma=2)
#Plot magnitude spectrum
plt.plot(wavelength, np.abs(fft_signal)) 
plt.title('FFT Magnitude')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
plt.savefig("test_spectrum.png")







# positionsar = np.array(positions)
# intensitiesar = np.array(intensities)
# dx = positionsar[1]-positionsar[0]


# fft_result = np.fft.fft(intensitiesar)
# frequencies = np.fft.fftfreq(len(intensitiesar), d = dx)

# magnitude = np.abs(fft_result)

# plt.plot(frequencies[:len(frequencies)//2], magnitude[:len(magnitude)//2])
# plt.title("Fourier Transform of Intensity vs Position")
# plt.xlabel("Frequency (1/units of position)")
# plt.ylabel("Magnitude")
# plt.grid(True)
# plt.show()