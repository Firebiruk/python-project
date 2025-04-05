from tkinter import *
import math

def press(num):
    global equation
    if num in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
        equation += f"{num}("
    elif num == 'x!':
        equation += "x!("
    elif num == 'Ans':
        equation += last_answer
    else:
        equation += str(num)
    equation_text.set(equation)
    
def equals():
    global equation, last_answer
    try:
        open_parentheses = equation.count('(')
        close_parentheses = equation.count(')')
        if open_parentheses > close_parentheses:
            expression += ')' * (open_parentheses - close_parentheses)
        equation = equation.replace('x!', 'math.factorial')
        equation = equation.replace('√', 'math.sqrt')
        equation = equation.replace('sin', 'math.sin')
        equation = equation.replace('cos', 'math.cos')
        equation = equation.replace('tan', 'math.tan')
        equation = equation.replace('log', 'math.log10')
        equation = equation.replace('ln', 'math.log')
        equation = equation.replace('Rad', 'math.radians')
        equation = equation.replace('Deg', 'math.degrees')
        equation = equation.replace('π', 'math.pi')
        equation = equation.replace('e', 'math.e')
        equation = equation.replace('^', '**')
        equation = equation.replace('EXP', 'math.exp')
        equation = equation.replace('Inv', '1/')
        
        
        result = str(eval(equation))
        equation_text.set(result)
        equation = ''
    except:
        equation_text.set("Error")
        equation = ""

def clear():
    global equation
    equation = equation[:-1]
    equation_text.set(equation)

def clear_all():
    global equation
    equation = ''
    equation_text.set("")

window = Tk()
window.title("Scientific Calculator")
window.geometry("1000x1000")
window.config(bg="#0a0a0a")
window.resizable(0, 0)

equation = ""
equation_text = StringVar()
buttons = ['AC', 'C', '(', ')', 'x!', 'Rad', 'Deg',
           '7', '8', '9', '/', 'ln', 'sin', 'Inv',
           '4', '5', '6', '*', 'log', 'cos', 'π',
           '1', '2', '3', '-', '√', 'tan', 'e',
           '0', '.', '=', '+', '^', 'EXP', 'Ans']
operators = ['+', '-', '*', '/', '^', 'x!', '(', ")", '√', 'sin', 'cos', 'tan', 'log', 'ln', 'EXP', 'Rad', 'Deg', 'Inv', 'π', 'e', 'Ans']
row=0
column=1

last_answer = ''

equation_label = Label(window, textvariable=equation_text, font=("Courier new", 17, "bold"), bg="#000", fg="#FFF", width=52, height=3)
equation_label.pack()

frame = Frame(window)
frame.pack()

for i in buttons:
    button = Button(frame, text=i, font=("Courier new", 15, "bold"), fg="white", bg="black", width=8, height=4, command=lambda i=i: press(i))
    button.grid(row=row, column=column)
    column+=1
    if column>7:
        column=1
        row+=1
    if i in operators:
        button.config(bg="green")
    elif i == '=':
        button.config(bg="#fb7c14", command=equals)
    elif i == 'AC' or i == 'C':
        if i == 'AC':
            command = clear_all
        else:
            command=clear
        button.config(bg="blue", command=command)

    

window.mainloop()