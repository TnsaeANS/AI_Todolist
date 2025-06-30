from tasks import load_tasks, add_task, delete_task, complete_task, list_tasks
from reminders import show_reminders
from nlp_processor import process_command

def main():
    tasks = load_tasks()
    print("AI To-Do List Assistant")
    show_reminders(tasks)
    print("\nI can help you add, delete, complete, and list tasks.")

    while True:
        command = input("> ").strip()
        intent, entities = process_command(command)

        if intent == "exit":
            print("Goodbye!")
            break
        elif intent == "add_task":
            if entities["task_description"]:
                add_task(tasks, entities["task_description"], entities["due_date"])
            else:
                print("I need a description of the task you want to add.")
        elif intent == "delete_task":
            if entities["task_id"]:
                delete_task(tasks, entities["task_id"])
            else:
                print("I need the number of the task you want to delete.")
        elif intent == "complete_task":
            if entities["task_id"]:
                complete_task(tasks, entities["task_id"])
            else:
                print("I need the number of the task you want to complete.")
        elif intent == "list_tasks":
            list_tasks(tasks)
        elif intent == "show_reminders":
            show_reminders(tasks)
        else:
            print("I'm not sure how to help with that. Please try a different command.")

if __name__ == "__main__":
    main()
