import numpy as np


class AppleGame:
    def __init__(self):
        self.COLS = 17
        self.ROWS = 10
        self.action_size = int(self.COLS*(self.COLS+1)/2*self.ROWS*(self.ROWS+1)/2)

        self.action_to_range = []
        for start_row in range(self.ROWS):
            for start_col in range(self.COLS): 
                for end_row in range(start_row, self.ROWS): 
                    for end_col in range(start_col, self.COLS):
                        self.action_to_range.append([start_row, start_col, end_row, end_col])

    def get_init_board(self):
        b = np.random.randint(1, 10, size=(self.ROWS, self.COLS))
        return b

    def get_board_size(self):
        return self.ROWS * self.COLS

    def get_action_size(self):
        return self.action_size

    def get_next_state(self, board: np.ndarray, action: int):
        b = np.copy(board)
        start_row, start_col, end_row, end_col = self.action_to_range[action]
        sum = b[start_row:end_row+1, start_col:end_col+1].sum()
        if sum == 10:
            b[start_row:end_row+1, start_col:end_col+1] = 0
        return b

    def has_legal_moves(self, board: np.ndarray):
        for start_row in range(self.ROWS):
            for start_col in range(self.COLS):
                for end_row in range(start_row, self.ROWS):
                    for end_col in range(start_col, self.COLS):
                        rect_sum = np.sum(board[start_row:end_row+1, start_col:end_col+1])
                        if rect_sum == 10:
                            return True
                        if rect_sum > 10:
                            break
        return False

    # def get_valid_moves(self, board: np.ndarray):
    #     valid_moves = np.zeros(self.action_size)
    #     index = 0
    #     for start_row in range(self.ROWS):
    #         for start_col in range(self.COLS):
    #             for end_row in range(start_row, self.ROWS):
    #                 for end_col in range(start_col, self.COLS):
    #                     rect_sum = np.sum(board[start_row:end_row+1, start_col:end_col+1])
    #                     valid_moves[index] = rect_sum==10
    #                     index = index+1
    #     return valid_moves
    def get_valid_moves(self, board: np.ndarray):
        ROWS, COLS = self.ROWS, self.COLS
        valid_moves = np.zeros(self.action_size, dtype=np.uint8)
        
        # prefix_sum (O(ROWS * COLS))
        prefix_sum = np.zeros((ROWS + 1, COLS + 1), dtype=np.int32)
        
        for r in range(ROWS):
            for c in range(COLS):
                prefix_sum[r+1][c+1] = (board[r][c] + 
                                        prefix_sum[r][c+1] + 
                                        prefix_sum[r+1][c] - 
                                        prefix_sum[r][c])

        index = 0
        for start_row in range(ROWS):
            for start_col in range(COLS):
                for end_row in range(start_row, ROWS):
                    rect_sum = (prefix_sum[end_row+1][start_col+1] 
                                - prefix_sum[start_row][start_col+1] 
                                - prefix_sum[end_row+1][start_col] 
                                + prefix_sum[start_row][start_col])
                    if rect_sum > 10:
                        index += (ROWS - end_row) * (COLS - start_col)
                        break  
                    for end_col in range(start_col, COLS):
                        rect_sum = (prefix_sum[end_row+1][end_col+1] 
                                    - prefix_sum[start_row][end_col+1] 
                                    - prefix_sum[end_row+1][start_col] 
                                    + prefix_sum[start_row][start_col])
                        
                        if rect_sum > 10:
                            index += COLS - end_col
                            break

                        valid_moves[index] = (rect_sum == 10)
                        index += 1

        return valid_moves

    def get_score(self, board: np.ndarray):
        return np.count_nonzero(board == 0)