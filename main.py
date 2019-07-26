import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog
from PyQt5.uic import loadUi


class WelcomePage(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/welcome_page.ui', self)

        self.login_button.clicked.connect(self.login_clicked)
        self.register_button.clicked.connect(self.register_clicked)

    def login_clicked(self):
        print(self.sender())
        self.login_page = LoginRegisterPage(self.sender())
        self.login_page.show()

    def register_clicked(self):
        print(self.sender())
        self.register_page = LoginRegisterPage(self.sender())
        self.register_page.show()


class LoginRegisterPage(QWidget):

    def __init__(self, sender):
        super().__init__()
        loadUi('./ui/login_reg_page.ui', self)

        if sender.text() == 'Register':
            self.header_label.setText('Register')
            self.login_reg_button.setText('Register')
            self.login_reg_button.clicked.connect(self.register_clicked)
        else:
            self.login_reg_button.clicked.connect(self.login_clicked)

        self.cancel_button.clicked.connect(self.close)

    def login_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        print('Username: %s Password: %s' % (self.username, self.password))

    def register_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        print('Username: %s Password: %s' % (self.username, self.password))


class RegisterPage(QWidget):

    def __init__(self):
        super().__init__()


class Page(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/page.ui', self)

        self.back_button.clicked.connect(self.back)

    def back(self):
        self.login_page = LoginPage()
        self.close()
        self.login_page.show()


def main(argv):
    app = QApplication(argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
