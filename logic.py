import random
import itertools
import app

MUTATE = 0.05
ELITE = 0.4
NEW_MATRICES = 0.1
NUM_OF_SOLUTIONS = 100


class Logic:
    def __init__(self):
        with open('input.txt') as file:
            lines = file.readlines()

        self.size = int(lines[0].strip('\n'))
        self.matrix_size = self.size * 2 - 1
        self.num_of_digits = int(lines[1].strip('\n'))
        self.coordinates_of_given_digits = []
        for i in range(0, self.num_of_digits):
            self.coordinates_of_given_digits.append(lines[i + 2].strip('\n'))

        self.num_of_greater_then_sign = int(lines[self.num_of_digits + 2].strip('\n'))
        self.coordinates_of_greater_then_sign = []
        for i in range(0, self.num_of_greater_then_sign):
            self.coordinates_of_greater_then_sign.append(lines[i + self.num_of_digits + 3].strip('\n'))

        self.generation = []
        self.initialize_first_generation()
        self.main_loop()

    def initialize_first_generation(self):
        self.generation = self.generate_matrices(100)
        self.fitness()

    def fitness(self):
        k = 0
        for matrix in self.generation:
            penalty = 0
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
            for i in range(len(sign_grid_by_row)):
                del sign_grid_by_row[i][-1]

            nums = list(range(1, self.size +1))
            permutations = list(itertools.permutations(nums))
            for i in range(0, self.size):
                permutation = list(permutations[random.randrange(len(permutations))])
                for j in range(0, self.size):
                    if grid[i][j] != "0":
                        permutation.remove(int(grid[i][j]))
                for j in range(0, self.size):
                    if grid[i][j] == "0":
                        grid[i][j] = permutation[0]
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
            mutate = random.randint(1, self.size - 1)
            temp = matrices[i][0][row][col]
            matrices[i][0][row][col] = matrices[i][0][row][mutate]
            matrices[i][0][row][mutate] = temp
        return matrices

    def main_loop(self):
        current_generation = 1
        while True:
            if self.generation[0][3] == 0:
                app.App.paint_board(self, self.generation[0][0], self.generation[0][1], self.generation[0][2])
                print(current_generation)
                #add information
                break

            next_generation = []
            # fix the number to be fixed
            for i in range(0, 40): # 30% of best result in the last generation (should work without fixed number)
                next_generation.append(self.generation[i])

            # fix the number to be fixed
            new_matrices = self.generate_matrices(10)
            for i in range(0, 10):
                next_generation.append(new_matrices[i])

            crossed_matrices = self.crossover(next_generation)
            for i in range(0, len(crossed_matrices)):
                next_generation.append(crossed_matrices[i])

            # fix the number to be fixed
            temp = []
            random.shuffle(next_generation)
            for i in range(0, 20):
                temp.append(next_generation[i])
            mutate_matrices = self.mutation(temp)
            for i in range(0, 20):
                next_generation[i] = mutate_matrices[i]

            self.generation = next_generation
            self.fitness()
            self.generation.sort(key=lambda tup: tup[3])
            if current_generation == 1200:
                app.App.paint_board(self, self.generation[0][0], self.generation[0][1], self.generation[0][2])
                print(self.generation[0][3])
                print("current generation is 1200, quiting")
                print(self.generation[99][3])
                break

            current_generation += 1