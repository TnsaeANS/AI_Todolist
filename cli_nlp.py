from nlp_processor import process_command
from storage import load_tasks, save_tasks
from tasks import add_task, delete_task, complete_task, list_tasks

def main():
    print("🤖 Welcome to AI To-Do CLI! Type your command (or 'exit' to quit).")
    while True:
        command = input(">>> ")

        if command.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        intent, entities = process_command(command)
        tasks = load_tasks()

        if intent == "add_task":
            desc = entities["task_description"]
            due = entities["due_date"]
            add_task(tasks, desc, due)

        elif intent == "delete_task":
            task_id = entities.get("task_id")
            if task_id:
                delete_task(tasks, task_id)
            else:
                print("⚠️ Please specify which task to delete.")

        elif intent == "complete_task":
            task_id = entities.get("task_id")
            if task_id:
                complete_task(tasks, task_id)
            else:
                print("⚠️ Please specify which task to mark as complete.")

        elif intent == "list_tasks":
            list_tasks(tasks)

        elif intent == "show_reminders":
            print("🔔 (This intent is not handled in CLI — check the UI for reminders.)")

        else:
            print("❓ I didn't understand that command. Try: 'add', 'delete', 'complete', 'list'.")

        save_tasks(tasks)

if __name__ == "__main__":
    main()
