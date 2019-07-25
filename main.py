import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog
from PyQt5.uic import loadUi


class WelcomePage(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/welcome_page.ui', self)

        self.login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        user = 'Apostolis'
        password = 'Me'
        self.login_page = LoginPage(user, password)
        self.close()
        self.login_page.show()


class LoginPage(QWidget):

    def __init__(self, user=None, password=None):
        super().__init__()
        loadUi('./ui/login_page.ui', self)
        self.user = user
        self.password = password
        print(self.user, self.password)

        self.cancel_button.clicked.connect(self.cancel_clicked)

    def cancel_clicked(self):
        self.welcome_page = WelcomePage()
        self.close()
        self.welcome_page.show()


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
