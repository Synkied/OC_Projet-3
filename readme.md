# McGyver maze

A simple python game made for my OpenClassrooms' Python developer course.

## The game

The game requires python3.5+ and pygame to be installed. 
To start the game, go in the "mcgyver_maze" folder and run "python main.py" or "python3 main.py" in a terminal.

In order to win, McGyver needs to collect a needle, a tube and some ether in order to craft a syringe and put the guardian to sleep.

## Controls

* Arrows to move around
* Tab to display the inventory
* Space to display controls while in menu 
* Escape to quit

## Settings

To change the settings, edit game_settings.py. You may edit the following attributes:

        SPRITE_SIZE: The size of the sprites
        NB_SPRITES: The number of sprites to display
        INV_WIDTH and INV_HEIGHT: The width and height of the inventory window
        ITEMS_SPRITES: Add or remove items.
        MAP: Name of the file where the map is located
        WALLS_MAP_NAME/FLOOR_MAP_NAME: The alphanum character that represents a wall/floor in the map file
        Everyting under "Sprites constants", paths to image files of game's items.
