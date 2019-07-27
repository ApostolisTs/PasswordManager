import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi


class WelcomePage(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/welcome_page.ui', self)

        self.login_button.clicked.connect(self.login_clicked)
        self.register_button.clicked.connect(self.register_clicked)

    def login_clicked(self):
        self.login_page = LoginPage(self)
        self.login_page.show()

    def register_clicked(self):
        self.register_page = RegisterPage()
        self.register_page.show()


class LoginPage(QWidget):

    def __init__(self, welcome_page):
        super().__init__()
        loadUi('./ui/login_reg_page.ui', self)

        self.welcome_page = welcome_page
        self.login_reg_button.clicked.connect(self.login_clicked)
        self.cancel_button.clicked.connect(self.close)

    def login_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        if self.username == 'Apostolis' and self.password == 'pass':
            self.account_page = AccountsPage(self.username)
            self.account_page.show()
            self.welcome_page.close()
            self.close()
        else:
            print('Wrong credentials')


class RegisterPage(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/login_reg_page.ui', self)

        self.header_label.setText('Register')
        self.login_reg_button.setText('Register')
        self.login_reg_button.clicked.connect(self.register_clicked)
        self.cancel_button.clicked.connect(self.close)

    def register_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        print('Username: %s Password: %s' % (self.username, self.password))


class AccountsPage(QWidget):

    def __init__(self, username):
        super().__init__()
        loadUi('./ui/passwords.ui', self)

        self.fill_table()
        self.username_label.setText(
            'Hello %s, your passwords are:' % (username))

    def fill_table(self):
        accounts = {'id': 1, 'Account': 'Fb',
                    'email': 'me', 'password': 'password'}

        self.table.setRowCount(1)
        self.table.setItem(0, 0, QTableWidgetItem(str(accounts['id'])))
        self.table.setItem(0, 1, QTableWidgetItem(accounts['Account']))
        self.table.setItem(0, 2, QTableWidgetItem(accounts['email']))
        self.table.setItem(0, 3, QTableWidgetItem(accounts['password']))


def main(argv):
    app = QApplication(argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
