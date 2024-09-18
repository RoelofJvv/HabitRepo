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
        check_if_streak_broken(self)
        return self.current_streak

    def mark_as_completed(self):
        """Mark the habit as completed for the day."""
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

def check_if_streak_broken(habit):
    """Check if the streak is broken based on the periodicity and last completed date."""
    now = datetime.now()

    if habit.last_completed == "NA":
        return False

    last_completed_date = datetime.strptime(habit.last_completed, '%Y-%m-%d %H:%M:%S')

    if habit.periodicity == "daily":
        if (now - last_completed_date).days > 1:
            habit.current_streak = 0
            return True

    elif habit.periodicity == "weekly":
        if (now - last_completed_date).days > 7:
            habit.current_streak = 0
            return True

    return False

def find_habit(habits, task):
    task = task.strip().lower()
    for habit in habits:
        if habit.task == task:
            return habit
    return None

def add_habit(habits, task, periodicity):
    """Add a new habit. If a habit with the same task name already exists, do not create a duplicate."""
    task = task.strip().lower()

    if find_habit(habits, task):
        return

    periodicity = periodicity.strip().lower()
    current_streak = 0
    last_completed = "NA"
    completed_today = False
    completed_at = "NA"
    highest_streak = 0
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

    streak_broken = check_if_streak_broken(habit)

    if habit.completed_today:
        return False 

    habit.mark_as_completed()

    if streak_broken:
        habit.current_streak = 1 
        return "Streak broken, reset to 1 but marked as completed"
    
    return True  

def analyze_habit(habits, task):
    """Analyze the details of a specific habit."""
    habit = find_habit(habits, task)
    if habit:
        task = habit.task
        periodicity = habit.periodicity
        current_streak = habit.current_streak
        highest_streak = habit.highest_streak
        return task, periodicity, current_streak, highest_streak
    return None, None, None, None



