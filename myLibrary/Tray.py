from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QAction, QStyle, QMessageBox, QTableWidget
from PyQt5 import QtGui, QtCore


# Класс для сворачивания приложения в трее
class TrayIcon(QWidget):
    def __init__(self, parent=None, style=None):
        super().__init__()
        self.mainWindow = parent

        # Объявим и добавим действия для работы с иконкой системного трея
        # show - показать окно
        # hide - скрыть окно
        # exit - выход из программы

        # Устанавливаем иконку
        app_icon = QtGui.QIcon()
        app_icon.addFile('Нужное/favicon_48.ico', QtCore.QSize(48, 48))
        app_icon.addFile('Нужное/favicon_64.ico', QtCore.QSize(64, 64))
        app_icon.addFile('Нужное/favicon_72.ico', QtCore.QSize(72, 72))
        app_icon.addFile('Нужное/favicon_96.ico', QtCore.QSize(96, 96))

        self.mainWindow.tray_icon = QSystemTrayIcon()
        self.mainWindow.tray_icon.setIcon(app_icon)
        self.mainWindow.tray_icon.ActivationReason()

        show_action = QAction("Показать", self.mainWindow)
        hide_action = QAction("Скрыть", self.mainWindow)
        quit_action = QAction("Закрыть", self.mainWindow)

        # self.mainWindow.tray_icon.DoubleClick.connect(self.mainWindow.show)
        show_action.triggered.connect(self.mainWindow.show_action)
        hide_action.triggered.connect(self.mainWindow.close)
        quit_action.triggered.connect(self.mainWindow.exit_action)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.mainWindow.tray_icon.activated.connect(self.onActivated)
        self.mainWindow.tray_icon.setContextMenu(tray_menu)
        self.mainWindow.tray_icon.show()

    def exit(self):

        self.mainWindow.tray_icon.hide()
        self.mainWindow.tray_icon.deleteLater()

    def onActivated(self, reason):
        if reason == 3:
            if self.mainWindow.isVisible():
                self.mainWindow.close()
            else:
                self.mainWindow.show_action()
