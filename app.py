from tkinter import *
from tkinter.font import Font
from logic import Logic

class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('500x500')
        self.minsize(500, 500)
        self.maxsize(500, 500)
        self.title('Futoshiki')
        self.frame = Canvas(
            bg="#404040",
            bd=0,
            highlightbackground="#100100100",
            width=300,
            height=300)
        self.frame.place(relx=0.2, rely=0.15)
        Logic()
