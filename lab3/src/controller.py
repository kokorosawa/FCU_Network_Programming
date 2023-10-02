import typing
from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess,subprocess
import os,sys,time
from PyQt6.QtCore import QThread, pyqtSignal,QProcess,QObject
from mail import Mail

class EmittingStr(QObject):
    textwriter = pyqtSignal(str)
    
    def write(self, text):
        self.textwriter.emit(str(text))
        QtWidgets.QApplication.processEvents()

class MainWindow(QtWidgets.QMainWindow):
    signal = pyqtSignal()
    msg = ""
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.init_text()
        self.ui.logIn.clicked.connect(self.login)
        self.ui.listMail.clicked.connect(self.listAllMail)
        self.ui.listMailDetail.clicked.connect(self.listMailDetail)
        self.ui.showMailContext.clicked.connect(self.showMailcontext)
        self.ui.deleteMail.clicked.connect(self.deleteMail)
        self.ui.quit.clicked.connect(self.quit)
        sys.stdout = EmittingStr(textwriter=self.display)
        
    def init_text(self):
        self.ui.username.setText("iecs07")
        self.ui.password.setText("3SmUnqYy")
        
    def login(self):
        self.username = self.ui.username.text()
        self.password = self.ui.password.text()
        self.mail = Mail(self.username, self.password)
        self.mail.ready()
        self.mail.logIn()
        
    def display(self,log: str):
        self.ui.displayBox.append(log)
    
    def listAllMail(self):
        self.ui.displayBox.setText("")
        self.mail.listMailNum()
        
    def listMailDetail(self):
        self.ui.displayBox.setText("")
        self.readNumber = self.ui.listMailNumber.text()
        self.mail.readMail(self.readNumber)
        
    def showMailcontext(self):
        self.ui.displayBox.setText("")
        self.mail.showMailcontext(self.ui.listMailNumber.text())
        
    def deleteMail(self):
        self.ui.displayBox.setText("")
        self.mail.deleteMail(self.ui.deleteMailNumber.text())
    
    def quit(self):
        self.ui.displayBox.setText("")
        self.mail.quit()
        
# class MailTask(QThread):
#     def __init__(self,username,password):
#         self.username = username
#         self.passwrod = password
#         super().__init__()
    
#     def run(self):
#         self.mail = Mail(self.username, self.passwrod)