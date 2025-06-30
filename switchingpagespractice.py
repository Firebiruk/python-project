from tkinter import *
from tkinter import messagebox
import random
window = Tk()
window.title("Quiz App")
window.geometry("800x600")

questions = [
    {
        "Question": "What is the language that a computer uses?",
        "Choices": ["Programming languages", "Binary numbers",  "Human languages", "None"],
        "Answer": "Binary numbers",
        "Explanation": "Computers operate using binary numbers (0s and 1s), which represent the most basic form of data a computer can process."
    },
    {
        "Question": "What is the most common language used for programming?",
        "Choices": ["JavaScript", "C++", "Python", "Java"],
        "Answer": "Python",
        "Explanation": "Python is one of the most widely used programming languages due to its simplicity and versatility."
    },
    {
        "Question": "What type of programming language is Python?",
        "Choices": ["High level", "Mid level", "Low level", "Machine language"],
        "Answer": "High level",
        "Explanation": "Python is a high-level language, meaning it's easier for humans to read and write compared to low-level machine code."
    },
    {
        "Question": "Which can be included under the application of Python?",
        "Choices": ["Creating websites", "Data analysis", "Artificial intelligence", "All of the above"],
        "Answer": "All of the above",
        "Explanation": "Python is used in a wide variety of fields including web development, data science, and AI."
    },
    {
        "Question": "Who is the creator of Python?",
        "Choices": ["Dennis Ritchie", "Willium Gates", "Martin Odersky", "Guido van Rossum"],
        "Answer": "Guido van Rossum",
        "Explanation": "Guido van Rossum developed Python in the late 1980s and released it in 1991."
    },
    {
        "Question": "Which one is not a programming language",
        "Choices": ["Python", "HTML", "RUST", "Java"],
        "Answer": "HTML",
        "Explanation": "HTML is a markup language used to structure content on the web, not a programming language."
    },
    {
        "Question": "Which one is the correct syntax for a variable in Python?",
        "Choices": ["Variable_name = value", "let variable_name = value;", "data_type variableName = value;", "None"],
        "Answer": "Variable_name = value",
        "Explanation": "In Python, variables are assigned using the equals sign without specifying data types."
    },
    {
        "Question": "Which one of programming languages does Python support?",
        "Choices": ["Object-Oriented Programming", "Structured Programming", "Functional Programming", "All"],
        "Answer": "All",
        "Explanation": "Python supports multiple programming paradigms including OOP, structured, and functional programming."
    },
    {
        "Question": "Which can legally be a name for a variable in Python?",
        "Choices": ["first-name", "@address", "name_1", "class"],
        "Answer": "name_1",
        "Explanation": "Valid Python variable names can include letters, numbers, and underscores but cannot start with numbers or use reserved keywords like 'class'."
    },
    {
        "Question": "Which one is the correct syntax for a comment in Python?",
        "Choices": ["/*Comment*/", "#Comment", "//Comment", "<!--Comment-->"],
        "Answer": "#Comment",
        "Explanation": "In Python, comments start with the '#' symbol."
    },
    {
        "Question": "Which one is the correct order of operations in Python?",
        "Choices": ["Parentheses, Exponents, Multiplication, Division, Addition, Subtraction", "Exponents, Parentheses, Multiplication, Division, Addition, Subtraction", "Parentheses, Exponents, Addition, Multiplication, Division, Subtraction", "Addition, Subtraction, Multiplication, Division, Exponents, Parentheses"],
        "Answer": "Parentheses, Exponents, Multiplication, Division, Addition, Subtraction",
        "Explanation": "Python follows the standard PEMDAS order of operations in arithmetic expressions."
    },
    {
        "Question": "Which operators combine multiple conditions and return True or False based on the logic?",
        "Choices": ["Arithmetic operators", "Logical operators", "Comparison operators", "Assignment operators"],
        "Answer": "Logical operators",
        "Explanation": "Logical operators like 'and', 'or', and 'not' are used to combine multiple conditions in Python."
    },
    {
        "Question": "Which one is a block of code that only runs when it is called?",
        "Choices": ["Class", "Condition", "Object", "Function"],
        "Answer": "Function",
        "Explanation": "A function is a reusable block of code that only executes when it is specifically called."
    },
    {
        "Question": "Which one correctly defines the use of loops in Python?",
        "Choices": ["To define a class that inherits all the methods and properties from another class", "To repeatedly perform a block of code as long as the conditions are satisfied", "To create Graphical User interfaces (GUIs)", "To store multiple values in a single variable"],
        "Answer": "To repeatedly perform a block of code as long as the conditions are satisfied",
        "Explanation": "Loops in Python, such as 'for' and 'while', are used to repeat actions as long as a condition holds."
    },
    {
        "Question": "Which one of the following matches data types with their respective characteristics?",
        "Choices": ["List- Unordered, changeable, and allows duplicate values", "Tuple- Ordered, changeable, and allow duplicate values", "Set- Unordered, unchangeable, and does not allow duplicate values", "Dictionary- Unordered, unchangeable, and allow duplicates"],
        "Answer": "Set- Unordered, unchangeable, and does not allow duplicate values",
        "Explanation": "Sets in Python are unordered collections of unique items, and they cannot be modified once created."
    },
    {
        "Question": "Which one is correct about lambda functions in Python?",
        "Choices": ["A lambda function is a small anonymous function", "A lambda function can take any number of arguments, but can only have one expression", "A lambda function can be applicable inside another function", "All of the above"],
        "Answer": "All of the above",
        "Explanation": "Lambda functions are anonymous, single-expression functions that can be used wherever small functions are needed."
    },
    {
        "Question": "What is the use of Class in Python?",
        "Choices": ["To create operators", "To define operators", "To create objects", "None of the above"],
        "Answer": "To create objects",
        "Explanation": "A class is a blueprint for creating objects, encapsulating data and functions together."
    },
    {
        "Question": "The process of resolving errors that occur in a program is called?",
        "Choices": ["File handling", "Exception handling", "Problem solving", "Iterating"],
        "Answer": "Exception handling",
        "Explanation": "Exception handling is the method of managing errors during program execution using try-except blocks."
    },
    {
        "Question": "Which one is the best known framework for Python?",
        "Choices": ["Django", "Bootstrap", "React", "Angular"],
        "Answer": "Django",
        "Explanation": "Django is a high-level Python web framework used for building secure and scalable web applications."
    },
    {
        "Question": "A GUI element which allows the user to choose exactly one of a predefined set of options is called?",
        "Choices": ["Button", "Checkbox", "Radio button", "Listbox"],
        "Answer": "Radio button",
        "Explanation": "Radio buttons allow users to select only one option from a group."
    },
    {
        "Question": "Which one returns a number selected at random within the range?",
        "Choices": ["Super", "Class", "Scale", "Random"],
        "Answer": "Random",
        "Explanation": "The 'random' module in Python provides functions to generate random numbers."
    },
    {
        "Question": "Which one is a widget that creates a drop-down list?",
        "Choices": ["Button", "Listbox", "Menu", "Label"],
        "Answer": "Menu",
        "Explanation": "The Menu widget in GUI toolkits like Tkinter can be used to create drop-down lists."
    },
    {
        "Question": "Which one is a widget that is used to draw graphs, plots, and other graphics?",
        "Choices": ["Frame", "Label", "Checkbutton", "Canvas"],
        "Answer": "Canvas",
        "Explanation": "Canvas is a widget in GUI libraries that provides space for drawing shapes and graphics."
    },
    {
        "Question": "What is Application Program Interface (API)?",
        "Choices": ["A set of rules that allows one software application to access another", "A program that draws codes from a database", "An application software used to write codes", "A program that allows one software application to access the hardware"],
        "Answer": "A set of rules that allows one software application to access another",
        "Explanation": "An API is a set of rules and protocols for building and interacting with software applications."
    },
    {
        "Question": "Which one is used to get the documentation of a module, class, functions, methods, variables, etc?",
        "Choices": ["doc()", "info()", "help()", "get()"],
        "Answer": "help()",
        "Explanation": "The help() function in Python provides the documentation of objects such as modules, classes, or functions."
    }
]

