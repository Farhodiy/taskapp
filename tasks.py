from models import Task
def add_task(tasks: list[Task], next_id: int, name: str, description: str, deadline: str) -> tuple[Task, int]:
    task = Task(id=next_id, name=name, description=description, deadline=deadline)
    tasks.append(task)
    return task, next_id + 1


def update_task(tasks: list[Task], task_id: int, name: str = None, description: str = None,
                deadline: str = None, status: str = None) -> bool:
    for task in tasks:
        if task.id == task_id:
            if name is not None:
                task.name = name
            if description is not None:
                task.description = description
            if deadline is not None:
                task.deadline = deadline
            if status is not None and status in ("pending", "done"):
                task.status = status
            return True
    
    return False


def delete_task(tasks: list[Task], task_id: int) -> bool:
    for i, t in enumerate(tasks):
        if t.id == task_id:
            del tasks[i]
            return True
    return False