# Todo App CLI

A simple command-line todo list application built with Python, Typer, and Pydantic.

## Features

- Add tasks to your todo list.
- List all current tasks.
- Mark tasks as completed.
- Tasks are stored locally in a JSON file.

## Quick Start

### 1. Installation

First, clone the repository and navigate into the project directory.

It is recommended to use a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

Then, install the application in editable mode with all development dependencies:

```bash
pip install -e '.[dev]'
```

### 2. Usage

Once installed, you can use the `todo` command:

**Add a task:**
```bash
todo add "Buy groceries"
```

**List all tasks:**
```bash
todo list
```

**Complete a task:**
(Use the ID from the list command)
```bash
todo complete <TASK_ID>
```

## Development

### Running Tests

This project uses `pytest`. Tests are separated into unit and integration tests.

**Run all tests:**
```bash
pytest
```

**Run only unit tests:**
(Unit tests are located in `tests/test_unit.py`)
```bash
pytest tests/test_unit.py
```

**Run only integration tests:**
(Integration tests are located in `tests/test_integration.py`)
```bash
pytest tests/test_integration.py
```

### Linting

This project uses `ruff` for linting and formatting.

**Check for linting errors:**
```bash
ruff check .
```

**Automatically fix errors:**
```bash
ruff check . --fix
```

### Building the Project

The project is configured for packaging with `build`. To create a source distribution and a wheel:

```bash
python -m build
```

The distributable files will be located in the `dist/` directory.
