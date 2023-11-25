import windialog as wd
import plot


class ButtonActions:
    def __init__(self, ui, serial_controller):
        self.ui = ui
        self.serial_controller = serial_controller

    def save_setup_clicked(self):
        self.ui.append_to_console("Save Setup button clicked (not ready yet)")

    def save_plot_clicked(self):
        self.ui.append_to_console("Save Plot button clicked (not ready yet)")

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

    def start_plot_clicked(self):
        self.ui.append_to_console("Start Plot button clicked (not ready yet)")

    def clear_clicked(self):
        self.ui.clear_console()

    def help_clicked(self):
        self.ui.append_to_console("Help button clicked (not ready yet)")

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
