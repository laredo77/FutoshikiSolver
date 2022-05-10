import random
import itertools
from tkinter import *
from tkinter.font import Font


class Logic:
    def __init__(self):
        with open('input.txt') as file:
            lines = file.readlines()

        self.SIZE = int(lines[0].strip('\n'))
        self.matrix_size = self.SIZE * 2 - 1
        NUM_OF_DIGITS = int(lines[1].strip('\n'))
        COORDINATES_OF_GIVEN_DIGIT = []
        for i in range(0, NUM_OF_DIGITS):
            COORDINATES_OF_GIVEN_DIGIT.append(lines[i + 2].strip('\n'))

        NUM_OF_GRATER_THEN_SIGN = int(lines[NUM_OF_DIGITS + 2].strip('\n'))
        COORDINATES_OF_GREATER_THEN_SIGN = []
        for i in range(0, NUM_OF_GRATER_THEN_SIGN):
            COORDINATES_OF_GREATER_THEN_SIGN.append(lines[i + NUM_OF_DIGITS + 3].strip('\n'))

        self.grid = [["0" for i in range(self.SIZE)] for j in range(self.SIZE)]
        for coordinate in COORDINATES_OF_GIVEN_DIGIT:
            coordinate = coordinate.split()
            self.grid[int(coordinate[0]) - 1][int(coordinate[1]) - 1] = coordinate[2]

        self.sign_grid_by_row = [["" for i in range(self.SIZE)] for j in range(self.SIZE)]
        self.sign_grid_by_col = [["" for i in range(self.SIZE)] for j in range(self.SIZE)]
        for coordinate in COORDINATES_OF_GREATER_THEN_SIGN:
            coordinate = coordinate.split()
            if coordinate[0] == coordinate[2]:
                if coordinate[1] > coordinate[3]:
                    self.sign_grid_by_row[int(coordinate[0]) - 1][int(coordinate[3]) - 1] = "<"
                else:
                    self.sign_grid_by_row[int(coordinate[0]) - 1][int(coordinate[1]) - 1] = ">"
            else:
                if coordinate[0] > coordinate[2]:
                    self.sign_grid_by_col[int(coordinate[2]) - 1][int(coordinate[1]) - 1] = "/\\"
                else:
                    self.sign_grid_by_col[int(coordinate[0]) - 1][int(coordinate[3]) - 1] = "\/"

        del self.sign_grid_by_col[-1]
        for i in range(len(self.sign_grid_by_row)):
            del self.sign_grid_by_row[i][-1]

        self.initialize_first_generation()
        self.paint_board(self.grid, self.sign_grid_by_row, self.sign_grid_by_col)

    def paint_board(self, grid, sign_rows, sign_cols):

        y = 0.22
        for i in range(0, 5):
            x = 0.25
            for j in range(0, 5):
                self.frame = Canvas(
                    bg="#307070",
                    bd=0,
                    highlightbackground="#100100100",
                    width=20,
                    height=20)
                self.frame.create_text(10, 10, text=grid[i][j], fill="black")
                self.frame.place(relx=x, rely=y)
                x += 0.1
            y += 0.1


        y = 0.22
        for i in range(len(sign_rows)):
            x = 0.3
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

        y = 0.27
        for i in range(len(sign_cols)):
            x = 0.25
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

    def initialize_first_generation(self):
        new_grid = self.grid
        nums = []
        for i in range(1, self.SIZE + 1):
            nums.append(i)
        permutations = list(itertools.permutations(nums))
        for i in range(0, self.SIZE):
            permutation = list(permutations[random.randrange(len(permutations))])
            for j in range(0, self.SIZE):
                if new_grid[i][j].isdigit() and new_grid[i][j] != "0":
                    permutation.remove(int(new_grid[i][j]))
            for j in range(0, self.SIZE):
                if new_grid[i][j] == "0":
                    new_grid[i][j] = permutation[0]
                    permutation.pop(0)
        self.grid = new_grid

