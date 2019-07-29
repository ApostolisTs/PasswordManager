import sqlite3


class Database(object):

    def __init__(self):
        pass

    def connect(self):
        self.__conn = sqlite3.connect('password_keeper.db')
        self.__cursor = self.__conn.cursor()

    def insert_user(self, username, password):
        self.__cursor.execute("""INSERT INTO users VALUES (:username, :password)""",
                              {'username': username, 'password': password})
        self.__conn.commit()

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def select_user(self):
        pass

    def insert_account(self):
        pass

    def update_account(self):
        pass

    def delete_account(self):
        pass

    def select_account(self):
        pass
