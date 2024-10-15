

import tkinter as tk
from tkinter import messagebox
import math

# Global variable for calculator mode (simple/scientific)
mode = "simple"
memory = None

# Function to handle button clicks
def button_click(value):
    current = entry_field.get()
    entry_field.delete(0, tk.END)
    entry_field.insert(tk.END, current + value)

# Function to clear the entry field
def clear():
    entry_field.delete(0, tk.END)

# Function to delete the last character
def delete_last():
    current = entry_field.get()
    entry_field.delete(0, tk.END)
    entry_field.insert(tk.END, current[:-1])

# Function to evaluate the expression
def evaluate():
    try:
        result = eval(entry_field.get())
        entry_field.delete(0, tk.END)
        entry_field.insert(tk.END, str(result))
        update_history(entry_field.get() + " = " + str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")

# Function to perform scientific operations
def scientific_operation(operation):
    try:
        value = float(entry_field.get())
        if operation == 'sqrt':
            result = math.sqrt(value)
        elif operation == 'sin':
            result = math.sin(math.radians(value))
        elif operation == 'cos':
            result = math.cos(math.radians(value))
        elif operation == 'tan':
            result = math.tan(math.radians(value))
        elif operation == 'log':
            result = math.log10(value)
        elif operation == 'factorial':
            result = math.factorial(int(value))
        entry_field.delete(0, tk.END)
        entry_field.insert(tk.END, str(result))
        update_history(operation + "(" + str(value) + ") = " + str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")

# Function to switch between simple and scientific mode
def switch_mode():
    global mode
    if mode == "simple":
        mode = "scientific"
        for button in scientific_buttons:
            button.grid()
    else:
        mode = "simple"
        for button in scientific_buttons:
            button.grid_remove()

# Function to store value in memory
def memory_store():
    global memory
    memory = entry_field.get()
    memory_label.config(text="Memory: " + memory)

# Function to recall value from memory
def memory_recall():
    if memory:
        entry_field.delete(0, tk.END)
        entry_field.insert(tk.END, memory)
    else:
        messagebox.showinfo("Memory", "No value stored in memory")

# Function to clear memory
def memory_clear():
    global memory
    memory = None
    memory_label.config(text="Memory: None")

# Function to update history log
def update_history(entry):
    history.insert(tk.END, entry + "\n")

# Function to clear history
def clear_history():
    history.delete(1.0, tk.END)

# Initialize main window
root = tk.Tk()
root.title("Numix: The Num Calculator")
root.geometry("400x600")

# Add background color or gradient background
root.configure(bg="#E0F7FA") # Light blue background

# Entry field for user input
entry_field = tk.Entry(root, font=("Helvetica", 20), bd=10, relief=tk.RIDGE, justify='right')
entry_field.grid(row=0, column=0, columnspan=5, padx=10, pady=20)

# Memory and History UI
memory_label = tk.Label(root, text="Memory: None", font=("Helvetica", 12), anchor="w", bg="#E0F7FA")
memory_label.grid(row=1, column=0, columnspan=5, sticky="w")
history = tk.Text(root, height=6, width=48, bg="#E3F2FD", state="normal", relief=tk.RIDGE)
history.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

# Button layout with styling
buttons = [
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
    ('0', 6, 0), ('.', 6, 1), ('+', 6, 2), ('=', 6, 3),
    ('C', 7, 0), ('Del', 7, 1), ('M+', 7, 2), ('MR', 7, 3)
]

for (text, row, col) in buttons:
    action = lambda x=text: button_click(x) if x not in ['=', 'C', 'Del', 'M+', 'MR'] else None
    button = tk.Button(root, text=text, width=8, height=2, font=("Arial", 14), bg="#B2EBF2", fg="#00796B", 
                       activebackground="#4DB6AC", activeforeground="white", command=action)
    button.grid(row=row, column=col, padx=5, pady=5)

# Special function buttons
tk.Button(root, text="=", width=8, height=2, font=("Arial", 14), bg="#004D40", fg="white", command=evaluate).grid(row=6, column=3)
tk.Button(root, text="C", width=8, height=2, font=("Arial", 14), bg="#D32F2F", fg="white", command=clear).grid(row=7, column=0)
tk.Button(root, text="Del", width=8, height=2, font=("Arial", 14), bg="#D32F2F", fg="white", command=delete_last).grid(row=7, column=1)
tk.Button(root, text="M+", width=8, height=2, font=("Arial", 14), bg="#00796B", fg="white", command=memory_store).grid(row=7, column=2)
tk.Button(root, text="MR", width=8, height=2, font=("Arial", 14), bg="#00796B", fg="white", command=memory_recall).grid(row=7, column=3)

# Scientific buttons (initially hidden)
scientific_buttons = [
    tk.Button(root, text="√x", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('sqrt')),
    tk.Button(root, text="sin", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('sin')),
    tk.Button(root, text="cos", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('cos')),
    tk.Button(root, text="tan", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('tan')),
    tk.Button(root, text="log", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('log')),
    tk.Button(root, text="x!", width=8, height=2, font=("Arial", 14), bg="#4DD0E1", command=lambda: scientific_operation('factorial'))
]

for i, button in enumerate(scientific_buttons):
    button.grid(row=8 + i//3, column=i%3, padx=5, pady=5)
    button.grid_remove()

# Toggle between simple and scientific modes
tk.Button(root, text="Scientific Mode", width=35, height=2, font=("Arial", 14), bg="#009688", fg="white", command=switch_mode).grid(row=9, column=0, columnspan=5)

# History and memory clear buttons
tk.Button(root, text="Clear History", width=35, height=2, font=("Arial", 14), bg="#ADD8E6", command=clear_history).grid(row=10, column=0, columnspan=5)

# Run the application
root.mainloop()