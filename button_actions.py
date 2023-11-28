import windialog as wd
from PySide6 import QtWidgets

import plot
from connection_window import ConnectionWindow
from error_dialogs import show_error_dialog
from preferences import Preferences


class ButtonActions:
    def __init__(self, ui, serial_controller):
        self.ui = ui
        self.serial_controller = serial_controller
        self.preferences = Preferences()
        self.connect_button_connected_config = self.preferences.get_button_state_config("connect_button", "connected")
        self.connect_button_disconnected_config = self.preferences.get_button_state_config("connect_button",
                                                                                           "disconnected")
        print("connected: " + str(self.connect_button_connected_config))
        print("disconnected: " + str(self.connect_button_disconnected_config))

    def disconnect_serial_device(self):
        self.serial_controller.disconnect_from_device()
        self.ui.append_to_console("Disconnected from Serial Device.")
        self.ui.buttons["connect_button"].setText(self.connect_button_disconnected_config.get("title"))
        self.ui.buttons["connect_button"].setStyleSheet(
            f"QPushButton {{ background-color: {self.connect_button_disconnected_config.get("color")}; color: #fff; padding: 6px; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: #fff; color: {self.connect_button_disconnected_config.get("color")}; padding: 6px; border-radius: 4px; }}"
        )

    def connect_serial_device(self):
        try:
            session_config = Preferences().get_session_config()
            serial_device = session_config.get("serial_device")
            baud_rate = session_config.get("baud_rate")

            if serial_device and baud_rate:
                if self.serial_controller.connect_to_device(serial_device, baud_rate):
                    self.ui.append_to_console(f"Connected to Serial Device on {serial_device}")
                    self.ui.buttons["connect_button"].setText(self.connect_button_connected_config.get("title"))
                    self.ui.buttons["connect_button"].setStyleSheet(
                        f"QPushButton {{ background-color: {self.connect_button_connected_config.get("color")}; color: #fff; padding: 6px; border-radius: 4px; }}"
                        f"QPushButton:hover {{ background-color: #fff; color: {self.connect_button_connected_config.get("color")}; padding: 6px; border-radius: 4px; }}"
                    )
                else:
                    self.ui.append_to_console(
                        "Failed to connect. Maybe the device is already connected or the device is not connected to the computer."
                    )
                    pass
        except Exception as e:
            show_error_dialog(self, "Error loading the connection configuration",
                              "The configuration of the connection session was not loaded correctly",
                              str(e))

    def on_connect_serial_button_clicked(self):
        if self.serial_controller.is_connected():
            self.disconnect_serial_device()
        else:
            self.connect_serial_device()

    def on_connection_edit_button_clicked(self):
        popup = ConnectionWindow(serial_controller=self.serial_controller)
        if popup.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def load_plot_clicked(self):
        filetypes = (
            (
                "JSON Files",
                "*.json",
            ),
        )

        title = "Load Plot JSON-Data"
        ok_text = "Load Plot"
        file_text = "Selected Plot Data"

        file_path = wd.getfile(
            0,
            *filetypes,
            title=title,
            ok_text=ok_text,
            file_text=file_text,
        )

        if isinstance(file_path, list) and file_path:
            file_path = file_path[0]

        if file_path:
            with open(file_path, "r") as f:
                plot_evaluator = plot.PlotEvaluator(self.ui)
                plot_evaluator.evaluate_plot(data=f.read())

    def save_terminal_clicked(self):
        console_content = self.ui.get_terminal_text()

        filetypes = (
            (
                "Text Files",
                "*.txt",
            ),
        )

        title = "Save the Terminal content"
        ok_text = "Save Terminal content"
        file_text = "Selected File"

        file_path = wd.getsave(
            0,
            *filetypes,
            title=title,
            ok_text=ok_text,
            file_text=file_text,
        )

        if file_path:
            with open(file_path, "w") as f:
                f.write(console_content)

    def clear_clicked(self):
        self.ui.clear_console()

    def send_command_clicked(self, entry_index):
        if self.serial_controller.serial_instance:
            command_text = self.ui.command_entries[entry_index].text()

            if self.serial_controller.write_to_device(command_text):
                self.ui.append_to_console(f"Send command '{command_text}'")
            else:
                self.ui.append_to_console("Error sending command to the device.")
        else:
            self.ui.append_to_console("Error: Not connected to a serial device.")

    def button_clicked(self, function_name):
        getattr(self, function_name)()
