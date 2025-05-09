from tkinter import*
from tkinter import messagebox
import random

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

score = 0

def show_question():
    question = questions[current_question]
    label.config(text=question["Question"])
    question_number_label.config(text=f"Question {current_question + 1} of {len(questions)}")
    choose = question["Choices"]
    random.shuffle(choose)
    for i in range(4):
        choice_buttons[i].config(text=choose[i], state="normal")
    feedback.config(text="")
    next.config(state="disabled")

def check_answer(choice):
    question = questions[current_question]
    selection = choice_buttons[choice].cget("text")
    if selection == question["Answer"]:
        global score
        score += 1
        score_label.config(text="Score:"+str(score))
        feedback.config(text=f"Correct!\nExplanation: {question['Explanation']}", font=("Consolas", 20), fg="green")
    else:
        score_label.config(text="Score:"+str(score))
        feedback.config(text=f"Incorrect! Correct answer: {question['Answer']}", font=("Consolas", 20), fg="red")
        for i in choice_buttons:
            if i.cget("text") == question["Answer"]:
                i.config(bg="light green")
    for i in choice_buttons:
        i.config(state="disabled")
    next.config(state="normal")

def next_question():
    global current_question
    current_question+=1
    if current_question<len(questions):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed", f"Your final score is {score} out of {len(questions)}.")
        window.destroy()

window = Tk()
window.title("Quiz App")
window.geometry("900x700")

mainframe = Frame(window)
mainframe.pack(fill=BOTH, expand=1)

canvas = Canvas(mainframe)
# canvas.pack(side=LEFT, fill=BOTH, expand=1)

scroll = Scrollbar(mainframe, orient=VERTICAL, command=canvas.yview)
#scroll.pack(side=RIGHT, fill=Y)

# canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = Frame(canvas, padx=40)
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

label = Label(frame, width=50, font=("Consolas", 20), anchor=CENTER, pady=10, wraplength=700)
label.pack(pady=50)

choice_buttons = []
for i in range(4):
    choice = Button(frame, width=50, font=("Consolas", 20), wraplength=750, command=lambda i=i: check_answer(i))
    choice.pack(anchor=CENTER, pady=5, padx=5)
    choice_buttons.append(choice)

question_number_label = Label(frame, text=f"Question 1 of {len(questions)}", font=("Consolas", 14), anchor=W, pady=10)
question_number_label.place(x=20, y=20)

feedback = Label(frame, anchor=CENTER, pady=10, wraplength=800, justify="center", font=("Consolas", 16))
feedback.pack()

score_label = Label(frame, anchor=CENTER, pady=10, text="Score: "+str(score), font=("Consolas", 20))
score_label.pack()

next = Button(frame, text="Next", font=("Consolas", 20), state=DISABLED, command=next_question)
next.pack(pady=10)

random.shuffle(questions)
current_question = 0

show_question()

window.mainloop()