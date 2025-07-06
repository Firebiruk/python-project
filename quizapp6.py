from tkinter import*
from tkinter import messagebox
import random
import json
import os
import datetime

login_frame = None
update_frame = None
quiz_frame = None
home_frame = None
header_frame = None
signup_file = "signup.json"
header_frame = None
nav_labels = {}
quizzes_file = "questions.json"
quiz_subjects = [
    {"name": "ICT", "emoji": "💻", "color": "#00FFFF"},  # Bright Cyan
    {"name": "Mathematics", "emoji": "➗", "color": "#FF00FF"},  # Bright Magenta
    {"name": "Physics", "emoji": "🧲", "color": "#FFFF00"},  # Bright Yellow
    {"name": "Biology", "emoji": "🧬", "color": "#00FF00"},  # Bright Green
    {"name": "Chemistry", "emoji": "⚗️", "color": "#FF0000"},  # Bright Red
    {"name": "History", "emoji": "📜", "color": "#FFA500"},  # Bright Orange
    {"name": "Geography", "emoji": "🌍", "color": "#9400D3"},  # Bright Violet
]
quiz_page_index = 0
quizzes_per_page = 3

window = Tk()
window.title("QuizApp")
window.geometry("800x600")
window.config(bg="white")

def load_users():
    if not os.path.exists(signup_file):
        return {}
    with open(signup_file, "r") as f:
        return json.load(f)

def save_users(users):
    with open(signup_file, "w") as f:
        json.dump(users, f)

def sign_up(username, password):
    users = load_users()
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return False
    
    # Initialize user with empty progress data
    users[username] = {
        "password": password,
        "is_admin": False,
        "progress": {
            "quizzes_taken": 0,
            "total_score": 0,
            "average_score": 0,
            "perfect_scores": 0
        },
        "history": []
    }
    
    save_users(users)
    messagebox.showinfo("Success", "Sign up successful! You can now log in.")
    return True

def login(username, password):
    global current_user
    global current_is_admin

    users = load_users()
    if username not in users:
        messagebox.showerror("Error", "Username does not exist!")
        return False
    if users[username]["password"] != password:
        messagebox.showerror("Error", "Incorrect password!")
        return False
    current_user = username
    current_is_admin = users[username].get("is_admin", False)
    if current_is_admin:
        messagebox.showinfo("Admin Login", "Welcome, Admin!")
        home_page()
    else:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        home_page()
    return True

def set_active_nav(active):
    for name, label in nav_labels.items():
        if name == active:
            label.config(fg="#0298DD")
        else:
            label.config(fg="black")

def create_header():
    global header_frame, nav_labels
    if header_frame is not None and header_frame.winfo_exists():
        header_frame.destroy()
    header_frame = Frame(window, bg="white")
    header_frame.pack(side=TOP, fill=X)

    header_label = Label(header_frame, text="QuizApp", font=("Consolas", 25, "bold"), bg="white", fg="#0298DD")
    header_label.pack(side=LEFT, padx=20)

    nav_labels.clear()
    nav_labels["Settings"] = Label(header_frame, text="Settings", font=("Consolas", 15), bg="white", fg="black")
    nav_labels["Settings"].pack(side=RIGHT, padx=20)
    nav_labels["Settings"].bind("<Button-1>", lambda e: (set_active_nav("Settings"), settings_page()))

    nav_labels["About"] = Label(header_frame, text="About", font=("Consolas", 15), bg="white", fg="black")
    nav_labels["About"].pack(side=RIGHT, padx=20)
    nav_labels["About"].bind("<Button-1>", lambda e: (set_active_nav("About"), about_page()))

    nav_labels["Update"] = Label(header_frame, text="Update", font=("Consolas", 15), bg="white", fg="black")
    nav_labels["Update"].pack(side=RIGHT, padx=20)
    nav_labels["Update"].bind("<Button-1>", lambda e: (set_active_nav("Update"), update_page()))

    nav_labels["Quizzes"] = Label(header_frame, text="Quizzes", font=("Consolas", 15), bg="white", fg="black")
    nav_labels["Quizzes"].pack(side=RIGHT, padx=20)
    nav_labels["Quizzes"].bind("<Button-1>", lambda e: (set_active_nav("Quizzes"), quiz_page()))

    nav_labels["Home"] = Label(header_frame, text="Home", font=("Consolas", 15), bg="white", fg="black")
    nav_labels["Home"].pack(side=RIGHT, padx=20)
    nav_labels["Home"].bind("<Button-1>", lambda e: (set_active_nav("Home"), home_page()))

    if current_user:  # Only show history if logged in
        nav_labels["History"] = Label(header_frame, text="History", font=("Consolas", 15), bg="white", fg="black")
        nav_labels["History"].pack(side=RIGHT, padx=20)
        nav_labels["History"].bind("<Button-1>", lambda e: (set_active_nav("History"), view_full_history()))

