from storage import save_tasks

def add_task(tasks, description, due_date=None):
    tasks.append({"description": description, "status": "pending", "due_date": due_date})
    save_tasks(tasks)
    due_date_info = f", due {due_date}" if due_date else ""
    print(f"Task added: '{description}'{due_date_info}")

def delete_task(tasks, task_id):
    try:
        task_index = int(task_id) - 1
        if 0 <= task_index < len(tasks):
            removed_task = tasks.pop(task_index)
            save_tasks(tasks)
            print(f"Deleted task: '{removed_task['description']}'")
        else:
            print("Invalid task number.")
    except (ValueError, IndexError):
        print("Invalid command. Please provide a valid task number.")

def complete_task(tasks, task_id):
    try:
        task_index = int(task_id) - 1
        if 0 <= task_index < len(tasks):
            tasks[task_index]["status"] = "completed"
            save_tasks(tasks)
            print(f"Completed task: '{tasks[task_index]['description']}'")
        else:
            print("Invalid task number.")
    except (ValueError, IndexError):
        print("Invalid command. Please provide a valid task number.")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks):
        due_date_info = f" (Due: {task['due_date']})" if task['due_date'] else ""
        print(f"{i+1}. {task['description']} [{task['status']}] {due_date_info}")
