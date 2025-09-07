import pygame
import sys
from utils.constants import *
from components.game_logic import GameLogic
from components.renderer import Renderer
from Ai_player import ai_player

def show_menu(screen, renderer, game_logic):
    """Show the main menu and handle menu selections"""
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 50)
    option_font = pygame.font.SysFont('Arial', 30)

    title_text = title_font.render("Tic Tac Toe", True, TEXT_COLOR)
    pvp_text = option_font.render("1. Player vs Player", True, TEXT_COLOR)
    pvc_easy_text = option_font.render("2. Player vs Computer (Easy)", True, TEXT_COLOR)
    pvc_medium_text = option_font.render("3. Player vs Computer (Medium)", True, TEXT_COLOR)
    pvc_hard_text = option_font.render("4. Player vs Computer (Hard)", True, TEXT_COLOR)
    quit_text = option_font.render("5. Quit", True, TEXT_COLOR)

    # Calculate positions
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    pvp_rect = pvp_text.get_rect(center=(WIDTH // 2, HEIGHT // 6 + 80))
    pvc_easy_rect = pvc_easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 6 + 130))
    pvc_medium_rect = pvc_medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 6 + 180))
    pvc_hard_rect = pvc_hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 6 + 230))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 6 + 280))

    # Menu loop
    while True:

        # Clear screen
        screen.fill(BG_COLOR)

        # Draw menu items
        screen.blit(title_text, title_rect)
        screen.blit(pvp_text, pvp_rect)
        screen.blit(pvc_easy_text, pvc_easy_rect)
        screen.blit(pvc_medium_text, pvc_medium_rect)
        screen.blit(pvc_hard_text, pvc_hard_rect)
        screen.blit(quit_text, quit_rect)

        # Update display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_logic.set_game_mode("PVP")
                    game_logic.reset_game()
                    return "GAME"
                elif event.key == pygame.K_2:
                    game_logic.set_game_mode("PVC", ai_player.EASY)
                    game_logic.reset_game()
                    return "GAME"
                elif event.key == pygame.K_3:
                    game_logic.set_game_mode("PVC", ai_player.MEDIUM)
                    game_logic.reset_game()
                    return "GAME"
                elif event.key == pygame.K_4:
                    game_logic.set_game_mode("PVC", ai_player.HARD)
                    game_logic.reset_game()
                    return "GAME"
                elif event.key == pygame.K_5:
                    return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pvp_rect.collidepoint(mouse_pos):
                    game_logic.set_game_mode("PVP")
                    game_logic.reset_game()
                    return "GAME"
                elif pvc_easy_rect.collidepoint(mouse_pos):
                    game_logic.set_game_mode("PVC", ai_player.EASY)
                    game_logic.reset_game()
                    return "GAME"
                elif pvc_medium_rect.collidepoint(mouse_pos):
                    game_logic.set_game_mode("PVC", ai_player.MEDIUM)
                    game_logic.reset_game()
                    return "GAME"
                elif pvc_hard_rect.collidepoint(mouse_pos):
                    game_logic.set_game_mode("PVC", ai_player.HARD)
                    game_logic.reset_game()
                    return "GAME"
                elif quit_rect.collidepoint(mouse_pos):
                    return "QUIT"

def run_game(screen, renderer, game_logic):
    """Run the main game loop"""
    # Initial render
    renderer.render_game(game_logic)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN and not game_logic.is_game_over():
                mouseX = event.pos[0]  # x coordinate
                mouseY = event.pos[1]  # y coordinate

                # Get clicked row and column
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                # Make move
                if game_logic.make_move(clicked_row, clicked_col):
                    # Re-render the game if move was valid
                    renderer.render_game(game_logic)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    game_logic.reset_game()
                    renderer.render_game(game_logic)

                elif event.key == pygame.K_m or (game_logic.is_game_over() and event.key == pygame.K_RETURN):
                    # Return to menu
                    return "MENU"

                elif event.key == pygame.K_q:
                    # Quit game
                    return "QUIT"

        # Re-render if needed for AI moves
        if game_logic.game_mode == "PVC" and game_logic.current_player == 'O' and not game_logic.is_game_over():
            renderer.render_game(game_logic)

def main():
    # Initialize pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Tic Tac Toe')

    # Initialize game components
    game_logic = GameLogic()
    renderer = Renderer(screen)

    # Initial state is menu
    current_state = "MENU"

    # Main game loop
    while True:
        if current_state == "MENU":
            current_state = show_menu(screen, renderer, game_logic)
        elif current_state == "GAME":
            current_state = run_game(screen, renderer, game_logic)
        elif current_state == "QUIT":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()