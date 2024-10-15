import tkinter as tk
from tkinter import messagebox
import secrets
import string

# Helper Function for Password Strength Calculation
def calculate_strength(password):
    length = len(password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_numbers = any(char.isdigit() for char in password)
    has_symbols = any(char in string.punctuation for char in password)

    strength = 0
    if length >= 8:
        strength += 1
    if has_upper:
        strength += 1
    if has_lower:
        strength += 1
    if has_numbers:
        strength += 1
    if has_symbols:
        strength += 1

    return strength

# Password Generation Function
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    if not (use_upper or use_lower or use_digits or use_symbols):
        return "" # Return empty if no options are selected

    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    password = ''.join(secrets.choice(char_pool) for _ in range(length))
    return password

# Update Password Strength Bar
def update_strength_bar(password, strength_var, strength_label):
    strength = calculate_strength(password)
    strength_var.set(strength)
    strength_label.config(text=f"Password Strength: {strength}/5")

# Main Application UI
class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keybee: The Key Maker")
        self.geometry("400x500")
        self.configure(bg="#2c3e50")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        tk.Label(self, text="Keybee: The Key Maker", font=("Arial", 24, "bold"), fg="white", bg="#2c3e50").pack(pady=20)

        # Password Length Slider
        tk.Label(self, text="Password Length:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack()
        self.length_var = tk.IntVar(value=12)
        tk.Scale(self, from_=8, to=64, orient="horizontal", variable=self.length_var, bg="#34495e", fg="white").pack(pady=10)

        # Checkbuttons for character types
        self.use_upper_var = tk.BooleanVar(value=True)
        self.use_lower_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_symbols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(self, text="Include Uppercase", variable=self.use_upper_var, bg="#2c3e50", fg="white").pack(anchor="w", padx=20)
        tk.Checkbutton(self, text="Include Lowercase", variable=self.use_lower_var, bg="#2c3e50", fg="white").pack(anchor="w", padx=20)
        tk.Checkbutton(self, text="Include Numbers", variable=self.use_digits_var, bg="#2c3e50", fg="white").pack(anchor="w", padx=20)
        tk.Checkbutton(self, text="Include Symbols", variable=self.use_symbols_var, bg="#2c3e50", fg="white").pack(anchor="w", padx=20)

        # Password Display Box
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 12), width=30)
        self.password_entry.pack(pady=20)

        # Password Strength Bar
        self.strength_var = tk.IntVar(value=0)
        self.strength_bar = tk.Scale(self, from_=0, to=5, orient="horizontal", variable=self.strength_var, bg="#34495e", fg="white", state="disabled")
        self.strength_bar.pack(pady=10)
        self.strength_label = tk.Label(self, text="Password Strength: 0/5", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.strength_label.pack()

        # Generate Button
        tk.Button(self, text="Generate Password", command=self.generate_password, bg="#e74c3c", fg="white", font=("Arial", 14)).pack(pady=20)

    def generate_password(self):
        length = self.length_var.get()
        use_upper = self.use_upper_var.get()
        use_lower = self.use_lower_var.get()
        use_digits = self.use_digits_var.get()
        use_symbols = self.use_symbols_var.get()

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        
        # Check if the password is empty (indicating no options were selected)
        if not password:
            messagebox.showerror("Error", "Please select at least one option.")
            return
        
        self.password_var.set(password)
        update_strength_bar(password, self.strength_var, self.strength_label)

# Main Loop
if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()