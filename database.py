import sqlite3


class Database(object):

    __conn = sqlite3.connect('database.db')
    __cursor = __conn.cursor()

    @classmethod
    def insert_user(cls, username, password):
        cls.__cursor.execute("""INSERT INTO users VALUES (:username, :password);""",
                             {'username': username, 'password': password})
        cls.__conn.commit()

    @classmethod
    def update_user(cls, old_username, new_username, new_password):
        cls.__cursor.execute("""UPDATE users SET username = :new_username, password = :password
                                    WHERE username = :old_username;""",
                             {'new_username': new_username, 'password': new_password, 'old_username': old_username})
        cls.__conn.commit()

    @classmethod
    def delete_user(cls):
        pass

    @classmethod
    def select_user(cls, username):
        cls.__cursor.execute("""SELECT * FROM users WHERE username = :username;""",
                             {'username': username})
        return cls.__cursor.fetchone()

    @classmethod
    def insert_account(cls, account_type, username, email, password, user):
        cls.__cursor.execute("""INSERT INTO accounts (account_type, username, email, password, user)
                                    VALUES (:account_type, :username, :email, :password, :user);""",
                             {'account_type': account_type, 'username': username, 'email': email, 'password': password, 'user': user})
        cls.__conn.commit()

    @classmethod
    def update_account_by_id(cls, id, account_type, username, email, password):
        cls.__cursor.execute(""" UPDATE accounts SET account_type = :account_type,
                                    username = :username, email = :email, password = :password
                                    WHERE id = :id;""",
                             {'id': id, 'account_type': account_type, 'username': username, 'email': email, 'password': password})
        cls.__conn.commit()

    @classmethod
    def update_user_field_in_accounts(cls, new_username, old_username):
        cls.__cursor.execute("""UPDATE accounts SET user = :new_username
                                    WHERE user = :old_username;""",
                             {'new_username': new_username, 'old_username': old_username})
        cls.__conn.commit()

    @classmethod
    def delete_account_by_id(cls, id):
        cls.__cursor.execute("""DELETE FROM accounts WHERE id= :id; """,
                             {'id': id})
        cls.__conn.commit()

    @classmethod
    def select_account_by_id(cls, id):
        cls.__cursor.execute("""SELECT account_type, username, email, password FROM accounts
                                    WHERE id = :id;""",
                             {'id': id})
        return cls.__cursor.fetchone()

    @classmethod
    def select_accounts_by_user(cls, user):
        cls.__cursor.execute("""SELECT * FROM accounts WHERE user= :user;""",
                             {'user': user})
        return cls.__cursor.fetchall()

    @classmethod
    def select_account_password_by_id(cls, id):
        cls.__cursor.execute(""" SELECT password FROM accounts WHERE id = :id;""",
                             {'id': id})
        return cls.__cursor.fetchone()

    @classmethod
    def close(cls):
        cls.__conn.close()
