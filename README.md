# Minimalist Weekly Planner

A simple, minimalist weekly planner application built with PyQt6 and SQLite. This application helps users organize their week by managing tasks with enhanced details and providing a clean, intuitive interface.

## Features

* **Weekly View:** Navigate easily between weeks.
* **Task Management:**
    * Add new tasks for specific days.
    * Mark tasks as completed.
    * Edit existing tasks.
    * Delete tasks.
* **Enhanced Task Details (NEW!):**
    * **Name:** A concise title for your task (e.g., "Team Meeting", "Grocery Shopping").
    * **Description:** Detailed notes or information about the task (multi-line support).
    * **Time (Optional):** Specify a time for your task (e.g., "09:30").
    * **Location (Optional):** Add a location for the task (e.g., "Office", "Supermarket").
    * **File/Image Attachment (Optional):** Attach relevant files or images directly to a task. Click the file name to open it with your system's default application.
* **Persistent Data:** All tasks are saved to a local SQLite database (`planner.db`), so your data is preserved between sessions.

## Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <repository_url_here>
    cd weekly_planner_app
    ```
    (Replace `<repository_url_here>` with the actual URL if you're using Git).

2.  **Create a Python Virtual Environment (recommended):**
    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    * **On macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    * **On Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    * **On Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    ```bash
    pip install PyQt6
    ```

## Usage

1.  **Ensure your virtual environment is activated.**

2.  **Run the application:**
    ```bash
    python main.py
    ```

3.  **Navigating Weeks:** Use the "Previous Week" and "Next Week" buttons at the top to change the displayed week.

4.  **Adding a New Task:**
    * Click the "Add New Task" button located at the bottom of each day's column.
    * A dialog will appear where you can enter:
        * **Name:** (Required) A short title for your task.
        * **Description:** (Optional) More details about the task.
        * **Time:** (Optional) A specific time.
        * **Location:** (Optional) Where the task takes place.
        * **Attachment:** Click "Browse..." to select a file or image from your computer to attach.
    * Click "OK" to save the task.

5.  **Editing a Task:**
    * Click the "✏️" (pencil) icon next to an existing task.
    * The "Add/Edit Task" dialog will open, pre-filled with the task's current details.
    * Make your changes and click "OK" to update.

6.  **Marking Tasks Complete:**
    * Click the checkbox next to a task to toggle its completion status. Completed tasks will have their text visually styled (e.g., strikethrough).

7.  **Deleting a Task:**
    * Click the "❌" (cross) icon next to a task.
    * Confirm your decision in the pop-up message box.

8.  **Opening Attached Files:**
    * If a task has an attached file, a link with the filename will appear below its description.
    * Click this link to open the file using your operating system's default application.

## Project Structure

* `main.py`: The entry point of the application.
* `ui_planner.py`: Contains the `WeeklyPlannerApp` UI definition and logic.
* `data_manager.py`: Handles all interactions with the SQLite database.
* `styles.py`: (Optional, if you add one) Contains QSS (Qt Style Sheet) for styling the application's appearance.
* `planner.db`: The SQLite database file (created automatically on first run).
* `uploads/`: Directory where attached files will be copied (created automatically).

## Future Enhancements (Planned)

* **Recurring Schedule/Events:** Ability to define fixed working hours, class schedules, or recurring meetings that appear automatically each week.
* More advanced file management (e.g., delete attached files when tasks are deleted).
* Search and filter functionality for tasks.
* Customizable themes and appearance.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

[MIT License]
