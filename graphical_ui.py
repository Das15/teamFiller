import sys
import os
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGridLayout, QPushButton, QWidget, QLabel, \
    QScrollArea
from PySide6.QtGui import QAction, QPicture, QImage, QPixmap


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


class MainLayout(QGridLayout):
    def __init__(self, parent=None):
        super(MainLayout, self).__init__(parent)


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Hello world")
        self.resize(800, 400)

        file_menu = self.menuBar().addMenu("&File")
        self.openAction = QtGui.QAction("&Open...", self)
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QtGui.QAction("&Save", self)
        self.saveAction.setDisabled(True)
        self.saveAction.triggered.connect(self.save_file)

        self.saveAsAction = QtGui.QAction("S&ave as...", self)
        self.saveAsAction.setDisabled(True)
        self.openAction.triggered.connect(self.save_as_file)

        file_menu.addAction(self.openAction)
        file_menu.addAction(self.saveAction)
        file_menu.addAction(self.saveAsAction)

        self.teamButton = QPushButton("Hi", self)
        self.mappoolButton = QPushButton("Hello there!", self)
        self.ladderButton = QPushButton("Hi mark!", self)

        self.imageDisplay = QLabel(self)
        image = QImage()
        image.load("C:\\Users\\Das\\PycharmProjects\\teamFiller\\output.png")
        self.imageDisplay.setPixmap(QPixmap.fromImage(image))

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageDisplay)

        layout = QGridLayout()
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.teamButton, 0, 0)
        layout.addWidget(self.mappoolButton, 1, 0)
        layout.addWidget(self.ladderButton, 2, 0)
        layout.addWidget(self.scrollArea, 0, 1)
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setStyleSheet("background-color: blue")
        self.setCentralWidget(widget)
        self.setStyleSheet("top: 0")

    def save_as_file(self):
        ...

    def save_file(self):
        ...

    def open_file(self):
        file_dialog = FileDialog(self, "Open bracket file", os.getcwd(), None)
        if file_dialog.exec():
            print(file_dialog.selectedFiles())
        self.saveAction.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
