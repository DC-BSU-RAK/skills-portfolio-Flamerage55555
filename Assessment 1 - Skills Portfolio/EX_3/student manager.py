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

        create_btn("View All", self.view_all_records, COLOR_BLUE).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        create_btn("Find", self.view_individual_record, COLOR_GREEN).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        create_btn("Highest", self.show_highest_score, COLOR_ORANGE).grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        create_btn("Lowest", self.show_lowest_score, COLOR_RED).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        # Row 2
        create_btn("Sort", self.sort_records, "#A855F7").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        create_btn("Add", self.add_record, "#EC4899").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        create_btn("Delete", self.delete_record, "#EF4444").grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        create_btn("Update", self.update_record, "#3B82F6").grid(row=1, column=3, sticky="ew", padx=5, pady=5)

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

    def save_data(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "studentMarks.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s.code},{s.name},{s.course_marks[0]},{s.course_marks[1]},{s.course_marks[2]},{s.exam_mark}\n")
            self.update_status("Data Saved Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data: {e}")

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

    def sort_records(self):
        # Ask user for sort order
        choice = messagebox.askyesno("Sort Students", "Sort by Overall Score?\nYes: Ascending\nNo: Descending")
        # Note: askyesno returns True for Yes (Ascending), False for No (Descending). 
        # But we want to confirm if they cancelled? No, askyesno is binary. 
        # Let's assume Yes=Ascending, No=Descending for now as per simple requirement.
        
        reverse_sort = not choice  # If choice is True (Asc), reverse is False.
        
        self.students.sort(key=lambda s: s.get_overall_total(), reverse=reverse_sort)
        self.view_all_records()
        order = "Ascending" if not reverse_sort else "Descending"
        self.update_status(f"Sorted by Score ({order})")

    def add_record(self):
        # Create a dialog to add a new student
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("400x450")
        add_window.configure(bg=BG_COLOR)
        
        fields = ["Student ID", "Name", "Course 1 Mark", "Course 2 Mark", "Course 3 Mark", "Exam Mark"]
        entries = {}

        for i, field in enumerate(fields):
            lbl = tk.Label(add_window, text=field, bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN)
            lbl.pack(pady=(10, 5), padx=20, anchor='w')
            entry = tk.Entry(add_window, font=FONT_MAIN)
            entry.pack(pady=0, padx=20, fill='x')
            entries[field] = entry

        def submit():
            try:
                code = entries["Student ID"].get().strip()
                name = entries["Name"].get().strip()
                m1 = int(entries["Course 1 Mark"].get())
                m2 = int(entries["Course 2 Mark"].get())
                m3 = int(entries["Course 3 Mark"].get())
                exam = int(entries["Exam Mark"].get())
                
                if not code or not name:
                    raise ValueError("ID and Name cannot be empty")
                
                # Check for duplicate ID
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Error", "Student ID already exists!")
                    return

                new_student = Student(code, name, m1, m2, m3, exam)
                self.students.append(new_student)
                self.save_data()
                self.view_all_records()
                add_window.destroy()
                messagebox.showinfo("Success", "Student added successfully")
                
            except ValueError as e:
                messagebox.showerror("Invalid Input", f"Please check your inputs.\nMarks must be integers.\n{e}")

        save_btn = tk.Button(add_window, text="Save Record", command=submit, 
                           bg=ACCENT_COLOR, fg="white", font=FONT_BOLD, relief=tk.FLAT, pady=10)
        save_btn.pack(pady=30, padx=20, fill='x')

    def delete_record(self):
        search_term = simpledialog.askstring("Delete Student", "Enter Name or ID to delete:")
        if not search_term: return

        # Find potential matches
        matches = [s for s in self.students if search_term.lower() in s.name.lower() or search_term == s.code]
        
        if not matches:
            messagebox.showinfo("Not Found", "No matching student found.")
            return
        
        # If multiple matches or one, confirm deletion. 
        # For simplicity, if multiple, we'll ask user to be more specific or delete the first one?
        # A robust solution lists them. Let's try to delete the first match but warn if multiple.
        
        target = matches[0]
        if len(matches) > 1:
            if not messagebox.askokcancel("Multiple Matches", f"Found {len(matches)} matches. Deleting: {target}\nProceed?"):
                return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {target}?"):
            self.students.remove(target)
            self.save_data()
            self.view_all_records()
            self.update_status(f"Deleted {target.name}")

    def update_record(self):
        search_term = simpledialog.askstring("Update Student", "Enter Name or ID to update:")
        if not search_term: return

        matches = [s for s in self.students if search_term.lower() in s.name.lower() or search_term == s.code]
        
        if not matches:
            messagebox.showinfo("Not Found", "No matching student found.")
            return

        student = matches[0] # Pick first match
        
        # Sub-menu window for updates
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update {student.name}")
        update_window.geometry("300x400")
        update_window.configure(bg=BG_COLOR)
        
        tk.Label(update_window, text=f"Update: {student.name}", bg=BG_COLOR, fg=SECONDARY_FG, font=FONT_HEADER).pack(pady=10)

        def update_attr(attr_name, is_int=False, is_list_idx=None):
            # Helper to ask for value and update
            current_val = getattr(student, attr_name)
            if is_list_idx is not None:
                current_val = student.course_marks[is_list_idx]
                
            new_val = simpledialog.askstring("Update", f"Enter new {attr_name}:", initialvalue=str(current_val), parent=update_window)
            
            if new_val is not None:
                try:
                    if is_int:
                        val = int(new_val)
                    else:
                        val = new_val
                    
                    if is_list_idx is not None:
                        student.course_marks[is_list_idx] = val
                    else:
                        setattr(student, attr_name, val)
                    
                    self.save_data()
                    self.view_all_records()
                    messagebox.showinfo("Success", "Record updated")
                    
                except ValueError:
                    messagebox.showerror("Error", "Invalid input format")

        # Buttons for each field
        tk.Button(update_window, text="Update Name", command=lambda: update_attr('name'), width=25).pack(pady=5)
        tk.Button(update_window, text="Update ID", command=lambda: update_attr('code'), width=25).pack(pady=5)
        tk.Button(update_window, text="Update Course Mark 1", command=lambda: update_attr('course_marks', True, 0), width=25).pack(pady=5)
        tk.Button(update_window, text="Update Course Mark 2", command=lambda: update_attr('course_marks', True, 1), width=25).pack(pady=5)
        tk.Button(update_window, text="Update Course Mark 3", command=lambda: update_attr('course_marks', True, 2), width=25).pack(pady=5)
        tk.Button(update_window, text="Update Exam Mark", command=lambda: update_attr('exam_mark', True), width=25).pack(pady=5)
        
        tk.Button(update_window, text="Done", command=update_window.destroy, bg=ACCENT_COLOR, fg='white').pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
