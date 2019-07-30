import sys
from sqlite3 import IntegrityError
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.uic import loadUi
from database import Database

db = Database()


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

        loadUi('./ui/login_register_page.ui', self)
        self.welcome_page = welcome_page
        self.login_reg_button.clicked.connect(self.login_clicked)
        self.cancel_button.clicked.connect(self.close)

    def login_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        credentials = db.select_from_users(self.username)

        if credentials and (credentials[0][1] == self.password):
            self.account_page = AccountsPage(self.username)
            self.account_page.show()
            self.welcome_page.close()
            self.close()
        else:
            self.show_error_message()

    def show_error_message(self):
        popup = QMessageBox()
        popup.setWindowTitle('Information')
        popup.setIcon(QMessageBox.Information)
        popup.setText('Wrong username!')
        popup.exec_()


class RegisterPage(QWidget):

    def __init__(self):
        super().__init__()

        loadUi('./ui/login_register_page.ui', self)
        self.header_label.setText('Register')
        self.login_reg_button.setText('Register')
        self.login_reg_button.clicked.connect(self.register_clicked)
        self.cancel_button.clicked.connect(self.close)

    def register_clicked(self):
        self.username = self.username_txt.text()
        self.password = self.password_txt.text()

        try:
            db.insert_user(self.username, self.password)
            self.show_info_message(success=True)
            self.close()
        except IntegrityError as e:
            self.show_info_message(success=False)

    def show_info_message(self, success):
        """ Creates a information window that informs the user if their
        registration was successful or not. """

        popup = QMessageBox()
        popup.setWindowTitle('Information')
        popup.setIcon(QMessageBox.Information)
        if success:
            popup.setText('You registered successfully!')
        else:
            popup.setText(
                'This username is taken!\nPlease choose another username!')
        popup.exec_()


class AccountsPage(QWidget):

    def __init__(self, user):
        super().__init__()
        self.user = user

        loadUi('./ui/accounts.ui', self)  # Load the ui file.

        # Customize its column's resize mode seperately.
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.populate_table()
        self.username_label.setText(
            'Hello %s, your passwords are:' % (self.user))

        # Map buttons to functions.
        self.add_button.clicked.connect(self.add_account_clicked)
        self.delete_button.clicked.connect(self.delete_account_clicked)
        self.modify_button.clicked.connect(self.modify_account_clicked)
        self.logout_button.clicked.connect(self.logout_clicked)

    def populate_table(self):
        accounts = db.select_from_accounts(self.user)

        self.table.setRowCount(len(accounts))
        for i, account in enumerate(accounts):
            self.table.setItem(i, 0, QTableWidgetItem(str(account[0])))
            self.table.setItem(i, 1, QTableWidgetItem(account[1]))
            if account[2]:
                self.table.setItem(i, 2, QTableWidgetItem(account[2]))
            else:
                self.table.setItem(i, 2, QTableWidgetItem('No username'))
            self.table.setItem(i, 3, QTableWidgetItem(account[3]))
            self.table.setItem(i, 4, QTableWidgetItem(account[4]))

    def add_account_clicked(self):
        # db.insert_account('facebook', 'testing', 'database',
        #                   'insert into', 'accounts table')
        pass

    def delete_account_clicked(self):
        pass

    def modify_account_clicked(self):
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
