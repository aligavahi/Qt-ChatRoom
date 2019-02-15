from mainWindow import Ui_MainWindow
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtGui import QCloseEvent
from json import dumps


class ClientApp(QMainWindow):
    def __init__(self, addr="127.0.0.1", port=8585):
        super(QMainWindow, self).__init__()
        self.socket = QTcpSocket()
        self.socket.connectToHost(addr, port)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sendBtn.clicked.connect(self.send_msg)
        self.ui.regBtn.clicked.connect(self.register)
        self.ui.logBtn.clicked.connect(self.login)
        self.socket.readyRead.connect(self.receive)
        self.show()

    def send_msg(self):
        msg = self.ui.sendLine.text()
        self.ui.sendLine.setText("")
        if msg != "":
            data = {"flag": "msg", "msg": msg}
            toArrayData = QByteArray()
            out = QDataStream(toArrayData, QIODevice.ReadWrite)
            out.writeQString(dumps(data))
            if self.socket.isOpen():
                if not self.socket.write(toArrayData):
                    print(" failed")
            else:
                print("connection not open")
        else:
            print("fill all field")

    def register(self):
        name = self.ui.registerName.text()
        userName = self.ui.registerUserName.text()
        passWord = self.ui.registerPassWord.text()
        if name != "" and userName != "" and passWord != "":
            data = {"flag": "register", "name": name, "user_name": userName, "pass_word": passWord}
            toArrayData = QByteArray()
            out = QDataStream(toArrayData, QIODevice.ReadWrite)
            out.writeQString(dumps(data))
            if self.socket.isOpen():
                if not self.socket.write(toArrayData):
                    print(" failed")
            else:
                print("connection not open")
        else:
            print("fill all field")

    def login(self):
        userName = self.ui.loginUserName.text()
        passWord = self.ui.loginPassWord.text()
        if userName != "" and passWord != "":
            data = {"flag": "login", "user_name": userName, "pass_word": passWord}
            toArrayData = QByteArray()
            out = QDataStream(toArrayData, QIODevice.ReadWrite)
            out.writeQString(dumps(data))
            if self.socket.isOpen():
                if not self.socket.write(toArrayData):
                    print(" failed")
            else:
                print("connection not open")
        else:
            print("fill all field")

    def receive(self):
        arrayData = self.socket.readAll()
        inp = QDataStream(arrayData, QIODevice.ReadWrite)
        msg = inp.readQString()
        while msg != "":
            if msg == "ok":
                self.freeze()
                self.ui.status.setText("you are logged in")
            elif msg == "failedl":
                self.ui.status.setText("login failed!! invalid username or password")
            elif msg == "failedr":
                self.ui.status.setText("register failed!! change username or name")
            else:
                self.ui.msg_veiw.append(msg)
            msg = inp.readQString()

    def closeEvent(self, event: QCloseEvent):
        data = {"flag": "logout"}
        toArrayData = QByteArray()
        out = QDataStream(toArrayData, QIODevice.ReadWrite)
        out.writeQString(dumps(data))
        self.socket.write(toArrayData)

    def freeze(self):
        self.ui.loginPassWord.setEnabled(False)
        self.ui.loginUserName.setEnabled(False)
        self.ui.registerUserName.setEnabled(False)
        self.ui.registerName.setEnabled(False)
        self.ui.registerPassWord.setEnabled(False)
        self.ui.logBtn.setEnabled(False)
        self.ui.regBtn.setEnabled(False)


if __name__ == '__main__':
    app = QApplication([])
    client = ClientApp()
    app.exec()
