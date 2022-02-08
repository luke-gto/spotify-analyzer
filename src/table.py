# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView, QVBoxLayout
import webbrowser

class Ui_tableWindow(object):

    def __init__(self, dataframe):
        self.data = dataframe

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(866, 702)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        horizontalHeader = self.tableWidget.horizontalHeader()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 866, 702))
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(self.data.shape[0])
        self.tableWidget.setColumnCount(self.data.shape[1])
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 866, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.load_data()
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for i in range(self.data.shape[1]):            
            horizontalHeader.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.itemDoubleClicked.connect(self.OpenLink)

    def OpenLink(self):
        for index in self.tableWidget.selectedIndexes():
            value = str(self.data.iloc[index.row()][index.column()])
            if value.startswith("http://") or value.startswith("https://"):
                webbrowser.open(value)
    
    def load_data(self):
        row = 0
        col = 0
        list = []
        for col_name in self.data.columns:
            list.append(col_name)
            self.tableWidget.setHorizontalHeaderLabels(list)

        for row in range (0, self.data.shape[0]):
                for col in range (0, self.data.shape[1]):
                        data = str(self.data.iloc[row, col] )
                        self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spotify Analyzer Data"))


def show_table(dataframe):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_tableWindow(dataframe)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())