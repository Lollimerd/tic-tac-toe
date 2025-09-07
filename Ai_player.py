import random
import math
from utils.constants import *

class ai_player:
    """AI player for Tic Tac Toe with configurable difficulty"""
    EASY = 0
    MEDIUM = 1
    HARD = 2
    def __init__(self, difficulty=MEDIUM):
        """
        Initialize the AI player with a difficulty level
        - EASY: Makes random legal moves
        - MEDIUM: Uses minimax but with limited depth
        - HARD: Uses full minimax with alpha-beta pruning
        """
        self.difficulty = difficulty
        self.player_symbol = 'O'  # AI is typically O, human is X

    def set_difficulty(self, difficulty):
        """Change the AI difficulty level"""
        self.difficulty = difficulty

    def set_player_symbol(self, symbol):
        """Set AI's symbol (X or O)"""
        self.player_symbol = symbol

    def get_move(self, board):
        """
        Determine the next move based on current board state and difficulty
        Returns (row, col) for the chosen move
        """
        if self.difficulty == ai_player.EASY:
            return self._get_random_move(board)
        elif self.difficulty == ai_player.MEDIUM: # Medium uses minimax but with limited depth of 2
            return self._get_minimax_move(board, depth_limit=2)
        else:  # HARD
            # Hard uses full minimax with alpha-beta pruning
            return self._get_minimax_move(board, depth_limit=9)  # 9 is more than needed for 3x3

    def _get_random_move(self, board):
        """Returns a random valid move"""
        available_moves = []
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_square_available(row, col):
                    available_moves.append((row, col))
        if not available_moves:
            return None
        return random.choice(available_moves)

    def _get_minimax_move(self, board, depth_limit):
        """minimax algorithm simulation"""
        # Create a board copy to simulate moves
        board_copy = self._copy_board(board)
        opponent_symbol = 'X' if self.player_symbol == 'O' else 'O'
        best_score = -math.inf
        best_move = None

        # Try each available move
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_square_available(row, col):

                    # Make the move
                    board_copy.board[row][col] = self.player_symbol

                    # Calculate score from this move using minimax
                    score = self._minimax(board_copy, 0, depth_limit, False, opponent_symbol, -math.inf, math.inf)

                    # Undo the move
                    board_copy.board[row][col] = None

                    # Update best move if needed
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        # If no moves found or all moves have the same (negative) score, return random move
        if best_move is None:
            return self._get_random_move(board)
        return best_move

    def _minimax(self, board, depth, depth_limit, is_maximizing, current_player, alpha, beta):
        """minimax algorithm implementation with alpha-beta pruning"""
        # set turn
        opponent = 'X' if current_player == 'O' else 'O'

        # Check for terminal states
        winner = self._check_winner(board)
        if winner == self.player_symbol:
            return 10 - depth  # Win (prefer quicker wins)

        elif winner == opponent: return -10 + depth  # Loss (prefer slower losses)

        elif self._is_board_full(board) or depth == depth_limit:
            return 0  # Draw or depth limit reached

        if is_maximizing:
            # Maximizing player (AI)
            max_score = -math.inf
            for row in range(board.rows):
                for col in range(board.cols):
                    if board.is_square_available(row, col):
                        # Make move
                        board.board[row][col] = current_player

                        # Recurse
                        score = self._minimax(board, depth + 1, depth_limit, False, opponent, alpha, beta)

                        # Undo move
                        board.board[row][col] = None

                        # Update max score
                        max_score = max(score, max_score)

                        # Alpha-beta pruning
                        alpha = max(alpha, max_score)
                        if beta <= alpha:
                            break
            return max_score
        else:
            # Minimizing player (opponent)
            min_score = math.inf
            for row in range(board.rows):
                for col in range(board.cols):
                    if board.is_square_available(row, col):
                        # Make move
                        board.board[row][col] = current_player

                        # Recursive call
                        score = self._minimax(board, depth + 1, depth_limit, True, opponent, alpha, beta)

                        # Undo move
                        board.board[row][col] = None

                        # Update min score
                        min_score = min(score, min_score)

                        # Alpha-beta pruning
                        beta = min(beta, min_score)
                        if beta <= alpha:
                            break
            return min_score

    def _copy_board(self, board):
        """Creates a copy of the board"""
        from components.board import Board
        board_copy = Board(board.rows, board.cols)
        for row in range(board.rows):
            for col in range(board.cols):
                board_copy.board[row][col] = board.board[row][col]
        return board_copy

    def _check_winner(self, board):
        """Check if there is a winner and return the winner's symbol"""
        # Check rows
        for row in range(board.rows):
            if board.board[row][0] == board.board[row][1] == board.board[row][2] and board.board[row][0] is not None:
                return board.board[row][0]

        # Check columns
        for col in range(board.cols):
            if board.board[0][col] == board.board[1][col] == board.board[2][col] and board.board[0][col] is not None:
                return board.board[0][col]

        # Check diagonal (top-left to bottom-right)
        if board.board[0][0] == board.board[1][1] == board.board[2][2] and board.board[0][0] is not None:
            return board.board[0][0]

        # Check diagonal (top-right to bottom-left)
        if board.board[0][2] == board.board[1][1] == board.board[2][0] and board.board[0][2] is not None:
            return board.board[0][2]
        return None

    def _is_board_full(self, board):
        """Check if the board is full"""
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] is None:
                    return False
        return True