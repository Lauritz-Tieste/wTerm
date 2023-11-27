from PySide6 import QtWidgets, QtGui
from functools import partial

from button_actions import ButtonActions
from error_dialogs import show_error_dialog
from preferences import Preferences
from w_term_config import BUTTON_CONFIG, COMMAND_CONFIG
from plot import PlotEvaluator
from serial_reader import SerialReader
from w_term_config import CONNECT_BUTTON_CONFIG, CONNECTION_EDIT_BUTTON
from connection_window import ConnectionWindow


class UserInterface(QtWidgets.QWidget):
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

    def connect_serial_device(self):
        try:
            session_config = Preferences().get_session_config()
            serial_device = session_config.get("serial_device")
            baud_rate = session_config.get("baud_rate")

            if serial_device and baud_rate:
                if self.serial_controller.connect_to_device(serial_device, baud_rate):
                    self.append_to_console(f"Connected to Serial Device on {serial_device}")
                    self.connect_serial_button.setText(CONNECT_BUTTON_CONFIG[1][0])
                    self.connect_serial_button.setStyleSheet(
                        f"QPushButton {{ background-color: {CONNECT_BUTTON_CONFIG[1][1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
                        f"QPushButton:hover {{ background-color: #fff; color: {CONNECT_BUTTON_CONFIG[1][1]}; padding: 6px; border-radius: 4px; }}"
                    )
                else:
                    self.append_to_console(
                        "Failed to connect. Maybe the device is already connected or the device is not connected to the computer."
                    )
        except Exception as e:
            show_error_dialog(self, "Error loading the connection configuration",
                              "The configuration of the connection session was not loaded correctly",
                              str(e))

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

    def on_connection_edit_button_clicked(self):
        popup = ConnectionWindow(serial_controller=self.serial_controller)
        if popup.exec_() == QtWidgets.QDialog.Accepted:
            pass

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

        self.connection_layout = QtWidgets.QHBoxLayout(self)

        self.connect_serial_button = QtWidgets.QPushButton(CONNECT_BUTTON_CONFIG[0][0])
        self.connect_serial_button.clicked.connect(self.on_connect_serial_button_clicked)
        self.connect_serial_button.setStyleSheet(
            f"QPushButton {{ background-color: {CONNECT_BUTTON_CONFIG[0][1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {CONNECT_BUTTON_CONFIG[0][1]}; padding: 6px; border-radius: 4px; }}"
        )
        self.connection_layout.addWidget(self.connect_serial_button)

        self.connection_edit_button = QtWidgets.QPushButton(CONNECTION_EDIT_BUTTON[0])
        self.connection_edit_button.clicked.connect(self.on_connection_edit_button_clicked)
        self.connection_edit_button.setStyleSheet(
            f"QPushButton {{ background-color: {CONNECTION_EDIT_BUTTON[1]}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {CONNECTION_EDIT_BUTTON[1]}; padding: 6px; border-radius: 4px; }}"
        )
        self.connection_layout.addWidget(self.connection_edit_button)

        self.terminalLayout.addLayout(self.connection_layout)

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
        self.create_command_layout()
        self.create_terminal()
