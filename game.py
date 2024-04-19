rules = """
-1 is BLACK or RED
1 is WHITE or GREEN
Each puzzle consists of a square grid with numbers appearing in all squares. The object is to shade squares so:

    1. No number appears in a row or column more than once.
    2. Shaded (black) squares do not touch each other vertically or horizontally.
    3. When completed, all un-shaded (white) squares create a single continuous area.
"""
from colorama import Fore, Style
from enum import Enum
import time
import os
import psutil
import csv

class Color(Enum):
    BLACK = -1
    WHITE = 1
class Hitori:
    def __init__(self, board, difficulty):
        self.size = len(board)
        if not self.is_square(board):
            raise ValueError("The board must be a square.")
        self.board = board
        self.state = [[Color.WHITE for _ in row] for row in board]
        self.call = 0
        self.difficulty = difficulty
        self.log_file = open("hitori_log.txt", "w")

    def __del__(self):
        self.log_file.close()

    def log(self, message):
        self.log_file.write(message+'\n')

    def is_square(self,board):
        return all(len(row) == self.size for row in board)
    
    def iterate_board(self, callback):
        for row in range(self.size):
            for col in range(self.size):
                if not callback(row, col):
                    return False
        return True

    def print_board(self,state=None):
        if not state: state = self.state
        for row in range(self.size):
            printed_row = []
            for col in range(self.size):
                cell = self.board[row][col]
                if state[row][col] == Color.BLACK:
                    printed_row.append(Fore.RED + str(cell) + Style.RESET_ALL)
                elif state[row][col] == Color.WHITE:
                    printed_row.append(Fore.GREEN + str(cell) + Style.RESET_ALL)
            print(' '.join(printed_row))
    def check_numbers(self,numbers, label, index):
        for number in numbers:
            count = numbers.count(number)
            if count > 1:
                self.log(f"Number {number} in {label} {index+1} has appeared {count} times")
                return False
        return True
    def rule_1_check_row(self,row_num,state):
        numbers = [self.board[row_num][col] for col in range(self.size) if state[row_num][col] in [Color.WHITE]]
        if not self.check_numbers(numbers,'row',row_num):
            return False

    def rule_1_check(self,state):
        for row in range(self.size):
            numbers = [self.board[row][col] for col in range(self.size) if state[row][col] in [Color.WHITE]]
            if not self.check_numbers(numbers, 'row', row):
                return False

        for col in range(self.size):
            numbers = [self.board[row][col] for row in range(self.size) if state[row][col] in [Color.WHITE]]
            if not self.check_numbers(numbers, 'col', col):
                return False

        return True

    def rule_2_check(self,state):
        def check_shaded_touch(row, col):
            if state[row][col] == Color.BLACK:
                if row != (self.size-1) and state[row+1][col] == Color.BLACK:
                    self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+2}, col {col+1}")
                    return False
                if row != 0 and state[row-1][col] == Color.BLACK:
                    self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row}, col {col+1}")
                    return False
                if col != (self.size-1) and state[row][col+1] == Color.BLACK:
                    self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col+2}")
                    return False
                if col != 0 and state[row][col-1] == Color.BLACK:
                    self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col}")
                    return False
            return True

        return self.iterate_board(check_shaded_touch)
    def rule_2_check_cell(self,row,col):
        if row != (self.size-1) and self.state[row+1][col] == Color.BLACK:
            self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+2}, col {col+1}")
            return False
        if row != 0 and self.state[row-1][col] == Color.BLACK:
            self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row}, col {col+1}")
            return False
        if col != (self.size-1) and self.state[row][col+1] == Color.BLACK:
            self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col+2}")
            return False
        if col != 0 and self.state[row][col-1] == Color.BLACK:
            self.log(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col}")
            return False
        return True

    def rule_3_check(self,state):
        # Initialize visited matrix
        visited = [[False]*self.size for _ in range(self.size)]

        # Find the first white square
        start = None
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == Color.WHITE:
                    start = (i, j)
                    break
            if start is not None:
                break
        if start is None:
            self.log("No white cell at all")
            return False

        # Define DFS function
        def dfs(i, j):
            if i < 0 or i >= self.size or j < 0 or j >= self.size or visited[i][j] or state[i][j] != Color.WHITE:
                return
            visited[i][j] = True
            dfs(i-1, j)
            dfs(i+1, j)
            dfs(i, j-1)
            dfs(i, j+1)

        # Start DFS from the first white square
        dfs(*start)

        # Check if all white squares have been visited
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == Color.WHITE and not visited[i][j]:
                    self.log(f"White cell at ({i+1},{j+1}) is not connected to the main white area.")
                    return False

        return True


    def is_solved(self):
        if not self.rule_1_check(self.state):
            self.log("Rule 1 check failed.")
            return False
        if not self.rule_2_check(self.state):
            self.log("Rule 2 check failed.")
            return False
        if not self.rule_3_check(self.state):
            self.log("Rule 3 check failed.")
            return False
        print("All checks passed. The board is solved.")
        return True

    def dfs_solve(self, row=0, col=0,depth=0):

        print(f"dfs call no.{self.call}")
        self.print_board()
        self.call += 1
        if depth > self.max_depth_reached:
            self.max_depth_reached = depth
        if row == self.size:
            return self.is_solved()

        next_row, next_col = (row + (col + 1) // self.size, (col + 1) % self.size)

        # Kiem tra luat 1 sau khi duyet qua 1 row
        if next_col < col and self.rule_1_check_row(row,self.state): return False

        self.state[row][col] = Color.BLACK
        # Kiem tra luat 2 truoc khi quyet dinh to den
        if self.rule_2_check_cell(row,col):
            if self.dfs_solve(next_row, next_col,depth+1):
                return True

        self.state[row][col] = Color.WHITE
        if self.dfs_solve(next_row, next_col,depth+1):
            return True

        return False

    def solve(self):
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss

        if self.dfs_solve():
            print("Puzzle solved successfully!")
            self.print_board()
        else:
            print("No solution found.")

        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss

        time_taken = end_time - start_time
        memory_used = end_memory - start_memory

        print(f"Time taken: {time_taken} seconds")
        print(f"Memory used: {memory_used} MB")

        # Save the results in a CSV file
        with open(f'hitori_metrics_{self.size}x{self.size}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.size,self.difficulty,self.call, time_taken, memory_used])
if __name__ == "__main__":
    board = [
[1,2,1],
[2,3,2],
[3,1,3],
]
    difficulty = "Easy"
    game = Hitori(board, difficulty)
    game.solve()
