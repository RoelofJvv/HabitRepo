import click
from habit_manager import add_habit, delete_habit, is_completed_today, list_completion_history, mark_habit_as_completed, list_all_habits, find_habit, find_habits_by_periodicity
from data_manager import load_habits_from_file, save_habits_to_file
from analytics import calculate_median_completion_time, analyze_habit, longest_streak_of_all_habits

# Load habits file (common logic for all commands)
def load_habits():
    return load_habits_from_file('habits.json')

def save_habits(habits):
    save_habits_to_file(habits, 'habits.json')

@click.group()
def cli():
    """A command-line interface for managing habits."""
    pass

@click.command(name="add")
@click.argument('task')
@click.argument('periodicity')
def add(task, periodicity):
    """Add a new habit with TASK and PERIODICITY. Check if the habit already exists."""
    habits = load_habits()

    # Check if habit already exists
    if find_habit(habits, task):
        click.echo(f"Habit '{task}' already exists. Cannot add a duplicate.")
    else:
        add_habit(habits, task, periodicity)
        save_habits(habits)
        click.echo(f"Added new habit: {task} with periodicity: {periodicity}")

@click.command(name="delete")
@click.argument('task')
def delete(task):
    """Delete a habit with the given TASK name."""
    habits = load_habits()
    habit = find_habit(habits, task)

    if habit:
        delete_habit(habits, task)
        save_habits(habits)
        click.echo(f"Deleted habit: {task}")
    else:
        click.echo(f"Habit '{task}' not found.")

@click.command(name="list")
def list_command():
    """List all habits."""
    habits = load_habits()
    habit_details = list_all_habits(habits)
    click.echo(habit_details)

@click.command(name="complete")
@click.argument('task')
def complete(task):
    """Mark a habit with TASK as completed. Check if the habit has already been completed today."""
    habits = load_habits()
    habit = find_habit(habits, task)

    if habit is None:
        click.echo(f"Habit '{task}' not found.")
        return

    # Check if habit has already been completed today
    if is_completed_today(habit):
        click.echo(f"Habit '{task}' has already been completed today.")
    else:
        mark_habit_as_completed(habits, task)
        save_habits(habits)
        click.echo(f"Marked habit '{task}' as completed.")

@click.command(name="analyze")
@click.argument('task')
def analyze(task):
    """Analyze a specific habit with TASK name."""
    habits = load_habits()
    habit = find_habit(habits, task)

    if habit is None:
        click.echo(f"Habit '{task}' not found.")
        return

    task, periodicity, current_streak, highest_streak = analyze_habit(habits, task)
    click.echo(f"Task: {task}, Periodicity: {periodicity}, Current Streak: {current_streak}, Longest Streak: {highest_streak}")

@click.command(name="median")
@click.argument('task')
def median(task):
    """Calculate the median time of the completion of a TASK."""
    habits = load_habits()
    habit = find_habit(habits, task)

    if habit is None:
        click.echo(f"Habit '{task}' not found.")
        return

    median = calculate_median_completion_time(habits, task)
    if median is None:
        click.echo(f"No completion records for habit '{task}'.")
    else:
        click.echo(f"Habit '{task}' is completed at a median time of '{median}'.")

@click.command(name="history")
@click.argument('task')
def history(task):
    """Return the list of completion dates of a TASK."""
    habits = load_habits()
    habit = find_habit(habits, task)

    if habit is None:
        click.echo(f"Habit '{task}' not found.")
        return

    history_list = list_completion_history(habits, task)
    if history_list is None:
        click.echo(f"There is no history of completion for the habit {task}.")
    else:
        click.echo(f"The completion history for {task}: \n{history_list}")

@click.command(name="longest_streak")
def longest_streak():
    """Display the habit with the longest current streak."""
    habits = load_habits()
    longest = longest_streak_of_all_habits(habits)

    if longest is None:
        click.echo("No habits found.")
    else:
        click.echo(f"The habit with the longest streak is '{longest[0]}' with a streak of {longest[1]}.")

@cli.command()
@click.argument('periodicity')
def list_by_periodicity(periodicity):
    """List all habits with the given periodicity (e.g., daily, weekly)."""
    habits = load_habits()
    matching_habits = find_habits_by_periodicity(habits, periodicity)
    
    if matching_habits:
        habit_list = [f"Task: '{habit.task}', Periodicity: '{habit.periodicity}', Streak: {habit.get_streak()}" for habit in matching_habits]
        click.echo("\n".join(habit_list))
    else:
        click.echo(f"No habits found with periodicity: {periodicity}")


# Register the commands explicitly
cli.add_command(add)
cli.add_command(delete)
cli.add_command(list_command)
cli.add_command(complete)
cli.add_command(analyze)
cli.add_command(median)
cli.add_command(history)
cli.add_command(longest_streak)
cli.add_command(list_by_periodicity)

if __name__ == "__main__":
    cli()
