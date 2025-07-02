import streamlit as st
import datetime
from tasks import add_task, delete_task, complete_task
from storage import load_tasks, save_tasks
from reminders import show_reminders

def load_custom_css(file_path="style.css"):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_custom_css()

# Initialize session state variables early
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "edit_task_index" not in st.session_state:
    st.session_state.edit_task_index = None

# Callback to mark task as complete
def complete_task_callback(task_index):
    if st.session_state.tasks[task_index]["status"] != "completed":
        complete_task(st.session_state.tasks, str(task_index + 1))
        save_tasks(st.session_state.tasks)

# Callback to toggle task status based on checkbox state
def toggle_task_status(index):
    key = f"check_{index}"
    is_checked = st.session_state.get(key, False)
    task = st.session_state.tasks[index]
    task["status"] = "completed" if is_checked else "pending"
    save_tasks(st.session_state.tasks)

# Callback to delete a task
def delete_task_callback(task_index):
    delete_task(st.session_state.tasks, str(task_index + 1))
    save_tasks(st.session_state.tasks)
    st.session_state.pop(f"show_menu_{task_index}", None)
    if st.session_state.edit_task_index == task_index:
        st.session_state.edit_task_index = None

# Callback to start editing a task
def edit_task_callback(task_index):
    st.session_state.edit_task_index = task_index
    st.session_state[f"show_menu_{task_index}"] = False

st.set_page_config(page_title="AI To-Do", layout="wide")
st.title("To-Do List Assistant")

color_map = {
    "Overdue": "red",
    "Due Today": "orange",
    "Due Now": "green"
}

reminders = show_reminders(st.session_state.tasks)
if reminders:
    with st.expander("🔔 You have tasks that are due or overdue!", expanded=True):
        for task, kind in reminders:
            due_info = f"{task['due_date']}"
            if task.get("due_time"):
                due_info += f" at {task['due_time']}"
            color = color_map.get(kind, "gray")
            st.markdown(
                f"<div style='color:{color}; font-weight:bold;'>"
                f"• {task['description']} → {kind} (Due: {due_info})"
                f"</div>",
                unsafe_allow_html=True
            )

btn_col1, btn_col2, _ = st.columns([1, 1, 4])
with btn_col1:
    st.button(
        "Add Task",
        key="add_task_btn",
        on_click=lambda: st.session_state.update({"show_add_form": True}),
        use_container_width=True
    )
with btn_col2:
    if st.button("⚡ AI Organize", key="ai_organize_btn", use_container_width=True):
        importance_rank = {
            "very important": 0,
            "medium importance": 1,
            "low": 2
        }
        st.session_state.tasks.sort(key=lambda t: importance_rank.get(t.get("importance", "medium importance")))
        save_tasks(st.session_state.tasks)
        st.success("Tasks organized by importance.")

# Add Task form
if st.session_state.show_add_form:
    st.markdown("### 📝 Add New Task")
    st.markdown("Fill in the details for your new task.")

    with st.container():
        with st.columns([1, 5, 1])[1]:
            st.text_input("Task", key="new_description", placeholder="e.g., Finish project report")
            st.selectbox("Importance", ["very important", "medium importance", "low"], index=1, key="new_importance")
            st.date_input("Deadline", key="new_due_date")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                hour = st.selectbox("Hour", list(range(1, 13)), key="due_hour")
            with col2:
                minute = st.selectbox("Minute", [f"{i:02}" for i in range(0, 60, 5)], key="due_minute")
            with col3:
                ampm = st.selectbox("AM/PM", ["AM", "PM"], key="due_ampm")

            due_time_str = f"{hour}:{minute} {ampm}"

            if st.button("Create Task", key="create_task_button"):
                if not st.session_state.new_description.strip():
                    st.error("Please enter a task description.")
                else:
                    due_date_obj = st.session_state.new_due_date
                    due_date_str = due_date_obj.strftime("%Y-%m-%d") if due_date_obj else None

                    add_task(
                        st.session_state.tasks,
                        st.session_state.new_description,
                        due_date_str,
                        due_time_str,
                        st.session_state.new_importance
                    )
                    save_tasks(st.session_state.tasks)
                    st.success("Task created!")
                    st.session_state.show_add_form = False
                    st.rerun()

