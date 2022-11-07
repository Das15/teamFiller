import sys
import os
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QAction


class FileDialog(QFileDialog):
    def __init__(self, parent=None, window_title: str = "Open file",
                 default_dir: str = None, opened_file_on_fail: str = None, allowed_formats="Text files (*.txt *.csv)"):
        super(FileDialog, self).__init__(parent)

        self.setWindowTitle(window_title)
        self.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        self.setNameFilter(allowed_formats)
        self.opened_file_on_fail = opened_file_on_fail

        if default_dir:
            self.setDirectory(default_dir)

    def execute(self):
        if self.exec():
            return self.selectedFiles()[0]
        if self.opened_file_on_fail:
            if not os.path.exists(self.opened_file_on_fail):
                with open(self.opened_file_on_fail, "w"):
                    pass
            os.startfile(self.opened_file_on_fail)
            input("Press enter when done editing the file.")
            return self.opened_file_on_fail


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Hello world")

        fileMenu = self.menuBar().addMenu("&File")
        self.openAction = QtGui.QAction("&Open...", self)
        self.openAction.triggered.connect(self.openFile)
        fileMenu.addAction(self.openAction)

    def openFile(self):
        fileDialog = FileDialog(self, "Open bracket file", os.getcwd(), None)
        if fileDialog.exec():
            print(fileDialog.selectedFiles())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
