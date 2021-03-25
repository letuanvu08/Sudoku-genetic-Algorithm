from random import choice, sample, random, randint
import numpy as np
import math
from copy import deepcopy
from functools import reduce


class Generate_board:
    _sideGrid = 3
    _side = _sideGrid**2
    _goalBoard = []

    def __init__(self, sideGrid):
        Generate_board._sideGrid = sideGrid
        Generate_board._side = Generate_board._sideGrid**2
        Generate_board._goalBoard = [
            [0 for i in range(Generate_board._side)]for j in range(Generate_board._side)]
        self.Generateboard()
        self.board_Puzzle = []
        self.Fix_board = []
        self.generate_board_Puzzle()
        # print("Goal board:")
        self.displayBoard(Generate_board._goalBoard)
        # print("Puzzle board:")
        # self.displayBoard(self.board_Puzzle)

    def pattern(self, r, c):
        return (Generate_board._sideGrid*(r % Generate_board._sideGrid)+r//Generate_board._sideGrid+c) % Generate_board._side

    def shuffle(self):
        return sample(range(1, Generate_board._side+1), Generate_board._side)

    def checkValid(self, r, c, number):
        for i in range(Generate_board._side):
            if Generate_board._goalBoard[r][i] == number | Generate_board._goalBoard[i][c] == number:
                return False
        for i in range(Generate_board._sideGrid):
            for j in range(Generate_board._sideGrid):
                if Generate_board._goalBoard[(r+i) % Generate_board._sideGrid+r//Generate_board._sideGrid][(c+j) % Generate_board._sideGrid+c//Generate_board._sideGrid] == number:
                    return False
        return True

    def Generateboard(self):
        numbers = sample(range(1, Generate_board._side+1),
                         Generate_board._side)
        Generate_board._goalBoard = [[numbers[self.pattern(row, col)]for col in range(
            Generate_board._side)]for row in range(Generate_board._side)]
        rows = [row for grid in sample(range(Generate_board._sideGrid), Generate_board._sideGrid) for row in sample(
            range(grid*Generate_board._sideGrid, (grid+1)*Generate_board._sideGrid), Generate_board._sideGrid)]
        cols = [col for grid in sample(range(Generate_board._sideGrid), Generate_board._sideGrid) for col in sample(
            range(grid*Generate_board._sideGrid, (grid+1)*Generate_board._sideGrid), Generate_board._sideGrid)]
        Generate_board._goalBoard = [
            [Generate_board._goalBoard[r][c]for c in cols] for r in rows]
        return Generate_board._goalBoard
        # for i in range(Generate_board._side):
        #     numbers=self.shuffle()
        #     col=[]
        #     for j in range(Generate_board._side):
        #         for number in numbers:
        #             if self.checkValid(i,j,number)==True:
        #                 Generate_board._goalBoard[i][j]=number
        #                 break

    def generate_board_Puzzle(self):
        self.board_Puzzle = deepcopy(Generate_board._goalBoard)
        self.Fix_board = [
            [1 for _ in range(Generate_board._side)]for _ in range(Generate_board._side)]
        squares = Generate_board._side*Generate_board._side
        empties = squares * 3//4
        for p in sample(range(squares), empties):
            self.board_Puzzle[p//Generate_board._side][p %
                                                       Generate_board._side] = 0
            self.Fix_board[p//Generate_board._side][p %
                                                    Generate_board._side] = 0

    def displayBoard(self, board):
        def expand_line(line): return line[0]+line[5:9].join(
            [line[1:5]*(Generate_board._sideGrid-1)]*Generate_board._sideGrid)+line[9:13]
        line0 = expand_line("╔═══╤═══╦═══╗")
        line1 = expand_line("║ . │ . ║ . ║")
        line2 = expand_line("╟───┼───╫───╢")
        line3 = expand_line("╠═══╪═══╬═══╣")
        line4 = expand_line("╚═══╧═══╩═══╝")

        nums = [[""] + [str(n) for n in row] for row in board]
        for r in range(1, Generate_board._side + 1):
            print(
                "".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
            print([line2, line3, line4][(r % Generate_board._side ==
                  0) + (r % Generate_board._sideGrid == 0)])

    def createCandidate(self):
        return Candidate(deepcopy(self.board_Puzzle),
                         deepcopy(self.Fix_board))


class Candidate:
    def __init__(self, board_Puzzle, Fixed_board):
        self.board = board_Puzzle
        self.Fixed_board = Fixed_board
        self.random_gen()
        self.fitness = self.update_fitness()

    def mutate(self):
        size = len(self.board)
        rows = sample(range(0, 8), 3)
        for row in rows:
            mutationsize = randint(1, 3)

            for _ in range(mutationsize):
                col = randint(0, 8)
                count = 0
                while(self.Fixed_board[row][col] != 0 & count > size):
                    count += 1
                    col = (col+1) % size
                if count <= size:
                    self.board[row][col] = self.choicenumber(row, col)
        self.update_fitness()
        return self

    def choicenumber(self, r, c):
        number = randint(1, 9)
        count = 0
        while((self.is_row_duplicate(r, number) | self.is_column_duplicate(c, number) | self.is_Grid_duplicate(r, c, number)) and count < 9):
            number = (number) % 9+1
            count += 1
        return number

    def mate(self, mate):
        children1 = []
        children2 = []
        size = len(self.board)
        # typemate = randint(1, 2)
        # if typemate == 1:
        for i in range(size):
            col = randint(0, 8)
            children1.append(self.board[i][:col]+mate.board[i][col:])
            children2.append(mate.board[i][:col] + self.board[i][col:])
        # else:
        #     rows = randint(1, 8)
        #     children1 = [row for row in self.board[:rows]] + \
        #         [row for row in mate.board[rows:]]
        #     children2 = [row for row in mate.board[:rows]] + \
        #         [row for row in self.board[rows:]]
        return (Candidate(children1, self.Fixed_board), Candidate(children2, self.Fixed_board))

    def calculate_num_occurrences_row(self):
        size = len(self.board)
        score = 0
        for row in self.board:
            numbers = [0]*size
            for col in row:
                numbers[col-1] = 1
            score += sum(numbers)
        
        return score

    def calculate_num_occurrences_col(self):
        size = len(self.board)
        score = 0
        for i in range(size):
            numbers = [0]*size
            for j in range(size):
                numbers[self.board[j][i]-1] = 1
            score += sum(numbers)
       
        return score

    def calculate_num_occurrences_grid(self):
        size = len(self.board)
        size_grid = int(size**0.5)
        score = 0
        for i in range(size_grid):
            for j in range(size_grid):
                numbers = [0]*size
                for r in range(size_grid):
                    for c in range(size_grid):
                        numbers[self.board[i*size_grid+r][j*size_grid+c]-1] = 1
                score += sum(numbers)
        
        return score

    def update_fitness(self):
        self.fitness = self.calculate_num_occurrences_col(
        )+self.calculate_num_occurrences_row()+self.calculate_num_occurrences_grid()
        return self.fitness

    def random_gen(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    self.board[i][j] = choice(range(1, int(len(self.board))))

    def is_Grid_duplicate(self, r, c, number):
        size = len(self.board)
        grid = int(size**0.5)
        rGrid = r//grid
        cGrid = c//grid
        for row in range(grid):
            for col in range(grid):
                if self.board[rGrid*grid+row][cGrid*grid+col] == number:
                    return False
        return True

    def is_column_duplicate(self, c, number):
        for i in range(len(self.board)):
            if self.board[i][c] == number:
                return True
        return False

    def is_row_duplicate(self, r, number):
        for ele in self.board[r]:
            if number == ele:
                return True
        return False


class Population:
    _tournamentSize = 20

    def __init__(self, generate_board, size=100, crossover=0.6, elitism=0.1, mutation=0.8, tournamentSize=10):
        self.elitism = elitism
        self.crossover = crossover
        self.mutation = mutation
        buf = []
        for i in range(size):
            buf.append(generate_board.createCandidate())
        self.population = list(
            sorted(buf, key=lambda x: x.fitness, reverse=True))

    def tournamentSelection(self):
        best = choice(self.population)
        for i in range(Population._tournamentSize):
            cont = choice(self.population)
            if cont.fitness > best.fitness:
                best = cont
        return best

    def selectParent(self):
        return (self.tournamentSelection(), self.tournamentSelection())

    def evolve(self):
        size = len(self.population)
        index = int(size*self.elitism)
        buf = self.population[:index]
        while index < size:
            if random() <= self.crossover:
                (parent1, parent2) = self.selectParent()
                childrens = parent1.mate(parent2)
              
                for children in childrens:
                    if random() <= self.mutation:
                        buf.append(children.mutate())
                    else:
                        buf.append(children)
                index += 2
            else:
                if random() <= self.mutation:
                    buf.append(self.population[index].mutate())
                else:
                    buf.append(self.population[index])
                index += 1
        self.population = list(
            sorted(buf, key=lambda x: x.fitness, reverse=True))


if __name__ == "__main__":
    maxGeneration = 100000
    generateBoard = Generate_board(3)
    candidate = generateBoard.createCandidate()
    pop = Population(generate_board=generateBoard, size=1000,
                     crossover=0.8, elitism=0.01, mutation=0.8, tournamentSize=10)
    for i in range(maxGeneration):
        pop.evolve()
        if pop.population[0].fitness == 243:
            break
        else:
            print("Generation: "+str(i) + " Max Score: " +
                  str(pop.population[0].fitness))
            # print(generateBoard.displayBoard(pop.population[0].board))