questions2 = [
    {
        "Question": "What is the value of π (pi) approximately?",
        "Choices": ["2.14", "3.14", "4.14", "5.14"],
        "Answer": "3.14",
        "Explanation": "Pi (π) is the ratio of a circle’s circumference to its diameter, approximately equal to 3.14."
    },
    {
        "Question": "Which operation is performed first in the expression 3 + 4 × 2?",
        "Choices": ["Addition", "Multiplication", "Subtraction", "Division"],
        "Answer": "Multiplication",
        "Explanation": "According to the order of operations (PEMDAS), multiplication is performed before addition."
    },
    {
        "Question": "What is the square root of 64?",
        "Choices": ["6", "8", "10", "12"],
        "Answer": "8",
        "Explanation": "The square root of 64 is 8 because 8 × 8 = 64."
    },
    {
        "Question": "Which of the following is a prime number?",
        "Choices": ["4", "6", "9", "11"],
        "Answer": "11",
        "Explanation": "11 is a prime number because it has only two factors: 1 and itself."
    },
    {
        "Question": "What is the result of 2² + 3²?",
        "Choices": ["13", "14", "15", "12"],
        "Answer": "13",
        "Explanation": "2² = 4 and 3² = 9, so the result is 4 + 9 = 13."
    },
    {
        "Question": "What is the formula for the area of a triangle?",
        "Choices": ["base*height", "½ *base*height", "length*width", "side²"],
        "Answer": "½*base*height",
        "Explanation": "The area of a triangle is calculated using the formula ½*base*height."
    },
    {
        "Question": "What is the greatest common divisor (GCD) of 24 and 36?",
        "Choices": ["6", "8", "12", "18"],
        "Answer": "12",
        "Explanation": "12 is the largest number that divides both 24 and 36 evenly."
    },
    {
        "Question": "What does the slope of a line represent in coordinate geometry?",
        "Choices": ["The distance between two points", "The angle of the line", "The steepness of the line", "The midpoint"],
        "Answer": "The steepness of the line",
        "Explanation": "The slope measures how steep a line is; it is the ratio of rise over run."
    },
    {
        "Question": "What is 15 percent of 200?",
        "Choices": ["25", "30", "35", "40"],
        "Answer": "30",
        "Explanation": "15 percent of 200 is 0.15*200 = 30."
    },
    {
        "Question": "What type of number is √2?",
        "Choices": ["Rational", "Whole", "Irrational", "Natural"],
        "Answer": "Irrational",
        "Explanation": "√2 is irrational because it cannot be expressed as a simple fraction."
    }
]

