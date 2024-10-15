import sqlite3
from datetime import time, datetime, timedelta
import pytz
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_userold(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO 'reg' ('user_id', 'user_name') VALUES (?, ?)", (user_id, user_name))

    #HP func
    def add_user(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_name') VALUES (?, ?)", (user_id, user_name))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, user_name FROM users WHERE admin = 0").fetchall()
        
    def get_not_active_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, user_name FROM users WHERE active = 0 and admin = 0").fetchall()
        
    def get_admins(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, user_name FROM users WHERE admin = 1").fetchall()
    
    def get_admins_id(self):
        with self.connection:
            admins = self.cursor.execute("SELECT user_id FROM users WHERE admin = 1").fetchall()
            id = []
            for i in admins:
                id.append(i[0])
            return(id)


    def user_active(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT active FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(user[0])
        
    def user_tryed(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT tryed FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(user[0])

    def is_admin(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(user[0])
    
    def set_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET admin = 1 WHERE user_id = ?", (user_id,))
        
    def del_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET admin = 0 WHERE user_id = ?", (user_id,))

    def get_day(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT days FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        
    def set_active(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = 1 WHERE user_id = ?", (user_id,))
        
    def set_tryed(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET tryed = 1 WHERE user_id = ?", (user_id,))
        
    def delete_id(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    def day_count(self, user_id):
        with self.connection:
            day = self.cursor.execute("SELECT days FROM users WHERE user_id = ?", (user_id,)).fetchone()[0] + 1
            return self.cursor.execute("UPDATE users SET days = ? WHERE user_id = ?", (day, user_id))
