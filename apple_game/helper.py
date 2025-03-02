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
            if self.check_valid_rectangle():
                self.generate_event()
                        

    def check_valid_rectangle(self):
        for j in range(1, self.COLS):
            index = self.x_start + self.COLS*self.y_start
            for i in range(self.GRID_NUM):
                y,x = divmod((index+i)%self.GRID_NUM, self.COLS)                
                if self.check_right(x, y, j):
                    return True
                
                if self.check_up(x, y, j):
                    return True
                
                if self.check_left(x, y, j):
                    return True
                
                if self.check_down(x, y, j):
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

    
    def check_right(self, x, y, length):
        if y + length >= self.ROWS: return False
        value_sum = 0
        for i in range(self.COLS):
            if x+i >= self.COLS: return False
            for j in range(length):
                value_sum = value_sum + self.puzzle_game.grid[y+j][x+i]
            if value_sum == 10:
                self.update_range(x,y,i,length-1)
                return True
            elif value_sum < 10: continue
            else: return False
    
    
    def check_up(self, x, y, length):
        if x + length >= self.COLS: return False
        value_sum = 0
        for i in range(self.ROWS):
            if y-i < 0: return False
            for j in range(length):
                value_sum = value_sum + self.puzzle_game.grid[y-i][x+j]
            if value_sum == 10:
                self.update_range(x,y,length-1,-i)
                return True
            elif value_sum < 10: continue
            else: return False

    
    def check_left(self, x, y, length):
        if y - length < 0: return False
        value_sum = 0
        for i in range(self.COLS):
            if x-i < 0: return False
            for j in range(length):
                value_sum = value_sum + self.puzzle_game.grid[y-j][x-i]
            if value_sum == 10:
                self.update_range(x,y,-i, -(length-1))
                return True
            elif value_sum < 10: continue
            else: return False
    
    
    def check_down(self, x, y, length):
        if x - length < 0: return False
        value_sum = 0
        for i in range(self.ROWS):
            if y+i >= self.ROWS: return False
            for j in range(length):
                value_sum = value_sum + self.puzzle_game.grid[y+i][x-j]
            if value_sum == 10:
                self.update_range(x,y,-(length-1), i)
                return True
            elif value_sum < 10: continue
            else: return False


    def update_range(self, x, y, dx, dy):
        self.x_start = x
        self.x_end = x+dx
        self.y_start = y
        self.y_end = y+dy 
