# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Programming\Python\Goblin_drilling_v.2.2\Lib\site-packages\QtDesigner\Drilling_modes_win.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_drilling_modes(object):
    def setupUi(self, drilling_modes):
        drilling_modes.setObjectName("drilling_modes")
        drilling_modes.resize(623, 606)
        drilling_modes.setMinimumSize(QtCore.QSize(600, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(drilling_modes)
        self.verticalLayout.setContentsMargins(1, 0, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(drilling_modes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(139, 197, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(139, 197, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(139, 197, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(139, 197, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(0, 3, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.textBrowser_footer = QtWidgets.QTextBrowser(drilling_modes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textBrowser_footer.sizePolicy().hasHeightForWidth())
        self.textBrowser_footer.setSizePolicy(sizePolicy)
        self.textBrowser_footer.setMinimumSize(QtCore.QSize(0, 21))
        self.textBrowser_footer.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textBrowser_footer.setBaseSize(QtCore.QSize(0, 0))
        self.textBrowser_footer.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.textBrowser_footer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser_footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textBrowser_footer.setReadOnly(False)
        self.textBrowser_footer.setObjectName("textBrowser_footer")
        self.verticalLayout.addWidget(self.textBrowser_footer)

        self.retranslateUi(drilling_modes)
        QtCore.QMetaObject.connectSlotsByName(drilling_modes)

    def retranslateUi(self, drilling_modes):
        _translate = QtCore.QCoreApplication.translate
        drilling_modes.setWindowTitle(_translate("drilling_modes", "Form"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("drilling_modes", "Шапка"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("drilling_modes", "1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("drilling_modes", "2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("drilling_modes", "3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("drilling_modes", "4"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("drilling_modes", "От"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("drilling_modes", "До"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("drilling_modes", "Забой"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("drilling_modes", "Описание работ"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.textBrowser_footer.setHtml(_translate("drilling_modes", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">hello!</p></body></html>"))
