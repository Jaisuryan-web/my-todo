import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# --- Page config MUST come first ---
st.set_page_config(page_title="📝 Stylish To-Do App", page_icon="📝", layout="centered")

DATA_FILE = Path("tasks.json")

# --- Utility Functions ---
def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# --- Inject CSS for styling ---
st.markdown(
    """
    <style>
    /* Base button style */
    .stButton>button {
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: bold;
        transition: 0.3s;
        color: white;
    }

    /* Done button: green inner glow on hover */
    .stButton>button:has(span:contains("Done")) {
        background-color: #1f77b4;
        border: 2px solid #4CAF50;
    }
    .stButton>button:has(span:contains("Done")):hover {
        background-color: #4CAF50;
        box-shadow: inset 0 0 10px #4CAF50;
    }

    /* Delete button: red inner glow on hover */
    .stButton>button:has(span:contains("Delete")) {
        background-color: #b71c1c;
        border: 2px solid #b71c1c;
    }
    .stButton>button:has(span:contains("Delete")):hover {
        background-color: #ff1744;
        box-shadow: inset 0 0 10px #ff1744;
    }

    /* Task card */
    .task-card {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 8px;
        transition: 0.3s;
    }
    .task-card:hover {
        box-shadow: 0 0 10px #1f77b4;
        border-color: #1f77b4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App UI ---
st.title("📝 Stylish To-Do App")

# Add Task Section
st.header("Add New Task")
with st.form("add_task", clear_on_submit=True):
    task_name = st.text_input("Task Name")
    category = st.text_input("Category", "General")
    due = st.date_input("Due Date", value=datetime.today())
    submitted = st.form_submit_button("Add Task")
    if submitted:
        tasks = load_tasks()
        tasks.append({
            "task": task_name,
            "category": category,
            "due": due.strftime("%Y-%m-%d"),
            "done": False
        })
        save_tasks(tasks)
        st.success(f"✅ Added: {task_name}")

# Display Tasks
st.header("Tasks")
tasks = load_tasks()
if tasks:
    for i, t in enumerate(tasks, 1):
        status = "✔️" if t["done"] else "❌"
        st.markdown(
            f'<div class="task-card"><b>{i}. {t["task"]}</b> | {t["category"]} | Due: {t["due"]} | {status}</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1])

        # Done button
        done_button = col1.button("✅ Done", key=f"done_{i}")
        if done_button:
            t["done"] = True
            save_tasks(tasks)
            st.experimental_rerun()

        # Delete button
        delete_button = col2.button("🗑 Delete", key=f"del_{i}")
        if delete_button:
            tasks.pop(i-1)
            save_tasks(tasks)
            st.experimental_rerun()
else:
    st.info("No tasks yet! 🎉")
