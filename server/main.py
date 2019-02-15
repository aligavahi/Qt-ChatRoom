from server import Server
from PyQt5.QtCore import QCoreApplication

if __name__ == '__main__':
    app = QCoreApplication([])
    server = Server()
    app.exec()