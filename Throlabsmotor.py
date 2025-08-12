from turtle import position
import numpy as np
import clr
import time
import os
import sys

# Replace with your actual Kinesis DLL path
kinesis_path = r"C:\Program Files\Thorlabs\Kinesis"

# Add DLLs to path and load
clr.AddReference(os.path.join(kinesis_path, "Thorlabs.MotionControl.DeviceManagerCLI.dll"))
clr.AddReference(os.path.join(kinesis_path, "Thorlabs.MotionControl.KCube.DCServoCLI.dll"))

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.DCServoCLI import KCubeDCServo
from System import Decimal

class LinearStage:
    """ Linear stage interface """
    def __init__(self):
        self.device = None

    def find_devices(self):
        """ Lists available device serial numbers """
        DeviceManagerCLI.BuildDeviceList()
        return [str(sn) for sn in DeviceManagerCLI.GetDeviceList()]

    def connect(self, serial_number):
        """ Connects to a device by serial number """
        DeviceManagerCLI.BuildDeviceList()  # Always refresh list
        available = [str(sn) for sn in DeviceManagerCLI.GetDeviceList()]
        if serial_number not in available:
            raise ValueError(f"Device with ID {serial_number} not found.")

        self.device = KCubeDCServo.CreateKCubeDCServo(serial_number)
        self.device.Connect(serial_number)
        #self.device.WaitForSettingsInitialized(10000)
        self.device.LoadMotorConfiguration(serial_number)
        self.device.StartPolling(250)
        self.device.EnableDevice()
        #self.device.Home(60000)

    def move(self, pos):
        """Move stage to position `pos` (in mm), suppressing console output."""
        # Suppress prints if any
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')   
        
        try:
            self.device.MoveTo(Decimal(pos), 60000) 
        finally:
            # Restore stdout no matter what
            sys.stdout.close()
            sys.stdout = original_stdout
        
        position = self.device.get_Position()
        return position

    def jog_and_measure(self, start, end, step,  function=None, wait_time=1):
        if function is None:
            function = self.device.get_Position

        positions = []
        measure = []
        for pos in np.arange(start, end + step, step):  
            self.device.MoveTo(Decimal(pos), 60000)
            time.sleep(wait_time)
            positions.append(pos)
            measure.append(function())

        return positions, measure
    
    def disconnect(self):
        #"""Gracefully disconnect the device."""
        if self.device is not None:
            try:
                self.device.StopPolling()
                self.device.Disconnect(True)
                self.device = None
            except Exception as e:
                print(f"Error during disconnection: {e}")

#stage = LinearStage()
#sn = stage.find_devices()[0]  # Get the first available device
#print(sn)
#stage.connect(sn)
#time.sleep(1)
#stage.move(5.01)
#pos = stage.move(10) 
#print(pos)
#jog_positions, measurements = stage.jog_and_measure(5, 5.2, 0.001)