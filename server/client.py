States = {"not_login": 0, "login": 1}


class Client:
    def __init__(self, socket):
        self.socket = socket
        self.user_name = ""
        self.pass_word = ""
        self.name = ""
        self.state = States["not_login"]

    def setLogin(self, login):
        if login:
            self.state = States["login"]
        else:
            self.state = States["not_login"]

    def isLogin(self):
        if self.state == States["login"]:
            return True
        return False