questions3 = [
    {
        "Question": "What is the unit of force in the SI system?",
        "Choices": ["Watt", "Joule", "Newton", "Pascal"],
        "Answer": "Newton",
        "Explanation": "The SI unit of force is the Newton (N), named after Isaac Newton."
    },
    {
        "Question": "What is the acceleration due to gravity on Earth?",
        "Choices": ["8.9 m/s²", "9.8 m/s²", "10.8 m/s²", "9.0 m/s²"],
        "Answer": "9.8 m/s²",
        "Explanation": "The average gravitational acceleration on Earth's surface is 9.8 meters per second squared."
    },
    {
        "Question": "What is the formula for calculating speed?",
        "Choices": ["distance ÷ time", "mass*acceleration", "force ÷ area", "energy ÷ time"],
        "Answer": "distance ÷ time",
        "Explanation": "Speed is calculated by dividing distance by time."
    },
    {
        "Question": "What is the main form of energy stored in a battery?",
        "Choices": ["Kinetic", "Thermal", "Chemical", "Mechanical"],
        "Answer": "Chemical",
        "Explanation": "Batteries store chemical energy, which is converted to electrical energy when used."
    },
    {
        "Question": "Which law explains that for every action, there is an equal and opposite reaction?",
        "Choices": ["First Law of Motion", "Second Law of Motion", "Third Law of Motion", "Law of Conservation of Energy"],
        "Answer": "Third Law of Motion",
        "Explanation": "Newton's Third Law states that every action has an equal and opposite reaction."
    },
    {
        "Question": "What is the speed of light in a vacuum?",
        "Choices": ["300,000 m/s", "300,000 km/h", "3*10⁸ m/s", "3*10⁶ m/s"],
        "Answer": "3*10⁸ m/s",
        "Explanation": "The speed of light in a vacuum is approximately 3*10⁸ meters per second."
    },
    {
        "Question": "What kind of wave is light?",
        "Choices": ["Sound wave", "Mechanical wave", "Electromagnetic wave", "Transverse wave"],
        "Answer": "Electromagnetic wave",
        "Explanation": "Light is an electromagnetic wave that can travel through a vacuum."
    },
    {
        "Question": "What is the unit of electric current?",
        "Choices": ["Volt", "Ampere", "Ohm", "Watt"],
        "Answer": "Ampere",
        "Explanation": "Electric current is measured in amperes (A)."
    },
    {
        "Question": "Which physical quantity is measured in joules?",
        "Choices": ["Force", "Power", "Work", "Current"],
        "Answer": "Work",
        "Explanation": "Work and energy are measured in joules (J)."
    },
    {
        "Question": "Which device is used to measure electric current?",
        "Choices": ["Voltmeter", "Ammeter", "Galvanometer", "Thermometer"],
        "Answer": "Ammeter",
        "Explanation": "An ammeter is used to measure the flow of electric current in a circuit."
    }
]

