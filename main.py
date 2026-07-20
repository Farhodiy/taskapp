from datetime import datetime
from storage import load_data, save_data
from tasks import add_task, update_task, delete_task


def prompt_deadline(current=None):
    """Prompt for a deadline, validate it, allow blank to skip (update only)."""
    while True:
        raw = input(f"Deadline (YYYY-MM-DDTHH:MM:SS){' [leave blank to keep]' if current else ''}: ").strip()
        if not raw and current is not None:
            return None  # signal: no change
        try:
            datetime.fromisoformat(raw)
            return raw
        except ValueError:
            print("Invalid format. Example: 2026-08-01T18:00:00")


def show_menu():
    print("\n1) Add task\n2) List tasks\n3) Update task\n4) Delete task\n5) Exit")


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    for t in tasks:
        print(f"[{t.id}] {t.name} - {t.display_status()} - due {t.deadline}")


def main():
    next_id, tasks = load_data()

    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            description = input("Description: ").strip()
            deadline = prompt_deadline()
            _, next_id = add_task(tasks, next_id, name, description, deadline)
            save_data(next_id, tasks)
            print("Task added.")

        elif choice == "2":
            list_tasks(tasks)

        elif choice == "3":
            try:
                task_id = int(input("Task ID to update: ").strip())
            except ValueError:
                print("Invalid ID.")
                continue

            name = input("New name [leave blank to keep]: ").strip() or None
            description = input("New description [leave blank to keep]: ").strip() or None
            deadline = prompt_deadline(current=True)
            status_choice = input("New status - 1) pending 2) done [leave blank to keep]: ").strip()
            status = {"1": "pending", "2": "done"}.get(status_choice)

            success = update_task(tasks, task_id, name=name, description=description,
                                   deadline=deadline, status=status)
            if success:
                save_data(next_id, tasks)
                print("Task updated.")
            else:
                print(f"No task found with ID {task_id}.")

        elif choice == "4":
            try:
                task_id = int(input("Task ID to delete: ").strip())
            except ValueError:
                print("Invalid ID.")
                continue

            success = delete_task(tasks, task_id)
            if success:
                save_data(next_id, tasks)
                print("Task deleted.")
            else:
                print(f"No task found with ID {task_id}.")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid choice, pick 1-5.")


if __name__ == "__main__":
    main()
    