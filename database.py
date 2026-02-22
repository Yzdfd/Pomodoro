import json
import os
from datetime import datetime

# --- Direktori dan file JSON ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

POMODORO_FILE = os.path.join(DATA_DIR, 'pomodoro_progress.json')
TODO_FILE = os.path.join(DATA_DIR, 'todo_list.json')
TODO_LOG_JSON_FILE = os.path.join(DATA_DIR, 'todo_log.json')
TIMER_LOG_FILE = os.path.join(DATA_DIR, 'timer_log.json')

# =============================
# 📌 POMODORO FUNCTIONS
# =============================

def load_pomodoro_progress():
    if not os.path.exists(POMODORO_FILE):
        return []
    with open(POMODORO_FILE, 'r') as f:
        return json.load(f)

def save_pomodoro_progress(data):
    with open(POMODORO_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_pomodoro_session(duration, session_type):
    data = load_pomodoro_progress()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.append({'date': date, 'duration': duration, 'type': session_type})
    save_pomodoro_progress(data)

def get_all_pomodoro_sessions():
    return load_pomodoro_progress()

# =============================
# 📌 TODO FUNCTIONS
# =============================

def load_todo_list():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as f:
        return json.load(f)

def save_todo_list(data):
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_todo_item(task):
    data = load_todo_list()
    data.append({'task': task, 'done': False})
    save_todo_list(data)
    write_todo_log_json(f"Added task: '{task}'")

def toggle_todo_item(index):
    data = load_todo_list()
    if 0 <= index < len(data):
        data[index]['done'] = not data[index]['done']
        save_todo_list(data)
        status = 'done' if data[index]['done'] else 'not done'
        write_todo_log_json(f"Toggled task at index {index} to {status}")

def remove_todo_item(index):
    data = load_todo_list()
    if 0 <= index < len(data):
        task = data[index]['task']
        data.pop(index)
        save_todo_list(data)
        write_todo_log_json(f"Removed task: '{task}'")

def mark_todo_done(index):
    data = load_todo_list()
    if 0 <= index < len(data):
        data[index]['done'] = True
        save_todo_list(data)
        write_todo_log_json(f"Marked task as done: '{data[index]['task']}'")

# =============================
# 📌 TODO LOG FUNCTIONS
# =============================

def load_todo_logs():
    if not os.path.exists(TODO_LOG_JSON_FILE):
        return []
    with open(TODO_LOG_JSON_FILE, 'r') as f:
        return json.load(f)

def save_todo_logs(logs):
    with open(TODO_LOG_JSON_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def write_todo_log_json(message):
    logs = load_todo_logs()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs.append({'timestamp': timestamp, 'message': message})
    save_todo_logs(logs)

def get_todo_logs_json():
    return load_todo_logs()

# =============================
# 📌 TIMER LOG FUNCTIONS
# =============================

def load_timer_logs():
    if not os.path.exists(TIMER_LOG_FILE):
        return []
    with open(TIMER_LOG_FILE, 'r') as f:
        return json.load(f)

def save_timer_logs(logs):
    with open(TIMER_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def add_timer_log(title):
    logs = load_timer_logs()
    logs.append({
        'task': title,
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_timer_logs(logs)

def save_log(message):
    logs = load_timer_logs()
    logs.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': message
    })
    save_timer_logs(logs)
    
def mark_todo_done_by_title(title):
    data = load_todo_list()
    for task in data:
        if task["task"] == title and not task.get("done", False):
            task["done"] = True
            break
    save_todo_list(data)
