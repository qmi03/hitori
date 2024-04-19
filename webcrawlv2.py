import requests
from bs4 import BeautifulSoup
import json
import time

def crawl_loop(board_size,num_puzzles):
    for game_id in range(num_puzzles):
        page_to_scrape = requests.get(f'https://menneske.no/hitori/{board_size}x{board_size}/eng/utskrift.html?number={game_id+1}')
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        numbers = soup.findAll("td")
        board = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(int(numbers[i * board_size + j].text))
            board.append(row)

        difficulty = soup.find('div', {'class': 'hitori'}).text.split('Difficulty: ')[1].split('<br>')[0]

        data = {
            'board': board,
            'difficulty': difficulty,
        }    
        print(board,difficulty)

        with open(f'boards_{board_size}x{board_size}.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

        time.sleep(60)  # Delay for 60 seconds

crawl_loop(6,200)
crawl_loop(8,200)
crawl_loop(9,200)
crawl_loop(12,200)
crawl_loop(15,200)
crawl_loop(20,5)
