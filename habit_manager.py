from datetime import datetime, timedelta

class Habit:
    def __init__(self, task, periodicity, current_streak, last_completed, completed_today, completed_at, highest_streak, creation_date, completion_history=None):
        self.task = task.strip().lower()
        self.periodicity = periodicity.strip().lower()
        self.current_streak = int(current_streak)
        self.last_completed = last_completed
        self.completed_today = completed_today
        self.completed_at = completed_at
        self.highest_streak = highest_streak
        self.creation_date = creation_date
        self.completion_history = completion_history if completion_history is not None else []

    def get_streak(self):
        """Return the current streak, after checking if the streak is broken."""
        check_if_streak_broken(self)  # Check if the streak is broken before returning
        return self.current_streak

    def mark_as_completed(self):
        """Mark the habit as completed for the day."""
        now = datetime.now()

        if self.completed_today:
            return 0  # Already completed today

        # Update the streak and completion history
        self.last_completed = now.strftime('%Y-%m-%d %H:%M:%S')
        self.completed_today = True
        self.completed_at = now.strftime('%Y-%m-%d %H:%M:%S')
        self.current_streak += 1

        if self.current_streak > self.highest_streak:
            self.highest_streak = self.current_streak

        # Add the completion time to the completion history
        self.completion_history.append({'datetime': self.completed_at})
        return 1  # Completed successfully

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
def check_if_streak_broken(habit):
    """Check if the streak is broken for a habit based on periodicity and last completed date."""
    now = datetime.now()

    # If no last_completed date, the streak cannot be broken
    if habit.last_completed == "NA":
        return False

    last_completed_date = datetime.strptime(habit.last_completed, '%Y-%m-%d %H:%M:%S')

    if habit.periodicity == "daily":
        if (now - last_completed_date).days > 1:
            habit.current_streak = 0  # Streak is broken
            return True

    elif habit.periodicity == "weekly":
        if (now - last_completed_date).days > 7:
            habit.current_streak = 0  # Streak is broken
            return True

    return False


# Function to find a habit by task name
def find_habit(habits, task):
    task = task.strip().lower()
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
        return None  # Habit not found

    streak_broken = check_if_streak_broken(habit)

    if habit.completed_today:
        return False  # Already completed today

    habit.mark_as_completed()

    if streak_broken:
        return "Streak broken, reset to 0 but marked as completed"
    
    return True  # Marked as completed successfully

def is_completed_today(habit):
    return habit.completed_today


