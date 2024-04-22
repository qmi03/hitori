import json
import random
import time
import csv
import psutil
import os
from heuristic import HitoriPuzzleSolover

def generate_random_hitori(size=8):
    # Create an empty grid
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Fill the grid with random numbers (1 or 0)
    for row in range(size):
        for col in range(size):
            grid[row][col] = random.randint(1, size)

    return grid


# Set recursion limit
import sys
sys.setrecursionlimit(3000)

# Iterate over each game configuration and generate random games
for game_config in range(1000):
    difficulty = "RANDOM"  # Set difficulty to "RANDOM"
    
    # Generate a random 8x8 Hitori game
    board = generate_random_hitori(size=8)
    
    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss
    
    # Initialize a Hitori board
    game = HitoriPuzzleSolover(board, difficulty)
    game.solve()
    
    end_time = time.time()
    end_memory = psutil.Process(os.getpid()).memory_info().rss

    time_taken = end_time - start_time
    memory_used = end_memory - start_memory
    
    # Write metrics to CSV file
    with open(f'hitori_heuristics_metrics_{game.input_level}x{game.input_level}_v2.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([game.input_level, game.difficulty, game.call, time_taken, memory_used,game.is_solved])
