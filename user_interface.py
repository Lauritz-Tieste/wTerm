from PySide6 import QtWidgets
from functools import partial
from button_actions import ButtonActions
from w_term_config import BUTTON_CONFIG, COMMAND_CONFIG


class UserInterface(QtWidgets.QWidget):
    def create_root_layout(self):
        self.root_layout = QtWidgets.QVBoxLayout(self)

    def create_serial_dropdown(self):
        self.serial_dropdown = QtWidgets.QComboBox(self)
        self.serial_dropdown.currentIndexChanged.connect(self.serial_device_changed)
        self.update_serial_dropdown()
        self.serial_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
            "QComboBox::down-arrow { image: url(down_arrow.png); }"
        )

    def update_serial_dropdown(self):
        devices = self.serial_controller.search_for_devices()
        self.serial_dropdown.clear()
        for device in devices:
            self.serial_dropdown.addItem(device.device)

    def create_buttons(self):
        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.root_layout.addLayout(self.buttonLayout)

        self.button_actions = ButtonActions(self, self.serial_controller)

        for label, color, function_name in BUTTON_CONFIG:
            button = QtWidgets.QPushButton(label)
            button.setStyleSheet(
                f"QPushButton {{ background-color: {color}; color: #fff; padding: 6px; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: #fff; color: {color}; padding: 6px; border-radius: 4px; }}"
            )
            button.clicked.connect(
                partial(self.button_actions.button_clicked, function_name)
            )

            self.buttonLayout.addWidget(button)

    def serial_device_changed(self, index):
        selected_device = self.serial_dropdown.itemText(index)
        print(f"Selected Serial Device: {selected_device}")

    def connect_serial_device(self):
        selected_device = self.serial_dropdown.currentText()
        if self.serial_controller.connect_to_device(selected_device):
            self.append_to_console(f"Connected to Serial Device on {selected_device}")
        else:
            self.append_to_console(
                "Failed to connect. Maybe you are already connected or the device is not connected to computer."
            )

    def create_command_layout(self):
        self.commandLayout = QtWidgets.QGridLayout(self)
        self.root_layout.addLayout(self.commandLayout)

        self.command_actions = ButtonActions(self, self.serial_controller)
        self.command_entries = []

        row, col = 0, 0
        for label, color, function_name in COMMAND_CONFIG:
            command_button = QtWidgets.QPushButton(label)
            command_button.setStyleSheet(
                f"QPushButton {{ background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: {color}; color: #fff; padding: 6px; border-radius: 4px; }}"
            )
            entry = QtWidgets.QLineEdit()
            entry.setPlaceholderText("Enter a command")
            entry.setStyleSheet(
                "QLineEdit {background-color: #fff; color: #000; padding: 6px; border-radius: 4px; };"
            )

            command_button.clicked.connect(
                partial(self.command_actions.send_command_clicked, col // 2)
            )
            self.commandLayout.addWidget(command_button, row, col)
            self.commandLayout.addWidget(entry, row, col + 1)

            self.command_entries.append(entry)

            col += 2
            if col >= 6:
                col = 0
                row += 1

    def create_terminal(self):
        self.terminalLayout = QtWidgets.QVBoxLayout(self)
        self.root_layout.addLayout(self.terminalLayout)

        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet(
            "QTextEdit {background-color: #d1d5db; padding: 6px; border-radius: 4px; };"
        )
        self.terminalLayout.addWidget(self.terminal)

        self.serial_dropdown_layout = QtWidgets.QHBoxLayout()
        self.serial_dropdown_layout.addWidget(self.serial_dropdown)
        self.terminalLayout.addLayout(self.serial_dropdown_layout)

        self.connect_serial_button = QtWidgets.QPushButton("Connect")
        self.connect_serial_button.clicked.connect(self.connect_serial_device)
        self.connect_serial_button.setStyleSheet(
            f"QPushButton {{ background-color: #ec4899; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: #ec4899; padding: 6px; border-radius: 4px; }}"
        )
        self.serial_dropdown_layout.addWidget(self.connect_serial_button)

    def append_to_console(self, text):
        self.terminal.append(text)

    def clear_console(self):
        self.terminal.clear()

    def return_terminal_text(self):
        return self.terminal.toPlainText()

    def __init__(self, serial_controller):
        super().__init__()

        self.serial_controller = serial_controller

        self.create_root_layout()
        self.create_buttons()
        self.create_serial_dropdown()
        self.create_command_layout()
        self.create_terminal()
