import pytest
from click.testing import CliRunner
from unittest.mock import patch, mock_open
from habit_manager import Habit, find_habit, list_all_habits, add_habit, delete_habit
from data_manager import load_habits_from_file, save_habits_to_file
from analytics import calculate_median_completion_time, analyze_habit, longest_streak_of_all_habits
from cli import cli
import json
from io import StringIO

# ===== CLI Tests =====

def test_add_missing_arguments():
    runner = CliRunner()
    result = runner.invoke(cli, ['add'])
    assert result.exit_code != 0
    assert "Missing argument 'TASK'" in result.output

def test_complete_missing_arguments():
    runner = CliRunner()
    result = runner.invoke(cli, ['complete'])
    assert result.exit_code != 0
    assert "Missing argument 'TASK'" in result.output

def test_invalid_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['nonexistent_command'])
    assert result.exit_code != 0
    assert "No such command" in result.output

def test_analyze_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['analyze', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

def test_complete_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['complete', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

def test_history_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['history', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

def test_cli_add_missing_periodicity():
    runner = CliRunner()
    result = runner.invoke(cli, ['add', 'exercise'])
    assert result.exit_code != 0
    assert "Missing argument 'PERIODICITY'" in result.output

def test_cli_delete_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['delete', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

def test_cli_complete_invalid_task():
    runner = CliRunner()
    result = runner.invoke(cli, ['complete', 'nonexistent_task'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_task' not found." in result.output

def test_cli_list_no_habits():
    runner = CliRunner()
    with patch('cli.load_habits', return_value=[]):
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert "No habits found." in result.output

def test_cli_analyze_nonexistent():
    runner = CliRunner()
    with patch('cli.load_habits', return_value=[]):
        result = runner.invoke(cli, ['analyze', 'nonexistent_task'])
        assert result.exit_code == 0
        assert "Habit 'nonexistent_task' not found." in result.output

def test_cli_median_nonexistent():
    runner = CliRunner()
    with patch('cli.load_habits', return_value=[]):
        result = runner.invoke(cli, ['median', 'nonexistent_task'])
        assert result.exit_code == 0
        assert "Habit 'nonexistent_task' not found." in result.output

# ===== Data Manager Tests =====

@patch('builtins.open', side_effect=FileNotFoundError)
def test_load_habits_file_not_found(mock_open):
    habits = load_habits_from_file('non_existent_file.json')
    assert habits == []

@patch('builtins.open', new_callable=mock_open, read_data="invalid_json")
@patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
def test_load_habits_json_decode_error(mock_json_load, mock_file):
    habits = load_habits_from_file('invalid_file.json')
    assert habits == []

def test_save_habits_to_file(predefined_habits):
    file_handle = StringIO()
    save_habits_to_file(predefined_habits, file_handle)
    written_data = file_handle.getvalue()

    saved_habits = json.loads(written_data)
    assert saved_habits[0]['task'] == 'exercise'
    assert len(saved_habits) == 2

@patch('builtins.open', side_effect=OSError("Write error"))
def test_save_habits_write_error(mock_open, predefined_habits):
    result = save_habits_to_file(predefined_habits, 'test_file.json')
    assert result is None

# ===== Analytics Tests =====

def test_calculate_median_completion_time_empty(predefined_habits):
    habit = predefined_habits[0]
    habit.completion_history = []
    median_time = calculate_median_completion_time(predefined_habits, 'exercise')
    assert median_time is None

def test_longest_streak(predefined_habits):
    result = longest_streak_of_all_habits(predefined_habits)
    assert result == ("exercise", 5)

def test_calculate_median_no_valid_completions(predefined_habits):
    predefined_habits[0].completion_history = [{'datetime': 'invalid_date'}]
    result = calculate_median_completion_time(predefined_habits, 'exercise')
    assert result is None

def test_calculate_median_completion_odd_history(predefined_habits):
    habit = predefined_habits[0]
    habit.completion_history = [{'datetime': '2024-09-10 07:00:00'}, {'datetime': '2024-09-11 08:00:00'}, {'datetime': '2024-09-12 09:00:00'}]
    result = calculate_median_completion_time(predefined_habits, 'exercise')
    assert result == '08:00'

def test_longest_streak_no_habits():
    habits = []
    result = longest_streak_of_all_habits(habits)
    assert result is None

# ===== Habit Manager Tests =====

def test_find_habit_not_found(predefined_habits):
    habit = find_habit(predefined_habits, "nonexistent_task")
    assert habit is None

def test_add_duplicate_habit(predefined_habits):
    add_habit(predefined_habits, "exercise", "daily")
    assert len(predefined_habits) == 2

def test_mark_habit_completed_no_streak(predefined_habits):
    habit = predefined_habits[0]
    habit.current_streak = 0
    habit.completed_today = False
    result = habit.mark_as_completed()
    assert result == 1
    assert habit.current_streak == 1

def test_mark_habit_as_completed_twice(predefined_habits):
    habit = predefined_habits[0]
    habit.mark_as_completed()
    assert habit.completed_today is True
    result = habit.mark_as_completed()
    assert result == 0
    assert habit.current_streak == 5

def test_delete_existing_habit(predefined_habits):
    delete_habit(predefined_habits, "exercise")
    assert len(predefined_habits) == 1

def test_delete_nonexistent_habit(predefined_habits):
    habits_before = len(predefined_habits)
    delete_habit(predefined_habits, 'nonexistent_task')
    assert len(predefined_habits) == habits_before

# ===== Fixtures and Utilities =====

@pytest.fixture
def predefined_habits():
    return [
        Habit(
            task="exercise",
            periodicity="daily",
            current_streak=5,
            last_completed="2024-09-16 07:00:00",
            completed_today=True,
            completed_at="2024-09-16 07:00:00",
            highest_streak=5,
            creation_date="2024-08-20 07:00:00",
            completion_history=[
                {'datetime': '2024-09-10 07:00:00'},
                {'datetime': '2024-09-11 07:00:00'},
                {'datetime': '2024-09-12 07:00:00'}
            ]
        ),
        Habit(
            task="reading",
            periodicity="weekly",
            current_streak=2,
            last_completed="2024-09-10 18:00:00",
            completed_today=False,
            completed_at="2024-09-10 18:00:00",
            highest_streak=2,
            creation_date="2024-08-25 10:00:00",
            completion_history=[
                {'datetime': '2024-09-01 18:00:00'},
                {'datetime': '2024-09-10 18:00:00'}
            ]
        )
    ]
