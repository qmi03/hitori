import json
from game import Hitori
# Load the JSON file
with open('boards_5x5.json', 'r') as f:
    games = json.load(f)

# Iterate over each game configuration
for game_config in games:
    board = game_config['board']
    difficulty = game_config['difficulty']

    # Initialize a Hitori board
    game = Hitori(board, difficulty)
    game.solve()