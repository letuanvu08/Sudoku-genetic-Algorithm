from random import choice,sample
import numpy as np
import math
from copy import deepcopy
class Generate_board:
    sideGrid=3
    side=sideGrid**2
    goalBoard=[]
    board_Puzzle=[]
    def __init__(self,sideGrid):
        self.sideGrid=sideGrid
        self.side=self.sideGrid**2
        self.goalBoard=[[0 for i in range(self.side)]for j in range(self.side)]
        self.generate_board()
        self.generate_board_Puzzle()
        print("Goal board:")
        self.displayBoard(self.goalBoard)
        print("Puzzle board:")
        self.displayBoard(self.board_Puzzle)
        
    def pattern(self,row,col):
        return (self.sideGrid*(row%self.sideGrid)+row//self.sideGrid+col)%self.side
    def shuffle(self):
        return sample(range(1,self.side+1),self.side)
    def checkValid(self,r,c,number):
        for i in range(self.side):
            if self.goalBoard[r][i]==number | self.goalBoard[i][c]==number:
                return False
        for i in range(self.sideGrid):
            for j in range(self.sideGrid):
                if self.goalBoard[(r+i)%self.sideGrid+r//self.sideGrid][(c+j)%self.sideGrid+c//self.sideGrid]==number:
                    return False
        return True

            
            

    def generate_board(self):
        numbers=sample(range(1,self.side+1),self.side)
        self.goalBoard=[[numbers[self.pattern(row,col)]for col in range(self.side)]for row in range(self.side)]
        rows=[row for grid in sample(range(self.sideGrid),self.sideGrid) for row in sample(range(grid*self.sideGrid,(grid+1)*self.sideGrid),self.sideGrid)]
        cols=[col for grid in sample(range(self.sideGrid),self.sideGrid) for col in sample(range(grid*self.sideGrid,(grid+1)*self.sideGrid),self.sideGrid)]
        self.goalBoard=[[self.goalBoard[r][c]for c in cols] for r in rows]
        return self.goalBoard
        # for i in range(self.side):
        #     numbers=self.shuffle()
        #     col=[]
        #     for j in range(self.side):
        #         for number in numbers:
        #             if self.checkValid(i,j,number)==True:
        #                 self.goalBoard[i][j]=number
        #                 break
            
    def generate_board_Puzzle(self):
        self.board_Puzzle=deepcopy(self.goalBoard)
        
        squares = self.side*self.side
        empties = squares * 3//4
        for p in sample(range(squares),empties):
            self.board_Puzzle[p//self.side][p%self.side] = 0

        numSize = len(str(self.side))

    def displayBoard(self,board):
        expand_line = lambda line : line[0]+line[5:9].join([line[1:5]*(self.sideGrid-1)]*self.sideGrid)+line[9:13]
        line0 = expand_line("╔═══╤═══╦═══╗")
        line1 = expand_line("║ . │ . ║ . ║")
        line2 = expand_line("╟───┼───╫───╢")
        line3 = expand_line("╠═══╪═══╬═══╣")
        line4 = expand_line("╚═══╧═══╩═══╝")
      
        nums = [[""] + [str(n) for n in row] for row in board]
        print(line0)
        for r in range(1, self.side + 1):
            print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
            print([line2, line3, line4][(r % self.side == 0) + (r % self.sideGrid == 0)])

    
if __name__=="__main__":
    generate_board=Generate_board(3)