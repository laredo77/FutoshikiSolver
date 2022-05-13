from tkinter import *
from logic import Logic


def createEntry(master, default_value):
    entry = Entry(
        master=master,
        font=("Consoles", 11, 'bold'),
        width=7,
        bg="#181818",
        fg="#f0f0f0",
        justify='center'
    )
    entry.insert(0, default_value)
    return entry


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('500x500')
        self.minsize(500, 500)
        self.maxsize(500, 500)
        self.title('Futoshiki')
        self.configure(background="#2c313a", highlightcolor="#1f7db7")
        self.logic = Logic(self)
        self.frame = Canvas(
            bg="#404040",
            bd=0,
            highlightbackground="#100100100",
            width=300,
            height=300)
        self.frame.place(relx=0.2, rely=0.13)

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
        self.run_btn.place(relx=0.24, rely=0.025, width=265, height=40)

    def run_btn_action(self):
        self.logic.main_loop()

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

    def paint_info(self, current_generation, best_sol, worst_sol):

        self.information = LabelFrame(
            master=self,
            bg="#404040",
            fg="#f0f0f0",
            text='Information',
            font=("Consoles", 11, 'bold')
        )
        self.information.place(relx=0.05, rely=0.75, width=450, height=120)

        Label(
            master=self.information,
            font=("Consoles", 9, 'bold'),
            bg="#404040",
            fg="#f0f0f0",
            text='Generation:'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.generation_entry = createEntry(self.information, current_generation)
        self.generation_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        Label(
            master=self.information,
            font=("Consoles", 9, 'bold'),
            bg="#404040",
            fg="#f0f0f0",
            text='# Of unsatisfaction constraints for best solution:'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.usc_best_sol = createEntry(self.information, best_sol)
        self.usc_best_sol.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        Label(
            master=self.information,
            font=("Consoles", 9, 'bold'),
            bg="#404040",
            fg="#f0f0f0",
            text='# Of unsatisfaction constraints for worst solution:'
        ).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.usc_worst_sol = createEntry(self.information, worst_sol)
        self.usc_worst_sol.grid(row=2, column=1, padx=5, pady=5, sticky='w')