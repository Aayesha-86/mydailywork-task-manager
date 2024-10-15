import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sqlite3

# Set up leaderboard database
def setup_leaderboard_db():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                 (name TEXT, score INTEGER)''')
    conn.commit()
    conn.close()

def save_score(name, score):
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

def get_top_scores():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    return c.fetchall()

# Quiz data
quiz_data = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": 2},
    {"question": "Which language is primarily used for web development?", "options": ["Python", "JavaScript", "C++", "Java"], "answer": 1},
    {"question": "What is the smallest planet in our solar system?", "options": ["Earth", "Mars", "Mercury", "Venus"], "answer": 2},
    {"question": "Which year did World War I begin?", "options": ["1914", "1918", "1939", "1945"], "answer": 0}
]

# Shuffle the questions
random.shuffle(quiz_data)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0") # Light gray background

        self.score = 0
        self.current_question = 0
        self.timer_label = None
        self.time_left = 10 # 10 seconds for each question

        # Setup leaderboard database
        setup_leaderboard_db()

        # Title label
        self.title_label = tk.Label(self.root, text="Welcome to the Quizzy!", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2E8B57")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=("Arial", 18), bg="#32CD32", fg="white", borderwidth=2, relief="raised")
        self.start_button.pack(pady=20)

        self.leaderboard_button = tk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard, font=("Arial", 18), bg="#FFA500", fg="white", borderwidth=2, relief="raised")
        self.leaderboard_button.pack(pady=20)

    def start_quiz(self):
        self.title_label.destroy()
        self.start_button.destroy()
        self.load_question()

    def load_question(self):
        if self.current_question < len(quiz_data):
            self.time_left = 10
            self.question_data = quiz_data[self.current_question]
            self.question_label = tk.Label(self.root, text=self.question_data['question'], font=("Arial", 18), bg="#f0f0f0")
            self.question_label.pack(pady=20)

            self.option_buttons = []
            for i, option in enumerate(self.question_data['options']):
                btn = tk.Button(self.root, text=option, font=("Arial", 14), command=lambda i=i: self.check_answer(i), bg="#4CAF50", fg="white", borderwidth=2, relief="raised")
                btn.pack(pady=5)
                self.option_buttons.append(btn)

            # Timer label
            self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left} seconds", font=("Arial", 14), bg="#f0f0f0")
            self.timer_label.pack(pady=10)
            self.update_timer()

        else:
            self.show_score()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.check_answer(-1) # Time up!

    def check_answer(self, selected_option):
        # Disable all option buttons
        for btn in self.option_buttons:
            btn.config(state="disabled")

        # Check the answer
        correct_option = self.question_data['answer']
        if selected_option == correct_option:
            self.score += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showwarning("Incorrect!", f"Wrong answer. The correct answer was: {self.question_data['options'][correct_option]}")

        # Move to the next question after a brief pause
        self.root.after(1000, self.next_question) # Wait for 1 second before loading the next question

    def next_question(self):
        # Clean up the current question display
        self.timer_label.destroy()
        self.question_label.destroy()
        for btn in self.option_buttons:
            btn.destroy()

        self.current_question += 1
        self.load_question()

    def show_score(self):
        name = simpledialog.askstring("Name", "Enter your name:")
        if name:
            save_score(name, self.score)
            messagebox.showinfo("Quiz Completed", f"Your final score is: {self.score}/{len(quiz_data)}")
        self.root.quit()

    def show_leaderboard(self):
        top_scores = get_top_scores()
        leaderboard_str = "Leaderboard:\n\n"
        for i, (name, score) in enumerate(top_scores):
            leaderboard_str += f"{i + 1}. {name} - {score}\n"
        messagebox.showinfo("Leaderboard", leaderboard_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()