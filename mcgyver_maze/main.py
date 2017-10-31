"""
Game: McGyver maze
Creator: Quentin Lathiere

The game is all about McGyver struggling to find 3 items,
in order to put a guard to sleep and escape the maze.

Python scripts used:
mcgyver_maze.py
constants.py
classes.py
"""

import pygame
from pygame.locals import *
from game_settings import *
from core import *

# ===========================
#      Initialize pygame
# ===========================
# initialize pygame and fonts
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 60)
# problem sur mac

# set window size
window = pygame.display.set_mode((WINDOW_SIDE, WINDOW_SIDE))

# icon settings
icon = pygame.image.load(ICON_IMG).convert_alpha()
pygame.display.set_icon(icon)

# window title setting
pygame.display.set_caption(WINDOW_TITLE)


# ===========================
#    Initialize the game
# ===========================
def launch_game():
    continue_game = True
    while continue_game:
        # set the background img
        menu_bckgrd = pygame.image.load(MENU_IMG).convert()

        # display the background img
        window.blit(menu_bckgrd, (0, 0))

        # update the window to display contents
        pygame.display.flip()

        # set loops to True
        in_menu = True
        in_game = True

        # ===========================
        #       In menu actions
        # ===========================
        while in_menu:
            for event in pygame.event.get():
                # quiting the game
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    continue_game, in_game, in_menu = False, False, False

                # launching the game or viewing controls
                elif event.type == KEYDOWN:
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        in_menu = False

        # creating and displaying the map
        mcgy_maze = Level(MAP)

        # creating character and NPC inst.
        mcgyver = Character(mcgy_maze)
        guardian = NPC(mcgy_maze, "GUARDIAN_CHAR")

        # ===========================
        #       In game actions
        # ===========================
        while in_game:
            pygame.time.Clock().tick(30)

            # change the window's title while in game
            pygame.display.set_caption(WINDOW_TITLE_IN_GAME)

            # gets currently pressed keys
            key_pressed = pygame.key.get_pressed()

            # listening for all type of events
            for event in pygame.event.get():

                # quiting the game
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    continue_game, in_game, in_menu = False, False, False
                    # in_game = False

                # listening for KEYDOWN events every frames
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        mcgyver.move("right")
                    if event.key == K_LEFT:
                        mcgyver.move("left")
                    if event.key == K_UP:
                        mcgyver.move("up")
                    if event.key == K_DOWN:
                        mcgyver.move("down")

            mcgy_maze.display_lvl(window)
            guardian.display(window)
            mcgyver.display(window)

            # display the inventory when tab key is pressed
            if key_pressed[K_TAB]:
                mcgyver._show_inventory(window)

            # If mcgyver position is equal to the guardian position,
            # change in_game and in_menu bools and display a message
            if mcgyver.position(mcgy_maze) == guardian.position(mcgy_maze):
                in_game, in_menu = mcgyver.check_inventory(guardian, window)

            # refreshing the window
            pygame.display.flip()


if __name__ == "__main__":
    launch_game()