import sys
from sqlite3 import IntegrityError
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog, QPushButton,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.uic import loadUi
from database import Database


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

        # Map button clicks to methods.
        self.login_reg_button.clicked.connect(self.login_clicked)
        self.cancel_button.clicked.connect(self.close)

    def login_clicked(self):
        username = self.username_txt.text()
        password = self.password_txt.text()

        credentials = Database.select_user(username)

        if credentials and (credentials[1] == password):
            self.account_page = AccountsPage(list(credentials))
            self.account_page.show()
            self.welcome_page.close()
            self.close()
        else:
            self.show_error_message()

    def show_error_message(self):
        """ Shows an error message if the username or the password are incorrect. """

        popup = QMessageBox()
        popup.setWindowTitle('Information')
        popup.setIcon(QMessageBox.Information)
        popup.setText('Wrong password or username!')
        popup.exec_()


class RegisterPage(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('./ui/login_register_page.ui', self)
        self.header_label.setText('Register')
        self.login_reg_button.setText('Register')

        # Map button clicks to methods.
        self.login_reg_button.clicked.connect(self.register_clicked)
        self.cancel_button.clicked.connect(self.close)

    def register_clicked(self):
        username = self.username_txt.text()
        password = self.password_txt.text()

        try:
            Database.insert_user(username, password)
            self.show_info_message(success=True)
            self.close()
        except IntegrityError as e:
            self.show_popup_message(success=False)

    def show_popup_message(self, success):
        """ Shows an information window that informs the user if their
        registration was successful or not. """

        popup = QMessageBox()
        if success:
            popup.setWindowTitle('Information')
            popup.setIcon(QMessageBox.Information)
            popup.setText('You registered successfully!')
        else:
            popup.setWindowTitle('Error')
            popup.setIcon(QMessageBox.Critical)
            popup.setText(
                'This username is taken!\nPlease choose another username!')
        popup.exec_()


class AccountsPage(QWidget):

    def __init__(self, credentials):
        super().__init__()
        self.credentials = credentials
        loadUi('./ui/accounts.ui', self)  # Load the ui file.
        self.set_username_label()
        self.populate_table()

        # Customize its column's resize mode seperately.
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        # Map button clicks to methods.
        self.add_button.clicked.connect(self.add_account_clicked)
        self.delete_button.clicked.connect(self.delete_account_clicked)
        self.modify_button.clicked.connect(self.modify_account_clicked)
        self.user_settings_button.clicked.connect(self.user_settings_clicked)
        self.logout_button.clicked.connect(self.logout_clicked)

    def populate_table(self):
        """ Populates the table with the accounts of the logged in user that
        are stored in the database. """

        accounts = Database.select_accounts_by_user(self.credentials[0])
        self.table.setRowCount(len(accounts))
        for i, account in enumerate(accounts):
            # Setting the account ID.
            self.table.setItem(i, 0, QTableWidgetItem(str(account[0])))

            # Setting the account type.
            self.table.setItem(i, 1, QTableWidgetItem(account[1]))

            if account[2]:
                # Setting a username if there is one.
                self.table.setItem(i, 2, QTableWidgetItem(account[2]))
            else:
                self.table.setItem(i, 2, QTableWidgetItem('No username'))

            # Setting the account email.
            self.table.setItem(i, 3, QTableWidgetItem(account[3]))

            # Setting the account password to stars '*' so it won't be visible right away.
            self.table.setItem(i, 4, QTableWidgetItem('**********'))

            # Setting a button that when clicked shows the password to the user.
            btn = QPushButton('Show Password')
            self.table.setCellWidget(i, 5, btn)
            btn.clicked.connect(self.show_password_clicked)

    def set_username_label(self):
        """ Sets the username label on the top of the window. """
        self.username_label.setText(
            'Hello %s, your passwords are:' % (self.credentials[0]))

    def show_password_clicked(self):
        """ Shows the ShowPasswordPage where the user can see a specific account password. """

        row = self.table.currentRow()
        account_id = self.table.item(row, 0).text()
        account_type = self.table.item(row, 1).text()

        self.show_password_page = ShowPasswordPage(
            account_id, account_type, self.credentials)
        self.show_password_page.show()

    def add_account_clicked(self):
        """ Shows the AddAccountPage for the user to add an account. """

        self.add_accounts_page = AddAccountPage(self)
        self.add_accounts_page.show()

    def delete_account_clicked(self):
        """ Deletes an account from the database and the table in accounts page. """

        selected_account = self.table.selectedItems()
        if selected_account:
            selected_account_id = selected_account[0].text()
            self.table.removeRow(self.table.currentRow())
            Database.delete_account_by_id(selected_account_id)
        else:
            self.show_error_message()

    def modify_account_clicked(self):
        """ Shows the ModifyAccountPage for the user to edit their account information. """

        selected_account = self.table.selectedItems()
        if selected_account:
            account_id = selected_account[0].text()
            self.modify_account_page = ModifyAccountPage(self, account_id)
            self.modify_account_page.show()
        else:
            self.show_error_message()

    def user_settings_clicked(self):
        """ Shows the UserSettingsPage for the user to edit their information. """

        self.user_settings_page = UserSettingsPage(self)
        self.user_settings_page.show()

    def logout_clicked(self):
        self.close()

    def show_error_message(self):
        """ Shows an error message if the user hasn't selected a row or an account
        from the table when he pressed the Delete or Modify Account button. """

        popup = QMessageBox()
        popup.setWindowTitle('Error')
        popup.setIcon(QMessageBox.Critical)
        popup.setText('Please select a row/account from the table!')
        popup.exec_()


class UserSettingsPage(QWidget):

    def __init__(self, accounts_page):
        super().__init__()
        self.accounts_page = accounts_page
        loadUi('./ui/user_settings.ui', self)
        self.username_txt.setText(self.accounts_page.credentials[0])
        self.password_txt.setText(self.accounts_page.credentials[1])

        # Map button clicks to methods.
        self.save_button.clicked.connect(self.save_clicked)
        self.cancel_button.clicked.connect(self.close)

    def save_clicked(self):
        """ Saves the new username and new password in the database and refreshes
        the accounts page. """

        new_username = self.username_txt.text()
        new_password = self.password_txt.text()

        if not (self.accounts_page.credentials[0] == new_username and self.accounts_page.credentials[1] == new_password):
            try:
                Database.update_user(
                    self.accounts_page.credentials[0], new_username, new_password)
                Database.update_user_field_in_accounts(
                    new_username, self.accounts_page.credentials[0])
                self.accounts_page.credentials[0] = new_username
                self.accounts_page.set_username_label()
                self.close()
            except IntegrityError as e:
                self.show_error_message()

    def show_error_message(self):
        popup = QMessageBox()
        popup.setWindowTitle('Error')
        popup.setIcon(QMessageBox.Critical)
        popup.setText(
            'This username is taken!\nPlease choose another username!')
        popup.exec_()


class AddAccountPage(QWidget):

    def __init__(self, accounts_page):
        super().__init__()
        self.accounts_page = accounts_page
        loadUi('./ui/add_account_page.ui', self)

        # Map button clicks to methods.
        self.cancel_button.clicked.connect(self.close)
        self.add_account_button.clicked.connect(self.add_account_clicked)

    def add_account_clicked(self):
        """ Adds an account to the database and refreshes the table in the
        accounts page. """

        account_type = self.account_txt.text()
        username = self.username_txt.text() if self.username_txt.text() else None
        email = self.email_txt.text()
        password = self.password_txt.text()

        if not (account_type and email and password):
            self.show_error_message()
        else:
            Database.insert_account(account_type, username, email,
                                    password, self.accounts_page.credentials[0])
            self.accounts_page.populate_table()
            self.close()

    def show_error_message(self):
        """ Shows an error message if the required fields are not filled. """

        popup = QMessageBox()
        popup.setWindowTitle('Error')
        popup.setIcon(QMessageBox.Critical)
        popup.setText('Please fill all the required fields!')
        popup.exec_()


class ModifyAccountPage(QWidget):

    def __init__(self, accounts_page, account_id):
        super().__init__()
        loadUi('./ui/modify_account_page.ui', self)
        self.accounts_page = accounts_page
        account_info = Database.select_account_by_id(account_id)
        self.account_id_label.setText('Account ID-%s' % (account_id))
        self.account_type_txt.setText(account_info[0])
        self.username_txt.setText(account_info[1])
        self.email_txt.setText(account_info[2])
        self.password_txt.setText(account_info[3])

        # Map button clicks to methods.
        self.save_button.clicked.connect(lambda: self.save_clicked(account_id))
        self.cancel_button.clicked.connect(self.close)

    def save_clicked(self, account_id):
        """ Saves the changes made to the selected account. """

        account_type = self.account_type_txt.text()
        username = self.username_txt.text()
        email = self.email_txt.text()
        password = self.password_txt.text()

        if not (account_type and email and password):
            self.show_error_message()
        else:
            Database.update_account_by_id(
                account_id, account_type, username, email, password)
            self.accounts_page.populate_table()
            self.close()

    def show_error_message(self):
        """ Shows an error message if the required fields are not filled. """

        popup = QMessageBox()
        popup.setWindowTitle('Error')
        popup.setIcon(QMessageBox.Critical)
        popup.setText('Please fill all the required fields!')
        popup.exec_()


class ShowPasswordPage(QWidget):

    def __init__(self, account_id, account_type, credentials):
        super().__init__()
        loadUi('./ui/show_password_page.ui', self)

        # Map button clicks to methods.
        self.show_button.clicked.connect(
            lambda: self.show_password(account_id, account_type, credentials))
        self.cancel_button.clicked.connect(self.close)

    def show_password(self, account_id, account_type, credentials):
        password = self.password_txt.text()

        if password == credentials[1]:
            account_password = Database.select_account_password_by_id(
                account_id)
            self.password_label.setText(
                'Your %s password is:\n %s' % (account_type, account_password[0]))


def main(argv):
    app = QApplication(argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
