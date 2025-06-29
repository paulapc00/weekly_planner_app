"""
styles.py

Contains Qt Style Sheet (QSS) for the minimalist weekly planner application.
This QSS is similar to CSS and allows for comprehensive styling of PyQt6 widgets.
"""

def get_minimalist_stylesheet():
    """
    Returns a QSS string for a minimalist theme.
    """
    return """
    QWidget {
        background-color: #f9f9f9; /* Very light grey background */
        font-family: "Inter", sans-serif; /* Modern, clean font. Will fallback if not available. */
        color: #333333; /* Dark grey text for readability */
        font-size: 14px;
    }

    QMainWindow {
        border-radius: 10px; /* Rounded corners for the main window */
    }

    /* Header for month/year navigation */
    #headerWidget {
        background-color: #ffffff; /* White background for header */
        border-bottom: 1px solid #eeeeee; /* Subtle separator */
        padding: 10px;
        border-top-left-radius: 8px; /* Match main window rounded corners */
        border-top-right-radius: 8px;
    }

    QLabel#monthYearLabel {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50; /* Darker blue-grey for emphasis */
        padding: 5px;
    }

    /* Navigation buttons */
    QPushButton {
        background-color: #4CAF50; /* Green for action buttons */
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px; /* Rounded buttons */
        font-weight: 500;
        outline: none; /* Remove focus outline */
    }

    QPushButton:hover {
        background-color: #45a049; /* Slightly darker green on hover */
    }

    QPushButton:pressed {
        background-color: #3e8e41; /* Even darker when pressed */
    }

    /* Specific styles for navigation buttons */
    QPushButton#navButton {
        background-color: #007bff; /* Blue for navigation */
        padding: 6px 12px;
    }

    QPushButton#navButton:hover {
        background-color: #0056b3;
    }

    /* Main week grid area */
    #weekGridWidget {
        background-color: #fcfcfc; /* Slightly different background for the grid */
        border-radius: 8px;
        margin: 10px;
        padding: 10px;
    }

    /* Day Column Headers (Mon, Tue, etc.) */
    QLabel.dayHeader {
        font-size: 15px;
        font-weight: bold;
        color: #555555; /* Medium grey */
        padding: 8px;
        text-align: center; /* Center text */
        border-bottom: 1px solid #dddddd; /* Separator for day headers */
    }

    /* Individual Day Cells */
    QFrame.dayCell {
        background-color: #ffffff; /* White background for each day */
        border: 1px solid #eeeeee; /* Light border */
        border-radius: 6px;
        padding: 10px;
        margin: 5px; /* Spacing between day cells */
        min-height: 150px; /* Minimum height for day cells */
        vertical-align: top;
    }

    /* Current Day Highlighting */
    QFrame#currentDayCell {
        background-color: #e0f2f7; /* Light blue for current day */
        border: 1px solid #a7d9ee;
    }

    QLabel.dayDate {
        font-size: 16px;
        font-weight: bold;
        color: #4CAF50; /* Green for dates */
        margin-bottom: 5px;
    }

    /* Task input field */
    QLineEdit {
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 6px;
        background-color: #ffffff;
        selection-background-color: #a7d9ee;
    }

    /* Add Task button inside day cells */
    QPushButton#addTaskButton {
        background-color: #2196F3; /* Blue for add task */
        padding: 5px 10px;
        font-size: 12px;
        margin-top: 5px;
    }

    QPushButton#addTaskButton:hover {
        background-color: #0b7dda;
    }

    /* Task display */
    QCheckBox {
        color: #333333;
        padding: 3px 0;
    }

    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border-radius: 3px;
        border: 1px solid #bbbbbb;
        background-color: #ffffff;
    }

    QCheckBox::indicator:checked {
        background-color: #4CAF50; /* Green when checked */
        border: 1px solid #4CAF50;
    }

    QCheckBox::indicator:checked:hover {
        background-color: #45a049;
    }

    /* Task text when completed */
    QCheckBox:checked {
        color: #888888; /* Lighter grey for completed tasks */
        text-decoration: line-through; /* Strikethrough for completed tasks */
    }

    /* Task actions (edit/delete) */
    QPushButton.taskActionButton {
        background-color: transparent;
        border: none;
        padding: 0 5px;
        min-width: 20px; /* Smaller size for action buttons */
        min-height: 20px;
        color: #777777; /* Grey icon color */
        font-size: 16px;
    }

    QPushButton.taskActionButton:hover {
        color: #333333; /* Darker on hover */
    }

    QPushButton#deleteTaskButton {
        color: #f44336; /* Red for delete button */
    }

    QPushButton#deleteTaskButton:hover {
        color: #d32f2f;
    }

    QPushButton#editTaskButton {
        color: #2196F3; /* Blue for edit button */
    }

    QPushButton#editTaskButton:hover {
        color: #0b7dda;
    }

    /* General QLabel styling within cells */
    QLabel {
        color: #444444;
    }
    """