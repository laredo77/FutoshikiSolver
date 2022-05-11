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
        self.NUM_OF_DIGITS = int(lines[1].strip('\n'))
        self.COORDINATES_OF_GIVEN_DIGIT = []
        for i in range(0, self.NUM_OF_DIGITS):
            self.COORDINATES_OF_GIVEN_DIGIT.append(lines[i + 2].strip('\n'))

        self.NUM_OF_GRATER_THEN_SIGN = int(lines[self.NUM_OF_DIGITS + 2].strip('\n'))
        self.COORDINATES_OF_GREATER_THEN_SIGN = []
        for i in range(0, self.NUM_OF_GRATER_THEN_SIGN):
            self.COORDINATES_OF_GREATER_THEN_SIGN.append(lines[i + self.NUM_OF_DIGITS + 3].strip('\n'))

        self.generation = []
        self.initialize_first_generation()
        self.main_loop()
        #self.paint_board(self.grid, self.sign_grid_by_row, self.sign_grid_by_col)

    # def paint_board(self, grid, sign_rows, sign_cols):
    #
    #     y = 0.22
    #     for i in range(0, 5):
    #         x = 0.25
    #         for j in range(0, 5):
    #             self.frame = Canvas(
    #                 bg="#307070",
    #                 bd=0,
    #                 highlightbackground="#100100100",
    #                 width=20,
    #                 height=20)
    #             self.frame.create_text(10, 10, text=grid[i][j], fill="black")
    #             self.frame.place(relx=x, rely=y)
    #             x += 0.1
    #         y += 0.1
    #
    #     y = 0.22
    #     for i in range(len(sign_rows)):
    #         x = 0.3
    #         for j in range(len(sign_rows[i])):
    #             self.row_signs_frame = Canvas(
    #                 bg="#404040",
    #                 bd=0,
    #                 highlightbackground="#404040",
    #                 width=20,
    #                 height=20)
    #             self.row_signs_frame.create_text(10, 10, text=sign_rows[i][j], fill="black", font='bold')
    #             self.row_signs_frame.place(relx=x, rely=y)
    #             x += 0.1
    #         y += 0.1
    #
    #     y = 0.27
    #     for i in range(len(sign_cols)):
    #         x = 0.25
    #         for j in range(len(sign_cols[i])):
    #             self.col_signs_frame = Canvas(
    #                 bg="#404040",
    #                 bd=0,
    #                 highlightbackground="#404040",
    #                 width=20,
    #                 height=20)
    #             self.col_signs_frame.create_text(10, 10, text=sign_cols[i][j], fill="black", font='bold')
    #             self.col_signs_frame.place(relx=x, rely=y)
    #             x += 0.1
    #         y += 0.1

    def initialize_first_generation(self):
        for matrix in range(0, 100):
            grid = [["0" for i in range(self.SIZE)] for j in range(self.SIZE)]
            for coordinate in self.COORDINATES_OF_GIVEN_DIGIT:
                coordinate = coordinate.split()
                grid[int(coordinate[0]) - 1][int(coordinate[1]) - 1] = int(coordinate[2])

            sign_grid_by_row = [["" for i in range(self.SIZE)] for j in range(self.SIZE)]
            sign_grid_by_col = [["" for i in range(self.SIZE)] for j in range(self.SIZE)]
            for coordinate in self.COORDINATES_OF_GREATER_THEN_SIGN:
                coordinate = coordinate.split()
                if coordinate[0] == coordinate[2]:
                    if coordinate[1] > coordinate[3]:
                        sign_grid_by_row[int(coordinate[0]) - 1][int(coordinate[3]) - 1] = "<"
                    else:
                        sign_grid_by_row[int(coordinate[0]) - 1][int(coordinate[1]) - 1] = ">"
                else:
                    if coordinate[0] > coordinate[2]:
                        sign_grid_by_col[int(coordinate[2]) - 1][int(coordinate[1]) - 1] = "/\\"
                    else:
                        sign_grid_by_col[int(coordinate[0]) - 1][int(coordinate[3]) - 1] = "\/"

            del sign_grid_by_col[-1]
            for i in range(len(sign_grid_by_row)):
                del sign_grid_by_row[i][-1]

            nums = list(range(1, self.SIZE +1))
            permutations = list(itertools.permutations(nums))
            for i in range(0, self.SIZE):
                permutation = list(permutations[random.randrange(len(permutations))])
                for j in range(0, self.SIZE):
                    if grid[i][j] != "0":
                        permutation.remove(int(grid[i][j]))
                for j in range(0, self.SIZE):
                    if grid[i][j] == "0":
                        grid[i][j] = permutation[0]
                        permutation.pop(0)
            grade = 0
            self.generation.append((grid, sign_grid_by_row, sign_grid_by_col, grade))
            self.fitness()

    def fitness(self):
        k = 0
        for matrix in self.generation:
            penalty = 0
            matrix_cols = []
            for i in range(0, self.SIZE):
                col = []
                for j in range(0, self.SIZE):
                    col.append(matrix[0][j][i])
                matrix_cols.append(col)

            for col in matrix_cols:
                unique_col = list(set(col))
                penalty += (self.SIZE - len(unique_col))

            for i in range(len(matrix[1])):
                for j in range(len(matrix[1][i])):
                    sign = matrix[1][i][j]
                    if sign != "":
                        if sign == "<":
                            if int(matrix[0][i][j]) >= int(matrix[0][i][j+1]):
                                penalty += 1
                        else:
                            if int(matrix[0][i][j]) <= int(matrix[0][i][j + 1]):
                                penalty += 1

            for i in range(len(matrix[2])):
                for j in range(len(matrix[2][i])):
                    sign = matrix[2][i][j]
                    if sign != "":
                        if sign == "\/":
                            if matrix[0][i][j] <= matrix[0][i+1][j]:
                                penalty += 1
                        else:
                            if matrix[0][i][j] >= matrix[0][i+1][j]:
                                penalty += 1
            temp = list(matrix)
            temp[3] = penalty
            self.generation[k] = tuple(temp)
            k += 1
            #self.paint_board(matrix[0], matrix[1], matrix[2])

    def main_loop(self):
        current_generation = 1
        while True:
            self.generation.sort(key=lambda tup: tup[3])
            if self.generation[0][3] == 0:
                print("finished, should quit or print solution")
                break

            next_generation = []



            current_generation += 1