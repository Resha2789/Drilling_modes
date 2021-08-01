from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from myLibrary import FramelessWindow, MainThread as maiThr
from myLibrary.My_pyqt5 import Settings_drilling_modes_win
from myLibrary.MainThread import Report

import re


class SettingsFrame(FramelessWindow.FramelessWindow):
    def __init__(self, main=None):
        super().__init__()
        # Поверх всех окон
        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose)

        self.mainWin = main
        self.setObjectName('SettingsWindow')
        self.widget = SettingsWidget(main=self)
        self.setWidget(self.widget)

        # Размер TitleBar
        self.setTitleBarHeight(20)
        self.titleBar.buttonClose.setMinimumWidth(50)
        self.titleBar.buttonMinimum.hide()
        self.titleBar.buttonMaximum.hide()

        # print(MainWindow.TypeReport.bashneft)


    def closeEvent(self, event):
        self.deleteLater()
        if not self.mainWin.isVisible():
            self.mainWin.show_action()
        self.mainWin.win_settings = False


class SettingsWidget(QWidget, Settings_drilling_modes_win.Ui_Settings_drilling_modes, Report):
    def __init__(self, main=None):
        super().__init__()
        Report.__init__(self)
        self.setupUi(self)
        self.mainWin = main

        self.set_value()
        self.set_connect()
        print(self.cogalm)

    def set_value(self):
        # Название суточное сводки
        self.label_select_file.setText(maiThr.md['Имя_файла'])

        # Тип рапорта
        print(maiThr.md)
        if self.cogalm == maiThr.md['Тип_рапорта']:
            self.radioButton_type_cogalm.click()
        if self.bashneft == maiThr.md['Тип_рапорта']:
            self.radioButton_type_bashneft.click()

    def set_connect(self):
        # Кнопка выбора файла
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.radioButton_type_cogalm.clicked.connect(self.select_type_report)
        self.radioButton_type_bashneft.clicked.connect(self.select_type_report)

    def select_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(caption="Выберите файл суточной сводки")

        name = re.sub(r'.*[/]+', '', directory[0])
        print(name)
        # открыть диалог выбора директории и установить значение переменной
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.label_select_file.setText(f"{name}")
            maiThr.md['Имя_файла'] = name
            maiThr.upDate_json()

    def select_type_report(self):
        x = self.sender()
        if x.objectName() == 'radioButton_type_cogalm':
            maiThr.md['Тип_рапорта'] = self.cogalm

        if x.objectName() == 'radioButton_type_bashneft':
            maiThr.md['Тип_рапорта'] = self.bashneft

        print(maiThr.md['Тип_рапорта'])