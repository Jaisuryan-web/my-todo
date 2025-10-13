import streamlit as st

# ⚙️ Must be the first Streamlit command
st.set_page_config(page_title="📝 Stylish To-Do App", page_icon="📝", layout="centered")

# 🌈 --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }

    /* Frosted glass card for content */
    .main {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.05);
    }

    /* Headings */
    h1 {
        text-align: center;
        font-weight: 700;
        color: #f5f5f5;
    }

    /* Task item style */
    .task-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s ease;
    }
    .task-item:hover {
        transform: scale(1.02);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.4rem 1rem;
        border: 2px solid transparent;
    }

    /* Add Button */
    .stButton>button[kind="primary"] {
        background-color: #1dd1a1;
        color: white;
        box-shadow: 0 0 10px rgba(29, 209, 161, 0.4);
    }
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 0 20px #1dd1a1, 0 0 40px #10ac84 inset;
        transform: translateY(-2px);
    }

    /* Done Button */
    .done-btn>button {
        background-color: transparent !important;
        color: #1dd1a1 !important;
        border: 2px solid #1dd1a1 !important;
        box-shadow: 0 0 10px rgba(29, 209, 161, 0.3);
    }
    .done-btn>button:hover {
        box-shadow: 0 0 20px #1dd1a1, 0 0 20px #1dd1a1 inset;
        background-color: rgba(29, 209, 161, 0.2) !important;
    }

    /* Delete Button */
    .delete-btn>button {
        background-color: transparent !important;
        color: #ff6b6b !important;
        border: 2px solid #ff6b6b !important;
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
    }
    .delete-btn>button:hover {
        box-shadow: 0 0 20px #ff6b6b, 0 0 20px #ff6b6b inset;
        background-color: rgba(255, 107, 107, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 --- App Logic ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("📝 Stylish To-Do App")

# Add new task
task = st.text_input("Enter a new task:")
if st.button("➕ Add Task", type="primary"):
    if task:
        st.session_state.tasks.append({"task": task, "done": False})
        st.success("Task added successfully!")

st.divider()

# Display tasks
if st.session_state.tasks:
    for i, t in enumerate(st.session_state.tasks):
        cols = st.columns([6, 1, 1])
        with cols[0]:
            st.markdown(f"""
                <div class="task-item">
                    <span style="text-decoration: {'line-through' if t['done'] else 'none'};">
                        {t['task']}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            done_key = f"done_{i}"
            with st.container():
                with st.form(done_key):
                    if st.form_submit_button("✅", use_container_width=True, key=done_key, help="Mark as Done", type="secondary"):
                        st.session_state.tasks[i]["done"] = not st.session_state.tasks[i]["done"]
        with cols[2]:
            delete_key = f"delete_{i}"
            with st.container():
                with st.form(delete_key):
                    if st.form_submit_button("🗑️", use_container_width=True, key=delete_key, help="Delete Task", type="secondary"):
                        st.session_state.tasks.pop(i)
                        st.rerun()
else:
    st.info("No tasks yet. Add one above!")

st.markdown("<br><center>✨ Designed with ❤️ using Streamlit ✨</center>", unsafe_allow_html=True)
