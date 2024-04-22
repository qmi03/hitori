import json
from heuristic import HitoriPuzzleSolover
import time
import csv
import psutil
import os
# Load the JSON file
with open('boards_12x12.json', 'r') as f:
    games = json.load(f)
import sys
sys.setrecursionlimit(3000)
# Iterate over each game configuration
for game_config in games:
    try:
        board = game_config['board']
        difficulty = game_config['difficulty']
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss
        # Initialize a Hitori board
        game = HitoriPuzzleSolover(board, difficulty)
        game.solve()
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss

        time_taken = end_time - start_time
        memory_used = end_memory - start_memory
        with open(f'hitori_heuristics_metrics_{game.input_level}x{game.input_level}_v2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([game.input_level,game.difficulty,game.call, time_taken, memory_used])
    except:
        with open(f'hitori_heuristics_metrics_{game.input_level}x{game.input_level}_v2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([len(game_config['board']),game_config['difficulty'],-1, -1, -1])