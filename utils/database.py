import sqlite3
import os
import json
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'kelnic.db')
        
        self.db_path = db_path
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def init_db(self):
        """Initialize database tables"""
        self.connect()
        
        # Users table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                items TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'completed',
                transaction_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Course access table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS course_access (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id TEXT NOT NULL,
                granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def create_user(self, name, email, password):
        """Create a new user"""
        # In a real implementation, you would hash the password
        password_hash = password  # This should be hashed in production
        
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user(self, user_id):
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, email, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, email, created_at FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def check_password(self, user_id, password):
        """Check if password is correct"""
        # In a real implementation, you would hash the password and compare
        cursor = self.conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return user['password_hash'] == password  # This should compare hashes in production
        
        return False
    
    def create_order(self, user_id, items, amount, transaction_id):
        """Create a new order"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO orders (user_id, items, amount, transaction_id) VALUES (?, ?, ?, ?)',
            (user_id, json.dumps(items), amount, transaction_id)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        orders = cursor.fetchall()
        return [dict(order) for order in orders]
    
    def grant_course_access(self, user_id, course_id):
        """Grant course access to a user"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO course_access (user_id, course_id) VALUES (?, ?)',
            (user_id, course_id)
        )
        self.conn.commit()
    
    def has_course_access(self, user_id, course_id):
        """Check if user has access to a course"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id FROM course_access WHERE user_id = ? AND course_id = ?',
            (user_id, course_id)
        )
        access = cursor.fetchone()
        return access is not None
    
    def get_user_courses(self, user_id):
        """Get all courses a user has access to"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT course_id, granted_at FROM course_access WHERE user_id = ?',
            (user_id,)
        )
        courses = cursor.fetchall()
        return [dict(course) for course in courses]

# Initialize database
def init_db():
    db = Database()
    db.init_db()
    db.close()

if __name__ == '__main__':
    init_db()
