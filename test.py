import json
from heuristic import HitoriPuzzleSolover  # Assuming the class name is HitoriPuzzleSolver

def load_games_from_json(file_path):
    with open(file_path, 'r') as f:
        games_data = json.load(f)
    return games_data

if __name__ == "__main__":
    # Load games from JSON file
    games = load_games_from_json('boards_12x12.json')  # Update the file path as needed

    # Iterate over each game configuration
    for game_config in games:
        board = game_config['board']
        difficulty = game_config['difficulty']

        # Initialize a Hitori board and solve
        print(board)
        print(difficulty)