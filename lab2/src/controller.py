from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess,subprocess
import os,sys
from PyQt6.QtCore import QThread, pyqtSignal,QProcess,QObject

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
        
    def openServer(self):
        # getter = Getter(self)
        # getter.start()
        # getter.resultChanged.connect(self.ui.serverLog.append)
        self.process = QProcess()
        # self.ui.serverLog.setText(self.process.readAllStandardOutput)
        # print(self.process.readAllStandardOutput.decode())
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.start("python3" , ["server.py"])
        while 1:
            
            self.process.waitForReadyRead()
            output = self.process.readAllStandardOutput
            output = bytearray(output).decode('gbk')
            self.PID = self.process.processId()
            if output != ' ':
                for i in output.split('\r\n')[:-1]:
                    print(i)
            if self.PID == 0:
                 break
        
    def addStdOut(self):
        output = bytes(self.process.readAllStandardOutput()).decode()   
        self.ui.serverLog.setText(output) 
        
    def addStdErr(self):
        output = bytes(self.process.readAllStandardError()).decode()      
       
        

class Process(QtCore.QObject):

    stdout = QtCore.pyqtSignal(str)
    stderr = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    def start(self, program, args):
        process = QtCore.QProcess()
        process.setProgram(program)
        process.setArguments(args)
        process.readyReadStandardError.connect(lambda: self.stderr.emit(process.readAllStandardError()))
        process.readyReadStandardOutput.connect(lambda: self.stderr.emit(process.readAllStandardOutput()))
        process.finished.connect(self.finished)
        process.start()
        
        self._process = process