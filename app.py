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
        self.configure(background="#2c313a", highlightcolor="#1f7db7")
        self.frame = Canvas(
            bg="#404040",
            bd=0,
            highlightbackground="#100100100",
            width=300,
            height=300)
        self.frame.place(relx=0.2, rely=0.15)

        self.frame2 = Canvas(
            bg="#307070",
            bd=0,
            highlightbackground="#100100100",
            width=20,
            height=20)

        self.run_btn = Button(
            master=self,
            width=27,
            bg="#404040",
            fg="#f0f0f0",
            relief='groove',
            font=("Consoles", 11, 'bold'),
            text='\u23F5 Start   ',
            command=self.run_btn_action
        )
        self.run_btn.place(relx=0.24, rely=0.05, width=265, height=40)

        self.information = LabelFrame(
            master=self,
            bg="#404040",
            fg="#f0f0f0",
            text='Information',
            font=("Consoles", 11, 'bold')
        )
        self.information.place(relx=0.225, rely=0.78, width=280, height=90)

    def run_btn_action(self):
        Logic()

    def paint_board(self, grid, sign_rows, sign_cols):
        y = 0.23
        for i in range(0, 5):
            x = 0.275
            for j in range(0, 5):
                self.frame2 = Canvas(
                    bg="#307070",
                    bd=0,
                    highlightbackground="#100100100",
                    width=20,
                    height=20)
                self.frame2.create_text(10, 10, text=grid[i][j], fill="black")
                self.frame2.place(relx=x, rely=y)
                x += 0.1
            y += 0.1

        y = 0.23
        for i in range(len(sign_rows)):
            x = 0.325
            for j in range(len(sign_rows[i])):
                self.row_signs_frame = Canvas(
                    bg="#404040",
                    bd=0,
                    highlightbackground="#404040",
                    width=20,
                    height=20)
                self.row_signs_frame.create_text(10, 10, text=sign_rows[i][j], fill="black", font='bold')
                self.row_signs_frame.place(relx=x, rely=y)
                x += 0.1
            y += 0.1

        y = 0.28
        for i in range(len(sign_cols)):
            x = 0.275
            for j in range(len(sign_cols[i])):
                self.col_signs_frame = Canvas(
                    bg="#404040",
                    bd=0,
                    highlightbackground="#404040",
                    width=20,
                    height=20)
                self.col_signs_frame.create_text(10, 10, text=sign_cols[i][j], fill="black", font='bold')
                self.col_signs_frame.place(relx=x, rely=y)
                x += 0.1
            y += 0.1