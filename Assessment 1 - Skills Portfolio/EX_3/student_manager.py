import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Define color scheme for the application.
BG_COLOR = "#1a0b2e" 
CARD_COLOR = "#2d1b4e" 
FG_COLOR = "#f3e8ff" 
SECONDARY_FG = "#d8b4fe" 
ACCENT_COLOR = "#a855f7" 
HIGHLIGHT_COLOR = "#4c1d95" 
BUTTON_TEXT = "#FFFFFF" 

COLOR_BLUE = "#0A84FF"
COLOR_GREEN = "#30D158"
COLOR_ORANGE = "#FF9F0A"
COLOR_RED = "#FF453A"

FONT_MAIN = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_HEADER = ("Helvetica", 13, "bold")

class Student:
    # Represents a student with personal details and academic marks
    # Stores code, name, three course marks, and exam mark
    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        self.code = code
        self.name = name
        self.course_marks = [mark1, mark2, mark3]
        self.exam_mark = exam_mark
        
    def get_total_coursework(self):
        return sum(self.course_marks)
    
    def get_overall_total(self):
        return self.get_total_coursework() + self.exam_mark
    
    def get_percentage(self):
        total = self.get_overall_total()
        return (total / 160) * 100
    
    def get_grade(self):
        percentage = self.get_percentage()
        if percentage >= 70: return 'A'
        elif percentage >= 60: return 'B'
        elif percentage >= 50: return 'C'
        elif percentage >= 40: return 'D'
        else: return 'F'

    def __str__(self):
        return f"{self.name} ({self.code})"

