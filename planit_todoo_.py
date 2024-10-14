import tkinter as tk
import subprocess
import sys

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install tkcalendar
install("tkcalendar")

# Now you can import the module
from tkcalendar import Calendar

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime

# Function placeholders
def load_tasks():
    return [] # Placeholder function for loading tasks, should return a list of tasks.

def add_task():
    task = entry_task.get()
    due_date = calendar.get_date() # Using Calendar widget for selecting date
    priority = priority_var.get()
    
    if task:
        task_listbox.insert(tk.END, f"{task} - {due_date} - {priority}")
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task")

def mark_complete():
    try:
        task_listbox.delete(task_listbox.curselection())
    except:
        messagebox.showwarning("Selection Error", "Please select a task to mark complete")

def delete_task():
    try:
        task_listbox.delete(task_listbox.curselection())
    except:
        messagebox.showwarning("Selection Error", "Please select a task to delete")

def update_task_list():
    tasks = load_tasks()
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Enhanced UI Setup
root = tk.Tk()
root.title("Planit")  

# Set window size and background color
root.geometry("600x600")
root.configure(bg="#2E3440") # Dark background for a modern look

# Title Label
title_label = tk.Label(root, text="Planit: The Task Planner", font=("Helvetica", 18, "bold"), bg="#2E3640", fg="#D8DEE9")
title_label.pack(pady=20)

# Task Entry Fields with custom fonts and colors
frame_top = tk.Frame(root, bg="#2E3440")
frame_top.pack(pady=10)

label_task = tk.Label(frame_top, text="Task:", font=("Helvetica", 12), bg="#2E3440", fg="#D8DEE9")
label_task.grid(row=0, column=0, padx=10)
entry_task = tk.Entry(frame_top, width=30, font=("Helvetica", 12), bg="#4C566A", fg="#ECEFF4")
entry_task.grid(row=0, column=1)

label_due = tk.Label(frame_top, text="Due Date:", font=("Helvetica", 12), bg="#2E3440", fg="#D8DEE9")
label_due.grid(row=1, column=0, padx=10)

# Add a calendar widget for date picking
calendar = Calendar(frame_top, selectmode='day', date_pattern='yyyy-mm-dd', background="#4C566A", disabledbackground="#2E3440", bordercolor="#D8DEE9", headersbackground="#4C566A", normalbackground="#4C566A", foreground="#ECEFF4", normalforeground="#ECEFF4", weekendbackground="#4C566A", weekendforeground="#ECEFF4")
calendar.grid(row=1, column=1, pady=10)

# Task Priority Dropdown with custom font and colors
priority_var = tk.StringVar(value="Medium")
label_priority = tk.Label(frame_top, text="Priority:", font=("Helvetica", 12), bg="#2E3440", fg="#D8DEE9")
label_priority.grid(row=2, column=0, padx=10)

priority_menu = ttk.OptionMenu(frame_top, priority_var, "Medium", "High", "Medium", "Low")
priority_menu.grid(row=2, column=1)

# Task List Display with custom background and font
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

task_listbox = tk.Listbox(frame_list, height=10, width=70, font=("Helvetica", 12), bg="#4C566A", fg="#ECEFF4", selectbackground="#88C0D0", selectforeground="#2E3440")
task_listbox.pack()

# Action Buttons with improved styling
frame_buttons = tk.Frame(root, bg="#2E3440")
frame_buttons.pack(pady=10)

button_add = tk.Button(frame_buttons, text="Add Task", command=add_task, font=("Helvetica", 12, "bold"), bg="#A3BE8C", fg="#2E3440", padx=10, pady=5)
button_add.grid(row=0, column=0, padx=5)

button_complete = tk.Button(frame_buttons, text="Mark Complete", command=mark_complete, font=("Helvetica", 12, "bold"), bg="#88C0D0", fg="#2E3440", padx=10, pady=5)
button_complete.grid(row=0, column=1, padx=5)

button_delete = tk.Button(frame_buttons, text="Delete Task", command=delete_task, font=("Helvetica", 12, "bold"), bg="#BF616A", fg="#ECEFF4", padx=10, pady=5)
button_delete.grid(row=0, column=2, padx=5)

# Load tasks into the listbox at startup
update_task_list()

root.mainloop()