st.subheader("📋 Your Tasks")

if st.session_state.tasks:
    half = (len(st.session_state.tasks) + 1) // 2
    left_tasks = st.session_state.tasks[:half]
    right_tasks = st.session_state.tasks[half:]

    left_col, right_col = st.columns(2)

def render_tasks_in_col(col, tasks_list, start_idx):
    with col:
        for idx, task in enumerate(tasks_list):
            i = start_idx + idx
            checkbox_key = f"check_{i}"
            cols = st.columns([0.07, 0.75, 0.18])

            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = task["status"] == "completed"

            with cols[0]:
                st.checkbox("", key=checkbox_key, on_change=toggle_task_status, args=(i,), label_visibility="hidden")

            with cols[1]:
                overdue = (
                    task.get("due_date")
                    and task["due_date"] < datetime.datetime.now().strftime("%Y-%m-%d")
                    and task["status"] == "pending"
                )
                desc = (
                    f"<span class='task-title'>{'~~' + task['description'] + '~~' if task['status'] == 'completed' else task['description']}</span>"
                )
                due_str = f"{task.get('due_date', '')}"
                if task.get("due_time"):
                    due_str += f" at {task['due_time']}"
                overdue_badge = f"<span class='overdue'>⚠️ Overdue</span>" if overdue else ""
                st.markdown(
                    f"""
                    <div class='task-card'>
                        {desc}<br/>
                        <div class='task-meta'>
                             🗓️ {due_str} {overdue_badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with cols[2]:
                st.button("✏️", key=f"edit_{i}", on_click=edit_task_callback, args=(i,))
                st.button("🗑️", key=f"delete_{i}", on_click=delete_task_callback, args=(i,))

render_tasks_in_col(left_col, left_tasks, 0)
render_tasks_in_col(right_col, right_tasks, half)

if st.session_state.edit_task_index is not None:
    idx = st.session_state.edit_task_index
    st.markdown("---")
    st.subheader(f"✏️ Edit Task {idx + 1}")

    def update_task():
        due_date_obj = st.session_state.edited_due
        due_date_str = due_date_obj.strftime("%Y-%m-%d") if due_date_obj else None

        st.session_state.tasks[idx]["description"] = st.session_state.edited_desc
        st.session_state.tasks[idx]["due_date"] = due_date_str
        st.session_state.tasks[idx]["due_time"] = f"{st.session_state.edited_hour}:{st.session_state.edited_minute} {st.session_state.edited_ampm}"
        st.session_state.tasks[idx]["importance"] = st.session_state.edited_importance

        save_tasks(st.session_state.tasks)
        st.success("Task updated!")
        st.session_state.edit_task_index = None

    if "edited_desc" not in st.session_state:
        st.session_state.edited_desc = st.session_state.tasks[idx]["description"]
    if "edited_due" not in st.session_state:
        due_str = st.session_state.tasks[idx].get("due_date", "")
        if due_str:
            st.session_state.edited_due = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
        else:
            st.session_state.edited_due = None
    if "edited_importance" not in st.session_state:
        st.session_state.edited_importance = st.session_state.tasks[idx].get("importance", "medium importance")

    current_due_time = st.session_state.tasks[idx].get("due_time", "12:00 PM")
    try:
        hour_str, rest = current_due_time.split(":")
        minute_str, ampm = rest.split(" ")
        hour = int(hour_str)
        minute = minute_str
    except:
        hour, minute, ampm = 12, "00", "PM"

    st.session_state.edited_hour = hour
    st.session_state.edited_minute = minute
    st.session_state.edited_ampm = ampm

    with st.form("edit_form"):
        st.text_input("Task description", key="edited_desc")
        st.date_input("Due date", key="edited_due")

        st.selectbox("Importance", ["very important", "medium importance", "low"], key="edited_importance")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.selectbox("Hour", list(range(1, 13)), key="edited_hour")
        with col2:
            st.selectbox("Minute", [f"{i:02}" for i in range(0, 60, 5)], key="edited_minute")
        with col3:
            st.selectbox("AM/PM", ["AM", "PM"], key="edited_ampm")

        st.form_submit_button("Update Task", on_click=update_task)
else:
    st.write("You don't have any tasks to edit yet.")
