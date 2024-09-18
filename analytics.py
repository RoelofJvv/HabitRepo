import statistics
from datetime import datetime
from habit_manager import find_habit, check_if_streak_broken

def calculate_median_completion_time(habits, task):
    """Calculate the median completion time of a specific habit"""
    habit = find_habit(habits, task)
    if habit is None or not habit.completion_history:
        return None
    
    completion_times = []
    for completion in habit.completion_history:
        try:
            time = datetime.strptime(completion['datetime'], '%Y-%m-%d %H:%M:%S')
            completion_times.append(time)
        except ValueError:
            continue
    
    if not completion_times:
        return None
    
    completion_seconds = [
        time.hour * 3600 + time.minute * 60 + time.second
        for time in completion_times
    ]
    
    median_time_seconds = statistics.median(completion_seconds)
    median_hour = int(median_time_seconds // 3600)
    median_minute = int((median_time_seconds % 3600) // 60)
    
    return f"{median_hour:02}:{median_minute:02}"

def analyze_habit(habits, task):
    habit = find_habit(habits, task)
    if habit:
        return habit.task, habit.periodicity, habit.get_streak(), habit.highest_streak
    return None

def longest_streak_of_all_habits(habits):
    if not habits:
        return None
    habit = max(habits, key=lambda h: h.get_streak())
    return habit.task, habit.get_streak()

def list_completion_history(habits, task):
    """List the completion history for a given habit"""
    habit = find_habit(habits, task)
    if habit and habit.completion_history:
        return "\n".join([completion['datetime'] for completion in habit.completion_history])
    return None

def list_all_habits(habits):
    """Return a list of all habits"""
    if not habits:
        return "No habits found."
    else:
        habit_list = [f"Task: '{habit.task}', Periodicity: '{habit.periodicity}', Streak: {habit.get_streak()}, Last Completed: {habit.last_completed}" for habit in habits]
        return "\n".join(habit_list)

def find_habits_by_periodicity(habits, periodicity):
    """Return a list of habits that match the given periodicity"""
    periodicity = periodicity.strip().lower() 
    return [habit for habit in habits if habit.periodicity == periodicity]

def get_longest_streak_for_habit(habits, task):
    """Return the longest streak for a given habit."""
    habit = find_habit(habits, task)
    if habit is None:
        return None
    return habit.highest_streak

def get_longest_streak_of_all_habits(habits):
    """Return the habit with the longest streak"""
    if not habits:
        return None, 0

    for habit in habits:
        check_if_streak_broken(habit)

    longest_streak_habit = max(habits, key=lambda habit: habit.highest_streak)
    return longest_streak_habit.task, longest_streak_habit.highest_streak


def get_longest_streak_for_habit(habits, task):
    """Return the longest streak for the given task"""
    habit = find_habit(habits, task)
    if habit is None:
        return None

    check_if_streak_broken(habit)
    return habit.highest_streak