def take_math_quiz():
    start_quiz(questions2)

def take_physics_quiz():
    start_quiz(questions3)

def take_python_quiz():
    global service_frame
    global service_main_frame
    global current_question
    global score
    global choice_buttons
    global question_label
    global question_number_label
    global next
    global timer_label, timer_id, time_left, total_quiz_time

    menubar.pack_forget()
    service_main_frame.pack_forget()
    score = 0
    current_question = 0

    quiz_frame = Frame(service_frame)
    quiz_frame.pack(fill=BOTH, expand=1)

    # --- Timer label at the top ---
    total_quiz_time = 60 * len(questions)  # 60 seconds per question
    time_left = total_quiz_time
    timer_label = Label(quiz_frame, text=f"Time left: {time_left}s", font=("Consolas", 16), fg="red")
    timer_label.pack(pady=(10, 0))

    # --- Scrollable area setup ---
    canvas = Canvas(quiz_frame)
    scrollbar = Scrollbar(quiz_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=Y)
    # --- End scrollable area setup ---

    question_label = Label(scrollable_frame, width=50, font=("Consolas", 20), anchor=CENTER, pady=10, wraplength=500, justify=LEFT)
    question_label.pack(pady=50)

    choice_buttons = []
    for i in range(4):
        choice = Button(scrollable_frame, width=40, font=("Consolas", 20), wraplength=600, anchor="w", justify=LEFT, command=lambda i=i: check_answer(i))
        choice.pack(anchor=W, pady=5, padx=5)
        choice_buttons.append(choice)

    question_number_label = Label(scrollable_frame, text="", font=("Consolas", 14), anchor=W, pady=10)
    question_number_label.pack(anchor=W, padx=10, pady=(10, 0))

    next_btn = Button(scrollable_frame, text="Next", font=("Consolas", 14), command=next_question, state="disabled")
    next_btn.pack(pady=10)
    next = next_btn

    show_question()
    start_timer()  # Start the timer ONCE here

