from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess,subprocess
import os,sys,time
from PyQt6.QtCore import QThread, pyqtSignal,QProcess,QObject
from server import server_task
class EmittingStr(QObject):
    textwriter = pyqtSignal(str)
    
    def write(self, text):
        self.textwriter.emit(str(text))
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
		# in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.serverPort.setText("6666")
        self.ui.serverPort.textChanged.connect(self.setClientConnectPort)
        self.ui.openServer.clicked.connect(self.openServer)
        # sys.stdout = EmittingStr(textwriter=self.outputWritten)
        # sys.stderr = EmittingStr(textwriter=self.outputWritten)
        
    def outputWritten(self, text):
        cursor = self.ui.serverLog.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.serverLog.setTextCursor(cursor)
        self.ui.serverLog.ensureCursorVisible()

    def setClientConnectPort(self):
        self.ui.clientConnectPort.setText(self.ui.serverPort.text())
        
    def outputWritten(self, text):
        cursor = self.ui.serverLog.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.serverLog.setTextCursor(cursor)
        self.ui.serverLog.ensureCursorVisible()

    def openServer(self):
        self.qthread = ThreadTask()
        self.ui.serverLog.setText("1")
        self.qthread.qthread_signal.connect(self.progress_changed) 
        self.qthread.start_progress()
        
    def progress_changed(self, value):        
       self.ui.serverLog.setText(str(value))
class ThreadTask(QThread):
    qthread_signal = pyqtSignal(int)

    def start_progress(self):
        max_value = 100
        for i in range(max_value):
            time.sleep(0.1)
            print('WorkerThread::run ' + str(i))
            self.qthread_signal.emit(i+1)