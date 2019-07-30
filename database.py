import sqlite3


class Database(object):

    def __init__(self):
        self.__conn = sqlite3.connect('database.db')
        self.__cursor = self.__conn.cursor()

    def insert_user(self, username, password):
        self.__cursor.execute("""INSERT INTO users VALUES (:username, :password);""",
                              {'username': username, 'password': password})
        self.__conn.commit()

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def select_user(self):
        self.__cursor.execute("""SELECT * FROM users;""")
        return self.__cursor.fetchall()

    def insert_account(self, account, username, email, password, user):
        self.__cursor.execute("""INSERT INTO accounts (account, username, email, password, user)
                                VALUES (:account, :username, :email, :password, :user);""",
                              {'account': account, 'username': username, 'email': email, 'password': password, 'user': user})
        self.__conn.commit()

    def update_account(self):
        pass

    def delete_account(self):
        pass

    def select_account(self):
        self.__cursor.execute("""SELECT * FROM accounts;""")
        return self.__cursor.fetchall()
