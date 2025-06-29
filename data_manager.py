from datetime import datetime
import sqlite3
import os # Import os for path manipulation

class DataManager:
    """
    Manages database interactions for the planner application.
    Handles tasks and, in the future, scheduled events.
    """
    def __init__(self, db_name='planner.db'):
        """
        Initializes the DataManager and connects to the SQLite database.
        Creates necessary tables if they don't exist.
        """
        self.db_name = db_name
        self.conn = None # Initialize connection to None
        self._connect() # Establish connection and create tables

        # Define a directory for uploaded files relative to the script
        self.upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(self.upload_dir, exist_ok=True) # Create the directory if it doesn't exist

    def _connect(self):
        """Establishes a connection to the database and creates tables."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
            self.cursor = self.conn.cursor()
            self._create_tables()
            print(f"Connected to database: {self.db_name}") #
            print("Table 'tasks' checked/created successfully.") #
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            # Handle error appropriately, e.g., exit or raise exception
            if self.conn:
                self.conn.close()
            self.conn = None # Set connection to None if failed

    def _create_tables(self):
        """
        Creates the 'tasks' table with new fields: name, time, location, file_path.
        Also creates the 'schedule' table for recurring events.
        """
        if self.conn is None:
            print("Cannot create tables: Database connection not established.")
            return

        # Tasks Table: Now includes 'name', 'time', 'location', 'file_path'
        # The 'name' is the main title, 'description' can be longer details.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                name TEXT NOT NULL,          -- New: Short name/title of the task
                description TEXT,            -- Existing: Detailed description
                time TEXT,                   -- New: Optional time (e.g., "09:00", "Morning")
                location TEXT,               -- New: Optional location
                file_path TEXT,              -- New: Path to an associated file/image
                is_completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')

        # Schedule Table: For recurring working hours or classes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week TEXT NOT NULL,   -- e.g., 'Monday', 'Tuesday'
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                type TEXT NOT NULL,          -- e.g., 'Work', 'Class', 'Meeting'
                description TEXT             -- Optional description for the schedule block
            )
        ''')
        self.conn.commit()

    def add_task(self, date, name, description="", time="", location="", file_path=""):
        """
        Adds a new task to the database with all new fields.
        Returns the ID of the new task or None on failure.
        """
        if self.conn is None: return None
        try:
            self.cursor.execute('''
                INSERT INTO tasks (date, name, description, time, location, file_path, is_completed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date, name, description, time, location, file_path, False))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            return None

    def get_tasks_for_week(self, start_date_str, end_date_str):
        """
        Retrieves all tasks within a specified date range.
        Returns a dictionary where keys are date strings and values are lists of task dicts.
        """
        if self.conn is None: return {}
        tasks_by_date = {}
        try:
            self.cursor.execute('''
                SELECT id, date, name, description, time, location, file_path, is_completed
                FROM tasks
                WHERE date BETWEEN ? AND ? ORDER BY date, time
            ''', (start_date_str, end_date_str))
            for row in self.cursor.fetchall():
                task_data = dict(row)
                tasks_by_date.setdefault(task_data['date'], []).append(task_data)
            return tasks_by_date
        except sqlite3.Error as e:
            print(f"Error getting tasks for week: {e}")
            return {}

    def update_task_status(self, task_id, is_completed):
        """Updates the completion status of a task."""
        if self.conn is None: return
        try:
            self.cursor.execute('''
                UPDATE tasks SET is_completed = ? WHERE id = ?
            ''', (is_completed, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating task status: {e}")

    def update_task(self, task_id, name, description, time, location, file_path):
        """
        Updates all fields of an existing task.
        """
        if self.conn is None: return
        try:
            self.cursor.execute('''
                UPDATE tasks SET name = ?, description = ?, time = ?, location = ?, file_path = ?
                WHERE id = ?
            ''', (name, description, time, location, file_path, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")

    def delete_task(self, task_id):
        """Deletes a task from the database."""
        if self.conn is None: return
        try:
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")

    def upload_file(self, source_path, task_id=None):
        """
        Copies a file to the upload directory and returns its new path.
        Optionally, renames the file to include task_id for uniqueness.
        """
        if not source_path or not os.path.exists(source_path):
            return ""

        filename = os.path.basename(source_path)
        # Create a unique filename, especially if associated with a task
        if task_id:
            base, ext = os.path.splitext(filename)
            unique_filename = f"{base}_{task_id}{ext}"
        else:
            # If no task_id, use a timestamp for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base, ext = os.path.splitext(filename)
            unique_filename = f"{base}_{timestamp}{ext}"

        destination_path = os.path.join(self.upload_dir, unique_filename)

        try:
            import shutil
            shutil.copy2(source_path, destination_path) # copy2 preserves metadata
            return destination_path
        except Exception as e:
            print(f"Error uploading file: {e}")
            return ""

    # --- Schedule Methods (Phase 3 - to be implemented fully later) ---
    def add_schedule_entry(self, day_of_week, start_time, end_time, entry_type, description=""):
        """Adds a new recurring schedule entry."""
        if self.conn is None: return None
        try:
            self.cursor.execute('''
                INSERT INTO schedule (day_of_week, start_time, end_time, type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (day_of_week, start_time, end_time, entry_type, description))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding schedule entry: {e}")
            return None

    def get_schedule_for_day(self, day_of_week):
        """Retrieves schedule entries for a specific day of the week."""
        if self.conn is None: return []
        try:
            self.cursor.execute('''
                SELECT id, day_of_week, start_time, end_time, type, description
                FROM schedule WHERE day_of_week = ? ORDER BY start_time
            ''', (day_of_week,))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error getting schedule: {e}")
            return []

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")