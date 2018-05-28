import sys, json, traceback
from pprint import pprint
from functools import partial

import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

import form_auto

class MyWindowClass(PyQt5.QtWidgets.QMainWindow, form_auto.Ui_MainWindow):
    def __init__(self, parent = None):
        PyQt5.QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setupNet()
        self.login_status = False
        self.Username = 'Logged out'
        
        actRefresh = QtWidgets.QAction('Refresh', self)
        actRefresh.triggered.connect(self.refresh)
        
        actLogin = QtWidgets.QAction('Login', self)
        actLogin.triggered.connect(self.loginDialog)
        
        self.actUsername = QtWidgets.QAction(self.Username, self)
        
        self.toolbar = self.addToolBar('Refresh')
        self.toolbar.addAction(actRefresh)
        self.toolbar.addAction(actLogin)
        self.toolbar.addAction(self.actUsername)
        
        self.actionQuit.triggered.connect(self.clExit)
        self.getContent()
        self.statusBar().showMessage('Ready')
    
    def setupNet(self):
        self.manager = QNetworkAccessManager()
        self.url_list = {"login": "http://127.0.0.1:8000/shop_site/cl_login/",
                            "content": "http://127.0.0.1:8000/shop_site/cl_index/",
                            "logout": "http://127.0.0.1:8000/shop_site/cl_logout/",
                            "checkout": "http://127.0.0.1:8000/shop_site/cl_checkout/"}
            
    def login(self, name_field, pass_field):
        print("Logging in...")
        self.Username = name_field.text()
        url = PyQt5.QtCore.QUrl(self.url_list['login'])
        request = QNetworkRequest()
        request.setUrl(url)
        request.setHeader(PyQt5.QtNetwork.QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        data = PyQt5.QtCore.QByteArray()
        data.append(''.join(['user=', name_field.text(), '&']))
        data.append(''.join(['password=', pass_field.text()]))
        self.replyObjectLogin = self.manager.post(request, data)
        self.replyObjectLogin.finished.connect(self.loginFinalize)
            
    def loginFinalize(self):
        if self.replyObjectLogin.error() == PyQt5.QtNetwork.QNetworkReply.AuthenticationRequiredError:
            print("Failed")
            self.statusBar().showMessage('Failed')
        elif self.replyObjectLogin.error() == PyQt5.QtNetwork.QNetworkReply.NoError:
            self.user_token = bytes(self.replyObjectLogin.readAll()).decode("utf-8")
            self.login_status = True
            self.actUsername.setText(''.join(['Logged in as ', self.Username]))
            self.statusBar().showMessage('Logged in')
    
    def refresh(self):
        self.scrollAreaWidgetContents.setParent(None)
        self.getContent()
    
    def getContent(self):
        print("Getting content...")
        url = PyQt5.QtCore.QUrl(self.url_list['content'])
        request = QNetworkRequest()
        request.setUrl(url)
        self.replyObject = self.manager.get(request)
        self.replyObject.finished.connect(self.populateTable)
    
    def loginDialog(self):
        dl = PyQt5.QtWidgets.QDialog(parent = self)
        dl.setWindowTitle("Log in Nothing Shop")
        dl.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
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
    
    def populateTable(self):
        answerAsJson = bytes(self.replyObject.readAll()).decode("utf-8")
        answerAsText = json.loads(answerAsJson)
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
        MerchNumList = []
        BuyButtonList = []
        MerchBoxHWidgetList = []
        MerchBoxH1LayoutList = []
        MerchBoxH2LayoutList = []
        MerchBoxV1LayoutList = []
        MerchBoxV2LayoutList = []
        pixmap1 = PyQt5.QtGui.QPixmap('no_image.png')
        for merch in answerAsText:
            MerchBoxList.append(QtWidgets.QGroupBox(self.scrollAreaWidgetContents))
            #MerchBoxList[-1].setObjectName("merchBox1")
            MerchBoxList[-1].setTitle(merch['name'])
            MerchBoxHWidgetList.append(QtWidgets.QWidget(MerchBoxList[-1]))
            #MerchBoxHWidgetList[-1].setGeometry(QtCore.QRect(5, 15, 620, 160))
            MerchBoxH1LayoutList.append(QtWidgets.QHBoxLayout(MerchBoxHWidgetList[-1]))
            MerchBoxH1LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxH1LayoutList[-1].setContentsMargins(0, 0, 10, 6)
            MerchBoxH1LayoutList[-1].setSpacing(10)
            ImageLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            ImageLabelList[-1].setMinimumSize(QtCore.QSize(150, 150))
            ImageLabelList[-1].setAlignment(QtCore.Qt.AlignCenter)
            ImageLabelList[-1].setPixmap(pixmap1)
            #self.merchImage1.setObjectName("merchImage1")
            MerchBoxH1LayoutList[-1].addWidget(ImageLabelList[-1])
            
            MerchBoxV1LayoutList.append(QtWidgets.QVBoxLayout())
            MerchBoxV1LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxV1LayoutList[-1].setContentsMargins(0, 0, 10, 10)
            MerchBoxV1LayoutList[-1].setSpacing(10)
            #MerchBoxV1LayoutList[-1].setObjectName("verticalLayout")
            NameLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            NameLabelList[-1].setText(merch['name'])
            #self.nameLabel1.setObjectName("nameLabel1")
            MerchBoxV1LayoutList[-1].addWidget(NameLabelList[-1])
            DescBoxList.append(QtWidgets.QTextEdit(MerchBoxHWidgetList[-1]))
            DescBoxList[-1].setPlainText(merch['desc'])
            DescBoxList[-1].setReadOnly(True)
            #self.merchDesc1.setObjectName("merchDesc1")
            MerchBoxV1LayoutList[-1].addWidget(DescBoxList[-1])
            MerchBoxH1LayoutList[-1].addLayout(MerchBoxV1LayoutList[-1])
            
            MerchBoxV2LayoutList.append(QtWidgets.QVBoxLayout())
            MerchBoxV2LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxV2LayoutList[-1].setContentsMargins(0, 0, 10, 10)
            MerchBoxV2LayoutList[-1].setSpacing(10)
            #MerchBoxV2LayoutList[-1].setObjectName("verticalLayout_2")
            RemainLabelList.append(QtWidgets.QLabel(MerchBoxHWidgetList[-1]))
            RemainLabelList[-1].setAlignment(QtCore.Qt.AlignCenter)
            RemainLabelList[-1].setText('Remaining: ' + str(merch['quantity']))
            #self.RemainingLabel1.setObjectName("RemainingLabel1")
            MerchBoxV2LayoutList[-1].addWidget(RemainLabelList[-1])
            MerchBoxH2LayoutList.append(QtWidgets.QHBoxLayout())
            MerchBoxH2LayoutList[-1].setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            MerchBoxH2LayoutList[-1].setContentsMargins(0, 0, 0, 0)
            MerchBoxH2LayoutList[-1].setSpacing(10)
            #self.horizontalLayout.setObjectName("horizontalLayout")
            MerchNumList.append(QtWidgets.QSpinBox(MerchBoxHWidgetList[-1]))
            MerchNumList[-1].setMinimum(1)
            MerchNumList[-1].setMaximum(merch['quantity'])
            #self.merchNum.setObjectName("merchNum")
            MerchBoxH2LayoutList[-1].addWidget(MerchNumList[-1])
            BuyButtonList.append(QtWidgets.QPushButton(MerchBoxHWidgetList[-1]))
            BuyButtonList[-1].setText("Buy")
            #self.BuyButton1.setObjectName("BuyButton1")
            MerchBoxH2LayoutList[-1].addWidget(BuyButtonList[-1])
            MerchBoxV2LayoutList[-1].addLayout(MerchBoxH2LayoutList[-1])
            MerchBoxH1LayoutList[-1].addLayout(MerchBoxV2LayoutList[-1])
            
            MerchBoxV1LayoutList[-1].addStretch(1)
            #MerchBoxV2LayoutList[-1].addStretch(1)
            #MerchBoxH1LayoutList[-1].addStretch(1)
            MerchBoxH2LayoutList[-1].addStretch(1)
            MerchBoxH1LayoutList[-1].setStretch(0, 3)
            MerchBoxH1LayoutList[-1].setStretch(1, 8)
            MerchBoxH1LayoutList[-1].setStretch(2, 2)
            MerchBoxList[-1].setLayout(MerchBoxH1LayoutList[-1])
            self.mainVerticalLayer.addWidget(MerchBoxList[-1])
        self.merchList.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.merchList)
        
    def clExit(self):
        app.quit()

   
if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()