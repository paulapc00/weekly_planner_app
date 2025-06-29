import os
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QPushButton, QLabel, QLineEdit, QCheckBox,
    QScrollArea, QMessageBox, QDialog, QDialogButtonBox,
    QSizePolicy, QFrame, QFileDialog, QTimeEdit, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QDate, QTime, QUrl
from PyQt6.QtGui import QFont, QIcon, QDesktopServices # QDesktopServices for opening files

import calendar
from datetime import datetime, timedelta

from data_manager import DataManager

# --- Task Dialog Class ---
class TaskDialog(QDialog):
    """
    A dialog for adding or editing task details, including Name, Description,
    Time, Location, and an optional file attachment.
    """
    def __init__(self, task_data=None, parent=None):
        """
        Initializes the TaskDialog.
        :param task_data: Dictionary containing existing task data for editing, or None for new task.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Task")
        self.setGeometry(200, 200, 400, 350) # Set a reasonable default size
        self.data_manager = parent.data_manager # Access data_manager from parent (WeeklyPlannerApp)

        self.original_file_path = "" # To keep track of the original file path during editing

        layout = QVBoxLayout(self)
        layout.setSpacing(10) # Add some spacing between form elements

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Task Name (e.g., 'Meeting', 'Groceries')")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Description
        description_layout = QHBoxLayout()
        description_layout.addWidget(QLabel("Description:"))
        self.description_input = QPlainTextEdit() # Use QPlainTextEdit for multi-line description
        self.description_input.setPlaceholderText("Detailed description (optional)")
        self.description_input.setMinimumHeight(60) # Give it some height
        description_layout.addWidget(self.description_input)
        layout.addLayout(description_layout) # Use addLayout for QHBoxLayout wrapped in a QVBoxLayout

        # Time
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Time:"))
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm") # 24-hour format
        self.time_input.setTime(QTime(datetime.now().hour, datetime.now().minute)) # Default to current time
        self.time_input.setToolTip("Optional: Time for the task")
        time_layout.addWidget(self.time_input)
        time_layout.addStretch() # Push to left
        layout.addLayout(time_layout)

        # Location
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Location:"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location (optional)")
        location_layout.addWidget(self.location_input)
        layout.addLayout(location_layout)

        # File Upload
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Attachment:"))
        self.file_path_label = QLabel("No file selected.")
        self.file_path_label.setWordWrap(True)
        file_layout.addWidget(self.file_path_label)
        self_file_upload_button = QPushButton("Browse...")
        self_file_upload_button.clicked.connect(self._select_file)
        file_layout.addWidget(self_file_upload_button)
        layout.addLayout(file_layout)

        # Button Box (OK/Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self._load_task_data(task_data) # Load data if in edit mode

    def _load_task_data(self, task_data):
        """Loads existing task data into the form fields if provided."""
        if task_data:
            self.setWindowTitle("Edit Task")
            self.name_input.setText(task_data.get('name', ''))
            self.description_input.setPlainText(task_data.get('description', ''))
            
            # Load time if available
            task_time_str = task_data.get('time', '')
            if task_time_str:
                try:
                    task_time = QTime.fromString(task_time_str, "HH:mm")
                    if task_time.isValid():
                        self.time_input.setTime(task_time)
                except ValueError:
                    pass # If format is wrong, leave default time

            self.location_input.setText(task_data.get('location', ''))
            self.original_file_path = task_data.get('file_path', '')
            if self.original_file_path:
                self.file_path_label.setText(os.path.basename(self.original_file_path))
            else:
                self.file_path_label.setText("No file selected.")


    def _select_file(self):
        """Opens a file dialog for the user to select a file."""
        # QFileDialog.getOpenFileName returns (filePath, filter), we only need filePath
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Images (*.png *.jpg *.jpeg *.gif);;Documents (*.pdf *.docx *.txt)")
        if file_path:
            self.file_path_label.setText(os.path.basename(file_path)) # Display only filename in UI
            self.file_to_upload_path = file_path # Store original path for upload later
        else:
            self.file_path_label.setText("No file selected.")
            self.file_to_upload_path = "" # Clear path if no file selected

    def get_task_data(self):
        """
        Returns a dictionary of task data entered in the dialog.
        Handles file upload if a new file was selected.
        """
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        time_str = self.time_input.time().toString("HH:mm")
        location = self.location_input.text().strip()

        file_path = self.original_file_path # Default to original path

        # If a new file was selected via browse, upload it
        if hasattr(self, 'file_to_upload_path') and self.file_to_upload_path:
            # We don't have task_id here for new tasks, will update once task is added
            # For editing, we already have task_id, so pass it.
            # This logic needs adjustment. For simplicity, we'll handle actual DB update
            # and file path storage in _add_task_to_day or _edit_task after the dialog closes.
            file_path = self.file_to_upload_path # Temporarily store the source path
            # The actual file copy will happen *after* task is added/updated in DB
            # This is because we might need the task_id for unique filenames.

        return {
            'name': name,
            'description': description,
            'time': time_str,
            'location': location,
            'file_path': file_path # This will be the source path initially for new files
        }


# --- Main Application Class ---
class WeeklyPlannerApp(QMainWindow):
    """
    The main window for the Minimalist Weekly Planner application.
    Manages the UI, week navigation, and task display/management.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimalist Weekly Planner")
        self.setGeometry(100, 100, 1000, 700)

        self.data_manager = DataManager('planner.db')

        self.current_date = QDate.currentDate()

        self._setup_ui()
        self._update_week_display()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)

        self.prev_week_button = QPushButton("Previous Week")
        self.prev_week_button.setObjectName("navButton")
        self.prev_week_button.clicked.connect(self._go_to_previous_week)
        header_layout.addWidget(self.prev_week_button)

        header_layout.addStretch(1)

        self.month_year_label = QLabel()
        self.month_year_label.setObjectName("monthYearLabel")
        self.month_year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.month_year_label)

        header_layout.addStretch(1)

        self.next_week_button = QPushButton("Next Week")
        self.next_week_button.setObjectName("navButton")
        self.next_week_button.clicked.connect(self._go_to_next_week)
        header_layout.addWidget(self.next_week_button)

        main_layout.addWidget(header_widget)

        self.week_grid_scroll_area = QScrollArea()
        self.week_grid_scroll_area.setWidgetResizable(True)
        self.week_grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.week_grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.week_grid_widget = QWidget()
        self.week_grid_widget.setObjectName("weekGridWidget")
        self.week_grid_layout = QGridLayout(self.week_grid_widget)
        self.week_grid_layout.setSpacing(10)
        self.week_grid_layout.setContentsMargins(15, 15, 15, 15)

        self.week_grid_scroll_area.setWidget(self.week_grid_widget)
        main_layout.addWidget(self.week_grid_scroll_area)

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, name in enumerate(day_names):
            day_header_label = QLabel(name)
            day_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_header_label.setProperty("class", "dayHeader")
            self.week_grid_layout.addWidget(day_header_label, 0, i)

    def _update_week_display(self):
        """
        Updates the displayed week based on `self.current_date`.
        Calculates the week's dates, fetches tasks, and populates the grid.
        """
        for i in reversed(range(self.week_grid_layout.count())):
            item = self.week_grid_layout.itemAt(i)
            if item is None:
                continue

            row, _, _, _ = self.week_grid_layout.getItemPosition(i)

            if row > 0:
                widget = item.widget()
                if widget:
                    self.week_grid_layout.removeWidget(widget)
                    widget.deleteLater()

        start_of_week = self.current_date.addDays(-self.current_date.dayOfWeek() + 1)
        end_of_week = start_of_week.addDays(6)

        month_format = "MMMM yyyy"
        if start_of_week.month() == end_of_week.month():
            self.month_year_label.setText(start_of_week.toString(month_format))
        else:
            self.month_year_label.setText(
                f"{start_of_week.toString('MMM yyyy')} - {end_of_week.toString(month_format)}"
            )

        tasks_in_week = self.data_manager.get_tasks_for_week(
            start_of_week.toString("yyyy-MM-dd"),
            end_of_week.toString("yyyy-MM-dd")
        )
        
        # --- SCHEDULE FEATURE (PLACEHOLDER - to be added in Phase 3) ---
        # For now, we'll assume there's no visible schedule data.
        # This will be fetched and displayed here in the next iteration.

        for i in range(7):
            day_date = start_of_week.addDays(i)
            day_date_str = day_date.toString("yyyy-MM-dd")

            day_cell_frame = QFrame()
            day_cell_frame.setProperty("class", "dayCell")
            day_cell_layout = QVBoxLayout(day_cell_frame)
            day_cell_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            day_cell_layout.setContentsMargins(5, 5, 5, 5)

            if day_date == QDate.currentDate():
                day_cell_frame.setObjectName("currentDayCell")

            date_label = QLabel(day_date.toString("ddd, MMM dd"))
            date_label.setProperty("class", "dayDate")
            day_cell_layout.addWidget(date_label)

            # --- Task List for the Day ---
            tasks_list_widget = QWidget()
            tasks_list_layout = QVBoxLayout(tasks_list_widget)
            tasks_list_layout.setContentsMargins(0,0,0,0)
            tasks_list_layout.setSpacing(5) # Increased spacing for better readability of new fields

            tasks_for_this_day = tasks_in_week.get(day_date_str, [])
            for task_data in tasks_for_this_day:
                self._add_task_widget(tasks_list_layout, task_data)

            day_cell_layout.addWidget(tasks_list_widget)

            # --- Add Task Button (opens dialog) ---
            add_task_button = QPushButton("Add New Task")
            add_task_button.setObjectName("addTaskButton")
            # Pass the date string to the add task method
            add_task_button.clicked.connect(lambda _, date=day_date_str:
                                            self._open_add_task_dialog(date))
            day_cell_layout.addWidget(add_task_button) # Add button directly, no separate input field

            day_cell_layout.addStretch(1) # Pushes content to top

            self.week_grid_layout.addWidget(day_cell_frame, 1, i)
            self.week_grid_layout.setColumnStretch(i, 1)

    def _add_task_widget(self, parent_layout, task_data):
        """
        Creates and adds a QWidget representing a single task to the given parent_layout.
        Now displays Name, Description, Time, Location, and a link for file_path.
        """
        task_id = task_data['id']
        name = task_data['name']
        description = task_data['description']
        time = task_data['time']
        location = task_data['location']
        file_path = task_data['file_path']
        is_completed = task_data['is_completed']

        task_widget = QWidget()
        task_layout = QVBoxLayout(task_widget) # Use QVBoxLayout for task content
        task_layout.setContentsMargins(0, 0, 0, 0)
        task_layout.setSpacing(2) # Tight spacing within a single task entry

        # Top row: Checkbox, Name, Time, Action Buttons
        top_row_layout = QHBoxLayout()
        checkbox = QCheckBox()
        checkbox.setChecked(is_completed)
        checkbox.stateChanged.connect(lambda state, id=task_id:
                                      self._toggle_task_completion(id, state == Qt.CheckState.Checked))
        top_row_layout.addWidget(checkbox)

        # Task Name Label (primary identifier, bold)
        name_label = QLabel(name)
        name_label.setProperty("class", "taskName")
        if is_completed:
            name_label.setProperty("taskCompleted", "true")
        else:
            name_label.setProperty("taskCompleted", "false")
        name_label.setWordWrap(True)
        top_row_layout.addWidget(name_label)

        # Time label (if provided)
        if time:
            time_label = QLabel(f"<span class='taskTime'>{time}</span>")
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            top_row_layout.addWidget(time_label)

        top_row_layout.addStretch(1) # Pushes name/time to left, buttons to right

        # Edit Button
        edit_button = QPushButton("✏️")
        edit_button.setProperty("class", "taskActionButton")
        edit_button.setObjectName("editTaskButton")
        edit_button.setToolTip("Edit task")
        edit_button.clicked.connect(lambda _, id=task_id:
                                    self._open_edit_task_dialog(id, task_data)) # Pass full task_data
        top_row_layout.addWidget(edit_button)

        # Delete Button
        delete_button = QPushButton("❌")
        delete_button.setProperty("class", "taskActionButton")
        delete_button.setObjectName("deleteTaskButton")
        delete_button.setToolTip("Delete task")
        delete_button.clicked.connect(lambda _, id=task_id:
                                      self._delete_task(id))
        top_row_layout.addWidget(delete_button)

        task_layout.addLayout(top_row_layout)

        # Description Label (if provided)
        if description:
            desc_label = QLabel(description)
            desc_label.setProperty("class", "taskDescription")
            if is_completed:
                desc_label.setProperty("taskCompleted", "true")
            else:
                desc_label.setProperty("taskCompleted", "false")
            desc_label.setWordWrap(True)
            task_layout.addWidget(desc_label)

        # Location Label (if provided)
        if location:
            loc_label = QLabel(f"Location: <span class='taskLocation'>{location}</span>")
            loc_label.setProperty("class", "taskInfo")
            if is_completed: # Apply completion style to location too
                loc_label.setProperty("taskCompleted", "true")
            else:
                loc_label.setProperty("taskCompleted", "false")
            task_layout.addWidget(loc_label)

        # File Link (if provided)
        if file_path:
            file_name = os.path.basename(file_path)
            file_link = QLabel(f"File: <a href='{file_path}'><span class='taskFileLink'>{file_name}</span></a>")
            file_link.setOpenExternalLinks(False) # Important: handle opening via function
            file_link.linkActivated.connect(lambda url, path=file_path: self._open_file(path))
            file_link.setProperty("class", "taskInfo")
            if is_completed: # Apply completion style
                file_link.setProperty("taskCompleted", "true")
            else:
                file_link.setProperty("taskCompleted", "false")
            task_layout.addWidget(file_link)


        task_widget.setProperty("class", "individualTask") # For styling border/background of each task
        parent_layout.addWidget(task_widget)

    def _open_file(self, file_path):
        """Attempts to open the given file path using the system's default application."""
        if os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        else:
            QMessageBox.warning(self, "File Not Found", f"The file '{os.path.basename(file_path)}' could not be found at '{file_path}'. It might have been moved or deleted.")


    def _open_add_task_dialog(self, date_str):
        """
        Opens the TaskDialog for adding a new task.
        """
        dialog = TaskDialog(parent=self) # Pass self as parent to access data_manager
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_data = dialog.get_task_data()
            name = task_data['name']
            description = task_data['description']
            time = task_data['time']
            location = task_data['location']
            source_file_path = task_data['file_path'] # This is the source path from dialog

            if not name:
                QMessageBox.warning(self, "Input Error", "Task Name cannot be empty.")
                return

            uploaded_file_path = ""
            if source_file_path:
                # Upload the file first to get the final path in the uploads directory
                uploaded_file_path = self.data_manager.upload_file(source_file_path)

            # Add task to the database with all details and the *final* uploaded file path
            task_id = self.data_manager.add_task(date_str, name, description, time, location, uploaded_file_path)
            if task_id is not None:
                # If a file was uploaded, update its name to include the task_id for uniqueness.
                # This requires a rename if the file was copied before the task_id was known.
                # A simpler approach: if upload_file handled task_id based naming initially, we're good.
                # The current upload_file *can* use task_id if passed.
                # Let's re-upload with task_id if a file was selected.
                if source_file_path:
                    final_uploaded_path = self.data_manager.upload_file(source_file_path, task_id=task_id)
                    if final_uploaded_path != uploaded_file_path: # If filename changed due to task_id
                        self.data_manager.update_task(task_id, name, description, time, location, final_uploaded_path)
                        QMessageBox.information(self, "File Upload", f"File saved as: {os.path.basename(final_uploaded_path)}")
                self._update_week_display() # Refresh UI
            else:
                QMessageBox.critical(self, "Database Error", "Failed to add task to database.")

    def _open_edit_task_dialog(self, task_id, current_task_data):
        """
        Opens the TaskDialog for editing an existing task.
        """
        dialog = TaskDialog(task_data=current_task_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_task_data()
            name = updated_data['name']
            description = updated_data['description']
            time = updated_data['time']
            location = updated_data['location']
            source_file_path = updated_data['file_path'] # This is the source path or original DB path

            if not name:
                QMessageBox.warning(self, "Input Error", "Task Name cannot be empty.")
                return

            final_file_path = current_task_data['file_path'] # Start with existing path

            # Check if a *new* file was selected for upload or if existing was cleared
            # This logic needs to be careful:
            # 1. User selected a new file -> upload it, update DB path
            # 2. User cleared an existing file path -> update DB path to empty
            # 3. User kept original file path -> do nothing
            if hasattr(dialog, 'file_to_upload_path') and dialog.file_to_upload_path:
                # A new file was selected in the dialog
                uploaded_path = self.data_manager.upload_file(dialog.file_to_upload_path, task_id=task_id)
                final_file_path = uploaded_path
            elif dialog.file_path_label.text() == "No file selected." and current_task_data['file_path']:
                # User explicitly cleared the file
                final_file_path = "" # Clear the path in DB

            # Update the task in the database
            self.data_manager.update_task(task_id, name, description, time, location, final_file_path)
            self._update_week_display() # Refresh UI

    def _toggle_task_completion(self, task_id, is_completed):
        """
        Toggles the completion status of a task in the database and updates the UI.
        """
        self.data_manager.update_task_status(task_id, is_completed)
        self._update_week_display()

    def _delete_task(self, task_id):
        """
        Deletes a task from the database after user confirmation.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Deletion")
        msg_box.setText("Are you sure you want to delete this task?")
        msg_box.setIcon(QMessageBox.Icon.Warning)

        yes_button = msg_box.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)

        msg_box.setDefaultButton(no_button)
        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            # Optionally, you might want to delete the associated file from the 'uploads' directory here
            # For now, we only delete the DB entry.
            self.data_manager.delete_task(task_id)
            self._update_week_display()

    def _go_to_previous_week(self):
        """Moves the planner view to the previous week."""
        self.current_date = self.current_date.addDays(-7)
        self._update_week_display()

    def _go_to_next_week(self):
        """Moves the planner view to the next week."""
        self.current_date = self.current_date.addDays(7)
        self._update_week_display()

    def closeEvent(self, event):
        """
        Handles the window close event to ensure the database connection is closed.
        """
        self.data_manager.close()
        event.accept()