class StudentManagerApp:
    # Main application class that manages the GUI and student data
    # Handles window setup, UI creation, data loading, and user interactions
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)
        self.root.minsize(700, 480)
        
        self.students = []
        
        self.setup_styles()
        self.create_header()
        self.create_menu()
        self.create_data_view()
        self.create_status_bar()
        
        self.load_data()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure the appearance of the Treeview list widget.
        style.configure("Treeview", 
                background=BG_COLOR, 
                foreground=FG_COLOR, 
                fieldbackground=BG_COLOR,
                font=FONT_MAIN,
                rowheight=30,
                borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background=BG_COLOR, 
                        foreground=SECONDARY_FG, 
                        font=FONT_HEADER,
                        borderwidth=0)
        
        style.map("Treeview", 
                  background=[('selected', HIGHLIGHT_COLOR)],
                  foreground=[('selected', FG_COLOR)])
        
        # Remove visual borders for a cleaner look
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(8, 6), padx=12)
        
        title_label = tk.Label(header_frame, 
                               text="Student Manager", 
                               font=("Helvetica", 18, "bold"), 
                               bg=BG_COLOR, 
                               fg=FG_COLOR,
                               anchor="w")
        title_label.pack(fill=tk.X)

    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg=BG_COLOR)
        menu_frame.pack(pady=6, padx=12, fill=tk.X)
        def create_btn(text, command, color):
            # Helper function to create styled buttons with consistent appearance
            btn = tk.Button(menu_frame, 
                            text=text, 
                            command=command,
                            bg=CARD_COLOR,  # Dark card style background
                            fg=color,       # Colored text distinguishes action buttons
                            activebackground=HIGHLIGHT_COLOR,
                            activeforeground=color,
                            font=FONT_BOLD,
                            relief=tk.FLAT,
                            bd=0,
                            pady=12,
                            cursor="hand2")
            return btn

        # Arrange buttons in a grid with equal widths
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.columnconfigure(1, weight=1)
        menu_frame.columnconfigure(2, weight=1)
        menu_frame.columnconfigure(3, weight=1)

        create_btn("View All", self.view_all_records, COLOR_BLUE).grid(row=0, column=0, sticky="ew", padx=5)
        create_btn("Find", self.view_individual_record, COLOR_GREEN).grid(row=0, column=1, sticky="ew", padx=5)
        create_btn("Highest", self.show_highest_score, COLOR_ORANGE).grid(row=0, column=2, sticky="ew", padx=5)
        create_btn("Lowest", self.show_lowest_score, COLOR_RED).grid(row=0, column=3, sticky="ew", padx=5)

    def create_data_view(self):
        # Build the Treeview table that displays student records
        # Create a container frame to hold the student list
        list_container = tk.Frame(self.root, bg=BG_COLOR)
        list_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Add a thin separator line above the table for visual distinction
        tk.Frame(list_container, bg=HIGHLIGHT_COLOR, height=1).pack(fill=tk.X, pady=(0, 10))

        columns = ("code", "name", "coursework", "exam", "percentage", "grade")
        self.tree = ttk.Treeview(list_container, columns=columns, show="headings", selectmode="browse")
        
        # Define table columns with left-aligned text and center-aligned numbers
        self.tree.heading("code", text="ID", anchor=tk.W)
        self.tree.heading("name", text="Name", anchor=tk.W)
        self.tree.heading("coursework", text="Coursework", anchor=tk.CENTER)
        self.tree.heading("exam", text="Exam", anchor=tk.CENTER)
        self.tree.heading("percentage", text="%", anchor=tk.CENTER)
        self.tree.heading("grade", text="Grade", anchor=tk.CENTER)
        
        self.tree.column("code", width=80, anchor=tk.W)
        self.tree.column("name", width=200, anchor=tk.W)
        self.tree.column("coursework", width=100, anchor=tk.CENTER)
        self.tree.column("exam", width=80, anchor=tk.CENTER)
        self.tree.column("percentage", width=80, anchor=tk.CENTER)
        self.tree.column("grade", width=60, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        # Create a status bar at the bottom to display application status messages
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(self.root, 
                              textvariable=self.status_var, 
                              bd=0, 
                              anchor=tk.W,
                              bg=BG_COLOR,
                              fg=SECONDARY_FG,
                              font=("Helvetica", 10),
                              pady=10,
                              padx=20)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        self.status_var.set(message)

    def load_data(self):
        self.update_status("Loading...")
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "studentMarks.txt")

            # Create template file if it doesn't exist to prevent file not found errors
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as wf:
                    wf.write("0\n")

            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if not lines:
                    self.update_status("No data")
                    return

                try:
                    num_students = int(lines[0].strip())
                except Exception:
                    num_students = None

                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        code = parts[0].strip()
                        name = parts[1].strip()
                        try:
                            m1 = int(parts[2])
                            m2 = int(parts[3])
                            m3 = int(parts[4])
                            exam = int(parts[5])
                            student = Student(code, name, m1, m2, m3, exam)
                            self.students.append(student)
                        except ValueError: pass
                            
            self.update_status(f"{len(self.students)} Students")
            self.view_all_records()
            
        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_student_into_tree(self, student):
        self.tree.insert("", tk.END, values=(
            student.code,
            student.name,
            student.get_total_coursework(),
            student.exam_mark,
            f"{student.get_percentage():.1f}%",  # Format percentage to one decimal for readability
            student.get_grade()
        ))

    def view_all_records(self):
        # Display all student records in the table
        self.clear_tree()
        if not self.students:
            return
        for student in self.students:
            self.insert_student_into_tree(student)
        self.update_status(f"All Records ({len(self.students)})")

    def view_individual_record(self):
        search_term = simpledialog.askstring("Find", "Name or ID:")
        if search_term:
            self.clear_tree()
            found = 0
            for student in self.students:
                if search_term.lower() in student.name.lower() or search_term == student.code:
                    self.insert_student_into_tree(student)
                    found += 1
            self.update_status(f"Found {found} matches")
            if found == 0: self.view_all_records()

    def show_highest_score(self):
        # Find and display the student with the highest overall score
        if not self.students:
            return
        max_score = max(s.get_overall_total() for s in self.students)
        self.clear_tree()
        for student in self.students:
            if student.get_overall_total() == max_score:
                self.insert_student_into_tree(student)
        self.update_status(f"Highest Score: {max_score}")

    def show_lowest_score(self):
        # Find and display the student with the lowest overall score
        if not self.students:
            return
        min_score = min(s.get_overall_total() for s in self.students)
        self.clear_tree()
        for student in self.students:
            if student.get_overall_total() == min_score:
                self.insert_student_into_tree(student)
        self.update_status(f"Lowest Score: {min_score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
