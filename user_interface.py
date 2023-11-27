from PySide6 import QtWidgets, QtGui
from functools import partial

from button_actions import ButtonActions
from w_term_config import BUTTON_CONFIG, COMMAND_CONFIG
from plot import PlotEvaluator
from serial_reader import SerialReader


class UserInterface(QtWidgets.QWidget):
    def create_buttons(self):
        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.root_layout.addLayout(self.buttonLayout)

        self.button_actions = ButtonActions(self, self.serial_controller)

        for label, color, function_name, button_name in BUTTON_CONFIG:
            button = QtWidgets.QPushButton(label)
            button.setStyleSheet(
                f"QPushButton {{ background-color: {color}; color: #fff; padding: 6px; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: #fff; color: {color}; padding: 6px; border-radius: 4px; }}"
            )
            button.clicked.connect(partial(self.button_actions.button_clicked, function_name))

            self.buttonLayout.addWidget(button)
            self.buttons[button_name] = button

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

        self.buttons = {}

        self.serial_controller = serial_controller
        self.plot_evaluator = PlotEvaluator(self)

        self.root_layout = QtWidgets.QVBoxLayout(self)

        self.create_buttons()
        self.create_command_layout()
        self.create_terminal()
