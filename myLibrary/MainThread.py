from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import time
import clipboard
import re
import pythoncom
import win32com.client
import json

md = {
    'Операции': [],
    'Размер_окна': [600, 300],
    'Расположение_окна': [0, 0],
    'Имя_файла': '',
    'Тип_рапорта': 'Сводка Башнефть'
}


class Report:
    def __init__(self):
        self.cogalm = 'Сводка Когалымская'
        self.bashneft = 'Сводка Башнефть'


class ReadClipboard():
    def __init__(self):
        self.initReadClipboard()

    def initReadClipboard(self):
        self.mainData = {'Давление': [0, 0], 'Нагрузка': [0, 0], 'Расход': [0, 0], 'Обороты': [0, 0], 'Момент': [0, 0], 'Насос_1': [0, 0],
                         'Насос_2': [0, 0], 'Электропроводность_вых': [0, 0]}
        self.lastData = ''
        self.newData = ''
        clipboard.copy('')

    def read_clipboard(self):

        self.newData = re.sub(r'[,]', '..', clipboard.paste())

        if self.lastData != self.newData and re.search(r'Давление ПЖ на входе', self.newData):

            self.upDataLasData()

            reData = re.sub(r'[.]+', '.', self.newData)
            pattern = r'.*\n'
            reData = re.findall(pattern, reData)

            pattern = r'(\d+[.]\d+|\s\d+\s)'

            for j in reData:
                min, max, avr = 0, 0, 0
                if re.search(r'(Давление|'
                             r'Нагрузка|'
                             r'Расход ПЖ на входе|'
                             r'Обороты ротора|'
                             r'Крутящий момент ротора|'
                             r'Ходы насоса-1|'
                             r'Ходы насоса-2|'
                             r'Электропроводность вых)', j):
                    min = float(re.findall(pattern, j)[2])
                    max = float(re.findall(pattern, j)[1])
                    avr = float(re.findall(pattern, j)[0])

                if re.search(r'Давление ПЖ на входе', j):
                    print(min, max, avr)
                    self.mainData['Давление'] = [self.myround(min, 5), self.myround(max, 5), self.myround(avr, 5)]

                if re.search(r'Нагрузка на долото', j):
                    self.mainData['Нагрузка'] = [round(min), round(max), round(avr)]

                if re.search(r'Расход ПЖ на входе', j):
                    self.mainData['Расход'] = [self.myround(min, 1), self.myround(max, 1), self.myround(avr, 1)]

                if re.search(r'Обороты ротора', j):
                    self.mainData['Обороты'] = [self.myround(min, 5), self.myround(max, 5), self.myround(avr, 5)]

                if re.search(r'Крутящий момент ротора', j):
                    self.mainData['Момент'] = [round(min), round(max), round(avr)]

                if re.search(r'Ходы насоса-1', j):
                    self.mainData['Насос_1'] = [self.myround(min, 1), self.myround(max, 1), self.myround(avr, 1)]

                if re.search(r'Ходы насоса-2', j):
                    self.mainData['Насос_2'] = [self.myround(min, 1), self.myround(max, 1), self.myround(avr, 1)]

                if re.search(r'Электропроводность вых', j):
                    self.mainData['Электропроводность_вых'] = [round(min, 1), round(max, 1), round(avr, 1)]

            print(f"read {self.mainData}")
            return True
        else:
            return False

    def myround(self, x, base=5):
        return base * round(x / base)

    def upDataLasData(self):
        self.lastData = self.newData


