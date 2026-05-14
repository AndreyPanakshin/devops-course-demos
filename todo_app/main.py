import typer
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from todo_app.models import Task
from todo_app.database import load_tasks, save_tasks

# Define the data file path
# Use a default filename in the user's home directory for convenience
APP_DIR = typer.get_app_dir("todo-app-cli")
DATA_FILE = Path(APP_DIR) / "tasks.json"

app = typer.Typer(help="A simple CLI todo list application.")

@app.callback()
def main():
    """
    Manage your todo tasks.
    """
    # Ensure the app directory exists
    Path(APP_DIR).mkdir(parents=True, exist_ok=True)

@app.command()
def add(description: str = typer.Argument(..., help="Description of the task.")) -> None:
    """
    Adds a new task to the todo list.
    """
    tasks = load_tasks(DATA_FILE)
    new_task = Task(description=description)
    tasks.append(new_task)
    save_tasks(DATA_FILE, tasks)
    typer.echo(f"Task added: '{new_task.description}' (ID: {new_task.id})")

@app.command()
def list() -> None:
    """
    Lists all tasks in the todo list.
    """
    tasks = load_tasks(DATA_FILE)
    if not tasks:
        typer.echo("No tasks found. Add one with 'todo add <description>'.")
        return

    typer.echo("Your tasks:")
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        typer.echo(f"  {status} {task.description} (ID: {task.id})")

@app.command()
def complete(task_id: UUID = typer.Argument(..., help="The ID of the task to complete.")) -> None:
    """
    Marks a task as completed.
    """
    tasks = load_tasks(DATA_FILE)
    found = False
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            found = True
            break
    
    if found:
        save_tasks(DATA_FILE, tasks)
        typer.echo(f"Task {task_id} marked as completed.")
    else:
        typer.echo(f"Task with ID {task_id} not found.", err=True)

if __name__ == "__main__":
    app()
