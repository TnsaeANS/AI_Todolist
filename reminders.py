from datetime import datetime

def show_reminders(tasks):
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    reminders = []

    for t in tasks:
        if t["status"] == "pending" and t.get("due_date"):
            # Overdue by date
            if t["due_date"] < today_str:
                reminders.append((t, "Overdue"))
            # Due today and time has passed
            elif t["due_date"] == today_str and t.get("due_time"):
                if t["due_time"] <= time_str:
                    reminders.append((t, "Due Now"))

    return reminders