class Excel(Report):
    def __init__(self, parent=None):
        super().__init__()
        self.initExcel()

    def initExcel(self):

        self.Excel = None
        self.workBook = None
        self.sheet = None
        self.resultWrite = None
        self.dataForFrame = None
        self.writeData = {'Давление': '', 'Нагрузка': '', 'Расход': '', 'Обороты': '', 'Момент': ''}
        self.readData = {'Строка': [None], 'От': [None], 'До': [None], 'Забой': [None], 'Описание': [None]}
        self.read_data = True
        self.open_excel = False

    def openExcel(self):

        try:
            if not self.open_excel:
                # Показываем что СОМ объект будет использовать в отдельном потоке
                # noinspection PyUnresolvedReferences
                pythoncom.CoInitialize()

                # Cоздадим COM объект
                self.Excel = win32com.client.Dispatch("Excel.Application")

                if self.Excel.Application.Workbooks.Count > 0:
                    if not self.set_properti_excel():
                        return False

                    # Проверяем наличие открытой сводки
                    for i in range(1, self.Excel.Application.Workbooks.Count + 1):
                        if md['Имя_файла'] == self.Excel.Application.Workbooks(i).Name:
                            self.workBook = self.Excel.Application.Workbooks(i)
                            break

                if self.workBook == None:
                    return False

                # Выбираем лист "Стр. 1"
                if md['Тип_рапорта'] == self.cogalm:
                    self.sheet = self.workBook.Sheets("Хронометраж")
                if md['Тип_рапорта'] == self.bashneft:
                    self.sheet = self.workBook.Sheets("03.Сводка")

                # print(f"openExcel Имя файла {self.workBook.Name}")
                # print(f"openExcel Имя листа {self.sheet.Name}")

                self.open_excel = True
                print(f"open_excel")

            return True

        except:

            self.open_excel = False
            # print(f"not_open_excel")
            return False

    def readExcel(self):
        try:
            if md['Тип_рапорта'] == self.cogalm:
                # Номер первой строки найденная по дате
                row = self.Excel.Application.WorksheetFunction.Match(self.workBook.Sheets("Стр. 1").Cells(5, 5), self.sheet.Columns("C:C"))

                # Массив данных с листа Хронометраж
                data = self.sheet.Range(self.sheet.Cells(row, 5), self.sheet.Cells(row + 1000, 38)).Value

                self.readData = {'Строка': [None], 'От': [None], 'До': [None], 'Операция': [None], 'Забой': [None], 'Описание': [None]}

                for i in data:

                    if i[1] == None:
                        break
                    start = time.strftime('%H:%M', time.gmtime(round(i[0] * 24 * 60 * 60, 2)))
                    stop = time.strftime('%H:%M', time.gmtime(round(i[1] * 24 * 60 * 60, 2)))

                    self.readData['Строка'].append(row)
                    self.readData['От'].append(start)
                    self.readData['До'].append(stop)
                    self.readData['Операция'].append(i[3])
                    self.readData['Забой'].append(i[32])
                    self.readData['Описание'].append(i[4])
                    row += 1

                # print(f"read")
                return True

            if md['Тип_рапорта'] == self.bashneft:
                data = self.sheet.Range(self.sheet.Cells(49, 2), self.sheet.Cells(298, 29)).Value
                self.readData = {'Строка': [None],
                                 'От': [None],
                                 'До': [None],
                                 'Операция': [None],
                                 'Забой': [None],
                                 'Описание': [None],
                                 'Vмех': [None],
                                 'Нагрузка': [None],
                                 'Давление': [None],
                                 'Расход': [None],
                                 'Момент': [None],
                                 'Обороты': [None],
                                 'Насос_1': [None],
                                 'Насос_2': [None],
                                 'Электропроводность_вых': [None], }
                row = 49
                hour_24 = False

                for i in data:

                    if i[1] == None or i[15] == None or (re.search(r'Бурение', i[15]) and i[3] == None):
                        if not hour_24:
                            break
                        else:
                            row += 1
                            continue
                    iStart = time.strftime('%H:%M', time.gmtime(round(i[0] * 24 * 60 * 60, 2)))
                    iStop = time.strftime('%H:%M', time.gmtime(round(i[1] * 24 * 60 * 60, 2)))

                    if iStop == '00:00':
                        hour_24 = True

                    self.readData['Строка'].append(row)
                    self.readData['От'].append(iStart)
                    self.readData['До'].append(iStop)
                    self.readData['Операция'].append(i[6])
                    self.readData['Забой'].append(i[3])
                    self.readData['Описание'].append(i[15])
                    self.readData['Vмех'].append(i[18])
                    self.readData['Нагрузка'].append(i[19])
                    self.readData['Давление'].append(i[20])
                    self.readData['Расход'].append(i[21])
                    self.readData['Момент'].append(i[22])
                    self.readData['Обороты'].append(i[23])
                    self.readData['Насос_1'].append(int(i[24])) if i[24] is not None else self.readData['Насос_1'].append(i[24])
                    self.readData['Насос_2'].append(int(i[25])) if i[25] is not None else self.readData['Насос_2'].append(i[25])
                    self.readData['Электропроводность_вых'].append(i[26])
                    row += 1

                # print(f"read")
                return True

        except:

            print(f"not read")
            self.open_excel = False
            return False

    def writeToExcel(self, data=None, row=None):
        print(f"data {data},n\ row {row}")
        if md['Тип_рапорта'] == self.cogalm:
            # Запуск макроса из VBA
            try:
                for i in range(1, len(self.readData['Строка'])):
                    if self.readData['Операция'][i] == None or self.readData['Забой'][i] == None:
                        self.sheet.Cells(self.readData['Строка'][i], 9).Select()
                        self.Excel.Application.Run("Макросы.xlsb!Когалымская_сводка.Операции_интервалы")
            except:
                pass

            pattern = ['Бурение слайд', 'Бурение', 'Промывка', 'Замер', 'Проработка', 'Программ', 'Насос_1', 'Насос_2', 'Электропроводность_вых',
                       '\w{2,}']

            if data['Нагрузка'][1] - data['Нагрузка'][0] >= 1 and data['Нагрузка'][0] > 0:
                self.writeData['Нагрузка'] = f"G={data['Нагрузка'][0]}-{data['Нагрузка'][1]}т;"
            elif data['Нагрузка'][0] < 1:
                self.writeData['Нагрузка'] = f"G={data['Нагрузка'][2]}т;"
            else:
                self.writeData['Нагрузка'] = f"G={data['Нагрузка'][2]}т;"

            if data['Расход'][1] - data['Расход'][0] >= 3 and data['Расход'][0] > 0:
                self.writeData['Расход'] = f"Qвх={data['Расход'][0]}-{data['Расход'][1]}л/с;"
            elif data['Расход'][0] < 1:
                self.writeData['Расход'] = f"Qвх={data['Расход'][1]}л/с;"
            else:
                self.writeData['Расход'] = f"Qвх={data['Расход'][2]}л/с;"

            if data['Давление'][1] - data['Давление'][0] >= 4 and data['Давление'][0] > 0:
                self.writeData['Давление'] = f"Pвх={data['Давление'][0]}-{data['Давление'][1]}атм;"
            elif data['Давление'][0] < 1:
                self.writeData['Давление'] = f"Pвх={data['Давление'][1]}атм;"
            else:
                self.writeData['Давление'] = f"Pвх={data['Давление'][2]}атм;"

            if data['Обороты'][1] - data['Обороты'][0] >= 5 and data['Обороты'][0] > 0:
                self.writeData['Обороты'] = f"N={data['Обороты'][0]}-{data['Обороты'][1]}об/мин;"
            elif data['Обороты'][0] < 2:
                self.writeData['Обороты'] = f"N={data['Обороты'][1]}об/мин;"
            else:
                self.writeData['Обороты'] = f"N={data['Обороты'][2]}об/мин;"

            if data['Момент'][1] - data['Момент'][0] >= 2 and data['Момент'][0] > 0:
                self.writeData['Момент'] = f"M={data['Момент'][0]}-{data['Момент'][1]}кН*м;"
            elif data['Момент'][0] < 1:
                self.writeData['Момент'] = f"M={data['Момент'][1]}кН*м;"
            else:
                self.writeData['Момент'] = f"M={data['Момент'][2]}кН*м;"

            # Режим бурения
            for i in pattern:
                if re.search(i, self.sheet.Cells(row, 9).value):

                    if i == 'Бурение слайд':
                        self.resultWrite = f"" \
                                           f"{self.writeData['Нагрузка']} " \
                                           f"{self.writeData['Расход']} " \
                                           f"{self.writeData['Давление']}"

                    elif i == 'Бурение':
                        self.resultWrite = f"" \
                                           f"{self.writeData['Нагрузка']} " \
                                           f"{self.writeData['Расход']} " \
                                           f"{self.writeData['Давление']} " \
                                           f"{self.writeData['Обороты']} " \
                                           f"{self.writeData['Момент']}"

                    elif i == 'Промывка' or i == 'Замер':
                        if data['Обороты'][2] > 4:
                            self.resultWrite = f"" \
                                               f"{self.writeData['Расход']} " \
                                               f"{self.writeData['Давление']} " \
                                               f"{self.writeData['Обороты']} " \
                                               f"{self.writeData['Момент']}"
                        else:
                            self.resultWrite = f"" \
                                               f"{self.writeData['Расход']} " \
                                               f"{self.writeData['Давление']}"

                    elif i == 'Проработка' or i == 'Программ':
                        self.resultWrite = f"" \
                                           f"{self.writeData['Расход']} " \
                                           f"{self.writeData['Давление']} " \
                                           f"{self.writeData['Обороты']} " \
                                           f"{self.writeData['Момент']}"

                    else:
                        if data['Обороты'][2] > 4:
                            self.resultWrite = f"" \
                                               f"{self.writeData['Расход']} " \
                                               f"{self.writeData['Давление']} " \
                                               f"{self.writeData['Обороты']} " \
                                               f"{self.writeData['Момент']}"
                        else:
                            self.resultWrite = f"" \
                                               f"{self.writeData['Расход']} " \
                                               f"{self.writeData['Давление']}"
                    break

            cell_data = self.sheet.Cells(row, 9).value
            vmex = 0

            # Обновляем интервал бурения и Vмех
            if re.search(r'Бурение', cell_data):

                if self.sheet.Cells(row, 37).value != None and self.sheet.Cells(row - 1, 37).value != None:

                    start = self.sheet.Cells(row - 1, 37).value

                    if start % 1 == 0:
                        start = round(start)
                    else:
                        start = re.sub(r'[.]', ',', f"{start}")

                    stop = self.sheet.Cells(row, 37).value

                    if stop % 1 == 0:
                        stop = round(stop)
                    else:
                        stop = re.sub(r'[.]', ',', f"{stop}")

                    vmex = round((stop - start) / (self.sheet.Cells(row, 7).value * 24), 2)

                    if vmex % 1 == 0:
                        vmex = round(vmex)
                    else:
                        vmex = re.sub(r'[.]', ',', f"{vmex}")

                    data = f" в инт. {start}-{stop}м."

                    pattern = r'(\s+в\s*инт[.]\s*\d+\s*[-]\s*\d*м[.]*)'

                    # Ставим
                    # Бурение в инт. 250-265м.
                    # Бурение слайд в инт. 250-265м.
                    if re.search(pattern, cell_data):
                        cell_data = re.sub(pattern, data, cell_data)
                    else:
                        if re.search(r'Бурение слайд', cell_data):
                            cell_data = re.sub(r'Бурение слайд[.]*', f"Бурение слайд{data}", cell_data)
                        else:
                            cell_data = re.sub(r'Бурение[.]*', f"Бурение{data}", cell_data)
                    print(f"cell_data {cell_data}")

            # Если бурение то добавляем в конец Vмех и заменяем точки на запятые
            # (G=7-12т; Qвх=32л/с; Pвх=175-205атм; N=50об/мин; M=2-14кН*м; Vмех=30м/ч;)
            if re.search(r'Бурение', cell_data):
                self.resultWrite = f"({re.sub(r'[.]', ',', self.resultWrite)} Vмех={vmex}м/ч;)"
            else:
                self.resultWrite = f"({re.sub(r'[.]', ',', self.resultWrite)})"


            # Если режимы бурения уже установлены то заменяем их на новые режимы
            # Бурение в инт. 250-265м. (G=7-12т; Qвх=32л/с; Pвх=175-205атм; N=50об/мин; M=2-14кН*м; Vмех=30м/ч;)
            pattern = r'[(]*(G=.+м/ч;|Qвх.+кН.м.|Qвх.+атм.)[)]*'
            if re.search(pattern, cell_data):
                self.resultWrite = re.sub(pattern, self.resultWrite, cell_data)
            else:
                self.resultWrite = f"{cell_data} {self.resultWrite}"

            self.sheet.Cells(row, 9).value = re.sub(r'\s+', ' ', self.resultWrite)

            self.dataForFrame = self.resultWrite
            print(f"resultWrite {self.resultWrite}")

        if md['Тип_рапорта'] == self.bashneft:

            # Запуск макроса из VBA
            try:
                for i in range(1, len(self.readData['Строка'])):
                    if self.readData['Операция'][i] == None or self.readData['Забой'][i] == None:
                        self.sheet.Cells(self.readData['Строка'][i], 17).Select()
                        self.Excel.Application.Run("Макросы.xlsb!Башкирская_сводка.Цели_Операции_инт_гл_id")
            except:
                pass

            pattern = ['Бурение слайд', 'Бурение', 'Промывка', 'Замер', 'Проработка', 'Программ', '\w{2,}']
            # Режим бурения
            # V мех., м/ч;	Нагр. на долото, т;	Давл. на вх., Атм;	Расход ПЖ, л/с;	Момент кН*м; Обор. рот, об/мин;	Н1, ход/ мин;	Н2, ход/ мин; Эл.пр-ть на вых. См/м;
            print(self.sheet.Cells(row, 17).value)
            for i in pattern:
                if re.search(i, self.sheet.Cells(row, 17).value):
                    if i == 'Бурение слайд':
                        self.resultWrite = [data['Нагрузка'][2],
                                            data['Давление'][2],
                                            data['Расход'][2],
                                            0,
                                            0,
                                            data['Насос_1'][2],
                                            data['Насос_2'][2],
                                            data['Электропроводность_вых'][2]
                                            ]
                    elif i == 'Бурение':
                        self.resultWrite = [data['Нагрузка'][2],
                                            data['Давление'][2],
                                            data['Расход'][2],
                                            data['Момент'][2],
                                            data['Обороты'][2],
                                            data['Насос_1'][2],
                                            data['Насос_2'][2],
                                            data['Электропроводность_вых'][2]
                                            ]
                    elif i == 'Промывка' or i == 'Замер':
                        self.resultWrite = [0,
                                            data['Давление'][2],
                                            data['Расход'][2],
                                            0,
                                            0,
                                            data['Насос_1'][2],
                                            data['Насос_2'][2],
                                            data['Электропроводность_вых'][2]
                                            ]
                    elif i == 'Проработка' or i == 'Программ':
                        self.resultWrite = [0,
                                            data['Давление'][2],
                                            data['Расход'][2],
                                            data['Момент'][2],
                                            data['Обороты'][2],
                                            data['Насос_1'][2],
                                            data['Насос_2'][2],
                                            data['Электропроводность_вых'][2]
                                            ]
                    else:
                        if self.writeData['Обороты'] == "N=0об/мин;":
                            self.resultWrite = [0,
                                                data['Давление'][2],
                                                data['Расход'][2],
                                                0,
                                                0,
                                                data['Насос_1'][2],
                                                data['Насос_2'][2],
                                                data['Электропроводность_вых'][2]
                                                ]
                        else:
                            self.resultWrite = [0,
                                                data['Давление'][2],
                                                data['Расход'][2],
                                                data['Момент'][2],
                                                data['Обороты'][2],
                                                data['Насос_1'][2],
                                                data['Насос_2'][2],
                                                data['Электропроводность_вых'][2]
                                                ]
                    break

            print(f"resultWrite {self.resultWrite}")

            # Режимы
            index = 0
            for i in range(21, 29):
                if self.resultWrite[index] != 0:
                    self.sheet.Cells(row, i).value = self.resultWrite[index]
                index += 1

            # Мех скорость
            if re.search('Бурение', self.sheet.Cells(row, 17).value):
                self.sheet.Cells(row, 20).value = """=IFERROR((RC[-15]-R[-1]C[-15])/(SUMIF(RC[-3], "Бурение*", RC[-16])*24),)"""

    def set_properti_excel(self):
        try:
            self.Excel.Application.DisplayAlerts = False
            self.Excel.Application.ScreenUpdating = True
            # self.Excel.Application.visible = True
            return True

        except:
            print("except")

            return False


