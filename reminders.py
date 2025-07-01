from datetime import datetime

def show_reminders(tasks):
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    reminders = []

    for t in tasks:
        if t["status"] == "pending" and t.get("due_date"):
            if t["due_date"] < today_str:
                reminders.append((t, "Overdue"))
            elif t["due_date"] == today_str:
                if t.get("due_time"):
                    if t["due_time"] <= time_str:
                        reminders.append((t, "Due Now"))
                    else:
                        reminders.append((t, "Due Today"))
                else:
                    reminders.append((t, "Due Today"))

    return reminders
