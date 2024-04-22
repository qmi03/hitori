import json
from heuristic import HitoriPuzzleSolover
# Load the JSON file
with open('boards_12x12.json', 'r') as f:
    games = json.load(f)
import sys
sys.setrecursionlimit(3000)
# Iterate over each game configuration
for game_config in games:
    board = game_config['board']
    difficulty = game_config['difficulty']

    # Initialize a Hitori board
    game = HitoriPuzzleSolover(board, difficulty)
    game.solve()
