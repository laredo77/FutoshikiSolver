# Itamar Laredo
from tkinter import *
from tkinter import filedialog
from futoshiki import FutoshikiSolver

# app dimensions
DIMENSIONS = ["5", "500x500", "500", "300", "0.2 0.13", "0.24 0.025", "0.275 0.23 0.325 0.23 0.275 0.28",
              "0.05 0.75", "0.017 0.25",
              "6", "550x550", "550", "350", "0.17 0.1", "0.25 0.01", "0.21 0.15 0.26 0.15 0.21 0.2",
              "0.099 0.752", "0.017 0.25",
              "7", "650x650", "650", "450", "0.15 0.08", "0.28 0.01", "0.18 0.1 0.23 0.1 0.18 0.15",
              "0.15 0.8", "0.017 0.25"]

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

"""
Create a GUI for the board game.
Initialize buttons and their location on the frame.
"""
class App(Tk):
    def __init__(self, size):
        super().__init__()
        if size == 5:
            line = 1
        elif size == 6:
            line = 10
        else:
            line = 19

        self.geometry(DIMENSIONS[line].strip('\n'))
        self.minsize(int(DIMENSIONS[line+1].strip('\n')), int(DIMENSIONS[line+1].strip('\n')))
        self.maxsize(int(DIMENSIONS[line+1].strip('\n')), int(DIMENSIONS[line+1].strip('\n')))
        self.title('Futoshiki')
        self.configure(background="#2c313a", highlightcolor="#1f7db7")
        self.method_flag = 0
        self.input = ""
        self.solver = FutoshikiSolver(self)
        self.frame = Canvas(
            bg="#404040",
            bd=0,
            highlightbackground="#100100100",
            width=int(DIMENSIONS[line+2].strip('\n')),
            height=int(DIMENSIONS[line+2].strip('\n')))
        frame_pos = DIMENSIONS[line+3].split()
        self.frame.place(relx=float(frame_pos[0]), rely=float(frame_pos[1]))

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
            highlightbackground="#100100100",
            relief='groove',
            font=("Consoles", 11, 'bold'),
            text='\u23F5 Start   ',
            command=self.run_btn_action
        )
        run_btn_pos = DIMENSIONS[line+4].split()
        self.run_btn.place(relx=float(run_btn_pos[0]), rely=float(run_btn_pos[1]), width=265, height=40)

        self.darwin_btn = Button(
            master=self,
            width=27,
            bg="#404040",
            fg="#f0f0f0",
            highlightbackground="#100100100",
            relief='groove',
            font=("Consoles", 7, 'bold'),
            text='Darwin Method',
            command=self.darwin_btn_action
        )
        darwin_btn_pos = DIMENSIONS[line+7].split()
        self.darwin_btn.place(relx=float(darwin_btn_pos[0]), rely=float(darwin_btn_pos[1]), width=80, height=40)

        self.lamarck_btn = Button(
            master=self,
            width=27,
            bg="#404040",
            fg="#f0f0f0",
            highlightbackground="#100100100",
            relief='groove',
            font=("Consoles", 7, 'bold'),
            text='Lamarck Method',
            command=self.lamarck_btn_action
        )
        self.lamarck_btn.place(relx=float(darwin_btn_pos[0]), rely=float(darwin_btn_pos[1]) + 0.1, width=80, height=40)

        self.regular_btn = Button(
            master=self,
            width=27,
            bg="#404040",
            fg="#f0f0f0",
            highlightbackground="#100100100",
            relief='groove',
            font=("Consoles", 7, 'bold'),
            text='Regular Method',
            command=self.regular_btn_action
        )
        self.regular_btn.place(relx=float(darwin_btn_pos[0]), rely=float(darwin_btn_pos[1]) + 0.2, width=80, height=40)

        self.args_btn = Button(
            master=self,
            width=27,
            bg="#404040",
            fg="#f0f0f0",
            highlightbackground="#100100100",
            relief='groove',
            font=("Consoles", 7, 'bold'),
            text='Add args',
            command=self.open_txt
        )
        self.args_btn.place(relx=0.01, rely=0.02, width=80, height=40)

        self.lines_pos = DIMENSIONS[line+5].split()
        self.information_pos = DIMENSIONS[line+6].split()

    def open_txt(self):
        text_file = filedialog.askopenfilename(initialdir="./", title="Open Text File", filetypes=(("Text Files", "*.txt"), ))
        text_file = open(text_file, 'r')
        txt = text_file.read()
        self.solver.initialize_app(txt)
        text_file.close()

    def run_btn_action(self):
        if not self.method_flag:
            return
        self.solver.main_loop()

    def darwin_btn_action(self):
        if self.method_flag:
            return
        self.method_flag = 1
        self.solver.darwin = 1

    def lamarck_btn_action(self):
        if self.method_flag:
            return
        self.method_flag = 1
        self.solver.lamarck = 1

    def regular_btn_action(self):
        if self.method_flag:
            return
        self.method_flag = 1
        self.solver.lamarck = 1

    def paint_board(self, grid, sign_rows, sign_cols):
        y = float(self.lines_pos[1])
        for i in range(0, len(grid)):
            x = float(self.lines_pos[0])
            for j in range(0, len(grid)):
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

        y = float(self.lines_pos[3])
        for i in range(len(sign_rows)):
            x = float(self.lines_pos[2])
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

        y = float(self.lines_pos[5])
        for i in range(len(sign_cols)):
            x = float(self.lines_pos[4])
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
            highlightbackground="#100100100",
            text='Information',
            font=("Consoles", 11, 'bold')
        )
        self.information.place(relx=float(self.information_pos[0]), rely=float(self.information_pos[1]), width=450, height=120)

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