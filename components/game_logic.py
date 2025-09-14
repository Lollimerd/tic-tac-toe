from utils.constants import *
from .board import Board
from Ai_player import ai_player


class GameLogic:
    """Represents the game logic and its state"""

    def __init__(self, game_mode="PVP"):
        self.board = Board(BOARD_ROWS, BOARD_COLS)
        self.current_player = 'X'  # X goes first
        self.game_over = False
        self.winner = None

        # Game mode: "PVP" (Player vs Player) or "PVC" (Player vs Computer)
        self.game_mode = game_mode
        self.ai_player = ai_player()

    def set_game_mode(self, mode, ai_difficulty=ai_player.MEDIUM):
        """Set game mode and AI difficulty"""
        self.game_mode = mode
        self.ai_player.set_difficulty(ai_difficulty)

    def reset_game(self):
        """Reset the game to initial state"""
        self.board.reset()
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        """Process a player's move and update game state"""
        if self.game_over or not self.board.mark_square(row, col, self.current_player):
            return False

        # Check for win
        if self.board.check_win(SQUARE_SIZE, WIDTH, HEIGHT):
            self.game_over = True
            self.winner = self.current_player
            return True

        # Check for draw
        if self.board.is_board_full():
            self.game_over = True
            self.winner = "Draw"
            return True

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

        # If in PVC mode and it's AI's turn (O), make AI move
        if self.game_mode == "PVC" and self.current_player == 'O' and not self.game_over:
            self.make_ai_move()

        return True

    def make_ai_move(self):
        """Have the AI make a move"""
        ai_move = self.ai_player.get_move(self.board)
        if ai_move:
            row, col = ai_move
            self.board.mark_square(row, col, self.current_player)

            # Check for win after AI move
            if self.board.check_win(SQUARE_SIZE, WIDTH, HEIGHT):
                self.game_over = True
                self.winner = self.current_player
                return

            # Check for draw after AI move
            if self.board.is_board_full():
                self.game_over = True
                self.winner = "Draw"
                return

            # Switch back to player
            self.current_player = 'X'

    def get_board(self):
        """Get the game board"""
        return self.board

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over

    def get_winner(self):
        """Get the winner (X, O, or Draw)"""
        return self.winner

    def get_current_player(self):
        """Get the current player"""
        return self.current_player