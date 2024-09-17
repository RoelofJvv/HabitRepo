# Habit Tracker Application

This is a Python-based command-line interface (CLI) habit-tracking application. It allows users to add, delete, complete, and analyze their habits. The application tracks habits, calculates the longest streak, and provides analytics on habit completion. It uses JSON to store the habits persistently.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Commands](#commands)
- [Analytics](#analytics)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Features
- Add new habits with specific periodicity (daily, weekly).
- Mark habits as complete for the day.
- View completion history and analyze the longest streak.
- Calculate the median time for habit completion.
- Store habits persistently in a JSON file.

## Installation

### Prerequisites
- Python 3.12 or higher
- `pip` (Python package installer)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/RoelofJvv/HabitRepo
   cd habit-tracker
   ```

2. **Install the Required Dependencies**
   All required Python packages are listed in the `requirements.txt` file. Install them using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the Habit Data**
   Ensure the `habits.json` file is present in the root directory, as it stores your habit data.

## Running the Application

### Using the CLI
The application is run entirely from the command line. Once installed, you can use the following commands:

```bash
py cli.py [command] [arguments]
```

Example:
```bash
py cli.py add "exercise" "daily"
```

### Commands

1. **Add a Habit**
   Adds a new habit with a specific periodicity (daily, weekly, etc.).
   ```bash
   py cli.py add <task> <periodicity>
   ```
   Example:
   ```bash
   py cli.py add "exercise" "daily"
   ```

2. **List All Habits**
   Displays a list of all the habits with their current streaks and periodicity.
   ```bash
   py cli.py list
   ```

3. **Delete a Habit**
   Removes a habit by task name.
   ```bash
   py cli.py delete <task>
   ```
   Example:
   ```bash
   py cli.py delete "exercise"
   ```

4. **Mark a Habit as Complete**
   Marks a habit as completed for the day.
   ```bash
   py cli.py complete <task>
   ```
   Example:
   ```bash
   py cli.py complete "exercise"
   ```

5. **Analyze a Habit**
   Displays the current streak and longest streak of a habit.
   ```bash
   py cli.py analyze <task>
   ```
   Example:
   ```bash
   py cli.py analyze "exercise"
   ```

6. **View Completion History**
   Shows the full completion history for a habit.
   ```bash
   py cli.py history <task>
   ```
   Example:
   ```bash
   py cli.py history "exercise"
   ```

7. **Calculate Median Completion Time**
   Calculates the median completion time for a habit (if available).
   ```bash
   py cli.py median <task>
   ```
   Example:
   ```bash
   py cli.py median "exercise"
   ```

8. **View Longest Streak Across All Habits**
   Displays the habit with the longest streak.
   ```bash
   py cli.py longest_streak
   ```

## Analytics
- **List**: Return a list of all currently tracked habits.
- **List by Periodicity**: Return a list of all habits with the same periodicity
- **Longest Ever Streak**: Return the longest run streak of all defined habits
- **Longest Streak**: Return the longest run streak for a given habit
- **Median Completion Time**: Calculates and returns the median time of day when the habit is completed, based on past completion history.

## Testing

### Running Unit Tests
The application is fully tested with unit tests. To run the tests, use the following command:

```bash
py -m pytest --cov-report term-missing --cov=.
```

This will run all the tests and provide a coverage report.

## Troubleshooting

1. **Habit Not Found**:
   If you receive a message like `"Habit 'task_name' not found"`, ensure the task exists by running the `list` command and double-checking the spelling.

2. **Habit Already Completed**:
   If you try to mark a habit as complete but receive the message `"Habit 'task_name' is already completed today."`, you need to wait until the next day to complete the task again (if it's a daily habit).

3. **Permission Errors with JSON File**:
   If you're experiencing permission issues with the `habits.json` file, ensure the file has read/write permissions for your user.

---

### `requirements.txt`:
```txt
click==8.0.0
pytest==7.0.1
```

---
