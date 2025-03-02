import pygame
import random

class PuzzleGame:
    def __init__(self):
        # Game settings
        self.WIDTH, self.HEIGHT = 800, 500  # Window size
        self.ROWS, self.COLS = 10, 17  # Grid size
        self.MARGIN = 50  # Margin around the grid
        self.TIME_LIMIT = 120  # Time limit in seconds (2 minutes)
        self.cell_size = min((self.WIDTH - 2 * self.MARGIN) // self.COLS, (self.HEIGHT - 2 * self.MARGIN) // self.ROWS)
        self.grid_x = (self.WIDTH - (self.cell_size * self.COLS)) // 2
        self.grid_y = (self.HEIGHT - (self.cell_size * self.ROWS)) // 2

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.HIGHLIGHT = (255, 200, 200)
        self.BACKGROUND = (220, 220, 220)

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Number Sum Puzzle")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        # Generate grid
        self.grid = self.generate_grid()
        self.start_pos = None
        self.selected_cells = []
        self.score = 0
        self.start_time = pygame.time.get_ticks()

        self.events = []

    def generate_grid(self):
        """Generate a grid filled with random numbers from 1 to 9."""
        return [[random.randint(1, 9) for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def draw_grid(self):
        """Draw the grid and highlight selected cells."""
        self.screen.fill(self.BACKGROUND)

        for row in range(self.ROWS):
            for col in range(self.COLS):
                rect = pygame.Rect(self.grid_x + col * self.cell_size, self.grid_y + row * self.cell_size, self.cell_size, self.cell_size)
                if (row, col) in self.selected_cells and self.grid[row][col] != 0:
                    pygame.draw.rect(self.screen, self.HIGHLIGHT, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 2)
                if self.grid[row][col] != 0:
                    text = self.font.render(str(self.grid[row][col]), True, self.BLACK)
                    self.screen.blit(text, (self.grid_x + col * self.cell_size + 10, self.grid_y + row * self.cell_size + 10))

    def draw_game_over(self):
        """Displays the game over message in the center of the screen."""
        overlay_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, self.HEIGHT // 2)
        pygame.draw.ellipse(self.screen, self.GRAY, overlay_rect)
        game_over_text = self.font.render("Game Over", True, self.BLACK)
        score_text = self.font.render(f"Final Score: {self.score}", True, self.BLACK)
        self.screen.blit(game_over_text, (self.WIDTH // 2 - 50, self.HEIGHT // 2 - 40))
        self.screen.blit(score_text, (self.WIDTH // 2 - 70, self.HEIGHT // 2))
        pygame.display.flip()

        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
            self.clock.tick(30)

    
    def get_selected_cells(self, start, end, grid_x, grid_y, cell_size):
        """Determine the selected cells within the drawn rectangle."""
        x1, y1 = min(start[0], end[0]), min(start[1], end[1])
        x2, y2 = max(start[0], end[0]), max(start[1], end[1])
        return [(r, c) for r in range(y1, y2+1) for c in range(x1, x2+1)]

    def run(self):
        """Main game loop."""
        self.running = True
        while self.running:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_time = max(self.TIME_LIMIT - elapsed_time, 0)
            if remaining_time == 0:
                self.running = False

            self.screen.fill(self.BACKGROUND)
            cell_size = min((self.WIDTH - 2 * self.MARGIN) // self.COLS, (self.HEIGHT - 2 * self.MARGIN) // self.ROWS)
            grid_x = (self.WIDTH - (cell_size * self.COLS)) // 2
            grid_y = (self.HEIGHT - (cell_size * self.ROWS)) // 2
            self.draw_grid()

            # Display score and remaining time
            score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
            time_text = self.font.render(f"Time: {remaining_time}s", True, self.BLACK)
            self.screen.blit(score_text, (self.MARGIN, self.HEIGHT - 40))
            self.screen.blit(time_text, (self.WIDTH - 150, self.HEIGHT - 40))

            pygame.display.flip()
            
            for event in pygame.event.get() + self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_pos = ((event.pos[0] - grid_x) // cell_size, (event.pos[1] - grid_y) // cell_size)
                elif event.type == pygame.MOUSEMOTION and self.start_pos:
                    end_pos = ((event.pos[0] - grid_x) // cell_size, (event.pos[1] - grid_y) // cell_size)
                    self.selected_cells = [(r, c) for r, c in self.get_selected_cells(self.start_pos, end_pos, grid_x, grid_y, cell_size) if 0 <= r < self.ROWS and 0 <= c < self.COLS and self.grid[r][c] != 0]
                elif event.type == pygame.MOUSEBUTTONUP and self.start_pos:
                    end_pos = ((event.pos[0] - grid_x) // cell_size, (event.pos[1] - grid_y) // cell_size)
                    self.selected_cells = [(r, c) for r, c in self.get_selected_cells(self.start_pos, end_pos, grid_x, grid_y, cell_size) if 0 <= r < self.ROWS and 0 <= c < self.COLS and self.grid[r][c] != 0]
                    
                    # Calculate the sum of selected numbers
                    total = sum(self.grid[r][c] for r, c in self.selected_cells if self.grid[r][c] != 0)
                    if total == 10:
                        self.score += len(self.selected_cells)
                        for r, c in self.selected_cells:
                            self.grid[r][c] = 0  # Remove numbers
                    
                    self.selected_cells = []
                    self.start_pos = None
                
                self.events.clear()
            
            self.clock.tick(30)

        self.draw_game_over()
        print(f"Game Over! Your final score: {self.score}")

    def add_event(self, event):
        self.events.append(event)