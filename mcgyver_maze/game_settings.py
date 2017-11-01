import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_ROOT_PATH = os.path.abspath(os.path.join(ROOT_PATH, os.pardir))

print(PARENT_ROOT_PATH)


""" Window constants"""
SPRITE_SIZE = 30
NB_SPRITES = 15
WINDOW_SIDE = SPRITE_SIZE * NB_SPRITES
WINDOW_TITLE = "McGyver Maze"
WINDOW_TITLE_IN_GAME = "McGyver Maze | *PLAYING*"
INV_WIDTH = WINDOW_SIDE // 2
INV_HEIGHT = WINDOW_SIDE // 4


""" Sprites constants """
ICON_IMG = "../resources/img/macgyver.png"
MENU_IMG = "../resources/img/menu.png"
CONTROLS_IMG = "../resources/img/controls.png"
WALL_IMG = "../resources/img/wall_tile.png"
FLOOR_IMG = "../resources/img/floor_tile.png"

ITEMS_SPRITES = {
    "ether": "../resources/img/ether.png",
    "needle": "../resources/img/needle.png",
    "tube": "../resources/img/tube.png",
}

DECORS = {
    "wall": "../resources/img/wall_tile.png",
    "floor": "../resources/img/floor_tile.png",
}


""" Playable characters constants """
HEROES = {
    "mcgyver": "../resources/img/macgyver.png"
}


""" NPCS constants """
NPCS = {
    "guardian": "../resources/img/guardian.png"
}


""" Maps constants """
MAP = "../resources/map/map1.txt"
WALLS_MAP_NAME = "m"
FLOOR_MAP_NAME = "f"
