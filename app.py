# Itamar Laredo, 311547087
from tkinter import *
from futoshiki import FutoshikiSolver


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
    def __init__(self, size):
        super().__init__()
        with open('dimentions.txt') as file:
            lines = file.readlines()
        if size == 5:
            line = 1
        elif size == 6:
            line = 10
        else:
            line = 19
        self.geometry(lines[line].strip('\n'))
        self.minsize(int(lines[line+1].strip('\n')), int(lines[line+1].strip('\n')))
        self.maxsize(int(lines[line+1].strip('\n')), int(lines[line+1].strip('\n')))
        self.title('Futoshiki')
        self.configure(background="#2c313a", highlightcolor="#1f7db7")
        self.solver = FutoshikiSolver(self)
        self.method_flag = 0
        self.frame = Canvas(
            bg="#404040",
            bd=0,
            highlightbackground="#100100100",
            width=int(lines[line+2].strip('\n')),
            height=int(lines[line+2].strip('\n')))
        frame_pos = lines[line+3].split()
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
        run_btn_pos = lines[line+4].split()
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
        darwin_btn_pos = lines[line+7].split()
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

        self.lines_pos = lines[line+5].split()
        self.information_pos = lines[line+6].split()

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