def show_question():
    global current_question
    global score
    global choice_buttons
    global question_label
    global question_number_label

    question = questions[current_question]
    question_label.config(text=question["Question"])
    question_number_label.config(text=f"Question {current_question + 1} of {len(questions)}")
    choices = question["Choices"][:]
    random.shuffle(choices)
    for i in range(4):
        choice_buttons[i].config(text=choices[i], state="normal", bg="SystemButtonFace")
    next.config(state="disabled")

def check_answer(choice):
    question = questions[current_question]
    selection = choice_buttons[choice].cget("text")
    if selection == question["Answer"]:
        global score
        score += 1
    for i in choice_buttons:
        i.config(state="disabled")
    next.config(state="normal")

def next_question():
    global choice_buttons
    global score
    global current_question
    current_question += 1
    if current_question < len(questions):
        show_question()
        for i in choice_buttons:
            i.config(bg="white")
    else:
        messagebox.showinfo("Quiz Completed", f"Your final score is {score} out of {len(questions)}.")

def start_timer():
    global timer_id
    update_timer()

def update_timer():
    global time_left, timer_id
    timer_label.config(text=f"Time left: {time_left}s")
    if time_left > 0:
        time_left -= 1
        timer_id = timer_label.after(1000, update_timer)
    else:
        end_quiz_due_to_time()

def stop_timer():
    global timer_id
    if timer_id:
        timer_label.after_cancel(timer_id)
        timer_id = None

def end_quiz_due_to_time():
    stop_timer()
    for btn in choice_buttons:
        btn.config(state="disabled")
    next.config(state="disabled")
    messagebox.showinfo("Time's up!", f"Time is up! Your final score is {score} out of {len(questions)}.")

def extend_animation():
    if menubar.winfo_width() <= 250:
        menubar.config(width=menubar.winfo_width() + 10)
        window.after(1, extend_animation)


def shrink_animation():    
    if menubar.winfo_width() > 60:
        menubar.config(width=menubar.winfo_width() - 10)
        window.after(1, shrink_animation)

def switch_indicator(indicator_label, page):
    home_btn_indicator.config(bg=menubar_color)
    service_btn_indicator.config(bg=menubar_color)
    update_btn_indicator.config(bg=menubar_color)
    contact_btn_indicator.config(bg=menubar_color)
    about_btn_indicator.config(bg=menubar_color)
    indicator_label.config(bg="white")

    if menubar.winfo_width() > 60:
        extend_menubar()

    for frame in main_frame.winfo_children():
        frame.destroy()

    page()

def extend_menubar():
    if menubar.winfo_width() == 60:
        extend_animation()
        toggle_btn.config(image=close_icon)
    elif menubar.winfo_width() > 60:
        shrink_animation()
        toggle_btn.config(image=toggle_icon)

def home_page():
    home_frame = Frame(main_frame, bg="#c3c3c3")
    header_frame = Frame(home_frame)
    header_label = Label(header_frame, text="QUIZ APP", font=("Arial", 24, "bold"), fg="black")
    header_label.pack(side=LEFT, padx=20)
    header_frame.pack(side=TOP, fill=X)
    header_frame.config(height=70)
    home_frame.pack(fill=BOTH, expand=1)

    home_main_frame = Frame(home_frame, bg="#c3c3c3")
    home_main_frame.pack(fill=BOTH, expand=1, pady=50)

    lb = Label(home_main_frame, text="Welcome to Quiz App, learner!", font=("Bold", 30), fg="black", bg="#c3c3c3")
    lb.place(x=120, y=100)

    lb1 = Label(home_main_frame, text="Ready to test your knowledge?", font=("Bold", 16), fg="black", bg="#c3c3c3")
    lb1.place(x=200, y=180)

    btn = Button(home_main_frame, text="Start Quiz", font=("Bold", 16), fg="black", command=lambda: switch_indicator(service_btn_indicator, page=service_page))
    btn.place(x=280, y=250)


