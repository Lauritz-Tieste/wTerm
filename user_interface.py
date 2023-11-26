from PySide6 import QtWidgets, QtGui
from functools import partial
from button_actions import ButtonActions
from w_term_config import BUTTON_CONFIG, COMMAND_CONFIG
from plot import PlotEvaluator
from serial_reader import SerialReader
from w_term_config import BAUD_RATES, CONNECT_BUTTON_CONFIG


class UserInterface(QtWidgets.QWidget):
    def create_dropdowns(self):
        self.serial_dropdown = QtWidgets.QComboBox(self)
        self.serial_dropdown.currentIndexChanged.connect(self.serial_device_changed)
        self.update_serial_dropdown()
        self.serial_dropdown.setStyleSheet(
            "QComboBox { background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox:hover { background-color: #d1d5db; color: #000; padding: 6px; border-radius: 4px; }"
            "QComboBox::drop-down { width: 20px; height: 20px; border: 0px; }"
            "QComboBox::down-arrow { image: url(down_arrow.png); }"
        )

        self.baud_dropdown = QtWidgets.QComboBox(self)
        self.baud_dropdown.currentIndexChanged.connect(self.baud_rate_changed)
        self.baud_dropdown.addItems([str(baud_rate) for baud_rate in BAUD_RATES])
        self.baud_dropdown.setStyleSheet(
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
        self.serial_dropdown.itemText(index)

    def baud_rate_changed(self, index):
        self.baud_dropdown.itemText(index)

    def connect_serial_device(self):
        selected_device = self.serial_dropdown.currentText()
        baud_rate = int(self.baud_dropdown.currentText())
        if self.serial_controller.connect_to_device(selected_device, baud_rate):
            self.append_to_console(f"Connected to Serial Device on {selected_device}")
            self.connect_serial_button.setText(CONNECT_BUTTON_CONFIG[1][0])
            self.connect_serial_button.setStyleSheet(
                f"QPushButton {{ background-color: {CONNECT_BUTTON_CONFIG[1][1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: #fff; color: {CONNECT_BUTTON_CONFIG[1][1]}; padding: 6px; border-radius: 4px; }}"
            )
        else:
            self.append_to_console(
                "Failed to connect. Maybe the device is already connected or the device is not connected to computer."
            )

    def disconnect_serial_device(self):
        self.serial_controller.disconnect_from_device()
        self.append_to_console("Disconnected from Serial Device.")
        self.connect_serial_button.setText(CONNECT_BUTTON_CONFIG[0][0])
        self.connect_serial_button.setStyleSheet(
            f"QPushButton {{ background-color: {CONNECT_BUTTON_CONFIG[0][1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {CONNECT_BUTTON_CONFIG[0][1]}; padding: 6px; border-radius: 4px; }}"
        )

    def create_command_layout(self):
        self.commandLayout = QtWidgets.QGridLayout(self)
        self.root_layout.addLayout(self.commandLayout)

        self.command_actions = ButtonActions(self, self.serial_controller)
        self.command_entries = []

        row, col = 0, 0
        for label, color, function_name, command in COMMAND_CONFIG:
            command_button = QtWidgets.QPushButton(label)
            command_button.setStyleSheet(
                f"QPushButton {{ background-color: #fff; color: #000; padding: 6px; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: {color}; color: #fff; padding: 6px; border-radius: 4px; }}"
            )
            entry = QtWidgets.QLineEdit()
            entry.setPlaceholderText("Enter a command")
            entry.setText(command)
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

    def on_connect_serial_button_clicked(self):
        if self.serial_controller.is_connected():
            self.disconnect_serial_device()
        else:
            self.connect_serial_device()

    def create_terminal(self):
        self.terminalLayout = QtWidgets.QVBoxLayout(self)
        self.root_layout.addLayout(self.terminalLayout)

        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setReadOnly(True)

        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.terminal.setFont(font)

        self.terminal.setStyleSheet(
            "QTextEdit {background-color: #d1d5db; padding: 6px; border-radius: 4px; };"
        )
        self.terminalLayout.addWidget(self.terminal)

        self.serial_dropdown_layout = QtWidgets.QHBoxLayout()
        self.serial_dropdown_layout.addWidget(self.serial_dropdown)
        self.serial_dropdown_layout.addWidget(self.baud_dropdown)
        self.terminalLayout.addLayout(self.serial_dropdown_layout)

        self.connect_serial_button = QtWidgets.QPushButton(CONNECT_BUTTON_CONFIG[0][0])
        self.connect_serial_button.clicked.connect(self.on_connect_serial_button_clicked)
        self.connect_serial_button.setStyleSheet(
            f"QPushButton {{ background-color: {CONNECT_BUTTON_CONFIG[0][1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {CONNECT_BUTTON_CONFIG[0][1]}; padding: 6px; border-radius: 4px; }}"
        )
        self.serial_dropdown_layout.addWidget(self.connect_serial_button)

        self.serial_reader = SerialReader(self.serial_controller)
        self.serial_reader.message_received.connect(self.append_to_console)
        self.serial_reader.make_plot.connect(self.plot_evaluator.evaluate_plot)
        self.serial_reader.start()

    def append_to_console(self, text):
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        self.terminal.append(text + "\n")

    def clear_console(self):
        self.terminal.clear()

    def get_terminal_text(self):
        return self.terminal.toPlainText()

    def __init__(self, serial_controller):
        super().__init__()

        self.serial_controller = serial_controller
        self.plot_evaluator = PlotEvaluator(self)

        self.root_layout = QtWidgets.QVBoxLayout(self)

        self.create_buttons()
        self.create_dropdowns()
        self.create_command_layout()
        self.create_terminal()
