import sqlite3


class Database(object):
    """ A Database class that interacts with the actual database. """

    @classmethod
    def connect(cls):
        """ Connects to the database. """

        cls.__conn = sqlite3.connect('database.db')
        cls.__cursor = cls.__conn.cursor()

    @classmethod
    def create_tables(cls):
        """ Creates the database tables if they don't exist already. """

        with open('create_tables.sql', 'r') as file:
            cls.__cursor.executescript(file.read())
            cls.__conn.commit()

    @classmethod
    def insert_user(cls, username, password):
        """ Inserts a user into the users table. """

        cls.__cursor.execute("""INSERT INTO users VALUES (:username, :password);""",
                             {'username': username, 'password': password})
        cls.__conn.commit()

    @classmethod
    def update_user(cls, old_username, new_username, new_password):
        """ Updates a user's fields in the users table. """

        cls.__cursor.execute("""UPDATE users SET username = :new_username, password = :password
                                    WHERE username = :old_username;""",
                             {'new_username': new_username, 'password': new_password, 'old_username': old_username})
        cls.__conn.commit()

    @classmethod
    def delete_user(cls):
        # TODO
        pass

    @classmethod
    def select_user(cls, username):
        """ Selects a user from the users table based on the username field. """

        cls.__cursor.execute("""SELECT * FROM users WHERE username = :username;""",
                             {'username': username})
        return cls.__cursor.fetchone()

    @classmethod
    def insert_account(cls, account_type, username, email, password, user):
        """ Inserts an account into the accounts table. """

        cls.__cursor.execute("""INSERT INTO accounts (account_type, username, email, password, user)
                                    VALUES (:account_type, :username, :email, :password, :user);""",
                             {'account_type': account_type, 'username': username, 'email': email, 'password': password, 'user': user})
        cls.__conn.commit()

    @classmethod
    def update_account_by_id(cls, id, account_type, username, email, password):
        """ Updates an account's fields in the accounts table based on the id field. """

        cls.__cursor.execute(""" UPDATE accounts SET account_type = :account_type,
                                    username = :username, email = :email, password = :password
                                    WHERE id = :id;""",
                             {'id': id, 'account_type': account_type, 'username': username, 'email': email, 'password': password})
        cls.__conn.commit()

    @classmethod
    def update_accounts_user_field(cls, new_username, old_username):
        """ Updates the user field in the accounts of the user that is logged in. """

        cls.__cursor.execute("""UPDATE accounts SET user = : new_username
                                    WHERE user =: old_username; """,
                             {'new_username': new_username, 'old_username': old_username})
        cls.__conn.commit()

    @classmethod
    def delete_account_by_id(cls, id):
        """ Deletes an account from the accounts table based on the id field. """

        cls.__cursor.execute("""DELETE FROM accounts WHERE id =: id; """,
                             {'id': id})
        cls.__conn.commit()

    @classmethod
    def select_account_by_id(cls, id):
        """ Selects an account's account_type, username, email and password fields
        from the accounts table based on the id field. """

        cls.__cursor.execute("""SELECT account_type, username, email, password FROM accounts
                                    WHERE id =: id; """,
                             {'id': id})
        return cls.__cursor.fetchone()

    @classmethod
    def select_accounts_by_user(cls, user):
        """ Selects accounts from the accounts table based on the user field. """

        cls.__cursor.execute("""SELECT * FROM accounts WHERE user = : user; """,
                             {'user': user})
        return cls.__cursor.fetchall()

    @classmethod
    def select_account_password_by_id(cls, id):
        """ Selects the password field of an account based on the id field. """

        cls.__cursor.execute(""" SELECT password FROM accounts WHERE id = : id;""",
                             {'id': id})
        return cls.__cursor.fetchone()

    @classmethod
    def close(cls):
        """ Closes the database connection. """

        cls.__conn.close()

# End of Database class.


if __name__ == '__main__':
    pass
