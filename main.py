import sys
from PySide6 import QtWidgets

from user_interface import UserInterface
from serial_controller import SerialController

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    serial_controller = SerialController()

    widget = UserInterface(serial_controller)
    widget.setWindowTitle("wTerm")
    widget.resize(1000, 700)
    widget.show()

    sys.exit(app.exec())
