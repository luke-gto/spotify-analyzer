from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import webbrowser
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pathlib import Path

d = str(Path(__file__).resolve().parents[1])

print(d)


class average_window(QWidget):
    def __init__(self, dataframe):
        self.data = dataframe

    def createWindow(self, WindowWidth, WindowHeight):

        parent = None
        super(average_window, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(WindowWidth, WindowHeight)
        self.tableWidget = QtWidgets.QTableWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())

        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 866, 745))
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(self.data.shape[0])
        self.tableWidget.setColumnCount(self.data.shape[1])
        self.tableWidget.setObjectName("tableWidget")
        Ui_tableWindow.load_data(self)
        horizontalHeader = self.tableWidget.horizontalHeader()
        for i in range(self.data.shape[1]):
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            horizontalHeader.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents
            )
            horizontalHeader.setFont(font)


class Ui_tableWindow(object):
    def __init__(self, dataframe, av_df):
        self.data = dataframe
        self.av_data = av_df

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(866, 702)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(d + "/resources/images/icon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        MainWindow.setWindowIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(d + "/resources/images/icon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        horizontalHeader = self.tableWidget.horizontalHeader()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 866, 745))
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 866, 200))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        if not self.av_data.empty:

            self.menuStats = QtWidgets.QMenu(self.menubar)
            self.menuStats.setObjectName("menuStats")
            self.actionStats = QtWidgets.QAction(MainWindow)
            self.actionStats.setObjectName("actionStats")
            self.menubar.addAction(self.actionStats)
            self.retranslateUi(MainWindow)
            self.actionStats.triggered.connect(
                (lambda: self.open_average_window(self.av_data))
            )

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.load_data()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for i in range(self.data.shape[1]):
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            horizontalHeader.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents
            )
            horizontalHeader.setFont(font)

        self.tableWidget.itemDoubleClicked.connect(self.OpenLink)

    def open_average_window(self, dataframe):
        self.mySubwindow = average_window(dataframe)
        self.mySubwindow.createWindow(500, 400)
        self.mySubwindow.show()

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

        for row in range(0, self.data.shape[0]):
            for col in range(0, self.data.shape[1]):
                data = str(self.data.iloc[row, col])
                self.tableWidget.setItem(
                    row, col, QtWidgets.QTableWidgetItem(str(data))
                )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spotify Analyzer Data"))
        if not self.av_data.empty:
            self.menuStats.setTitle(_translate("MainWindow", "Average values"))
            self.actionStats.setText(_translate("MainWindow", "Average values"))


def show_table(dataframe, av_df):
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_tableWindow(dataframe, av_df)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
