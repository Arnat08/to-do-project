import sqlite3


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = 'db.sqlite3'
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    @staticmethod
    def all():
        db = 'db.sqlite3'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        result = []
        query = cursor.execute("SELECT * FROM users")
        for data in query.fetchall():
            result.append({
                'id': data[0],
                'username': data[1]
            })
        return result

    @staticmethod
    def get_user_by_id(id):
        db = 'db.sqlite3'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        query = cursor.execute("SELECT id, username FROM users WHERE id = ?", (id, ))
        data = query.fetchone()
        return {
            'id': data[0],
            'username': data[1]
        }

    @staticmethod
    def update_user_by_id(id, username):
        db = 'db.sqlite3'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, id))
        connection.commit()
        return {
            'id': id,
            'username': username
        }


    @staticmethod
    def delete_user_by_id(id):
        db = 'db.sqlite3'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ? ", (id, ))
        connection.commit()
        return 'user deleted'

    def get_all_users(self):
        result = []
        query = self.cursor.execute("SELECT * FROM users")
        for data in query.fetchall():
            result.append({
                'id': data[0],
                'username': data[1]
            })
        return result

    def register_user(self):
        self.cursor.execute(
            '''
                INSERT INTO users(username, password) VALUES (?, ?)
            ''', (self.username, self.password)
        )
        self.connection.commit()

    def get_user(self):
        result = {}
        query = self.cursor.execute('''
            SELECT * FROM users WHERE username = ?
        ''', (self.username,))
        data = query.fetchone()
        result['username'] = data[1]
        result['password'] = data[2]

        return result
