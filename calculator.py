import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.current = "0"
        self.previous = None
        self.operation = None
        self.replace_current = True
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.display_var = tk.StringVar(value=self.current)
        display = ttk.Entry(main_frame, textvariable=self.display_var, 
                           font=("Arial", 16), state="readonly", justify="right")
        display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for button_info in buttons:
            text = button_info[0]
            row = button_info[1]
            col = button_info[2]
            colspan = button_info[3] if len(button_info) > 3 else 1
            
            if text in '0123456789.':
                cmd = lambda t=text: self.number_click(t)
            elif text in '+-*/%':
                cmd = lambda t=text: self.operation_click(t)
            elif text == '=':
                cmd = self.equals_click
            elif text == 'C':
                cmd = self.clear_click
            elif text == '±':
                cmd = self.sign_click
            
            btn = ttk.Button(main_frame, text=text, command=cmd, width=5)
            btn.grid(row=row, column=col, columnspan=colspan, 
                    sticky="ew", padx=2, pady=2)
        
        for i in range(4):
            main_frame.columnconfigure(i, weight=1)
    
    def number_click(self, number):
        if self.replace_current:
            self.current = number
            self.replace_current = False
        else:
            if number == '.' and '.' in self.current:
                return
            self.current += number
        
        self.display_var.set(self.current)
    
    def operation_click(self, op):
        if self.previous is not None and not self.replace_current:
            self.calculate()
        
        self.previous = float(self.current)
        self.operation = op
        self.replace_current = True
    
    def equals_click(self):
        if self.previous is not None and self.operation:
            self.calculate()
            self.operation = None
            self.previous = None
            self.replace_current = True
    
    def calculate(self):
        try:
            current_val = float(self.current)
            
            if self.operation == '+':
                result = self.previous + current_val
            elif self.operation == '-':
                result = self.previous - current_val
            elif self.operation == '*':
                result = self.previous * current_val
            elif self.operation == '/':
                if current_val == 0:
                    self.current = "Помилка"
                    self.display_var.set(self.current)
                    return
                result = self.previous / current_val
            elif self.operation == '%':
                result = self.previous % current_val
            else:
                return
            
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 8))
            
            self.display_var.set(self.current)
            
        except:
            self.current = "Помилка"
            self.display_var.set(self.current)
    
    def clear_click(self):
        self.current = "0"
        self.previous = None
        self.operation = None
        self.replace_current = True
        self.display_var.set(self.current)
    
    def sign_click(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display_var.set(self.current)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()