import tkinter as tk
import random
import os
from typing import Tuple

# --- Color Palette ---
COLOR_BG_MAIN = "#FFFAF0"       # Floral White
COLOR_FRAME_BG = "#FFFFFF"      # White
COLOR_PRIMARY = "#FF6B6B"       # Pastel Red
COLOR_SECONDARY = "#4ECDC4"     # Medium Turquoise
COLOR_ACCENT = "#FFE66D"        # Pastel Yellow
COLOR_TEXT_MAIN = "#2C3E50"     # Dark Blue Grey
COLOR_TEXT_ACCENT = "#1A535C"   # Dark Cyan
COLOR_BTN_HOVER = "#FF8E8E"     # Lighter Red for hover

class JokeApp:
    def __init__(self, root_window: tk.Tk):
        self.root_window = root_window
        self.root_window.title("Ultimate Joke Teller")
        self.root_window.geometry("600x750")
        self.root_window.resizable(False, False)
        self.root_window.configure(bg=COLOR_BG_MAIN)

        # Data holders
        self.current_joke_setup = ""
        self.current_joke_punchline = ""

        # Setup UI
        self.setup_ui()
        
        # Load first joke
        self.fetch_new_content()

    def setup_ui(self):
        # --- Main Container ---
        # Using a colorful border
        self.main_frame = tk.Frame(self.root_window, bg=COLOR_FRAME_BG, bd=0, highlightbackground=COLOR_SECONDARY, highlightthickness=4)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=520, height=650)

        # --- Title ---
        title_label = tk.Label(self.main_frame, text="✨ Ultimate Joke Teller ✨", font=("Comic Sans MS", 24, "bold"), bg=COLOR_FRAME_BG, fg=COLOR_PRIMARY)
        title_label.pack(pady=20)

        # --- Joke Setup ---
        self.setup_label = tk.Label(self.main_frame, text="Fetching a joke...", wraplength=450, font=("Verdana", 14), bg=COLOR_FRAME_BG, fg=COLOR_TEXT_MAIN)
        self.setup_label.pack(pady=20, padx=15)

        # --- Joke Punchline ---
        self.punchline_label = tk.Label(self.main_frame, text="", wraplength=450, font=("Verdana", 14, "bold italic"), bg=COLOR_FRAME_BG, fg=COLOR_SECONDARY)
        self.punchline_label.pack(pady=10, padx=15)

        # --- Controls ---
        btn_frame = tk.Frame(self.main_frame, bg=COLOR_FRAME_BG)
        btn_frame.pack(pady=30)

        # Helper to create styled buttons
        def create_hover_button(parent, text, command, bg_color, hover_color, fg_color="white"):
            btn = tk.Button(
                parent, 
                text=text, 
                command=command, 
                bg=bg_color, 
                fg=fg_color, 
                font=("Comic Sans MS", 12, "bold"), 
                relief=tk.FLAT, 
                padx=20, 
                pady=10,
                activebackground=hover_color,
                activeforeground=fg_color,
                cursor="hand2"
            )
            # Bind hover events
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
            return btn

        # Show Punchline Button
        self.btn_punchline = create_hover_button(btn_frame, "Show Punchline 🎭", self.reveal_punchline, COLOR_SECONDARY, "#45b7af")
        self.btn_punchline.grid(row=0, column=0, padx=10)
        self.btn_punchline.config(state=tk.DISABLED)

        # Next Joke Button
        self.btn_next = create_hover_button(btn_frame, "Next Joke ➡️", self.fetch_new_content, COLOR_PRIMARY, COLOR_BTN_HOVER)
        self.btn_next.grid(row=0, column=1, padx=10)

        # Quit Button 
        quit_btn = tk.Button(self.root_window, text="Quit", command=self.root_window.destroy, bg="#ff4d4d", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2")
        quit_btn.place(relx=0.99, rely=0.99, anchor=tk.SE)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#cc0000"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg="#ff4d4d"))

    def fetch_new_content(self):
        """Grabs a fresh joke from the stash instantly🤞"""
        # Get the joke directly
        setup, punchline = self.get_joke()
        
        # Update data
        self.current_joke_setup = setup
        self.current_joke_punchline = punchline
        
        # Update UI
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.btn_punchline.config(state=tk.NORMAL, cursor="hand2")

    def get_joke(self) -> Tuple[str, str]:
        """Picks a random joke from our secret text file stash🤞"""  
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "resources", "randomJokes.txt")
            with open(path, "r", encoding="utf-8") as f:
                raw_lines = [ln.rstrip("\n") for ln in f.readlines()]

            # Normalize and collect non-empty lines
            lines = [ln.strip() for ln in raw_lines]

            jokes = []  # list of (setup, punchline)
            i = 0
            while i < len(lines):
                line = lines[i]
                if not line:
                    i += 1
                    continue

                # Case 1: setup and punchline on same line separated by '?'
                if "?" in line:
                    parts = line.split("?", 1)
                    setup = parts[0].strip() + "?"
                    punch = parts[1].strip()

                    # If punch is empty, try to take next non-empty line as punchline
                    if not punch and i + 1 < len(lines) and lines[i + 1]:
                        punch = lines[i + 1].strip()
                        i += 1

                    jokes.append((setup, punch))

                else:
                    # Case 2: two-line joke where setup doesn't include '?'
                    # Treat current line as setup and next non-empty line as punchline
                    if i + 1 < len(lines) and lines[i + 1]:
                        setup = line
                        punch = lines[i + 1].strip()
                        jokes.append((setup, punch))
                        i += 1

                i += 1

            if jokes:
                setup, punch = random.choice(jokes)
                return setup, punch
        except Exception:
            pass

        return "Why did the developer go broke?", "Because he used up all his cache!"

    def reveal_punchline(self):
        """The moment of truth! Shows the punchline."""
        self.punchline_label.config(text=self.current_joke_punchline)
        self.btn_punchline.config(state=tk.DISABLED, cursor="arrow")


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
