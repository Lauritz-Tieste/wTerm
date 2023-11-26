import serial
import serial.tools.list_ports


class SerialController:
    def __init__(self):
        self.serial_instance = None

    @staticmethod
    def search_for_devices():
        return serial.tools.list_ports.comports()

    def connect_to_device(self, addr, baud_rate):
        try:
            self.serial_instance = serial.Serial(addr, baud_rate, timeout=1)
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
