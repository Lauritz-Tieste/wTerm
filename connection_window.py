from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QComboBox
import json

from w_term_config import BAUD_RATES
from preferences import Preferences


class ConnectionWindow(QDialog):
    SESSION_CONFIG_FILE = "session_config.json"

    def __init__(self, serial_controller):
        super().__init__()
        self.serial_controller = serial_controller

        layout = QVBoxLayout()

        self.serial_dropdown = QComboBox(self)
        self.update_serial_dropdown()
        layout.addWidget(self.serial_dropdown)
        self.serial_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
            "QComboBox::down-arrow { image: url(down_arrow.png); }"  # TODO: Add the down_arrow.png to the project
        )

        self.baud_dropdown = QComboBox(self)
        self.baud_dropdown.addItems([str(baud_rate) for baud_rate in BAUD_RATES])
        self.baud_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
            "QComboBox::down-arrow { image: url(down_arrow.png); }"  # TODO: Add the down_arrow.png to the project
        )
        layout.addWidget(self.baud_dropdown)

        # TODO: Add the colors of the button to the ui configuration file
        button = QPushButton("Save connection details")
        button.clicked.connect(self.save_button_clocked)
        button.setStyleSheet(
            "QPushButton { background-color: #22c55e; color: #fff; padding: 6px; border-radius: 4px; }"
            "QPushButton:hover { background-color: #fff; color: #22c55e; padding: 6px; border-radius: 4px; }"
        )
        layout.addWidget(button)

        self.setLayout(layout)

        self.setWindowTitle("wTerm | Edit Connection Details")
        self.resize(400, 0)

        self.load_connection_details()

    def update_serial_dropdown(self):
        devices = self.serial_controller.search_for_devices()
        self.serial_dropdown.clear()
        for device in devices:
            self.serial_dropdown.addItem(device.device)

    def save_button_clocked(self):
        serial_device = self.serial_dropdown.currentText()
        baud_rate = self.baud_dropdown.currentText()

        connection_details = {"serial_device": serial_device, "baud_rate": baud_rate}
        with open(self.SESSION_CONFIG_FILE, "w") as config_file:
            json.dump(connection_details, config_file)

        self.accept()

    def load_connection_details(self):
        session_config = Preferences().get_session_config()
        serial_device = session_config.get("serial_device")
        baud_rate = session_config.get("baud_rate")

        if serial_device in [self.serial_dropdown.itemText(i) for i in range(self.serial_dropdown.count())]:
            self.serial_dropdown.setCurrentText(serial_device)

        if baud_rate in [self.baud_dropdown.itemText(i) for i in range(self.baud_dropdown.count())]:
            self.baud_dropdown.setCurrentText(baud_rate)
