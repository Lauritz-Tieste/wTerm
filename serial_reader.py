from PySide6 import QtCore
import time


class SerialReader(QtCore.QThread):
    message_received = QtCore.Signal(str)
    make_plot = QtCore.Signal(str)

    def __init__(self, serial_controller):
        super().__init__()
        self.serial_controller = serial_controller
        self.partial_message = b""

    def run(self):
        while True:
            if self.serial_controller.serial_instance:
                message = self.serial_controller.read_from_device()
                if message:
                    self.process_message(message)
            time.sleep(0.001)

    def process_message(self, message):
        message_bytes = message.encode() if isinstance(message, str) else message

        self.partial_message += message_bytes
        start_index = self.partial_message.find(b'\x02')
        end_index = self.partial_message.find(b'\x03')

        while start_index != -1 and end_index != -1:
            data = self.partial_message[start_index + 1:end_index]
            self.make_plot.emit(data.decode())

            self.partial_message = self.partial_message[end_index + 1:]

            start_index = self.partial_message.find(b'\x02')
            end_index = self.partial_message.find(b'\x03')
