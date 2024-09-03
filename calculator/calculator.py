from tkinter import *
import math

form = Tk()
W, H = 410, 480
L, T = (form.winfo_screenwidth() - W) // 2, (form.winfo_screenheight() - H) // 2
form.geometry(f"{W}x{H}+{L}+{T}")
form.title('Калькулятор')
form.configure(bg="#38373E")

field = Label(form, text='', font=("arial", 20), bg='gray')
field.grid(row=0, column=0, columnspan=4, sticky='nsew')

buttons = ['%', '√', 'x²', '1/x',
           'CE', 'C', '←', '÷',
           '7', '8', '9', 'x',
           '4', '5', '6', '-',
           '1', '2', '3', '+',
           '+/-', '0', '.', '=']

firstNumber = secondNumber = result = operator = ""


def cut(digit):
    global result
    result = str(digit)
    if result.endswith(".0"):
        result = result[:-2]
    return result

def calculations():
    global firstNumber, secondNumber, result, operator
    if operator == "+":
        result = float(secondNumber) + float(firstNumber)
    elif operator == "-":
        result = float(secondNumber) - float(firstNumber)
    elif operator == "x":
        result = float(secondNumber) * float(firstNumber)
    elif operator == "÷":
        result = float(secondNumber) / float(firstNumber)
    return cut(result)


def buttonclick(x):
    global firstNumber, secondNumber, operator, result
    if x.isdigit() or x == ".":
        firstNumber += x
        field.config(text=firstNumber)
    elif x == "%":
        firstNumber = cut(float(firstNumber)/100)
        field.config(text=firstNumber)
    elif x == "√":
        field.config(text=f"√ {firstNumber}")
        result = math.sqrt(float(firstNumber))
    elif x == "x²":
        field.config(text=f"{firstNumber}²")
        result = float(firstNumber) ** 2
    elif x == "1/x":
        field.config(text=f"1/{firstNumber}")
        result = 1 / float(firstNumber)
    elif x == "CE":
        firstNumber, result = "", ""
        field.config(text=firstNumber)
    elif x == "C":
        firstNumber = secondNumber = result = ""
        field.config(text=result)
    elif x == "←":
        firstNumber = firstNumber[0:-1]
        field.config(text=firstNumber)
    elif x in ["+", "-", "x", "÷"]:
        field.config(text=f"{firstNumber} {x}")
        secondNumber, firstNumber, operator = firstNumber, "", x
    elif x == "+/-":
        firstNumber = str(cut((-1 * float(firstNumber))))
        field.config(text=firstNumber)
    elif x == "=":
        result = calculations()
        field.config(text=result)
        firstNumber = result
        operator = ""


row = 1
col = 0
for button in buttons:
    getButton = (Button(text=button, font=('arial', 16), bg="#444341", command=lambda x=button: buttonclick(x))
                 .grid(row=row, column=col, sticky='nsew'))
    col += 1
    if col > 3:
        col = 0
        row += 1

for columns in range(4):
    form.columnconfigure(index=columns, weight=1)
for rows in range(7):
    form.rowconfigure(index=rows, weight=1)

form.mainloop()
