from datetime import datetime

class Habit:
    def __init__(self, task, periodicity, current_streak, last_completed, completed_today, completed_at, highest_streak, creation_date, completion_history=None):
        self.task = task.strip().lower()  # Normalize to lowercase
        self.periodicity = periodicity.strip().lower()
        self.current_streak = int(current_streak)
        self.last_completed = last_completed
        self.completed_today = completed_today
        self.completed_at = completed_at
        self.highest_streak = highest_streak
        self.creation_date = creation_date
        self.completion_history = completion_history if completion_history is not None else []

    def get_streak(self):
        return self.current_streak

    def mark_as_completed(self):
        now = datetime.now()
        if self.completed_today:
            return 0

        self.last_completed = now.strftime('%Y-%m-%d %H:%M:%S')
        self.completed_today = True
        self.completed_at = now.strftime('%Y-%m-%d %H:%M:%S')
        self.current_streak += 1

        if self.current_streak > self.highest_streak:
            self.highest_streak = self.current_streak

        self.completion_history.append({'datetime': self.completed_at})
        return 1

    def to_dict(self):
        return {
            'task': self.task,
            'periodicity': self.periodicity,
            'current_streak': self.current_streak,
            'last_completed': self.last_completed,
            'completed_today': self.completed_today,
            'completed_at': self.completed_at,
            'highest_streak': self.highest_streak,
            'creation_date': self.creation_date,
            'completion_history': self.completion_history,
        }

# Function to find a habit by task name
def find_habit(habits, task):
    """Find a habit by task name."""
    task = task.strip().lower()  # Normalize to lowercase
    for habit in habits:
        if habit.task == task:
            return habit
    return None

# Function to add a new habit
def add_habit(habits, task, periodicity):
    """Add a new habit. If a habit with the same task name already exists, do not create a duplicate."""
    task = task.strip().lower()  # Normalize task name to lowercase

    # Check if the habit already exists
    if find_habit(habits, task):
        return  # Do nothing if the habit already exists

    periodicity = periodicity.strip().lower()  # Normalize periodicity to lowercase
    current_streak = 0
    last_completed = "NA"
    completed_today = False
    completed_at = "NA"
    highest_streak = 0
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a new Habit instance and add it to the list
    habit = Habit(task, periodicity, current_streak, last_completed, completed_today, completed_at, highest_streak, creation_date)
    habits.append(habit)

def delete_habit(habits, task):
    habit = find_habit(habits, task)
    if habit:
        habits.remove(habit)

def mark_habit_as_completed(habits, task):
    habit = find_habit(habits, task)
    if habit is None:
        return None
    if habit.completed_today:
        return False
    habit.mark_as_completed()
    return True

def is_completed_today(habit):
    return habit.completed_today


