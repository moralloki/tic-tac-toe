#!/bin/env python3
# Simple pygame program

# Import and initialize the pygame library
import TicTacToe
import pygame
from pygame.locals import MOUSEBUTTONUP


def draw_circle(screen, rect):
    radius = 35
    thickness = 3
    pygame.draw.circle(screen, BLACK, rect.center, radius, thickness)
    pygame.display.update()


def draw_x(screen, rect):
    buffer = 20
    thickness = 5
    pygame.draw.line(
        screen,
        BLACK,
        (rect.left+buffer, rect.top+buffer),
        (rect.right-buffer, rect.bottom-buffer),
        thickness
    )
    pygame.draw.line(
        screen,
        BLACK,
        (rect.left+buffer, rect.bottom-buffer),
        (rect.right-buffer, rect.top+buffer),
        thickness
    )
    pygame.display.update()


def claim_square(screen, rect, marker):
    if marker.lower() == 'x':
        draw_x(screen, rect)
    elif marker.lower() == 'o':
        draw_circle(screen, rect)
    else:
        raise ValueError


def draw_board(screen, thickness):
    # Fill the background with white
    screen.fill(WHITE)

    # Draw a Tic-Tac-Toe board
    pygame.draw.line(screen, BLACK, (200, 100),
                     (200, 400), thickness)
    pygame.draw.line(screen, BLACK, (300, 100),
                     (300, 400), thickness)
    pygame.draw.line(screen, BLACK, (100, 200),
                     (400, 200), thickness)
    pygame.draw.line(screen, BLACK, (100, 300),
                     (400, 300), thickness)
    pygame.display.update()


def main():
    # Set up some global variables
    global board_line_thickness, rects, WHITE, BLACK

    CANVAS_HEIGHT = 500
    CANVAS_WIDTH = 500
    board_line_thickness = 5
    rects = [
        pygame.Rect((100, 100), (98, 98)),
        pygame.Rect((202, 100), (98, 98)),
        pygame.Rect((302, 100), (98, 98)),
        pygame.Rect((100, 202), (98, 98)),
        pygame.Rect((202, 202), (98, 98)),
        pygame.Rect((302, 202), (98, 98)),
        pygame.Rect((100, 302), (98, 98)),
        pygame.Rect((202, 302), (98, 98)),
        pygame.Rect((302, 302), (98, 98)),
    ]
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Initialize pygame?
    # pygame.init()
    board = TicTacToe.TicTacToe()
    print(board)

    # Set up the drawing window
    screen = pygame.display.set_mode([CANVAS_WIDTH, CANVAS_HEIGHT])

    draw_board(screen, board_line_thickness)

    # Run until the user asks to quit
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                running = False
            # Did the user click in a board spot?
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #logger.debug("Clicked at: {}".format(pos))
                if not game_over:
                    for index, rect in enumerate(rects, start=1):
                        if rect.collidepoint(pos) and board.space_is_free(index):
                            #logger.info("Working in rect: {}".format(rect))
                            claim_square(screen, rect, board.current_player())
                            board.update_board(index)
                            # Check for a win/tie here
                            winning_marker = board.winner()
                            if winning_marker:
                                print(f"{winning_marker.upper()} wins!")
                                game_over = True
                            print(board)

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
