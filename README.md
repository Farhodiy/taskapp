# Task App

A simple command-line task manager built to learn Python fundamentals: OOP with dataclasses, file-based persistence, and defensive error handling.

## Features
- Add, list, update, and delete tasks through an interactive menu
- Task status is `pending` or `done`; an `expired` status is calculated automatically once a task's deadline has passed
- Data is stored locally in `tasks.json`, saved after every change
- Handles missing or corrupted data files without crashing (auto-backs up unreadable files)

## Requirements
- Python 3.10+
- No external dependencies — standard library only

## Usage
Clone the repo and run:

    python3 main.py

You'll see a menu:

    1) Add task
    2) List tasks
    3) Update task
    4) Delete task
    5) Exit

## Project structure

    taskapp/
    ├── main.py       # CLI menu loop
    ├── models.py     # Task dataclass and status logic
    ├── storage.py    # JSON load/save, corrupted-file recovery
    ├── tasks.py      # add/update/delete task functions
    ├── tests/
    │   └── test_tasks.py
    ├── tasks.example.json   # sample data shape
    └── tasks.json    # your real data (gitignored, created on first run)

## Design notes
- Task IDs are never reused, even after deletion — a persistent counter tracks the next available ID independently of the current task list.
- `expired` is never stored; it's calculated at display time by comparing a task's deadline to the current time, so a completed task never gets mislabeled just because its deadline passed.

## Running tests

    python3 -m unittest discover -s tests

## Possible future additions
- Task priority levels
- Categories/tags
- Deadline reminder notifications
- SQLite backend instead of JSON