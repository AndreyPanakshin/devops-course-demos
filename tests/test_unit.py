from uuid import UUID

from todo_app.models import Task


def test_task_creation_defaults():
    """
    Test that a Task can be created with just a description
    and defaults like 'completed' and 'id' are set correctly.
    """
    description = "Buy groceries"
    task = Task(description=description)

    assert task.description == description
    assert not task.completed
    assert isinstance(task.id, UUID)

def test_task_creation_with_completed_true():
    """
    Test that a Task can be created with completed set to True.
    """
    description = "Finish report"
    task = Task(description=description, completed=True)

    assert task.description == description
    assert task.completed
    assert isinstance(task.id, UUID)

def test_task_id_is_uuid():
    """
    Test that the task ID is indeed a UUID object.
    """
    task = Task(description="Check ID type")
    assert isinstance(task.id, UUID)

def test_task_id_is_unique():
    """
    Test that two tasks created without specifying ID have unique IDs.
    """
    task1 = Task(description="Task 1")
    task2 = Task(description="Task 2")
    assert task1.id != task2.id
