import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Arithmetic Quiz Master")
        
        # Make window responsive
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        # Start maximized on launch to avoid hidden controls on small screens/DPI
        try:
            self.root.state('zoomed')
        except Exception:
            pass
        
        # Configure root grid to be responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Modern color scheme
        self.colors = {
            'primary': '#6366f1',      # Indigo
            'secondary': '#8b5cf6',    # Purple
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'dark': '#1f2937',         # Dark gray
            'light': '#f9fafb',        # Light gray
            'white': '#ffffff',
            'text': '#111827'
        }
        
        # Configure root background with gradient effect
        self.root.configure(bg=self.colors['light'])
        
        # Quiz state variables
        self.difficulty = None
        self.score = 0
        self.question_count = 0
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operation = ''
        self.correct_answer = 0
        self.attempts = 0
        
        # Animation variables
        self.animation_id = None
        
        # Start with menu
        self.displayMenu()
    
    def create_gradient_frame(self, parent):
        """Create a frame with gradient-like appearance"""
        frame = tk.Frame(parent, bg=self.colors['light'])
        return frame
    
    def create_modern_button(self, parent, text, command, bg_color, width=20):
        """Create a modern styled button with hover effect"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 12, 'bold'),
            bg=bg_color,
            fg='white',
            activebackground=self.adjust_color(bg_color, -20),
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            width=width,
            height=1,
            borderwidth=0,
            padx=8,
            pady=6
        )
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.adjust_color(bg_color, -20)))
        btn.bind('<Leave>', lambda e: btn.config(bg=bg_color))
        
        return btn
    
    def adjust_color(self, color, amount):
        """Adjust color brightness for hover effects"""
        # Simple color adjustment (darkening)
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def displayMenu(self):
        """Display the difficulty level menu with modern design"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reset quiz state
        self.score = 0
        self.question_count = 0
        
        # Main container with responsive grid
        main_frame = self.create_gradient_frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Top spacer
        tk.Frame(main_frame, bg=self.colors['light']).grid(row=0, column=0)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.grid(row=1, column=0, sticky='n')
        
        # Animated title with emoji
        title_label = tk.Label(
            content_frame,
            text="🎯 ARITHMETIC QUIZ",
            font=('Segoe UI', 36, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['primary']
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            content_frame,
            text="Test Your Math Skills!",
            font=('Segoe UI', 14),
            bg=self.colors['light'],
            fg=self.colors['text']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Difficulty card
        card_frame = tk.Frame(
            content_frame,
            bg='white',
            relief='flat',
            borderwidth=0
        )
        card_frame.pack(pady=16, padx=20, fill='x')
        
        # Add shadow effect simulation
        shadow_frame = tk.Frame(content_frame, bg='#e5e7eb', height=2)
        shadow_frame.place(in_=card_frame, relx=0.02, rely=1, relwidth=0.96)
        
        # Card header
        header_label = tk.Label(
            card_frame,
            text="🎮 SELECT DIFFICULTY LEVEL",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        header_label.pack(pady=(30, 20))
        
        # Buttons container
        btn_container = tk.Frame(card_frame, bg='white')
        btn_container.pack(pady=(10, 30), padx=30)
        
        # Difficulty buttons with icons and descriptions
        difficulties = [
            ("🟢 EASY", "Single Digit Numbers", self.colors['success'], 1),
            ("🟡 MODERATE", "Double Digit Numbers", self.colors['warning'], 2),
            ("🔴 ADVANCED", "4-Digit Numbers", self.colors['danger'], 3)
        ]
        
        for text, desc, color, level in difficulties:
            btn_frame = tk.Frame(btn_container, bg='white')
            btn_frame.pack(pady=8, fill='x')
            
            btn = self.create_modern_button(
                btn_frame,
                f"{text}\n{desc}",
                lambda l=level: self.startQuiz(l),
                color,
                width=25
            )
            btn.pack()
        
        # Bottom spacer
        tk.Frame(main_frame, bg=self.colors['light']).grid(row=2, column=0)
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="💡 Answer 10 questions • Get up to 100 points!",
            font=('Segoe UI', 10),
            bg=self.colors['light'],
            fg='#6b7280'
        )
        footer_label.grid(row=2, column=0, sticky='s', pady=(0, 20))
    
    def randomInt(self, difficulty):
        """Generate random integers based on difficulty level"""
        if difficulty == 1:  # Easy: 1-9
            return random.randint(1, 9)
        elif difficulty == 2:  # Moderate: 10-99
            return random.randint(10, 99)
        else:  # Advanced: 1000-9999
            return random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide between addition and subtraction"""
        return random.choice(['+', '-'])
    
    def startQuiz(self, difficulty):
        """Start the quiz with selected difficulty"""
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.displayProblem()
    
    def displayProblem(self):
        """Display a new problem with modern design"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Check if quiz is complete
        if self.question_count >= 10:
            self.displayResults()
            return
        
        # Generate new problem
        self.current_num1 = self.randomInt(self.difficulty)
        self.current_num2 = self.randomInt(self.difficulty)
        self.current_operation = self.decideOperation()
        
        # Calculate correct answer
        if self.current_operation == '+':
            self.correct_answer = self.current_num1 + self.current_num2
        else:
            self.correct_answer = self.current_num1 - self.current_num2
        
        self.attempts = 0
        
        # Main container
        main_frame = self.create_gradient_frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar container
        progress_container = tk.Frame(main_frame, bg=self.colors['light'])
        progress_container.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        # Progress info
        progress_frame = tk.Frame(progress_container, bg=self.colors['light'])
        progress_frame.pack(fill='x')
        
        question_label = tk.Label(
            progress_frame,
            text=f"Question {self.question_count + 1} of 10",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['text']
        )
        question_label.pack(side='left')
        
        score_label = tk.Label(
            progress_frame,
            text=f"Score: {self.score} pts",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['primary']
        )
        score_label.pack(side='right')
        
        # Visual progress bar
        progress_bg = tk.Frame(progress_container, bg='#e5e7eb', height=8)
        progress_bg.pack(fill='x', pady=(10, 0))
        
        progress_fill = tk.Frame(
            progress_bg,
            bg=self.colors['primary'],
            height=8
        )
        progress_width = (self.question_count / 10)
        progress_fill.place(relx=0, rely=0, relwidth=progress_width, relheight=1)
        
        # Problem card
        problem_card = tk.Frame(main_frame, bg='white', relief='flat')
        problem_card.grid(row=1, column=0, sticky='n', pady=20)
        
        # Problem display with large text
        problem_container = tk.Frame(problem_card, bg='white')
        problem_container.pack(pady=30, padx=30)
        
        # Operation symbol styling
        op_color = self.colors['success'] if self.current_operation == '+' else self.colors['danger']
        
        problem_label = tk.Label(
            problem_container,
            text=f"{self.current_num1}  {self.current_operation}  {self.current_num2}  =",
            font=('Segoe UI', 48, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        problem_label.pack(pady=20)
        
        # Answer input section
        input_frame = tk.Frame(problem_card, bg='white')
        input_frame.pack(pady=(20, 40))
        
        answer_label = tk.Label(
            input_frame,
            text="Your Answer:",
            font=('Segoe UI', 14),
            bg='white',
            fg=self.colors['text']
        )
        answer_label.pack(pady=(0, 10))
        
        # Styled entry
        entry_container = tk.Frame(input_frame, bg='white')
        entry_container.pack()
        
        self.answer_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 24, 'bold'),
            width=12,
            justify='center',
            relief='solid',
            borderwidth=2,
            fg=self.colors['text']
        )
        self.answer_entry.pack(ipady=10)
        self.answer_entry.focus()
        
        # Entry focus effects
        self.answer_entry.bind('<FocusIn>', lambda e: self.answer_entry.config(borderwidth=3))
        self.answer_entry.bind('<FocusOut>', lambda e: self.answer_entry.config(borderwidth=2))
        
        # Bind Enter key
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        # Submit button
        submit_btn = self.create_modern_button(
            problem_card,
            "✓ SUBMIT ANSWER",
            self.checkAnswer,
            self.colors['primary'],
            width=20
        )
        submit_btn.pack(pady=(20, 30))
        
        # Feedback label
        self.feedback_label = tk.Label(
            problem_card,
            text="",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            height=2
        )
        self.feedback_label.pack(pady=(0, 20))
    
    def checkAnswer(self):
        """Check if the user's answer is correct with animations"""
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(
                text="⚠️ Please enter a valid number!",
                fg=self.colors['warning']
            )
            self.shake_widget(self.answer_entry)
            return
        
        if self.isCorrect(user_answer):
            # Correct answer
            if self.attempts == 0:
                self.score += 10
                self.feedback_label.config(
                    text="✓ CORRECT! +10 points",
                    fg=self.colors['success']
                )
            else:
                self.score += 5
                self.feedback_label.config(
                    text="✓ CORRECT! +5 points",
                    fg=self.colors['success']
                )
            
            self.question_count += 1
            self.root.after(1200, self.displayProblem)
        else:
            # Wrong answer
            self.attempts += 1
            if self.attempts < 2:
                self.feedback_label.config(
                    text="✗ Incorrect. Try one more time!",
                    fg=self.colors['danger']
                )
                self.shake_widget(self.answer_entry)
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                self.feedback_label.config(
                    text=f"✗ Incorrect. The answer was {self.correct_answer}",
                    fg=self.colors['danger']
                )
                self.question_count += 1
                self.root.after(2500, self.displayProblem)
    
    def shake_widget(self, widget):
        """Animate widget with shake effect"""
        original_x = widget.winfo_x()
        
        def shake(count=0):
            if count < 4:
                offset = 5 if count % 2 == 0 else -5
                widget.place(x=original_x + offset)
                self.root.after(50, lambda: shake(count + 1))
            else:
                widget.pack()
        
        shake()
    
    def isCorrect(self, user_answer):
        """Check if the answer is correct"""
        return user_answer == self.correct_answer
    
    def displayResults(self):
        """Display final results with celebration design"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Calculate grade
        percentage = self.score
        if percentage >= 90:
            grade = "A+"
            emoji = "🏆"
            color = self.colors['success']
            message = "OUTSTANDING!"
        elif percentage >= 80:
            grade = "A"
            emoji = "⭐"
            color = self.colors['success']
            message = "EXCELLENT!"
        elif percentage >= 70:
            grade = "B"
            emoji = "👍"
            color = '#3b82f6'
            message = "GOOD JOB!"
        elif percentage >= 60:
            grade = "C"
            emoji = "👌"
            color = self.colors['warning']
            message = "NOT BAD!"
        elif percentage >= 50:
            grade = "D"
            emoji = "💪"
            color = self.colors['warning']
            message = "KEEP TRYING!"
        else:
            grade = "F"
            emoji = "📚"
            color = self.colors['danger']
            message = "PRACTICE MORE!"
        
        # Main container
        main_frame = self.create_gradient_frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Results card
        results_card = tk.Frame(main_frame, bg='white', relief='flat')
        results_card.grid(row=0, column=0, sticky='n')
        
        # Celebration emoji
        emoji_label = tk.Label(
            results_card,
            text=emoji,
            font=('Segoe UI', 72),
            bg='white'
        )
        emoji_label.pack(pady=(40, 20))
        
        # Message
        message_label = tk.Label(
            results_card,
            text=message,
            font=('Segoe UI', 28, 'bold'),
            bg='white',
            fg=color
        )
        message_label.pack(pady=(0, 30))
        
        # Score circle
        score_frame = tk.Frame(results_card, bg=color, width=200, height=200)
        score_frame.pack(pady=20)
        score_frame.pack_propagate(False)
        
        score_label = tk.Label(
            score_frame,
            text=f"{self.score}",
            font=('Segoe UI', 56, 'bold'),
            bg=color,
            fg='white'
        )
        score_label.pack(expand=True)
        
        points_label = tk.Label(
            score_frame,
            text="POINTS",
            font=('Segoe UI', 12, 'bold'),
            bg=color,
            fg='white'
        )
        points_label.place(relx=0.5, rely=0.75, anchor='center')
        
        # Grade
        grade_label = tk.Label(
            results_card,
            text=f"Grade: {grade}",
            font=('Segoe UI', 32, 'bold'),
            bg='white',
            fg=color
        )
        grade_label.pack(pady=(30, 10))
        
        # Out of 100
        total_label = tk.Label(
            results_card,
            text="out of 100",
            font=('Segoe UI', 14),
            bg='white',
            fg='#6b7280'
        )
        total_label.pack(pady=(0, 40))
        
        # Action buttons
        button_frame = tk.Frame(results_card, bg='white')
        button_frame.pack(pady=(20, 40))
        
        play_again_btn = self.create_modern_button(
            button_frame,
            "🔄 PLAY AGAIN",
            self.displayMenu,
            self.colors['primary'],
            width=18
        )
        play_again_btn.grid(row=0, column=0, padx=10)
        
        quit_btn = self.create_modern_button(
            button_frame,
            "✕ QUIT",
            self.root.quit,
            '#6b7280',
            width=18
        )
        quit_btn.grid(row=0, column=1, padx=10)

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()