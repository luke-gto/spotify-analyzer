# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from os.path import join
from dotenv import load_dotenv
import dotenv
from PyQt5.QtWidgets import QMessageBox, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from src.table import Ui_tableWindow
from src.spotify_analyzer import tracks_analyzer, top_artist, last_played, export_csv, export_ods
import spotipy
import os
import pandas as pd
import webbrowser
import sys
from pathlib import Path

home = str(Path.home())
script_directory = os.path.dirname(os.path.realpath(__file__))
working_directory = home + '/spotify-analyzer-data'
env_file = script_directory + "/.env"

def setup_directories():
    if os.path.isdir(working_directory):
        pass
    else:
        os.mkdir(working_directory)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(683, 732)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(script_directory + "/resources/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.time_range_label = QtWidgets.QLabel(self.centralwidget)
        self.time_range_label.setGeometry(QtCore.QRect(140, 380, 400, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_range_label.sizePolicy().hasHeightForWidth())
        self.time_range_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.time_range_label.setFont(font)
        self.time_range_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.time_range_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_range_label.setObjectName("time_range_label")
        self.songs_num_label = QtWidgets.QLabel(self.centralwidget)
        self.songs_num_label.setGeometry(QtCore.QRect(182, 300, 400, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.songs_num_label.setFont(font)
        self.songs_num_label.setObjectName("songs_num_label")
        self.songs_num_line = QtWidgets.QLineEdit(self.centralwidget)
        self.songs_num_line.setGeometry(QtCore.QRect(330, 330, 41, 31))
        self.songs_num_line.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.songs_num_line.setMaxLength(2)
        self.songs_num_line.setAlignment(QtCore.Qt.AlignCenter)
        self.songs_num_line.setObjectName("songs_num_line")
        self.analysis_type_label = QtWidgets.QLabel(self.centralwidget)
        self.analysis_type_label.setGeometry(QtCore.QRect(250, 210, 211, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.analysis_type_label.setFont(font)
        self.analysis_type_label.setObjectName("analysis_type_label")
        self.pushButton = QtWidgets.QRadioButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 240, 100, 33))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")

        self.choice_button_group = QtWidgets.QButtonGroup(MainWindow)
        self.choice_button_group.setObjectName("choice_button_group")
        self.choice_button_group.addButton(self.pushButton)
        self.pushButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 240, 95, 33))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.choice_button_group.addButton(self.pushButton_2)


        self.history_button = QtWidgets.QRadioButton(self.centralwidget)
        self.history_button.setGeometry(QtCore.QRect(287, 240, 120, 33))
        self.history_button.setCheckable(True)
        self.history_button.setObjectName("history_button")
        self.choice_button_group.addButton(self.history_button)


        self.analysis_type_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.analysis_type_label_2.setGeometry(QtCore.QRect(260, 470, 181, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.analysis_type_label_2.setFont(font)
        self.analysis_type_label_2.setObjectName("analysis_type_label_2")
        self.csv_button = QtWidgets.QRadioButton(self.centralwidget)
        self.csv_button.setGeometry(QtCore.QRect(200, 500, 95, 33))
        self.csv_button.setCheckable(True)
        self.csv_button.setObjectName("csv_button")
        self.export_button_group = QtWidgets.QButtonGroup(MainWindow)
        self.export_button_group.setObjectName("export_button_group")
        self.export_button_group.addButton(self.csv_button)
        self.ods_button = QtWidgets.QRadioButton(self.centralwidget)
        self.ods_button.setGeometry(QtCore.QRect(400, 500, 95, 33))
        self.ods_button.setCheckable(True)
        self.ods_button.setObjectName("ods_button")
        self.export_button_group.addButton(self.ods_button)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(240, 560, 231, 51))

        self.reload_button = QtWidgets.QPushButton(self.centralwidget)
        self.reload_button.setGeometry(QtCore.QRect(240, 620, 231, 51))


        palette2 = QtGui.QPalette()
        brush2 = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush2.setStyle(QtCore.Qt.SolidPattern)
        palette2.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush2)


        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 255, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 255, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 255, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 127, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.start_button.setPalette(palette)
        self.reload_button.setPalette(palette2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setAutoFillBackground(False)
        self.start_button.setObjectName("start_button")

        self.reload_button.setFont(font)
        self.reload_button.setAutoFillBackground(False)
        self.reload_button.setObjectName("reload_button")


        self.saved_credentials_button = QtWidgets.QPushButton(self.centralwidget)
        self.saved_credentials_button.setGeometry(QtCore.QRect(310, 60, 301, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.saved_credentials_button.setFont(font)
        self.saved_credentials_button.setObjectName("saved_credentials_button")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 261, 181))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.client_label = QtWidgets.QLabel(self.widget)
        self.client_label.setObjectName("client_label")
        self.gridLayout.addWidget(self.client_label, 0, 0, 1, 1)
        self.client_line = QtWidgets.QLineEdit(self.widget)
        self.client_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.client_line.setClearButtonEnabled(True)
        self.client_line.setObjectName("client_line")
        self.gridLayout.addWidget(self.client_line, 1, 0, 1, 1)
        self.secret_label = QtWidgets.QLabel(self.widget)
        self.secret_label.setObjectName("secret_label")
        self.gridLayout.addWidget(self.secret_label, 2, 0, 1, 1)
        self.secret_line = QtWidgets.QLineEdit(self.widget)
        self.secret_line.setInputMask("")
        self.secret_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.secret_line.setClearButtonEnabled(True)
        self.secret_line.setObjectName("secret_line")
        self.gridLayout.addWidget(self.secret_line, 3, 0, 1, 1)
        self.URI_label = QtWidgets.QLabel(self.widget)
        self.URI_label.setObjectName("URI_label")
        self.gridLayout.addWidget(self.URI_label, 4, 0, 1, 1)
        self.URI_line = QtWidgets.QLineEdit(self.widget)
        self.URI_line.setStatusTip("")
        self.URI_line.setWhatsThis("")
        self.URI_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.URI_line.setClearButtonEnabled(True)
        self.URI_line.setObjectName("URI_line")
        self.gridLayout.addWidget(self.URI_line, 5, 0, 1, 1)
        self.medium_button = QtWidgets.QRadioButton(self.centralwidget)
        self.medium_button.setGeometry(QtCore.QRect(296, 410, 110, 33))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.medium_button.setFont(font)
        self.medium_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.medium_button.setCheckable(True)
        self.medium_button.setObjectName("medium_button")
        self.button_time_Group = QtWidgets.QButtonGroup(MainWindow)
        self.button_time_Group.setObjectName("button_time_Group")
        self.button_time_Group.addButton(self.medium_button)
        self.long_button = QtWidgets.QRadioButton(self.centralwidget)
        self.long_button.setGeometry(QtCore.QRect(520, 410, 95, 33))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.long_button.setFont(font)
        self.long_button.setCheckable(True)
        self.long_button.setObjectName("long_button")
        self.button_time_Group.addButton(self.long_button)
        self.short_button = QtWidgets.QRadioButton(self.centralwidget)
        self.short_button.setGeometry(QtCore.QRect(80, 410, 102, 33))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.short_button.setFont(font)
        self.short_button.setCheckable(True)
        self.short_button.setObjectName("short_button")
        self.button_time_Group.addButton(self.short_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 683, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuExit = QtWidgets.QMenu(self.menuBar)
        self.menuExit.setObjectName("menuExit")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionGuide = QtWidgets.QAction(MainWindow)
        self.actionGuide.setObjectName("actionGuide")
        self.menuBar.addAction(self.actionGuide)
        self.menuBar.addAction(self.actionExit)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionGuide.triggered.connect(self.open_guide)

        self.client_line.editingFinished.connect(self.save_client_id)
        self.secret_line.editingFinished.connect(self.save_client_secret)
        self.URI_line.editingFinished.connect(self.save_URI)

        self.saved_credentials_button.clicked.connect(self.load_credentials)

        self.button_time_Group.buttonClicked.connect(self.time_choice)
        self.choice_button_group.buttonClicked.connect(self.set_choice)
        self.export_button_group.buttonClicked.connect(self.export_choice)
        self.start_button.clicked.connect(self.start_analyze)
        self.reload_button.clicked.connect(self.reload_app)
        

    def reload_app(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def open_guide(self):
        webbrowser.open('https://luke-gto.github.io/spotify-analyzer/')
                

    def openWindow(self, dataframe, av_df):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_tableWindow(dataframe, av_df)
        self.ui.setupUi(self.window)
        self.window.show()

    def start_analyze(self):


        if self.button_time_Group.checkedId() == 4 or self.button_time_Group.checkedId() == 2 or self.button_time_Group.checkedId() == 3 and self.set_choice() == -4: ### check whether last played and time range is selected at the same time
            msg = QMessageBox()
            msg.setWindowTitle("Ooops!")
            msg.setText("The time range option is not available for 'Last played songs'. Reload the app please.")
            msg.setIcon(msg.Critical)
            msg.exec()

            return

        try:

            self.load_credentials()
            if self.set_choice() != -2 and self.set_choice() != -3 and self.set_choice() != -4:

                msg = QMessageBox()
                msg.setWindowTitle("Ooooops!")
                msg.setText("Choose an option first")
                msg.setIcon(msg.Warning)
                msg.exec()
                return

            if self.song_num() == '' or int(self.song_num()) > 50:   ### check correct number of songs BEFORE continuing to execute the script
                msg = QMessageBox()
                msg.setWindowTitle("Ooops!")
                msg.setText("Wrong number of songs selected. Max = 50")
                msg.setIcon(msg.Warning)
                msg.exec()
                return

            msg = QMessageBox()
            msg.setWindowTitle("Whoooa!")
            msg.setText("I'm working, DON'T PANIC if it seems like I'm hang up!")
            msg.setIcon(msg.Information)
            msg.exec()


            if self.set_choice() == -2:

                data_retrieved = tracks_analyzer(self.time_choice(), self.song_num())
                dataframe = data_retrieved[0]
                av_df = data_retrieved[1]

                Ui_tableWindow(dataframe, av_df)
                self.openWindow(dataframe, av_df)


                if self.export_choice() == -3:

                    export_ods(dataframe, av_df, working_directory, file_name='top_tracks')

                if self.export_choice() == -2:

                    export_csv(dataframe, av_df, working_directory, file_name='top_tracks')


            if self.set_choice() == -3:

                dataframe = top_artist(self.time_choice(), self.song_num())
                av_df = pd.DataFrame()
                av_df.empty
                Ui_tableWindow(dataframe, av_df)
                self.openWindow(dataframe, av_df)

                if self.export_choice() == -3:

                    export_ods(dataframe, working_directory, file_name='top_artists')


                if self.export_choice() == -2:

                    export_csv(dataframe, working_directory, file_name='top_artists')


            if self.set_choice() == -4:

                data_retrieved = last_played(self.song_num())
                dataframe = data_retrieved[0]
                av_df = data_retrieved[1]

                Ui_tableWindow(dataframe, av_df)
                self.openWindow(dataframe, av_df)

                if self.export_choice() == -3:

                    export_ods(dataframe, av_df, working_directory, file_name='tracks_history')

                if self.export_choice() == -2:

                    export_csv(dataframe, av_df, working_directory, file_name='tracks_history')

        except spotipy.oauth2.SpotifyOauthError:
                msg = QMessageBox()
                msg.setWindowTitle("Ooops!")
                msg.setText("Invalid credentials. Try again.")
                msg.setIcon(msg.Critical)
                msg.exec()
                return


    def export_choice(self):

        key = self.export_button_group.checkedId()
        return key


    def set_choice(self): ### first row buttons --- which one is pressed?
        key = self.choice_button_group.checkedId()
        return key      


    def time_choice(self):
        key = self.button_time_Group.checkedId()
        if key == -4:
            return 'short_term'
        if key == -2:
            return "medium_term"
        if key == -3:
            return "long_term"

    def song_num(self):
        num = self.songs_num_line.text()
        return num


    def load_credentials(self):

        msg = QMessageBox()

        if os.path.isfile(script_directory + '/.env'):

            dotenv_path = join(script_directory, '.env')
            load_dotenv(dotenv_path)
            SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
            SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
            SPOTIPY_REDIRECT_URI= os.environ.get("SPOTIPY_REDIRECT_URI")

            if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI != "":

                msg.setWindowTitle("Yeah!")
                msg.setText("Valid credentials found!")
                msg.setIcon(msg.Information)
                msg.exec()
                self.client_line.setText(SPOTIPY_CLIENT_ID)
                self.secret_line.setText(SPOTIPY_CLIENT_SECRET)
                self.URI_line.setText(SPOTIPY_REDIRECT_URI)

            else:
                msg.setWindowTitle("ERROR")
                msg.setText("Credentials not valid. Pleae fill the form again.")
                msg.setIcon(msg.Critical)
                msg.exec()
                if os.path.exists(env_file):
                    os.remove(env_file)
        else:
            msg.setWindowTitle("ERROR")
            msg.setText("Credentials not found. Pleae fill the form again.")
            msg.setIcon(msg.Critical)
            msg.exec()

            if os.path.exists(env_file):
                os.remove(env_file)
            self.client_line.setText('')
            self.secret_line.setText('')
            self.URI_line.setText('')

    def exit_app(self):
        sys.exit()

    def save_client_id(self):    ### save user input section
        config_file = env_file
        user_input = self.client_line.text()
        dotenv.set_key(config_file, "SPOTIPY_CLIENT_ID", user_input)
        return 1

    def save_client_secret(self):
        config_file = env_file
        user_input = self.secret_line.text()
        dotenv.set_key(config_file, "SPOTIPY_CLIENT_SECRET", user_input)
        return 1

    def save_URI(self):
        config_file = env_file
        user_input = self.URI_line.text()
        dotenv.set_key(config_file, "SPOTIPY_REDIRECT_URI", user_input)
        return 1
                                                ### save user input section ends here

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spotify Data Retriever"))
        self.time_range_label.setText(_translate("MainWindow", "Select the time range - NOT FOR LAST PLAYED SONGS"))
        self.songs_num_label.setText(_translate("MainWindow", "How many songs do you want to retrieve? Max = 50"))
        self.analysis_type_label.setText(_translate("MainWindow", "Select the type of analysis"))
        self.pushButton.setStatusTip(_translate("MainWindow", "Analyze your favorite songs"))
        self.pushButton.setText(_translate("MainWindow", "Top tracks"))
        self.pushButton_2.setStatusTip(_translate("MainWindow", "Retrieve your favorite artists"))
        self.pushButton_2.setText(_translate("MainWindow", "Top artists"))

        self.history_button.setStatusTip(_translate("MainWindow", "Retrieve your last played songs"))
        self.history_button.setText(_translate("MainWindow", "Last played songs"))


        self.analysis_type_label_2.setText(_translate("MainWindow", "Export data - Optional"))
        self.csv_button.setText(_translate("MainWindow", ".csv File"))
        self.ods_button.setText(_translate("MainWindow", ".xlsx File"))
        self.start_button.setText(_translate("MainWindow", "START"))
        self.reload_button.setText(_translate("MainWindow", "RELOAD APP"))
        self.saved_credentials_button.setStatusTip(_translate("MainWindow", "Only if you\'ve already used this tool"))
        self.saved_credentials_button.setText(_translate("MainWindow", "Load saved credentials"))
        self.client_label.setText(_translate("MainWindow", "Enter Spotify Client ID"))
        self.secret_label.setText(_translate("MainWindow", "Enter Spotify Secret ID"))
        self.secret_line.setStatusTip(_translate("MainWindow", "DO NOT SHARE THIS STRING"))
        self.URI_label.setText(_translate("MainWindow", "Enter Spotify redirect URI"))
        self.medium_button.setStatusTip(_translate("MainWindow", "Retrieve data from the last 6 months"))
        self.medium_button.setText(_translate("MainWindow", "Medium term "))
        self.long_button.setStatusTip(_translate("MainWindow", "Retrieve data from several years "))
        self.long_button.setText(_translate("MainWindow", "Long term "))
        self.short_button.setStatusTip(_translate("MainWindow", "Retrieve data from the last 4 weeks"))
        self.short_button.setText(_translate("MainWindow", "Short term "))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuExit.setTitle(_translate("MainWindow", "Exit"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionGuide.setText(_translate("MainWindow", "Guide"))


if __name__ == '__main__':
    setup_directories()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())