from puzzle_game import PuzzleGame
import pygame
import time


class Helper:
    def __init__(self, puzzle_game: PuzzleGame):
        self.puzzle_game = puzzle_game

        self.COLS = self.puzzle_game.COLS
        self.ROWS = self.puzzle_game.ROWS
        self.GRID_NUM = self.COLS*self.ROWS
        self.x_start = 0
        self.y_start = 0
        self.x_end = 0
        self.y_end = 0

    def convert_2d_to_1d(self, x, y):
        return x + self.COLS*y
        
    def run(self):
        while self.puzzle_game.running:
            if self.update_range():
                self.generate_event()
                        

    def update_range(self):
        index = self.x_start + self.COLS*self.y_start
        
        for i in range(self.GRID_NUM):
            y,x = divmod((index+i)%self.GRID_NUM, self.COLS)
            if self.puzzle_game.grid[y][x] == 0:
                continue
            
            if self.check_right(x, y):
                return True
            
            if self.check_up(x, y):
                return True
            
            if self.check_left(x, y):
                return True
            
            if self.check_down(x, y):
                return True
        return False
            
    def generate_event(self):
        self.puzzle_game.add_event(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                "pos": [
                    self.puzzle_game.grid_x + self.x_start * self.puzzle_game.cell_size, 
                    self.puzzle_game.grid_y + self.y_start * self.puzzle_game.cell_size,
                ], 
                "button": 1,
            })
        )
        self.puzzle_game.add_event(
            pygame.event.Event(pygame.MOUSEMOTION, {
                "pos": [
                    self.puzzle_game.grid_x + self.x_end * self.puzzle_game.cell_size, 
                    self.puzzle_game.grid_y + self.y_end * self.puzzle_game.cell_size,
                ],
            })
        )
        time.sleep(0.1)
        self.puzzle_game.add_event(
            pygame.event.Event(pygame.MOUSEBUTTONUP, {
                "pos": [
                    self.puzzle_game.grid_x + self.x_end * self.puzzle_game.cell_size, 
                    self.puzzle_game.grid_y + self.y_end * self.puzzle_game.cell_size,
                ],
                "button": 1,
            })
        )
        time.sleep(0.1)

    
    def check_right(self, x, y):
        value_sum = self.puzzle_game.grid[y][x]
        for i in range(1,self.COLS):
            if x+i >= self.COLS: return False
            value_sum = value_sum + self.puzzle_game.grid[y][x+i]
            if value_sum == 10:
                self.update_range_right(x,y,i)
                return True
            elif value_sum < 10: continue
            else: return False
    
    
    def check_up(self, x, y):
        value_sum = self.puzzle_game.grid[y][x]
        for i in range(1,self.ROWS):
            if y-i < 0: return False
            value_sum = value_sum + self.puzzle_game.grid[y-i][x]
            if value_sum == 10:
                self.update_range_up(x,y,i)
                return True
            elif value_sum < 10: continue
            else: return False

    
    def check_left(self, x, y):
        value_sum = self.puzzle_game.grid[y][x]
        for i in range(1,self.COLS):
            if x-i < 0: return False
            value_sum = value_sum + self.puzzle_game.grid[y][x-i]
            if value_sum == 10:
                self.update_range_left(x,y,i)
                return True
            elif value_sum < 10: continue
            else: return False
    
    
    def check_down(self, x, y):
        value_sum = self.puzzle_game.grid[y][x]
        for i in range(1,self.COLS):
            if y+i >= self.ROWS: return False
            value_sum = value_sum + self.puzzle_game.grid[y+i][x]
            if value_sum == 10:
                self.update_range_down(x,y,i)
                return True
            elif value_sum < 10: continue
            else: return False


    def update_range_right(self, x, y, i):
        self.x_start = x
        self.x_end = x+i
        self.y_start = y
        self.y_end = y


    def update_range_up(self, x, y, i):
        self.x_start = x
        self.x_end = x
        self.y_start = y
        self.y_end = y-i


    def update_range_left(self, x, y, i):
        self.x_start = x
        self.x_end = x-i
        self.y_start = y
        self.y_end = y


    def update_range_down(self, x, y, i):
        self.x_start = x
        self.x_end = x
        self.y_start = y
        self.y_end = y+i