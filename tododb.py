import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
DATABASE = "tasks.db"

def setup_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )"""
    )
    conn.commit()
    conn.close()

def add_task_to_db(task):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def get_tasks_from_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def remove_task_from_db(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def mark_task_done_in_db(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# GUI Functions
def load_tasks():
    tasks_listbox.delete(0, tk.END)
    for task_id, task, status in get_tasks_from_db():
        display_text = f"{task} {'(Done)' if status == 'done' else ''}"
        tasks_listbox.insert(tk.END, (task_id, display_text))

def add_task():
    task = task_entry.get().strip()
    if task:
        add_task_to_db(task)
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    selected = tasks_listbox.curselection()
    if selected:
        task_id, _ = tasks_listbox.get(selected[0])
        remove_task_from_db(task_id)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def mark_task_done():
    selected = tasks_listbox.curselection()
    if selected:
        task_id, _ = tasks_listbox.get(selected[0])
        mark_task_done_in_db(task_id)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as done!")

# App setup
root = tk.Tk()
root.title("To-Do List with Database")
root.geometry("500x500")
root.resizable(False, False)

# Task input
task_entry = ttk.Entry(root, width=40, font=("Arial", 12))
task_entry.pack(pady=10)
add_task_button = ttk.Button(root, text="Add Task", command=add_task)
add_task_button.pack(pady=5)

# Task list with scrollbar
tasks_frame = ttk.Frame(root)
tasks_frame.pack(pady=10)
tasks_listbox = tk.Listbox(tasks_frame, width=50, height=15, font=("Arial", 12))

tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=tasks_listbox.yview)
tasks_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Buttons
mark_done_button = ttk.Button(root, text="Mark as Done", command=mark_task_done)
mark_done_button.pack(pady=5)
remove_task_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_task_button.pack(pady=5)

# Load tasks on start
setup_database()
load_tasks()

# Run the application
root.mainloop()
