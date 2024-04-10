rules = """
Each puzzle consists of a square grid with numbers appearing in all squares. The object is to shade squares so:

    1. No number appears in a row or column more than once.
    2. Shaded (black) squares do not touch each other vertically or horizontally.
    3. When completed, all un-shaded (white) squares create a single continuous area.
"""

class Hitori:
    def __init__(self, board):
        self.size = len(board)
        if not self.is_square(board):
            raise ValueError("The board must be a square.")
        self.board = [[(cell,0) for cell in row] for row in board]

    def is_square(self,board):
        return all(len(row) == self.size for row in board)
    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))

    def rule_1_check(self):
        for row in self.board:
            numbers = [cell[0] for cell in row if cell[1] in [0,1]]
            for number in numbers:
                if numbers.count(number) > 1:
                    return False
        for col in range(self.size):
            numbers = [self.board[row][col][0] for row in range(self.size) if self.board[row][col][1] in [0,1]]
            for number in numbers:
                if numbers.count(number) > 1:
                    return False
        return True


    def is_valid(self):
        # Add your logic here to check if the current board is a valid Hitori solution
        pass

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
