import typing
from PyQt6 import QtWidgets, QtGui, QtCore
from view import Ui_Form
import subprocess
import subprocess
import os
import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal, QProcess, QObject
from Client import Client


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
        self.client = Client()
        self.ui.registerButton.clicked.connect(self.register)
        self.ui.create.clicked.connect(self.create)
        self.ui.subject.clicked.connect(self.subject)
        self.ui.reply.clicked.connect(self.reply)
        self.ui.discussion.clicked.connect(self.discussion)
        self.ui.quit.clicked.connect(self.delete)
        sys.stdout = EmittingStr(textwriter=self.display)

    def register(self):
        self.ui.displayBox.setText("")
        username = self.ui.username.text()
        password = self.ui.password.text()
        self.client.register(username, password)

    def create(self):
        self.ui.displayBox.setText("")
        topic_name = self.ui.createTopicName.text()
        description = self.ui.description.text()
        founder_name = self.ui.username.text()
        self.client.create(topic_name, description, founder_name)

    def subject(self):
        self.ui.displayBox.setText("")
        self.client.subject()

    def reply(self):
        self.ui.displayBox.setText("")
        topic_name = self.ui.replyTopicName.text()
        username = self.ui.username.text()
        content = self.ui.replyBox.toPlainText()
        self.client.reply(topic_name, username, content)

    def discussion(self):
        self.ui.displayBox.setText("")
        topic_name = self.ui.viewTopicName.text()
        self.client.discussion(topic_name)

    def delete(self):
        self.ui.displayBox.setText("")
        topic_name = self.ui.deleteTopicName.text()
        self.client.delete(topic_name)

    def display(self, log: str):
        self.ui.displayBox.append(log)
