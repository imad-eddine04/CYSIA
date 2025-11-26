import tkinter as tk
from tkinter import messagebox

ques = [
    {
        "question": "What is my name?",
        "options": ["Amine", "Abdessamie", "Abdelouahab"],
        "answer": 1
    },
    {
        "question": "What is my age?",
        "options": [18, 21, 100],
        "answer": 2
    },
    {
        "question": "What is my favorite color?",
        "options": ["Green", "Blue", "Black"],
        "answer": 3
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Osaka", "Kyoto", "Nara", "Tokyo"],
        "answer": 4
    },
    {
        "question": "Who invented the light bulb?",
        "options": ["Nikola Tesla", "Thomas Edison", "Menad"],
        "answer": 2
    },
]


class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        master.title("Test QCM 🧠")
        master.geometry("450x300")

        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.selected_option = tk.IntVar()

        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=('Arial', 12, 'bold'))
        self.score_label.pack(pady=5)

        self.question_text = tk.StringVar()
        self.question_label = tk.Label(master, textvariable=self.question_text, wraplength=400, font=('Arial', 14))
        self.question_label.pack(pady=10)

        self.options_frame = tk.Frame(master)
        self.options_frame.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit Answer", command=self.check_answer, font=('Arial', 12),
                                       bg='lightblue')
        self.submit_button.pack(pady=10)

        self.display_question()

    def display_question(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        q_data = self.questions[self.current_question_index]
        self.question_text.set(f"Q{self.current_question_index + 1}: {q_data['question']}")

        self.selected_option.set(0)

        for index, option in enumerate(q_data['options']):
            rb = tk.Radiobutton(self.options_frame, text=option, variable=self.selected_option,
                                value=index + 1, font=('Arial', 10))
            rb.pack(anchor='w', padx=20)

    def check_answer(self):
        user_answer = self.selected_option.get()
        correct_answer = self.questions[self.current_question_index]['answer']

        if user_answer == 0:
            messagebox.showwarning("Warning", "Please select an option first!")
            return

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "✅ Correct!")
        else:
            if self.score > 0:
                self.score -= 1
            messagebox.showinfo("Result", "❌ Incorrect!")

        self.score_label.config(text=f"Score: {self.score}")

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        self.submit_button.config(state=tk.DISABLED)
        self.question_label.pack_forget()
        self.options_frame.pack_forget()

        final_message = f"Quiz Finished!\nYour final score is: {self.score} out of {len(self.questions)}"
        self.final_label = tk.Label(self.master, text=final_message, font=('Arial', 16, 'bold'), fg='green')
        self.final_label.pack(pady=50)


if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root, ques)
    root.mainloop()