# Считываем данных с setting.txt
def loadMd():
    global md

    try:
        md = json.load(open('Нужное/setting.txt'))
        print(f"Данные setting загружены {md}")

    except:
        upDate_json()
        print(f"Данных нет {md}")


# Сохраняем данные в setting.txt
def upDate_json():
    global md

    temp_md = {}
    temp_md.update(md)
    setting_json = open('Нужное/setting.txt', 'w')
    json.dump(temp_md, setting_json, sort_keys=True, indent=4, ensure_ascii=False)
    setting_json.close()


# Объект, который будет перенесён в другой поток для выполнения кода
class MainThreading(QThread, Excel, ReadClipboard):
    def __init__(self, parent=None, widget=None):
        super().__init__()
        self.mainWindow = parent
        self.widget = widget
        self.initMainThreading()
        self.threading = True

    def initMainThreading(self):

        loadMd()
        self.initExcel()
        self.initReadClipboard()

    # Метод, который будет выполнять алгоритм в другом потоке
    def run(self):

        print("run Запуск нового потока")

        while self.threading:

            QtCore.QThread.msleep(500)

            # Считываем данные с Excel
            if self.openExcel() and self.readExcel():

                # Посылаем сигнал из второго потока в GUI поток в окно Drilling_modes_win (обновляем строки в таблици)
                self.widget.Commun.table_change.emit([self.readData])

                if self.read_clipboard():  # Чтение буфера обмена

                    for i in self.widget.tableWidget.selectedIndexes():
                        # Записываем тех. параметры в Excel
                        self.writeToExcel(data=self.mainData, row=self.readData['Строка'][i.row()])

                        # Посылаем сигнал из второго потока в GUI поток в окно Drilling_modes_win (замена текста в выбранной строке таблицы)
                        self.widget.Commun.rowTable_change.emit([i.row(), f"{self.dataForFrame}"])
                        break

            else:
                # Посылаем сигнал из второго потока в GUI поток в окно Drilling_modes_win (Удаляем все стоки)
                self.widget.Commun.table_clear.emit(self.open_excel)
