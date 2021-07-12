import os
from sys import argv, exit
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from window_ui import Ui_MainWindow
from reader import (
    read_file,
    save_this_shit
)


class Converter(QtWidgets.QMainWindow):
    def __init__(self):
        super(Converter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.ui.DragDropLabel.setAcceptDrops(True)
        self.__path: Optional[Path] = None
        self.__save_path: Optional[Path] = None

    def init_UI(self):
        self.setWindowTitle('Конвертер')
        self.setFixedSize(800, 602)
        self.ui.LoadFile.clicked.connect(self.__browse)
        self.ui.ConvertFile.clicked.connect(self.__convert)
        self.ui.SaveFile.clicked.connect(self.__browse_save)

    def __browse(self):
        self.__path = self.__get_path('pgc')
        self.ui.DragDropLabel.setText(os.path.basename(self.__path))

    def __browse_save(self):
        self.__save_path = self.__get_save()
        if str(self.__save_path) == '.':
            pass
        else:
            self.ui.comboBox.addItem(str(self.__save_path))

    def __get_path(self, name: str):
        caption = f'Open {name}'
        filter = 'PowerGraph files (*.pgc)'
        path, _ = QFileDialog.getOpenFileName(self, caption, filter=filter)
        return Path(path)

    def __get_save(self):
        foo_dir = QFileDialog.getExistingDirectory(self, 'Select an awesome directory')
        return Path(foo_dir)

    def __path_check(self):
        if (self.__path is None) or (str(self.__save_path) == '.') or (self.__save_path is None):
            self.__show_error()
            return False
        else:
            return True

    def __convert(self) -> None:
        if self.__path_check() is False:
            return
        else:
            result = read_file(self.__path)
            save_this_shit(self.__save_path, result)
            self.ui.comboBox.clear()
            self.__save_path = None
            self.__show_success()

    def __show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Файл и/или директория не выбраны :^(')
        msg.setWindowTitle('Error')
        msg.exec()

    def __show_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information) #а где иконка лол
        msg.setText('Всё прошло атлишна')
        msg.setWindowTitle('Yay')
        msg.exec()


app = QtWidgets.QApplication(argv)
application = Converter()
application.show()
exit_code = app.exec()
exit(exit_code)

