import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import QObject
from myLibrary import Tray as Tr, FramelessWindow as Fr, SettingsWindow, MainThread as maiThr
from myLibrary.My_pyqt5 import Drilling_modes_win
import time, datetime

# Для иконки в приложении
try:
    # Включите в блок try/except, если вы также нацелены на Mac/Linux
    from PyQt5.QtWinExtras import QtWin  # !!!

    myappid = 'mycompany.myproduct.subproduct.version'  # !!!
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)  # !!!
except ImportError:
    pass

class Communicate(QObject):
    rowTable_change = QtCore.pyqtSignal(object)
    table_change = QtCore.pyqtSignal(object)
    table_clear = QtCore.pyqtSignal(object)


class MainWindowFrame(Fr.FramelessWindow):
    def __init__(self):
        super().__init__()
        self.initMainWindow()

    def initMainWindow(self):

        self.setObjectName('MainWindow')

        # Устанавливаем иконку
        app_icon = QtGui.QIcon()
        app_icon.addFile('Нужное/favicon_32.ico', QtCore.QSize(32, 32))
        app_icon.addFile('Нужное/favicon_48.ico', QtCore.QSize(48, 48))
        app_icon.addFile('Нужное/favicon_64.ico', QtCore.QSize(64, 64))
        app_icon.addFile('Нужное/favicon_72.ico', QtCore.QSize(72, 72))
        app_icon.addFile('Нужное/favicon_96.ico', QtCore.QSize(96, 96))
        self.setWindowIcon(app_icon)

        # Окно настроик
        self.win_settings = False

        # Загрузка данных
        maiThr.loadMd()

        # Поверх всех окон
        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose)

        # Расположение и размер главного окна
        self.location_on_the_screen()

        # EventFilter на все окно
        self.installEventFilter(self)

        # Инициализируем QSystemTrayIcon
        self.trayIcon = Tr.TrayIcon(self, 8)

        # Размер TitleBar
        self.setTitleBarHeight(20)
        self.titleBar.buttonClose.setMinimumWidth(50)
        self.titleBar.buttonMinimum.hide()
        self.titleBar.buttonMaximum.hide()

        # Иконка для pushButton_settings
        app_icon = QtGui.QIcon()
        app_icon.addFile('Нужное/Настройки.png', QtCore.QSize(20, 20))

        # Кнопка настроик
        self.pushButton_settings = QtWidgets.QPushButton()
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.pushButton_settings.setText("")
        self.pushButton_settings.setMinimumHeight(20)
        self.pushButton_settings.setIcon(app_icon)
        self.titleBar.layout_custom_widget.addWidget(self.pushButton_settings)
        self.horizontalSpacer_2 = QtWidgets.QSpacerItem(5, 20)
        self.titleBar.layout_custom_widget.addItem(self.horizontalSpacer_2)

        # Авто пойск
        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setObjectName("checkBox_autoFind")
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setText("Авто пойск")
        self.checkBox.setChecked(True)
        self.titleBar.layout_custom_widget.addWidget(self.checkBox)
        self.horizontalSpacer_1 = QtWidgets.QSpacerItem(30, 20)
        self.titleBar.layout_custom_widget.addItem(self.horizontalSpacer_1)

        # Добавляем Widget
        self.widget = MainWindowWidget(main=self)
        self.setWidget(self.widget)

        # Устанавливаем данные в окно
        self.set_value()

        # Устанавливаем коннекторы
        self.set_connect()

        # Устанавливаем свои стили
        self.setMyStyle()

    def set_value(self):
        if maiThr.md['Имя_файла'] != '':
            # self.pushButton_selectFile.setText(maiThr.md['Имя_файла'])
            pass

    def set_connect(self):
        # Настройки
        self.pushButton_settings.clicked.connect(self.settings_show)

        # Выбор файла
        # self.pushButton_selectFile.clicked.connect(self.selectFile)
        pass

    def setMyStyle(self):
        style = """
				#pushButton_settings
				{
					background-color: rgb(54, 157, 180);
				}
				#checkBox_autoFind
				{
				    color: rgb(0, 0, 0);
				}
				"""
        Fr.STYLE_SHEET = Fr.STYLE_SHEET + style
        self.setStyleSheet(Fr.STYLE_SHEET)

    def closeEvent(self, event):
        maiThr.md['Размер_окна'] = [self.size().width(), self.size().height()]
        maiThr.md['Расположение_окна'] = [self.geometry().left(), self.geometry().top()]
        maiThr.upDate_json()

        # print(self.isVisible())

        if self.widget.MainThread.threading:
            event.ignore()
            self.hide()
            self.widget.MainThread.threading = False
        else:
            event.accept()
            self.deleteLater()
            self.trayIcon.exit()

    def exit_action(self):
        try:

            print('Закрытие через трей')
            self.widget.MainThread.threading = False
            del self.widget.MainThread.Excel
            if self.win_settings:
                self.win_settings.close()

            self.close()

        except:
            pass

    def show_action(self):
        # Запускаем дополнительный поток
        try:
            if not self.widget.MainThread.threading:
                self.widget.MainThread = maiThr.MainThreading(parent=self, widget=self.widget)
                self.widget.MainThread.start()
                self.show()
        except:
            pass

    def location_on_the_screen(self):
        self.setGeometry(maiThr.md['Расположение_окна'][0],
                         maiThr.md['Расположение_окна'][1],
                         maiThr.md['Размер_окна'][0],
                         maiThr.md['Размер_окна'][1])

    def eventFilter(self, source, event):

        if source.objectName() == 'MainWindow':

            if event.type() == QtCore.QEvent.Enter:
                self.widget.cell_clicked = True
                # Сброс курсора
                self.unsetCursor()
                self.setFocus()

            if event.type() == QtCore.QEvent.Leave:
                self.widget.cell_clicked = False

        return False

    def settings_show(self):
        if not self.win_settings:
            self.win_settings = SettingsWindow.SettingsFrame(main=self)
            self.win_settings.setObjectName('win_settings')
            self.win_settings.show()


