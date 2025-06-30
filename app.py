import streamlit as st
import datetime
from tasks import add_task, delete_task, complete_task
from storage import load_tasks, save_tasks
from reminders import show_reminders

# Initialize session state variables early
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "edit_task_index" not in st.session_state:
    st.session_state.edit_task_index = None

# Define add task callback function
def add_task_callback():
    if st.session_state.new_description.strip() == "":
        st.session_state.add_task_error = "Please provide a task description."
        return

    # Convert due date (datetime.date) to string if not None
    due_date_obj = st.session_state.new_due_date
    due_date_str = due_date_obj.strftime("%Y-%m-%d") if due_date_obj else None

    add_task(st.session_state.tasks, st.session_state.new_description, due_date_str)
    save_tasks(st.session_state.tasks)
    st.session_state.show_add_form = False
    st.session_state.new_description = ""
    st.session_state.new_due_date = None  # reset date picker
    st.session_state.add_task_error = ""

# Callback to mark task as complete
def complete_task_callback(task_index):
    if st.session_state.tasks[task_index]["status"] != "completed":
        complete_task(st.session_state.tasks, str(task_index + 1))
        save_tasks(st.session_state.tasks)

# Callback to delete a task
def delete_task_callback(task_index):
    delete_task(st.session_state.tasks, str(task_index + 1))
    save_tasks(st.session_state.tasks)
    # Hide menu after delete
    st.session_state.pop(f"show_menu_{task_index}", None)
    # If editing the deleted task, clear edit index
    if st.session_state.edit_task_index == task_index:
        st.session_state.edit_task_index = None

# Callback to start editing a task
def edit_task_callback(task_index):
    st.session_state.edit_task_index = task_index
    st.session_state[f"show_menu_{task_index}"] = False

st.set_page_config(page_title="AI To-Do", layout="wide")
st.title("To-Do List Assistant")

reminders = show_reminders(st.session_state.tasks)
if reminders:
    with st.expander("🔔 You have tasks that are due or overdue!", expanded=True):
        for task, kind in reminders:
            due_info = f"{task['due_date']}"
            if task.get("due_time"):
                due_info += f" at {task['due_time']}"
            st.markdown(f"- **{task['description']}** → _{kind}_ (Due: `{due_info}`)")

st.button(
    "Add Tasks",
    key="fallback_add_button",
    on_click=lambda: st.session_state.update({"show_add_form": True}),
)

# Add Task form
if st.session_state.show_add_form:
    st.text_input("Task description", key="new_description")

    new_due = st.session_state.get("new_due_date")
    if not isinstance(new_due, datetime.date):
        new_due = None
    st.date_input("Due date (optional)", key="new_due_date", value=new_due)

    if st.button("Add Task", on_click=add_task_callback):
        st.success("Task added!")

    if st.session_state.get("add_task_error"):
        st.error(st.session_state.add_task_error)

st.subheader("📋 Your Tasks")

if st.session_state.tasks:
    # Split tasks into two halves for two-column display
    half = (len(st.session_state.tasks) + 1) // 2
    left_tasks = st.session_state.tasks[:half]
    right_tasks = st.session_state.tasks[half:]

    left_col, right_col = st.columns(2)

    def render_tasks_in_col(col, tasks_list, start_idx):
        with col:
            for idx, task in enumerate(tasks_list):
                i = start_idx + idx
                cols = st.columns([0.07, 0.75, 0.18])

                with cols[0]:
                    checked = task["status"] == "completed"
                    st.checkbox(
                        "",
                        value=checked,
                        key=f"check_{i}",
                        on_change=complete_task_callback,
                        args=(i,),
                        label_visibility="hidden",
                    )

                with cols[1]:
                    desc = task["description"]
                    if task["status"] == "completed":
                        desc = f"~~{desc}~~"  # strikethrough markdown
                    due_text = f"(Due: {task['due_date']})" if task.get("due_date") else ""
                    st.markdown(f"**{i + 1}. {desc}** {due_text}")

                with cols[2]:
                    if st.button("⋮", key=f"menu_{i}"):
                        st.session_state[f"show_menu_{i}"] = not st.session_state.get(f"show_menu_{i}", False)

                    if st.session_state.get(f"show_menu_{i}", False):
                        st.button("Edit", key=f"edit_{i}", on_click=edit_task_callback, args=(i,))
                        st.button("Delete", key=f"delete_{i}", on_click=delete_task_callback, args=(i,))

    render_tasks_in_col(left_col, left_tasks, 0)
    render_tasks_in_col(right_col, right_tasks, half)

    # Edit form
    if st.session_state.edit_task_index is not None:
        idx = st.session_state.edit_task_index
        st.markdown("---")
        st.subheader(f"✏️ Edit Task {idx + 1}")

        def update_task():
            # Convert edited_due (date) to string or None before saving
            due_date_obj = st.session_state.edited_due
            due_date_str = due_date_obj.strftime("%Y-%m-%d") if due_date_obj else None

            st.session_state.tasks[idx]["description"] = st.session_state.edited_desc
            st.session_state.tasks[idx]["due_date"] = due_date_str
            save_tasks(st.session_state.tasks)
            st.success("Task updated!")
            st.session_state.edit_task_index = None

        # Initialize edit fields in session state if missing
        if "edited_desc" not in st.session_state:
            st.session_state.edited_desc = st.session_state.tasks[idx]["description"]
        if "edited_due" not in st.session_state:
            due_str = st.session_state.tasks[idx].get("due_date", "")
            if due_str:
                st.session_state.edited_due = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
            else:
                st.session_state.edited_due = None

        with st.form("edit_form"):
            st.text_input("Task description", key="edited_desc")
            st.date_input("Due date", key="edited_due", value=st.session_state.edited_due)
            st.form_submit_button("Update Task", on_click=update_task)

else:
    st.write("You don't have any tasks yet.")
