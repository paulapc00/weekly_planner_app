import sys
from PyQt6.QtWidgets import QApplication
from ui_planner import WeeklyPlannerApp
from styles import get_minimalist_stylesheet

if __name__ == "__main__":
    # 1. Create the QApplication instance. This is required for any PyQt GUI application.
    app = QApplication(sys.argv)

    # 2. Apply the minimalist stylesheet defined in styles.py.
    # This sets the visual theme for all widgets in the application.
    app.setStyleSheet(get_minimalist_stylesheet())

    # 3. Create an instance of our main application window.
    planner_app = WeeklyPlannerApp()

    # 4. Show the main window.
    planner_app.show()

    # 5. Start the application's event loop.
    # This keeps the application running and responsive to user interactions
    # until the window is closed. sys.exit() ensures a clean exit.
    sys.exit(app.exec())