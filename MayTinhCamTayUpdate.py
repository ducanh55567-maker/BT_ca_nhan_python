import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg="#121212")  
        
        self.display = tk.Entry(
            root,
            font=('Arial', 28),
            borderwidth=0,
            justify='right',
            bg="#1e1e1e",
            fg="white",
            insertbackground="white"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

        buttons = [
            (' ', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('⌫', 1, 3),
            ('1/x', 2, 0), ('x²', 2, 1), ('√x', 2, 2), ('÷', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('+/-', 6, 0), ('0', 6, 1), ('.', 6, 2), ('=', 6, 3)
        ]

        for (text, row, col) in buttons:
            action = lambda x=text: self.on_click(x)

            
            bg = "#2c2c2c"  
            fg = "white"

            if text in ["+", "-", "×", "÷"]:
                bg = "#ff9500" 
            elif text == "=":
                bg = "#00c853"  
            elif text in ["C", "CE"]:
                bg = "#d32f2f"  
            elif text == "⌫":
                bg = "#7b1fa2"  
            elif text in ["1/x", "x²", "√x", "+/-"]:
                bg = "#455a64"  

            btn = tk.Button(
                root,
                text=text,
                font=('Arial', 16, 'bold'),
                bg=bg,
                fg=fg,
                activebackground="#00adb5",
                activeforeground="white",
                borderwidth=0,
                command=action
            )

            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        for i in range(7):
            root.grid_rowconfigure(i, weight=1)

        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def on_click(self, char):
        try:
            if char == "=":
                res = self.display.get().replace('×', '*').replace('÷', '/')
                result = eval(res)
                self.update_display(result)

            elif char == "C":
                self.update_display("")

            elif char == "CE":
                expr = self.display.get()
                if not expr:
                    return

                if expr[-1].isdigit() or expr[-1] == '.':
                    i = len(expr) - 1
                    while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):
                        i -= 1
                    self.update_display(expr[:i+1])
                else:
                    self.update_display(expr[:-1])

            elif char == "⌫":
                self.update_display(self.display.get()[:-1])

            elif char == "x²":
                val = float(self.display.get())
                self.update_display(val ** 2)

            elif char == "√x":
                val = float(self.display.get())
                self.update_display(math.sqrt(val))

            elif char == "1/x":
                val = float(self.display.get())
                self.update_display(1 / val)

            elif char == "+/-":
                val = float(self.display.get())
                self.update_display(val * -1)

            else:
                self.display.insert(tk.END, char)

        except:
            messagebox.showerror("Lỗi", "Phép tính không hợp lệ")
            self.update_display("")

    def update_display(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, text)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("320x450")
    Calculator(root)
    root.mainloop()