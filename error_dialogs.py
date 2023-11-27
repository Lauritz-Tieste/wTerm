from PySide6.QtWidgets import QMessageBox


def show_error_dialog(self, title, text, detailed_text):
    error_dialog = QMessageBox(self)
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle(title)
    error_dialog.setText(text)
    error_dialog.setDetailedText(detailed_text)
    error_dialog.exec_()
