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

class Color(Enum):
    BLACK = -1
    WHITE = 1
class Hitori:
    def __init__(self, board):
        self.size = len(board)
        if not self.is_square(board):
            raise ValueError("The board must be a square.")
        self.board = board
        self.state = [[Color.WHITE for _ in row] for row in board]

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

    def rule_1_check(self,state):
        def check_numbers(numbers, label, index):
            for number in numbers:
                count = numbers.count(number)
                if count > 1:
                    print(f"Number {number} in {label} {index+1} has appeared {count} times")
                    return False
            return True

        for row in range(self.size):
            numbers = [self.board[row][col] for col in range(self.size) if state[row][col] in [Color.WHITE]]
            if not check_numbers(numbers, 'row', row):
                return False

        for col in range(self.size):
            numbers = [self.board[row][col] for row in range(self.size) if state[row][col] in [Color.WHITE]]
            if not check_numbers(numbers, 'col', col):
                return False

        return True

    def rule_2_check(self,state):
        def check_shaded_touch(row, col):
            if state[row][col] == Color.BLACK:
                if row != (self.size-1) and state[row+1][col] == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+2}, col {col+1}")
                    return False
                if row != 0 and state[row-1][col] == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row}, col {col+1}")
                    return False
                if col != (self.size-1) and state[row][col+1] == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col+2}")
                    return False
                if col != 0 and state[row][col-1] == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col}")
                    return False
            return True

        return self.iterate_board(check_shaded_touch)

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
            print("No white cell at all")
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
                    print(f"White cell at ({i+1},{j+1}) is not connected to the main white area.")
                    return False

        return True


    def is_solved(self):
        if not self.rule_1_check(self.state):
            print("Rule 1 check failed.")
            return False
        if not self.rule_2_check(self.state):
            print("Rule 2 check failed.")
            return False
        if not self.rule_3_check(self.state):
            print("Rule 3 check failed.")
            return False
        print("All checks passed. The board is solved.")
        return True

    def dfs_solve(self, row=0, col=0):
        # If we have reached the end of the board, check if the current state is a solution
        if row == self.size:
            print("Reached the end of the board. Checking if the current state is a solution...")
            return self.is_solved()

        # Calculate the next cell
        next_row, next_col = (row + (col + 1) // self.size, (col + 1) % self.size)

        # Try to leave the cell white
        self.state[row][col] = Color.WHITE
        print(f"Trying to leave the cell at row {row+1}, col {col+1} white...")
        if self.rule_2_check(self.state):
            print(f"Cell at row {row+1}, col {col+1} can be white. Moving on to the next cell...")
            if self.dfs_solve(next_row, next_col):
                return True

        # Try to color the cell black
        self.state[row][col] = Color.BLACK
        print(f"Trying to color the cell at row {row+1}, col {col+1} black...")
        if self.rule_2_check(self.state):
            print(f"Cell at row {row+1}, col {col+1} can be black. Moving on to the next cell...")
            if self.dfs_solve(next_row, next_col):
                return True

        # If neither white nor black leads to a solution, backtrack
        print(f"Neither white nor black leads to a solution for cell at row {row+1}, col {col+1}. Backtracking...")
        self.state[row][col] = Color.WHITE
        return False

    def solve(self):
        if self.dfs_solve():
            print("Puzzle solved successfully!")
            self.print_board()
        else:
            print("No solution found.")
# Initialize a Hitori board
board = [
    [1, 2, 1],
    [2, 3, 2],
    [3, 1, 3]
]
print(len(board))
game = Hitori(board)
game.print_board()

game.solve()
