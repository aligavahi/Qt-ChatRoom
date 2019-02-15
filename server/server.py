from PyQt5.QtNetwork import QTcpServer, QHostAddress, QTcpSocket
from PyQt5.QtCore import QIODevice, QDataStream, QByteArray
from json import loads
from client import Client
from time import sleep


class Server:
    def __init__(self, ip="127.0.0.1", port=8585):
        self.server = QTcpServer()
        self.server.listen(QHostAddress(ip), port)
        self.server.newConnection.connect(self.add_client)
        self.clients = []
        self.msgs = []

    def add_client(self):
        clientConnection = self.server.nextPendingConnection()
        clientConnection.readyRead.connect(lambda: self.read(clientConnection))
        self.clients.append(Client(clientConnection))

    def read(self, socket: QTcpSocket):
        arrayData = socket.readAll()
        inp = QDataStream(arrayData, QIODevice.ReadWrite)
        json_data = loads(inp.readQString())
        print(json_data)
        key = json_data["flag"]
        if key == "register":
            self.register(socket, json_data["name"], json_data["user_name"], json_data["pass_word"])
        elif key == "login":
            self.login(socket, json_data["user_name"], json_data["pass_word"])
        elif key == "msg":
            self.save_msg(json_data["msg"], socket)
        elif key == "logout":
            self.logout(socket)
        else:
            print("invalid key")

    def register(self, socket: QTcpSocket, name, userName, passWord):
        if any(client for client in self.clients if client.name == name or client.user_name == userName):
            socket.write(self.toByteArray("failedr"))
        else:
            for client in self.clients:
                if client.socket == socket:
                    client.name = name
                    client.pass_word = passWord
                    client.user_name = userName
                    client.setLogin(True)
                    socket.write(self.toByteArray("ok"))
                    self.sendAllMsg(socket)
                    break

    def login(self, socket: QTcpSocket, userName, passWord):
        loggedin = False
        for client in self.clients:
            if client.user_name == userName and client.pass_word == passWord and not client.isLogin():
                client.socket = socket
                client.setLogin(True)
                loggedin = True
                socket.write(self.toByteArray("ok"))
                self.sendAllMsg(socket)
                break

        if not loggedin:
            socket.write(self.toByteArray("failedl"))

    def save_msg(self, msg, socket):
        for client in self.clients:
            if client.socket == socket and client.isLogin():
                name = client.name
                self.msgs.append(name + " :   " + msg)
                for receiver in self.clients:
                    if receiver.isLogin():
                        receiver.socket.write(self.toByteArray(name + " :   " + msg))
                return

    def logout(self, socket):
        for client in self.clients:
            if client.socket == socket:
                client.setLogin(False)
                break

    def sendAllMsg(self, socket):
        for msg in self.msgs:
            socket.write(self.toByteArray(msg))

    def toByteArray(self, data):
        toArrayData = QByteArray()
        out = QDataStream(toArrayData, QIODevice.ReadWrite)
        out.writeQString(data)
        return toArrayData
