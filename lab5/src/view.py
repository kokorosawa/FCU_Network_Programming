# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt6 UI code generator 6.5.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(556, 422)
        self.clear = QtWidgets.QPushButton(parent=Form)
        self.clear.setGeometry(QtCore.QRect(440, 370, 113, 32))
        self.clear.setObjectName("clear")
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(286, 216, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(24, 245, 58, 16))
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(parent=Form)
        self.label_6.setGeometry(QtCore.QRect(286, 245, 55, 16))
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(24, 274, 73, 16))
        self.label_2.setObjectName("label_2")
        self.serverPort = QtWidgets.QLineEdit(parent=Form)
        self.serverPort.setGeometry(QtCore.QRect(286, 274, 125, 21))
        self.serverPort.setObjectName("serverPort")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(24, 308, 123, 16))
        self.label_4.setObjectName("label_4")
        self.clientConnectPort = QtWidgets.QLabel(parent=Form)
        self.clientConnectPort.setGeometry(QtCore.QRect(286, 308, 33, 16))
        self.clientConnectPort.setObjectName("clientConnectPort")
        self.label_7 = QtWidgets.QLabel(parent=Form)
        self.label_7.setGeometry(QtCore.QRect(24, 337, 87, 16))
        self.label_7.setObjectName("label_7")
        self.serverLog = QtWidgets.QTextBrowser(parent=Form)
        self.serverLog.setGeometry(QtCore.QRect(24, 11, 256, 192))
        self.serverLog.setObjectName("serverLog")
        self.openClient = QtWidgets.QPushButton(parent=Form)
        self.openClient.setGeometry(QtCore.QRect(280, 367, 108, 32))
        self.openClient.setObjectName("openClient")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(24, 216, 63, 16))
        self.label.setObjectName("label")
        self.openServer = QtWidgets.QPushButton(parent=Form)
        self.openServer.setGeometry(QtCore.QRect(18, 367, 112, 32))
        self.openServer.setObjectName("openServer")
        self.clientLog = QtWidgets.QTextBrowser(parent=Form)
        self.clientLog.setGeometry(QtCore.QRect(286, 11, 256, 192))
        self.clientLog.setObjectName("clientLog")
        self.inputNum = QtWidgets.QLineEdit(parent=Form)
        self.inputNum.setGeometry(QtCore.QRect(286, 337, 125, 21))
        self.inputNum.setObjectName("inputNum")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.clear.setText(_translate("Form", "Clear"))
        self.label_5.setText(_translate("Form", "127.0.0.1"))
        self.label_3.setText(_translate("Form", "Client IP :"))
        self.label_6.setText(_translate("Form", "127.0.0.1"))
        self.label_2.setText(_translate("Form", "Server Port:"))
        self.label_4.setText(_translate("Form", "Client Connect Port:"))
        self.clientConnectPort.setText(_translate("Form", "6666"))
        self.label_7.setText(_translate("Form", "Input Number:"))
        self.openClient.setText(_translate("Form", "openClient"))
        self.label.setText(_translate("Form", "Server IP :"))
        self.openServer.setText(_translate("Form", "openServer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
