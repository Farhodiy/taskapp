
success = delete_task(tasks, task_id)
if not success:
    print(f"No task found with ID {task_id}.")
else:
    save_data(next_id, tasks)
    print("Task deleted.")