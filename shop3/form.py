#!/usr/bin/env python3

import sys, json, time, urllib.request
from functools import partial

import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import form_auto

class Merch:
    def __init__(self, id, name, desc, quant, price, image=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.quant = quant
        self.price = price
        self.image = image


class MyWindowClass(QtWidgets.QMainWindow, form_auto.Ui_MainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setupNet()
        self.login_status = False
        self.Username = 'Logged out'
        self.Usercart = []
        self.Shoplist = []
        self.last_error_msg = None

        actRefresh = QtWidgets.QAction(QIcon('icon_refresh.png'), 'Refresh', self)
        actRefresh.triggered.connect(self.refresh)
        actRegister = QtWidgets.QAction(QIcon('icon_reg.png'), 'Register', self)
        actRegister.triggered.connect(self.regDialog)
        actLogin = QtWidgets.QAction(QIcon('icon_login.png'), 'Log in', self)
        actLogin.triggered.connect(self.loginDialog)
        actLogout = QtWidgets.QAction(QIcon('icon_logout.png'), 'Log out', self)
        actLogout.triggered.connect(self.logoutDialog)
        actQuit = QtWidgets.QAction(QIcon('icon_quit.png'), 'Quit', self)
        actQuit.triggered.connect(self.clExit)
        self.actUsername = QtWidgets.QAction(self.Username, self)
        self.actCart = QtWidgets.QAction(QIcon('icon_cart.png'), 'Cart', self)
        self.actCart.setEnabled(False)
        self.actCart.triggered.connect(self.cartPrepare)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(actRefresh)
        self.toolbar.addAction(actLogin)
        self.toolbar.addAction(self.actUsername)
        self.toolbar.addAction(self.actCart)

        self.menuUser.addAction(actLogin)
        self.menuUser.addAction(self.actCart)
        self.menuUser.addSeparator()
        self.menuUser.addAction(actLogout)
        self.menuQuit.addAction(actRegister)
        self.menuQuit.addSeparator()
        self.menuQuit.addAction(actQuit)
        self.menubar.addAction(self.menuQuit.menuAction())
        self.menubar.addAction(self.menuUser.menuAction())

        self.getContent()
        #self.populateTable()
        self.statusBar().showMessage('Ready.')

    def setupNet(self):
        self.manager = QNetworkAccessManager()
        self.url_list = {"login": "http://127.0.0.1:8000/shop_site/cl_login/",
                            "register": "http://127.0.0.1:8000/shop_site/cl_reg/",
                            "content": "http://127.0.0.1:8000/shop_site/cl_index/",
                            "logout": "http://127.0.0.1:8000/shop_site/cl_logout/",
                            "cart": "http://127.0.0.1:8000/shop_site/cl_cart/",
                            "checkout": "http://127.0.0.1:8000/shop_site/cl_check/"}

    def regDialog(self):
        dr = QtWidgets.QDialog(parent = self)
        dr.setWindowTitle("Register in Nothing Shop")
        dr.setWindowModality(QtCore.Qt.ApplicationModal)
        dr_layoutV = QtWidgets.QVBoxLayout()
        label_name = QtWidgets.QLabel(dr)
        label_name.setText('Enter your name:')
        dr_layoutV.addWidget(label_name)
        text_name = QtWidgets.QLineEdit(dr)
        dr_layoutV.addWidget(text_name)
        label_pass1 = QtWidgets.QLabel(dr)
        label_pass1.setText('Enter your password:')
        dr_layoutV.addWidget(label_pass1)
        text_pass1 = QtWidgets.QLineEdit(dr)
        text_pass1.setEchoMode(2)
        dr_layoutV.addWidget(text_pass1)
        label_pass2 = QtWidgets.QLabel(dr)
        label_pass2.setText('Enter your password again:')
        dr_layoutV.addWidget(label_pass2)
        text_pass2 = QtWidgets.QLineEdit(dr)
        text_pass2.setEchoMode(2)
        dr_layoutV.addWidget(text_pass2)
        dr_layoutH = QtWidgets.QHBoxLayout()
        submit = QtWidgets.QPushButton("Register", dr)
        dr_layoutH.addWidget(submit)
        cancel = QtWidgets.QPushButton("Cancel", dr)
        dr_layoutH.addWidget(cancel)
        dr_layoutV.addLayout(dr_layoutH)
        submit.clicked.connect(partial(self.register, text_name, text_pass1, text_pass2))
        cancel.clicked.connect(dr.close)
        dr.setLayout(dr_layoutV)
        dr.exec_()

    def register(self, name, pass1, pass2):
        print("Registering...")
        if not name.text() or not pass1.text() or not pass2.text():
            msg = QtWidgets.QMessageBox.warning(self, 'Unfilled fields', 'You didn\'t fill all required fields!', QtWidgets.QMessageBox.Ok)
            return
        if pass1.text() != pass2.text():
            msg = QtWidgets.QMessageBox.warning(self, 'Passwords mismatch', 'Passwords entered in both fields are not same!', QtWidgets.QMessageBox.Ok)
            return
        self.statusBar().showMessage('Registering...')
        url = QtCore.QUrl(self.url_list['register'])
        request = QNetworkRequest()
        request.setUrl(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        data = QtCore.QByteArray()
        data.append(''.join(['user=', name.text(), '&']))
        data.append(''.join(['password=', pass1.text()]))
        self.replyObjectReg = self.manager.post(request, data)
        self.replyObjectReg.finished.connect(self.registerFinalize)

    def registerFinalize(self):
        if self.replyObjectReg.error() == QNetworkReply.AuthenticationRequiredError:
            msg = QtWidgets.QMessageBox.warning(self, 'Registration failed', 'Registration failed due to:\n'+ bytes(self.replyObjectReg.readAll()).decode("utf-8"), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('Registration failed.')
            return
        elif self.replyObjectReg.error() != QNetworkReply.NoError:
            msg = QtWidgets.QMessageBox.warning(self, 'Registration failed', ''.join(['An error was encountered during connecting to shop server.\nError code: ', str(self.replyObjectReg.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('An error was encountered.')
            return
        msg = QtWidgets.QMessageBox.information(self, 'Registration successful', 'You are now registered in Nothing Shop!\n You can now use entered username and password to log in!', QtWidgets.QMessageBox.Ok)
        self.findChild(QtWidgets.QDialog).close()

    def loginDialog(self):
        if self.login_status:
            msg = QtWidgets.QMessageBox.information(self, 'Information', ''.join(['You are already logged in as:\n', self.Username]), QtWidgets.QMessageBox.Ok)
        else:
            dl = QtWidgets.QDialog(parent = self)
            dl.setWindowTitle("Log in Nothing Shop")
            dl.setWindowModality(QtCore.Qt.ApplicationModal)
            dl.setFixedSize(220, 110)
            dl_layoutV = QtWidgets.QVBoxLayout()
            text_log = QtWidgets.QLineEdit(dl)
            text_log.setPlaceholderText('Enter your username here...')
            dl_layoutV.addWidget(text_log)
            text_pass = QtWidgets.QLineEdit(dl)
            text_pass.setEchoMode(2)
            text_pass.setPlaceholderText('Enter your password here...')
            dl_layoutV.addWidget(text_pass)
            dl_layoutH = QtWidgets.QHBoxLayout()
            submit = QtWidgets.QPushButton("Login", dl)
            dl_layoutH.addWidget(submit)
            cancel = QtWidgets.QPushButton("Cancel", dl)
            dl_layoutH.addWidget(cancel)
            dl_layoutV.addLayout(dl_layoutH)
            submit.clicked.connect(partial(self.login, text_log, text_pass))
            cancel.clicked.connect(dl.close)
            dl.setLayout(dl_layoutV)
            dl.exec_()

    def login(self, name_field, pass_field):
        print("Logging in...")
        self.statusBar().showMessage('Logging in...')
        self.Username = name_field.text()
        url = QtCore.QUrl(self.url_list['login'])
        request = QNetworkRequest()
        request.setUrl(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        data = QtCore.QByteArray()
        data.append(''.join(['user=', name_field.text(), '&']))
        data.append(''.join(['password=', pass_field.text()]))
        self.replyObjectLogin = self.manager.post(request, data)
        self.replyObjectLogin.finished.connect(self.loginFinalize)

    def loginFinalize(self):
        if self.replyObjectLogin.error() == QNetworkReply.AuthenticationRequiredError:
            msg = QtWidgets.QMessageBox.warning(self, 'Login failed', 'Wrong username or password.\nPlease try again.', QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('Login attempt failed.')
            return
        elif self.replyObjectLogin.error() != QNetworkReply.NoError:
            msg = QtWidgets.QMessageBox.warning(self, 'Login failed', ''.join(['An error was encountered during connecting to shop server.\n Error code: ', str(self.replyObjectReg.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('An error was encountered.')
            return
        self.user_token = bytes(self.replyObjectLogin.readAll()).decode("utf-8")
        self.login_status = True
        self.findChild(QtWidgets.QDialog).close()
        self.actUsername.setText(''.join(['Logged in as ', self.Username]))
        self.actCart.setEnabled(True)
        self.statusBar().showMessage('Logged in.')

    def logoutDialog(self):
        if self.login_status:
            msg = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to log out?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if msg == QtWidgets.QMessageBox.Yes:
                self.user_token = None
                self.login_status = False
                self.Username = 'Logged out'
                self.Usercart = []
                self.actUsername.setText(self.Username)
                self.actCart.setEnabled(False)
                self.statusBar().showMessage('Logged out.')
        else:
            msg = QtWidgets.QMessageBox.question(self, 'Information', 'You are already logged out!', QtWidgets.QMessageBox.Ok)

    def refresh(self):
        try:
            self.scrollAreaWidgetContents.setParent(None)
        except AttributeError:
            pass
        self.getContent()

    def getContent(self):
        print("Getting content...")
        url = QtCore.QUrl(self.url_list['content'])
        request = QNetworkRequest()
        request.setUrl(url)
        self.replyObject = self.manager.get(request)
        self.replyObject.finished.connect(self.populateShopList)

    def populateShopList(self):
        print('Populating list...')
        if self.replyObject.error() == QNetworkReply.ConnectionRefusedError:
            msg = QtWidgets.QMessageBox.warning(self, 'Shoplist fetching failed', 'Shop server is currently refusing connections.\nCheck your internet connection.', QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage("Couldn't connect to shop server.")
            return
        elif self.replyObject.error() != QNetworkReply.NoError:
            msg = QtWidgets.QMessageBox.warning(self, 'Shoplist fetching failed', ''.join(['An error was encountered during connecting to shop server.\n Error code: ', str(self.replyObject.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('An error was encountered.')
            return
        answerAsJson = bytes(self.replyObject.readAll()).decode("utf-8")
        try:
            answerAsText = json.loads(answerAsJson)
        except json.decoder.JSONDecodeError:
            msg = QtWidgets.QMessageBox.warning(self, 'Shoplist fetching failed', 'An error was encountered while parsing shoplist data.\nPlease try again.', QtWidgets.QMessageBox.Ok)
            return
        self.Shoplist.clear()
        for item in answerAsText:
            self.Shoplist.append(Merch(item['id'], item['name'], item['desc'], item['quantity'], item['price']))
            data = urllib.request.urlopen(''.join(['http://127.0.0.1:8000/static/', item['image']]))
            self.Shoplist[-1].image = QtGui.QPixmap()
            self.Shoplist[-1].image.loadFromData(data.read())
        self.populateTable()

    def populateTable(self):
        print("Making tables...")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 620, 419))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.merchList.setWidget(self.scrollAreaWidgetContents)

        self.mainVerticalLayer = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainVerticalLayer.setObjectName("mainVerticalLayer")

        MerchBoxList = []
        ImageLabelList = []
        NameLabelList = []
        DescBoxList = []
        RemainLabelList = []
        PriceLabelList = []
        MerchNumList = []
        BuyButtonList = []
        MerchBoxHWidgetList = []
        MerchBoxH1LayoutList = []
        MerchBoxH2LayoutList = []
        MerchBoxV1LayoutList = []
        MerchBoxV2LayoutList = []
        for merch in self.Shoplist:
            MerchBoxList.append(QtWidgets.QGroupBox(self.scrollAreaWidgetContents))
            MerchBoxList[-1].setTitle(merch.name)

            MerchBoxHWidgetList.append(QtWidgets.QWidget(MerchBoxList[-1]))
            # Columnt 1 - Image
            MerchBoxH1LayoutList.append(QtWidgets.QHBoxLayout(MerchBoxHWidgetList[-1]))
            MerchBoxH1LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxH1LayoutList[-1].setContentsMargins(0, 0, 10, 6)
            MerchBoxH1LayoutList[-1].setSpacing(10)

            ImageLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            ImageLabelList[-1].setMinimumSize(QtCore.QSize(150, 150))
            ImageLabelList[-1].setAlignment(QtCore.Qt.AlignCenter)
            ImageLabelList[-1].setPixmap(merch.image.scaled(ImageLabelList[-1].size(), 1))
            MerchBoxH1LayoutList[-1].addWidget(ImageLabelList[-1])

            # Column 2 - Name, description
            MerchBoxV1LayoutList.append(QtWidgets.QVBoxLayout())
            MerchBoxV1LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxV1LayoutList[-1].setContentsMargins(0, 0, 10, 10)
            MerchBoxV1LayoutList[-1].setSpacing(10)

            NameLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            NameLabelList[-1].setText(merch.name)
            MerchBoxV1LayoutList[-1].addWidget(NameLabelList[-1])

            DescBoxList.append(QtWidgets.QTextEdit(MerchBoxHWidgetList[-1]))
            DescBoxList[-1].setPlainText(merch.desc)
            DescBoxList[-1].setReadOnly(True)
            MerchBoxV1LayoutList[-1].addWidget(DescBoxList[-1])
            MerchBoxH1LayoutList[-1].addLayout(MerchBoxV1LayoutList[-1])

            # Column 3 - Remaining, Price, Put in cart controls
            MerchBoxV2LayoutList.append(QtWidgets.QVBoxLayout())
            MerchBoxV2LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxV2LayoutList[-1].setContentsMargins(0, 0, 10, 10)
            MerchBoxV2LayoutList[-1].setSpacing(10)

            RemainLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            RemainLabelList[-1].setAlignment(QtCore.Qt.AlignCenter)
            RemainLabelList[-1].setText('Remaining: ' + str(merch.quant))
            MerchBoxV2LayoutList[-1].addWidget(RemainLabelList[-1])

            PriceLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            PriceLabelList[-1].setAlignment(QtCore.Qt.AlignCenter)
            PriceLabelList[-1].setText('Price: $' + str(merch.price))
            MerchBoxV2LayoutList[-1].addWidget(PriceLabelList[-1])

            MerchBoxH2LayoutList.append(QtWidgets.QHBoxLayout())
            MerchBoxH2LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxH2LayoutList[-1].setContentsMargins(0, 0, 0, 0)
            MerchBoxH2LayoutList[-1].setSpacing(10)

            MerchNumList.append(QtWidgets.QSpinBox(MerchBoxHWidgetList[-1]))
            MerchNumList[-1].setMinimum(1)
            MerchNumList[-1].setMaximum(merch.quant)
            MerchBoxH2LayoutList[-1].addWidget(MerchNumList[-1])

            BuyButtonList.append(QtWidgets.QPushButton(MerchBoxHWidgetList[-1]))
            BuyButtonList[-1].setText("In cart")
            BuyButtonList[-1].clicked.connect(partial(self.putCart, merch, MerchNumList[-1], True))
            if merch.quant == 0:
                BuyButtonList[-1].setEnabled(False)
            MerchBoxH2LayoutList[-1].addWidget(BuyButtonList[-1])
            MerchBoxV2LayoutList[-1].addLayout(MerchBoxH2LayoutList[-1])
            MerchBoxH1LayoutList[-1].addLayout(MerchBoxV2LayoutList[-1])

            MerchBoxV1LayoutList[-1].addStretch(1)
            MerchBoxH2LayoutList[-1].addStretch(1)
            MerchBoxH1LayoutList[-1].setStretch(0, 3)
            MerchBoxH1LayoutList[-1].setStretch(1, 8)
            MerchBoxH1LayoutList[-1].setStretch(2, 2)
            MerchBoxList[-1].setLayout(MerchBoxH1LayoutList[-1])
            self.mainVerticalLayer.addWidget(MerchBoxList[-1])
        self.merchList.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.merchList)

    def cartPrepare(self):
        print("Fetching user cart...")
        self.statusBar().showMessage('Fetching user cart...')
        url = QtCore.QUrl(self.url_list['cart'])
        request = QNetworkRequest()
        request.setUrl(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        data = QtCore.QByteArray()
        data.append(''.join(['token=', self.user_token, '&']))
        data.append(''.join(['submethod=', 'get']))
        self.replyObjectCart = self.manager.post(request, data)
        self.replyObjectCart.finished.connect(self.cartDialog)

    def cartDialog(self):
        if self.replyObjectCart.error() == QNetworkReply.AuthenticationRequiredError:
            msg = QtWidgets.QMessageBox.warning(self, 'Login error', ''.join(['There was a problem with your credentials.\nPlease try logging in again.\n Error code: ', str(self.replyObjectCart.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage("Couldn't fetch user cart.")
            return
        answerAsJson = bytes(self.replyObjectCart.readAll()).decode("utf-8")
        answerAsText = json.loads(answerAsJson)
        self.Usercart.clear()
        for item in answerAsText:
            self.Usercart.append({"merch": next(x for x in self.Shoplist if x.id == item['id']), "num": item['num']})
        dc = QtWidgets.QDialog(parent = self)
        dc.setWindowTitle(''.join(["Shop Cart - ", self.Username]))
        dc.setWindowModality(QtCore.Qt.ApplicationModal)
        #dc.resize(600, 420)
        dc_layoutV = QtWidgets.QVBoxLayout()
        lazylist = []
        BoxList = []
        BoxWidgetList = []
        BoxLayoutList = []
        ImgList = []
        NameList = []
        NumList = []
        NumEditList = []
        RemButtonList = []
        if self.Usercart:
            for item in self.Usercart:
                BoxList.append(QtWidgets.QGroupBox(dc))
                BoxList[-1].setObjectName(''.join(['Box', str(item['merch'].id)]))
                BoxWidgetList.append(QtWidgets.QWidget(BoxList[-1]))
                BoxLayoutList.append(QtWidgets.QHBoxLayout(BoxWidgetList[-1]))
                BoxLayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
                BoxLayoutList[-1].setContentsMargins(5, 5, 5, 5)
                BoxLayoutList[-1].setSpacing(10)

                ImgList.append(QtWidgets.QLabel(BoxWidgetList[-1]))
                ImgList[-1].setMinimumSize(QtCore.QSize(50, 50))
                ImgList[-1].setAlignment(QtCore.Qt.AlignCenter)
                ImgList[-1].setPixmap(item['merch'].image.scaled(ImgList[-1].size(), 1))
                BoxLayoutList[-1].addWidget(ImgList[-1])

                NameList.append(QtWidgets.QLabel(BoxWidgetList[-1]))
                NameList[-1].setAlignment(QtCore.Qt.AlignCenter)
                NameList[-1].setText(item['merch'].name)
                BoxLayoutList[-1].addWidget(NameList[-1])

                NumList.append(QtWidgets.QLabel(BoxWidgetList[-1]))
                NumList[-1].setAlignment(QtCore.Qt.AlignCenter)
                NumList[-1].setText(''.join(['In cart: ', str(item['num']), ' units']))
                NumList[-1].setObjectName(''.join(['NumLabel', str(item['merch'].id)]))
                BoxLayoutList[-1].addWidget(NumList[-1])

                NumEditList.append(QtWidgets.QSpinBox(BoxWidgetList[-1]))
                NumEditList[-1].setMinimum(1)
                NumEditList[-1].setMaximum(item['num'])
                BoxLayoutList[-1].addWidget(NumEditList[-1])

                RemButtonList.append(QtWidgets.QPushButton(BoxWidgetList[-1]))
                RemButtonList[-1].setText('Remove from cart')
                RemButtonList[-1].clicked.connect(partial(self.putCart, item['merch'], NumEditList[-1], False))
                BoxLayoutList[-1].addWidget(RemButtonList[-1])

                BoxList[-1].setLayout(BoxLayoutList[-1])
                dc_layoutV.addWidget(BoxList[-1])
        else:
            nothinglabel = QtWidgets.QLabel(dc)
            nothinglabel.setText('Your cart is empty!')
            dc_layoutV.addWidget(nothinglabel)
        submitbtn = QtWidgets.QPushButton("Purchase!", dc)
        submitbtn.clicked.connect(self.purchaseDialog)
        submitbtn.setObjectName('submitbtn')
        if not self.Usercart:
            submitbtn.setEnabled(False)
        dc_layoutV.addWidget(submitbtn)
        cancelbtn = QtWidgets.QPushButton("Close cart...", dc)
        dc_layoutV.addWidget(cancelbtn)
        cancelbtn.clicked.connect(dc.close)
        dc.setLayout(dc_layoutV)
        dc.exec_()

    def putCart(self, merch, num_field, add):
        print("Putting merchandize in cart...")
        self.statusBar().showMessage('Putting merchandize in cart...')
        if self.login_status:
            url = QtCore.QUrl(self.url_list['cart'])
            request = QNetworkRequest()
            request.setUrl(url)
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
            data = QtCore.QByteArray()
            data.append(''.join(['token=', self.user_token, '&']))
            data.append(''.join(['submethod=', 'change', '&']))
            data.append(''.join(['merchid=', str(merch.id), '&']))
            if add:
                data.append(''.join(['merchnum=', str(num_field.value())]))
            else:
                data.append(''.join(['merchnum=-', str(num_field.value())]))
            self.replyObjectPutCart = self.manager.post(request, data)
            self.replyObjectPutCart.finished.connect(self.putCartResult)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Information', 'You need to log in first\nto use shopping cart!', QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('Not logged in yet.')

    def putCartResult(self):
        print("A thing is happening!")
        if self.replyObjectPutCart.error() == QNetworkReply.AuthenticationRequiredError:
            self.statusBar().showMessage("Authentication failed.")
            msg = QtWidgets.QMessageBox.warning(self, 'Authentication failed', 'Your login session has expired.\nPlease relog into shop and try again.', QtWidgets.QMessageBox.Ok)
            return
        elif self.replyObjectPutCart.error() != QNetworkReply.NoError:
            msg = QtWidgets.QMessageBox.warning(self, 'Authentication failed', ''.join(['An error was encountered during connecting to shop server.\n Error code: ', str(self.replyObjectPutCart.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('An error was encountered.')
            return
        answerAsJson = bytes(self.replyObjectPutCart.readAll()).decode("utf-8")
        answerAsText = json.loads(answerAsJson)
        print(answerAsText)
        if 'merch+' in answerAsText:
            print("A merch+ is happening!")
            next(x for x in self.Shoplist if x.id == answerAsText['merch+']).quant = answerAsText['quantity']
            self.scrollAreaWidgetContents.setParent(None)
            self.populateTable()
            self.statusBar().showMessage('Placed merchandize in cart.')
        elif 'merch-' in answerAsText:
            print("A merch- is happening!")
            item = next(x for x in self.Usercart if x['merch'].id == answerAsText['merch-'])
            item['num'] -= answerAsText['quantity']
            item['merch'].quant += answerAsText['quantity']
            dc = self.findChild(QtWidgets.QDialog)
            if item['num'] < 1:
                dc.findChild(QtWidgets.QGroupBox, ''.join(['Box', str(item['merch'].id)])).hide()
                self.Usercart.remove(item)
                if not self.Usercart:
                    dc.findChild(QtWidgets.QPushButton, 'submitbtn').setEnabled(False)
            else:
                label = dc.findChild(QtWidgets.QLabel, ''.join(['NumLabel', str(item['merch'].id)]))
                label.setText(''.join(['In cart: ', str(item['num']), ' units']))
            self.scrollAreaWidgetContents.setParent(None)
            self.populateTable()
            self.statusBar().showMessage('Removed merchandize from cart.')

    def purchaseDialog(self):
        dp = QtWidgets.QDialog(parent = self)
        dp.setWindowTitle("Checkout")
        dp.setWindowModality(QtCore.Qt.ApplicationModal)
        dp_layoutV = QtWidgets.QVBoxLayout()
        label_address = QtWidgets.QLabel(dp)
        label_address.setText('Enter your address:')
        dp_layoutV.addWidget(label_address)
        text_address = QtWidgets.QTextEdit(dp)
        dp_layoutV.addWidget(text_address)
        label_date = QtWidgets.QLabel(dp)
        label_date.setText('Enter date when you want to receive your purchase:')
        dp_layoutV.addWidget(label_date)
        text_date = QtWidgets.QLineEdit(dp)
        dp_layoutV.addWidget(text_date)
        label_mail = QtWidgets.QLabel(dp)
        label_mail.setText('Enter your mail to receive confirmation letter:')
        dp_layoutV.addWidget(label_mail)
        text_mail = QtWidgets.QLineEdit(dp)
        dp_layoutV.addWidget(text_mail)
        dp_layoutH = QtWidgets.QHBoxLayout()
        submit = QtWidgets.QPushButton("Purchase!", dp)
        dp_layoutH.addWidget(submit)
        cancel = QtWidgets.QPushButton("Cancel", dp)
        dp_layoutH.addWidget(cancel)
        dp_layoutV.addLayout(dp_layoutH)
        submit.clicked.connect(self.purchase)
        cancel.clicked.connect(dp.close)
        dp.setLayout(dp_layoutV)
        dp.exec_()

    def purchase(self):
        print("Confirming purchase...")
        self.statusBar().showMessage('Confirming purchase...')
        url = QtCore.QUrl(self.url_list['checkout'])
        request = QNetworkRequest()
        request.setUrl(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        data = QtCore.QByteArray()
        data.append(''.join(['token=', self.user_token]))
        self.replyObjectPur = self.manager.post(request, data)
        self.replyObjectPur.finished.connect(self.purchaseFinalize)

    def purchaseFinalize(self):
        if self.replyObjectPur.error() == QNetworkReply.AuthenticationRequiredError:
            self.statusBar().showMessage("Authentication failed.")
            msg = QtWidgets.QMessageBox.warning(self, 'Authentication failed', 'Your login session has expired.\nPlease relog into shop and try again.', QtWidgets.QMessageBox.Ok)
            return
        elif self.replyObjectPur.error() != QNetworkReply.NoError:
            msg = QtWidgets.QMessageBox.warning(self, 'Confirmation failed', ''.join(['An error was encountered during connecting to shop server.\n Error code: ', str(self.replyObjectPutCart.error())]), QtWidgets.QMessageBox.Ok)
            self.statusBar().showMessage('An error was encountered.')
            return
        msg = QtWidgets.QMessageBox.information(self, 'Purchase completed!', 'Congratulations! Your merchandize is already on it\'s way!', QtWidgets.QMessageBox.Ok)
        for window in self.findChildren(QtWidgets.QDialog):
            window.close()

    def clExit(self):
        app.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
