import tkinter as tk
from tkinter import ttk, messagebox
import os

# File to save tasks
TASKS_FILE = "tasks.txt"

# Function to load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                tasks_listbox.insert(tk.END, line.strip())

# Function to save tasks to file
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        tasks = tasks_listbox.get(0, tk.END)
        for task in tasks:
            file.write(f"{task}\n")

# Function to add a task
def add_task():
    task = task_entry.get()
    if task.strip():
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to remove a selected task
def remove_task():
    selected_task_index = tasks_listbox.curselection()
    if selected_task_index:
        tasks_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove!")

# Function to clear all tasks
def clear_all_tasks():
    tasks_listbox.delete(0, tk.END)
    messagebox.showinfo("Info", "All tasks cleared!")

# Function to mark a task as done
def mark_task_done():
    selected_task_index = tasks_listbox.curselection()
    if selected_task_index:
        task = tasks_listbox.get(selected_task_index)
        # Append " (Done)" if not already marked
        if " (Done)" not in task:
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, f"{task} (Done)")
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as done!")

# Create the main application window
root = tk.Tk()
root.title("Enhanced To-Do List")
root.geometry("500x500")
root.resizable(False, False)

# Use ttk for better styling
style = ttk.Style(root)
style.theme_use("clam")

# Input field and add button
task_entry = ttk.Entry(root, width=40, font=("Arial", 12))
task_entry.pack(pady=10)
add_task_button = ttk.Button(root, text="Add Task", command=add_task)
add_task_button.pack(pady=5)

# Task listbox
tasks_frame = ttk.Frame(root)
tasks_frame.pack(pady=10)

tasks_listbox = tk.Listbox(tasks_frame, width=50, height=15, font=("Arial", 12), selectmode=tk.SINGLE)
tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=tasks_listbox.yview)
tasks_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Buttons for additional features
mark_done_button = ttk.Button(root, text="Mark as Done", command=mark_task_done)
mark_done_button.pack(pady=5)

remove_task_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_task_button.pack(pady=5)

clear_all_button = ttk.Button(root, text="Clear All Tasks", command=clear_all_tasks)
clear_all_button.pack(pady=5)

# Load tasks when app starts and save when it closes
load_tasks()
root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])

# Run the application
root.mainloop()
