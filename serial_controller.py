import serial
import serial.tools.list_ports
from w_term_config import BIT_RATE, PARITY, STOP_BITS


class SerialController:
    def __init__(self):
        self.serial_instance = None

    @staticmethod
    def search_for_devices():
        return serial.tools.list_ports.comports()

    def connect_to_device(self, device, baud_rate, bit_rate, parity, stop_bit):
        try:
            addr = device[device.find("(") + 1:device.find(")")]
            self.serial_instance = serial.Serial(addr, baud_rate, timeout=1)

            for bit in BIT_RATE:
                if bit["title"] == bit_rate:
                    bit_rate = bit["variable"]
                    break

            for par in PARITY:
                if par["title"] == parity:
                    parity = par["variable"]
                    break

            for stop in STOP_BITS:
                if stop["title"] == stop_bit:
                    stop_bit = stop["variable"]
                    break

            self.serial_instance.bytesize = bit_rate
            self.serial_instance.parity = parity
            self.serial_instance.stopbits = stop_bit
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to device: {e}")
            return False

    def read_from_device(self):
        if self.serial_instance:
            return self.serial_instance.readline().decode("utf-8").strip()
        else:
            return None

    def write_to_device(self, data):
        if self.serial_instance:
            encoded_data = (data + "\r\n").encode()
            self.serial_instance.write(encoded_data)
            return True
        else:
            return False

    def disconnect_from_device(self):
        if self.serial_instance:
            self.serial_instance.close()
            self.serial_instance = None
            return True
        else:
            return False

    def is_connected(self):
        if self.serial_instance:
            return True
        else:
            return False
