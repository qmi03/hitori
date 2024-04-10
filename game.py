rules = """
-1 is BLACK or RED
0 is GREY or BLUE
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
    GREY = 0
    WHITE = 1

class Cell:
    def __init__(self, number, color):
        self.number = number
        self.color = color
    def color_to(self,color):
        self.color = color

class Hitori:
    def __init__(self, board):
        self.size = len(board)
        if not self.is_square(board):
            raise ValueError("The board must be a square.")
        self.board = [[Cell(num,Color.GREY) for num in row] for row in board]

    def is_square(self,board):
        return all(len(row) == self.size for row in board)
    
    def iterate_board(self, callback):
        for row in range(self.size):
            for col in range(self.size):
                if not callback(row, col):
                    return False
        return True

    def print_board(self):
        for row in self.board:
            printed_row = []
            for cell in row:
                if cell.color == Color.BLACK:
                    printed_row.append(Fore.RED + str(cell.number) + Style.RESET_ALL)
                elif cell.color == Color.GREY:
                    printed_row.append(Fore.BLUE + str(cell.number) + Style.RESET_ALL)
                elif cell.color == Color.WHITE:
                    printed_row.append(Fore.GREEN + str(cell.number) + Style.RESET_ALL)
            print(' '.join(printed_row))

    def rule_1_check(self):
        def check_numbers(numbers, label, index):
            for number in numbers:
                count = numbers.count(number)
                if count > 1:
                    print(f"Number {number} in {label} {index+1} has appeared {count} times")
                    return False
            return True

        for row in range(self.size):
            numbers = [self.board[row][col].number for col in range(self.size) if self.board[row][col].color in [Color.GREY,Color.WHITE]]
            if not check_numbers(numbers, 'row', row):
                return False

        for col in range(self.size):
            numbers = [self.board[row][col].number for row in range(self.size) if self.board[row][col].color in [Color.GREY,Color.WHITE]]
            if not check_numbers(numbers, 'col', col):
                return False

        return True

    def rule_2_check(self):
        def check_shaded_touch(row, col):
            if self.board[row][col].color == Color.BLACK:
                if row != (self.size-1) and self.board[row+1][col].color == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+2}, col {col+1}")
                    return False
                if row != 0 and self.board[row-1][col].color == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row}, col {col+1}")
                    return False
                if col != (self.size-1) and self.board[row][col+1].color == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col+2}")
                    return False
                if col != 0 and self.board[row][col-1].color == Color.BLACK:
                    print(f"Shaded squares touch at row {row+1}, col {col+1} and row {row+1}, col {col}")
                    return False
            return True

        return self.iterate_board(check_shaded_touch)


    def is_fully_shaded(self):
        def check_grey(row, col):
            if self.board[row][col].color == Color.GREY:
                print(f"Cell at ({row+1},{col+1} is still GREY!)")
                return False
            return True

        return self.iterate_board(check_grey)

    def rule_3_check(self):
        # Initialize visited matrix
        visited = [[False]*self.size for _ in range(self.size)]

        # Find the first white square
        start = None
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].color == Color.WHITE:
                    start = (i, j)
                    break
            if start is not None:
                break
        if start is None:
            print("No white cell at all")
            return False

        # Define DFS function
        def dfs(i, j):
            if i < 0 or i >= self.size or j < 0 or j >= self.size or visited[i][j] or self.board[i][j].color != Color.WHITE:
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
                if self.board[i][j].color == Color.WHITE and not visited[i][j]:
                    print(f"White cell at ({i+1},{j+1}) is not connected to the main white area.")
                    return False

        return True


    def is_solved(self):
        if not self.rule_1_check():
            print("Rule 1 check failed.")
            return False
        if not self.rule_2_check():
            print("Rule 2 check failed.")
            return False
        if not self.is_fully_shaded():
            print("Not all cells are shaded.")
            return False
        if not self.rule_3_check():
            print("Rule 3 check failed.")
            return False
        print("All checks passed. The board is solved.")
        return True

    def solve(self):
        # Add your logic here to solve the Hitori puzzle
        pass

# Initialize a Hitori board
board = [
    [1, 2, 1],
    [2, 3, 2],
    [3, 1, 3]
]
print(len(board))
game = Hitori(board)
game.print_board()
print(game.rule_1_check())
print(game.rule_2_check())
game.is_solved()