class MainWindowWidget(QWidget, Drilling_modes_win.Ui_drilling_modes):
    def __init__(self, main=None):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = main

        self.initMainWindow()

    def initMainWindow(self):

        self.setObjectName('Widget')

        # Конектим пользовательский сигнал на Widget
        self.Commun = Communicate()
        self.Commun.rowTable_change.connect(self.rowTable_change)
        self.Commun.table_change.connect(self.table_change)
        self.Commun.table_clear.connect(self.table_clear)

        # Запускаем дополнительный поток
        self.MainThread = maiThr.MainThreading(parent=self.mainWindow, widget=self)
        self.MainThread.start()

        self.tableWidget.cellClicked.connect(self.cellClicked)
        self.mainWindow.checkBox.clicked.connect(self.autoFind)
        self.textBrowser_footer.textChanged.connect(self.sizeChange)  # Подключаем слот sizeChange (авто изменение размера textBrowser_footer)

        # Устанавливаем цвет выделения строк
        palette = self.tableWidget.palette()
        palette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtGui.QColor(197, 95, 82)))
        palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.tableWidget.setPalette(palette)

        # Колличество строка в которых нету тех. параметров (устанавливаем текст в titleBar)
        self.totalRows = 0

        # Выделеная строка
        self.rowSelected = 0

        self.cell_clicked = False

    def rowTable_change(self, data):

        if maiThr.md['Тип_рапорта'] == 'Сводка Башнефть':
            return

        row, write = data[0], data[1]

        self.tableWidget.item(row, 3).setText(write)
        if self.totalRows == 1:
            self.tableWidget.item(row, 0).setSelected(False)
            self.tableWidget.item(row, 1).setSelected(False)
            self.tableWidget.item(row, 2).setSelected(False)
            self.tableWidget.item(row, 3).setSelected(False)
            self.rowSelected = 0

        # Проверяем стоит ли галочка на выбранной строке если нет то выбираем следующию строку
        for i in range(row + 1, self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 3).checkState() == QtCore.Qt.Checked and not re.search(r"Qвх=", self.tableWidget.item(i, 3).text()):
                self.tableWidget.scrollToItem(self.tableWidget.selectRow(0), QAbstractItemView.PositionAtCenter)
                self.tableWidget.selectRow(i)
                self.rowSelected = i
                break

        # Колличество строка в которых нету тех. параметров (устанавливаем текст в titleBar)
        self.totalRows -= 1
        self.textBrowser_footer.setText(f"Cтрок для установки тех. параметров {self.totalRows}")

    def table_change(self, Data):
        # Сброс курсора
        self.mainWindow.unsetCursor()

        data = Data[0]
        modes = None

        if maiThr.md['Тип_рапорта'] == 'Сводка Башнефть':
            pattern = ['Бурение слайд', 'Бурение', 'Промывка', 'Замер', 'Проработка', 'Программ', '\w{2,}']

            for j in range(1, len(data['Строка'])):
                for i in pattern:
                    if re.search(i, data['Описание'][j]) and data['Расход'][j] is not None:
                        # Vмех=25,23м/ч; G=4-12т; Qвх=28л/с; Рвх=90-115атм; N=50об/мин; Мкр=22-26кН*м;

                        if data['От'][j] != '00:00':
                            tm_1 = datetime.datetime.strptime(data['От'][j], '%H:%M')
                            tm_2 = datetime.datetime.strptime(data['До'][j], '%H:%M')
                            tm = (tm_2 - tm_1).seconds / 60 / 60
                        else:
                            a = time.strptime(data['До'][j], "%H:%M")
                            b = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).seconds
                            tm = b / 60 / 60

                        # Проходка
                        d = re.findall(r'\d+[-]\d+', data['Описание'][j])
                        if len(d) > 0:
                            d = int(d[0].split('-')[1]) - int(d[0].split('-')[0])

                        if i == 'Бурение слайд':
                            modes = f"Vмех={round((d) / (tm), 2)}м/ч; " \
                                    f"G={data['Нагрузка'][j]}т; " \
                                    f"Qвх={data['Расход'][j]}л/с; " \
                                    f"Рвх={data['Давление'][j]}атм; " \
                                    f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                    f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                    f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                        elif i == 'Бурение':
                            modes = f"Vмех={round((d) / (tm), 2)}м/ч; " \
                                    f"G={data['Нагрузка'][j]}т; " \
                                    f"Qвх={data['Расход'][j]}л/с; " \
                                    f"Рвх={data['Давление'][j]}атм; " \
                                    f"N={data['Обороты'][j]}об/мин; " \
                                    f"Мкр={data['Момент'][j]}кН*м; " \
                                    f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                    f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                    f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                        elif i == 'Промывка' or i == 'Замер':
                            modes = f"Qвх={data['Расход'][j]}л/с; " \
                                    f"Рвх={data['Давление'][j]}атм; " \
                                    f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                    f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                    f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                        elif i == 'Проработка' or i == 'Программ':
                            modes = f"Qвх={data['Расход'][j]}л/с; " \
                                    f"Рвх={data['Давление'][j]}атм; " \
                                    f"N={data['Обороты'][j]}об/мин; " \
                                    f"Мкр={data['Момент'][j]}кН*м; " \
                                    f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                    f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                    f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                        else:
                            if data['Обороты'][j] == 0:
                                modes = f"Qвх={data['Расход'][j]}л/с; " \
                                        f"Рвх={data['Давление'][j]}атм; " \
                                        f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                        f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                        f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                            else:
                                modes = f"Qвх={data['Расход'][j]}л/с; " \
                                        f"Рвх={data['Давление'][j]}атм; " \
                                        f"N={data['Обороты'][j]}об/мин; " \
                                        f"Мкр={data['Момент'][j]}кН*м; " \
                                        f"N_нас1={data['Насос_1'][j]}ход/мин; " \
                                        f"N_нас2={data['Насос_2'][j]}ход/мин; " \
                                        f"Эл.пр-ть_вых.={data['Электропроводность_вых'][j]}См/м;"
                        modes = re.sub(r'[.]', ',', modes)
                        data['Описание'][j] = f"{data['Описание'][j]} {modes}"
                        break

        if len(data['Строка']) != self.tableWidget.rowCount():
            print(f"Колличество строк изменилось {len(data['Строка'])} / {self.tableWidget.rowCount()}")
            # Добавляем строки с данными в окно
            self.tableWidget.setRowCount(len(data['Строка']))  # Добавляем строки
            self.cell_clicked = False

        # Обновляем строки в таблице
        for i in range(1, len(data['Строка'])):
            try:
                if self.tableWidget.item(i, 3).text() != data['Описание'][i]:
                    print(f"tableWidget {self.tableWidget.item(i, 3).text()}")
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{data['От'][i]}"))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{data['До'][i]}"))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{data['Забой'][i]}"))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(f"{data['Описание'][i]}"))
            except:
                self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{data['От'][i]}"))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{data['До'][i]}"))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{data['Забой'][i]}"))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(f"{data['Описание'][i]}"))
            # print(f"tableWidget {self.tableWidget.item(i, 3).text()}")

            # Устанавливаем галочки на те строки в которые можно устанавливать тех. параметры
            text = f"{data['Описание'][i]}"
            reText = re.search(r"\w+", text)[0]

            if reText in maiThr.md['Операции']:
                self.tableWidget.item(i, 3).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.tableWidget.item(i, 3).setCheckState(QtCore.Qt.Checked)

        # Подсчитываем колличество строк в которых нужно установить тех. параметры, после выделяем самою первою строку
        row = 0
        self.totalRows = 0
        for i in range(1, len(data['Строка'])):
            if self.tableWidget.item(i, 3).checkState() == QtCore.Qt.Checked:
                if not re.search(r"Qвх=", self.tableWidget.item(i, 3).text()):
                    self.totalRows += 1
                    if row == 0:
                        row = i

        # Выделяем первою строку на которой надо установить тех. параметры
        if row > 0 and self.mainWindow.checkBox.isChecked() and not self.cell_clicked:
            self.tableWidget.scrollToItem(self.tableWidget.selectRow(0), QAbstractItemView.PositionAtCenter)
            self.tableWidget.selectRow(row)
            self.rowSelected = row

        # Колличество строка в которых нету тех. параметров (устанавливаем текст в titleBar)
        self.textBrowser_footer.setText(f"Cтрок для установки тех. параметров {self.totalRows}")

    def table_clear(self, data):
        # print("table_clear")
        # Устанавливаем текст в titleBar
        self.textBrowser_footer.setText(f"Сводка закрыта, либо нужно выйте из режима редактирования")
        # if read_data == False and open_excel:
        # 	self.textBrowser_footer.setText(f"Выйдети из ячейки!")

        self.tableWidget.setRowCount(1)  # Удаляем строки

        self.tableWidget.item(0, 0).setSelected(False)
        self.tableWidget.item(0, 1).setSelected(False)
        self.tableWidget.item(0, 2).setSelected(False)
        self.tableWidget.item(0, 3).setSelected(False)

    def cellClicked(self, row):

        self.mainWindow.checkBox.setChecked(False)
        text = self.tableWidget.item(row, 3).text()
        reText = re.search(r"\w+", text)[0]
        self.rowSelected = row

        if self.tableWidget.item(row, 3).checkState() == QtCore.Qt.Unchecked:
            if not reText in maiThr.md['Операции']:
                maiThr.md['Операции'].append(reText)
                maiThr.upDate_json()
                print(maiThr.md)
                # Убирам галочки в строках в которых есть точно такая же операция
                for i in range(1, self.tableWidget.rowCount()):
                    if re.search(reText, self.tableWidget.item(i, 3).text()):
                        self.tableWidget.item(i, 3).setCheckState(QtCore.Qt.Unchecked)

        if self.tableWidget.item(row, 3).checkState() == QtCore.Qt.Checked:
            if reText in maiThr.md['Операции']:
                maiThr.md['Операции'].remove(reText)
                maiThr.upDate_json()
                print(maiThr.md)
                # Ставим галочки в строках в которых есть точно такая же операция
                for i in range(1, self.tableWidget.rowCount()):
                    if re.search(reText, self.tableWidget.item(i, 3).text()):
                        self.tableWidget.item(i, 3).setCheckState(QtCore.Qt.Checked)

            # Выделяем первою строку на которой надо установить тех. параметры
            # for i in range(1, len(self.MainThread.excel.readData['Строка'])):
            # 	if self.tableWidget.item(i, 3).checkState() == QtCore.Qt.Checked and not re.search(r"Qвх=", self.tableWidget.item(i, 3).text()):
            # 		self.tableWidget.scrollToItem(self.tableWidget.selectRow(0), QAbstractItemView.PositionAtCenter)
            # 		self.tableWidget.selectRow(i)
            # 		print(f"scrollToItem")
            # 		break

        # Подсчитываем колличество строк в которых нужно установить тех. параметры, после выделяем самою первою строку
        self.totalRows = 0
        for i in range(1, len(self.MainThread.readData['Строка'])):
            if self.tableWidget.item(i, 3).checkState() == QtCore.Qt.Checked and not re.search(r"Qвх=", self.tableWidget.item(i, 3).text()):
                self.totalRows += 1

        # Колличество строка в которых нету тех. параметров (устанавливаем текст в titleBar)
        self.textBrowser_footer.setText(f"Cтрок для установки тех. параметров {self.totalRows}")

    def autoFind(self):
        if self.mainWindow.checkBox.isChecked():
            self.cell_clicked = False
            if self.rowSelected > 0:
                self.tableWidget.item(self.rowSelected, 0).setSelected(False)
                self.tableWidget.item(self.rowSelected, 1).setSelected(False)
                self.tableWidget.item(self.rowSelected, 2).setSelected(False)
                self.tableWidget.item(self.rowSelected, 3).setSelected(False)
                self.rowSelected = 0
        else:
            self.cell_clicked = True

    def sizeChange(self):
        docHeight = self.textBrowser_footer.document().size().height()
        if self.minimumHeight() <= docHeight <= self.maximumHeight():
            self.textBrowser_footer.setMinimumHeight(docHeight)
