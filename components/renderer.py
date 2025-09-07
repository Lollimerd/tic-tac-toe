import pygame
from utils.constants import *
from Ai_player import ai_player


class Renderer:
    """All visual elements and UI rendering"""

    def __init__(self, screen):
        self.screen = screen

        # Set up fonts
        pygame.font.init()
        self.main_font = pygame.font.SysFont('Arial', 60)
        self.small_font = pygame.font.SysFont('Arial', 30)
        self.info_font = pygame.font.SysFont('Arial', 20)

    def draw_board_lines(self):
        """Draw the grid lines for the board"""
        # Horizontal lines
        pygame.draw.line(self.screen,
                         LINE_COLOR,
                         (0, SQUARE_SIZE),
                         (WIDTH, SQUARE_SIZE),
                         LINE_WIDTH)
        pygame.draw.line(self.screen,
                         LINE_COLOR,
                         (0, 2 * SQUARE_SIZE),
                         (WIDTH, 2 * SQUARE_SIZE),
                         LINE_WIDTH)

        # Vertical lines
        pygame.draw.line(self.screen,
                         LINE_COLOR,
                         (SQUARE_SIZE, 0),
                         (SQUARE_SIZE, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(self.screen,
                         LINE_COLOR,
                         (2 * SQUARE_SIZE, 0),
                         (2 * SQUARE_SIZE, HEIGHT),
                         LINE_WIDTH)

    def draw_figures(self, board):
        """Draw X's and O's on the board"""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board.board[row][col] == 'X':
                    # Draw X
                    pygame.draw.line(self.screen,
                                     CROSS_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                     ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                                     CROSS_WIDTH
                                     )
                    pygame.draw.line(self.screen,
                                     CROSS_COLOR,
                                     ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                     (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                                     CROSS_WIDTH
                                     )
                elif board.board[row][col] == 'O':
                    # Draw O
                    pygame.draw.circle(self.screen,
                                       CIRCLE_COLOR,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       CIRCLE_RADIUS,
                                       CIRCLE_WIDTH
                                       )

    def draw_winning_line(self, winning_line):
        """Draw the winning line"""
        if winning_line:
            pygame.draw.line(
                self.screen,
                WIN_COLOR,
                winning_line[0],
                winning_line[1],
                WIN_LINE_WIDTH
            )

    def draw_game_info(self, game_logic):
        """Draw game information at the bottom of the screen"""
        # Create a semi-transparent bar at the bottom
        info_bar = pygame.Surface((WIDTH, 40), pygame.SRCALPHA)
        info_bar.fill((0, 0, 0, 100))
        self.screen.blit(info_bar, (0, HEIGHT - 40))

        # Display game mode
        mode_text = "Player vs Player" if game_logic.game_mode == "PVP" else "Player vs Computer"

        # Add difficulty level if in PVC mode
        if game_logic.game_mode == "PVC":
            difficulty = "Easy"
            if game_logic.ai_player.difficulty == ai_player.MEDIUM:
                difficulty = "Medium"
            elif game_logic.ai_player.difficulty == ai_player.HARD:
                difficulty = "Hard"
            mode_text += f" ({difficulty})"

        # Display text
        mode_surface = self.info_font.render(mode_text, True, TEXT_COLOR)
        self.screen.blit(mode_surface, (10, HEIGHT - 30))

        # Display current player if game is not over
        if not game_logic.is_game_over():
            turn_text = f"Current turn: Player {game_logic.get_current_player()}"
            turn_surface = self.info_font.render(turn_text, True, TEXT_COLOR)
            self.screen.blit(turn_surface, (WIDTH - turn_surface.get_width() - 10, HEIGHT - 30))

    def draw_winner_overlay(self, winner, game_mode):
        """Draw the semi-transparent overlay with winner text"""
        # Create a new surface with per-pixel alpha
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_BG_COLOR)  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        # Draw the winner text
        if winner == "Draw":
            text = self.main_font.render("Draw!", True, TEXT_COLOR)
        elif winner == "X":
            text = self.main_font.render("Player X wins!", True, TEXT_COLOR)
        else:  # O wins
            if game_mode == "PVP":
                text = self.main_font.render("Player O wins!", True, TEXT_COLOR)
            else:
                text = self.main_font.render("Computer wins!", True, TEXT_COLOR)

        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        self.screen.blit(text, text_rect)

        # Draw restart instruction
        restart_text = self.small_font.render("Press 'R' to restart", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)

        # Draw menu instruction
        menu_text = self.small_font.render("Press 'M' to return to menu", True, TEXT_COLOR)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        self.screen.blit(menu_text, menu_rect)

        # Draw quit instruction
        quit_text = self.small_font.render("Press 'Q' to quit", True, TEXT_COLOR)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        self.screen.blit(quit_text, quit_rect)

    def render_game(self, game_logic):
        """Render the full game state"""
        # Clear screen
        self.screen.fill(BG_COLOR)

        # Draw board lines
        self.draw_board_lines()

        # Draw X's and O's
        self.draw_figures(game_logic.get_board())

        # Draw game info
        self.draw_game_info(game_logic)

        # Draw winning line if game is over and there's a winner
        if game_logic.is_game_over() and game_logic.get_winner() != "Draw":
            self.draw_winning_line(game_logic.get_board().get_winning_line())

        # Draw overlay if game is over
        if game_logic.is_game_over():
            self.draw_winner_overlay(game_logic.get_winner(), game_logic.game_mode)

        # Update display
        pygame.display.update()