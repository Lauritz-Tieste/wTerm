from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QComboBox, QLabel, QHBoxLayout

from w_term_config import BAUD_RATES, BIT_RATE, PARITY, STOP_BITS
from preferences import Preferences
from w_term_config import CONNECTION_EDIT_WINDOW_SAVE_BUTTON
from error_dialogs import show_warning_dialog


class ConnectionWindow(QDialog):

    def __init__(self, serial_controller):
        super().__init__()
        self.serial_controller = serial_controller

        layout = QVBoxLayout()

        self.serial_layout = QHBoxLayout()
        layout.addLayout(self.serial_layout)

        self.serial_dropdown_label = QLabel("Serial Device")
        self.serial_dropdown_label.setFixedWidth(100)
        self.serial_layout.addWidget(self.serial_dropdown_label)

        self.serial_dropdown = QComboBox(self)
        self.update_serial_dropdown()
        self.serial_layout.addWidget(self.serial_dropdown, stretch=2)
        self.serial_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
        )

        self.baud_layout = QHBoxLayout()
        layout.addLayout(self.baud_layout)

        self.baud_dropdown_label = QLabel("Baud Rate")
        self.baud_dropdown_label.setFixedWidth(100)
        self.baud_layout.addWidget(self.baud_dropdown_label)

        self.baud_dropdown = QComboBox(self)
        self.baud_dropdown.addItems([str(baud_rate) for baud_rate in BAUD_RATES])
        self.baud_layout.addWidget(self.baud_dropdown, stretch=2)
        self.baud_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
        )

        self.bitrate_layout = QHBoxLayout()
        layout.addLayout(self.bitrate_layout)

        self.bitrate_dropdown_label = QLabel("Bit Rate")
        self.bitrate_dropdown_label.setFixedWidth(100)
        self.bitrate_layout.addWidget(self.bitrate_dropdown_label)

        self.bitrate_dropdown = QComboBox(self)
        self.bitrate_dropdown.addItems([str(items["title"]) for items in BIT_RATE])
        self.bitrate_layout.addWidget(self.bitrate_dropdown, stretch=2)
        self.bitrate_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
        )

        self.parity_layout = QHBoxLayout()
        layout.addLayout(self.parity_layout)

        self.parity_dropdown_label = QLabel("Parity")
        self.parity_dropdown_label.setFixedWidth(100)
        self.parity_layout.addWidget(self.parity_dropdown_label)

        self.parity_dropdown = QComboBox(self)
        self.parity_dropdown.addItems([str(items["title"]) for items in PARITY])
        self.parity_layout.addWidget(self.parity_dropdown, stretch=2)
        self.parity_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
        )

        self.stop_bit_layout = QHBoxLayout()
        layout.addLayout(self.stop_bit_layout)

        self.stop_bit_dropdown_label = QLabel("Stop Bit")
        self.stop_bit_dropdown_label.setFixedWidth(100)
        self.stop_bit_layout.addWidget(self.stop_bit_dropdown_label)

        self.stop_bit_dropdown = QComboBox(self)
        self.stop_bit_dropdown.addItems([str(items["title"]) for items in STOP_BITS])
        self.stop_bit_layout.addWidget(self.stop_bit_dropdown, stretch=2)
        self.stop_bit_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
        )

        layout.addSpacing(20)

        button = QPushButton(CONNECTION_EDIT_WINDOW_SAVE_BUTTON[0])
        button.clicked.connect(self.save_button_clicked)
        button.setStyleSheet(
            f"QPushButton {{ background-color: {CONNECTION_EDIT_WINDOW_SAVE_BUTTON[1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {CONNECTION_EDIT_WINDOW_SAVE_BUTTON[1]}; padding: 6px; border-radius: 4px; }}"
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
            self.serial_dropdown.addItem(str(device))

    def save_button_clicked(self):
        serial_device = self.serial_dropdown.currentText()
        baud_rate = self.baud_dropdown.currentText()

        connection_details = {"serial_device": serial_device, "baud_rate": baud_rate,
                              "bit_rate": self.bitrate_dropdown.currentText(),
                              "parity": self.parity_dropdown.currentText(),
                              "stop_bit": self.stop_bit_dropdown.currentText()}
        Preferences().save_session_config(connection_details)

        self.accept()

    def load_connection_details(self):
        try:
            session_config = Preferences().get_session_config()
            serial_device = session_config.get("serial_device")
            baud_rate = session_config.get("baud_rate")
            bit_rate = session_config.get("bit_rate")
            parity = session_config.get("parity")
            stop_bit = session_config.get("stop_bit")

            if serial_device in [self.serial_dropdown.itemText(i) for i in range(self.serial_dropdown.count())]:
                self.serial_dropdown.setCurrentText(serial_device)

            if baud_rate in [self.baud_dropdown.itemText(i) for i in range(self.baud_dropdown.count())]:
                self.baud_dropdown.setCurrentText(baud_rate)

            if bit_rate in [self.bitrate_dropdown.itemText(i) for i in range(self.bitrate_dropdown.count())]:
                self.bitrate_dropdown.setCurrentText(bit_rate)

            if parity in [self.parity_dropdown.itemText(i) for i in range(self.parity_dropdown.count())]:
                self.parity_dropdown.setCurrentText(parity)

            if stop_bit in [self.stop_bit_dropdown.itemText(i) for i in range(self.stop_bit_dropdown.count())]:
                self.stop_bit_dropdown.setCurrentText(stop_bit)
        except Exception as e:
            show_warning_dialog(self, "No connection configuration file existing",
                                "There is no connection configuration file. Continue to create one.",
                                str(e))