def start_quiz(subject):
    global quiz_questions, quiz_index, quiz_score, quiz_subject, quiz_answers, quiz_time_left, quiz_timer_id, quiz_time_left
    if header_frame is not None and header_frame.winfo_exists():
        header_frame.destroy()
    quiz_subject = subject
    with open(quizzes_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    quiz_questions = data.get(subject, [])
    if not quiz_questions:
        messagebox.showinfo("No Questions", f"No questions found for {subject.title()}!")
        return
    quiz_index = 0
    quiz_score = 0
    quiz_answers = [None] * len(quiz_questions)
    quiz_time_left = len(quiz_questions) * 60
    show_question()
    start_timer()

def show_question():
    global quiz_frame, timer_label, back_btn, choice_btns, next_btn, finish_btn
    try:
        quiz_frame.destroy()
    except:
        pass

    quiz_frame = Frame(window, bg="white")
    quiz_frame.pack(fill=BOTH, expand=1)

    # Top bar: Back button (left), Timer (right)
    top_bar = Frame(quiz_frame, bg="white")
    top_bar.pack(fill=X, pady=10)
    back_btn = Button(top_bar, text="\u2190", font=("Consolas", 20, "bold"), fg="#0298DD", bg="white", borderwidth=2, relief="solid", command=on_quit_attempt)
    back_btn.pack(side=LEFT, padx=10)
    timer_label = Label(top_bar, text="", font=("Consolas", 16), bg="white", fg="#0298DD")
    timer_label.pack(side=RIGHT, padx=10)

    # Question
    q = quiz_questions[quiz_index]
    Label(quiz_frame, text=f"Q{quiz_index+1}: {q['Question']}", font=("Consolas", 18, "bold"), bg="white", wraplength=700).pack(pady=20)

    # Choices as buttons
    letters = ["A", "B", "C", "D"]
    choice_btns = []

    for i, choice in enumerate(q["Choices"]):
        outer_frame = Frame(quiz_frame, bg="white")
        outer_frame.pack(pady=6)

        wrapper = Frame(outer_frame, bg="#0298DD", padx=1, pady=1)
        wrapper.pack()

        inner_frame = Frame(wrapper, bg="white")
        inner_frame.pack()

        label_letter = Label(inner_frame, text=letters[i], font=("Consolas", 14, "bold"),
                             width=2, bg="#0298DD", fg="white")
        label_letter.pack(side=LEFT, padx=4, pady=2)

        btn = Button(inner_frame, text=choice, font=("Consolas", 13),
                     wraplength=400, anchor="w", justify="left", width=40,
                     bg="white", fg="black", relief="flat", borderwidth=0,
                     command=lambda idx=i: select_choice(idx))
        btn.pack(side=LEFT, fill="x", expand=True, padx=(0, 4), pady=2)

        choice_btns.append(btn)

    # Navigation buttons (bottom right)
    nav_frame = Frame(quiz_frame, bg="white")
    nav_frame.pack(side=BOTTOM, anchor="e", pady=20, padx=20)
    back_nav_btn = Button(nav_frame, text="\u2190 Back", font=("Consolas", 16), bg="white", fg="#0298DD", borderwidth=2, relief="solid", highlightbackground="#0298DD", command=go_back)
    back_nav_btn.pack(side=LEFT, padx=5)
    if quiz_index == len(quiz_questions) - 1:
        finish_btn = Button(nav_frame, text="Finish", font=("Consolas", 16), bg="#0298DD", fg="white", borderwidth=2, relief="solid", command=on_finish_attempt)
        finish_btn.pack(side=LEFT, padx=5)
        finish_btn.config(state="normal" if all(a is not None for a in quiz_answers) else "disabled")
    else:
        next_btn = Button(nav_frame, text="Next \u2192", font=("Consolas", 16), bg="#0298DD", fg="white", borderwidth=2, relief="solid", command=go_next)
        next_btn.pack(side=LEFT, padx=5)

def select_choice(idx):
    quiz_answers[quiz_index] = idx
    for i, btn in enumerate(choice_btns):
        if i == idx:
            btn.config(bg="#b3e6fa", highlightbackground="#0298DD", highlightcolor="#0298DD", highlightthickness=3)
        else:
            btn.config(bg="white", highlightbackground="#0298DD", highlightcolor="#0298DD", highlightthickness=1)
    if quiz_index == len(quiz_questions) - 1 and all(a is not None for a in quiz_answers):
        finish_btn.config(state="normal")

def go_back():
    global quiz_index
    if quiz_index > 0:
        quiz_index -= 1
        show_question()
    else:
        messagebox.showinfo("Info", "You are already at the first question.")
    
def go_next():
    global quiz_index
    if quiz_answers[quiz_index] is None:
        messagebox.showwarning("No selection", "Please select an answer.")
        return
    quiz_index += 1
    show_question()

def on_finish_attempt():
    stop_timer()
    if not all(a is not None for a in quiz_answers):
        messagebox.showinfo("Incomplete", "You still have some questions left.")
        return
    if quiz_time_left > 0:
        if not messagebox.askyesno("Finish Early", "You still have some time left. Do you want to finish?"):
            start_timer()
            return
    end_quiz()

def end_quiz():
    global quiz_score
    
    # Calculate score
    quiz_score = sum(
        1 for i, q in enumerate(quiz_questions)
        if quiz_answers[i] is not None and q["Choices"][quiz_answers[i]] == q["Answer"]
    )
    
    # Update user progress
    users = load_users()
    if current_user in users:
        user_data = users[current_user]
        
        # Update progress stats
        user_data["progress"]["quizzes_taken"] += 1
        user_data["progress"]["total_score"] += quiz_score
        
        # Calculate average score safely
        total_possible = user_data["progress"]["quizzes_taken"] * len(quiz_questions)
        if total_possible > 0:
            user_data["progress"]["average_score"] = round(
                (user_data["progress"]["total_score"] / total_possible) * 100,
                1
            )
        
        if quiz_score == len(quiz_questions):
            user_data["progress"]["perfect_scores"] += 1
        
        # Add to history
        user_data["history"].append({
            "subject": quiz_subject,
            "score": quiz_score,
            "total": len(quiz_questions),
            "percentage": round((quiz_score / len(quiz_questions)) * 100, 1),
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # Keep only last 10 attempts
        user_data["history"] = user_data["history"][-10:]
        
        save_users(users)
    
    if messagebox.askyesno("Quiz Finished", 
                         f"Your score: {quiz_score} out of {len(quiz_questions)}\nReview your answers?"):
        show_review()
    else:
        quiz_page()

def show_review():
    global quiz_frame
    try:
        quiz_frame.destroy()
    except:
        pass

    # --- Scrollable Frame Setup ---
    quiz_frame = Frame(window, bg="white")
    quiz_frame.pack(fill=BOTH, expand=1)

    # Canvas and scrollbar
    canvas = Canvas(quiz_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(quiz_frame, orient=VERTICAL, command=canvas.yview)
    scroll_frame = Frame(canvas, bg="white")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # --- Back to Quizzes Button ---
    Button(scroll_frame, text="Back to Quizzes", font=("Consolas", 14), bg="#0298DD", fg="white", command=quiz_page).grid(row=0, column=0, columnspan=2, pady=10)

    scroll_frame.grid_columnconfigure(0, weight=1, minsize=400)
    scroll_frame.grid_columnconfigure(1, weight=1, minsize=400)
    for i, q in enumerate(quiz_questions):
        col = i % 2
        row = (i // 2) + 1

        q_frame = Frame(scroll_frame, bg="white", bd=2, relief="groove", padx=10, pady=10, width=380, height=250)
        q_frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        q_frame.grid_propagate(False)  # Prevent auto-resizing

        # Question label with wrapping
        Label(
            q_frame, text=f"Q{i+1}: {q['Question']}",
            font=("Consolas", 13, "bold"),
            bg="white", wraplength=360, justify="left"
        ).pack(anchor="w", pady=5)

        letters = ["A", "B", "C", "D"]
        for j, choice in enumerate(q["Choices"]):
            btn_bg = "white"
            btn_fg = "black"
            if q["Choices"][j] == q["Answer"]:
                btn_bg = "#b6fcb6"  # green
            if quiz_answers[i] == j and q["Choices"][j] != q["Answer"]:
                btn_bg = "#ffb3b3"  # red

            wrapper = Frame(q_frame, bg="#0298DD", padx=1, pady=1)
            wrapper.pack(anchor="center", pady=4)

            inner = Frame(wrapper, bg="white")
            inner.pack()

            label_letter = Label(inner, text=letters[j], font=("Consolas", 12, "bold"),
                                 width=2, bg="#0298DD", fg="white")
            label_letter.pack(side=LEFT, padx=4, pady=2)

            btn = Button(inner, text=choice, font=("Consolas", 11),
                         wraplength=330, anchor="w", justify="left", width=30,
                         bg=btn_bg, fg=btn_fg, relief="flat", borderwidth=0,
                         state="disabled")
            btn.pack(side=LEFT, fill="x", expand=True, padx=(0, 4), pady=2)



    # Make sure the scroll_frame expands horizontally
    scroll_frame.grid_columnconfigure(0, weight=1)
    scroll_frame.grid_columnconfigure(1, weight=1)

def on_quit_attempt():
    stop_timer()
    if messagebox.askyesno("Quit Quiz", "Do you want to quit?"):
        quiz_page()
    else:
        start_timer()

def start_timer():
    global quiz_time_left, quiz_timer_id
    update_timer()

def update_timer():
    global quiz_time_left, quiz_timer_id
    mins = quiz_time_left // 60
    secs = quiz_time_left % 60
    timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
    if quiz_time_left > 0:
        quiz_time_left -= 1
        quiz_timer_id = window.after(1000, update_timer)
    else:
        end_quiz_by_time()

def stop_timer():
    global quiz_timer_id
    if quiz_timer_id:
        window.after_cancel(quiz_timer_id)
        quiz_timer_id = None

def end_quiz_by_time():
    stop_timer()
    messagebox.showinfo("Time's up!", "Time is up!")
    end_quiz()

def view_full_history():
    if not current_user:
        messagebox.showinfo("Info", "Please log in to view your history")
        return
    
    users = load_users()
    user_data = users.get(current_user, {})
    history = user_data.get("history", [])
    
    history_window = Toplevel(window)
    history_window.title("Your Quiz History")
    history_window.geometry("600x400")
    
    canvas = Canvas(history_window, bg="white")
    scrollbar = Scrollbar(history_window, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    if not history:
        Label(scrollable_frame, text="No quiz history yet!", 
              font=("Consolas", 14), bg="white").pack(pady=20)
    else:
        for attempt in reversed(history):
            attempt_frame = Frame(scrollable_frame, bg="#FAFAFA", 
                                 padx=15, pady=10, highlightbackground="#DDDDDD", 
                                 highlightthickness=1)
            attempt_frame.pack(fill=X, padx=10, pady=5)
            
            # Subject and date
            Label(attempt_frame, 
                  text=f"{attempt['subject'].title()} - {attempt['date']}", 
                  font=("Consolas", 14, "bold"), bg="#FAFAFA").pack(anchor="w")
            
            # Score bar
            score_bar = Frame(attempt_frame, bg="#E0E0E0", height=20)
            score_bar.pack(fill=X, pady=5)
            
            percentage = attempt['score'] / attempt['total']
            colored_bar = Frame(score_bar, bg="#0298DD", width=percentage*300)
            colored_bar.pack(side=LEFT, fill=Y)
            
            # Score text
            Label(attempt_frame, 
                  text=f"{attempt['score']}/{attempt['total']} ({attempt['percentage']}%)", 
                  font=("Consolas", 12), bg="#FAFAFA").pack(anchor="w")

def welcome_page():
    global welcome_frame
    if header_frame is not None and header_frame.winfo_exists():
        header_frame.destroy()

    welcome_frame = Frame(window, bg="white")
    photolabel = Label(welcome_frame, image=welcome_background, border=0)
    photolabel.pack(side=TOP)
    welcome_frame.pack(fill=BOTH, expand=1)

    welcome_label = Label(welcome_frame, text="Welcome to QuizApp", font=("Consolas", 30, "bold"), bg="white")
    welcome_label.pack(side="top", pady=10)

    welcome_label2 = Label(welcome_frame, text="Whether you want to test your knowledge, have fun with quizzes or take exams, you are at the right place.", font=("Consolas", 15), bg="white", width=100, wraplength=600)
    welcome_label2.pack(side="top", pady=10)

    start_button = Button(welcome_frame, text="LET'S GO!", font=("Consolas", 20, "bold"), bg="#0191D4", fg="white", activeforeground="white", activebackground="#0298DD", border=0, command=login_page)
    start_button.pack(side="top", pady=10)

def login_page():
    global login_frame, login_frame2, header_frame  # Make sure to declare login_frame2 as global
    
    # Destroy header if exists
    if header_frame is not None and header_frame.winfo_exists():
        header_frame.destroy()

    def hide_username(event):
        username_entry.delete(0, "end")
        username_entry.config(fg="black")

    def show_username(event):
        if username_entry.get() == "":
            username_entry.insert(0, "Username")
            username_entry.config(fg="grey")

    def hide_password(event):
        if password_entry.get() == "Password":  # Only clear if it's the placeholder
            password_entry.delete(0, "end")
            password_entry.config(fg="black", show="*")
    
    def show_password(event):
        if password_entry.get() == "":  # Only show placeholder if empty
            password_entry.insert(0, "Password")
            password_entry.config(fg="grey", show="")

    # Destroy welcome frame if exists
    if 'welcome_frame' in globals() and welcome_frame.winfo_exists():
        welcome_frame.destroy()

    # Create main login frame
    login_frame = Frame(window, bg="white")
    login_frame.pack(fill=BOTH, expand=1)

    # Left side - image
    image_frame = Frame(login_frame, bg="white")
    image_frame.pack(side=LEFT)
    image_label = Label(image_frame, image=login_image, border=0)
    image_label.pack(padx=5, pady=20)

    # Right side - login form (THIS MUST COME BEFORE ANY REFERENCES TO login_frame2)
    login_frame2 = Frame(login_frame, bg="white")
    login_frame2.pack(side=RIGHT, fill=BOTH, expand=1)

    # Login title
    login_label = Label(login_frame2, text="Welcome Back :)", font=("Consolas", 30, "bold"), bg="white", fg="#0298DD")
    login_label.place(x=0, y=80)

    # Username field
    username_entry = Entry(login_frame2, font=("Consolas", 20), width=30, border=0)
    username_entry.place(x=0, y=240)
    username_entry.insert(0, "Username")
    username_entry.config(fg="grey")
    username_entry.bind("<FocusIn>", hide_username)
    username_entry.bind("<FocusOut>", show_username)
    Frame(login_frame2, width=295, height=2, bg="black").place(x=0, y=270)

    # Password field (NOW THIS IS SAFE SINCE login_frame2 EXISTS)
    password_entry = Entry(login_frame2, font=("Consolas", 20), width=30, border=0)
    password_entry.place(x=0, y=300)
    password_entry.insert(0, "Password")
    password_entry.config(fg="grey")
    password_entry.bind("<FocusIn>", hide_password)
    password_entry.bind("<FocusOut>", show_password)
    Frame(login_frame2, width=295, height=2, bg="black").place(x=0, y=330)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        if password == "Password":  # Don't allow the placeholder as password
            messagebox.showerror("Error", "Please enter your actual password!")
            return
        password_entry.delete(0, END)  # Clear the password field after attempt
        login(username, password)
    
    def on_sign_up():
        username = username_entry.get()
        password = password_entry.get()
        if password == "Password":  # Don't allow the placeholder as password
            messagebox.showerror("Error", "Please enter your actual password!")
            return
        password_entry.delete(0, END)  # Clear the password field after attempt
        sign_up(username, password)

    # Login button
    login_btn = Button(login_frame2, text="Login Now", font=("Consolas", 20), 
                      border=0, bg="#0298DD", fg="white", 
                      activeforeground="#0298DD", activebackground="white", 
                      command=on_login)
    login_btn.place(x=0, y=400)

    # Sign up button
    sign_up_btn = Button(login_frame2, text="Sign Up", font=("Consolas", 20), 
                        bg="#D8D6D6", fg="#0298DD", 
                        activeforeground="#0298DD", activebackground="white", 
                        border=0, command=on_sign_up)
    sign_up_btn.place(x=190, y=400)

def save_question(subject, question, choices, answer, explanation):
    # Load existing questions
    if os.path.exists(quizzes_file):
        with open(quizzes_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Add subject if not present
    if subject not in data:
        data[subject] = []

    # Add new question
    data[subject].append({
        "Question": question,
        "Choices": choices,
        "Answer": answer,
        "Explanation": explanation
    })

    with open(quizzes_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def home_page():
    global home_frame
    
    # Clear existing frames
    for frame in [login_frame, update_frame, quiz_frame, home_frame]:
        try:
            frame.destroy()
        except:
            pass

    if header_frame is None or not header_frame.winfo_exists():
        create_header()
    set_active_nav("Home")

    # Create main home frame with scrollable canvas
    home_frame = Frame(window, bg="white")
    home_frame.pack(fill=BOTH, expand=1)
    
    canvas = Canvas(home_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(home_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # --- Welcome Section ---
    welcome_frame = Frame(scrollable_frame, bg="white", padx=20, pady=20)
    welcome_frame.pack(fill=X)
    
    welcome_text = f"Welcome back, {current_user}!" if current_user else "Welcome to QuizApp!"
    Label(welcome_frame, text=welcome_text, 
          font=("Consolas", 24, "bold"), bg="white").grid(row=0, column=0, sticky="w")
    
    # Add a decorative icon next to welcome text
    if current_user:
        Label(welcome_frame, text="🎯", font=("Arial", 24), bg="white").grid(row=0, column=1, padx=10)
    
    Label(welcome_frame, 
          text="Test your knowledge and learn something new today!", 
          font=("Consolas", 14), bg="white", fg="#555555").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0,20))

    # --- Quick Stats Section --- (Only shown when logged in)
    if current_user:
        users = load_users()
        user_data = users.get(current_user, {})
        progress = user_data.get("progress", {
            "quizzes_taken": 0,
            "total_score": 0,
            "average_score": 0,
            "perfect_scores": 0
        })
        history = user_data.get("history", [])
        
        # Stats Frame with shadow effect
        stats_frame = Frame(scrollable_frame, bg="#F5F5F5", padx=20, pady=15, 
                          highlightbackground="#E0E0E0", highlightthickness=1)
        stats_frame.pack(fill=X, padx=20, pady=10)
        
        Label(stats_frame, text="📊 Your Progress", 
              font=("Consolas", 16, "bold"), bg="#F5F5F5").pack(anchor="w")
        
        # Stats Grid with icons
        stats_grid = Frame(stats_frame, bg="#F5F5F5")
        stats_grid.pack(fill=X, pady=10)
        
        # Calculate average score safely
        avg_score = progress["average_score"] if progress["quizzes_taken"] > 0 else 0
        
        stats = [
            {"value": progress["quizzes_taken"], "label": "Quizzes Taken", "icon": "📝"},
            {"value": f"{avg_score}%", "label": "Avg. Score", "icon": "📈"},
            {"value": progress["perfect_scores"], "label": "Perfect Scores", "icon": "⭐"},
            {"value": len(history), "label": "Total Attempts", "icon": "🔄"}
        ]
        
        for i, stat in enumerate(stats):
            stat_frame = Frame(stats_grid, bg="#F5F5F5", padx=15)
            stat_frame.pack(side=LEFT, padx=10)
            
            # Icon and value in same row
            icon_val_frame = Frame(stat_frame, bg="#F5F5F5")
            icon_val_frame.pack()
            
            Label(icon_val_frame, text=stat["icon"], 
                  font=("Arial", 20), bg="#F5F5F5").pack(side=LEFT, padx=5)
            Label(icon_val_frame, text=stat["value"], 
                  font=("Consolas", 24, "bold"), bg="#F5F5F5", fg="#0298DD").pack(side=LEFT)
            
            Label(stat_frame, text=stat["label"], 
                  font=("Consolas", 12), bg="#F5F5F5", fg="#777777").pack()

    # --- Recent Activity Section ---
    if current_user and history:
        recent_frame = Frame(scrollable_frame, bg="white", padx=20, pady=20)
        recent_frame.pack(fill=X)
        
        Label(recent_frame, text="📅 Recent Activity", 
              font=("Consolas", 18, "bold"), bg="white").pack(anchor="w", pady=(0,15))
        
        # Show last 3 attempts
        for attempt in reversed(history[-3:]):
            attempt_frame = Frame(recent_frame, bg="#FAFAFA", 
                                padx=15, pady=10, highlightbackground="#DDDDDD", 
                                highlightthickness=1)
            attempt_frame.pack(fill=X, pady=5)
            
            # Subject and date
            subject_date_frame = Frame(attempt_frame, bg="#FAFAFA")
            subject_date_frame.pack(fill=X)
            
            Label(subject_date_frame, 
                  text=f"📚 {attempt['subject'].title()}", 
                  font=("Consolas", 14, "bold"), bg="#FAFAFA").pack(side=LEFT)
            
            Label(subject_date_frame, 
                  text=f"🗓️ {attempt['date']}", 
                  font=("Consolas", 12), bg="#FAFAFA", fg="#666666").pack(side=RIGHT)
            
            # Score bar with percentage
            score_frame = Frame(attempt_frame, bg="#FAFAFA")
            score_frame.pack(fill=X, pady=5)
            
            percentage = attempt['score'] / attempt['total']
            Label(score_frame, 
                  text=f"Score: {attempt['score']}/{attempt['total']} ({attempt['percentage']}%)", 
                  font=("Consolas", 12), bg="#FAFAFA").pack(side=LEFT)
            
            # Retry button
            Button(score_frame, text="Retry", font=("Consolas", 10), 
                  bg="#0298DD", fg="white", width=8,
                  command=lambda s=attempt['subject']: start_quiz(s.lower())).pack(side=RIGHT)

    # --- Recommended Quizzes ---
    rec_frame = Frame(scrollable_frame, bg="white", padx=20, pady=20)
    rec_frame.pack(fill=X)
    
    Label(rec_frame, text="💡 Recommended For You", 
          font=("Consolas", 18, "bold"), bg="white").pack(anchor="w", pady=(0,15))
    
    # Create 3 quiz cards in a row
    rec_quizzes = random.sample(quiz_subjects, min(3, len(quiz_subjects)))
    cards_frame = Frame(rec_frame, bg="white")
    cards_frame.pack(fill=X)
    
    for quiz in rec_quizzes:
        card = Frame(cards_frame, bg="#F5F5F5", padx=15, pady=15, 
                    highlightbackground="#DDDDDD", highlightthickness=1)
        card.pack(side=LEFT, padx=10, expand=True, fill=BOTH)
        
        Label(card, text=quiz["emoji"], font=("Arial", 30), bg="#F5F5F5").pack()
        Label(card, text=quiz["name"], font=("Consolas", 14, "bold"), bg="#F5F5F5").pack(pady=5)
        
        Button(card, text="Start Quiz", font=("Consolas", 12), 
              bg="#0298DD", fg="white", width=12,
              command=lambda s=quiz["name"].lower(): start_quiz(s)).pack(pady=5)

    # --- Motivational Quote ---
    quotes = [
        "The expert in anything was once a beginner.",
        "Learning is a treasure that will follow its owner everywhere.",
        "Success is the sum of small efforts, repeated daily.",
        "Don't stop when you're tired. Stop when you're done."
    ]
    
    quote_frame = Frame(scrollable_frame, bg="#E3F2FD", padx=20, pady=15)
    quote_frame.pack(fill=X, padx=20, pady=20)
    
    Label(quote_frame, text=f'"{random.choice(quotes)}"', 
          font=("Consolas", 14, "italic"), bg="#E3F2FD", wraplength=600).pack()
    Label(quote_frame, text="- Unknown", 
          font=("Consolas", 12), bg="#E3F2FD", fg="#555555").pack(anchor="e")

    # Make sure the scrollable frame expands properly
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
def update_quiz_cards():
    global quiz_cards_frame, quiz_page_index, back_button, next_button

    for widget in quiz_cards_frame.winfo_children():
        widget.destroy()

    start = quiz_page_index * quizzes_per_page
    end = start + quizzes_per_page
    subjects_to_show = quiz_subjects[start:end]

    for subject in subjects_to_show:
        frame = Frame(quiz_cards_frame, width=200, height=250, bg="white")
        frame.pack(side=LEFT, padx=20)
        frame.pack_propagate(False)

        icon_frame = Frame(frame, bg=subject["color"], width=200, height=120)
        icon_frame.pack(pady=5)
        icon_frame.pack_propagate(False)
        Label(icon_frame, text=subject["emoji"], font=("Arial", 50), bg=subject["color"]).pack(expand=True)

        Label(frame, text=subject["name"], font=("Arial", 16, "bold"), fg="black", bg="white").pack(pady=4)
        Button(frame, text="Take Quiz", font=("Bold", 14), bg="#0298DD", fg="white",
               command=lambda name=subject["name"].lower(): start_quiz(name)).pack(pady=6)

    # Enable/disable buttons
    back_button.config(state=NORMAL if quiz_page_index > 0 else DISABLED)
    next_button.config(state=NORMAL if end < len(quiz_subjects) else DISABLED)


def quiz_page():
    global quiz_frame, quiz_cards_frame, next_button, back_button, quiz_page_index
    
    try:
        home_frame.destroy()
    except:
        pass

    try:
        quiz_frame.destroy()
    except:
        pass

    try:
        update_frame.destroy()
    except:
        pass

    def next_page():
        global quiz_page_index
        if (quiz_page_index + 1) * quizzes_per_page < len(quiz_subjects):
            quiz_page_index += 1
            update_quiz_cards()

    def back_page():
        global quiz_page_index
        if quiz_page_index > 0:
            quiz_page_index -= 1
            update_quiz_cards()

    if header_frame is None or not header_frame.winfo_exists():
        create_header()
    set_active_nav("Quizzes")

    quiz_frame = Frame(window, bg="white")
    quiz_frame.pack(fill=BOTH, expand=1)

    quiz_frame_label = Label(quiz_frame, text="Available Quizzes", font=("Consolas", 20), fg="#0298DD", bg="white")
    quiz_frame_label.pack(pady=30)

    # Main container for quiz cards
    quiz_cards_container = Frame(quiz_frame, bg="white")
    quiz_cards_container.pack(pady=20)

    # Function to update quiz cards display
    def update_quiz_cards():
        global quiz_cards_frame
        
        # Destroy existing cards frame if it exists
        try:
            quiz_cards_frame.destroy()
        except:
            pass
        
        # Create new cards frame
        quiz_cards_frame = Frame(quiz_cards_container, bg="white")
        quiz_cards_frame.pack()

        start = quiz_page_index * quizzes_per_page
        end = start + quizzes_per_page
        subjects_to_show = quiz_subjects[start:end]

        for subject in subjects_to_show:
            # Outer frame with colored border
            border_frame = Frame(quiz_cards_frame, bg=subject["color"], width=210, height=310)
            border_frame.pack(side=LEFT, padx=20)
            border_frame.pack_propagate(False)

            # Inner content frame
            content_frame = Frame(border_frame, bg="white", width=200, height=300)
            content_frame.pack(expand=True)
            content_frame.pack_propagate(False)

            # Subject emoji/icon
            icon_label = Label(content_frame, text=subject["emoji"], font=("Arial", 50), bg="white")
            icon_label.pack(pady=10)

            # Subject name
            Label(content_frame, text=subject["name"], font=("Arial", 16, "bold"), fg="black", bg="white").pack(pady=4)

            # Take quiz button
            Button(content_frame, text="Take Quiz", font=("Bold", 14), bg="#0298DD", fg="white",
                  command=lambda name=subject["name"].lower(): start_quiz(name)).pack(pady=10)

        # Update navigation buttons state
        back_button.config(state=NORMAL if quiz_page_index > 0 else DISABLED)
        next_button.config(state=NORMAL if end < len(quiz_subjects) else DISABLED)

    # Navigation buttons frame
    nav_frame = Frame(quiz_frame, bg="white")
    nav_frame.pack(pady=20)

    back_button = Button(nav_frame, text=" \u2190 ", font=("Consolas", 20, "bold"), 
                        fg="black", bg="#0298DD", state=DISABLED, command=back_page)
    back_button.pack(side=LEFT, padx=10)

    next_button = Button(nav_frame, text=" \u2192 ", font=("Consolas", 20, "bold"), 
                        fg="black", bg="#0298DD", command=next_page)
    next_button.pack(side=LEFT, padx=10)

    # Initial display of quiz cards
    update_quiz_cards()

# Modified update_page function with required features

def update_page():
    global update_frame, question_count
    question_count = 1

    try:
        home_frame.destroy()
    except:
        pass
    try:
        quiz_frame.destroy()
    except:
        pass
    try:
        update_frame.destroy()
    except:
        pass

    if header_frame is None or not header_frame.winfo_exists():
        create_header()
    set_active_nav("Update")

    update_frame = Frame(window, bg="white")
    update_frame.pack(fill=BOTH, expand=1)

    if not current_is_admin:
        Label(update_frame, text='Access denied', font=("Consolas", 24, "bold"), fg="#0298DD", bg="white").pack(anchor="n", fill="x", pady=(10,0))
        Label(update_frame, text="Only administrators can access the update page.", font=("Consolas", 16), fg="black", bg="white").pack(anchor="n", fill="x")
        return

    # Create a canvas and scrollbar for the entire page
    canvas = Canvas(update_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(update_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)

    Label(scrollable_frame, text="Quiz Builder", font=("Consolas", 24, "bold"), bg="white", fg="#0298DD").pack(anchor="n", fill="x", pady=(10, 0))

    quiz_area = Frame(scrollable_frame, bg="white")
    quiz_area.pack(fill=BOTH, expand=1, padx=20)

    # Quiz Name Frame with blue border effect - more compact
    quiz_name_frame = Frame(quiz_area, bg="white")
    quiz_name_frame.pack(anchor="center", pady=(10, 0))
    
    # Quiz name label and entry in a single row
    Label(quiz_name_frame, text="Quiz Name:", font=("Consolas", 16), bg="white").pack(side=LEFT, padx=(0, 5))
    
    # Entry with blue border effect
    subject_outer = Frame(quiz_name_frame, bg="#0298DD", padx=1, pady=1)
    subject_outer.pack(side=LEFT, padx=(0, 10))
    subject_inner = Frame(subject_outer, bg="white")
    subject_inner.pack()
    subject_entry = Entry(subject_inner, font=("Consolas", 16), width=25, borderwidth=0, highlightthickness=0)
    subject_entry.pack()

    # Emoji label and dropdown in same row
    Label(quiz_name_frame, text="Emoji:", font=("Consolas", 16), bg="white").pack(side=LEFT, padx=(0, 5))
    
    # Emoji menu with blue border effect
    emoji_outer = Frame(quiz_name_frame, bg="#0298DD", padx=1, pady=1)
    emoji_outer.pack(side=LEFT)
    emoji_inner = Frame(emoji_outer, bg="white")
    emoji_inner.pack()
    emoji_var = StringVar(value="💻")
    emoji_menu = OptionMenu(emoji_inner, emoji_var, *[s["emoji"] for s in quiz_subjects])
    emoji_menu.config(font=("Consolas", 16), borderwidth=0, highlightthickness=0)
    emoji_menu.pack()

    question_frames = []

    def add_question():
        global question_count
        # Outer frame with blue border effect
        question_outer = Frame(quiz_area, bg="#0298DD", padx=2, pady=2)
        question_outer.pack(anchor="center", pady=10, fill="x")
        
        question_frame = Frame(question_outer, bg="white", padx=10, pady=10)
        question_frame.pack(fill="x")

        # Question label and entry in compact form
        q_label_frame = Frame(question_frame, bg="white")
        q_label_frame.pack(anchor="w")
        Label(q_label_frame, text=f"Question {question_count}:", font=("Consolas", 16), bg="white").pack(side=LEFT, padx=(0, 5))
        
        # Question entry with blue border effect
        q_outer = Frame(q_label_frame, bg="#0298DD", padx=1, pady=1)
        q_outer.pack(side=LEFT)
        q_inner = Frame(q_outer, bg="white")
        q_inner.pack()
        q_entry = Entry(q_inner, font=("Consolas", 16), width=50, borderwidth=0, highlightthickness=0)
        q_entry.pack()

        choices_frame = Frame(question_frame, bg="white")
        choices_frame.pack(anchor="w")
        
        choices = []
        letters = ["A", "B", "C", "D"]

        def add_choice():
            index = len(choices)
            if index >= 4:  # Limit to 4 choices (A-D)
                messagebox.showwarning("Warning", "Maximum 4 choices allowed!")
                return
                
            letter = chr(65 + index)
            ch_frame = Frame(choices_frame, bg="white")
            ch_frame.pack(anchor="w")
            
            # Choice label
            Label(ch_frame, text=f"{letter}:", font=("Consolas", 16), bg="white", width=2).pack(side=LEFT)
            
            # Choice entry with blue border effect
            ch_outer = Frame(ch_frame, bg="#0298DD", padx=1, pady=1)
            ch_outer.pack(side=LEFT, padx=(0, 5))
            ch_inner = Frame(ch_outer, bg="white")
            ch_inner.pack()
            ch_entry = Entry(ch_inner, font=("Consolas", 16), width=40, borderwidth=0, highlightthickness=0)
            ch_entry.pack()
            choices.append(ch_entry)

        # Add initial 2 choices
        for _ in range(2):
            add_choice()

        # Add choice button with blue styling
        Button(choices_frame, text="Add a new choice", font=("Consolas", 14), 
               command=add_choice, bg="#0298DD", fg="white", relief="flat").pack(anchor="w", pady=5)

        # Correct answer in compact form
        ans_label_frame = Frame(question_frame, bg="white")
        ans_label_frame.pack(anchor="w")
        Label(ans_label_frame, text="Correct Answer:", font=("Consolas", 16), bg="white").pack(side=LEFT, padx=(0, 5))
        
        # Answer entry with blue border effect
        ans_outer = Frame(ans_label_frame, bg="#0298DD", padx=1, pady=1)
        ans_outer.pack(side=LEFT)
        ans_inner = Frame(ans_outer, bg="white")
        ans_inner.pack()
        answer_entry = Entry(ans_inner, font=("Consolas", 16), width=30, borderwidth=0, highlightthickness=0)
        answer_entry.pack()

        # Explanation in compact form
        exp_label_frame = Frame(question_frame, bg="white")
        exp_label_frame.pack(anchor="w")
        Label(exp_label_frame, text="Explanation:", font=("Consolas", 16), bg="white").pack(side=LEFT, padx=(0, 5))
        
        # Explanation entry with blue border effect
        exp_outer = Frame(exp_label_frame, bg="#0298DD", padx=1, pady=1)
        exp_outer.pack(side=LEFT)
        exp_inner = Frame(exp_outer, bg="white")
        exp_inner.pack()
        explanation_entry = Entry(exp_inner, font=("Consolas", 16), width=50, borderwidth=0, highlightthickness=0)
        explanation_entry.pack()

        question_frames.append((q_entry, choices, answer_entry, explanation_entry))
        question_count += 1

    def save_quiz():
        subject = subject_entry.get().strip()
        emoji = emoji_var.get()
        if not subject:
            messagebox.showerror("Error", "Quiz name is required!")
            return

        # Update subjects if not already added
        if not any(s['name'].lower() == subject.lower() for s in quiz_subjects):
            quiz_subjects.append({"name": subject, "emoji": emoji, "color": "#FFFFFF"})

        for q_entry, ch_entries, answer_entry, explanation_entry in question_frames:
            question = q_entry.get().strip()
            choices = [c.get().strip() for c in ch_entries if c.get().strip()]
            answer = answer_entry.get().strip()
            explanation = explanation_entry.get().strip()
            if not (question and choices and answer):
                continue
            save_question(subject.lower(), question, choices, answer, explanation)

        messagebox.showinfo("Success", "Quiz and questions saved!")
        quiz_page()

    add_question()

    # Centered buttons frame - stacked vertically
    buttons_frame = Frame(scrollable_frame, bg="white")
    buttons_frame.pack(pady=10)
    
    # Add another question button (top)
    Button(buttons_frame, text="Add another Question", font=("Consolas", 16), 
           command=add_question, bg="#0298DD", fg="white", relief="flat").pack(pady=5)
    
    # Add quiz button (bottom)
    Button(buttons_frame, text="Add Quiz", font=("Consolas", 18), 
           command=save_quiz, bg="#0298DD", fg="white", relief="flat").pack(pady=5)

    # Configure the buttons frame to center its children
    buttons_frame.pack_propagate(False)
    buttons_frame.config(width=400, height=120)
    
def about_page():
    global about_frame
    try:
        if home_frame and home_frame.winfo_exists():
            home_frame.destroy()
    except: pass
    try:
        if quiz_frame and quiz_frame.winfo_exists():
            quiz_frame.destroy()
    except: pass
    try:
        if update_frame and update_frame.winfo_exists():
            update_frame.destroy()
    except: pass
    try:
        if about_frame and about_frame.winfo_exists():
            about_frame.destroy()
    except: pass

    if header_frame is None or not header_frame.winfo_exists():
        create_header()
    set_active_nav("About")

    about_frame = Frame(window, bg="white")
    about_frame.pack(fill=BOTH, expand=1)

    # --- Scrollable Frame Setup ---
    canvas = Canvas(about_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(about_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # --- Add About Page Content Here ---
    Label(scrollable_frame, text="About QuizApp", font=("Consolas", 25, "bold"), fg="#0298DD", bg="white").pack(pady=30)

    about_text = '''
QuizApp is a versatile quiz application designed to provide an engaging and interactive experience for users who want to test their knowledge across various subjects. Whether you're a student preparing for exams, a teacher creating quizzes, or just someone who loves learning, QuizApp has something for you.

Features:
- User-friendly interface for easy navigation
- Secure login and sign-up with password protection
- Admin-only quiz creation and management
- Timed quizzes from different subjects to simulate exams
- Clickable buttons, clear layout, A–D multiple choice formatting
- Instant score calculation with correct and wrong answers
- Post-quiz breakdown of user’s answers vs correct answers

Upcoming features:
- Progress tracking to view past scores, average performance, and quiz   history
- Choose quiz difficulty: Easy, Medium, Hard
- Multi-language interface (Amharic, English etc.)
- Show top scorers (local) and gamification
- Filtering by subject, topic, or number of questions
- Teachers can assign quizzes and track student scores
    '''

    Label(scrollable_frame, text=about_text, font=("Consolas", 14), bg="white", wraplength=750, justify="left").pack(padx=20, pady=10)

    about_text2 = """This QuizApp is prepared for you by Abune Gorgorios Secondary School ICT Club Group 2, comprising of
    - Firebiruk Gezu (firebirukgezu84@gmail.com) -Group leader
    - Abenezer Shambel (shambelabenezer301@gmail.com)
    - Ermias Addis 
    - Nuhamin
    - 
    - 
    Any comments can be directly emailed by the emails given above.
    
    """

    Label(scrollable_frame, text=about_text2, font=("Consolas", 14), bg="white", wraplength=750, justify="left").pack(padx=20, pady=10)

    Label(scrollable_frame, text="Special Thanks", font=("Consolas", 20, "bold"), fg="#0298DD", bg="white").pack(pady=(30, 10))

    thanks_text = '''
We would like to express our heartfelt gratitude to:

- Our teachers, for inspiring the pursuit of knowledge.
- Friends and testers who provided valuable feedback.
- The open-source Python community for the tools and libraries that made this   project  possible.
- Everyone who supported this project directly or indirectly.

Thank you!
'''
    Label(scrollable_frame, text=thanks_text, font=("Consolas", 13), bg="white", wraplength=750, justify="left").pack(pady=(0, 20), padx=20)


def settings_page():
    global settings_frame
    
    try:
        home_frame.destroy()
    except:
        pass
    try:
        quiz_frame.destroy()
    except:
        pass
    try:
        update_frame.destroy()
    except:
        pass
    try:
        settings_frame.destroy()
    except:
        pass

    if header_frame is None or not header_frame.winfo_exists():
        create_header()
    set_active_nav("Settings")

    settings_frame = Frame(window, bg="white")
    settings_frame.pack(fill=BOTH, expand=1)

    # Main container with scrollbar
    canvas = Canvas(settings_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(settings_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Settings title
    Label(scrollable_frame, text="Settings", font=("Consolas", 24, "bold"), 
          bg="white", fg="#0298DD").pack(pady=20)

    # Account Settings Section
    account_frame = Frame(scrollable_frame, bg="white", padx=20, pady=10)
    account_frame.pack(fill=X)

    Label(account_frame, text="Account Settings", font=("Consolas", 18, "bold"), 
          bg="white").pack(anchor="w", pady=10)

    # Change Password
    pass_frame = Frame(account_frame, bg="white")
    pass_frame.pack(fill=X, pady=5)

    Label(pass_frame, text="Change Password:", font=("Consolas", 14), 
          bg="white").pack(side=LEFT, padx=5)

    old_pass = Entry(pass_frame, font=("Consolas", 14), show="*", width=20)
    old_pass.pack(side=LEFT, padx=5)
    old_pass.insert(0, "Current Password")

    new_pass = Entry(pass_frame, font=("Consolas", 14), show="*", width=20)
    new_pass.pack(side=LEFT, padx=5)
    new_pass.insert(0, "New Password")

    def change_password():
        users = load_users()
        if current_user not in users:
            messagebox.showerror("Error", "User not found!")
            return
            
        if users[current_user]["password"] != old_pass.get():
            messagebox.showerror("Error", "Current password is incorrect!")
            return
            
        if len(new_pass.get()) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return
            
        users[current_user]["password"] = new_pass.get()
        save_users(users)
        messagebox.showinfo("Success", "Password changed successfully!")
        old_pass.delete(0, END)
        new_pass.delete(0, END)

    Button(pass_frame, text="Update", font=("Consolas", 12), bg="#0298DD", 
           fg="white", command=change_password).pack(side=LEFT, padx=10)

    # Add space before Appearance section
    Frame(scrollable_frame, height=20, bg="white").pack()

    # Theme Settings Section
    theme_frame = Frame(scrollable_frame, bg="white", padx=20, pady=10)
    theme_frame.pack(fill=X)

    Label(theme_frame, text="Appearance (Coming Soon)", font=("Consolas", 18, "bold"), 
          bg="white").pack(anchor="w", pady=(20, 10))

    # Disabled theme selection
    theme_var = StringVar(value="light")
    Radiobutton(theme_frame, text="Light Theme", variable=theme_var, value="light",
               font=("Consolas", 12), bg="white", selectcolor="#0298DD", state=DISABLED).pack(anchor="w")
    Radiobutton(theme_frame, text="Dark Theme", variable=theme_var, value="dark",
               font=("Consolas", 12), bg="white", selectcolor="#0298DD", state=DISABLED).pack(anchor="w")

    Button(theme_frame, text="Apply Theme", font=("Consolas", 12), bg="#CCCCCC",
           fg="#666666", state=DISABLED, command=lambda: messagebox.showinfo("Info", "Theme switching coming in a future update!")).pack(pady=10)

    # Quiz Settings Section
    quiz_frame = Frame(scrollable_frame, bg="white", padx=20, pady=10)
    quiz_frame.pack(fill=X)

    Label(quiz_frame, text="Quiz Preferences", font=("Consolas", 18, "bold"), 
          bg="white").pack(anchor="w", pady=10)

    # Time per question
    time_frame = Frame(quiz_frame, bg="white")
    time_frame.pack(fill=X, pady=5)

    Label(time_frame, text="Time per question (seconds):", font=("Consolas", 14), 
          bg="white").pack(side=LEFT)

    time_spin = Spinbox(time_frame, from_=10, to=120, increment=5, width=5,
                       font=("Consolas", 14))
    time_spin.pack(side=LEFT, padx=10)
    time_spin.delete(0, END)
    time_spin.insert(0, "60")

    def save_quiz_prefs():
        messagebox.showinfo("Saved", "Quiz preferences saved!")

    Button(quiz_frame, text="Save Preferences", font=("Consolas", 12), bg="#0298DD",
           fg="white", command=save_quiz_prefs).pack(pady=10)

    # Data Management Section
    data_frame = Frame(scrollable_frame, bg="white", padx=20, pady=10)
    data_frame.pack(fill=X)

    Label(data_frame, text="Data Management", font=("Consolas", 18, "bold"), 
          bg="white").pack(anchor="w", pady=10)

    def clear_history():
        if messagebox.askyesno("Confirm", "Clear all your quiz history?"):
            users = load_users()
            if current_user in users:
                users[current_user]["history"] = []
                users[current_user]["progress"] = {
                    "quizzes_taken": 0,
                    "total_score": 0,
                    "average_score": 0,
                    "perfect_scores": 0
                }
                save_users(users)
                messagebox.showinfo("Cleared", "Your history has been cleared")

    Button(data_frame, text="Clear Quiz History", font=("Consolas", 12), 
           bg="#FF6B6B", fg="white", command=clear_history).pack(pady=5)

    def export_data():
        messagebox.showinfo("Export", "Data export feature coming soon!")

    Button(data_frame, text="Export My Data", font=("Consolas", 12), 
           bg="#0298DD", fg="white", command=export_data).pack(pady=5)

toggle_icon = PhotoImage(file="toggle_btn_icon.png")
home_icon = PhotoImage(file="home_icon.png")
quiz_icon = PhotoImage(file="services_icon.png")
update_icon = PhotoImage(file="updates_icon.png")
contact_icon = PhotoImage(file="contact_icon.png")
about_icon = PhotoImage(file="about_icon.png")
close_icon = PhotoImage(file="close_btn_icon.png")
python_icon = PhotoImage(file="python_icon2.png")
math_icon = PhotoImage(file="math_icon.png")
physics_icon = PhotoImage(file="physics_icon.png")
welcome_background = PhotoImage(file="Quizapp.png")
login_image = PhotoImage(file="login.png")

current_user = None
current_is_admin = False

welcome_page()

window.mainloop()