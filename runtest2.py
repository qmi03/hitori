import json
import os
import time
from dfs import Hitori

# Path to the JSON file
file_path = 'boards_6x6.json'

# Wait until the file exists
while not os.path.isfile(file_path):
    print(f"Waiting for file {file_path} to exist...")
    time.sleep(60)  # Wait for 1 second

print(f"File {file_path} found. Proceeding with the game configurations...")

# Load the JSON file
with open(file_path, 'r') as f:
    games = json.load(f)

# Iterate over each game configuration
for game_config in games:
    board = game_config['board']
    difficulty = game_config['difficulty']

    # Initialize a Hitori board
    game = Hitori(board, difficulty)
    game.solve()
