import statistics
from datetime import datetime
from habit_manager import find_habit

def calculate_median_completion_time(habits, task):
    """Calculate the median completion time of a specific habit."""
    habit = find_habit(habits, task)
    if habit is None or not habit.completion_history:
        return None
    
    completion_times = []
    for completion in habit.completion_history:
        try:
            time = datetime.strptime(completion['datetime'], '%Y-%m-%d %H:%M:%S')
            completion_times.append(time)
        except ValueError:
            # Skip invalid date formats
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
