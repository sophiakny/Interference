from ctypes import cdll
#from matplotlib import pyplot as plt
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK 
import numpy as np
import os 
import time

# Load DLL
dll_path = r"D:\IT\Photonics\Camera\Scientific Camera Interfaces\SDK\Python Toolkit\dlls\64_lib\thorlabs_tsi_camera_sdk.dll"
cdll.LoadLibrary(dll_path)

dll_dir=r"D:\IT\Photonics\Camera\Scientific Camera Interfaces\SDK\Python Toolkit\dlls\64_lib"
os.add_dll_directory(dll_dir)
os.environ["PATH"] = dll_dir + ";" + os.environ["PATH"]
import cv2
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE

class Cam:
    def __init__(self):
        self.sdk = TLCameraSDK()
        self.device = None
        self.available_cameras = []

    def find_devices(self):
        self.available_cameras = self.sdk.discover_available_cameras()
        if not self.available_cameras:
            print("No cameras detected")
        else:
            print(f"Found cameras: {self.available_cameras}")

    def connect(self):
        if not self.available_cameras:
            print("No cameras available to connect")
            return
        self.device = self.sdk.open_camera(self.available_cameras[0])
        self.device.exposure_time_us = 1000
        self.device.frames_per_trigger_zero_for_unlimited = 0
        self.device.image_poll_timeout_ms = 500
        self.device.arm(2)
        self.device.issue_software_trigger()
        print("Camera connected and armed")

    def acquire(self):
        if not self.device:
            print("Camera not connected")
            return [], []
        
        frame = self.device.get_pending_frame_or_null()
        if frame is None:
            print("Timeout reached, stopping acquisition")

        image = frame.image_buffer  # this may be .image_buffer or similar depending on SDK
        #plt.imshow(image, cmap='gray')  # grayscale is common for camera images
        #plt.title("Captured Frame")
        #plt.colorbar()
        #plt.show()    
        img = np.copy(frame.image_buffer)
        #print(img)
        mean = img.mean()
        singlepixel = img[698, 1080]
        print(f"Frame {frame.frame_count} single pixel: {singlepixel}")
        return singlepixel

    def disconnect(self):
        if self.device:
            self.device.disarm()
            self.device = None
            print("Camera disconnected")

# Usage example
#camera = Cam()
#camera.find_devices()
#camera.connect()
#mean = camera.acquire()
#camera.disconnect()