import typing
from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess, subprocess
import os, sys, time
from PyQt6.QtCore import QThread, pyqtSignal, QProcess, QObject
from server import server_task
from producer import producer_task
from consumer import consumer_task


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
        sys.stdout = EmittingStr(textwriter=self.update_console)

    def set_control(self):
        self.ui.openConsumer.clicked.connect(self.openConsumer)
        self.ui.openProducer.clicked.connect(self.openProducer)
        self.ui.openServer.clicked.connect(self.openServer)

    def openConsumer(self):
        self.qthread = ConsumerTask()
        self.qthread.start()

    def openProducer(self):
        self.qthread = ProducerTask(self.ui.NumberBox.text())
        self.qthread.start()

    def openServer(self):
        self.qthread = ServerTask()
        self.qthread.start()

    def update_console(self, log: str):
        if "Server" in log:
            self.ui.Server.append(log)
        if "Producer" in log:
            self.ui.Producer.append(log)
        if "Consumer" in log:
            self.ui.Consumer.append(log)
        if "Queue" in log:
            self.ui.Queue.append(log)


class ServerTask(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        server_task()


class ProducerTask(QThread):
    def __init__(self, num):
        self.num = num
        super().__init__()

    def run(self):
        producer_task(int(self.num))


class ConsumerTask(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        consumer_task()
