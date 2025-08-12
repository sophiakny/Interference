from Throlabsmotor import LinearStage
import numpy as np
from ctypes import cdll
from matplotlib import pyplot as plt
import time
from camera import Cam

stage = LinearStage()
sn = stage.find_devices()[0]  # Get the first available device
stage.connect(sn)
time.sleep(1)
#stage.move(10)  # Move to position 10 mm
camera = Cam()
camera.find_devices()
camera.connect()

step = 0.00004  # Step size in mm
pos, intensity = stage.jog_and_measure(0, 0.05, step, camera.acquire, 0.1)  # Jog from 0 tom 5 m in steps of 0.01 um
print(pos)
print(intensity)
camera.disconnect()
stage.disconnect()

plt.plot(pos, intensity)
plt.xlabel('Position (mm)')
plt.ylabel('Mean Camera Value')
plt.show()
plt.savefig("test_interferogram.png")
  
np.savetxt("intensity_0808.txt", intensity, fmt='%d')
np.savetxt("position_0808.txt", pos, fmt='%.5f')

# Consider that light goes back and forward
pos = pos*2*10**6 

# Compute Fourier Transform subtracting the mean value
fft_signal = np.fft.fft(intensity - np.mean(intensity))

#Shift 
np.fft.fftshift(fft_signal)

# Compute frequency axis
freq = np.fft.fftfreq(len(intensity), pos[2]-pos[1])
wavelength = 1/freq

# positive_x_y = [(xi), (yi) for xi, yi in zip (wavelength, fft_signal) if xi >= 0]

# if positive_x_y:
#     peak_x, peak_y = max(positive_x_y, key=lambda pair: pair[1])
#     print("Peak Y:", peak_y)
#     print("Corresponding X:", peak_x)
# else:
#     print("No positive X values found.")






#Plot magnitude spectrum
plt.plot(wavelength, np.abs(fft_signal))
plt.title('FFT Magnitude')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
plt.savefig("test_spectrum.png")

