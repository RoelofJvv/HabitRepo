import json
from habit_manager import Habit
import logging
import os

# Set up basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def load_habits_from_file(filename: str) -> list:
    """Load habits from a JSON file and convert them into Habit objects."""
    habits = []
    try:
        with open(filename, 'r') as file:
            habits_data = json.load(file)
            for habit_data in habits_data:
                habit = Habit(
                    task=habit_data['task'],
                    periodicity=habit_data['periodicity'],
                    current_streak=habit_data['current_streak'],
                    last_completed=habit_data['last_completed'],
                    completed_today=habit_data['completed_today'],
                    completed_at=habit_data['completed_at'],
                    highest_streak=habit_data['highest_streak'],
                    creation_date=habit_data['creation_date'],
                    completion_history=habit_data.get('completion_history', [])
                )
                habits.append(habit)
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file '{filename}'.")
    except Exception as e:
        logging.error(f"An error occurred while loading habits from file '{filename}': {e}")
    
    return habits

def save_habits_to_file(habits, file_path_or_obj):
    """Save a list of Habit objects to a JSON file or file-like object."""
    try:
        if isinstance(file_path_or_obj, (str, bytes, os.PathLike)):
            with open(file_path_or_obj, 'w') as file:
                habits_data = [habit.to_dict() for habit in habits]
                json.dump(habits_data, file, indent=4)
        else:
            habits_data = [habit.to_dict() for habit in habits]
            json.dump(habits_data, file_path_or_obj, indent=4)
    except Exception as e:
        logging.error(f"Error saving habits to file '{file_path_or_obj}': {e}")
