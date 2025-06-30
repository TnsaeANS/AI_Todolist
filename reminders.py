from datetime import datetime

def show_reminders(tasks):
    today = datetime.now().strftime("%Y-%m-%d")
    reminders = [t for t in tasks if t["status"] == "pending" and t["due_date"] and t["due_date"] <= today]
    
    if reminders:
        print("\n--- Reminders ---")
        for task in reminders:
            print(f"- {task['description']} is due! (Due: {task['due_date']})")
        print("-----------------")
