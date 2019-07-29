import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog,
                             QTableWidgetItem, QHeaderView)
from PyQt5.uic import loadUi
from database import Database

# db = Database()
# db.connect()


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
            # testing database.
            # db.insert_user(self.username, self.password)
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
        loadUi('./ui/accounts.ui', self)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # CODE TO CUSTOMIZE ITS COLUMN'S RESIZE MODE SEPERATELY.
        # header = self.table.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.fill_table()
        self.username_label.setText(
            'Hello %s, your passwords are:' % (username))
        self.add_button.clicked.connect(self.add_clicked)
        self.delete_button.clicked.connect(self.delete_clicked)
        self.modify_button.clicked.connect(self.modify_clicked)
        self.logout_button.clicked.connect(self.logout_clicked)

    def fill_table(self):
        account_1 = {'id': 1, 'Account': 'Fb', 'username': 'apostolis',
                     'email': 'me', 'password': '**********'}
        account_2 = {'id': 2, 'Account': 'Fb', 'username': 'apostolis',
                     'email': 'me', 'password': '**********'}
        account_3 = {'id': 3, 'Account': 'Fb', 'username': 'apostolis',
                     'email': 'me', 'password': '**********'}
        account_4 = {'id': 4, 'Account': 'Fb', 'username': 'apostolis',
                     'email': 'me', 'password': '**********'}

        accounts = []
        accounts.append(account_1)
        accounts.append(account_2)
        accounts.append(account_3)
        accounts.append(account_4)

        self.table.setRowCount(len(accounts))
        for i, account in enumerate(accounts):

            self.table.setItem(i, 0, QTableWidgetItem(str(account['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(account['Account']))
            self.table.setItem(i, 2, QTableWidgetItem(account['username']))
            self.table.setItem(i, 3, QTableWidgetItem(account['email']))
            self.table.setItem(i, 4, QTableWidgetItem(account['password']))

    def add_clicked(self):
        pass

    def delete_clicked(self):
        pass

    def modify_clicked(self):
        pass

    def logout_clicked(self):
        self.close()


def main(argv):
    app = QApplication(argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