def service_page():
    global service_frame
    global service_main_frame
    service_frame = Frame(main_frame, bg="#c3c3c3")
    header_frame = Frame(service_frame)
    header_label = Label(header_frame, text="QUIZ APP", font=("Arial", 24, "bold"), fg="black")
    header_label.pack(side=LEFT, padx=20)
    header_frame.pack(side=TOP, fill=X)
    header_frame.config(height=70)

    service_main_frame = Frame(service_frame)
    service_main_frame.pack(fill=BOTH, expand=1, pady=50)
    lb = Label(service_main_frame, text="Choose the subject you want", font=("Bold", 20), fg="black")
    lb.place(x=200, y=0)

    frm1 = Frame(service_main_frame, bg="#c3c3c3", border=1, width=200, height=300)
    frm1.pack(side=LEFT, padx=20)
    frm1img = Label(frm1, image=python_icon, width=200, height=150)
    frm1img.pack(side=TOP) 

    frm1lb = Label(frm1, text="Python", font=("Arial", 16, "bold"), bg="#c3c3c3", fg="black")
    frm1lb.pack(pady=4)

    frm1btn = Button(frm1, text="Take Quiz", font=("Bold", 16), bg="white", fg="black", command=take_python_quiz)
    frm1btn.pack(pady=4)

    frm2 = Frame(service_main_frame, bg="#c3c3c3", width=200, height=300, border=1)
    frm2.pack(padx=20, side=LEFT)

    frm2img = Label(frm2, image=math_icon, width=200, height=150)
    frm2img.pack(side=TOP) 

    frm2lb = Label(frm2, text="Mathematics", font=("Arial", 16, "bold"), bg="#c3c3c3", fg="black")
    frm2lb.pack(pady=4)

    frm2btn = Button(frm2, text="Take Quiz", font=("Bold", 16), bg="white", fg="black", command=take_math_quiz)
    frm2btn.pack(pady=4)

    frm3 = Frame(service_main_frame, bg="#c3c3c3", width=200, height=300, border=1)
    frm3.pack(side=LEFT, padx=20)

    frm3img = Label(frm3, image=physics_icon, width=200, height=150)
    frm3img.pack(side=TOP) 

    frm3lb = Label(frm3, text="Physics", font=("Arial", 16, "bold"), bg="#c3c3c3", fg="black")
    frm3lb.pack(pady=4)

    frm3btn = Button(frm3, text="Take Quiz", font=("Bold", 16), bg="white", fg="black", command=take_physics_quiz)
    frm3btn.pack(pady=4)

    service_frame.pack(fill=BOTH, expand=1)

def update_page():
    update_frame = Frame(main_frame, bg="#c3c3c3")
    lb = Label(update_frame, text="Welcome to the Update Page", font=("Bold", 20), bg="#c3c3c3")
    lb.pack()
    update_frame.pack(fill=BOTH, expand=1)

def contact_page():
    contact_frame = Frame(main_frame, bg="#c3c3c3")
    lb = Label(contact_frame, text="Welcome to the Contact Page", font=("Bold", 20), bg="#c3c3c3")
    lb.pack()
    contact_frame.pack(fill=BOTH, expand=1)

def about_page():
    about_frame = Frame(main_frame, bg="#c3c3c3")
    lb = Label(about_frame, text="Welcome to the About Page", font=("Bold", 20), bg="#c3c3c3")
    lb.pack()
    about_frame.pack(fill=BOTH, expand=1)

