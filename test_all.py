import pytest
from click.testing import CliRunner
from unittest.mock import patch, mock_open
from habit_manager import Habit, find_habit, add_habit, delete_habit, mark_habit_as_completed
from analytics import list_completion_history, list_all_habits, find_habits_by_periodicity, get_longest_streak_for_habit, calculate_median_completion_time, get_longest_streak_of_all_habits
from data_manager import load_habits_from_file, save_habits_to_file
from cli import cli
import json
from io import StringIO

# ===== CLI Tests =====

# Test adding a habit with missing arguments
def test_add_missing_arguments():
    runner = CliRunner()
    result = runner.invoke(cli, ['add'])
    assert result.exit_code != 0
    assert "Missing argument 'TASK'" in result.output

# Test completing a habit with missing arguments
def test_complete_missing_arguments():
    runner = CliRunner()
    result = runner.invoke(cli, ['complete'])
    assert result.exit_code != 0
    assert "Missing argument 'TASK'" in result.output

# Test analyzing a nonexistent habit
def test_analyze_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['analyze', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

# Test completing a nonexistent habit
def test_complete_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['complete', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

# Test history for a nonexistent habit
def test_history_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['history', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

# Test deleting a nonexistent habit
def test_delete_nonexistent_habit():
    runner = CliRunner()
    result = runner.invoke(cli, ['delete', 'nonexistent_habit'])
    assert result.exit_code == 0
    assert "Habit 'nonexistent_habit' not found." in result.output

# Test list when no habits are present
def test_cli_list_no_habits():
    runner = CliRunner()
    with patch('cli.load_habits', return_value=[]):
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert "No habits found." in result.output

# Test listing habits by periodicity
def test_list_by_periodicity(predefined_habits):
    runner = CliRunner()
    with patch('cli.load_habits', return_value=predefined_habits):
        result = runner.invoke(cli, ['list_by_periodicity', 'daily'])
        assert result.exit_code == 0
        assert "exercise" in result.output

def test_cli_add_missing_arguments():
    """Test adding a habit with missing arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ['add'])
    assert result.exit_code != 0
    assert "Missing argument 'TASK'" in result.output

def test_list_by_invalid_periodicity(predefined_habits):
    """Test listing habits by an invalid periodicity."""
    runner = CliRunner()
    with patch('cli.load_habits', return_value=predefined_habits):
        result = runner.invoke(cli, ['list_by_periodicity', 'invalid_periodicity'])
        assert result.exit_code == 0
        assert "No habits found with periodicity: invalid_periodicity" in result.output


# ===== Data Manager Tests =====

# Test for a FileNotFoundError
@patch('builtins.open', side_effect=FileNotFoundError)
def test_load_habits_file_not_found(mock_open):
    habits = load_habits_from_file('non_existent_file.json')
    assert habits == []

# Test saving habits to file using StringIO
def test_save_habits_to_file(predefined_habits):
    file_handle = StringIO()
    save_habits_to_file(predefined_habits, file_handle)
    written_data = file_handle.getvalue()

    saved_habits = json.loads(written_data)
    assert saved_habits[0]['task'] == 'exercise'
    assert len(saved_habits) == 2

# ===== Analytics Tests =====

# Test listing the completion history of a habit
def test_list_completion_history(predefined_habits):
    history = list_completion_history(predefined_habits, "exercise")
    assert history is not None
    assert "2024-09-10" in history

# Test listing habits by periodicity
def test_find_habits_by_periodicity(predefined_habits):
    daily_habits = find_habits_by_periodicity(predefined_habits, "daily")
    assert len(daily_habits) == 1
    assert daily_habits[0].task == "exercise"

# Test getting the longest streak for a habit
def test_get_longest_streak_for_habit(predefined_habits):
    longest_streak = get_longest_streak_for_habit(predefined_habits, "exercise")
    assert longest_streak == 5

def test_calculate_median_no_history(predefined_habits):
    """Test calculating the median completion time when there's no history."""
    predefined_habits[0].completion_history = []  # No completion history
    result = calculate_median_completion_time(predefined_habits, 'exercise')
    assert result is None  # Should return None since no data is available

def test_calculate_median_invalid_dates(predefined_habits):
    """Test calculating the median completion time with invalid dates."""
    predefined_habits[0].completion_history = [{'datetime': 'invalid_date'}]  # Invalid date format
    result = calculate_median_completion_time(predefined_habits, 'exercise')
    assert result is None  # Should return None since date parsing fails

def test_get_longest_streak_no_streak(predefined_habits):
    """Test getting the longest streak when no streak is defined."""
    predefined_habits[0].highest_streak = 0  # No streak
    result = get_longest_streak_for_habit(predefined_habits, 'exercise')
    assert result == 0  # Should return 0 since no streak is present

# Test longest streak of all habits
def test_get_longest_streak_of_all_habits(predefined_habits):
    task, streak = get_longest_streak_of_all_habits(predefined_habits)
    assert task == "exercise"
    assert streak == 5


# Test longest streak for a specific habit
def test_get_longest_streak_for_habit(predefined_habits):
    streak = get_longest_streak_for_habit(predefined_habits, "exercise")
    assert streak == 5

    streak_nonexistent = get_longest_streak_for_habit(predefined_habits, "nonexistent_habit")
    assert streak_nonexistent is None



# ===== Habit Manager Tests =====

# Test finding a habit that does not exist
def test_find_habit_not_found(predefined_habits):
    habit = find_habit(predefined_habits, "nonexistent_task")
    assert habit is None

# Test adding a duplicate habit
def test_add_duplicate_habit(predefined_habits):
    add_habit(predefined_habits, "exercise", "daily")
    assert len(predefined_habits) == 2  # Habit should not be added again

# Test marking a habit as completed
def test_mark_habit_completed(predefined_habits):
    result = mark_habit_as_completed(predefined_habits, "exercise")
    assert result is True  # The habit should be marked as completed
    assert predefined_habits[0].completed_today is True

# Test marking a habit that is already completed
def test_mark_habit_completed(predefined_habits):
    # Make sure the habit is not marked as completed today initially
    predefined_habits[0].completed_today = False
    result = mark_habit_as_completed(predefined_habits, "exercise")
    assert result is True  # The habit should be marked as completed
    assert predefined_habits[0].completed_today is True


# Test deleting an existing habit
def test_delete_existing_habit(predefined_habits):
    delete_habit(predefined_habits, "exercise")
    assert len(predefined_habits) == 1  # One habit should remain

def test_mark_habit_as_completed_nonexistent(predefined_habits):
    """Test trying to mark a nonexistent habit as completed."""
    result = mark_habit_as_completed(predefined_habits, 'nonexistent_task')
    assert result is None  # Should return None when habit is not found

def test_mark_habit_as_already_completed(predefined_habits):
    """Test marking a habit that's already completed today."""
    predefined_habits[0].completed_today = True  # Already completed today
    result = mark_habit_as_completed(predefined_habits, 'exercise')
    assert result is False  # Should return False since the habit was already completed

def test_delete_nonexistent_habit(predefined_habits):
    """Test trying to delete a nonexistent habit."""
    initial_habit_count = len(predefined_habits)
    delete_habit(predefined_habits, 'nonexistent_task')
    assert len(predefined_habits) == initial_habit_count  # List size should remain the same


# ===== Fixtures and Utilities =====

@pytest.fixture
def predefined_habits():
    """Fixture to provide predefined habit data for testing."""
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
