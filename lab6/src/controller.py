import typing
from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess,subprocess
import os,sys,time
from PyQt6.QtCore import QThread, pyqtSignal,QProcess,QObject
from server import server_task
from client import client_task


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
        self.set_control()
        self.ui.serverPort.setText("6666")
        sys.stdout = EmittingStr(textwriter=self.update_console)
    
    def set_control(self):
        self.ui.serverPort.textChanged.connect(self.setClientConnectPort)
        self.ui.openServer.clicked.connect(self.openServer)
        self.ui.openClient.clicked.connect(self.openClient)
    
    def openClient(self):
        self.qthread = ClientTask(self.ui.serverPort.text(), self.ui.inputNum.text())
        self.qthread.start()
        
    def signalListener(self):
        print('收到信號')

    def setClientConnectPort(self):
        self.ui.clientConnectPort.setText(self.ui.serverPort.text())

    def openServer(self):
        self.qthread = ServerTask(self.ui.serverPort.text())
        self.qthread.start()
        
        
    def progress_changed(self, value):  
        self.ui.openServer.clicked.connect(lambda:self.signal.emit())
        self.ui.serverLog.setText(str(value))
        
    def update_console(self, log: str):
        if "Server" in log:
            self.ui.serverLog.append(log)
        if "Client" in log:
            self.ui.clientLog.append(log)
    
class ServerTask(QThread):
    def __init__(self,port):
        self.port = port
        super().__init__()
    
    def run(self):
        server_task(self.port)
        
class ClientTask(QThread):
    def __init__(self,port,num):
        self.num = num
        self.port = port
        super().__init__()
    
    def run(self):
        client_task(int(self.port),int(self.num))   