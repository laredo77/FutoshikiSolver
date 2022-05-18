# Itamar Laredo, 311547087
import random
import itertools
from matplotlib import pyplot as plt
import numpy as np

MUTATE = 0.00
ELITE = 0.15
NEW_MATRICES = 0.35
NUM_OF_SOLUTIONS = 100
MAX_ITERATIONS = 1200


class FutoshikiSolver:
    def __init__(self, app):
        with open('input.txt') as file:
            lines = file.readlines()

        self.app = app
        self.size = int(lines[0].strip('\n'))
        self.num_of_digits = int(lines[1].strip('\n'))
        self.coordinates_of_given_digits = []
        for i in range(0, self.num_of_digits):
            self.coordinates_of_given_digits.append(lines[i + 2].strip('\n'))

        self.num_of_greater_then_sign = int(lines[self.num_of_digits + 2].strip('\n'))
        self.coordinates_of_greater_then_sign = []
        for i in range(0, self.num_of_greater_then_sign):
            self.coordinates_of_greater_then_sign.append(lines[i + self.num_of_digits + 3].strip('\n'))

        self.generation = []
        first_generation_matrices = self.generate_matrices(NUM_OF_SOLUTIONS)
        self.generation = self.fitness(first_generation_matrices)
        self.data = []
        self.darwin = 0
        self.lamarck = 0
        self.regular = 0

    def fitness(self, matrices):
        returned_matrices = []
        for matrix in matrices:
            penalty = 0
            matrix_rows = []
            for i in range(0, self.size):
                row = []
                for j in range(0, self.size):
                    row.append(matrix[0][i][j])
                matrix_rows.append(row)

            for row in matrix_rows:
                unique_row = list(set(row))
                penalty += (self.size - len(unique_row))

            matrix_cols = []
            for i in range(0, self.size):
                col = []
                for j in range(0, self.size):
                    col.append(matrix[0][j][i])
                matrix_cols.append(col)

            for col in matrix_cols:
                unique_col = list(set(col))
                penalty += (self.size - len(unique_col))

            for i in range(len(matrix[1])):
                for j in range(len(matrix[1][0])):
                    sign = matrix[1][i][j]
                    if sign != "":
                        if sign == "<":
                            if int(matrix[0][i][j]) >= int(matrix[0][i][j + 1]):
                                penalty += 1
                        elif sign == ">":
                            if int(matrix[0][i][j]) <= int(matrix[0][i][j + 1]):
                                penalty += 1

            for i in range(len(matrix[2])):
                for j in range(len(matrix[2][0])):
                    sign = matrix[2][i][j]
                    if sign != "":
                        if sign == "\/":
                            if matrix[0][i][j] <= matrix[0][i + 1][j]:
                                penalty += 1
                        elif sign == "/\\":
                            if matrix[0][i][j] >= matrix[0][i + 1][j]:
                                penalty += 1

            temp = list(matrix)
            temp[3] = penalty
            returned_matrices.append(tuple(temp))
        return returned_matrices

    def generate_matrices(self, amount):
        matrices = []
        for i in range(0, amount):
            grid = [["0" for i in range(self.size)] for j in range(self.size)]
            for coordinate in self.coordinates_of_given_digits:
                coordinate = coordinate.split()
                grid[int(coordinate[0]) - 1][int(coordinate[1]) - 1] = int(coordinate[2])

            sign_grid_by_row = [["" for i in range(self.size)] for j in range(self.size)]
            sign_grid_by_col = [["" for i in range(self.size)] for j in range(self.size)]
            for coordinate in self.coordinates_of_greater_then_sign:
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
            for j in range(len(sign_grid_by_row)):
                del sign_grid_by_row[j][-1]

            nums = list(range(1, self.size + 1))
            permutations = list(itertools.permutations(nums))
            for k in range(0, self.size):
                permutation = list(permutations[random.randrange(len(permutations))])
                for j in range(0, self.size):
                    if grid[k][j] != "0":
                        permutation.remove(int(grid[k][j]))
                for j in range(0, self.size):
                    if grid[k][j] == "0":
                        grid[k][j] = permutation[0]
                        permutation.pop(0)
            grade = 0
            matrices.append((grid, sign_grid_by_row, sign_grid_by_col, grade))

        return matrices

    def crossover(self, matrices):
        return_matrices = []
        random.shuffle(matrices)
        for i in range(0, len(matrices) - 1):
            new_matrix = []
            partition = random.randint(0, self.size)
            for j in range(0, partition):
                new_matrix.append(matrices[i][0][j])

            for j in range(partition, self.size):
                new_matrix.append(matrices[i + 1][0][j])

            return_matrices.append((new_matrix, matrices[i][1], matrices[i][2], matrices[i][3]))
        return_matrices.append(matrices[0])
        return return_matrices

    def mutation(self, matrices):
        for i in range(len(matrices)):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            mutate = random.randint(0, self.size - 1)
            matrices[i][0][row][col], matrices[i][0][row][mutate] = matrices[i][0][row][mutate], matrices[i][0][row][col]
        return matrices

    def lamarckism(self, matrices):
        returned_matrices = []
        for matrix in matrices:
            for i in range(0, len(matrix[1])):
                for j in range(0, len(matrix[1][0])):
                    sign = matrix[1][i][j]
                    if sign != "":
                        if sign == "<":
                            if int(matrix[0][i][j]) >= int(matrix[0][i][j + 1]):
                                matrix[0][i][j], matrix[0][i][j + 1] = int(matrix[0][i][j + 1]), int(matrix[0][i][j])
                        elif sign == ">":
                            if int(matrix[0][i][j]) <= int(matrix[0][i][j + 1]):
                                matrix[0][i][j], matrix[0][i][j + 1] = int(matrix[0][i][j + 1]), int(matrix[0][i][j])

            returned_matrices.append(matrix)
        return returned_matrices

    def main_loop(self):
        current_generation = 1
        while True:
            self.generation.sort(key=lambda tup: tup[3])
            if (current_generation % 100) == 0:
                self.data.append((self.generation[0][3], self.generation[int(NUM_OF_SOLUTIONS/2)][3],
                                self.generation[NUM_OF_SOLUTIONS - 1][3], current_generation))
            if self.generation[0][3] == 0 or current_generation == MAX_ITERATIONS:
                self.app.paint_board(self.generation[0][0], self.generation[0][1], self.generation[0][2])
                self.app.paint_info(current_generation, self.generation[0][3], self.generation[NUM_OF_SOLUTIONS - 1][3])
                self.plot()
                break
            next_generation = []
            for i in range(0, int(NUM_OF_SOLUTIONS * ELITE)):
                next_generation.append(self.generation[i])

            num_of_new_matrices = int((NUM_OF_SOLUTIONS / 2) - int(NUM_OF_SOLUTIONS * ELITE))
            new_matrices = self.generate_matrices(num_of_new_matrices)
            for i in range(0, num_of_new_matrices):
                next_generation.append(new_matrices[i])

            crossed_matrices = self.crossover(next_generation)
            for i in range(0, len(crossed_matrices)):
                next_generation.append(crossed_matrices[i])

            temp = []
            random.shuffle(next_generation)
            for i in range(0, int(NUM_OF_SOLUTIONS * MUTATE)):
                temp.append(next_generation[i])
            mutate_matrices = self.mutation(temp)
            for i in range(0, int(NUM_OF_SOLUTIONS * MUTATE)):
                next_generation[i] = mutate_matrices[i]

            if self.darwin:
                darwin_next_generation = next_generation
                next_generation = self.lamarckism(next_generation) # Optional: Lamarckism
                next_generation = self.fitness(next_generation)
                self.generation = next_generation
            elif self.lamarck:
                next_generation = self.lamarckism(next_generation)  # Optional: Lamarckism
                self.generation = self.fitness(next_generation)
            elif self.regular:
                self.generation = self.fitness(next_generation)

            current_generation += 1

    def plot(self):
        plt.figure()
        plt.title('Graph')
        plt.xlabel('# Generation x 100')
        plt.ylabel('# Amount of unsetesfaction constraints')
        best_sol = []
        avg_sol = []
        wst_sol = []
        cur_gen = []

        for i in range(0, len(self.data)):
            best_sol.append(self.data[i][0])
            avg_sol.append(self.data[i][1])
            wst_sol.append(self.data[i][2])
            cur_gen.append(self.data[i][3])

        x_axis = np.arange(len(cur_gen))
        ax = plt.subplot(111)
        w = 0.3
        ax.bar(x_axis - w, wst_sol, width=w, color='r', align='center', label="Worst")
        ax.bar(x_axis, avg_sol, width=w, color='g', align='center', label="Average")
        ax.bar(x_axis + w, best_sol, width=w, color='b', align='center', label="Best")
        plt.legend()
        plt.savefig('./graph.png')
        plt.show()
