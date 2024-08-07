import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UserDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_connection(self):
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_key TEXT PRIMARY KEY,
                    date_created TEXT,
                    premium BOOLEAN,
                    allocated_space INTEGER,
                    used_space INTEGER DEFAULT 0,
                    last_modified TEXT,
                    api_key TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_key TEXT,
                    file_path TEXT,
                    file_size INTEGER,
                    upload_date TEXT,
                    FOREIGN KEY(user_key) REFERENCES users(user_key)
                )
            ''')
            connection.commit()
            logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            connection.close()

    def add_user(self, user_key, premium, allocated_space, last_modified, api_key):
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO users (user_key, date_created, premium, allocated_space, used_space, last_modified, api_key)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_key, date_created, premium, allocated_space, 0, last_modified, api_key))
            connection.commit()

            return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error adding user {user_key}: {e}")
            return False
        except sqlite3.OperationalError as e:
            logger.error(f"Operational error adding user {user_key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error adding user {user_key}: {e}")
            return False
        finally:
            connection.close()

    def get_user(self, user_key):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE user_key = ?', (user_key,))
            user = cursor.fetchone()
            if user:
                logger.info(f"Retrieved user {user_key}")
            else:
                logger.warning(f"User {user_key} not found")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user {user_key}: {e}")
            return None
        finally:
            connection.close()

    def get_user_by_api_key(self, api_key):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE api_key = ?', (api_key,))
            user = cursor.fetchone()
            if user:
                logger.info(f"Retrieved user with API key {api_key}")
            else:
                logger.warning(f"User with API key {api_key} not found")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with API key {api_key}: {e}")
            return None
        finally:
            connection.close()

    def update_used_space(self, user_key, new_used_space):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE users SET used_space = ?, last_modified = ? WHERE user_key = ?
            ''', (new_used_space, current_date, user_key))
            connection.commit()
            logger.info(
                f"Updated used space for user {user_key} to {new_used_space}")
        except Exception as e:
            logger.error(f"Error updating used space for user {user_key}: {e}")
        finally:
            connection.close()

    def update_premium_status(self, user_key, new_premium_status, allocated_space):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE users SET premium = ?, allocated_space = ?, last_modified = ? WHERE user_key = ?
            ''', (new_premium_status, allocated_space, current_date, user_key))
            connection.commit()
            logger.info(
                f"Updated premium status for user {user_key} to {new_premium_status}")
        except Exception as e:
            logger.error(
                f"Error updating premium status for user {user_key}: {e}")
        finally:
            connection.close()

    def update_allocated_space(self, user_key, new_allocated_space):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE users SET allocated_space = ?, last_modified = ? WHERE user_key = ?
            ''', (new_allocated_space, current_date, user_key))
            connection.commit()
            logger.info(
                f"Updated allocated space for user {user_key} to {new_allocated_space}")
        except Exception as e:
            logger.error(
                f"Error updating allocated space for user {user_key}: {e}")
        finally:
            connection.close()

    def add_user_file(self, user_key, file_path, file_size):
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO user_files (user_key, file_path, file_size, upload_date)
                VALUES (?, ?, ?, ?)
            ''', (user_key, file_path, file_size, upload_date))
            connection.commit()
            logger.info(f"Added file {file_path} for user {user_key}")
        except Exception as e:
            logger.error(
                f"Error adding file {file_path} for user {user_key}: {e}")
        finally:
            connection.close()

    def update_user_file(self, user_key, file_path, file_size):
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE user_files SET file_size = ?, upload_date = ? WHERE user_key = ? AND file_path = ?
            ''', (file_size, upload_date, user_key, file_path))
            connection.commit()
            logger.info(f"Updated file {file_path} for user {user_key}")
        except Exception as e:
            logger.error(
                f"Error updating file {file_path} for user {user_key}: {e}")
        finally:
            connection.close()

    def get_user_file(self, user_key, file_path):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM user_files WHERE user_key = ? AND file_path = ?', (user_key, file_path))
            file = cursor.fetchone()
            if file:
                logger.info(f"Retrieved file {file_path} for user {user_key}")
            else:
                logger.warning(
                    f"File {file_path} for user {user_key} not found")
            return file
        except Exception as e:
            logger.error(
                f"Error retrieving file {file_path} for user {user_key}: {e}")
            return None
        finally:
            connection.close()

    def get_user_files(self, user_key):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM user_files WHERE user_key = ?', (user_key,))
            files = cursor.fetchall()
            logger.info(f"Retrieved files for user {user_key}")
            return files
        except Exception as e:
            logger.error(f"Error retrieving files for user {user_key}: {e}")
            return []
        finally:
            connection.close()

    def get_total_used_space(self, user_key):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT SUM(file_size) FROM user_files WHERE user_key = ?', (user_key,))
            total_used_space = cursor.fetchone()[0] or 0
            logger.info(
                f"Total used space for user {user_key}: {total_used_space}")
            return total_used_space
        except Exception as e:
            logger.error(
                f"Error getting total used space for user {user_key}: {e}")
            return 0
        finally:
            connection.close()
