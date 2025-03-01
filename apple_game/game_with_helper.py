import pygame
from puzzle_game import PuzzleGame
from helper import Helper
import threading


game = PuzzleGame()
def run_game():
    game.run()

game_thread = threading.Thread(target=run_game)
game_thread.start()

pygame.time.delay(1000) 

helper = Helper(game)
helper.run()
