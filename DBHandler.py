import sqlite3
from datetime import datetime

class UserDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_key TEXT PRIMARY KEY,
                date_created TEXT,
                premium BOOLEAN,
                allocated_space INTEGER,
                last_modified TEXT
            )
        ''')
        self.connection.commit()

    def add_user(self, user_key, premium, allocated_space, last_modified):
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
        self.cursor.execute('''
            INSERT INTO users (user_key, date_created, premium, allocated_space, last_modified)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_key, date_created, premium, allocated_space, last_modified))
        self.connection.commit()

    def get_user(self, user_key):
        self.cursor.execute('SELECT * FROM users WHERE user_key = ?', (user_key,))
        return self.cursor.fetchone()
    
    def update_premium_status(self, user_key, new_premium_status, allocated_space):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
        self.cursor.execute('''
            UPDATE users SET premium = ?, allocated_space = ?, last_modified = ? WHERE user_key = ?
        ''', (new_premium_status, allocated_space, current_date, user_key))
        self.connection.commit()
        
        

    def update_allocated_space(self, user_key, new_allocated_space):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
        self.cursor.execute('''
            UPDATE users SET allocated_space = ?, last_modified = ? WHERE user_key = ?
        ''', (new_allocated_space, current_date, user_key))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

""" TESTCASE 1

user_db = UserDatabase("user_database.db")

# Add a new user
user_db.add_user("user1234", True, 1024, "2022-01-15")

# Retrieve the user information
retrieved_user = user_db.get_user("user123")
print("Retrieved User:", retrieved_user)

# Update the premium status and allocated space
user_db.update_premium_status("user123", False)
user_db.update_allocated_space("user123", 2048)

# Retrieve the updated user information
updated_user = user_db.get_user("user123")
print("Updated User:", updated_user)

# Close the database connection
user_db.close_connection()

"""