class Board:
    """Represents the game board and its state"""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.winning_line = None

    def reset(self):
        """Reset the board to initial state"""
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.winning_line = None

    def mark_square(self, row, col, player):
        """Mark a square with the given player's symbol"""
        if self.is_square_available(row, col):
            self.board[row][col] = player
            return True
        return False

    def is_square_available(self, row, col):
        """Check if a square is available"""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.board[row][col] is None

    def is_board_full(self):
        """Check if the board is full"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    return False
        return True

    def check_win(self, square_size, width, height):
        """Check if there is a winner and set winning line coordinates if so"""
        # Check rows
        for row in range(self.rows):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winning_line = (
                    (0, row * square_size + square_size // 2),
                    (width, row * square_size + square_size // 2)
                )
                return True

        # Check columns
        for col in range(self.cols):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winning_line = (
                    (col * square_size + square_size // 2, 0),
                    (col * square_size + square_size // 2, height)
                )
                return True

        # Check diagonal (top-left to bottom-right)
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winning_line = ((0, 0), (width, height))
            return True

        # Check diagonal (top-right to bottom-left)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winning_line = ((width, 0), (0, height))
            return True

        return False

    def get_winning_line(self):
        """Return the winning line coordinates"""
        return self.winning_line