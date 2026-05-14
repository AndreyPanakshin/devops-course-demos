import json
from pathlib import Path
from typing import List

import pytest
from typer.testing import CliRunner

from todo_app.main import app
from todo_app.models import Task


# Fixture for the Typer CLI runner
@pytest.fixture(name="runner")
def runner_fixture() -> CliRunner:
    return CliRunner()

# Fixture for a temporary data file path
@pytest.fixture(name="temp_data_file")
def temp_data_file_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Provides a temporary data file path for tests using monkeypatch to ensure isolation.
    """
    # Create a temporary app dir inside tmp_path
    temp_app_dir = tmp_path / "test_app_dir"
    temp_app_dir.mkdir()
    temp_file = temp_app_dir / "tasks.json"

    # Use monkeypatch to temporarily change the module's global variables
    monkeypatch.setattr("todo_app.main.APP_DIR", str(temp_app_dir))
    monkeypatch.setattr("todo_app.main.DATA_FILE", temp_file)

    return temp_file

def get_tasks_from_file(file_path: Path) -> List[Task]:
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        tasks_data = json.load(f)
    return [Task(**data) for data in tasks_data]


def test_add_and_list_task(runner: CliRunner, temp_data_file: Path):
    """
    Test adding a task and then listing it to confirm persistence.
    """
    result = runner.invoke(app, ["add", "Test task description"])
    assert result.exit_code == 0
    assert "Task added:" in result.stdout

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Test task description" in result.stdout
    assert "[ ]" in result.stdout # Check for incomplete status

    tasks_in_file = get_tasks_from_file(temp_data_file)
    assert len(tasks_in_file) == 1
    assert tasks_in_file[0].description == "Test task description"
    assert not tasks_in_file[0].completed

def test_list_no_tasks(runner: CliRunner, temp_data_file: Path):
    """
    Test that the list command correctly reports no tasks when the file is empty.
    """
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No tasks found. Add one with 'todo add <description>'." in result.stdout

def test_complete_task(runner: CliRunner, temp_data_file: Path):
    """
    Test adding a task, completing it, and verifying its status.
    """
    # Add a task
    add_result = runner.invoke(app, ["add", "Task to complete"])
    assert add_result.exit_code == 0

    # Extract UUID from output
    task_id_str = add_result.stdout.split("(ID: ")[1].split(")")[0].strip()

    # Complete the task
    complete_result = runner.invoke(app, ["complete", task_id_str])
    assert complete_result.exit_code == 0
    assert f"Task {task_id_str} marked as completed." in complete_result.stdout

    # List tasks and verify status
    list_result = runner.invoke(app, ["list"])
    assert list_result.exit_code == 0
    assert "[x]" in list_result.stdout # Check for completed status
    assert "Task to complete" in list_result.stdout

    tasks_in_file = get_tasks_from_file(temp_data_file)
    assert len(tasks_in_file) == 1
    assert tasks_in_file[0].completed
    assert str(tasks_in_file[0].id) == task_id_str


def test_complete_non_existent_task(runner: CliRunner, temp_data_file: Path):
    """
    Test attempting to complete a task that does not exist.
    """
    non_existent_id = "12345678-1234-5678-1234-567812345678" # A random UUID
    result = runner.invoke(app, ["complete", non_existent_id])
    # Typer commands often exit with 0 even on functional errors
    assert result.exit_code == 0
    assert f"Task with ID {non_existent_id} not found." in result.stderr

    tasks_in_file = get_tasks_from_file(temp_data_file)
    assert len(tasks_in_file) == 0 # No tasks should have been added
