# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.merchList = QtWidgets.QScrollArea(self.centralwidget)
        self.merchList.setWidgetResizable(True)
        self.merchList.setAlignment(QtCore.Qt.AlignCenter)
        self.merchList.setObjectName("merchList")
        #self.scrollAreaWidgetContents = QtWidgets.QWidget()
        #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 620, 419))
        #self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        #self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        #self.verticalLayout_3.setObjectName("verticalLayout_3")
        #self.merchList.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.merchList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menuUser = QtWidgets.QMenu(self.menubar)
        self.menuUser.setObjectName("menuUser")
        self.menuQuit = QtWidgets.QMenu(self.menubar)
        self.menuQuit.setObjectName("menuQuit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #self.actionLogin = QtWidgets.QAction(MainWindow)
        #self.actionLogin.setObjectName("actionLogin")
        #self.actionLogout = QtWidgets.QAction(MainWindow)
        #self.actionLogout.setObjectName("actionLogout")
        #self.actionQuit = QtWidgets.QAction(MainWindow)
        #self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nothing Shop"))
        self.menuUser.setTitle(_translate("MainWindow", "User"))
        self.menuQuit.setTitle(_translate("MainWindow", "File"))
        #self.actionLogin.setText(_translate("MainWindow", "Login"))
        #self.actionLogout.setText(_translate("MainWindow", "Logout"))
        #self.actionQuit.setText(_translate("MainWindow", "Quit"))