menubar_color = "#383838"
toggle_icon = PhotoImage(file="toggle_btn_icon.png")
home_icon = PhotoImage(file="home_icon.png")
service_icon = PhotoImage(file="services_icon.png")
update_icon = PhotoImage(file="updates_icon.png")
contact_icon = PhotoImage(file="contact_icon.png")
about_icon = PhotoImage(file="about_icon.png")
close_icon = PhotoImage(file="close_btn_icon.png")
python_icon = PhotoImage(file="python_icon2.png")
math_icon = PhotoImage(file="math_icon.png")
physics_icon = PhotoImage(file="physics_icon.png")

main_frame = Frame(window)
main_frame.place(relwidth=1, relheight=1, x=66, y=4)
home_page()

menubar = Frame(window)

toggle_btn = Button(menubar, image=toggle_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=extend_menubar)
toggle_btn.place(x=10, y=10)

home_btn = Button(menubar, image=home_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=lambda: switch_indicator(home_btn_indicator, page=home_page))
home_btn.place(x=10, y=125, width=40)

home_btn_indicator = Label(menubar, bg="white")
home_btn_indicator.place(x=3, y=120, width=4, height=40)

home_label = Label(menubar, text="Home", bg=menubar_color, fg="white", font=("Bold", 20), anchor="w", activebackground=menubar_color)
home_label.place(x=60, y=120, width=100, height=40)

home_label.bind("<Button-1>", lambda e: switch_indicator(home_btn_indicator))

service_btn = Button(menubar, image=service_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=lambda: switch_indicator(service_btn_indicator, page=service_page))
service_btn.place(x=10, y=185, width=40)

service_btn_indicator = Label(menubar, bg=menubar_color)
service_btn_indicator.place(x=3, y=180, width=4, height=40)

service_label = Label(menubar, text="Quiz", bg=menubar_color, fg="white", font=("Bold", 20), anchor="w", activebackground=menubar_color)
service_label.place(x=60, y=180, width=100, height=40)

service_label.bind("<Button-1>", lambda e:switch_indicator(service_btn_indicator))

update_btn = Button(menubar, image=update_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=lambda: switch_indicator(update_btn_indicator, page=update_page))
update_btn.place(x=10, y=245, width=40)

update_btn_indicator = Label(menubar, bg=menubar_color)
update_btn_indicator.place(x=3, y=240, width=4, height=40)

update_label = Label(menubar, text="Update", bg=menubar_color, fg="white", font=("Bold", 20), anchor="w", activebackground=menubar_color)
update_label.place(x=60, y=240, width=100, height=40)

update_label.bind("<Button-1>", lambda e: switch_indicator(update_btn_indicator))

contact_btn = Button(menubar, image=contact_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=lambda: switch_indicator(contact_btn_indicator, page=contact_page))
contact_btn.place(x=10, y=305, width=40)

contact_btn_indicator = Label(menubar, bg=menubar_color)
contact_btn_indicator.place(x=3, y=300, width=4, height=40)

contact_label = Label(menubar, text="Contact Us", bg=menubar_color, fg="white", font=("Bold", 20), anchor="w", activebackground=menubar_color)
contact_label.place(x=60, y=300, width=100, height=40)

contact_label.bind("<Button-1>", lambda e:switch_indicator(contact_btn_indicator))

about_btn = Button(menubar, image=about_icon, bg=menubar_color, bd=0, activebackground=menubar_color, command=lambda: switch_indicator(about_btn_indicator, page=about_page))
about_btn.place(x=10, y=365, width=40)

about_btn_indicator = Label(menubar, bg=menubar_color)
about_btn_indicator.place(x=3, y=360, width=4, height=40)

about_label = Label(menubar, text="About", bg=menubar_color, fg="white", font=("Bold", 20), anchor="w", activebackground=menubar_color)
about_label.place(x=60, y=360, width=100, height=40)

about_label.bind("<Button-1>", lambda e:switch_indicator(about_btn_indicator))

menubar.pack(side=LEFT, fill=Y, padx=3, pady=4)
menubar.pack_propagate(False)
menubar.config(width=60, bg=menubar_color)

timer_label = None
timer_id = None
time_left = 60

window.mainloop()