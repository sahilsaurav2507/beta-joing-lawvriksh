import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteDatabaseConnection:
    def __init__(self, db_path: str = "lawviksh.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            # Create database directory if it doesn't exist
            db_file = Path(self.db_path)
            db_file.parent.mkdir(parents=True, exist_ok=True)
            
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            self.cursor = self.connection.cursor()
            
            # Create tables if they don't exist
            self.create_tables()
            
            logger.info("SQLite database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Error connecting to SQLite: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("SQLite database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return [dict(row) for row in self.cursor.fetchall()]
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise e
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute multiple queries with different parameters"""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing multiple queries: {e}")
            raise e
    
    def create_tables(self):
        """Create all required tables"""
        try:
            # Users table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone_number TEXT NOT NULL,
                    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other', 'Prefer not to say')),
                    profession TEXT CHECK(profession IN ('Student', 'Lawyer', 'Other')),
                    interest_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Not interested users table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS not_interested_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    not_interested_reason TEXT CHECK(not_interested_reason IN ('Too complex', 'Not relevant', 'Other')),
                    improvement_suggestions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Feedback forms table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS feedback_forms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # UI ratings table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS ui_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_form_id INTEGER NOT NULL,
                    visual_design_rating INTEGER CHECK(visual_design_rating BETWEEN 1 AND 5),
                    visual_design_comments TEXT,
                    ease_of_navigation_rating INTEGER CHECK(ease_of_navigation_rating BETWEEN 1 AND 5),
                    ease_of_navigation_comments TEXT,
                    mobile_responsiveness_rating INTEGER CHECK(mobile_responsiveness_rating BETWEEN 1 AND 5),
                    mobile_responsiveness_comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE
                )
            """)
            
            # UX ratings table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS ux_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_form_id INTEGER NOT NULL,
                    overall_satisfaction_rating INTEGER CHECK(overall_satisfaction_rating BETWEEN 1 AND 5),
                    overall_satisfaction_comments TEXT,
                    task_completion_rating INTEGER CHECK(task_completion_rating BETWEEN 1 AND 5),
                    task_completion_comments TEXT,
                    service_quality_rating INTEGER CHECK(service_quality_rating BETWEEN 1 AND 5),
                    service_quality_comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE
                )
            """)
            
            # Suggestions and needs table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS suggestions_and_needs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_form_id INTEGER NOT NULL,
                    liked_features TEXT,
                    improvement_suggestions TEXT,
                    desired_features TEXT,
                    legal_challenges TEXT,
                    additional_feedback TEXT,
                    follow_up_consent TEXT CHECK(follow_up_consent IN ('yes', 'no')) DEFAULT 'no',
                    follow_up_email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE
                )
            """)
            
            # Form submissions log table
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS form_submissions_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_type TEXT CHECK(form_type IN ('join_as_user', 'not_interested', 'feedback')) NOT NULL,
                    user_ip TEXT,
                    user_agent TEXT,
                    submission_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("All tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise e

# Global database instance
db = SQLiteDatabaseConnection() 